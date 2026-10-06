# NewWorldOrder – WASM Scripting Guide

Last updated: 2026-09-28

WASM scripting lets mods execute sandboxed logic in response to game events without shipping managed DLLs.
The host runtime calls into a WASM module via the `ModHookBus` event system.

---

## 1. Architecture Overview

```
Game ECS Systems
     │  EnqueueXxx()
     ▼
ModHookBus (ConcurrentQueue<ModHookEvent>)
     │  dispatched each frame by ModHookDispatchSystem (main thread)
     ▼
WASM Host (ModWasmHost)             C# event delegates
     │  calls exported functions          │
     ▼                                    ▼
WASM module (your mod .wasm)        C# mod code (Mods/ assembly)
```

By default the WASM host and C# event delegates are both consumers of the same hooks. With `runtimePolicy` `"coexist"` (the default), a mod's WASM module and its managed DLLs are both loaded, and each is called for the hooks it handles. Set `runtimePolicy` in `mod.json` to run only one of them (see §2.1 of the [Modding Reference](./MODDING_REFERENCE.md)):

- `"csharp_only"` — the mod's WASM module is not loaded.
- `"wasm_only"` — the mod's managed DLLs are not loaded. If C# hook subscribers are already registered (by any mod), the WASM host does not subscribe at all and reports a load error.

---

## 2. WASM ABI Version

Set `wasmAbiVersion` in `mod.json`:
```json
{ "wasmAbiVersion": 3 }
```

The host currently accepts ABI versions **1** through **3**. ABI **3** is the current version for new mods.

**ABI 3 additions:** `on_province_captured`, `on_alliance_formed`, `on_alliance_broken`, `on_economy_tick`, `on_trade_agreement_signed`.

---

## 3. Exported Functions (your WASM must export)

The host calls these functions if they are exported. All are optional. The table after the listing says exactly when the game calls each one.

```wat
;; Called once, right after the module loads
(func $on_init (export "on_init"))

;; Called each game tick
(func $on_game_tick (export "on_game_tick")
  (param $tick i32) (param $year i32) (param $month i32))

;; Called when a war is declared
(func $on_war_declared (export "on_war_declared")
  (param $attacker i32) (param $defender i32) (param $tick i32))

;; Called when peace is signed
(func $on_peace_signed (export "on_peace_signed")
  (param $proposer i32) (param $target i32))

;; Called when a tech is researched
(func $on_tech_researched (export "on_tech_researched")
  (param $country i32) (param $tech_index i32))

;; Called when a building is completed
(func $on_building_completed (export "on_building_completed")
  (param $province_id i32) (param $building_def i32))

;; Called when an event is queued for a country
(func $on_event_fired (export "on_event_fired")
  (param $country i32) (param $event_index i32))

;; Called when a country is eliminated
(func $on_country_eliminated (export "on_country_eliminated")
  (param $country i32))

;; Called when a mod UI button is clicked (hook_name and mod_id are UTF-8 strings in WASM memory)
(func $on_ui_action (export "on_ui_action")
  (param $hook_name_ptr i32) (param $hook_name_len i32)
  (param $mod_id_ptr i32)    (param $mod_id_len i32))

;; ── ABI 3 additions ──────────────────────────────────────────────────────

;; Called when a province changes owner: a peace deal, or an annex_province /
;; annex_country event effect (once per province). A military capture changes
;; only control, not the owner, and does not call it.
;; province_id = map province ID; new_owner / old_owner = country indices
(func $on_province_captured (export "on_province_captured")
  (param $province_id i32) (param $new_owner i32) (param $old_owner i32))

;; Called when two countries form an alliance
(func $on_alliance_formed (export "on_alliance_formed")
  (param $country1 i32) (param $country2 i32))

;; Called when an existing alliance is broken
(func $on_alliance_broken (export "on_alliance_broken")
  (param $country1 i32) (param $country2 i32))

;; Called once per economy tick (roughly monthly)
(func $on_economy_tick (export "on_economy_tick")
  (param $year i32) (param $month i32))

;; Called when a bilateral trade agreement is signed
(func $on_trade_agreement_signed (export "on_trade_agreement_signed")
  (param $country1 i32) (param $country2 i32))
```

**When each hook runs.** Country arguments are country handles: pass them straight back to the imports in §4. Hooks run on the main thread. Every hook except `on_ui_action` (below) is raised by the simulation, on every player's game. This table lists every export the host looks for; an EditMode test (`WasmScriptingDocsParityTests`) fails when it and the host drift apart.

<!-- parity:hook-exports:begin -->
| Export | Arguments | When the game calls it |
|---|---|---|
| `on_init` | none | Once, right after the module loads. The game world may not exist yet, so don't read game state here. |
| `on_game_tick` | tick, year, month | Once per game tick (one in-game day). At high speed several ticks can pass in one frame; each gets its own call. |
| `on_war_declared` | attacker, defender, tick | A country declares war on another. |
| `on_peace_signed` | proposer, target | A peace deal is signed. |
| `on_tech_researched` | country, tech_index | A country completes a doctrine tier (Knowledge Network). `tech_index` is the tier's gate bit: branch × 5 + (tier − 1). |
| `on_building_completed` | province_id, building_def | A new building finishes, on the monthly economy tick where construction completes. Upgrades of an existing building are not reported. `building_def` is the building's index in this game's building table. |
| `on_country_eliminated` | country | A country is eliminated. |
| `on_event_fired` | country, event_index | An event is queued for a country: a monthly roll or reactive trigger, a chain that comes due, or a script's `fire_event`. `event_index` is the event's index in this game's event table. Raised once per queued event; the choice made later does not raise it again, and the same event queued again later (after the choice) raises it again. |
| `on_ui_action` | hook_name, mod_id | A button injected by a mod is clicked. Both arguments are UTF-8 strings in your memory. |
| `on_province_captured` | province_id, new_owner, old_owner | A province changes owner through a peace deal's transfer or an `annex_province` / `annex_country` event effect: once per province. Occupation in a war changes only who controls a province, not who owns it, so it does not raise this hook. |
| `on_alliance_formed` | country1, country2 | An alliance is formed, by the player or the AI. `country1` proposed it. |
| `on_alliance_broken` | country1, country2 | A bilateral alliance ends: one side breaks it (player or AI), one ally declares war on the other, or the player dishonours a call to arms (declines it or lets it expire). `country1` is the side that ended it. An alliance that ends because a country was eliminated raises only `on_country_eliminated`. |
| `on_economy_tick` | year, month | Once per monthly economy tick. |
| `on_trade_agreement_signed` | country1, country2 | A trade agreement is signed. `country1` proposed it. |
<!-- parity:hook-exports:end -->

**`on_ui_action` in multiplayer.** A button click runs `on_ui_action` on the clicking player's game only. Every other hook is raised by the simulation and runs the same way on every player's game. So in a multiplayer session, calls made from `on_ui_action` that would change the game are refused: `country_set_treasury`, `add_treasury`, `fire_event` and `fire_trigger` (and, for C# mods, the same writes through `ModHookBus` / `ModGameActionRequest`, including country flags). Each mod gets one warning in the log. `show_mod_popup` and `log` still work, because they only affect the local screen. Changes to the game must come from sim hooks such as `on_game_tick` or `on_economy_tick`. Don't store the click and apply it later from a sim hook: the stored click exists on one player's game only, so the sessions would still drift apart. Single-player is not affected; there, `on_ui_action` can change the game as before.

---

## 4. Imported Functions (host provides to WASM)

Your module imports these functions from the `gp` module. The tables list every import the game provides, no more and no fewer: an EditMode test (`WasmScriptingDocsParityTests`) compares them with the host's import tables and fails when they drift apart.

A country argument is a country handle, as the hooks pass it. A handle that names no country reads as 0 and turns a write into a no-op. Money is in US dollars, the unit of `treasury` and `gdp` in §4.3 of the [Modding Reference](./MODDING_REFERENCE.md). Stability runs from 0 to 100.

**Core modules (the default runtime).** The signature column uses wasm3's `ret(args)` notation: `i` = i32, `I` = i64, `f` = f32, `F` = f64, `v` = no result. Declare an import with exactly one of the signatures listed for it; any other signature fails to link, and the mod browser shows a load error that names the import.

<!-- parity:wasm3-imports:begin -->
| Import | Signature | Arguments → result | Permission |
|---|---|---|---|
| `log` | `v(ii)` | (msg_ptr, msg_len): writes a UTF-8 message to the log | none |
| `get_tick` | `i()` | → the current game tick | none |
| `get_year` | `i()` | → the current year | none |
| `get_month` | `i()` | → the current month, 1–12 | none |
| `country_get_gdp` | `F(i)` | (country) → annual GDP | none |
| `country_get_treasury` | `F(i)` | (country) → treasury | none |
| `country_set_treasury` | `v(iF)` | (country, value): sets the treasury to value | `WriteTreasury` |
| `country_get_stability` | `f(i)` | (country) → stability | none |
| `country_get_tech_level` | `i(i)` | (country) → number of completed doctrine tiers | none |
| `fire_event` | `v(iii)` | (country, id_ptr, id_len): queues an event by id (see below) | `FireTriggers` |
| `show_mod_popup` | `v(iiii)` | (title_ptr, title_len, body_ptr, body_len): shows a popup (§10) | `InjectUI` |
| `log_string` | `v(i)` | Older name. Logs a fixed line and ignores its argument; use `log`. | none |
| `get_current_tick` | `i()` | Older name of `get_tick` | none |
| `get_current_year` | `i()` | Older name of `get_year` | none |
| `get_current_month` | `i()` | Older name of `get_month` | none |
| `get_country_gdp` | `f(i)` | Older 32-bit form of `country_get_gdp` | none |
| `get_country_treasury` | `f(i)` | Older 32-bit form of `country_get_treasury` | none |
| `get_country_stability` | `f(i)` | Older name of `country_get_stability` | none |
| `get_country_manpower` | `I(i)` | (country) → available manpower, in people | none |
| `get_country_manpower` | `i(i)` | Older 32-bit form of the above, capped at the i32 range | none |
| `add_treasury` | `v(if)` | (country, amount): adds amount to the treasury | `WriteTreasury` |
| `fire_trigger` | `v(iii)` | (trigger_type, source, target): raises a reactive event trigger between two countries | `FireTriggers` |
<!-- parity:wasm3-imports:end -->

**Component-model binaries** (opt-in, §8) import the same functions from the `gp` interface, by these names. Strings are component `string` values instead of `(ptr, len)` pairs. `country-get-gdp` and `country-get-treasury` return f64 under every name listed for them, and `get_country_manpower` returns s64.

<!-- parity:component-imports:begin -->
| Function | Also accepted as |
|---|---|
| `log` | |
| `log_string` | |
| `get-tick` | `get_tick`, `get_current_tick` |
| `get-year` | `get_year`, `get_current_year` |
| `get-month` | `get_month`, `get_current_month` |
| `country-get-gdp` | `get_country_gdp` |
| `country-get-treasury` | `get_country_treasury` |
| `country-set-treasury` | `country_set_treasury` |
| `country-get-stability` | `get_country_stability` |
| `country-get-tech-level` | `country_get_tech_level` |
| `get_country_manpower` | |
| `add-treasury` | `add_treasury` |
| `fire-trigger` | `fire_trigger` |
| `fire-event` | `fire_event` |
| `show-mod-popup` | `show_mod_popup` |
<!-- parity:component-imports:end -->

Strings passed to a core module's imports are `(ptr, len)` pairs pointing into the module's linear memory, UTF-8, not null-terminated.

`fire_event` looks the id up among the base game's events and the engine events of every active mod: `Content/events/*.json` objects with a `type` field, which the game adds to the event table at game start (see §8.7 of the [Modding Reference](./MODDING_REFERENCE.md)). A match goes straight into that country's event queue, through the normal event pipeline: popup or AI choice, effects, chains and saves.

The script decides when the event fires, so the event's own conditions and cooldowns are **not** checked. Two rules still apply: a `target: "player"` event is refused for a country no human controls, and a `fire_once` event is refused once it has fired (or while it is still pending); the same event is never queued twice for one country. If the id is not an engine event, a legacy event (no `type`) with that id is shown as a popup whose buttons just close it. An unknown id is ignored, with a one-time warning in the log.

An engine event queued this way raises `on_event_fired` (§3) like any other queued event, for every mod that exports it, including the one that fired it.

---

## 5. Memory Model

- The host allocates no memory inside the WASM module. All buffers are owned by the WASM module.
- For strings returned **to** the host (e.g. event IDs), write the UTF-8 bytes into WASM linear memory and pass the pointer + length to the import function.
- The host does not call `free` — manage memory in your module's allocator.
- The host checks every `(ptr, len)` pair against your module's linear memory before reading it. A string that falls outside that memory (or has a negative pointer or length) is ignored, with a one-time warning in the log. The host reads at most 64 KB of any one string.

---

## 6. Permissions in WASM

Declare permissions in `mod.json` (§7 of the [Modding Reference](./MODDING_REFERENCE.md)); each can be written in PascalCase (`WriteTreasury`) or snake_case (`write_treasury`). A call that needs a permission the mod did not declare does nothing. `fire_event` and `show_mod_popup` also write a warning to the log. The same checks apply to C# mods.

| Permission | What it allows |
|---|---|
| `WriteTreasury` | `country_set_treasury`, `add_treasury`; C#: `ModGameActionRequest.AddTreasuryDelta` |
| `FireTriggers` | `fire_event`, `fire_trigger`; C#: `ModHookBus.FireEvent`, `ModGameActionRequest.FireEventTrigger` / `FireEventDirectById` |
| `InjectUI` | `show_mod_popup`, and the mod's `inject.json` UI; C#: `ModHookBus.ShowPopup` |
| `ReadEconomy` | Nothing yet. Every read import (`country_get_*`, `get_*`) works without a permission. The game accepts `ReadEconomy` so existing manifests stay valid. |
| `WriteFlags` | No WASM import yet. C# mods that reference the `GlobalProtocol.ECS` assembly: `ModGameActionRequest.SetCountryFlag` / `ClearCountryFlag`, a country's event flags (the ones `has_flag` conditions test). |

---

## 7. Example: AssemblyScript Mod

```typescript
// mod.ts (AssemblyScript)
import {
  country_get_treasury,
  country_set_treasury,
  log,
} from "gp";

export function on_war_declared(attacker: i32, defender: i32, tick: i32): void {
  const treasury = country_get_treasury(attacker); // US dollars
  if (treasury < 5.0e9) {
    log_str("Attacker is broke — boosting treasury");
    country_set_treasury(attacker, treasury + 1.0e10); // needs WriteTreasury
  }
}

function log_str(msg: string): void {
  const encoded = String.UTF8.encode(msg);
  log(changetype<i32>(encoded), encoded.byteLength);
}
```

Compile with `asc mod.ts -o mod.wasm --runtime stub`.

---

## 8. Registering a WASM Module

Place `mod.wasm` under the mod's `Content/` directory and reference it in `mod.json`:
```json
{
  "entrypoints": {
    "wasm": "Content/mod.wasm"
  }
}
```

The loader resolves `entrypoints.wasm` first. If that manifest path is missing or unresolved, it falls back to the legacy `scripts/main.wasm` path for compatibility.

The game validates the ABI version at load time and rejects mismatches with a clear error in the mod browser.

Core WebAssembly binaries are supported by the default runtime path.

Component-model binaries require explicit opt-in plus game runtime support:
- In your `mod.json`, set `"enableComponentRuntime": true`.
- The game must have component runtime integration enabled by configuration.
- The game must have a registered component backend implementation.

If any of those conditions is missing, the mod shows a clear load error and the binary is not loaded.

**Multiplayer.** The module the loader picks (`entrypoints.wasm`, or `scripts/main.wasm`) and every `Mods/*.dll` are part of the multiplayer lobby check. Players whose script files differ in any byte can't join the same game, even when the mod's id and version match.

---

## 9. Debugging

- `log()` messages go to the Unity console in the editor and to `Player.log` in a built game, prefixed with `[Mod:<your mod id>]`.
- Load and link errors (a bad ABI version, an import with the wrong signature) show in the mod browser and in the log.
- The game tick, year, and country handles are deterministic — use them as keys into your own mod state tables.

---

## 10. Localization Overrides for Mod Text

Localization is loaded from base game CSV first, then mod overrides are layered on top.

Supported mod paths:
- `Content/localization/en.csv`, `Content/localization/tr.csv`, ...
- `overrides/localization_en.csv`, `overrides/localization_tr.csv`, ...

At runtime, `L10n.Get("your.key")` resolves values from the merged dictionary. If a key is missing, it returns the key string itself.

Recommended pattern for host-side fallback UI text:

```csharp
string text = L10n.Get("mod.example.popup.title");
if (text == "mod.example.popup.title")
  text = "Fallback English title";
```

This lets mods ship translations in override CSV files without requiring extra registration steps.

**Localized popups from a script.** `show_mod_popup` (needs the `inject_ui` permission) takes the title and body as UTF-8 strings:

```wat
(import "gp" "show_mod_popup" (func (param $title_ptr i32) (param $title_len i32) (param $body_ptr i32) (param $body_len i32)))
```

There is no import that looks a key up yet. Instead, a title or body that is **exactly a localization key** (no spaces or commas, with at least one dot inside, e.g. `mymod.popup.intro.title`) is shown as that key's text in the player's language. Any other text is shown as written. C# mods get the same rule through `ModHookBus.ShowPopup(modId, title, body)`. Define the key in all 13 language files (§8.3 of the [Modding Reference](./MODDING_REFERENCE.md)); a player whose language file lacks it, or has it with an empty value, sees the key itself.

---

## 11. Windows Runtime Maintenance

For Windows x64 component runtime upgrades, use the canonical script:

`NewWorldOrder/tools/upgrade-wasmtime-win64.ps1`

Example:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\upgrade-wasmtime-win64.ps1 -Version v44.0.1
```

The script downloads the C API package, validates SHA-256 (for known versions), backs up the current DLL, replaces it, and probes required component symbols.

# NewWorldOrder – WASM Scripting Guide

Last updated: 2026-05-13

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
WASM Host (WasmModuleHost)          C# event delegates
     │  calls exported functions          │
     ▼                                    ▼
WASM module (your mod .wasm)        C# mod code (Mods/ assembly)
```

The WASM host and C# event delegates are mutually exclusive consumers — your mod uses one or the other, not both.

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

The host calls these functions if they are exported. All are optional.

```wat
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

;; Called when a scripted event fires
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

;; Called when a province changes owner (capture, peace deal, etc.)
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

---

## 4. Imported Functions (host provides to WASM)

Your WASM module may `import` these host-provided functions:

```wat
;; Read a country's treasury (returns float64 USD millions)
(import "gp" "country_get_treasury" (func (param $country_index i32) (result f64)))

;; Set a country's treasury (requires WriteTreasury permission)
(import "gp" "country_set_treasury" (func (param $country_index i32) (param $value f64)))

;; Read a country's stability (returns float32, 0..1)
(import "gp" "country_get_stability" (func (param $country_index i32) (result f32)))

;; Read a country's tech level (returns i32)
(import "gp" "country_get_tech_level" (func (param $country_index i32) (result i32)))

;; Request an event by ID for a country (requires FireTriggers permission)
(import "gp" "fire_event" (func (param $country_index i32) (param $event_id_ptr i32) (param $event_id_len i32)))

;; Log a string to the Unity console (debug builds only)
(import "gp" "log" (func (param $msg_ptr i32) (param $msg_len i32)))

;; Get the current game tick
(import "gp" "get_tick" (func (result i32)))

;; Get the current year
(import "gp" "get_year" (func (result i32)))
```

Strings are passed as `(ptr, len)` pairs pointing into the WASM linear memory. Strings from host to WASM are UTF-8, not null-terminated.

`fire_event` is currently a compatibility shim. The host maps a small set of known event IDs onto existing trigger families before dispatching into the ECS event pipeline. Arbitrary event-ID execution is not implemented yet, so mods should not assume full component/modern ABI parity here.

---

## 5. Memory Model

- The host allocates no memory inside the WASM module. All buffers are owned by the WASM module.
- For strings returned **to** the host (e.g. event IDs), write the UTF-8 bytes into WASM linear memory and pass the pointer + length to the import function.
- The host does not call `free` — manage memory in your module's allocator.

---

## 6. Permissions in WASM

Permission checks apply identically to WASM and C# callers. If your module calls `country_set_treasury` without `WriteTreasury` declared in `mod.json`, the call is a no-op and a warning is logged.

Required permissions per import:

| Import | Required Permission |
|---|---|
| `country_get_treasury` | `ReadEconomy` |
| `country_set_treasury` | `WriteTreasury` |
| `country_get_stability` | `ReadEconomy` |
| `fire_event` | `FireTriggers` |

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
  const treasury = country_get_treasury(attacker);
  if (treasury < 500.0) {
    log_str("Attacker is broke — boosting treasury");
    country_set_treasury(attacker, treasury + 1000.0);
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

---

## 9. Debugging

- WASM logs via `log()` appear in the Unity console on development builds.
- On release builds, WASM logs are suppressed.
- The game tick, year, and country indices are deterministic — use them as keys into your own mod state tables.
- Use the in-game Mod Debugger panel (F12 on dev builds) to inspect the hook event queue.

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

---

## 11. Windows Runtime Maintenance

For Windows x64 component runtime upgrades, use the canonical script:

`NewWorldOrder/tools/upgrade-wasmtime-win64.ps1`

Example:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\upgrade-wasmtime-win64.ps1 -Version v44.0.1
```

The script downloads the C API package, validates SHA-256 (for known versions), backs up the current DLL, replaces it, and probes required component symbols.

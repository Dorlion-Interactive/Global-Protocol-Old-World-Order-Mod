# NewWorldOrder – WASM Scripting Guide

Last updated: 2026-10-08

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

**Platforms.** The WASM backends ship for Windows and Linux. macOS has none yet: on a Mac a mod that ships a WASM module loads **data-only**. Its content (events, overrides, scenario, localization) works, its scripts do not run, and the player sees a load warning in the Mods panel. The Mod Builder's Manifest tab and Validate Mod show a note for any mod that ships WASM. Managed (C#) mods are not affected by this.

---

## 2. WASM ABI Version

Set `wasmAbiVersion` in `mod.json`:
```json
{ "wasmAbiVersion": 4 }
```

The host currently accepts ABI versions **1** through **4**. ABI **4** is the current version for new mods. The ABI only grows: every import and export of an older version keeps working, so a script built for ABI 1, 2 or 3 behaves the same under a newer game and needs no change. The version a mod declares decides which imports it may link: a script that imports a function from a newer ABI than its manifest declares fails to load, and the mod browser names the import (stage `link`).

**ABI 3 additions:** `on_province_captured`, `on_alliance_formed`, `on_alliance_broken`, `on_economy_tick`, `on_trade_agreement_signed`.

**ABI 4 additions:**
- Text by key (§4.4): `localize`, `format`, and the popup `show_mod_popup_key` (permission `inject_ui`).
- State writes, permission `flags.write` (§4.3): `country_set_flag`, `country_clear_flag`, `country_set_var`, `country_add_var`, `state_set`, `state_add`.
- World reads, permission `world.read` (§4.2): `state_get`, `country_lifetime`, `country_count`, `country_at`, `country_by_iso3`, `country_iso3`, `country_at_war_with`, `country_allied_with`, `country_war_count`, `country_war_enemy`, `province_owner`, `province_controller`, `country_has_flag`, `country_flag_age_months`, `country_get_var`.
- Hooks `on_espionage_resolved`, `on_game_ended` and `on_reload` (§3).
- End-screen row `register_end_screen_row` (§4.4, permission `inject_ui`).
- Alliance organizations and the world ceasefire, permission `write_diplomacy` (§4.5): `organization_create`, `organization_join`, `organization_leave`, `organization_invite`, `world_ceasefire_start`, `world_ceasefire_end`.

**Saves.** A save made while the active mods declared ABI 4 does not load under mods that declare an older ABI. A save made under an older ABI loads under a newer one.

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

;; ── ABI 4 additions ──────────────────────────────────────────────────────

;; Called when a covert mission reaches an outcome. mission_type: 0 gather
;; intelligence, 1 sabotage economy, 2 sabotage infrastructure, 3 steal
;; technology (the other kinds follow the in-game mission list).
;; state: 1 success, 2 failed, 3 caught.
(func $on_espionage_resolved (export "on_espionage_resolved")
  (param $source i32) (param $target i32) (param $mission_type i32) (param $state i32))

;; Called once when the game ends. victory_type: 1 military hegemony, 2 economic
;; superpower, 3 diplomatic leader, 4 technological ascendancy, 5 nuclear
;; deterrence, 6 one of the scenario's own endings. mod_row: that ending's position
;; among the scenario's accepted endings (-1 for a base victory).
(func $on_game_ended (export "on_game_ended")
  (param $winner i32) (param $victory_type i32) (param $mod_row i32))
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
| `on_economy_tick` | year, month | Once per monthly economy tick. It fires on the same update as the economy tick itself (the month rollover), not one update later. |
| `on_trade_agreement_signed` | country1, country2 | A trade agreement is signed. `country1` proposed it. |
| `on_espionage_resolved` | source, target, mission_type, state | A covert mission reaches an outcome (ABI 4). `source` is the country that ran it, `target` the country it ran against. `mission_type` is the mission kind (0 gather intelligence, 1 sabotage economy, 2 sabotage infrastructure, 3 steal technology, ...); `state` is 1 success, 2 failed, 3 caught. Raised once per mission, in ISO3 order of the acting country when several resolve together. |
| `on_reload` | none | Your module was rebuilt in a running single-player game (the Mod Builder's **APPLY TO RUNNING GAME** after you edited the `.wasm`). Called instead of `on_init`, if you export it. The module's memory and globals are fresh, so rebuild your tables here; what your mod keeps in the game (flags, variables, the `state_*` store) is untouched. If the new module fails to load, the previous one keeps running and the Mod Builder says why. |
| `on_game_ended` | winner, victory_type, mod_row | The game ends, once (ABI 4). `winner` is the winning country's handle. `victory_type` is 1 military hegemony, 2 economic superpower, 3 diplomatic leader, 4 technological ascendancy, 5 nuclear deterrence or 6 one of the scenario's own endings; `mod_row` is that ending's position among the scenario's accepted endings (-1 for a base victory). Not raised again for a game loaded after it ended. |
<!-- parity:hook-exports:end -->

**`on_ui_action` in multiplayer.** A button click runs `on_ui_action` on the clicking player's game only. Every other hook is raised by the simulation and runs the same way on every player's game. So in a multiplayer session, calls made from `on_ui_action` that would change the game are refused: `country_set_treasury`, `add_treasury`, `fire_event`, `fire_trigger`, `country_set_flag`, `country_clear_flag`, `country_set_var`, `country_add_var`, `state_set` and `state_add` (and, for C# mods, the same writes through `ModHookBus`, `IModServices` and `ModGameActionRequest`, including country flags). Each mod gets one warning in the log. `show_mod_popup` and `log` still work, because they only affect the local screen. Changes to the game must come from sim hooks such as `on_game_tick` or `on_economy_tick`. Don't store the click and apply it later from a sim hook: the stored click exists on one player's game only, so the sessions would still drift apart. Single-player is not affected; there, `on_ui_action` can change the game as before.

---

## 4. Imported Functions (host provides to WASM)

### 4.1 The `gp` imports

Your module imports these functions from the `gp` module. The tables list every import the game provides, no more and no fewer: an EditMode test (`WasmScriptingDocsParityTests`) compares them with the host's import tables and fails when they drift apart.

A country argument is a country handle, as the hooks pass it. A handle that names no country reads as 0 (or -1 where the table says so) and turns a write into a no-op. Handles are valid for the current session only; see §4.2 for how to keep a country across a save, and a multiplayer host and follower. Money is in US dollars, the unit of `treasury` and `gdp` in §4.3 of the [Modding Reference](./MODDING_REFERENCE.md). Stability runs from 0 to 100.

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
| `country_count` | `i()` | → number of countries in the directory (§4.2) | `world.read` |
| `country_at` | `i(i)` | (ordinal) → handle of the ordinal-th country in ISO3 order, or -1 | `world.read` |
| `country_by_iso3` | `i(ii)` | (iso3_ptr, iso3_len) → handle, or -1 | `world.read` |
| `country_iso3` | `i(iii)` | (country, out_ptr, cap) → bytes needed, or -1; writes the ISO3 to your buffer (§5) | `world.read` |
| `country_at_war_with` | `i(ii)` | (a, b) → 1 when the two countries are at war, else 0 | `world.read` |
| `country_allied_with` | `i(ii)` | (a, b) → 1 when either holds an alliance toward the other, else 0 | `world.read` |
| `country_war_count` | `i(i)` | (country) → number of countries it is at war with | `world.read` |
| `country_war_enemy` | `i(ii)` | (country, ordinal) → handle of its ordinal-th enemy in ISO3 order, or -1 | `world.read` |
| `province_owner` | `i(i)` | (province_id) → handle of the owning country, or -1 | `world.read` |
| `province_controller` | `i(i)` | (province_id) → handle of whoever holds it now (the occupier, else the owner), or -1 | `world.read` |
| `country_has_flag` | `i(iii)` | (country, name_ptr, name_len) → 1 when the event flag is set, else 0 | `world.read` |
| `country_flag_age_months` | `i(iii)` | (country, name_ptr, name_len) → whole months since the flag was set, 0 for this month, -1 when not set | `world.read` |
| `country_get_var` | `i(iii)` | (country, name_ptr, name_len) → the country's event variable, 0 when never set | `world.read` |
| `country_lifetime` | `I(ii)` | (country, counter) → a lifetime counter of the campaign as an i64: 0 personnel lost, 1 regiments lost, 2 ships lost, 3 aircraft lost, 4 civilians affected, 5 provinces gained, 6 provinces lost, 7 wars won, 8 wars lost (§4.2) | `world.read` |
| `state_get` | `i(ii)` | (key_ptr, key_len) → the mod's own saved state under that key, 0 when never set (§4.3) | `world.read` |
| `country_set_flag` | `i(iii)` | (country, name_ptr, name_len) → 1 when the flag is set afterwards, 0 when refused (§4.3) | `flags.write` |
| `country_clear_flag` | `i(iii)` | (country, name_ptr, name_len) → 1 when the flag was set and is now cleared, else 0 | `flags.write` |
| `country_set_var` | `i(iiii)` | (country, name_ptr, name_len, value) → 1 when applied, 0 when refused | `flags.write` |
| `country_add_var` | `i(iiii)` | (country, name_ptr, name_len, delta) → 1 when applied, 0 when refused | `flags.write` |
| `state_set` | `i(iii)` | (key_ptr, key_len, value) → 1 when applied, 0 when refused (§4.3) | `flags.write` |
| `state_add` | `i(iii)` | (key_ptr, key_len, delta) → 1 when applied, 0 when refused (§4.3) | `flags.write` |
| `localize` | `i(iiii)` | (key_ptr, key_len, out_ptr, cap) → bytes needed, or -1; writes the key's text in the player's language to your buffer (§4.4, §5) | none |
| `format` | `i(iiiiii)` | (key_ptr, key_len, args_ptr, args_len, out_ptr, cap) → bytes needed, or -1; like `localize` with `{0}`, `{1}`... filled from NUL-separated arguments (§4.4) | none |
| `show_mod_popup_key` | `v(iiiiii)` | (title_key_ptr, title_key_len, body_key_ptr, body_key_len, args_ptr, args_len): shows a popup whose title and body are keys, resolved in each player's language (§4.4) | `inject_ui` |
| `register_end_screen_row` | `i(iiii)` | (label_key_ptr, label_key_len, value_ptr, value_len) → 1 when a line was added to the end screen's mod record, else 0. The value says where the number comes from: `lifetime.ships_lost` (a lifetime counter of the player's country), `mod_state.your_key` (this mod's own state) or `variable.your_name` (an event variable of the player's country). Presentation only (§4.4) | `inject_ui` |
| `organization_create` | `i(iiii)` | (id_ptr, id_len, collective_defense, founder) → 1 when the organization was founded with that country as first member, else 0 (§4.5) | `write_diplomacy` |
| `organization_join` | `i(iiii)` | (id_ptr, id_len, country, force) → 1 when the country is a member afterwards, else 0 (§4.5) | `write_diplomacy` |
| `organization_leave` | `i(iii)` | (id_ptr, id_len, country) → 1 when the country left, else 0 (§4.5) | `write_diplomacy` |
| `organization_invite` | `i(iiii)` | (id_ptr, id_len, inviter, target) → 1 when the invitation was made, else 0 (§4.5) | `write_diplomacy` |
| `world_ceasefire_start` | `i(iii)` | (months, until_flag_ptr, until_flag_len) → 1 when the world ceasefire started, else 0; months 0 = no end date, an empty flag = none (§4.5) | `write_diplomacy` |
| `world_ceasefire_end` | `i()` | () → 1 when a ceasefire was running and is now ended, else 0 (§4.5) | `write_diplomacy` |
<!-- parity:wasm3-imports:end -->

**Component-model binaries** (opt-in, §8) import the same functions from the `gp` interface, by these names. Strings are component `string` values instead of `(ptr, len)` pairs. `country-get-gdp` and `country-get-treasury` return f64 under every name listed for them, and `get_country_manpower` returns s64. The ABI-4 world reads and state writes return s32 (truth values are 1 and 0), and the writes take `(s32, string)` or `(s32, string, s32)`; `localize(key: string) -> string`, `format(key: string, args: list<string>) -> string` and `show-mod-popup-key(title-key: string, body-key: string, args: list<string>)` take strings and a string list instead of (ptr, len) pairs; `country-by-iso3` takes a `string`, `country-has-flag`, `country-flag-age-months` and `country-get-var` take `(s32, string)`, and `country-iso3` returns a `string` (empty for an unknown handle).

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
| `country-count` | `country_count` |
| `country-at` | `country_at` |
| `country-by-iso3` | `country_by_iso3` |
| `country-iso3` | `country_iso3` |
| `country-at-war-with` | `country_at_war_with` |
| `country-allied-with` | `country_allied_with` |
| `country-war-count` | `country_war_count` |
| `country-war-enemy` | `country_war_enemy` |
| `province-owner` | `province_owner` |
| `province-controller` | `province_controller` |
| `country-has-flag` | `country_has_flag` |
| `country-flag-age-months` | `country_flag_age_months` |
| `country-get-var` | `country_get_var` |
| `country-lifetime` | `country_lifetime` |
| `state-get` | `state_get` |
| `country-set-flag` | `country_set_flag` |
| `country-clear-flag` | `country_clear_flag` |
| `country-set-var` | `country_set_var` |
| `country-add-var` | `country_add_var` |
| `state-set` | `state_set` |
| `state-add` | `state_add` |
| `localize` | |
| `format` | |
| `show-mod-popup-key` | `show_mod_popup_key` |
| `register-end-screen-row` | `register_end_screen_row` |
| `organization-create` | `organization_create` |
| `organization-join` | `organization_join` |
| `organization-leave` | `organization_leave` |
| `organization-invite` | `organization_invite` |
| `world-ceasefire-start` | `world_ceasefire_start` |
| `world-ceasefire-end` | `world_ceasefire_end` |
<!-- parity:component-imports:end -->

Strings passed to a core module's imports are `(ptr, len)` pairs pointing into the module's linear memory, UTF-8, not null-terminated.

`fire_event` looks the id up among the base game's events and the engine events of every active mod: `Content/events/*.json` objects with a `type` field, which the game adds to the event table at game start (see §8.7 of the [Modding Reference](./MODDING_REFERENCE.md)). A match goes straight into that country's event queue, through the normal event pipeline: popup or AI choice, effects, chains and saves.

The script decides when the event fires, so the event's own conditions and cooldowns are **not** checked. Two rules still apply: a `target: "player"` event is refused for a country no human controls, and a `fire_once` event is refused once it has fired (or while it is still pending); the same event is never queued twice for one country. If the id is not an engine event, a legacy event (no `type`) with that id is shown as a popup whose buttons just close it. An unknown id is ignored, with a one-time warning in the log.

An engine event queued this way raises `on_event_fired` (§3) like any other queued event, for every mod that exports it, including the one that fired it.

### 4.2 World reads (ABI 4, permission `world.read`)

A script declares `"wasmAbiVersion": 4` and `"permissions": ["world.read"]` in `mod.json`. A core module that imports one of these functions without both fails to load (stage `link`, naming the import and what is missing). A component-model script, which cannot be refused at link time, gets the neutral value from the call and one warning in the Mod Builder's Reload & Test and the log. The same reads exist for C# mods on `IModServices` (the same names in PascalCase: `CountryCount`, `CountryAt`, `FindCountry`, `CountryIso3`, `AtWar`, `Allied`, `WarCount`, `WarEnemyAt`, `ProvinceOwner`, `ProvinceController`, `HasFlag`, `FlagAgeMonths`, `GetVariable`; managed SDK 1.1).

**Countries and handles.** `country_count` and `country_at(n)` list the countries of the game (every country that has an ISO3, except those a scenario removed) in **ISO3 order**, the same on every player's game. A handle is the country's index in this session. It is what hooks pass you and what every function above takes, but it differs between a multiplayer host and a follower and between two runs, so **never store a handle**. To remember a country, store its ISO3 (`country_iso3`) or its position `n` and look the handle up again with `country_by_iso3` or `country_at`. A loop `for n in 0..country_count()` visits every country in the same order for every player, which is what keeps a script that writes to the game in step across multiplayer.

**Wars and alliances.** `country_war_enemy(country, n)` lists a country's enemies in ISO3 order, for `n` from 0 to `country_war_count(country) - 1`. `country_allied_with` is true for a bilateral alliance and for two members of the same collective-defence organisation, whichever country holds the row.

**Provinces.** `province_owner` is the legal owner (it changes by peace deal, annexation or a transfer); `province_controller` is whoever holds the province now, which is the occupier while it is occupied. An unknown province id reads -1.

**Flags and variables.** `country_has_flag`, `country_flag_age_months` and `country_get_var` read the same per-country state that events set with `set_flag`, `set_variable` and `change_variable` and test with `has_flag`, `flag_age_months_gt/lt` and `variable_gt/lt/eq`. The name is the exact text used in the event file. A variable that was never set reads 0.

**Lifetime counters.** `country_lifetime(country, counter)` returns one of nine whole-campaign counters as a 64-bit integer (`I` in the signature; `s64` in a component): 0 personnel lost, 1 regiments lost, 2 ships lost, 3 aircraft lost, 4 civilians affected, 5 provinces gained, 6 provinces lost, 7 wars won, 8 wars lost. They are the same numbers the end screen's Campaign record shows and the `lifetime_gt` / `lifetime_lt` event conditions test (§8.7 of the [Modding Reference](./MODDING_REFERENCE.md)); they are saved with the game and never reset by peace. An unknown counter or country reads 0. C# mods call `IModServices.GetLifetime`.

**When it works.** Reads see the game as it is while the hooks of the current frame are dispatched, so call them from a hook (`on_game_tick`, `on_economy_tick`, ...). From `on_init` there is no game yet and every read returns the neutral value.

### 4.3 State writes (ABI 4, permission `flags.write`)

`country_set_flag`, `country_clear_flag`, `country_set_var` and `country_add_var` change the same per-country state the events' `set_flag`, `clear_flag`, `set_variable` and `change_variable` effects change, so a script and an event file can drive each other: an event can test a flag a script set (`has_flag`, `flag_age_months_gt/lt`, `variable_gt/lt/eq`) and a script can read what an event set (§4.2). Declare `"flags.write"` (or the older `"write_flags"`) and `"wasmAbiVersion": 4`; a core module without both fails to load.

- **When they apply.** A write takes effect immediately, inside the hook that made it, and a read made later in the same hook sees it. A flag is stamped with the current game tick, so `flag_age_months_gt/lt` measure from the moment the script set it.
- **Names.** The name is the exact text an event file would use. A flag or variable name that no event file mentions still works: the dev console prints it as a hex number.
- **Limits.** A country holds at most `events.max_flags_per_country` flags and the same number of variables; a new one past the limit returns 0 (and logs once per country). A variable is a whole number kept within +-1,000,000,000: `country_set_var` clamps, `country_add_var` saturates instead of wrapping. A variable that was never set reads 0.
- **Results.** Every write returns 1 when it took effect and 0 when it was refused: no permission, a country that does not exist, a full country, or a refusal by the multiplayer rule below.
- **Multiplayer.** Every player's game runs the same hooks in the same order, so a write made from a simulation hook (`on_game_tick`, `on_economy_tick`, `on_war_declared`, ...) happens on every game. A write made from `on_ui_action` runs on one player's game only and is refused in a multiplayer session, like `country_set_treasury`. So is a write from outside any hook (a C# mod calling `IModServices` from its own callback). Single-player has no such limit.

C# mods use `IModServices.SetFlag`, `ClearFlag`, `SetVariable` and `AddVariable` (same rules, same permission).

**The mod's own state.** `state_set(key, value)` and `state_add(key, delta)` write, and `state_get(key)` reads, a small saved key/value store that belongs to your mod: whole numbers kept within +-1,000,000,000 (`state_set` clamps, `state_add` saturates), 0 for a key that was never set. Another mod's key of the same name is a different key. It is saved with the game, synced in multiplayer, and starts empty in a new game. Reading it needs `world.read`; writing it needs `flags.write` and the same multiplayer rule as the other writes. A mod may hold as many keys as one country may hold flags (`events.max_flags_per_country`); a new key past that returns 0 and logs once per mod. Events share the store: `"scope": "mod"` on `set_variable`, `change_variable` and `variable_gt/lt/eq` (see the [Modding Reference](./MODDING_REFERENCE.md), Flags and variables) reads and writes the same keys, so an event can test a counter a script keeps and the other way round. C# mods use `IModServices.GetState`, `SetState` and `AddState`.

### 4.4 Text by key (ABI 4)

A script can show and build text in each player's own language without shipping the text itself: the text lives in the mod's localization CSVs (§10) and the script names it by key.

- `localize(key_ptr, key_len, out_ptr, cap)` writes the text of the key, in the language this player has selected, to your buffer and returns the bytes it needs (§5). A key no string table defines, or defines with an empty value, comes back as the key itself, so you never get an empty string. Text that is not key-shaped (no dot, or spaces) comes back unchanged.
- `format(key_ptr, key_len, args_ptr, args_len, out_ptr, cap)` does the same and fills `{0}`, `{1}`... of the text from the arguments: UTF-8 strings joined with a NUL byte (`May`, NUL, `1450`), at most 32, a trailing NUL allowed. A template that cannot be filled (a stray brace, an index with no argument) comes back unformatted instead of failing. Pass numbers as text.
- `show_mod_popup_key(title_key, body_key, args)` queues a popup whose title and body are keys; each player sees it in their own language, with the arguments filled in. It needs `inject_ui`. Use it instead of building the text with `localize` and `show_mod_popup` whenever the popup is raised from a simulation hook.

**Do not branch on localized text.** `localize` and `format` return a different string for a player who plays in another language (and a different length). They are for showing, not for deciding: a script that compares them, measures them or uses them to choose a write would make a multiplayer host and follower diverge. `show_mod_popup_key` is safe because only the key and the arguments cross, and both are identical on every player's game. `localize` and `format` need no permission and work at any time, including `on_init`.

- `register_end_screen_row(label_key, value)` adds a line to the end screen's mod record (shown on every end screen, after the scenario's own `end_screen_rows`): the label is a text key of your mod, the value says where the number comes from (see the table above). It needs `inject_ui`, is presentation only, and a mod may add at most 12 rows. C# mods use `IModServices.RegisterEndScreenRow`.

C# mods use `IModServices.Localize`, `Format` and `ShowPopupLocalized`; `ModHookBus.ShowPopupLocalized(modId, titleKey, bodyKey, args)` is the same call for code that reaches the bus directly.

---

### 4.5 Alliance organizations and the world ceasefire (ABI 4, permission `write_diplomacy`)

These run the very same code as the `create_organization`, `join_organization`, `leave_organization`, `invite_to_organization`, `start_world_ceasefire` and `end_world_ceasefire` event effects (Modding Reference, §8.7), so a script and an event file cannot disagree. Declare `"write_diplomacy"` and `"wasmAbiVersion": 4`; a core module without both fails to load.

- **Arguments.** An organization id is `(ptr, len)` UTF-8 text (a component passes a `string`): lower-case letters, digits and underscore. Countries are the same handles the other imports use (§4.2); `collective_defense` and `force` are 0 or 1. `world_ceasefire_start(months, until_flag)`: the ceasefire ends after `months` 30-day months (0 = no end date), when the country-held event flag `until_flag` is set (empty = none), or when `world_ceasefire_end` is called; starting one replaces a running one.
- **Results.** Each returns 1 when the action ran and 0 when it did not: no permission, an unknown country or id, or the same refusal the event effect would give (the reason is written to `Player.log`).
- **Multiplayer.** Like the other writes (§4.3): a call from a simulation hook runs on every player's game; a call from `on_ui_action`, or from outside any hook, is refused in a multiplayer session.

C# mods use `IModServices.CreateOrganization`, `JoinOrganization`, `LeaveOrganization`, `InviteToOrganization`, `StartWorldCeasefire` and `EndWorldCeasefire` (same rules, same permission).

## 5. Memory Model

- The host allocates no memory inside the WASM module. All buffers are owned by the WASM module.
- For strings returned **to** the host (e.g. event IDs), write the UTF-8 bytes into WASM linear memory and pass the pointer + length to the import function.
- For strings the host returns **to you** (`country_iso3`), you pass a buffer: `(out_ptr, cap)`. The host writes at most `cap` bytes (UTF-8, no terminator) and returns the number of bytes the whole value needs. If that is larger than `cap` the value was cut; call again with a bigger buffer. A buffer that is not inside your memory is refused: nothing is written and the call returns -1.
- The host does not call `free` — manage memory in your module's allocator.
- The host checks every `(ptr, len)` pair against your module's linear memory before reading it. A string that falls outside that memory (or has a negative pointer or length) is ignored, with a one-time warning in the log. The host reads at most 64 KB of any one string.

---

## 6. Permissions in WASM

Declare permissions in `mod.json` (§7 of the [Modding Reference](./MODDING_REFERENCE.md)); each can be written in PascalCase (`WriteTreasury`) or snake_case (`write_treasury`). The two ABI-4 permissions are written `world.read` and `flags.write` (`ReadWorld` / `read_world` and `WriteFlags` / `write_flags` are accepted too). A call that needs a permission the mod did not declare does nothing. `fire_event` and `show_mod_popup` also write a warning to the log. The same checks apply to C# mods.

| Permission | What it allows |
|---|---|
| `WriteTreasury` | `country_set_treasury`, `add_treasury`; C#: `ModGameActionRequest.AddTreasuryDelta` |
| `FireTriggers` | `fire_event`, `fire_trigger`; C#: `ModHookBus.FireEvent`, `ModGameActionRequest.FireEventTrigger` / `FireEventDirectById` |
| `InjectUI` | `show_mod_popup`, `show_mod_popup_key`, `register_end_screen_row` (ABI 4; needs `wasmAbiVersion` 4), and the mod's `inject.json` UI; C#: `ModHookBus.ShowPopup`, `IModServices.ShowPopupLocalized` / `RegisterEndScreenRow` |
| `world.read` | The ABI-4 world reads (§4.2): `country_count`, `country_at`, `country_by_iso3`, `country_iso3`, `country_at_war_with`, `country_allied_with`, `country_war_count`, `country_war_enemy`, `province_owner`, `province_controller`, `country_has_flag`, `country_flag_age_months`, `country_get_var`; C#: the matching `IModServices` members. Needs `wasmAbiVersion` 4 for a WASM script. |
| `ReadEconomy` | Nothing yet. Every read import (`country_get_*`, `get_*`) works without a permission. The game accepts `ReadEconomy` so existing manifests stay valid. |
| `write_diplomacy` (`WriteDiplomacy`) | The ABI-4 diplomacy writes (§4.5): `organization_create`, `organization_join`, `organization_leave`, `organization_invite`, `world_ceasefire_start`, `world_ceasefire_end`; C#: `IModServices.CreateOrganization` / `JoinOrganization` / `LeaveOrganization` / `InviteToOrganization` / `StartWorldCeasefire` / `EndWorldCeasefire`. Needs `wasmAbiVersion` 4 for a WASM script. |
| `flags.write` (`WriteFlags`) | The ABI-4 state writes (§4.3): `country_set_flag`, `country_clear_flag`, `country_set_var`, `country_add_var`, `state_set`, `state_add`; C#: `IModServices.SetFlag` / `ClearFlag` / `SetVariable` / `AddVariable` / `SetState` / `AddState`, and for mods that reference the `GlobalProtocol.ECS` assembly `ModGameActionRequest.SetCountryFlag` / `ClearCountryFlag`. A country's event flags and variables, the state `has_flag` and `variable_*` conditions test. Needs `wasmAbiVersion` 4 for a WASM script. |

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

From ABI 4 a script can look keys up itself (`localize`, `format`) and show a popup by key with arguments (`show_mod_popup_key`); see §4.4. Independently of that, a title or body passed to `show_mod_popup` that is **exactly a localization key** (no spaces or commas, with at least one dot inside, e.g. `mymod.popup.intro.title`) is shown as that key's text in the player's language. Any other text is shown as written. C# mods get the same rule through `ModHookBus.ShowPopup(modId, title, body)`. Define the key in all 13 language files (§8.3 of the [Modding Reference](./MODDING_REFERENCE.md)); a player whose language file lacks it, or has it with an empty value, sees the key itself.

---

## 11. Windows Runtime Maintenance

For Windows x64 component runtime upgrades, use the canonical script:

`NewWorldOrder/tools/upgrade-wasmtime-win64.ps1`

Example:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\upgrade-wasmtime-win64.ps1 -Version v44.0.1
```

The script downloads the C API package, validates SHA-256 (for known versions), backs up the current DLL, replaces it, and probes required component symbols.

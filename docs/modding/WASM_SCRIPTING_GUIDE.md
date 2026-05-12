# NewWorldOrder – WASM Scripting Guide

Last updated: 2026-05-11

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
{ "wasmAbiVersion": 2 }
```

The host currently accepts ABI versions **1** through **2**. ABI 2 is the current version for new mods.

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

## 10. Building & Testing Your WASM Mod

### 10.1 Prerequisites

Choose one toolchain. .NET WASI is the primary path for this mod; AssemblyScript remains supported as a fallback path.

| Toolchain | What you need | Binary kind |
|---|---|---|
| **.NET WASI** (primary) | .NET 10 SDK + `dotnet workload install wasi-experimental` | Component (`XX 00 01 00`, e.g. `0A` or `0D`) |
| **AssemblyScript** (fallback) | Node.js ≥ 18 | Core WASM (`01 00 00 00`) |

### 10.2 Build Commands

**AssemblyScript** (from the mod's `Content/wasm-as/` directory):
```sh
npm install                                  # first time only
npm run build                                # outputs Content/mod.wasm (active entrypoint)
npm run build:named                          # outputs Content/mod-as.wasm (comparison/backup)
npm run build:debug                          # outputs with source maps for WASM debugger
```

**.NET WASI** (from the mod's `Content/wasm-dotnet/` directory):
```sh
dotnet workload install wasi-experimental    # first time only
dotnet publish -c Release                    # CopyWasmToContent target auto-copies to Content/mod.wasm
```

**Or just run `install.bat`** from the mod root — it detects your toolchain, builds, and installs in one step:
```
install.bat              # default: .NET WASI (primary) build + install
install.bat /dotnet      # .NET WASI build + install
install.bat /as          # AssemblyScript fallback build + install
install.bat /skip-build  # skip build, re-install existing mod.wasm
```

### 10.3 Verify the Binary Before Installing

Check that the right binary kind was produced:

```sh
# Windows PowerShell
Format-Hex Content\mod.wasm | Select-Object -First 1
```

| Bytes 0–7 | Binary kind | Engine path |
|---|---|---|
| `00 61 73 6D  01 00 00 00` | Core WASM | wasm3 runtime, no flags needed |
| `00 61 73 6D  XX 00 01 00` (for example `0A` or `0D`) | Component model | Needs `enableComponentRuntime: true` in `mod.json` |

### 10.4 In-Game Verification Checklist

After installing, run through this checklist to confirm everything works end-to-end:

1. **Launch the game** and open the Mods screen
2. **Enable "Old World Order"** — the mod card should load without a red error badge
3. **Start the 1450 scenario** — select any country
4. **Toolbar button** — a crown icon (🜲) should appear in the HUD toolbar
5. **First-tick hook** — on a dev build, open the Unity console and confirm:
   ```
   [Mod:globalprotocol.old_world_order] OWO: welcome popup shown on first tick
   ```
6. **UI action hook** — click the crown toolbar button and confirm:
   ```
   [Mod:globalprotocol.old_world_order] OWO: welcome popup reopened via toolbar button
   ```
7. **`fire_event` call** — the log lines above confirm the WASM hook ran successfully.
   The popup display itself depends on the event config system; log output is the reliable signal.

> **Dev builds only:** `log()` output is suppressed on release builds. Steps 5–6 require a development build of the game.

### 10.5 Common Errors & Fixes

| Error | Cause | Fix |
|---|---|---|
| `Mod ABI version X not supported` | `wasmAbiVersion` in `mod.json` is wrong | Set `"wasmAbiVersion": 2` |
| `component-model WASM detected but manifest does not opt in` | Built with .NET WASI but manifest missing opt-in | Add `"enableComponentRuntime": true` to `mod.json` |
| `no component backend is registered` | Component binary but engine has no backend | Use `/as` fallback for now (`install.bat /as`), or integrate/enable a component backend in the game build |
| `fire_event` call does nothing | Missing `FireTriggers` permission | Add `"FireTriggers"` to `permissions` in `mod.json` |
| Toolbar button missing | Missing `InjectUI` permission or `entrypoints.ui` path wrong | Check `mod.json` permissions and `Content/ui/inject.json` exists |
| `asc: command not found` | AssemblyScript not installed | Run `npm install` in `Content/wasm-as/` first |
| `wasi-experimental not found` | .NET WASM workload missing | Run `dotnet workload install wasi-experimental` |

### 10.6 Startup Briefing Localization (No Extra Setup)

The component fallback startup popup resolves text through the normal mod localization override pipeline.

Use these keys in both files:
- `overrides/localization_en.csv`
- `overrides/localization_tr.csv`

Required keys:
- `mod.owo.popup.startup.title`
- `mod.owo.popup.startup.body_with_date` (supports `{0}` year and `{1}` month)
- `mod.owo.popup.startup.body_no_date`

If a key is missing, the host uses built-in English fallback text.

### 10.7 Native C# Hook Showcase

For a modder-facing SDK sample of hook overrides, see:

- `Content/mod-csharp/ModEntrypoint.cs`

The sample demonstrates:
- overriding lifecycle hooks from `ModBase`
- filtering `OnUiAction` by `modId`
- routing a UI hook (`owo.welcome`) into `ModHookBus.FireEvent(...)`

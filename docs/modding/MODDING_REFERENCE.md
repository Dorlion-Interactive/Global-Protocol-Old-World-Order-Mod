# NewWorldOrder – Modding Reference

Last updated: 2026-05-11

This document is the authoritative reference for mod authors. It covers folder layout, the manifest, all data override types, scenario split files, permissions, and enum values.

---

## 1. Mod Folder Layout

```
%USERPROFILE%/Documents/GlobalProtocol/Mods/<mod-id>/
  mod.json                   ← required manifest
  Content/
    data/                    ← JSON balance/config overrides
    localization/            ← CSV localization additions
    events/                  ← scripted event JSON
    ui/                      ← USS/icon overrides
  scenario/                  ← optional split scenario folder
    scenario.json            ← required header (must contain scenarioId)
    countries_add.json
    countries_remove.json
    countries_state.json
    provinces_ownership.json
    units_define.json
    units_deploy_armies.json
    units_deploy_fleets.json
    units_deploy_air.json
```

Steam Workshop mods use the same layout under the Workshop item folder.

---

## 2. Manifest (mod.json)

`mod.json` remains the source of truth for mod-level metadata (identity, permissions, workshop metadata, visuals).
`scenario.json` is only for scenario/game-state setup data.

**Icon & Thumbnail Policy:** If `iconPath` or `thumbnailPath` are declared in the manifest, they are used exclusively — no implicit fallbacks to root filenames like `icon.png` or `logo.png`. Always explicitly declare the correct paths if visual assets are required.

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | ✓ | Unique reverse-domain ID, e.g. `com.myname.mymod` |
| `displayName` | string | ✓ | Display name shown in the mod browser |
| `iconPath` | string | | Relative path to a mod icon image. **When set, this path is used exclusively.** |
| `thumbnailPath` | string | | Relative path to a larger preview/thumbnail image. **When set, this path is used exclusively.** |
| `version` | string | ✓ | Semver string, e.g. `1.0.0` |
| `gameVersion` | string | | Semver range of compatible game versions |
| `author` | string | | Author display name |
| `description` | string | | Short description |
| `tags` | string[] | | Category tags |
| `dependencies` | string[] | | Mod IDs this mod requires |
| `loadOrderHint` | int | | Higher values load later |
| `enabledByDefault` | bool | | Whether the mod is pre-enabled on first install |
| `defaultScenarioFile` | string | | Relative path to a single `scenario.json` |
| `scenarioFolder` | string | | Relative path to a folder containing split scenario files. **Takes precedence over `defaultScenarioFile`.** |
| `wasmAbiVersion` | int | | WASM ABI version required (default: 1) |
| `runtimePolicy` | string | | WASM runtime coexistence policy: `"coexist"` (default), `"wasm_only"`, or `"csharp_only"`. See §2.1. |
| `enableComponentRuntime` | bool | | Allow component-model WASM binaries (requires a component backend to be registered). Set to `true` only if your WASM is component-format. See §2.2. |
| `permissions` | string[] | | Required permissions (see §7) |

**Auto-detection:** If neither `defaultScenarioFile` nor `scenarioFolder` is set but a `scenario/` subfolder containing `scenario.json` exists, it is loaded automatically.

### 2.1 WASM Runtime Policy

The `runtimePolicy` field controls how a mod's WASM and C# hooks coexist:

| Policy | Behavior |
|---|---|
| `"coexist"` (default) | Both WASM and C# event hooks run side-by-side. Useful for mods with fallback logic. |
| `"wasm_only"` | Only WASM exports are called. C# mod code is skipped. Useful for pure WASM mods. |
| `"csharp_only"` | Skip WASM loading entirely; only C# event hooks run. |

For managed C# hooks, place your compiled mod assembly under:

`<mod-root>/Mods/*.dll`

The runtime scans this folder for public `IModEntrypoint` implementations.

### 2.2 Component-Model WASM Support

The engine supports two WASM binary formats:
- **Core WASM** (default): Traditional WebAssembly modules. Set `wasmAbiVersion: 1` or `2`.
- **Component-Model WASM** (opt-in): WebAssembly component binaries (binary format version 0A 00 01 00). Requires explicit opt-in.

To use a component-model WASM in your mod:

1. Set `"enableComponentRuntime": true` in `mod.json`
2. Build your WASM as a component binary (not core module)
3. The engine will route it to `ModComponentWasmRuntime` instead of the standard wasm3 runtime

**Backend Requirements:** Component-model binaries require a backend to be registered via `ComponentWasmBackendRegistry`. If no backend is available at runtime, the mod will fail to load with a clear error message.

**Example manifest:**
```json
{
  "id": "com.example.component_mod",
  "wasmAbiVersion": 2,
  "enableComponentRuntime": true,
  "runtimePolicy": "wasm_only"
}
```

---

## 3. Scenarios

### 3.1 Single-File Scenario

Place all data in one `scenario.json` and point `defaultScenarioFile` at it.

Minimal example:
```json
{
  "scenarioId": "com.mymod.cold_war_2030",
  "displayName": "Cold War 2030",
  "version": "1.0.0",
  "startYear": 2030,
  "startMonth": 1,
  "startDay": 1,
  "clearDiplomaticRelationships": true
}
```

### 3.2 Split-Folder Scenario

Point `scenarioFolder` at a directory. The loader reads `scenario.json` first (must contain `scenarioId`), then merges the following domain files **in this exact order**:

| File | Domain |
|---|---|
| `countries_add.json` | New countries to spawn |
| `countries_remove.json` | Countries to remove |
| `countries_state.json` | Economic/political state overrides |
| `provinces_ownership.json` | Province and region reassignments |
| `units_define.json` | Custom unit type definitions |
| `units_deploy_air.json` | Air wing placements |
| `units_deploy_armies.json` | Army stack placements |
| `units_deploy_fleets.json` | Fleet placements |

Each file is optional; missing files are skipped. Lists from all files are **appended** — later files do not replace earlier ones.

### 3.3 Scenario Header Fields

| Field | Type | Default | Description |
|---|---|---|---|
| `scenarioId` | string | — | **Required.** Unique identifier |
| `displayName` | string | `""` | Shown in scenario picker |
| `version` | string | `""` | Semver string |
| `startYear` | int | 0 | Game start year (0 = use base game default) |
| `startMonth` | int | 1 | 1–12 |
| `startDay` | int | 1 | 1–31 |
| `startTick` | int | 0 | Absolute tick override (0 = derive from date) |
| `clearDiplomaticRelationships` | bool | false | Wipe all diplomatic relations before loading |
| `clearDiplomacyScope` | string | `"extended"` | `"core"` or `"extended"` |
| `rebuildNeutralRelations` | bool | true | Re-seed neutral opinion after clearing |
| `nationalGoalsFile` | string | `""` | Relative path to national goals JSON |
| `gdpScale` | float | 1.0 | Global GDP multiplier |
| `economicEraLabel` | string | `""` | Economy era key for init system |

---

## 4. Country Overrides

### 4.1 Adding Countries (`addCountries` / `countries_add.json`)

Each entry maps to `ScenarioCountryDefinition`. Required field: `iso3`.

| Field | Type | Description |
|---|---|---|
| `iso3` | string | ISO3 code of the new country (uppercase, 3 chars) |
| `templateISO3` | string | Copy stats from this existing country |
| `name` | string | Display name |
| `mapColor` | string | Hex color `#RRGGBB` |
| `flagPngPath` | string | Relative path to a 128×80 flag PNG in the mod folder |
| `capital` | string | Capital city display name |
| `capitalProvince` | string | Province name or numeric ID string |
| `population` | int | Total population |
| `areaKm2` | number | Territory area in km² |
| `governmentType` | string | See §8.1 |
| `governmentSubtype` | string | Free-form subtype label |
| `ideology` | string | See §8.2 |
| `militaryUnitTypeIds` | string[] | IDs of available unit types |
| `neighbors` | string[] | Land-adjacent ISO3 codes |
| `seaNeighbors` | string[] | Sea-adjacent ISO3 codes |
| `leaderTitle` | string | Override leader title (e.g. `"Chancellor"`) |
| `leaderName` | string | Override leader name |
| `homelandTerm` | string | Override homeland noun (e.g. `"Federation"`) |
| `continent` | string | See §8.3 |
| `region` | string | See §8.4 |

### 4.2 Removing Countries (`removeCountries` / `countries_remove.json`)

An array of ISO3 strings: `["XXX", "YYY"]`

### 4.3 State Overrides (`countryStateOverrides` / `countries_state.json`)

| Field | Type | Description |
|---|---|---|
| `iso3` | string | **Required.** Target country |
| `clearRelationships` | bool | Clear this country's diplomatic state |
| `clearDiplomacyScope` | string | `"core"` or `"extended"` |
| `governmentType` | string | New government type |
| `ideology` | string | New ideology |
| `techLevel` | int | 0–10 |
| `stability` | float | 0.0–1.0 |
| `corruption` | float | 0.0–1.0 |
| `treasury` | number | USD millions |
| `gdp` | number | Annual GDP in USD millions |
| `manpower` | int | Available manpower (thousands) |
| `reserve` | int | Reserve pool (thousands) |

---

## 5. Province & Region Ownership (`provinces_ownership.json`)

### Province-level
```json
{ "provinceOwnerOverrides": [
  { "provinceId": 1234, "ownerISO3": "DEU" }
] }
```

### Region-level (bulk)
Region overrides are applied **before** province overrides.
```json
{ "regionOwnerOverrides": [
  { "regionName": "WesternEurope", "ownerISO3": "FRA" }
] }
```

Region names match the `WorldRegion` enum — see §8.4.

---

## 6. Military Deployments

### 6.1 Custom Unit Types (`units_define.json`)

| Field | Type | Description |
|---|---|---|
| `id` | string | **Required.** Unique type ID |
| `category` | string | **Required.** See §8.5 |
| `ownerIso3` | string | Country-exclusive unit (optional) |
| `displayName` | string | |
| `attack / defense / hp / speed` | float | Base stats |
| `manpower` | int | Manpower cost |
| `airAttack / antiAir / range` | float | Air-specific stats |
| `terrainPlains/Mountain/Desert/Forest/Urban` | float | Terrain modifiers (1.0 = neutral) |

### 6.2 Stack Unit Entry (shared by armies/fleets/air)

| Field | Type | Default | Description |
|---|---|---|---|
| `unitTypeId` | string | — | **Required.** Type ID |
| `unitDefIndex` | int | -1 | Index into country's UnitDef list. -1 = auto. |
| `count` | int | 1 | Number of units in the stack slot |
| `currentHp` | float | -1 | HP override. -1 = full HP. |

### 6.3 Army Stacks (`units_deploy_armies.json`)

| Field | Required | Description |
|---|---|---|
| `ownerISO3` | ✓ | Owner country |
| `provinceId` | ✓ | Land province ID |
| `morale` | | 0–1, -1 = full |
| `units` | ✓ | Array of stack unit entries |

### 6.4 Fleet Stacks (`units_deploy_fleets.json`)

Same as armies plus `inHarbor: bool` (default `false`). `provinceId` = sea zone or coastal province.

### 6.5 Air Wing Stacks (`units_deploy_air.json`)

Same as armies plus:
- `missionType`: `"cas"`, `"interception"`, `"strategic_bombing"`, `"naval_strike"`, `"patrol"`, `"standby"`
- `readiness`: 0–1, -1 = full

---

## 7. Permissions

Declare required permissions in `mod.json`:
```json
{ "permissions": ["ReadEconomy", "WriteTreasury", "InjectUI"] }
```

| Permission | Description |
|---|---|
| `ReadEconomy` | Read-access to country economic state |
| `WriteTreasury` | Modify treasury via hook callbacks |
| `FireTriggers` | Trigger scripted events |
| `WriteFlags` | Override flag textures at runtime |
| `InjectUI` | Add UI elements to the HUD |

The game will reject mods that call gated APIs without the required permission.

For managed C# mods, `InjectUI` also gates `ModHookBus.ShowPopup(...)`.

---

## 8. Enum Reference

### 8.1 Government Types
`democracy`, `authoritarian`, `hybrid`, `monarchy`, `theocracy`, `military_junta`, `failed_state`, `city_state`

### 8.2 Ideologies
`progressive`, `centrist`, `conservative`, `nationalist`, `communist`, `islamist`, `libertarian`, `green`, `theocratic`

### 8.3 Continents
`Africa`, `Americas`, `Antarctica`, `Asia`, `Europe`, `Oceania`, `Unknown`

### 8.4 World Regions
`AustraliaNewZealand`, `CentralAsia`, `EastAsia`, `EasternEurope`, `LatinAmericaCaribbean`, `Melanesia`, `Micronesia`, `NorthernAfrica`, `NorthernAmerica`, `NorthernEurope`, `Polynesia`, `SouthAsia`, `SoutheastAsia`, `SouthernEurope`, `SubSaharanAfrica`, `Unknown`, `WesternAsia`, `WesternEurope`

### 8.5 Unit Categories
`infantry`, `cavalry`, `artillery`, `naval`, `air`, `armor`, `special_forces`

### 8.6 Air Mission Types
`cas`, `interception`, `strategic_bombing`, `naval_strike`, `patrol`, `standby`

### 8.7 Diplomacy Clear Scopes
- `core` — wars and alliances only
- `extended` — all diplomatic relationships (default)

---

## 9. WASM Binary Format & Backend Registration

### 9.1 Core vs. Component-Model Binaries

The engine detects WASM binary format at load time (magic bytes 0x00 0x61 0x73 0x6D followed by version bytes):

| Format | Version Bytes | Handled By | Requires `enableComponentRuntime` |
|---|---|---|---|
| **Core** | `01 00 00 00` | `ModWasmRuntime` (wasm3) | No |
| **Component** | `XX 00 01 00` (for example `0A 00 01 00` or `0D 00 01 00`) | `ModComponentWasmRuntime` (pluggable backend) | Yes |

**Core modules** (standard WebAssembly) are always supported.  
**Component modules** require:
1. `"enableComponentRuntime": true` in manifest
2. A component backend registered via `ComponentWasmBackendRegistry`

### 9.2 Component Backend Registration (Engine Developers)

Component-model binaries are routed to pluggable backends. To provide component support, register a backend during engine startup:

```csharp
// In your engine initialization code:
using GlobalProtocol.Core.Mods.Wasm;

// Register a factory function that creates component backends
ComponentWasmBackendRegistry.RegisterFactory((modId, permissions) =>
{
    return new YourCustomComponentBackend(modId, permissions);
});
```

The backend must implement `IComponentWasmBackend`:
```csharp
public interface IComponentWasmBackend : IDisposable
{
    bool Initialize(string modId, ModWasmPermissions permissions, byte[] wasmBytes);
    bool CallVoid(string exportName);
    bool CallI32(string exportName, int a);
    bool CallI32I32(string exportName, int a, int b);
    bool CallI32I32I32(string exportName, int a, int b, int c);
    bool CallI32I32I32I32(string exportName, int a, int b, int c, int d);
    bool CallUiAction(string exportName, string hookName, string modId);
}
```

If no backend is registered, the engine will reject component-model mods with a clear error: *"component-model WASM detected but no component backend is registered."*

---

## 9.3 WASM ABI Compatibility Matrix

`wasmAbiVersion` in `mod.json` declares which ABI version the mod was compiled against. The engine validates this at load time.

| Game ABI | Accepted `wasmAbiVersion` values | Notes |
|---|---|---|
| 1–2 (current) | `1`, `2` | Stable — all hook exports and host imports documented in WASM_SCRIPTING_GUIDE.md §3–4 |

**Support window:** ABI 1 and ABI 2 are both accepted for backwards compatibility. When ABI 3 ships, both `1` and `2` will be accepted for at least one major game release cycle. After that window, older ABI versions will be rejected with a clear error in the mod browser.

For versioning rules and the deprecation lifecycle, see `WASM_SCRIPTING_GUIDE.md` §10.

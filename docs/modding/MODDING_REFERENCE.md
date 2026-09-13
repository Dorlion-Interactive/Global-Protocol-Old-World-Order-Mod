# NewWorldOrder – Modding Reference

Last updated: 2026-09-11

This document is the authoritative reference for mod authors. It covers folder layout, the manifest, all data override types, scenario split files, permissions, and enum values.

---

## 1. Mod Folder Layout

```
%USERPROFILE%/Documents/GlobalProtocol/Mods/<mod-id>/
  mod.json                   ← required manifest
  Content/
    buildings.json           ← building roster: merge, replace or start from scratch (§8.1)
    units.json               ← unit roster (§8.1)
    resources.json           ← resource overrides and disables (§8.1)
    currencies.json          ← national currencies money is shown in, display-only (§8.5)
    localization/            ← CSV localization additions (<language>.csv)
    events/                  ← scripted event JSON (one event per file)
    ui/                      ← USS/icon overrides
  icons/                     ← replacement icons by id: buildings/, units/, resources/, doctrines/ (§8.4)
  overrides/                 ← sparse config overrides (see §9)
    game_settings.json
    doctrines.json
    game_flow.json
    events.json
    envoys.json
    military_markers.json
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
| `entrypoints` | object | | Explicit runtime entrypoints such as `entrypoints.wasm` and `entrypoints.ui` |
| `wasmAbiVersion` | int | | WASM ABI version required (default: 1) |
| `runtimePolicy` | string | | Runtime coexistence policy: `"coexist"` (default), `"wasm_only"`, `"csharp_only"` |
| `enableComponentRuntime` | bool | | Allow component-model WASM binaries for this mod |
| `permissions` | string[] | | Required permissions (see §7) |

`entrypoints.wasm` is the preferred way to declare the mod's WASM module. `entrypoints.ui` is the preferred way to declare `inject.json`. Legacy fallback paths are still accepted for compatibility when the manifest entrypoint is omitted or unresolved.

**Auto-detection:** If neither `defaultScenarioFile` nor `scenarioFolder` is set but a `scenario/` subfolder containing `scenario.json` exists, it is loaded automatically.

### 2.1 Runtime Policy

The `runtimePolicy` field controls how WASM and managed C# hooks coexist:

| Policy | Behavior |
|---|---|
| `"coexist"` (default) | WASM and C# hooks can run side-by-side. |
| `"wasm_only"` | Only WASM exports are called. Managed C# hooks are skipped. |
| `"csharp_only"` | WASM loading is skipped. Only managed C# hooks run. |

For managed C# hooks, place your compiled assembly under:

`<mod-root>/Mods/*.dll`

The runtime scans this folder for public `IModEntrypoint` implementations.

### 2.2 Component Runtime Opt-In

Set `enableComponentRuntime: true` only when your WASM binary is component-model format.
Core WASM modules should leave this `false`.

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
| `startYear` | int | 0 | Game start year (0 = use base game default). Any year from 1 to 3000, so historical scenarios can start centuries before the base game's 2026. |
| `startMonth` | int | 1 | 1–12 |
| `startDay` | int | 1 | 1–31 |
| `startTick` | int | 0 | Absolute tick override (0 = derive from date) |
| `clearDiplomaticRelationships` | bool | false | Wipe all diplomatic relations before loading |
| `clearDiplomacyScope` | string | `"extended"` | `"core"` or `"extended"` |
| `rebuildNeutralRelations` | bool | true | Re-seed neutral opinion after clearing |
| `nationalGoalsFile` | string | `""` | Relative path to national goals JSON |
| `gdpScale` | float | 1.0 | Multiplies every country's GDP, GDP per capita, exports, imports, foreign reserves and treasury once, when a new game starts. `countryStateOverrides` values are absolute and are applied after it. |
| `economicEraLabel` | string | `""` | Economy era key for init system |
| `currencySymbol` | string | `"$"` | Symbol shown in all money displays. Any UTF-8 string, e.g. `"€"`, `"fl."`, `"¥"`. Null/empty keeps the default `"$"`. With national currencies (§8.5) it is the base currency's symbol, and it wins over the file's `baseCurrency.symbol`. |
| `currenciesFile` | string | `""` | Currencies file, relative to the scenario folder (§8.5). Applied after every mod's `Content/currencies.json`. |
| `buildingsOverrideFile` | string | `""` | Buildings roster file, relative to the scenario folder (§8.1). Applied after every mod's `Content/buildings.json`. |
| `unitsOverrideFile` | string | `""` | Units roster file, relative to the scenario folder (§8.1). |
| `resourcesOverrideFile` | string | `""` | Resources file, relative to the scenario folder (§8.1). |
| `techOverrideFile` | string | `""` | **Ignored.** The tech tree was replaced by the Knowledge Network — use `overrides/doctrines.json` and `disabledDoctrineBranches`. |
| `disabledUnitCategories` | string[] | `[]` | Unit categories (§9.5) removed from recruitment and build eligibility. |
| `disabledUnitTypeIds` | string[] | `[]` | Specific unit ids, same effect. |
| `disabledBuildingCategories` | string[] | `[]` | `Economic`, `Military`, `Infrastructure`, `Research`, `Social`, `Defense`, `Intelligence` — removed from every build menu, starting seeding, the AI and the build command. |
| `disabledBuildingIds` | string[] | `[]` | Specific building ids, same effect. To drop most of the base roster, use `"mode": "replace"` (§8.1) instead. |
| `disabledDoctrineBranches` | string[] | `[]` | Knowledge Network branches hidden from research: `military`, `government`, `economy`, `industry`, `diplomacy`, `intelligence`, `cyber`, `space`, `energy`, `society`. Their tier gates never open, so everything gated behind them stays locked. |

Override file paths that do not resolve, and files that do not parse, are listed in the Mods panel
(and the Mod Builder's Reload & Test) instead of being skipped silently.

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

Localization overrides are loaded from both modern and legacy paths for compatibility:
- `Content/localization/<language>.csv`
- `overrides/localization_<language>.csv`

Use `Content/localization/` for new mods.

---

## 8. Data & Config Overrides

Balance and content changes live outside `scenario/`. Every file here is optional.

### 8.1 Content rosters (`Content/*.json`)

`Content/buildings.json`, `Content/units.json` and `Content/resources.json` — and a scenario's
`buildingsOverrideFile` / `unitsOverrideFile` / `resourcesOverrideFile` — describe the game's
content roster. Entries are matched against the base game by `id` (case-insensitive). Each file
picks a **mode**:

| Mode | What the file means |
|---|---|
| `"merge"` (default; also any bare array) | Change or add to the base game. Fields you write overwrite the base entry, fields you omit keep their base values, a new `id` is added. |
| `"replace"` | The file **is** the roster. Every base id it does not list is switched off. |
| `"replace"` with no entries | Start from scratch: every base entry is switched off. |

A merge file that re-prices one building:

```json
[
  { "id": "power_plant", "cost": { "money": 850, "build_time_months": 12 } }
]
```

A replace file for an earlier era:

```json
{
  "mode": "replace",
  "overrides": [
    { "id": "naval_base", "name": "Shipyard", "category": "military",
      "cost": { "money": 400, "build_time_months": 6 } },
    { "id": "castle", "name": "Castle", "category": "defense",
      "cost": { "money": 900, "build_time_months": 18 }, "effects": { "defense_bonus": 25 } }
  ],
  "disabled": []
}
```

`"replace": true` is accepted as a shorthand for `"mode": "replace"`. The entries may live under
`overrides` (what the Mod Builder writes) or under the base config's own root key (`buildings`,
`units`, `resources`).

**`disabled`** switches ids off in any mode, for buildings, units and resources alike. It wins over
being listed.

**`inherit`** decides what an entry for an **existing** base id means:

- `true` — overwrite only the fields you wrote (the classic sparse merge);
- `false` — the entry is the whole definition; fields you leave out take engine defaults instead of
  the base game's values.

Entries in a replace-mode file default to `inherit: false`, so a medieval roster cannot silently
keep modern recipes or effects; entries in a merge-mode file default to `true`. New ids are always
whole definitions. Nested objects (`cost`, `effects`, `prerequisites`) are replaced as a whole,
never merged field by field — write the full object.

**What "switched off" means.** Base entries are never removed from the game's data: saves store
buildings and units by position, and multiplayer compares unit positions. A switched-off building
is hidden from every build menu, never placed at game start, never chosen by the AI, and rejected
by the build command (upgrades included). A switched-off unit is hidden from recruitment, rejected
by the recruit commands, and removed from the base game's starting armies. A switched-off resource
is no longer produced.

**Load order.** Files apply in load order: every active mod alphabetically by mod id, then the
active scenario's override file. A later merge file wins on any field it sets and can bring back a
base id an earlier replace file dropped; a later replace file discards everything composed before
it (the Mods panel warns when that happens).

**Save compatibility.** Ids you add are appended in roster order. Keep that order between versions
of your mod — never remove or reorder ids you added — or saves made with the older version point at
the wrong entries.

**Buildings the engine finds by id.** Some features look their building up by id. Switching one off
switches that feature off, so a historical roster usually keeps the id and re-skins it (name, icon,
localization) instead. The Mods panel warns when one of these is off:

| Building id | Used for |
|---|---|
| `naval_base` | Fleet recruitment and docking |
| `airfield` | Air wing bases and starting airfields |
| `barracks`, `military_base` | Land unit recruitment (units name them in `cost.required_building`) |
| `submarine_pen`, `trade_port` | Coastal building rules |
| `intelligence_hq`, `cyber_ops_center`, `counterintel_bureau` | Espionage |
| `satellite_launch_facility` | Satellite launches |

**Units** name the building they are recruited at in `cost.required_building`. A unit whose building
is missing or switched off can never be recruited; the Mods panel says so.

**Resources** are a fixed set. A mod can re-price, re-skin or switch them off, but cannot add new
ones; unknown resource ids are reported.

**In the Mod Builder** (Content tab) the roster mode sits at the top of each file. In replace mode
the base entries you have not included are listed as switched off, each with an Include button, plus
Include all to start from a copy of the base game. Add brand-new ids (optionally copying an existing
entry), switch entries off, and set each entry's inherit flag right on its card. The checks box below
runs the same checks as the game's loader while you edit. The scenario header's disabled lists are
checklists of the game's real building, unit, category and branch ids on the Scenario tab.

**`Content/tech_tree.json` is retired.** Research is the Knowledge Network (`overrides/doctrines.json`,
§8.2). The file is ignored with a warning, and so is a scenario's `techOverrideFile`. To keep modern
technology out of an earlier era, hide whole branches with the scenario header's
`disabledDoctrineBranches` (§3.3): their tier gates never open, so everything gated behind them
stays locked.

Load problems — a file that does not parse, an override file that is not where the scenario says, a
unit that needs a switched-off building — are listed in the Mods panel and in the Mod Builder's
Reload & Test. Each entry validates against `building_type.schema.json` / `unit_type.schema.json` /
`resource_type.schema.json`; the file as a whole follows `mod_content_envelope.schema.json`.

### 8.2 Config overrides (`overrides/`)

Sparse documents against the shipped base config — write only the keys you want to change.

| File | Covers |
|---|---|
| `game_settings.json` | Balance sections: economy, population, diplomacy, world order, AI weights, fog of war, intelligence, map interaction, satellite, … |
| `doctrines.json` | Doctrine values, effects and text |
| `game_flow.json` / `events.json` / `envoys.json` | The matching `game_settings` sections, kept as separate files for backwards compatibility |
| `military_markers.json` | Map marker appearance |

Two constraints worth knowing before you edit:

- **Doctrines are structure-locked.** Branch, tier and doctrine positions are save-stable, so you can
  change a doctrine's numbers, effects and strings, but adding, removing or reordering entries is
  rejected — it would silently repoint every existing save.
- **`game_flow` cannot be modded in practice.** Autosave interval, autosave on/off, save-slot count
  and the pre-selected country are the *player's* settings (stored in their own `settings.json` and
  edited from the Settings screen). A mod override of that section is ignored, which is why the
  in-game Mod Builder hides it.

`overrides/laws.json` **is applied at runtime**: it merges onto the shipped `laws.json`
(sparse, index-wise) and the laws blob is re-baked at boot. Mods may retune values on
existing categories/options AND append new ones at the tail — appends are save-stable by
design. Removing, reordering or replacing existing entries is rejected (category/option
indices live in saves and on the multiplayer wire) and disables the offending mod. Caps:
16 categories, 6 options per category, 4 diplomacy-weighted categories; every appended
category needs at least one ungated option and a complete 10-government `defaults` block.
Law names/descriptions come from `politics.law.*` keys in the mod's
`Content/localization/<lang>.csv` files (all 13 shipped locales are loaded).

### 8.3 Localization

Add `Content/localization/<language>.csv` with plain `key,value` rows (UTF-8, no BOM, no header).
The 13 shipped languages are `cz, de, en, es, es-419, fr, ja, ko, pt, pt-br, ru, tr, zh`. Keys you
define override the base game's; keys you omit fall back to the shipped string.

### 8.4 Icons

A mod replaces the picture of a building, unit, resource or doctrine by shipping an image named after
its id. The game looks for mod icons first and falls back to the base game's art.

| Folder | File name | Shown in |
|---|---|---|
| `icons/buildings/` | building id, e.g. `castle.png` | Build menus, province view, tooltips, research unlock chips |
| `icons/units/` | unit id | Recruitment, army cards, unit lists |
| `icons/resources/` | resource id, e.g. `oil.png` | Resource panels and tooltips |
| `icons/doctrines/` | the doctrine's `icon` id from doctrines.json | Research screen cards, milestones, hidden cards |

- `.png`, `.jpg` and `.jpeg` are read; if one id has both a `.png` and a `.jpg`, the `.png` wins.
- `Content/icons/...` is read too, after `icons/...`.
- When several active mods ship the same icon, the mod that loads last (alphabetically by mod id)
  wins — the same order as content rosters.
- New ids you add to a roster (§8.1) get their icon the same way.
- Icons are presentation only and are not part of the multiplayer lobby check.
- Map markers are drawn per unit **subcategory**: set those with `overrides/military_markers.json`
  (`subcategory_icons`).

The Mod Builder's Content tab has an icon picker on every building, unit and resource card, and the
Doctrines tab lists every doctrine icon id with a picker; both copy your image to the right place.

### 8.5 Currencies (`Content/currencies.json`)

Countries can show money in their own currency. This is display-only. The simulation keeps one
money unit, the base currency, and every amount is converted when it is shown. Currencies are
therefore not part of the multiplayer lobby check.

```json
{
  "baseCurrency": { "id": "florin", "name": "Florin", "symbol": "fl." },
  "currencies": [
    { "id": "akce", "name": "Ottoman Akçe", "symbol": "ak.", "symbolPosition": "suffix",
      "exchangeRateToBase": 45.0, "associatedCountries": ["OTT", "CRA"] }
  ]
}
```

- `exchangeRateToBase` is local units per one base unit. At 45, an amount of 1,000 in the base
  currency is shown to an Ottoman player as `45.0K ak.`. The rate must be above 0; a currency without
  a valid rate or a `symbol` is skipped with a warning.
- `symbolPosition` is `"prefix"` (the default) or `"suffix"`. A leading symbol of two or more
  characters that ends in a letter or `.` is written with a space: `fl. 1.2K`.
- A country listed under two currencies keeps the first one, with a warning.
- Files stack like content rosters: every active mod's `Content/currencies.json` in load order, then
  the scenario's `currenciesFile`. A later file replaces a currency with the same `id`, and its
  `baseCurrency` replaces the base fields it sets.
- Each player sees their own country's currency. Spectators, menus and countries without a currency
  see the base currency. **Settings → Gameplay → Show money in the base currency** switches every
  amount to the base currency.
- Money written directly into localized prose (a few event texts) keeps `$`.

The Mod Builder's Content tab has a Currencies sub-tab for all of this.

---

## 9. Enum Reference

### 9.1 Government Types
`democracy`, `authoritarian`, `hybrid`, `monarchy`, `theocracy`, `military_junta`, `failed_state`, `city_state`

### 9.2 Ideologies
`progressive`, `centrist`, `conservative`, `nationalist`, `communist`, `islamist`, `libertarian`, `green`, `theocratic`

### 9.3 Continents
`Africa`, `Americas`, `Antarctica`, `Asia`, `Europe`, `Oceania`, `Unknown`

### 9.4 World Regions
`AustraliaNewZealand`, `CentralAsia`, `EastAsia`, `EasternEurope`, `LatinAmericaCaribbean`, `Melanesia`, `Micronesia`, `NorthernAfrica`, `NorthernAmerica`, `NorthernEurope`, `Polynesia`, `SouthAsia`, `SoutheastAsia`, `SouthernEurope`, `SubSaharanAfrica`, `Unknown`, `WesternAsia`, `WesternEurope`

### 9.5 Unit Categories
`infantry`, `cavalry`, `artillery`, `naval`, `air`, `armor`, `special_forces`

### 9.6 Air Mission Types
`cas`, `interception`, `strategic_bombing`, `naval_strike`, `patrol`, `standby`

### 9.7 Diplomacy Clear Scopes
- `core` — wars and alliances only
- `extended` — all diplomatic relationships (default)

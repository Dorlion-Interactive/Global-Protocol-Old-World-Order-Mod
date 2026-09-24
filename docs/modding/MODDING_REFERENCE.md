# NewWorldOrder – Modding Reference

Last updated: 2026-09-23

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
    events/                  ← event JSON: a bare array, a single object, or { "events": [...] } (§8.7)
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
    national_goals.json      ← optional, named by nationalGoalsFile (§8.6)
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
| `nationalGoalsFile` | string | `""` | National goals file, relative to the scenario folder (§8.6). It **replaces** the base game's goals for the Agenda panel and the AI. |
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
| `restrictOwnersToOwnedUnits` | bool | false | A unit type with an `ownerIso3` (§6.1) is exclusive to that country. When true, a country that owns unit types may recruit **only** those — each nation gets its own roster. When false, owners keep every other available unit too. |
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
| `militaryUnitTypeIds` | string[] | **Not enforced yet** — the game does not read it. To give a country its own units, set `ownerIso3` on the unit types (§6.1). |
| `neighbors` | string[] | Land-adjacent ISO3 codes |
| `seaNeighbors` | string[] | Sea-adjacent ISO3 codes |
| `leaderTitle` | string | Override leader title (e.g. `"Chancellor"`) |
| `leaderName` | string | Override leader name |
| `homelandTerm` | string | Override homeland noun (e.g. `"Federation"`) |
| `continent` | string | See §8.3 |
| `region` | string | See §8.4 |
| `neutral` | bool | Military neutrality. Omitted keeps the template's flag. An AI-controlled neutral forms no military alliances or defense pacts, gives no guarantees, joins no coalitions and answers no calls to arms (it still honors guarantees it already holds, and calls its own allies when attacked). A human player is unrestricted. |

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
| `neutral` | bool | Sets (`true`) or clears (`false`) military neutrality; omitted keeps the baked flag (see §4.1) |

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
| `id` | string | **Required.** Unique type ID, at most 29 bytes |
| `category` | string | **Required.** `infantry`, `cavalry`, `artillery`, `armor`, `special_forces`, `naval` or `air` |
| `ownerIso3` | string | Optional. Only this country can recruit the unit; everyone else is denied it. The owner keeps every other unit unless the scenario sets `restrictOwnersToOwnedUnits` (§3.3). |
| `displayName` | string | |
| `attack / defense / hp / speed` | float | Base stats |
| `manpower` | int | Manpower cost |
| `airAttack / antiAir / range` | float | Air-specific stats |
| `terrainPlains/Mountain/Desert/Forest/Urban` | float | Terrain modifiers (1.0 = neutral) |

A unit type whose `id` no content file defines (`Content/units.json` or the scenario's
`unitsOverrideFile`, §8.1) becomes a real, recruitable unit. It copies cost, upkeep, required
building, prerequisites and equipment from a base unit of its category — `infantry` for infantry
and cavalry, `artillery`, `armor` and `special_forces` from their namesakes, `frigate` for naval,
`fighter` for air — and the fields above replace that unit's name, stats and terrain modifiers. A
field you leave out keeps the base unit's value. When a content file does define the id, that
definition is used and these stats are ignored; set costs or requirements there.

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
| `WriteFlags` | Set or clear a country's event flags, the flags that `has_flag` / `not_has_flag` event conditions test. It has nothing to do with flag or banner images. |
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
localization) instead. The Mods panel warns when a replace roster leaves one of these out. When you
mean to drop the feature, name the id in the roster's `"disabled"` list (or the scenario's
`disabledBuildingIds`) and the warning goes away:

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

**Doctrine gates.** A building or unit whose `prerequisites.tech` names a tier of a hidden doctrine
branch (`disabledDoctrineBranches`, or a branch a replace-mode `doctrines.json` leaves out, §8.2) is
never offered. The Mods panel warns for the entries your roster lists; set their `prerequisites.tech`
to `"none"` or to a tier of a branch the game shows.

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
stays locked. To rebuild the tree itself for another era, use a replace-mode `doctrines.json` (§8.2).

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

- **Doctrines merge or replace.** `overrides/doctrines.json` has a root `"mode"`:
  - `"merge"` (the default) patches the base tree position by position. You can change a
    doctrine's numbers, effects and strings, but adding entries (branches, tiers, doctrines, hidden
    cards, directives) is rejected — positions are save-stable, and new ones would repoint every
    existing save. Nested objects merge key by key: an `effects` block you write keeps every base
    effect you did not mention.
  - `"replace"` rebuilds whole branches. Each branch the file lists, matched by `id` (file order does
    not matter), replaces the base branch outright: its tiers, doctrines, effects, icons, AI weights,
    milestone, directives and hidden cards are exactly what you wrote — nothing is inherited. Every
    base branch the file leaves out is **hidden**, exactly as if the scenario listed it in
    `disabledDoctrineBranches`, so its tier gates never open (laws, buildings and units gated behind
    it stay locked). A replacing branch needs the base branch's 5 tiers, each with 1 to 3 doctrines
    with unique ids; at most 16 hidden cards and 3 directives; effect values must be numbers.
    `settings` still merges sparsely, `starting_grants` replaces the base grants when present, and
    the legacy tech map is always the base game's. Names and descriptions come from your
    `name_key`/`desc_key` rows in the mod's localization CSVs; icons from `icons/doctrines/` (§8.4).

  ```json
  { "mode": "replace",
    "branches": [
      { "id": "military", "name_key": "doctrine.branch.military",
        "tiers": [
          { "name_key": "mymod.military.t1", "doctrines": [
              { "id": "feudal_levies", "name_key": "mymod.feudal_levies", "desc_key": "mymod.feudal_levies.desc",
                "icon": "military_t1a_professional_armed_forces", "effects": { "recruit_cost_mult": 0.9 },
                "ai": { "military": 0.6 } },
              { "id": "mercenary_companies", "name_key": "mymod.mercenaries", "effects": { "military_attack": 0.05 } } ] },
          "… tiers 2-5 …"
        ] } ] }
  ```

  Files apply in load order; a replace file starts again from the base tree and the Mods panel warns
  that it discarded the doctrine files loaded before it.
- **`game_flow` cannot be modded in practice.** Autosave interval, autosave on/off, save-slot count
  and the pre-selected country are the *player's* settings (stored in their own `settings.json` and
  edited from the Settings screen). A mod override of that section is ignored, which is why the
  in-game Mod Builder hides it.

The Mod Builder's **GOALS** tab edits the scenario's `nationalGoalsFile`: one set of goals per
country, with `type` and `priority` offered as dropdowns of exactly the values the loader accepts.
A value outside those lists is read as `economic`, so the AI pursues the goal on the wrong terms;
the Mods panel warns about it, and the editor will not let you author one.

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

A row is split at its **first** comma, so a value may contain commas and does not need quoting.

**There is no fallback between languages for a key only your mod defines.** The game layers the
base-game CSV, then the player's language CSV, then your mod's CSV *for that one language*. A key
you put in `en.csv` and nowhere else therefore renders as the raw key — `mymod.some.key` — for
every player not running English. Ship every key you define in all 13 files, even if some values
start out as English placeholders.

The Mod Builder's **TEXT** tab edits these files: pick a language, filter, edit values in place,
and add or remove a key across all 13 locales at once. Rows whose value still matches the English
one are flagged "same as English", with a count per language, so placeholder text is visible
rather than silent.

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

### 8.6 National goals (scenario `nationalGoalsFile`)

A scenario can bring its own national goals — the Agenda panel's goals, and the goals AI countries
pursue. The file is named by the scenario header's `nationalGoalsFile`, relative to the scenario
folder, and it **replaces** the base game's goals entirely: countries it does not list have no
agenda, and a file without `_BASIC` has no starter goals. It uses the base game's
`national_goals_2026.json` shape:

```json
{
  "_BASIC": { "goals": [
    { "id": "basic_secure_the_realm", "title_key": "mymod.goal.secure_realm",
      "description_key": "mymod.goal.secure_realm.desc", "type": "defense", "priority": "starter",
      "tasks": [ { "id": "war_chest", "title_key": "mymod.task.war_chest",
                   "condition": { "type": "treasury_above", "params": { "min_value": "5000" } } } ] } ] },
  "OTT": { "goals": [
    { "id": "ott_heir_of_rome", "title": "Heir of Rome", "title_key": "mymod.goal.heir_of_rome",
      "description_key": "mymod.goal.heir_of_rome.desc", "type": "territorial", "priority": "primary",
      "ai_weight": 0.9, "target_countries": ["BYZ"],
      "on_complete_effects": { "prestige": 50, "stability": 5 },
      "tasks": [ { "id": "war_on_byzantium", "title_key": "mymod.task.war_on_byzantium",
                   "condition": { "type": "declare_war_on", "params": { "target_iso3": "BYZ" } } } ] } ] }
}
```

- **Keys** are `_BASIC` (starter goals every country sees) or a country's upper-case code. Other
  `_`-prefixed keys are ignored as metadata.
- **`id`** is required and unique across the file; the player's active goal is saved by id. Starter
  goals appear in the planner's starter list only when their id starts with `basic_`.
- **`title_key` / `description_key`** are looked up in the mod's localization CSVs; `title` and
  `description` are the fallback text. The AI's copy of the goal uses `title` (or the key).
- **`type`**: `expansion`, `territorial`, `economic`, `unification`, `defense`, `prestige`,
  `diplomatic`, `ideological` (the AI understands these), plus `technology` and `intelligence` for the
  Agenda panel's task templates. **`priority`**: `starter`, `primary`, `secondary`, `aspirational`.
  Unknown values are reported and fall back to economic / secondary.
- **`ai_weight`** (0–1, default 0.5) and **`target_countries`** steer AI countries that pursue the goal.
- **`on_complete_effects`** — the AI applies `prestige`, `stability`, `aggression_modifier` and
  `military_modifier` when it completes a goal; the Agenda panel shows them as the reward.
- **`tasks`** are the player's steps. A goal without tasks gets a template from its `type`. Condition
  types and their `params`:

| `condition.type` | `params` |
|---|---|
| `own_provinces` | `province_owner` — counts owned provinces whose base-map country is this code |
| `alliance_with`, `declare_war_on`, `espionage_on`, `embassy_with`, `trade_agreement_with`, `defensive_pact_with`, `guarantee_independence`, `sphere_member` | `target_iso3` |
| `improve_relations` | `target_iso3` (optional), `min_value` (default 50) |
| `build_in_provinces` | `province_owner` (optional) |
| `recruit_units`, `military_units_above` | `unit_type`: `tanks`, `aircraft`, `ships`, `submarines`, `helicopters`, `apcs`, `artillery`, `personnel` — the count is the progress |
| `research_tech` | none — the number of completed doctrine tiers is the progress |
| `treasury_above`, `gdp_above` | `min_value`, in the base money unit |
| `tutorial_objective` | `objective_id` |

  `required_count` (default 1) is the progress a counting task needs, e.g. 10 for "own 10 provinces"
  or 5000 for "5,000 personnel"; yes/no conditions report 1 when met. Unknown condition types never
  progress.

A file that is not an object, uses a key that is not a country code, or has a goal without an id or
with a repeated id is rejected and the base goals stay; the Mods panel says why. The goals file is
part of the multiplayer lobby check.

### 8.7 Events (`Content/events/*.json`)

Every `*.json` file in `Content/events/` can hold any number of events, in any of three shapes:

```json
[ { "id": "my_event_a", ... }, { "id": "my_event_b", ... } ]
```
```json
{ "id": "my_event_a", ... }
```
```json
{ "events": [ { "id": "my_event_a", ... }, { "id": "my_event_b", ... } ] }
```

The envelope form is what the Mod Builder writes. Files load in file-name order (ordinal), mods in
mod-id order, and events in the order they appear in a file. Validate each event against
[`event.schema.json`](./schemas/event.schema.json).

#### Engine events and legacy events

An object **with a `type` field** (`scripted`, `procedural` or `reactive`) is an **engine event**.
At game start it is appended to the base game's event table and runs through the same engine as
the built-in events: monthly evaluation, conditions, the popup, AI choices, effects, chains, and
saves.

An object **without `type`** is a **legacy event**, and it behaves as before. It only appears when
a script fires it (`gp.fire_event` / `ModHookBus.FireEvent`), shows a popup whose buttons just
close it, and never fires on its own. Add `type` when you want the engine to run the event.

The effects decide too: an object that has `type` but writes any option effect as a string (the
old `"effects": ["stability:0.10"]` form) still loads as a legacy event, with a warning. Write
effects as objects (`{ "type": "modify_stat", ... }`) to run it in the event engine.

#### Ids

- Use lower-case ids (`a-z`, `0-9`, `_`), prefixed with your mod, e.g. `atlas_01`. The Mod Builder
  enforces this rule.
- An engine event whose id matches a base-game event, or an event that another mod loaded first, is
  **skipped**. It never replaces the other event. Use a new id to add an event.
- Saves store events by id, so renaming an event breaks it in existing saves.

#### Additions for mod events

| Field | Where | Meaning |
|---|---|---|
| `immediate: true` | event | No random roll. The event is eligible at the first monthly evaluation where all its conditions pass (MTTH 0). It can still lose: if other events are eligible for the same country in that evaluation, one is picked at random, weighted by `priority`. Use `priority: 10` for the best odds. If it loses, it tries again at a later evaluation, once the other event is answered and its cooldown has passed. Without `immediate`, `mean_time_to_happen_months` (default 12) sets the monthly chance, `1 - e^(-1/MTTH)`. |
| `target: "player"` | event | Only human-controlled countries can get the event. AI countries never roll it. In multiplayer, every human player can get it. |
| `fire_event` + `chain_event` + `delay_months` | option effect | Queues the event named by `chain_event` to fire `delay_months` later. `0` or no value uses the default (`chain_event_delay_months`, 1 month). The minimum is 1 month and the maximum is 600 months; a longer delay (or `chain_delay_months`) is cut to 600, with a warning. A month is 30 days. |
| `flag` | condition / effect | Same as `flag_name`. |
| `target` | condition / effect | Same as `target_country`. ISO3 codes are upper-cased. |
| `title_key`, `description_key`, option `text_key` / `tooltip_key` | event / option | Localization keys, looked up in your `Content/localization/<language>.csv`. The plain `title` / `description` / `text` / `tooltip` are the fallback. |

`change_government` accepts a government name as its `value`: `democracy`, `authoritarian`,
`hybrid`, `monarchy`, `theocracy`, `military_junta`, `one_party`, `communist_state` or
`transitional`.

#### When events fire

- **Monthly check.** Events are evaluated once per in-game month, on day 6–8, for every country.
  A game or scenario that starts after that day gets its first check on the first day it runs.
- **AI countries are staggered.** Each AI country rolls scripted and procedural events in about
  2.4 months per year: the countries are split into 5 groups, and one group rolls each month.
  Player countries roll every month. An `immediate` event for AI countries therefore arrives
  within the first few months after its conditions pass, not exactly on the first day.
- **One event at a time.** A country with an unanswered event gets no new scripted or procedural
  event that month.
- **Cooldown.** After a scripted or procedural event fires, that country gets no other scripted
  or procedural event for 60 days (`generated_post_event_cooldown_days`). After a reactive event the
  wait is 3 days (`reactive_post_event_cooldown_days`). `cooldown_months` adds a cooldown for one
  event.
- **Ties.** When several events are eligible in the same month, one is picked at random, weighted
  by `priority` (1–10).
- **Reactive events** fire from their `triggers` (`on_war_declared`, `on_coup`, …). A reactive
  event **without** triggers never fires on its own. It fires only as a chain target or from a
  script.
- **Choices.** AI countries choose an option automatically (`ai_weight` and the personality
  factors). The player sees a popup. If the player doesn't answer, the game picks an option after
  30 days (`player_event_auto_decide_days`).
- **Notification setting.** Players can hide less important popups. At "Important only",
  `social_cultural` and `technology_breakthrough` events are resolved with their **first option**
  and moved to the event log. At "Critical only", only `geopolitical_crisis`, `military_incident`,
  `natural_disaster` and `internal_politics` events show as popups. Use one of those four categories
  for story events the player must see.

#### Chains

A chain is an event-level `chain_event` (with `chain_delay_months`), or a `fire_event` effect on
one option. The effect form queues the follow-up only when the player or AI picks that option.

- **Recipient.** If the chained event is `specific_country`, it goes to that country. Otherwise it
  goes to the country that made the choice.
- **Conditions.** The chained event's own conditions are checked on the recipient when the chain
  comes due and the recipient can take it, not when it was queued. If they fail, the chain is
  dropped.
- **Fire once.** A chained `fire_once` event that the recipient has already had is dropped. A
  chained `target: "player"` event is dropped if the recipient is an AI country.
- **Busy recipient.** If the recipient already has an unanswered event, the chain waits. As soon
  as the queue is free, its conditions are checked and it fires.
- **No cooldown.** A chain ignores the 60-day cooldown, but it starts a new one when it fires.
- **Lookup order.** `chain_event` looks for your mod's events first, then the base game's. An id that
  matches neither is reported and the chain is dropped.

#### Condition support

| Condition | Works? | Notes |
|---|---|---|
| `date_after` | yes | `"YYYY-MM"` (a day part is ignored). Counts by month and includes the month itself: `"2026-06"` passes from June 2026. |
| `date_before` | yes | `"YYYY-MM"`, excludes the month itself. |
| `country_stat_gt` / `country_stat_lt` | yes | `field` + numeric `value`. Fields that work are listed below. Any other known field is always 0. |
| `at_war` / `not_at_war` | yes | Optional `target_country`: at war with that country. |
| `has_nuclear` | yes | The country has nuclear warheads. |
| `has_flag` / `not_has_flag` | yes | `flag_name` (or `flag`), set by `set_flag` or `gp.set_country_flag`. |
| `government_type` | yes | The same names as `change_government` above. |
| `continent` / `not_continent` | yes | `africa`, `americas`, `asia`, `europe`, `oceania`, `antarctica`. |
| `region` / `not_region` | yes | `northern_africa`, `sub_saharan_africa`, `latin_america_caribbean`, `northern_america`, `central_asia`, `east_asia`, `south_asia`, `southeast_asia`, `western_asia`, `eastern_europe`, `northern_europe`, `southern_europe`, `western_europe`, `australia_new_zealand`, `melanesia`, `micronesia`, `polynesia`. |
| `country_unrest_gt` / `country_unrest_lt` | yes | Average national unrest, 0–100. |
| `owns_province` / `not_owns_province` | yes | `value`: a province id (a whole number, e.g. `2276`). True when the country is the province's **legal owner**. Optional `target_country`: test that country instead. See [Province conditions](#province-conditions). |
| `controls_province` / `not_controls_province` | yes | `value`: a province id. True when the country **controls** the province: it occupies it, or owns it and nobody occupies it. Optional `target_country`. See [Province conditions](#province-conditions). |
| `has_tech`, `province_stat_gt`, `alliance_member`, `relation_above` / `relation_gt` / `relation_below` / `relation_lt`, `defcon_level` | **no** | Accepted, but the engine doesn't check them yet. They always fail, or compare against 0. You get a warning at load. |
| `active_law_is` | **no** | Rejected in mod events for now. |

Stat fields that `country_stat_gt` / `country_stat_lt` read: `economy.gdp`,
`economy.gdp_per_capita`, `economy.gdp_growth_rate`, `economy.inflation_rate`,
`economy.debt_to_gdp`, `economy.unemployment`, `economy.hdi`, `government.stability`,
`government.corruption`, `government.economic_stance`, `government.social_stance`,
`military.manpower`, `military.reserve`, `military.defense_budget`, `military.tanks`,
`military.aircraft`, `military.ships`, `military.nuclear_warheads`, `budget.tax_rate`,
`budget.treasury`, `budget.military_pct`, `budget.research_pct`.

#### Province conditions

`owns_province`, `not_owns_province`, `controls_province` and `not_controls_province` let an event
fire when a province changes hands. `value` is the province id from the game's province registry
(the Mod Builder's province picker shows it as "Name (id)").

```json
{ "type": "controls_province", "value": 2276, "target_country": "OTT" }
```

- **Owns** means the legal owner. It changes only when the province is transferred, for example
  by a peace deal. Taking the province with an army does **not** change the owner.
- **Controls** means the occupier, if the province is occupied, otherwise the owner. It changes as
  soon as an army captures the province, before any peace deal.
- **Subject.** Without `target_country` the condition tests the country that would get the event.
  With it, the condition tests the named country instead. The example above is true for **every**
  country once the Ottomans (`OTT`) control İstanbul (2276). An `any_country` event with it and
  `{ "type": "continent", "value": "europe" }` therefore goes to every European country. Add
  `{ "type": "not_controls_province", "value": 2276 }` to leave out the Ottomans themselves.
- A `target_country` that no longer exists owns and controls nothing, and so does any country for an
  unknown province id. The `not_` variants are then true.
- **Timing.** Conditions are checked at the monthly evaluation, not at the moment of capture. A
  player country is checked every month. An AI country rolls scripted events about 1 month in 5,
  so an AI recipient can get the event a few months after the capture. `immediate: true` removes the
  random roll, but still waits for that country's next evaluation.
- An event that should fire once per country when a province changes hands needs `fire_once: true`.
  Otherwise it can fire again every time its conditions pass, after its cooldowns.

#### Effect support

| Effect | Works? |
|---|---|
| `modify_stat`, `add_relation`, `set_flag`, `clear_flag`, `add_treasury`, `modify_unrest`, `impose_sanction`, `lift_sanction`, `engage_diplomatically`, `withdraw_forces`, `change_government`, `modify_resource_price` (alias `global_modifier`), `fire_event` | yes |
| `declare_war`, `create_unit`, `annex_province`, `start_research` | **no**: accepted, but they do nothing yet (warning at load) |

#### Errors

Mod events are checked strictly. These problems **skip the whole event**:
- an unknown `type`, `category`, `target`, condition, effect or trigger type;
- an unknown stat `field`;
- a date that isn't `"YYYY-MM"`;
- a province condition whose `value` isn't a whole number of 1 or more;
- an unknown continent, region or government name;
- a `specific_country` event without `target_country`;
- fewer than 1 or more than 6 options;
- a `fire_event` without `chain_event`, or a flag effect or condition without a flag name.

A duplicate id skips the later event. An unknown chain target keeps the event and drops the chain.
Text longer than its field is cut off, with a warning: 125 bytes for titles, keys and option
labels, 509 bytes for tooltips.

Where problems appear:
- the Loadout screen's error bar;
- the Mods panel;
- the Mod Builder's Reload & Test;
- `Player.log`.

Each message names the mod, the file, the event id and the reason. Two problems are found only
when your events are added to the game's event table, once per session shortly after the mods
load: an id that matches a base-game event, and a chain target that matches no event. They appear
in the Loadout screen's error bar and in `Player.log`, but not in the Mod Builder's Reload & Test.
Restart the game to check them again after a fix. A text that is cut off at that point is a
warning only: it is logged, but the mod is not marked as failing.

#### Firing from a script

`gp.fire_event(country, "event_id")` (and `ModHookBus.FireEvent`) looks the id up among the base
game's events and every active mod's engine events. A match is added to that country's queue
**immediately**, without checking conditions, `target`, `fire_once` or cooldowns: the script
decides. If the id isn't an engine event, a legacy event with that id is shown instead. See the
[WASM Scripting Guide](./WASM_SCRIPTING_GUIDE.md).

#### Saves and multiplayer

- Mod events are saved by id. If you load a save after removing or renaming an event, its pending
  entries for that event are dropped, with one warning.
- Every `Content/events/*.json` file is part of the multiplayer lobby check. Players with
  different event files can't join the same game.

#### Example

[`examples/atlantis/`](./examples/atlantis/) is a complete two-event chain. `atlas_01` fires once
for the player from June 2026. Its "Send an expedition" option sets a flag and queues `atlas_02`
one month later. The "Leave it" option sets a different flag, so `atlas_02` never comes. The example
includes English and Turkish text.

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

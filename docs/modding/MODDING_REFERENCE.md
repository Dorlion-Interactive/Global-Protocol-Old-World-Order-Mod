# NewWorldOrder – Modding Reference

Last updated: 2026-09-28

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
  images/events/             ← your own event pictures, named by an event's "image" (§8.4, §8.7)
  overrides/                 ← sparse config overrides (§8.2)
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

**One mod per folder.** A `mod.json` inside another mod's folder (a `workshop_content/` staging
copy, an old backup, a sample mod) never loads: discovery keeps the outer mod and lists the inner
file in the Mods panel and in the Mod Builder's Reload & Test message. When two folders in the same
mods folder use the same `id`, the shallowest one loads (a tie goes to the path that sorts first,
by character code) and the Mods panel warns about the other. Keep the folder name equal to the `id`
so this is easy to spot.

**What a Workshop upload contains.** PUBLISH uploads a clean copy of the mod folder, never the
folder itself. The copy leaves out, at any depth: `bin/`, `obj/`, `.git/`, `.vs/`,
`workshop_content/`, `__MACOSX/`, `*.pdb`, backups ending in `.bak` (also `.bak2`-style and
`.bak-<date>` copies), `.DS_Store`, `Thumbs.db`, `desktop.ini`, `._*`, symbolic links, and every
subfolder that has its own `mod.json`. To leave out more, add a `.modignore` file to the mod root.
It is never uploaded itself, and it cannot leave out the root `mod.json`, which always ships. Example:

```
# One pattern per line. A line starting with # is a comment.
# No "/": matches a file or folder name anywhere.
*.psd
# A leading "/" or an inner "/": a path from the mod root.
/notes.txt
# A trailing "/": folders only.
drafts/
# "*" stays within one folder, "**" crosses folders, "?" is one character.
docs/**/*.md
```

Matching ignores case. A `#` after a pattern is part of the pattern, not a comment. `!` (re-include) lines are not supported and are skipped. The PUBLISH tab
shows the file count, the upload size and what is left out before you press the button.

**Validate Mod.** The Mod Builder's **VALIDATE** button (next to SAVE ALL) saves your edits, then
checks the mod folder without loading it and lists what it finds, grouped by file. Click a line to
open the tab that edits that file; **COPY REPORT** copies the list as plain English text for a bug
report. Only the files the upload would contain are checked. The checks:

- **Schema.** `mod.json`, `Content/currencies.json`, the split scenario files and the scenario's
  national goals file are checked against the JSON Schemas in `schemas/` (the same files
  `DataPipeline/validate_all.py` reads); a mismatch is an error. The sparse `overrides/*.json` files
  and the `Content` rosters only list what they change, so they are checked without the required
  fields, and a mismatch is a warning. A roster field set to `null` where the schema wants text
  (`"required_building": null`) reads as unset, so it is not reported. A field the schema does not
  know is a warning, because the game ignores it (usually a misspelling). A JSON file under
  `Content/` or `overrides/` that the game never reads is a warning.
- **Manifest.** The id format and whether the folder is named after the id (warnings); a semver
  `version` (error); a `wasmAbiVersion` and `managedSdkVersion` this game supports (errors); every
  path the manifest names must exist and be part of the upload (`iconPath` / `thumbnailPath`:
  warnings; `entrypoints` and the scenario paths: errors); `gameVersion` (a range the game cannot
  read is an error, a range the running game is outside is a warning); `dependencies` (a malformed
  entry or the mod itself: errors; not installed here, or installed at a version outside the
  range: warnings).
- **Content.** The scenario loads, the files it names exist, the content roster checks Reload &
  Test runs, the `game_settings` sections the game does not apply (§8.2), text keys defined in some
  languages but not in others (§8.3), and the EVENTS tab's checks (§8.7).
- **Packaging.** Folders with their own `mod.json`, and a note of what the upload leaves out.

**PUBLISH runs the same check first.** Any error stops the upload before Steam is contacted (no
Workshop item is created), and the report opens. Warnings stop it once: press the button again to
publish with exactly those warnings; a warning that was not there the first time asks again.

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
| `version` | string | ✓ | Semver `MAJOR.MINOR.PATCH`, e.g. `1.0.0`. Validate reports any other form, and `id@range` dependencies are matched against it |
| `gameVersion` | string | | Semver range of game versions the mod was made for, e.g. `^0.5.0` (§2.3). Outside it the Loadout row shows a warning badge; the mod still loads |
| `author` | string | | Author display name |
| `description` | string | | Short description |
| `tags` | string[] | | Category tags. Informational: they never change how the mod loads |
| `dependencies` | string[] | | Mods that must be enabled for this one to load: `"other.mod"` or `"other.mod@^1.2.0"` (§2.3) |
| `loadOrderHint` | int | | Load position among independent mods: lower first, higher later (wins conflicting overrides; an engine event id stays with the first mod). Default `0` (§2.3) |
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

The WASM module the game loads and every `Mods/*.dll` are part of the multiplayer lobby check: players whose script files differ in any byte can't join the same game, even with the same mod id and version. The hooks a script can handle, and the functions it can call, are listed in the [WASM Scripting Guide](./WASM_SCRIPTING_GUIDE.md) (§3 and §4).

### 2.2 Component Runtime Opt-In

Set `enableComponentRuntime: true` only when your WASM binary is component-model format.
Core WASM modules should leave this `false`.

### 2.3 Load Order, Dependencies and Game Version

Every stage that layers mods (content rosters, config overrides, events, localization, icons)
applies them in one load order. A later mod wins where two mods change the same thing, with one
exception: an engine event's `id` (§8.7) belongs to the first mod in load order that defines it. A
later mod's engine event with the same `id` is skipped with a load error, and the earlier one stays,
so a patch mod cannot replace another mod's event: ship yours under a new `id` (the original
still loads). The game computes the order from the enabled mods' manifests:

1. **Dependencies first.** A mod always loads after every mod in its `dependencies`.
2. **Then `loadOrderHint`,** ascending, among mods that do not depend on each other. The default is `0`.
   Use a negative hint for a base or library mod, and a positive one for a patch meant to win.
3. **Then the mod id,** ordinal, to break ties. With no dependencies and no hints anywhere, the
   order is simply alphabetical by id, as before.

The Loadout panel shows each enabled mod's position as `[n]`. There are no up/down buttons.
In multiplayer every player must load the same mods in the same order. The order therefore
comes only from the manifests, never from one player's list. The lobby's mod-set check covers
the ordering fields.

**Dependencies** are written as `"other.mod"` (any installed version) or `"other.mod@range"`. A
mod does not load, and shows a red badge and a load error on the Mods panel, when a dependency:

- is not installed;
- is installed but not enabled (enable it and reload; the mod stays enabled meanwhile);
- has a `version` outside the range, or one that is not semver;
- could not load itself;
- is part of a dependency cycle.

A malformed entry and a mod that lists itself are errors too. Other mods keep loading.

**Ranges** (for `dependencies` and `gameVersion`) use the npm style:

| Form | Means |
|---|---|
| `1.2.3` or `=1.2.3` | exactly that version |
| `>=1.2.0`, `>1.2.0`, `<2.0.0`, `<=1.4.0` | comparisons |
| `>=0.5.0 <0.7.0` | both (space = AND) |
| `^1.2.3` | `>=1.2.3 <2.0.0` (for `^0.5.1`: `>=0.5.1 <0.6.0`) |
| `~1.2.3` | `>=1.2.3 <1.3.0` |
| `1.2`, `1.2.x`, `1`, `*` | any matching version (`*` = any) |
| `1.2.3 - 2.0.0` | inclusive range |
| `^1.0.0 \|\| ^2.0.0` | either (`\|\|` = OR) |

Pre-release versions (`1.0.0-beta.1`) compare by semver precedence. A `v` prefix is not
accepted.

**`gameVersion`** is compared with the running game's version (for example `0.5.10`). Outside the range, the mod still loads. Its Loadout row shows an amber badge and the
Mods panel lists a warning. An unreadable range gets the same badge.

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
| `gdpScale` | float | 1.0 | Multiplies every country's GDP, GDP per capita, exports, imports, foreign reserves, treasury and opening monthly budgets (revenue, expenses, defense, research) once, when a new game starts. Tutorial treasury rewards are paid times this scale too, capped at `economy.max_single_event_treasury_gdp_fraction` of the player's GDP (5%, the cap event treasury effects get). `countryStateOverrides` values are absolute and are applied after it; a country whose `gdp` is overridden has its opening monthly budgets and its trade (exports, imports and the tariff and commercial-hub revenue they bring) re-based on that GDP. |
| `unownedProvincePopulationScale` | float | 1.0 | Multiplies the population of every province still unowned after `removeCountries` and the ownership overrides, once, when a new game starts. Provinces are baked with 2026 headcounts, which unowned land brings back when it is colonised; a historical scenario sets this to roughly its declared world population divided by the 2026 population of the provinces its countries own. A scaled province keeps at least 100 people (or its own population, if smaller). Owned provinces follow each country's declared `population` instead (§4.1). |
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
| `templateISO3` | string | Existing country to copy from: economy, military, AI personality, political starting state and every field the entry leaves out. There is no fully custom country: when omitted, the country with the alphabetically first ISO3 (`ABW`, Aruba, in the base game) is used and a warning is logged; its identity fields (below) are not copied. Ignored for a re-skin (below). |
| `name` | string | Display name |
| `mapColor` | string | Hex color `#RRGGBB` |
| `flagPngPath` | string | A 128×80 flag PNG. A relative path is looked up in the mod folder (the one holding `mod.json`) first, then in the scenario folder (the split scenario folder, or the folder of a single-file scenario); an absolute path is used as is. The game and the Mod Builder preview use the same rule. A path that matches no file is listed in the Mods panel, and the country shows the base game's flag for its ISO3 (a re-skin) or an empty flag frame (a new ISO3). A changed flag shows when the scenario is loaded again (a new game, or the Mod Builder's Reload & Test). |
| `capital` | string | Capital city display name |
| `capitalProvince` | string | Province name or numeric ID string |
| `population` | int | Total population, spread over the country's provinces (see **Population** below) |
| `areaKm2` | number | Territory area in km² |
| `governmentType` | string | See §9.1 |
| `governmentSubtype` | string | See §9.8 |
| `ideology` | string | See §9.2 |
| `militaryUnitTypeIds` | string[] | The country's **unit roster** (§6.1). Non-empty: the country recruits only these unit types plus any it owns. Empty or omitted: the default set. |
| `neighbors` | string[] | Land-adjacent ISO3 codes |
| `seaNeighbors` | string[] | Sea-adjacent ISO3 codes |
| `leaderTitle` | string | Override leader title (e.g. `"Chancellor"`) |
| `leaderName` | string | Override leader name |
| `homelandTerm` | string | Override homeland noun (e.g. `"Federation"`) |
| `continent` | string | See §9.3 |
| `region` | string | See §9.4 |
| `neutral` | bool | Military neutrality. Omitted keeps the template's flag. An AI-controlled neutral forms no military alliances or defense pacts, gives no guarantees, joins no coalitions and answers no calls to arms (it still honors guarantees it already holds, and calls its own allies when attacked). A human player is unrestricted. |
| `dominantReligion` | string | Largest religion, e.g. `"Islam"` (max 29 bytes, see below). Drives kinship (below) and the religiosity of the interest groups. |
| `dominantEthnicity` | string | Largest ethnic group, e.g. `"Turkish"` (max 29 bytes). Drives kinship (below). |
| `primaryCulture` | string | Culture shown on the country overview, e.g. `"Ottoman"` (max 29 bytes) |
| `ethnicHomogeneity` | number | 0 (very diverse) to 1 (homogeneous); shown on the country overview when a culture or ethnicity is set |

**Reusing a base-game ISO3 (re-skin).** An entry whose `iso3` the base game already has (for
example `FRA` in a 1450 scenario) does not create a second country: its fields are applied onto the
existing one — name, map colours, leader, government, ideology (which reseeds the electorate, as in
§4.3), neutrality, homeland term, area, capital, continent, region, the identity fields and
population (both below). The roster (`militaryUnitTypeIds`) and `flagPngPath` apply per ISO3
either way. Anything the entry leaves out keeps the existing country's value, and the country
keeps its own provinces, economy, military, relations and politics; use `countries_state` (§4.3)
and `provinces_ownership.json` (§5) for those. That includes its starting missile stockpile
(nuclear warheads, cruise and ballistic missiles): `disabledUnitCategories` `Missile` switches off
missile units, not the stockpile. `templateISO3`, `neighbors` and `seaNeighbors` do
not apply to an existing country. The log prints one line per re-skinned ISO3. If `addCountries`
lists the same ISO3 twice, only the first entry is applied (with a warning). A new `name` replaces
the base game's `country.name.<ISO3>` text in every language your CSV does not translate (§8.3);
put its translations there.

A re-skinned country keeps **every base-game province that no ownership override (§5)
reassigns**, even when `removeCountries` also lists it (§4.2), and its declared `population` is
spread over those provinces too. Give each such province to a country in
`provinces_ownership.json`, or see §4.2 to leave it unowned. For example, a 1450 `COL`
(Electorate of Cologne) that is only given Nordrhein-Westfalen still owns Colombia's other
departments, and most of its people would live there.

**Identity and kinship.** Two countries with the same `dominantReligion`, or the same
`dominantEthnicity`, are kin: their relations warm over time, and the AI is slower to attack and
quicker to ally with them. Generic labels (`None`, `Other`, `Mixed`, `Unknown`, `European`,
`White`, `Black`, ...) and empty values are never kin. A label is stored in 29 bytes of UTF-8:
29 ASCII letters, but fewer accented or non-Latin ones (a Cyrillic letter takes 2 bytes, a CJK
character 3). A longer label is cut short and a warning is logged; the schema's `maxLength`
counts characters and cannot catch this. Each of the four identity fields, when
omitted, keeps the template's value; without a `templateISO3` all four start empty (the overview
shows "—" and the country has no kin) rather than inheriting the fallback's. A re-skin applies the
fields it sets and keeps the rest. Labels are shown translated through the
`demographics.religion.<Label>` and `demographics.identity.<Label>` localization keys (§8.3);
a label without a key is shown as written, with underscores as spaces.

**Population.** A declared `population` is made true of the provinces, not only of the country
record. Once `removeCountries` and the ownership overrides (§5) are done, the country's provinces
are rescaled in proportion to their baked (2026) populations so they sum exactly to the declared
figure; each keeps at least 100 people when the total allows it. Without this the monthly
population update, which re-adds a country's provinces, would bring the 2026 headcounts back. A
country that owns no province keeps the figure only until that first update (a warning is logged).
A `countries_state` `population` (§4.3) does the same for any country and wins over this one.
An `addCountries` `population` below the template's (or, for a re-skin, below the country's own)
also scales down the AI's peacetime army floor, which the country otherwise inherits as a 2026
active-duty headcount: a country with a tenth of the people keeps a tenth of it. A larger
population never raises it, and a `countries_state` `population` does not change it.
Provinces left unowned keep their 2026 people unless the header sets
`unownedProvincePopulationScale` (§3.3). All of this happens once, when a new game starts; saves
and multiplayer joins keep the populations they carry.

### 4.2 Removing Countries (`removeCountries` / `countries_remove.json`)

An array of ISO3 strings: `["XXX", "YYY"]`

An ISO3 that `addCountries` also lists is never removed: its entry re-skins the existing country
instead (§4.1). Listing it in both files states the intent, but the country is **not** cleared:
it keeps every province of the base country that no ownership override reassigns (§4.1).

To leave a province unowned, assign it in `provinces_ownership.json` to a country your scenario
removes and does not re-add. After the ownership overrides, land held by a removed country is
turned into unowned land.

A removed country takes its base-game military with it: its armies, fleets and air wings are destroyed at game start, whether or not the scenario disables any unit types. A code the same scenario re-adds through `addCountries` is not removed, so it keeps its military. Loading a save never removes stacks; the save already holds the stacks the game had.

### 4.3 State Overrides (`countryStateOverrides` / `countries_state.json`)

| Field | Type | Description |
|---|---|---|
| `iso3` | string | **Required.** Target country |
| `clearRelationships` | bool | Clear this country's diplomatic state |
| `clearDiplomacyScope` | string | `"core"` or `"extended"` |
| `governmentType` | string | New government type |
| `ideology` | string | New ideology |
| `techLevel` | int | Starting Knowledge Network level: tiers 1 to `techLevel` of every doctrine branch start completed (doctrine A), except branches hidden by `disabledDoctrineBranches` (§3.3). A branch has 5 tiers, so 6–10 act as 5; tiers the country already has are kept. New games only. 0 or omitted grants nothing. **Check existing mods:** this field did nothing until 2026-09, and older Mod Builder versions wrote `techLevel: 5` into every new override. Remove it, or set it to 0, unless you want the tiers. |
| `stability` | float | 0.0–1.0 |
| `corruption` | float | 0.0–1.0 |
| `treasury` | number | Treasury balance in US dollars (not millions) |
| `gdp` | number | Annual GDP in US dollars (not millions) |
| `manpower` | int | Available manpower in people (not thousands) |
| `reserve` | int | Reserve pool in people (not thousands) |
| `population` | int | Starting population, spread over the country's provinces like an `addCountries` population (§4.1). Wins over an `addCountries` population for the same country. 0 or omitted keeps the current one. |
| `neutral` | bool | Sets (`true`) or clears (`false`) military neutrality; omitted keeps the baked flag (see §4.1) |
| `militaryUnitTypeIds` | string[] | Gives an existing country a unit roster (§6.1); replaces an `addCountries` roster for the same country |
| `dominantReligion` | string | Sets the largest religion (see **Identity and kinship**, §4.1); omitted keeps the current one |
| `dominantEthnicity` | string | Sets the largest ethnic group (§4.1); omitted keeps the current one |
| `primaryCulture` | string | Sets the culture shown on the country overview; omitted keeps the current one |
| `ethnicHomogeneity` | number | 0–1; omitted keeps the current value |

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

Region names match the `WorldRegion` enum — see §9.4.

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

**Who can recruit a unit type**, in this order:

1. A disabled category or unit id (§3.3) is never available.
2. A country always has the unit types it owns (`ownerIso3`).
3. A country with a **roster** — a non-empty `militaryUnitTypeIds` in `addCountries` (§4.1) or
   `countryStateOverrides` (§4.3) — recruits only the unit types its roster lists. A roster is an
   explicit grant: it may list another country's exclusive unit (e.g. Tver's roster granting
   Muscovy's streltsy).
4. With `restrictOwnersToOwnedUnits` (§3.3), a country that owns unit types recruits nothing else.
5. Otherwise a country has every unit type except the ones exclusive to other countries.

Roster ids are matched case-insensitively. Ids no unit definition has, and rosters for countries the
game does not contain, are reported as warnings at game start.

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
- `missionType`: a value from §9.6, e.g. `"CloseAirSupport"` (the older `"cas"`, `"interception"`, `"strategic_bombing"`, `"naval_strike"`, `"patrol"` and `"standby"` still work)
- `readiness`: 0–1, -1 = full

---

## 7. Permissions

Declare required permissions in `mod.json`:
```json
{ "permissions": ["ReadEconomy", "WriteTreasury", "InjectUI"] }
```

| Permission | Description |
|---|---|
| `ReadEconomy` | Nothing yet: every read (treasury, GDP, stability, manpower, tech level, date) works without it. Accepted so existing manifests stay valid. |
| `WriteTreasury` | Change a country's treasury (`country_set_treasury`, `add_treasury`) |
| `FireTriggers` | Queue events and raise reactive triggers (`fire_event`, `fire_trigger`, `ModHookBus.FireEvent`) |
| `WriteFlags` | Set or clear a country's event flags, the flags that `has_flag` / `not_has_flag` event conditions test. There is no WASM import for this yet; only C# mods can do it (`ModGameActionRequest.SetCountryFlag` / `ClearCountryFlag`). It has nothing to do with flag or banner images. |
| `InjectUI` | Add UI elements to the HUD (`inject.json`) and show popups (`show_mod_popup`) |

A call that needs a permission the mod did not declare does nothing.

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

**Load order.** Files apply in load order: every active mod in the order of §2.3 (alphabetical by
mod id unless mods declare `dependencies` or `loadOrderHint`), then the active scenario's override
file. A later merge file wins on any field it sets and can bring back a
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

**Names and descriptions.** An entry's `name` (a building reads `display_name` first; a resource
uses `display_name`) and its `description` are what the game shows for that id. At load they become
the localization rows the UI reads — `building.<id>.name` / `.description`, `unit.<id>.name` /
`.description`, `resource.<Resource>.name` / `.description` — for every language whose
`Content/localization/<lang>.csv` does not define that key (an empty value counts as not defined).
So a re-skinned base building shows its new name and description instead of the base game's, and
a row in your CSV still wins for its language: put translations there (§8.3). An entry whose name
or description is the same as the base game's registers nothing, so copying a base entry just to
re-price it keeps the base game's translations.

**Units** name the building they are recruited at in `cost.required_building`. A unit whose building
is missing or switched off can never be recruited; the Mods panel says so, and names the doctrine
branch when that is why the building is gone.

**Doctrine gates.** A building or unit whose `prerequisites.tech` names a tier of a hidden doctrine
branch (`disabledDoctrineBranches`, or a branch a replace-mode `doctrines.json` leaves out, §8.2) is
never offered. The Mods panel warns for the entries your roster lists; set their `prerequisites.tech`
to `"none"` or to a tier of a branch the game shows. Base-game entries your roster does not list go
quietly with their branch, except the buildings the engine finds by id (table above): for those the
warning names the branch, because re-skinning the id alone keeps the base game's gate — list it with
its own `prerequisites.tech`.

`prerequisites.tech` must be `"none"` or `<branch>_t<tier>`: a branch id from doctrines.json exactly
as written there (`military`, `industry`, `cyber`, …, see §3.3) and a tier from 1 to 5, e.g.
`"industry_t2"`. The game compares the key exactly, so `"None"`, `"Industry_t2"`, a branch that
does not exist or an old tech-tree id such as `"cyber_operations"` can never be met, and the entry
stays locked for the whole game. The Mods panel and the Mod Builder's checks box warn about such a
key on any entry your roster lists.

**Resources** are a fixed set: the ids of the base game's `resources.json` (`Oil`, `Uranium`,
`Semiconductors`, …, matched case-insensitively). A mod can re-price, re-skin or switch them off,
but cannot add new ones; unknown resource ids are reported. A scenario takes modern commodities out
of an earlier era with its `resourcesOverrideFile` (§3.3), applied after every mod's
`Content/resources.json` like the other scenario override files:

```json
{ "disabled": ["Oil", "NaturalGas", "Uranium", "Lithium", "Semiconductors", "Batteries", "SolarPanels"] }
```

A `"mode": "replace"` file lists the resources the scenario keeps instead, and switches off every
resource it does not list. A switched-off resource is no longer produced, by buildings or by
province land, and is hidden from the spot market, trade-agreement proposal and resource overview
screens.

**In the Mod Builder** (Content tab) the roster mode sits at the top of each file. In replace mode
the base entries you have not included are listed as switched off, each with an Include button, plus
Include all to start from a copy of the base game. Add brand-new ids (optionally copying an existing
entry), switch entries off, and set each entry's inherit flag right on its card. The checks box below
runs the same checks as the game's loader while you edit. The scenario header's disabled lists are
checklists of the game's real building, unit, category and branch ids on the Scenario tab.

**`Content/tech_tree.json` is retired.** Research is the Knowledge Network (`overrides/doctrines.json`,
§8.2). The file is ignored with a warning (an empty one, which older Mod Builders created in every
mod, is ignored without one), and so is a scenario's `techOverrideFile`. To keep modern
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
| `game_settings.json` | Balance sections applied at runtime: population, diplomacy, advanced diplomacy, world order, AI weights, fog of war, intelligence, map interaction, satellite, military and buildings, plus `events` and `envoys` (see below for the ones that are not) |
| `doctrines.json` | Doctrine values, effects and text |
| `game_flow.json` / `events.json` / `envoys.json` | The matching `game_settings` sections, kept as separate files for backwards compatibility |
| `military_markers.json` | Map marker appearance |

**Sections the game does not apply yet.** `economy`, `technology`, `step42_diplomacy` and
`political_drift` are in `game_settings.schema.json`, but no runtime stage reads them from a mod:
values you write there are ignored. The Mod Builder's SETTINGS tab does not show them, Reload &
Test and the Mods panel list any you wrote by hand ("… are not applied at runtime yet and were
ignored"). They will become moddable once the runtime can re-bake those config blobs.

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

**Content names and descriptions** from your content rosters (§8.1) fill the
`building.<id>.*` / `unit.<id>.*` / `resource.<Resource>.*` rows of every language your CSV does
not define, so a re-skin is never hidden behind the base game's text. The `name` of an
`addCountries` entry that re-skins a base-game country (§4.1) fills `country.name.<ISO3>` the same
way. A row in your CSV wins for its language; that is where translations of those names go.

**Script popups.** `ModHookBus.ShowPopup(modId, title, body)` (C#) and the `show_mod_popup` import
(WASM) take plain text, and there is no lookup call in the scripting API yet. Instead, a title or
body that is **exactly a localization key** — no spaces or commas, with at least one dot inside,
e.g. `mymod.popup.intro.title` — is shown as that key's text in the player's language. Any other
text is shown as written, so English literals keep working. The same rule applies to a legacy
event's `title`, `description` and option `text` (§8.7). The key follows the rule above: define it
in all 13 files. Players see the key itself in a language you left out, or whose row for it is
still empty (the Mod Builder adds a new key to the other 12 files with an empty value).

```csharp
ModHookBus.ShowPopup("mymod", "mymod.popup.intro.title", "mymod.popup.intro.body");
```

### 8.4 Icons

A mod replaces the picture of a building, unit, resource or doctrine by shipping an image named after
its id. The game looks for mod icons first and falls back to the base game's art.

| Folder | File name | Shown in |
|---|---|---|
| `icons/buildings/` | building id, e.g. `castle.png` | Build menus, province view, tooltips, research unlock chips |
| `icons/units/` | unit id | Recruitment, army cards, unit lists |
| `icons/resources/` | resource id, e.g. `oil.png` | Resource panels and tooltips |
| `icons/doctrines/` | the doctrine's `icon` id from doctrines.json | Research screen cards, milestones, hidden cards |
| `images/events/` | an event's `image` name, e.g. `atlas_city.png` | The event popup's picture and the Mod Builder's event preview (§8.7) |

- `.png`, `.jpg` and `.jpeg` are read; if one id has both a `.png` and a `.jpg`, the `.png` wins.
- `Content/icons/...` is read too, after `icons/...`, and `Content/images/events/` after
  `images/events/`.
- An event picture can use a new name (your own events pick it with `image`) or a base picture's
  name, which replaces that picture for every event that uses it.
- When several active mods ship the same icon or event picture, the mod that loads last (§2.3)
  wins — the same order as content rosters.
- New ids you add to a roster (§8.1) get their icon the same way.
- Icons and event pictures are presentation only and are not part of the multiplayer lobby check.
- Map markers are drawn per unit **subcategory**: set those with `overrides/military_markers.json`
  (`subcategory_icons`).

The Mod Builder's Content tab has an icon picker on every building, unit and resource card, and the
Doctrines tab lists every doctrine icon id with a picker; both copy your image to the right place.
Event pictures have no import button yet: copy the file into `images/events/` yourself. The Events
tab's image picker then lists it first (the picker needs a loaded map; without one, type the name).

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
| `alliance_with` | `target_iso3` (one country) **or** `partners` — a comma-separated ISO3 list (`"ISR,SAU,ARE"`), or `"*"` for any country. Progress is the number of distinct listed countries holding a bilateral alliance or a Defense Pact treaty with the owner; collective-defense memberships such as NATO do not count. `required_count` is the target |
| `declare_war_on`, `espionage_on`, `embassy_with`, `trade_agreement_with`, `defensive_pact_with`, `guarantee_independence`, `sphere_member` | `target_iso3` |
| `improve_relations` | `target_iso3` (optional), `min_value` (default 50) |
| `build_in_provinces` | `province_owner` (optional) |
| `recruit_units`, `military_units_above` | `unit_type`: `tanks`, `aircraft`, `ships`, `submarines`, `helicopters`, `apcs`, `artillery`, `personnel` (or `active_personnel`) — the count is the progress. `military_units_above` also takes `min_value`, the count to reach, used when `required_count` is absent |
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
load order (§2.3), and events in the order they appear in a file. Validate each event against
[`event.schema.json`](./schemas/event.schema.json).

#### Engine events and legacy events

An object **with a `type` field** (`scripted`, `procedural` or `reactive`) is an **engine event**.
At game start it is appended to the base game's event table and runs through the same engine as
the built-in events: monthly evaluation, conditions, the popup, AI choices, effects, chains, and
saves.

An object **without `type`** is a **legacy event**, and it behaves as before. It only appears when
a script fires it (`gp.fire_event` / `ModHookBus.FireEvent`), shows a popup whose buttons just
close it, and never fires on its own. Add `type` when you want the engine to run the event. A legacy
event's `title`, `description` and option `text` may each be a localization key, shown in the
player's language (§8.3, "Script popups").

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
| `immediate: true` | event | No random roll (MTTH 0). The event fires at the first monthly evaluation where all its conditions pass. It ignores the 60-day cooldown left by an earlier event and always beats ordinary events in that evaluation. If several `immediate` events are eligible, the highest `priority` fires first; on a tie, the one loaded first. It still waits while the country has an unanswered event, and it still respects its own `cooldown_months`, `fire_once` and `target`. An `immediate` event that can repeat (no `fire_once`) and has no `cooldown_months` waits the 60 days after each of its own firings, and while its conditions hold it beats ordinary events every time: give it `fire_once`, `cooldown_months` or a condition that stops passing. `mean_time_to_happen_months: 0` without `immediate` works the same way, with a load note. Without `immediate`, `mean_time_to_happen_months` (default 12) sets the chance per roll, `1 - e^(-1/MTTH)`. An AI country rolls scripted events in 1 month out of 5. A human country rolls every month at 5× the MTTH, so over those 5 months its chance per event is the same as the AI's. `target: "player"` and `specific_country` events are the exception: humans roll them every month at the MTTH you wrote. |
| `target: "player"` | event | Only human-controlled countries can get the event. AI countries never roll it. In multiplayer, every human player can get it. |
| `fire_event` + `chain_event` + `delay_months` | option effect | Queues the event named by `chain_event` to fire `delay_months` later. `0` or no value uses the default (`chain_event_delay_months`, 1 month). The minimum is 1 month and the maximum is 600 months; a longer delay (or `chain_delay_months`) is cut to 600, with a warning. A month is 30 days. |
| `flag` | condition / effect | Same as `flag_name`. |
| `target` | condition / effect | Same as `target_country`. ISO3 codes are upper-cased. |
| `title_key`, `description_key`, option `text_key` / `tooltip_key` | event / option | Localization keys, looked up in your `Content/localization/<language>.csv`. The plain `title` / `description` / `text` / `tooltip` are the fallback. |
| `image` | event | The popup's picture, by file name without extension. The game looks in the active mods' `images/events/` and then `Content/images/events/` folders first (`.png`, `.jpg` or `.jpeg`; `.png` wins when one name has both; when several active mods ship a name, the mod that loads last wins), then in the base game's pictures (e.g. `event_airstrike`). The name is not a path: a name with `/`, `\`, `:` or `..` matches nothing. The popup shows the picture about 180 px tall, scaled to fill its width (about 370–510 px) and cropped around the centre. The base pictures are 640 × 640, so only their middle band shows; a wide picture, about 5:2 (e.g. 1000 × 400), shows almost whole. With no `image`, or a name that matches nothing, the popup shows the category's default picture. See §8.4. |

`change_government` accepts a government name as its `value`: `democracy`, `authoritarian`,
`hybrid`, `monarchy`, `theocracy`, `military_junta`, `one_party`, `communist_state` or
`transitional`.

#### When events fire

- **Monthly check.** Events are evaluated once per in-game month, on day 6–8, for every country.
  A game or scenario that starts after that day gets its first check on the first day it runs.
- **AI countries are staggered.** Each AI country rolls scripted and procedural events in about
  2.4 months per year: the countries are split into 5 groups, and one group rolls each month.
  Player countries roll every month. An `immediate` event for AI countries therefore arrives
  within 6 months after its conditions pass, not exactly on the first day. The gap between a
  group's turns is usually 5 months, but the group that rolls in December rolls again in January,
  so the other groups' turns across the New Year come 6 months apart.
- **One event at a time.** A country with an unanswered event gets no new scripted or procedural
  event that month. This applies to `immediate` events too: they fire at the next evaluation after
  the answer.
- **Cooldown.** After a scripted or procedural event fires, that country gets no other scripted
  or procedural event for 60 days (`generated_post_event_cooldown_days`). After a reactive event the
  wait is 3 days (`reactive_post_event_cooldown_days`). `cooldown_months` adds a cooldown for one
  event. An `immediate` event ignores the 60-day wait an earlier event left (it still starts a new
  one when it fires). One that can repeat and has no `cooldown_months` waits 60 days after its own
  firing, so it cannot fire every month.
- **Ties.** When several events are eligible in the same month, one is picked at random, weighted
  by `priority` (1–10). An eligible `immediate` event skips the draw and fires instead; among
  several, the highest `priority` wins, then the one loaded first.
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
| `alliance_member` | yes | `target_country`: the country is allied with that country. Without one it never passes. |
| `relation_above` / `relation_gt` / `relation_below` / `relation_lt` | yes | `target_country` + `value` (−100 to 100): the country's relation toward that country is above / below the value. Without a country the relation counts as 0. |
| `stakeholder` | yes | `target_country` (required) + `value`: the country is that country, is at war with it, is allied with it, or has a relation toward it whose size is at least `value` (positive or negative). Several `stakeholder` conditions on one event are OR-ed, then AND-ed with the rest. |
| `has_tech` | yes | `value`: a doctrine tier, `"<branch>_t<tier>"` with a tier from 1 to 5, e.g. `"cyber_t2"`. True when the country has completed that tier. Branch ids: `military`, `government`, `economy`, `industry`, `diplomacy`, `intelligence`, `cyber`, `space`, `energy`, `society`. Any other shape is rejected; a branch the game does not have gets a warning at load and never passes. |
| `province_stat_gt` | yes | `field`: `province.population`, `province.infrastructure`, `province.unrest`, `province.dev_level` or `province.radiation`; `value`: a number. True when at least one province the country **legally owns** has that stat above the value (occupied provinces count for their owner). A country without provinces never passes. Any other `field` is rejected. |
| `defcon_level` | yes | `value`: a whole number from 0 to 5. True when the country's DEFCON is at the value or more severe (5 = peace, 0 = nuclear exchange), so `3` passes at DEFCON 3, 2, 1 and 0. Countries without nuclear capability are always at 5. |
| `active_law_is` | **no** | Rejected in mod events for now. |

`has_tech`, `province_stat_gt` and `defcon_level` always check the country that gets the event. A
`target_country` on them is rejected.

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
  random roll, the 60-day wait and the draw, but still waits for that country's next evaluation.
- An event that should fire once per country when a province changes hands needs `fire_once: true`.
  Otherwise it can fire again every time its conditions pass, after its cooldowns.

#### Effect support

| Effect | Works? |
|---|---|
| `modify_stat`, `add_relation`, `set_flag`, `clear_flag`, `add_treasury`, `modify_unrest`, `impose_sanction`, `lift_sanction`, `engage_diplomatically`, `withdraw_forces`, `change_government`, `modify_resource_price` (alias `global_modifier`), `fire_event` | yes |
| `annex_province`, `annex_country` | yes, see [Territory effects](#territory-effects) |
| `create_unit` | yes, see [Unit effect](#unit-effect) |
| `declare_war`, `start_research` | **no**: accepted, but they do nothing yet (warning at load) |

#### Territory effects

`annex_province` gives one land province to a country. `annex_country` gives every province of
one country to the country that got the event.

```json
{ "type": "annex_province", "province_id": 2276, "target": "OTT" }
```
```json
{ "type": "annex_country", "target": "CYP" }
```

- **`annex_province`.** `province_id` is the id from the game's province registry (the Mod
  Builder's picker shows it as "Name (id)"). It must be a land province: sea zones (5001 and up)
  skip the event at load. An id in the land range that no province has is only found when the
  effect runs: it changes nothing, with a warning in `Player.log` (the Mod Builder's check warns
  about it earlier). `target` (or `target_country`) names the receiver. Without it, the
  country that got the event receives the province. If the named country no longer exists when
  the effect runs, the effect is skipped, with a warning in `Player.log`. Files that put the id in
  `value` instead of `province_id` still load.
- **`annex_country`.** `target` (or `target_country`) is required: the country to annex. The
  country that got the event takes every province that country owns when the effect runs. The
  annexed country is then eliminated exactly as after a peace deal that takes its last province:
  it leaves its wars, its units are disbanded and its diplomacy is cleared. The effect does nothing
  if that country no longer exists or is the recipient itself (a `specific_country` event whose
  `annex_country` names its own `target_country` gets a warning at load).
- **What changes.** The receiver becomes each province's owner and controller at once, on every
  copy of the province. Occupation and siege there end. Resistance is 0 and unrest is unchanged
  (a peace deal adds both). Missiles the old owner based in the province are removed. Borders and
  map ownership update as after a capture; economy and population follow on their next monthly
  pass, as after a peace deal. The receiver gains no aggressive expansion. A country that loses
  its capital gets a new one, a country left with no provinces is eliminated, and an eliminated
  receiver comes back.
- **Not changed.** Armies already in the province stay where they are, including the old owner's.
  Fleets are the exception: a fleet docked in a port that changed owner is undocked, as after a
  peace deal, and an AI fleet sitting on that land is moved one step out to sea.
- **Scripts.** `on_province_captured` fires once for each province that changed owner.
- **Multiplayer and saves.** The effects run on the same tick on every machine, in the order they
  are written in the option. A queued effect is saved with its province id.

#### Unit effect

`create_unit` gives a country one new stack of units.

```json
{ "type": "create_unit", "unit_id": "atl_hydro_sub", "count": 2, "province_id": 3277, "target": "HYP" }
```

- **`unit_id`** (required) is a unit type id: from the base `units.json`, from any active mod's
  `Content/units.json`, or from the scenario's unit types. Case does not matter. At most 29 bytes.
- **`count`** is how many units of that type the stack gets, from 1 to 100. Without it the stack
  gets 1. A larger count is cut to 100, with a warning at load. Files that put the count in `value`
  still load.
- **Who.** `target` (or `target_country`) names the receiver. Without it, the country that got the
  event receives the units. If the named country no longer exists when the effect runs, the effect
  is skipped.
- **Where.** `province_id` is optional. It must be a land province (1 to 5000). The stack starts
  there if the receiver owns and controls it. Otherwise it starts in the receiver's capital. If the
  capital doesn't qualify either, it starts in the receiver's lowest-numbered province that does.
  - Ground units can use any land province the receiver owns and controls.
  - Naval units need a coastal province and start docked in its port, as a newly built ship does.
  - Air units need a province whose airfield has a free wing slot, counted as for recruiting: the
    wings based there and the wings queued for it. A full airfield is passed over for the next one
    in this order, and air grants that run on the same tick count each other's wings.
- **What the stack is like.** It is a normal army, fleet or air wing, built the same way as a
  scenario's starting stacks. It costs nothing and needs no building. It starts at full strength
  and full morale, idle, and can take orders at once. It is saved like any other unit and is a
  separate stack (it does not merge into an army already in that province).
- **Scenario rules.** A unit type or category the scenario disables is not created. Units a
  scenario gives to one country only, and country unit lists, do **not** block this effect: the
  event is an explicit grant.
- **Skipped, with a warning in `Player.log`.** The effect creates nothing when:
  - no unit type has that id (the unit list is only complete once the game has started, so this is
    checked when the effect runs, not at load);
  - the unit is a missile;
  - the scenario disables the unit or its category;
  - the receiver has been eliminated;
  - the receiver has no suitable province.
- **Multiplayer and saves.** The stack appears on the same tick on every machine, in the order the
  effects are written. A queued effect is saved with its unit id, count and province.

#### Errors

Mod events are checked strictly. These problems **skip the whole event**:
- an unknown `type`, `category`, `target`, condition, effect or trigger type;
- an unknown stat `field`;
- a date that isn't `"YYYY-MM"`;
- a province condition whose `value` isn't a whole number of 1 or more;
- an `annex_province` without a land province id (`province_id`, a whole number from 1 to 5000),
  or an `annex_country` without `target_country`;
- a `create_unit` without `unit_id` (or with one longer than 29 bytes), with a `count` that isn't a
  whole number of 1 or more, or with a `province_id` that isn't a land province id;
- an unknown continent, region or government name;
- a `specific_country` event without `target_country`;
- fewer than 1 or more than 6 options;
- a `fire_event` without `chain_event`, or a flag effect or condition without a flag name.

**Check existing mods:** until 2026-09 `annex_province` and `create_unit` did nothing, so they
loaded without a province or a unit. Now an `annex_province` needs a land province id (in
`province_id`, or a whole-number `value`) and a `create_unit` needs a `unit_id`. An event with such
an effect that lacks its id is skipped whole, with the reason in the places listed below. Add the
id, or remove the effect.

A duplicate id skips the later event. An unknown chain target keeps the event and drops the chain.
Text longer than its field is cut off, with a warning: 125 bytes for titles, keys and option
labels, 509 bytes for tooltips.

Where problems appear:
- the Mod Builder's VALIDATE report and the check PUBLISH runs, before the mod is loaded at all;
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
**immediately**, without checking its conditions or cooldowns: the script decides. It is refused
when the event targets the player and no human controls that country, when it is a `fire_once`
event that has already fired, and when it is already pending for that country. A queued event
raises `on_event_fired` like any other. If the id isn't an engine event, a legacy event with that
id is shown instead. See the [WASM Scripting Guide](./WASM_SCRIPTING_GUIDE.md) (§4).

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

The JSON schemas in [`schemas/`](./schemas/) are authoritative: when this list and a schema
disagree, the schema is right. The values below are copied from the schema enums; write them as
shown. Older labels named under a list (§9.1, §9.2, §9.8) are not in the schema: the game still
reads them, with a warning, so existing mods keep loading, but new files should not use them.

### 9.1 Government Types
`governmentType` in `addCountries` (§4.1) and `countryStateOverrides` (§4.3):

`Unknown`, `Democracy`, `Authoritarian`, `Hybrid`, `Monarchy`, `Theocracy`, `MilitaryJunta`,
`OneParty`, `CommunistState`, `Transitional`

`Unknown` means "not set": the country keeps its template's (or its current) government type. Older
mods may still use the labels this list replaced; the game reads them with a warning in the log:
`military_junta` as `MilitaryJunta`, `failed_state` as `Transitional`, `city_state` as `Hybrid`.
Any other value is ignored with a warning.

### 9.2 Ideologies
`ideology` in `addCountries` (§4.1) and `countryStateOverrides` (§4.3):

`Unknown`, `Liberal`, `Conservative`, `Socialist`, `Nationalist`, `Islamist`, `Communist`,
`Fascist`, `Libertarian`, `Mixed`

`Unknown` means "not set", as above. Older labels, read with a warning: `progressive` as `Liberal`,
`centrist` and `green` as `Mixed`, `theocratic` as `Islamist`.

### 9.3 Continents
`Africa`, `Americas`, `Antarctica`, `Asia`, `Europe`, `Oceania`, `Unknown`

### 9.4 World Regions
`AustraliaNewZealand`, `CentralAsia`, `EastAsia`, `EasternEurope`, `LatinAmericaCaribbean`, `Melanesia`, `Micronesia`, `NorthernAfrica`, `NorthernAmerica`, `NorthernEurope`, `Polynesia`, `SouthAsia`, `SoutheastAsia`, `SouthernEurope`, `SubSaharanAfrica`, `Unknown`, `WesternAsia`, `WesternEurope`

### 9.5 Unit Categories
Two different lists use the word "category":

- A unit's `category` in `Content/units.json` / `unitsOverrideFile` (§8.1): `ground`, `air`,
  `naval`, `missile`, `special`. The scenario header's `disabledUnitCategories` (§3.3) names the
  same categories as `Ground`, `Air`, `Naval`, `Missile`, `Special`. A unit with any other
  `category` is read as `ground`; any other name in `disabledUnitCategories` switches nothing off.
- A unit type's `category` in `units_define.json` (§6.1): `infantry`, `cavalry`, `artillery`,
  `naval`, `air`, `armor`, `special_forces`. It picks the base unit a new unit type copies its cost
  and requirements from; any other value copies from `infantry`.

### 9.6 Air Mission Types
`missionType` in `units_deploy_air.json` (§6.5):

`None`, `AirSuperiority`, `CloseAirSupport`, `StrategicBombing`, `Reconnaissance`, `NavalStrike`

The schema also accepts these older spellings: `cas` (CloseAirSupport), `interception` and
`patrol` (AirSuperiority), `strategic_bombing` (StrategicBombing), `naval_strike` (NavalStrike) and
`standby` (None). It rejects any other value, and the game reads a value it does not recognise as
`None`.

### 9.7 Diplomacy Clear Scopes
- `core` — wars and alliances only
- `extended` — all diplomatic relationships (default)

### 9.8 Government Subtypes
`governmentSubtype` in `addCountries` (§4.1):

`None`, `FeudalMonarchy`, `Sultanate`, `Khanate`, `Shogunate`, `CityState`, `Duchy`, `Emirate`,
`Empire`, `Tribe`, `Chiefdom`, `LiberalDemocracy`, `IlliberalDemocracy`, `ParliamentaryMonarchy`,
`AbsoluteMonarchy`, `MilitaryDictatorship`, `Stratocracy`, `Theocracy`, `OnePartyState`,
`Despotic`, `Anarchy`, `Transitional`, `SocialistRepublic`, `FederalRepublic`

`None` means "not set". The older label `city_state` is read as `CityState`, with a warning.

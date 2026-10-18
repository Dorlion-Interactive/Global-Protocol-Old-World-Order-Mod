# NewWorldOrder – Modding Reference

Last updated: 2026-10-08

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
    victories.json           ← optional, named by victoryFile (§8.12)
    countries_add.json
    countries_remove.json
    countries_state.json
    diplomacy.json           ← optional: day-one alliances, treaties, wars, relations (§3.4)
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

**The game runs a lighter version of the check whenever a mod loads.** Every active mod is validated
at load and what is found lands in the same places as other load problems. Errors are listed in the
Loadout screen's error bar and the mod's error badge, and in the Mod Builder's Reload & Test; warnings
are listed in Reload & Test only (marked `(warning)`) and never mark the mod as failing. To keep
startup fast the load-time run reads only the JSON under `Content/`, `overrides/` and the scenario
folder, skips files over 512 KB, does not walk the rest of the folder or scan localization, and leaves
out what the load already reports itself (events, the WASM ABI and managed SDK, `gameVersion`,
dependencies, the roster composition and the unapplied `game_settings` sections). The whole pass has a
250 ms budget: if it runs out, one line in the Mods panel names how many mods were not checked.
Without an enabled mod nothing is read at all. Use VALIDATE in the Mod Builder for the full report.

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
| `wasmAbiVersion` | int | | WASM ABI version the script was built for, 1 to 4 (default: 1). ABI 4 adds the world-state imports (see the [WASM guide](./WASM_SCRIPTING_GUIDE.md) §4.2); every older import keeps working at every version |
| `runtimePolicy` | string | | Runtime coexistence policy: `"coexist"` (default), `"wasm_only"`, `"csharp_only"` |
| `enableComponentRuntime` | bool | | Allow component-model WASM binaries for this mod |
| `permissions` | string[] | | Required permissions (see §7) |

`entrypoints.wasm` is the preferred way to declare the mod's WASM module. `entrypoints.ui` is the preferred way to declare `inject.json` (the Mod Builder's INTERFACE tab edits it and writes the entrypoint for you; see [UI_INJECTION_GUIDE.md](UI_INJECTION_GUIDE.md)). Legacy fallback paths are still accepted for compatibility when the manifest entrypoint is omitted or unresolved.

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
| `diplomacy.json` | Day-one organizations, alliances, treaties, wars and relation values (§3.4) |
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
| `victoryFile` | string | `""` | Victory file, relative to the scenario folder (§8.12): the scenario's own endings, extra end-screen rows, and the switch that turns the base victories off. |
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
| `worldCeasefire` | object | — | A world ceasefire the scenario starts with (§3.5): `startDate`, `endDate`, `untilFlag`, `countries`, `blockDeclarations`, `suspendWars`. Absent = no ceasefire. |

Override file paths that do not resolve, and files that do not parse, are listed in the Mods panel
(and the Mod Builder's Reload & Test) instead of being skipped silently.

### 3.4 Starting diplomacy (`startingDiplomacy` / `diplomacy.json`)

A scenario can start with the diplomacy it needs: a Warsaw Pact that answers an attack on one member,
a defence pact, a non-aggression treaty, a war that is already running, hostile or friendly relations.
Put the block in `scenario/diplomacy.json`, or inline in `scenario.json`; lists from several files are
appended. It is written **once, when a new game starts**: a loaded save keeps the diplomacy it has. A scenario
without the block starts exactly as before. The Mod Builder's Diplomacy tab edits the file.

```json
{ "startingDiplomacy": {
  "organizations": [
    { "id": "WARSAW_PACT", "nameKey": "org.warsaw_pact.name", "type": "CollectiveDefense",
      "founder": "SOV", "members": ["SOV", "POL", "CZE"] }
  ],
  "alliances": [ { "a": "USA", "b": "GBR", "type": "Military" } ],
  "treaties": [
    { "type": "nap",   "a": "DEU", "b": "SOV" },
    { "type": "truce", "a": "ITA", "b": "ESP", "months": 24 }
  ],
  "wars": [
    { "id": "korea", "attackers": ["PRK", "CHN"], "defenders": ["KOR", "USA"],
      "casusBelli": "Territorial", "callAllies": false }
  ],
  "relations": [
    { "a": "USA", "b": "SOV", "opinion": -60, "trust": -40, "mutual": true, "anchor": true, "rival": true }
  ]
} }
```

Every country is an ISO3 code of a country the scenario has (a real one the scenario keeps, or one in
`addCountries`). An unknown country skips that entry with a warning in `Player.log`; Validate Mod reports it.

- **`organizations`.** A named alliance organization. `id` is 4 to 24 upper-case letters, digits or underscores,
  never starting with `IDX` (it is the organization's identity in saves and multiplayer). `nameKey` is the
  localization key of its display name, shipped in the mod's own text; blank uses `org.<id lower-case>.name` when
  the mod has it, then the id. `type` is `CollectiveDefense` (default: a mutual-defence pact, so an attack on one
  member is answered by all, and a member that attacks another is expelled), `Economic`, `Political` or
  `InternationalOrg` (plain memberships). The `founder` is a member; `members` lists the rest. Members of a
  `CollectiveDefense` organization count as allies of each other; an organization gives no shared map vision or
  transit (that needs a bilateral alliance). The id of a built-in organization, such as `NATO`, adds your members
  to it. Mod organizations do not count towards the prestige of the built-in G7, G20 and UN memberships.
- **`alliances`.** A bilateral alliance, `Military` (default; can be called into an offensive war) or `DefensePact`
  (defends only). Both sides hold it from day one and the AI does not drop it on its own, like the built-in
  pacts; a player can still break it.
- **`treaties`.** `nap` (non-aggression pact), `truce` (needs `months`, in 30-day months) or `trade_agreement`
  (the default trade terms), between `a` and `b`; or `guarantee`, where `a` guarantees `b`'s independence
  (`months` = how long, 0 = the diplomacy setting's length).
- **`wars`.** A war running from tick 0, with **exactly** the listed sides unless `callAllies` is true. The first
  attacker opens the war on the first defender through the normal war declaration; the others join their side.
  A starting war carries no aggression penalty (no aggressive-expansion gain, no goodwill drop with third
  countries, no embargo), whichever `casusBelli` it has: `Scripted` (default), `Territorial`, `Ideological`,
  `Humiliation`, `Defense`, `Liberation` or `Reconquest`. A truce between the two lead countries is ended by the
  war, and a country that is allied to someone on the other side stays out of it (a warning). The scenario's
  starting armies fight from the first day. The war is created a few frames after the scenario applies, before
  the first game tick.
- **`relations`.** Sets how much `a` likes (`opinion`, -100 to 100) and trusts (`trust`) `b`. `mutual` sets
  `b`'s view of `a` too. `anchor` also makes the values the level relations drift back to, so they do not fade
  towards the regional baseline. `rival` makes the two countries rivals (both ways when `mutual` is set).

Multiplayer: the block is part of the scenario every player loads, and everything it writes is saved and
hashed like any other diplomacy, so players stay in step.

---

### 3.5 World ceasefire (`worldCeasefire`)

A ceasefire that silences the wars between the countries it covers, from the first day or from a date you
choose. It is a header field of `scenario.json`, so it also appears in the Scenario tab of the Mod Builder.
Events and scripts can start and end one too (§8.7, §7).

```json
{
  "worldCeasefire": {
    "startDate": "1914-09-01",
    "endDate": "1915-01-01",
    "untilFlag": "armistice_broken",
    "countries": ["FRA", "DEU", "GBR"],
    "blockDeclarations": true,
    "suspendWars": true
  }
}
```

| Field | Default | Description |
|---|---|---|
| `startDate` | the scenario's first day | `YYYY-MM-DD`, with the game's 30-day months. A date in the future arms the ceasefire: it begins that day. |
| `endDate` | none | `YYYY-MM-DD`. The ceasefire ends on this day. |
| `untilFlag` | none | The ceasefire also ends the moment any country holds the event flag with this name (set by a `set_flag` effect). |
| `countries` | every country | ISO3 codes. A pair of countries is covered only when **both** are listed. |
| `blockDeclarations` | `true` | A declaration of war between covered countries is refused, for the player, the AI, the call to arms and the coalition wars alike. A `declare_war` effect with `"force": true` still goes through, and that one war stays live while the ceasefire holds. |
| `suspendWars` | `true` | The wars running between covered countries are suspended. |

With neither `endDate` nor `untilFlag` the ceasefire lasts until an `end_world_ceasefire` effect (or a
script) ends it; Validate Mod warns when nothing in the mod can.

What **suspended** means. The war, its participants, its occupations and its peace terms all stay, and a
peace deal can still be signed. But for each suspended pair:

- no new battle starts and a battle in progress stops (the armies stand down where they are);
- sieges and occupations **freeze**: no progress, no recovery, nothing cleared (an owner cannot reclaim a
  province, a besieger loses nothing);
- war score and war exhaustion stop moving, and the occupation costs stop accumulating;
- air strikes, close air support, ground fire and air interception between them stop, a blockade is lifted
  (and raised again afterwards), and nuclear and conventional missile strikes against the other side are
  refused;
- armies cannot enter the other side's land (an order that needs it is refused or paused);
- nobody can declare war on the other, or join a war against it (the call to arms and coalition joins are
  refused too).

The scenario's own `startingDiplomacy.wars` (§3.4) are declared first and then suspended, so a scenario
can open mid-war with the guns silent. The HUD shows a "World ceasefire" pill on the Diplomacy panel's
conflict line (with the end date when there is one) and a "Suspended" tag on the war rows, and toasts when
it starts and ends. The ceasefire is saved and hashed with the game, so saving, loading and multiplayer
resyncs keep it.

## 4. Country Overrides

### 4.1 Adding Countries (`addCountries` / `countries_add.json`)

Each entry maps to `ScenarioCountryDefinition`. Required field: `iso3`.

| Field | Type | Description |
|---|---|---|
| `iso3` | string | ISO3 code of the new country (uppercase, 3 chars). Use a code no real country has: one that belongs to a real country the scenario removes or does not play gives the new country that country's 2026 population pyramid and demographic rates (there is no `useSeedRow` switch), and the game logs a load warning (Mod Builder's Reload & Test list; Validate Mod warns for a removed base country). A base-game country that stays is a re-skin (below). |
| `templateISO3` | string | Existing country to copy from: economy, military, AI personality, political starting state and every field the entry leaves out. There is no fully custom country: when omitted, the country with the alphabetically first ISO3 (`ABW`, Aruba, in the base game) is used and a warning is logged; its identity fields (below) are not copied. Ignored for a re-skin (below). |
| `name` | string | Display name |
| `mapColor` | string | Hex color `#RRGGBB` |
| `flagPngPath` | string | A 128×80 flag PNG. A relative path is looked up in the mod folder (the one holding `mod.json`) first, then in the scenario folder (the split scenario folder, or the folder of a single-file scenario); the path must be mod-relative: an absolute path, or one whose `..` leaves the mod folder, is refused (Validate Mod reports an error and the flag does not load). The game and the Mod Builder preview use the same rule. A path that matches no file is listed in the Mods panel, and the country shows the base game's flag for its ISO3 (a re-skin) or an empty flag frame (a new ISO3). A changed flag shows when the scenario is loaded again (a new game, or the Mod Builder's Reload & Test). |
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
| `leaderGender` | string | `"male"` or `"female"`: the starting leader's gender, which picks a gender-matched portrait. Omitted: the first `leaderNamePool` entry decides (if it has a gender), else the template's. |
| `leaderPortraitPath` | string | Mod-relative PNG or JPG shown for the **starting** leader instead of the question-mark placeholder. Must stay inside the mod folder (see **Leader identity** below). |
| `leaderNamePool` | object[] | Names later leaders are drawn from, instead of the regional pool. Each `{ "name": "...", "title": "...", "gender": "male" }` (`title` and `gender` optional). See **Leader identity** below. |
| `lockLeaderTitle` | bool | `true` keeps `leaderTitle` on every leader drawn from `leaderNamePool`, whatever the government becomes. |
| `homelandTerm` | string | Override homeland noun (e.g. `"Federation"`) |
| `continent` | string | See §9.3 |
| `region` | string | See §9.4 |
| `neutral` | bool | Military neutrality. Omitted keeps the template's flag. An AI-controlled neutral forms no military alliances or defense pacts, gives no guarantees, joins no coalitions and answers no calls to arms (it still honors guarantees it already holds, and calls its own allies when attacked). A human player is unrestricted. |
| `dominantReligion` | string | Largest religion, e.g. `"Islam"` (max 29 bytes, see below). Drives kinship (below) and the religiosity of the interest groups. |
| `dominantEthnicity` | string | Largest ethnic group, e.g. `"Turkish"` (max 29 bytes). Drives kinship (below). |
| `primaryCulture` | string | Culture shown on the country overview, e.g. `"Ottoman"` (max 29 bytes) |
| `ethnicHomogeneity` | number | 0 (very diverse) to 1 (homogeneous); shown on the country overview when a culture or ethnicity is set |

**Leader identity.** A new country used to keep its template's leader (a human name on an alien
nation) until its first change of government, when the game gave it a human name from a regional
pool and a title from the government type. Four fields fix that:

- `leaderName`, `leaderTitle` and `leaderGender` set the starting leader. A country with a
  `leaderNamePool` but no `leaderName` starts with the pool's **first entry** (its name, its title if
  it has one, its gender), so a pool alone replaces the template's leader. A country that declares
  neither keeps the template's leader, exactly as before.
- `leaderNamePool` replaces the regional name pool **for that ISO3** (it also replaces a base-game
  pool when the entry re-skins one). Elections, coups, revolutions and leader deaths draw from it.
  An entry's `title` overrides the title the government type would give. Names are at most 61 bytes of
  UTF-8 and titles 29; longer ones are shortened and Validate Mod says so.
- `lockLeaderTitle: true` gives every pool entry the country's `leaderTitle`, so successors keep it
  whatever the government type becomes. It needs `leaderTitle` and a `leaderNamePool`; without a pool
  the regional pool picks successors and the title follows the government type (Validate Mod warns).
- `leaderPortraitPath` is shown for the starting leader. A relative path is tried against the mod folder,
  then the scenario folder, and the resolved file must lie **inside the mod folder**: an absolute path or
  one that climbs out (`../`) is refused (an error in Validate Mod; the placeholder is shown). Leaders
  who take over later use the mod's `portraits/<ISO3>/<ISO3>_m_01.jpg` (or `_f_` for women; `.jpg` or
  `.png`, numbered from 01) when you ship that folder, picked deterministically by leader number like
  the base game's bank; without it they get the base game's generated portrait if it has one, else the
  placeholder.

The Mod Builder's COUNTRIES tab has the matching controls on each added country: the leader name,
title, gender and title lock in the form, an Import button for the portrait (it copies the image to
`portraits/<ISO3>.<ext>`), and an editable name pool. The pools are rebuilt from the loaded scenario
each session, so they are not saved and a loaded game gets them back.

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
| `techLevel` | int | Starting Knowledge Network level: tiers 1 to `techLevel` of every doctrine branch start completed (doctrine A), except branches hidden by `disabledDoctrineBranches` (§3.3). A branch has 5 tiers, so 6–10 act as 5; tiers the country already has are kept. New games only. 0 or omitted grants nothing. **Check existing mods:** this field did nothing until 2026-09, and older Mod Builder versions wrote `techLevel: 5` into every new override. Remove it, or set it to 0, unless you want the tiers. The Mod Builder's Starting States editor has a **Starting Tech Level** row (0–5); it writes `techLevel` only when you tick it. |
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
{ "permissions": ["ReadEconomy", "WriteTreasury", "InjectUI", "world.read"] }
```

Each permission can be written in PascalCase (`WriteTreasury`) or snake_case (`write_treasury`); the two newer ones are written `world.read` and `flags.write`.

| Permission | Description |
|---|---|
| `ReadEconomy` | Nothing yet: every read (treasury, GDP, stability, manpower, tech level, date) works without it. Accepted so existing manifests stay valid. |
| `WriteTreasury` | Change a country's treasury (`country_set_treasury`, `add_treasury`) |
| `FireTriggers` | Queue events and raise reactive triggers (`fire_event`, `fire_trigger`, `ModHookBus.FireEvent`) |
| `world.read` (`ReadWorld`) | Scripts read the world: the country list and ISO3 lookups, wars and alliances, province owner and controller, country flags and variables (WASM ABI 4 imports and the matching C# `IModServices` members; [WASM guide](./WASM_SCRIPTING_GUIDE.md) §4.2). A WASM script that imports one of these without `wasmAbiVersion` 4 and this permission fails to load. |
| `flags.write` (`WriteFlags`) | Set or clear a country's event flags and set or add to its event variables: the state that `has_flag` / `not_has_flag` and `variable_gt/lt/eq` event conditions test. WASM ABI 4 imports (`country_set_flag`, `country_clear_flag`, `country_set_var`, `country_add_var`) and the matching C# `IModServices` members ([WASM guide](./WASM_SCRIPTING_GUIDE.md) §4.3); refused in multiplayer from a UI action or outside a simulation hook. It has nothing to do with flag or banner images. |
| `InjectUI` | Add UI elements to the HUD (`inject.json`) and show popups (`show_mod_popup`, and `show_mod_popup_key` / `IModServices.ShowPopupLocalized` from ABI 4) |
| `WriteDiplomacy` (`write_diplomacy`) | Found, join, leave and invite alliance organizations from a script (C#: `ModGameActionRequest.CreateOrganization` / `JoinOrganization` / `LeaveOrganization` / `InviteToOrganization`; the same actions as the `create_organization` ... `invite_to_organization` event effects, §8.7), and start or end the world ceasefire (C#: `ModGameActionRequest.StartWorldCeasefire` / `EndWorldCeasefire`; the same as the `start_world_ceasefire` / `end_world_ceasefire` effects, §8.7). A WASM script (ABI 4) calls `organization_create` / `organization_join` / `organization_leave` / `organization_invite` and `world_ceasefire_start` / `world_ceasefire_end`; a C# mod uses the matching `IModServices` members (WASM Scripting Guide §4.5). |

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
being listed. A disabled resource also disappears from the lists that show every resource: the Economy
overlay's Resources and Markets pages (rows, counts, top lists, category filter), Quick Build's shortage
scoring, and a building's output / recipe choices in its details (a recipe that needs or only makes a
disabled resource is left out). The pickers that already skipped them (spot market, trade proposals,
world overview, admin panel) are unchanged.

**`inherit`** decides what an entry for an **existing** base id means:

- `true` — overwrite only the fields you wrote (the classic sparse merge);
- `false` — the entry is the whole definition; fields you leave out take engine defaults instead of
  the base game's values.

Entries in a replace-mode file default to `inherit: false`, so a medieval roster cannot silently
keep modern recipes or effects; entries in a merge-mode file default to `true`. New ids are always
whole definitions. Nested objects (`cost`, `effects`, `prerequisites`) are replaced as a whole,
never merged field by field — write the full object.

**Which `inherit` applies when several layers touch one id.** The first layer that introduces an id decides its `inherit` flag, and that flag sticks. A later mod or scenario layer that edits the same id and leaves `inherit` out keeps the flag the first layer gave it, even when the later file is in the other mode (a merge-mode edit does not turn a replace-mode entry back into a sparse merge). The flag describes how the entry relates to the base game, and a partial edit does not change that. To change it, write `inherit` explicitly in the later entry; an explicit value always wins. In the Mod Builder's Content tab the "Keep base values for unlisted fields" switch writes this field, and its tooltip says the same.

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
| `satellite_launch_facility` | The vanilla satellite launch site (see "Satellite launch capacity" below) |

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
`"industry_t2"`. A mod that adds research (§8.8) can also name it: `"tech:<node or card id>"`, a mod
branch tier such as `"atlantis_t2"`, or a base branch tier above 5 such as `"military_t6"`; see "Tech ->
building, end to end" there. The game compares the key exactly, so `"None"`, `"Industry_t2"`, a branch that
does not exist or an old tech-tree id such as `"cyber_operations"` can never be met, and the entry
stays locked for the whole game. The Mods panel and the Mod Builder's checks box warn about such a
key on any entry your roster lists.

**Flag gates.** A unit or building can also wait for an event flag, so a story event can unlock it for
one country (player or AI) instead of it being available from the start:

```json
{ "id": "sunken_vault", "category": "military",
  "prerequisites": { "tech": "none", "flag": "atlantis_vault_found", "hidden_until_flag": true } }
```

- `prerequisites.flag` — the name a `set_flag` effect writes (§8.7). A country that does not hold the flag cannot recruit the unit or build the building,
  and cannot upgrade it. The recruit and build commands refuse it for the player, for the AI and
  for every multiplayer peer; the AI treats it as unavailable. The flag is an ordinary saved event
  flag, so nothing extra is written to the save. The name is trimmed and matched exactly, like
  `has_flag`.
- `prerequisites.hidden_until_flag` — `true` hides the entry from the recruit and build lists until
  the flag is set; without it the entry is listed but locked (the player sees an unmet
  requirement). It does nothing without a `flag`.
- The flag gate sits beside `prerequisites.tech`: both must be met. `prerequisites` is replaced as a
  whole (see above), so keep the `tech` you want when you add a `flag`.
- Only flags a mod event, a goal's `on_complete_flag` (§8.6) or a script sets can ever open the gate. The Validate Mod report
  and the Mod Builder's checks warn about a flag that no event of the mod sets.

In the Mod Builder, every building and unit card on the Content tab has a **Requires flag** field
with a picker of the flags your own events set, and a **Hidden until flag** toggle.

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
screens. The simulation enforces it as well, for the player, the AI and multiplayer peers alike: the
spot-market buy and sell command refuses the resource, the strategic-reserve auto-buy and auto-sell
skip it (a reserve target left on it is inert), and the AI never names it in the priority resources of
a trade agreement it proposes.

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
| `game_settings.json` | Balance sections applied at runtime: population, economy, technology, diplomacy, advanced diplomacy, `step42_diplomacy` (guarantees, rivals, aggressive expansion, coalitions, opinion, trust, embassies), world order, AI weights, fog of war, intelligence, map interaction, satellite, `political_drift` (drift, elections, coups, corruption, stability target), military and buildings, the mod-only `nuclear` section, plus `events` and `envoys` |
| `doctrines.json` | Doctrine values, effects and text |
| `laws.json` | Law values and appended categories/options (below) |
| `interest_groups.json` | The electorate: age-band leans, interest-group affinities, drivers and demand multipliers, law and doctrine bonuses, religiosity, country overrides (below) |
| `game_flow.json` / `events.json` / `envoys.json` | The matching `game_settings` sections, kept as separate files for backwards compatibility |
| `military_markers.json` | Map marker appearance |

**Economy, technology, step42_diplomacy, political_drift and nuclear.** These sections are applied at
runtime like the others: a key you write replaces the shipped value and every key you leave out keeps
it. Nested objects use the same names as the shipped file (`economy.central_bank.ai_rate_adjust_speed`,
`step42_diplomacy.guarantee.expire_ticks`, `political_drift.corruption_target_convergence_rate`).
Values are written raw, with none of the clamping the editor-side importer applies, so keep them
sensible. A key the runtime cannot place is listed in Player.log as unknown and skipped.
Two things to know:

- `economy.terrain_productivity` is accepted by the schema but nothing reads that table at runtime
  (province terrain multipliers are seeded from province data), so it is reported and ignored. A few
  other economy keys (`price_shock_decay_rate`, `resource_strategic_caps.*`,
  `trade_agreement_defaults.*` other than the three caps) have no config field behind them either.
- `nuclear` is **mod-only**: it has no counterpart in the shipped `game_settings.json`. It overrides
  `nuclear_config.json` and takes its sub-objects (`nuclear_consequences`, `recovery`, `deterrence`,
  `missile_defense`, `retaliation`, `defcon_escalation`, `ai_first_strike`) with the same key names.
  The DEFCON level table and the missile type list are not patchable. For example, a stronger shield:
  `{ "nuclear": { "missile_defense": { "base_intercept_chance": 0.8, "radar_bonus_cap": 0.4 } } }`.

The Mod Builder's SETTINGS tab shows all of these (the nuclear section with the shipped values as
hints). A section the game still does not apply is listed by Reload & Test as "… are not applied at
runtime yet and were ignored".

**Satellite launch capacity.** A country may keep as many satellites in orbit (active plus queued)
as the sum of the `satellite_launch_capacity` building effect over its completed buildings, and any
building carrying the effect is a launch site, not just `satellite_launch_facility`. In the shipped
game only the launch facility carries it (value 3, `buildings.json` `effects`), so one facility now
holds three satellites; before this was one per facility. `game_settings.satellite.max_per_facility`
is deprecated and no longer read. Give another building `"effects": { "satellite_launch_capacity": N }`
in Content > Buildings (or `Content/buildings.json`) to make it a launch site.

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

  **`requires_flag` on a doctrine card** locks that one card behind an event flag (a name a `set_flag`
  effect writes, §8.7). It is a value, so it works in both modes — in a merge file as
  `{ "branches": [ {}, { "tiers": [ {}, { "doctrines": [ {}, { "requires_flag": "my_flag" } ] } ] } ] }`
  (earlier positions are `{}` placeholders). A country without the flag sees the card locked, cannot
  start it (the research command is refused for every player and peer), and the AI never picks it;
  a tier whose three cards are all locked is not started by the AI. The Mod Builder's **Doctrines**
  tab has a *Flag-gated doctrine cards* section: pick the branch, tier and card, then type a flag or
  choose one of your events' flags.
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

**Interest groups and age bands (`overrides/interest_groups.json`).** The electorate config is applied
at runtime and re-baked at boot: a mod can make the senior vote more nationalist, give the Religious
group a different affinity or demand table, change a law or doctrine bonus, or pin a country's group
shares. It is a sparse patch against `interest_groups.schema.json`:

- `age_bands` and `groups` entries are matched by `id` (`youth, young, middle, senior` and
  `workers, entrepreneurs, military, religious, environmentalists`) and merge key by key, so
  `{ "age_bands": [ { "id": "senior", "lean": { "nationalist_conservative": 0.4 } } ] }` changes one
  number. **The model has exactly these four bands and five groups** (they are enum-indexed in the
  blob, the cohort state and the save), so an entry with any other id is rejected with a message
  naming it, and the mod is disabled; they cannot be added, removed, reordered or renamed.
- `law_bonuses` (matched by `category` + `option` + `group`) and `doctrine_bonuses` (`branch` +
  `group`) update the matching entry or append a new one. `country_overrides`, `religiosity_by_religion`
  and `neutrality_reference_shares` merge key by key; `gdp_factor_thresholds` replaces the list.
- The merged document must pass the same rules as the shipped file: bands and groups in order;
  turnout in (0, 1]; leans and affinities in [-1, 1]; law options, doctrine branches, resource
  categories and resources must exist; `fixed` country overrides list every group and sum to 1; and
  **demand multipliers stay neutral** (weighted by the world age mix for bands, or by
  `neutrality_reference_shares` for groups, every resource averages 1 within 10%). A mod that breaks
  one is disabled on its own and Reload & Test names the problem. Validate Mod reports the same
  findings as errors.
- The file is part of the lobby mod-set hash, so two peers with different electorate files do not
  match. Nothing is written to a save: the config is rebuilt from the loaded mods each session.

The Mod Builder's **POLITICS** tab (the former LAWS tab) holds two sub-tabs, **Laws** and **Interest
groups**. The latter edits this file with the shipped values beside every field: leans, affinities,
turnout and drivers as sliders, demand multipliers as a table (add a `category:` or `resource:` key,
or edit and revert an existing one), the religiosity table, and per-country shares. Nothing is
written until a value actually changes.

**Switching options off (`disabled_options`).** A mod can remove anachronistic options without
touching the save-stable order:

```json
{ "disabled_options": [ "conscription.cyber_reserve_corps", "press_freedom.platform_regulation" ] }
```

Each entry is `category.option` (the ids in laws.json) or a bare option id when only one category has
it. A disabled option keeps its index but is hidden in the Laws tab, skipped by the AI, refused by
the law commands for every player and multiplayer peer, and a country that has it active falls back
to its category default when a game loads (a pending debate for it is dropped). Lists from several
mods are combined. An entry is ignored, with a warning in the Mods panel and the Validate Mod report,
when it names nothing, is ambiguous, is the default option of a government type (change that default
first) or would leave its category with no enabled option. A starting-law override in
`country_overrides` that names a disabled option falls back to the usual seeding.

Options gated by a doctrine branch the game hides (the scenario's `disabledDoctrineBranches`, or a
branch a replace-mode doctrines.json leaves out) can never be unlocked, so the Laws tab no longer lists
them; you do not need to disable them. The Mod Builder's Laws tab shows a *Hidden: its doctrine
branch is disabled* badge on such options and a **Disable this option** switch on every option card.

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
(WASM) take plain text. A title or body that is **exactly a localization key** — no spaces or commas, with at least one dot inside,
e.g. `mymod.popup.intro.title` — is shown as that key's text in the player's language. Any other
text is shown as written, so English literals keep working. The same rule applies to a legacy
event's `title`, `description` and option `text` (§8.7). The key follows the rule above: define it
in all 13 files. Players see the key itself in a language you left out, or whose row for it is
still empty (the Mod Builder adds a new key to the other 12 files with an empty value).

```csharp
ModHookBus.ShowPopup("mymod", "mymod.popup.intro.title", "mymod.popup.intro.body");
```

For a popup whose text holds values, or for text a script composes itself, use the ABI-4 text calls: the
`localize` and `format` imports and `show_mod_popup_key` (WASM), or `IModServices.Localize`, `Format` and
`ShowPopupLocalized` (C#), which fill `{0}`, `{1}`... of a key's text from arguments. The text differs per
player's language, so a script shows it and never branches on it
([WASM guide](./WASM_SCRIPTING_GUIDE.md) §4.4).

```csharp
// mymod.popup.startup.body = "Strategic briefing: {0}-{1}"
services.ShowPopupLocalized("mymod.popup.startup.title", "mymod.popup.startup.body", new[] { "1450", "5" });
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
- Map markers are drawn per unit **subcategory** or per **unit**: set those with
  `overrides/military_markers.json` (see "Marker art" below).

The Mod Builder's Content tab has an icon picker on every building, unit and resource card, and the
Doctrines tab lists every doctrine icon id with a picker; both copy your image to the right place.
The Events tab's image row has an **IMPORT...** button: pick a PNG or JPG and it is copied into
`images/events/` under its file name (spaces and characters the file system rejects become `_`), selected
on the event and listed first in the picker. It asks before replacing an image of the same name, removes a
leftover file of the same name with another extension, and warns when the picture is far taller than 1:2
or wider than 4:1, because the popup crops to a wide band. (The picker needs a loaded map; without one the
row is a typed name and the Import button still works.)

#### Marker art (`overrides/military_markers.json`)

```json
{
  "army":  { "subcategory_icons": { "infantry": "icons/markers/army_infantry.png" },
             "unit_icons":        { "war_elephant": "icons/markers/army_unit_war_elephant.png" } },
  "fleet": { "subcategory_icons": { "destroyer": "icons/markers/fleet_destroyer.png" } },
  "air":   { }
}
```

- `subcategory_icons` replaces the marker of every unit in that subcategory. Keys are the 16 marker
  subcategories: `infantry`, `armor` (alias `tank`), `artillery`, `special_forces`, `fighter`, `bomber`,
  `helicopter`, `drone`, `destroyer`, `frigate`, `submarine`, `carrier`, `patrol_boat`, `amphibious`,
  `mechanized_infantry`, `cavalry`, or the numbers 0 to 15.
- `unit_icons` replaces the marker of a stack whose **dominant unit** is that unit: the strongest one
  (attack + defense) for an army, the most numerous one for a fleet or an air wing. A unit icon wins over its
  subcategory's. (The `army` section's `unit_icons` also gives the unit its picture in menus.) Pictures in
  `icons/units/` are portraits and are not drawn on the map unless a `unit_icons` entry points at them.
- Paths are relative to the mod folder (also looked up under `overrides/` and `Content/`) and must stay inside it.
- A mod with no marker art leaves the map exactly as the base game draws it. Each unit icon costs one extra
  slice in the marker picture array, built once when the mod loads.
- The Mod Builder edits this file on **Units > MARKERS**: pick the branch (army, fleet, air wing), choose a picture
  for any of the 16 subcategories, or add a unit and choose its picture. Choosing copies the PNG/JPG into
  `icons/markers/` (`<branch>_<subcategory>` or `<branch>_unit_<id>`; one file per entry) and writes the path.
  **Validate Mod** flags a key that is not a subcategory, a picture that is not in the mod folder, and a unit
  nobody defines. After SAVE ALL, the deployment preview on the Provinces tab shows the new markers.

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
folder. By default it **replaces** the base game's goals entirely: countries it does not list have no
agenda, and a file without `_BASIC` has no starter goals. Put `"mode": "merge"` at the root of the file
to keep the base game's goals and **append** yours instead, per country and in the shared `_BASIC` set
(a new country key gets its own list); a goal id may not repeat one of the base game's, or the file is
rejected. It uses the base game's `national_goals_2026.json` shape:

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
  `_`-prefixed keys are ignored as metadata. The root key `"mode"` is `"replace"` (default) or `"merge"`.
- **`id`** is required and unique across the file; the player's active goal is saved by id. Starter
  goals appear in the planner's starter list only when their id starts with `basic_`.
- **`title_key` / `description_key`** are looked up in the mod's localization CSVs; `title` and
  `description` are the fallback text. The AI's copy of the goal uses `title` (or the key).
- **`type`**: `expansion`, `territorial`, `economic`, `unification`, `defense`, `prestige`,
  `diplomatic`, `ideological` (the AI understands these), plus `technology` and `intelligence` for the
  Agenda panel's task templates. **`priority`**: `starter`, `primary`, `secondary`, `aspirational`.
  Unknown values are reported and fall back to economic / secondary.
- **`ai_weight`** (0–1, default 0.5) and **`target_countries`** steer AI countries that pursue the goal.
- **`on_complete_effects`** — paid **once** when the goal is completed, to the player and to AI
  countries alike: `prestige` (a fading prestige bonus), `stability` (added, kept within 0–100),
  `aggression_modifier` and `military_modifier` (added to the country's AI personality). `economy_boost`
  is read and shown but no system applies it yet. For the player the payment is a command
  (`CompleteAgendaGoal`) that every multiplayer peer runs from its own goals table, and the completion is
  saved, so reloading neither repays nor forgets it. The Agenda panel shows the same numbers as the reward.
- **`on_complete_flag`** — an event flag set on the country when the goal completes (player and AI), for
  `has_flag` conditions, other goals' `has_flag` tasks and the flag gates of units, buildings and doctrine
  cards (§8.1, §8.2) to test. **`on_complete_event`** — an event id queued for the player's country at the
  same moment, the way a script's `fire_event` queues it (its conditions and cooldowns are not checked);
  AI countries do not fire it.
- **`tasks`** are the player's steps. A goal without tasks gets a template from its `type`. Condition
  types and their `params`:

| `condition.type` | `params` |
|---|---|
| `own_provinces` | `province_owner` — counts owned provinces whose base-map country is this code |
| `alliance_with` | `target_iso3` (one country) **or** `partners` — a comma-separated ISO3 list (`"ISR,SAU,ARE"`), or `"*"` for any country. Progress is the number of distinct listed countries holding a bilateral alliance or a Defense Pact treaty with the owner; collective-defense memberships such as NATO do not count. `required_count` is the target |
| `declare_war_on`, `espionage_on`, `embassy_with`, `trade_agreement_with`, `defensive_pact_with`, `guarantee_independence` | `target_iso3` |
| `sphere_member` | `target_iso3` or `partners` — one ISO3 or a comma-separated list (absent = any member) — and/or `region`, a `WorldRegion` name such as `SoutheastAsia` (a member must match both when both are given). Progress is the number of members of the owner's sphere of influence that match; `required_count` is the target |
| `improve_relations` | `target_iso3` (optional), `min_value` (default 50) |
| `build_in_provinces` | `province_owner` (optional) |
| `recruit_units`, `military_units_above` | `unit_type`: `tanks`, `aircraft`, `ships`, `submarines`, `helicopters`, `apcs`, `artillery`, `personnel` (or `active_personnel`) — the count is the progress. `military_units_above` also takes `min_value`, the count to reach, used when `required_count` is absent |
| `research_tech` | none — the number of completed doctrine tiers is the progress |
| `treasury_above`, `gdp_above` | `min_value`, in the base money unit |
| `tutorial_objective` | `objective_id` |
| `has_flag`, `not_has_flag` | `flag_name` — met while the country holds (respectively does not hold) that saved event flag. Written by a mod event's `set_flag` effect or another goal's `on_complete_flag`. The AI ignores tasks, with one exception: it will not complete a goal while one of its `has_flag` / `not_has_flag` tasks fails |

  `required_count` (default 1) is the progress a counting task needs, e.g. 10 for "own 10 provinces"
  or 5000 for "5,000 personnel"; yes/no conditions report 1 when met. Unknown condition types never
  progress.

A file that is not an object, uses a key that is not a country code, has a `mode` other than
`merge` / `replace`, or has a goal without an id or with a repeated id (in merge mode, one that repeats a
base game goal) is rejected and the base goals stay; the Mods panel says why. The goals file is part of the
multiplayer lobby check. The Validate Mod report also warns about a `has_flag` task whose flag nothing in
the mod sets.

In the Mod Builder, the **Goals** tab has the replace / add switch at the top, and every goal card has
its rewards, `on_complete_flag`, `on_complete_event` and a task editor (condition type dropdown including
`has_flag` / `not_has_flag`, the parameters that type reads, required count), with pickers for the flags
and events the mod's own events define.

#### Goal prerequisites and the goal graph

A goal may list other goals it depends on:

```json
{ "id": "tur_modern_navy", "prerequisites": ["tur_shipyards"], "mutually_exclusive": ["tur_land_power"], "editor_position": [3, 1] }
```

* `prerequisites`: goal ids of the same country (or the shared `_BASIC` goals) that must be completed first, all of them. Until they are, the Agenda shows "Requires: ..." on the goal, it cannot be set
  active, its tasks do not complete it, and the simulation refuses its completion (a multiplayer peer included). AI countries make no progress on such a goal.
* `mutually_exclusive`: goal ids whose completion makes this goal unavailable ("Unavailable: ... is already done"). The relation is made symmetric when the file loads.
* `editor_position`: `[column, row]` in the Mod Builder's goal graph; the game ignores it. `incompatible_with` in the shipped goals stays informational.
* At load, unknown ids, a goal naming itself, ids of another country, entries that would close a cycle and an id that is both prerequisite and exclusion are dropped and listed in the mod warnings;
  Validate Mod reports them as errors. A goal that lists none of these behaves exactly as before.
* The player's completion set is per game, so another country's Agenda view never shows a lock. Mod Builder: Goals tab, **List | Graph** - drag from a goal's port onto another goal to add a prerequisite
  (a cycle is refused), the inspector under the graph removes prerequisites and adds exclusions (dashed red edge), **Auto layout** and **Reset view**.

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
| `pause_game` | event | `true` / `false`. Whether the event popup pauses the game when it opens. Absent, the game pauses for `geopolitical_crisis`, `military_incident`, `natural_disaster` and `internal_politics` events and not for `economic_shock`, `diplomatic_opportunity`, `technology_breakthrough` or `social_cultural`. `true` always pauses, `false` never does. The player's "Pause on Event Popup" setting (Settings, Gameplay) still turns pausing off for every event. |
| `target: "player"` | event | Only human-controlled countries can get the event. AI countries never roll it. In multiplayer, every human player can get it. |
| `target: "global"` | event | A world-scoped event. It is rolled once per check for a single country (the first human player by ISO3, else the first live country by ISO3), so it fires once, not once per country, and its conditions are tested on that country. The Mod Builder offers it in the Who-gets-it list. |
| `target: "every_country"` | event | Every country whose conditions pass gets the event, at the first monthly evaluation where they hold (day 6-8), all in the same evaluation. No random roll, no AI group rotation, no 60-day wait; the `mean_time_to_happen_months` you write is ignored. A country with an unanswered event gets this one queued behind it (at most `max_active_events_per_country`, 3 by default; one that is full is tried again next month). An AI country answers it in the same evaluation, each with its own choice weights; a human sees the popup. It still respects `fire_once` and `cooldown_months`; a repeatable one waits at least `repeatable_immediate_min_cooldown_days` between its own firings, so give it `fire_once`, `cooldown_months` or a condition that stops passing. Unlike `all` (which behaves like `any_country`), it never waits for a group to roll. Countries are judged in alphabetical ISO3 order on every player's game, so multiplayer sessions agree. Eliminated countries are skipped. |
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
  one when it fires). One that can repeat (not `fire_once`) and has no `cooldown_months` waits at
  least `repeatable_immediate_min_cooldown_days` (60 by default) after its own firing, so it cannot
  fire every month. A mod can raise that number in the `events` section of
  `overrides/game_settings.json` (the Mod Builder's Settings tab); it is never shorter than the
  scripted lane's own 60 days.
- **Ties.** When several events are eligible in the same month, one is picked at random, weighted
  by `priority` (1–10). An eligible `immediate` event skips the draw and fires instead; among
  several, the highest `priority` wins, then the one loaded first.
- **Reactive events** fire from their `triggers` (`on_war_declared`, `on_coup`, …). A reactive
  event **without** triggers never fires on its own. It fires only as a chain target or from a
  script. See [Reactive triggers](#reactive-triggers) for what raises each one.
- **Choices.** AI countries choose an option automatically (`ai_weight` and the personality
  factors). The player sees a popup. If the player doesn't answer, the game picks an option after
  30 days (`player_event_auto_decide_days`).
- **Notification setting.** Players can hide less important popups. At "Important only",
  `social_cultural` and `technology_breakthrough` events are resolved with their **first option**
  and moved to the event log. At "Critical only", only `geopolitical_crisis`, `military_incident`,
  `natural_disaster` and `internal_politics` events show as popups. Use one of those four categories
  for story events the player must see.

#### Reactive triggers

A reactive event lists one or more `triggers`. The game raises all thirteen types itself, for the
player and the AI alike, and a mod script can raise any of them too (the `fire_trigger` call).

| Trigger | Raised when | The event goes to (`source_country`) | `target_country` |
|---|---|---|---|
| `on_war_declared` | a country declares war | the country that declared | the defender |
| `on_peace_signed` | a peace deal is signed | the country that proposed it | the other party |
| `on_alliance_formed` | two countries form an alliance | the country that proposed it | the partner |
| `on_alliance_broken` | an alliance ends: broken, or the ally is attacked, or a call to arms is dishonoured | the country that broke it | the former ally |
| `on_sanction_applied` | a country imposes sanctions | the country that imposed them | the sanctioned country |
| `on_tech_researched` | a country completes a doctrine tier, or a mod research node | that country | none (the gate index of the tier, or `64 +` the node's gate index for a mod node) |
| `on_country_collapse` | a country is eliminated (its last province is lost) | the fallen country | none |
| `on_building_completed` | a building finishes construction | the country that owns the province | none |
| `on_coup`, `on_revolution`, `on_leader_death` | the government changes that way / the leader dies | that country | none |
| `on_nuke_launched` | a country launches a nuclear strike | the launching country | none |
| `on_espionage_resolved` | an espionage mission reaches an outcome: success, failure or caught | the country that ran the mission | the country it was run against |

- **Recipient.** The event is queued for the **source** country only. To react from the other side
  (the defender of a war), write a second reactive event with `target_country` set the other way
  round and a condition that only the other side meets.
- **Filters.** A trigger's `source_country` / `target_country` (ISO3) narrow it to those countries;
  leave them out to match any.
- **Timing.** The game collects triggers all month and the reactive events fire at the next monthly
  event evaluation (days 6-8), after the usual checks: a country with an unanswered event, a
  `cooldown_months` that is still running, a `fire_once` event it already had, or the 3-day
  reactive wait since its last reactive event all hold the event back (the trigger is not kept).
- **Cost.** A trigger is raised only while some loaded event lists it, so a mod that uses none
  of them costs the game nothing.
- **A fallen country** (`on_country_collapse`) still exists but owns no land, so keep that event's
  effects to things that do not need territory (flags, variables, relations).
- Mod scripts can listen to the same moments through the hooks (`on_war_declared`, …); the two do
  not depend on each other.

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
| `flag_age_months_gt` / `flag_age_months_lt` | yes | `flag_name` + `value` (a whole number of months, 0 to 1200). True when the flag was set more / fewer than that many **whole months** ago (a month is 30 days). Never true while the country lacks the flag. See [Flags and variables](#flags-and-variables). |
| `variable_gt` / `variable_lt` / `variable_eq` | yes | `variable` + `value` (a whole number): the country's variable is above / below / equal to the value. A variable that was never set reads 0. See [Flags and variables](#flags-and-variables). |
| `espionage_active` | yes | The country has an espionage mission running. Optional `mission_type` (`gather_intelligence`, `sabotage_economy`, `steal_technology`, `influence_government`, `counter_intelligence`, `satellite_surveillance`) narrows it to that kind, optional `target_country` to missions against that country. See [Covert operations](#covert-operations). |
| `mission_caught_recently` | yes | `months` (a whole number, 1 to 1200): one of the country's espionage missions was caught within that many months (a month is 30 days). Optional `target_country`. See [Covert operations](#covert-operations). |
| `lifetime_gt` / `lifetime_lt` | yes | `counter` + `value` (a whole number, 0 to 2,000,000,000): the country's lifetime counter is above / below the value. Counters: `personnel_lost`, `regiments_lost`, `ships_lost`, `aircraft_lost`, `civilians_affected`, `provinces_gained`, `provinces_lost`, `wars_won`, `wars_lost`. They add up over the whole campaign and peace never resets them. See [Lifetime counters](#lifetime-counters). |
| `government_type` | yes | The same names as `change_government` above. |
| `continent` / `not_continent` | yes | `africa`, `americas`, `asia`, `europe`, `oceania`, `antarctica`. |
| `region` / `not_region` | yes | `northern_africa`, `sub_saharan_africa`, `latin_america_caribbean`, `northern_america`, `central_asia`, `east_asia`, `south_asia`, `southeast_asia`, `western_asia`, `eastern_europe`, `northern_europe`, `southern_europe`, `western_europe`, `australia_new_zealand`, `melanesia`, `micronesia`, `polynesia`. |
| `country_unrest_gt` / `country_unrest_lt` | yes | Average national unrest, 0–100. |
| `owns_province` / `not_owns_province` | yes | `value`: a province id (a whole number, e.g. `2276`). True when the country is the province's **legal owner**. Optional `target_country`: test that country instead. See [Province conditions](#province-conditions). |
| `controls_province` / `not_controls_province` | yes | `value`: a province id. True when the country **controls** the province: it occupies it, or owns it and nobody occupies it. Optional `target_country`. See [Province conditions](#province-conditions). |
| `alliance_member` | yes | `target_country`: the country is allied with that country. Without one it never passes. |
| `relation_above` / `relation_gt` / `relation_below` / `relation_lt` | yes | `target_country` + `value` (−100 to 100): the country's relation toward that country is above / below the value. Without a country the relation counts as 0. |
| `stakeholder` | yes | `target_country` (required) + `value`: the country is that country, is at war with it, is allied with it, or has a relation toward it whose size is at least `value` (positive or negative). Several `stakeholder` conditions on one event are OR-ed, then AND-ed with the rest. |
| `has_tech` | yes | `value`: a doctrine tier, `"<branch>_t<tier>"` with a tier from 1 to 5, e.g. `"cyber_t2"`. True when the country has completed that tier. Branch ids: `military`, `government`, `economy`, `industry`, `diplomacy`, `intelligence`, `cyber`, `space`, `energy`, `society`. A mod's research works too: `"tech:<node id>"` (a research node or doctrine card), or a mod branch tier (`"atlantis_t2"`, or a base branch tier above 5 such as `"military_t6"`); true when the country has that gate open (§8.8). It never passes in a game whose mods add no such research, and a key no mod defines gets a warning at load. Any other shape is rejected; a branch the game does not have gets a warning at load and never passes. |
| `has_specialist` | yes | `specialist`: the id of a specialist in a mod's `Content/specialists.json` (§8.9). True when the country employs it. An unknown id never passes (warning at load). |
| `wave_eliminated` | yes | `wave_id`: a wave a `create_unit` of the same mod spawned has no stack left, however they were lost. See [Invasion waves](#invasion-waves). |
| `wave_remaining_gt` / `wave_remaining_lt` | yes | `wave_id` + `value` (a whole number) + optional `measure` (`units`, the default, or `stacks`): the wave's live units or stacks compared with the value. A wave never spawned fails both. |
| `armies_in_province_gt` / `armies_in_province_lt` | yes | `province_id` + `value` + optional `owner_country` and `measure` (`stacks`, the default, or `units`): the armies standing in that province, of one owner or of everyone. |
| `province_stat_gt` | yes | `field`: `province.population`, `province.infrastructure`, `province.unrest`, `province.dev_level` or `province.radiation`; `value`: a number. True when at least one province the country **legally owns** has that stat above the value (occupied provinces count for their owner). A country without provinces never passes. Any other `field` is rejected. |
| `in_organization` | yes | `id`: an alliance organization's id. True when the country is a member: a mod's own organization or a built-in one such as `NATO`. See [Alliance organization effects](#alliance-organization-effects). |
| `world_ceasefire_active` | yes | No arguments. True while a world ceasefire holds (§3.5). A fact about the whole world, so it is true or false for every country alike. |
| `defcon_level` | yes | `value`: a whole number from 0 to 5. True when the country's DEFCON is at the value or more severe (5 = peace, 0 = nuclear exchange), so `3` passes at DEFCON 3, 2, 1 and 0. Countries without nuclear capability are always at 5. |
| `active_law_is` | **no** | Rejected in mod events for now. |

`has_tech`, `has_specialist`, `province_stat_gt`, `defcon_level`, `flag_age_months_gt` / `flag_age_months_lt`,
`variable_gt` / `variable_lt` / `variable_eq`, `in_organization`, `world_ceasefire_active` and `lifetime_gt` /
`lifetime_lt` always check the country that gets the event. A `target_country` on them is rejected.

Stat fields that `country_stat_gt` / `country_stat_lt` read: `economy.gdp`,
`economy.gdp_per_capita`, `economy.gdp_growth_rate`, `economy.inflation_rate`,
`economy.debt_to_gdp`, `economy.unemployment`, `economy.hdi`, `government.stability`,
`government.corruption`, `government.economic_stance`, `government.social_stance`,
`military.manpower`, `military.reserve`, `military.defense_budget`, `military.tanks`,
`military.aircraft`, `military.ships`, `military.nuclear_warheads`, `budget.tax_rate`,
`budget.treasury`, `budget.military_pct`, `budget.research_pct`.

#### Lifetime counters

Every country keeps nine counters for the whole game, in every game, with or without mods. They are
saved with the game, shown on the end screen's Campaign record (the player's own) and readable from
events (`lifetime_gt` / `lifetime_lt`) and from scripts (`country_lifetime` in the
[WASM guide](./WASM_SCRIPTING_GUIDE.md) §4.2, `IModServices.GetLifetime`). Their ids, used by scripts, are
the order below.

| Id | `counter` | Counts |
|---|---|---|
| 0 | `personnel_lost` | Soldiers killed in ground combat, missile and air strikes and nuclear blasts: the same quantity the war ledger calls manpower lost, over the whole game. |
| 1 | `regiments_lost` | Regiments destroyed (the units behind the soldiers above). |
| 2 | `ships_lost` | Ships sunk in naval combat, by naval strikes from the air and by nuclear blasts. |
| 3 | `aircraft_lost` | Aircraft shot down by ground fire over bombing and close air support, and in nuclear blasts. |
| 4 | `civilians_affected` | Civilians affected on the country's own soil: the estimated casualties of an enemy occupation, and the population a nuclear strike kills. |
| 5 | `provinces_gained` | Provinces that changed owner to this country by treaty. |
| 6 | `provinces_lost` | Provinces that changed owner away from this country by treaty. |
| 7 | `wars_won` | Wars that ended with this country clearly ahead. |
| 8 | `wars_lost` | Wars that ended with this country clearly behind. |

A war's own ledger (the War detail screen) also lists, per side, the manpower, equipment, ships and
aircraft each side lost and the civilians and economic damage on its soil. That ledger ends with the war;
the lifetime counters do not.

#### Flags and variables

Flags are on/off marks on a country; variables are whole numbers kept on each country. Both live
until a mod clears or overwrites them, and both are saved with the game and synced in multiplayer.

```json
{ "type": "set_variable", "variable": "mymod_tension", "value": 0 }
{ "type": "change_variable", "variable": "mymod_tension", "value": 2 }
{ "type": "variable_gt", "variable": "mymod_tension", "value": 5 }
{ "type": "flag_age_months_gt", "flag_name": "mymod_referendum", "value": 18 }
```

- **`set_variable`** makes the variable equal `value`; **`change_variable`** adds `value` to it
  (negative to subtract). A variable that was never set counts as 0, so `change_variable` can be
  the first write. Values are whole numbers between -1,000,000,000 and 1,000,000,000: a fraction is
  rounded (with a warning at load) and a result past the limit stops at the limit.
- **Reading.** `variable_gt`, `variable_lt` and `variable_eq` compare the variable with `value`.
  They test the country that gets the event, in the monthly evaluation, in an option's own
  conditions and when a chained event comes due.
- **Flag age.** `flag_age_months_gt` / `flag_age_months_lt` compare how long ago `set_flag` set the
  flag. `set_flag` on a flag the country already has changes nothing, so the age keeps counting
  from the first time; `clear_flag` then `set_flag` restarts it. A flag written by a script
  (`gp.set_country_flag`) counts from the tick of the write.
- **The limit.** A country keeps at most `events.max_flags_per_country` flags (64 by default) and,
  separately, the same number of variables. A new flag or variable past it is dropped, and the game
  writes one `[Events] flag cap reached for <ISO3>` / `variable cap reached` line to `Player.log`
  per country. Changing a variable that already exists always works.
- **Scope.** A variable normally lives on a country. Add `"scope": "mod"` to `set_variable`,
  `change_variable` and `variable_gt` / `variable_lt` / `variable_eq` and it is one number for your
  whole mod instead: shared by every country, saved with the game, and the same store your scripts
  read and write (`state_get` / `state_set` / `state_add`, [WASM guide](./WASM_SCRIPTING_GUIDE.md) §4.3).
  Another mod's key of the same name is separate. Omit `scope` (or write `"country"`) for the
  country's own variable. A mod may hold as many keys as one country may hold flags
  (`events.max_flags_per_country`); a new key past that is dropped with one `Player.log` line per
  mod. The Mod Builder's Events tab has a Scope dropdown on those rows.
- **Names.** Start them with your mod's id (`mymod_tension`) so two mods do not share one.
  Variables and flags are separate: a flag and a variable may share a name. The Mod Builder's
  Events tab offers a "Reuse a name" list built from your own events and warns when an event
  reads a name nothing in the mod sets.

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
| `set_variable`, `change_variable` | yes, see [Flags and variables](#flags-and-variables) |
| `modify_stat`, `add_relation`, `set_flag`, `clear_flag`, `add_treasury`, `modify_unrest`, `impose_sanction`, `lift_sanction`, `engage_diplomatically`, `withdraw_forces`, `change_government`, `modify_resource_price` (alias `global_modifier`), `fire_event` | yes |
| `annex_province`, `annex_country` | yes, see [Territory effects](#territory-effects) |
| `create_unit` | yes, see [Unit effect](#unit-effect) and [Invasion waves](#invasion-waves) |
| `upgrade_units` | yes, see [Converting units](#converting-units) |
| `grant_command_authority`, `revoke_command_authority` | yes, see [Shared command](#shared-command) |
| `modify_military` | yes, see [Military modifiers](#military-modifiers) |
| `start_espionage_mission`, `steal_technology`, `sabotage_military` | yes, see [Covert operations](#covert-operations) |
| `declare_war`, `sign_peace`, `sign_truce`, `form_alliance`, `break_alliance` | yes, see [Diplomacy effects](#diplomacy-effects) |
| `create_organization`, `join_organization`, `leave_organization`, `invite_to_organization` | yes, see [Alliance organization effects](#alliance-organization-effects) |
| `start_world_ceasefire`, `end_world_ceasefire` | yes, see [World ceasefire effects](#world-ceasefire-effects) |
| `grant_specialist`, `remove_specialist` | yes, see [Specialists](#89-specialists-contentspecialistsjson) |
| `start_research` | **no**: accepted, but it does nothing yet (warning at load) |

#### Diplomacy effects

The country the event reached acts on the country in `target` (or `target_country`, required). They run
through the same commands the player and the AI use, so allies are called to arms, the
`on_war_declared` / `on_peace_signed` / alliance hooks and reactive triggers fire, trust and relations
change as usual, and a war is a real war with peace deals, war score and occupation.

```json
{ "type": "declare_war", "target": "TEU", "casus_belli": "territorial", "force": true }
{ "type": "sign_peace", "target": "TEU" }
{ "type": "sign_truce", "target": "TEU", "months": 60 }
{ "type": "form_alliance", "target": "POL" }
{ "type": "break_alliance", "target": "POL" }
```

- **`declare_war`.** Without `force` the war is **skipped** (a warning goes to `Player.log`) while a
  truce, a non-aggression pact or an alliance holds between the two countries, or when they are
  already at war. With `"force": true` the truce ends, the pact and the alliance are broken, and the war
  is declared. The enemy does not have to be a country the actor has "discovered". `casus_belli` is
  one of `scripted` (default; shown as "Story event"), `territorial`, `ideological`, `humiliation`,
  `defense`, `liberation`, `reconquest`. `scripted` counts as neither aggression nor an unjustified
  attack: no aggressive-expansion gain, no goodwill drop with third countries, no automatic embargo.
  The others behave as when a player picks them. Allies on both sides are called to arms in the normal
  way. A world ceasefire (§3.5) that refuses declarations is a gate too: without `force` the war is
  skipped while it holds between the two countries; with `"force": true` it goes through, and that one
  pair stays at war while the rest of the world is suspended.
- **`sign_peace`.** A **white peace**: the war between the two ends with no demands, and the usual
  truce follows. Skipped when they are not at war.
- **`sign_truce`.** A truce for `months` months (1-600; absent = the game's usual truce length) between
  two countries **not** at war, replacing any truce in force. Skipped while they are at war: use
  `sign_peace`.
- **`form_alliance`.** A bilateral alliance. Without `force` the normal rules decide (relations, treaty
  limits, and the other country has to want it; a human country is asked in its inbox). With
  `"force": true` it forms at once. Skipped when already allied or at war.
- **`break_alliance`.** Ends the bilateral alliance, with the usual relations and trust penalty.
  Skipped when they have no bilateral alliance. Membership in NATO-style organisations is not touched.
- **Order.** Several of these in one choice run in the order you wrote them, after the event's other
  effects. A country that no longer exists skips the action.
- **Multiplayer.** They are part of the simulation like any other effect, so every player's game
  runs the same actions in the same order.

#### Alliance organization effects

A named alliance organization (a Warsaw Pact, a league, a trade union) that events, scripts and the
scenario can found and that countries can join, leave and be invited to. They share the organization
registry that a scenario's `startingDiplomacy.organizations` fills (§3.4), so an organization a scenario
starts with can be joined or left by an event, and the other way round.

```json
{ "type": "create_organization", "id": "SOUTHERN_LEAGUE", "collective_defense": true }
{ "type": "join_organization", "id": "SOUTHERN_LEAGUE", "target": "ARG" }
{ "type": "leave_organization", "id": "SOUTHERN_LEAGUE" }
{ "type": "invite_to_organization", "id": "SOUTHERN_LEAGUE", "target": "CHL" }
{ "type": "in_organization", "id": "SOUTHERN_LEAGUE" }
```

- **`id`.** 4 to 24 letters, digits or underscores, upper-cased by the game, never starting with `IDX`.
  The organization's display name is the text you give the key `org.<id in lower case>.name` in your
  localization (otherwise the id is shown).
- **`create_organization`.** The country the event reached founds the organization and joins it.
  `collective_defense: true` makes it a defence pact: an attack on one member is answered by all the
  others (the call to arms of any alliance), and a member that attacks another is expelled. Without it
  the organization is a plain membership with no obligations. Skipped when the id is already in use,
  by a mod organization or a built-in one such as `NATO`.
- **`join_organization`.** The country the event reached, or `target` when you name one, joins. It can
  join a mod organization or a built-in one (`NATO`, `CSTO`...). A country already inside it is skipped, and so is
  a country at war with a member of a defence pact, unless `"force": true`.
- **`leave_organization`.** The country the event reached leaves; skipped when it is not a member.
  Leaving a built-in defence pact also drops its alliance with each former fellow member (unless another
  pact still ties them).
- **`invite_to_organization`.** The country the event reached, which must be a member, invites `target`
  (required). A **human** player gets an invitation in the diplomatic inbox: accepting joins, declining or
  letting it lapse costs nothing. An **AI** country answers on the spot, with no dice: it accepts when its
  average relation to the members reaches `diplomacy.alliance_form_min_relation`, and refuses when it is at
  war with a member or is a neutral and the organization is a defence pact.
- **`in_organization`.** A condition: the country holds the organization's membership.
- **Members of a defence pact are allies**: they see each other as allied for wars, joins and the call
  to arms. They do not share map vision or transit; form a bilateral alliance (`form_alliance`) for that.
  Mod organizations do not count towards the prestige of the built-in G7, G20 and UN memberships.
- **Scripts.** With the `WriteDiplomacy` permission (§7), a script does the same: WASM imports
  `organization_create`, `organization_join`, `organization_leave` and `organization_invite` (ABI 4),
  C# `IModServices.CreateOrganization` / `JoinOrganization` / `LeaveOrganization` / `InviteToOrganization`
  (or `ModGameActionRequest` for mods that reference the ECS assembly).
- **Saves and multiplayer.** Organizations and memberships are saved and hashed like any other
  diplomacy; the effects run in the simulation, in the order written, on every player's game.

#### World ceasefire effects

`start_world_ceasefire` suspends every running war and refuses every new declaration of war, until it is
ended; `end_world_ceasefire` ends it at once. They act on the world, not on the country the event reached
(a `target` is ignored). See §3.5 for what suspended means.

```json
{ "type": "start_world_ceasefire", "months": 6, "until_flag": "armistice_broken" }
{ "type": "end_world_ceasefire" }
{ "type": "world_ceasefire_active" }
```

- **`months`.** 1 to 600 (a month is 30 days): the ceasefire ends that long after the effect runs. Absent
  = no end date.
- **`until_flag`.** The ceasefire also ends the moment any country holds this event flag. Absent = no
  flag ends it. With neither, it lasts until an `end_world_ceasefire` effect.
- A ceasefire started here covers every country, blocks declarations and suspends wars (use the scenario
  header, §3.5, to scope one). Starting while one runs **replaces** it.
- **`end_world_ceasefire`** is skipped (a warning goes to `Player.log`) when none is running.
- **`world_ceasefire_active`** is a condition: it holds while a ceasefire holds.
- **Scripts.** With the `WriteDiplomacy` permission (§7), a WASM script calls the ABI-4 imports
  `world_ceasefire_start(months, until_flag)` and `world_ceasefire_end()`; a C# mod calls
  `IModServices.StartWorldCeasefire` / `EndWorldCeasefire` (or `ModGameActionRequest.StartWorldCeasefire(em, months, untilFlag, modId)` and `EndWorldCeasefire(em, modId)`).
- **Saves and multiplayer.** The ceasefire is saved and hashed; the effects run in the simulation on every
  player's game.

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

- **`unit_id`** (required, unless you give a `unit_category`) is a unit type id: from the base
  `units.json`, from any active mod's `Content/units.json`, or from the scenario's unit types. Case
  does not matter. At most 29 bytes.
- **`unit_category`** (`ground`, `air`, `naval` or `special`) replaces `unit_id`: the receiver gets
  its **best available unit of that category** when the effect runs. "Best" is the highest attack
  plus defense, times health; a tie goes to the lower unit id. Available means the same as for a
  recruit: the scenario's disabled units and categories, the scenario's unit roster, units a mod
  gives to another country only, and tiers the receiver has not researched are all excluded.
  Missiles are not offered. If nothing of that category is available the effect is skipped with a
  warning. With both keys, `unit_id` wins and a load note says the category is ignored.
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

#### Invasion waves

The same `create_unit` can spawn a **wave**: several stacks that carry one id, are sent at a target
drawn at random from a list, and that conditions can count until none is left.

```json
{ "type": "create_unit", "unit_id": "hyp_reaper", "count": 6, "target": "HYP",
  "stacks": 3, "wave_id": "wave_2",
  "assault_target_pool": [2276, 2281, 2290], "assault_coastal": true, "spread": "split",
  "on_arrival": "release", "timeout_days": 180 }
{ "type": "wave_eliminated", "wave_id": "wave_2" }
{ "type": "wave_remaining_lt", "wave_id": "wave_2", "value": 5, "measure": "units" }
```

- **`wave_id`** tags every stack the effect spawns (armies, fleets and air wings): 1 to 24
  lower-case letters, digits or underscores, per mod (two mods may both use `wave_1`). Stacks of a
  wave never merge with other stacks, and a split keeps the tag.
- **`stacks`** spawns that many stacks (1 to 20), each with `count` units.
- **Where they spawn.** `spawn_pool` lists the receiver's own provinces; one is drawn at random among
  those that suit the unit (otherwise the usual place). `spawn_mode: "landing"` spawns ground stacks
  directly in their drawn target when the receiver is at war with whoever holds it; when it is not,
  they spawn at home and march. Put a `declare_war` before the `create_unit` in the same option: the
  war is declared first.
- **What they attack.** `assault_target_pool` lists the candidate provinces; `assault_owned_by` (an
  ISO3), `assault_region` (a region name as the `region` condition takes it), `assault_coastal`
  narrow it, or choose the candidates on their own when there is no list. Provinces the receiver
  already holds are skipped unless `assault_include_controlled` is true. `spread: "together"` (the
  default) gives every stack the same spawn province and target; `"split"` draws one per stack
  without repeating a province until all were drawn. The draw is random but identical on every
  multiplayer machine.
- **The march.** Each ground stack gets an assault order: it marches to the target (by sea with its
  owner's transports when it must), fights its way there and besieges it. Once its owner controls the
  target it is released and becomes an ordinary army of its owner (`on_arrival: "hold"` keeps it
  standing there instead). It also gives up when a country its owner is not at war with holds the
  target, after `timeout_days` (0 = no limit), or when no route can be found several times in a row.
  While it holds the order its owner's AI does not move, merge or split it; a move order the player
  gives cancels it. Ships and aircraft in a wave are tagged and counted but never ordered.
- **Counting.** `wave_eliminated` is true once the wave was spawned and none of its stacks is left,
  however they were lost: battles, a sunk transport, a strike, a disband. `wave_remaining_gt/lt`
  compare its live units (or stacks with `"measure": "stacks"`). A later `create_unit` with the same
  `wave_id` adds to the wave and brings it back. `armies_in_province_gt/lt` count the armies standing
  in one province (`owner_country` for one country's).
- **Use it like this.** Put the waves in one event and the follow-up in another with a
  `wave_eliminated` condition and `fire_once: true` (it fires at the next monthly evaluation after
  the last stack is gone). There is no reactive trigger for it yet.
- **Saves and multiplayer.** Tags, orders and the wave records are saved and part of the multiplayer
  state check; a game without waves saves exactly as before.

#### Converting units

`upgrade_units` turns a country's stacks of one unit into another: its armies, fleets and air wings,
everywhere or only in one province, region or wave.

```json
{ "type": "upgrade_units", "from_unit_id": "infantry", "to_unit_id": "atl_power_armor", "target": "FRA",
  "months": 3, "cost_per_regiment": 50000000, "preserve_hp_pct": 100,
  "province_id": 2276, "region": "western_europe", "wave_id": "wave_2", "retire_old": true }
```

- **The pair.** `from_unit_id` and `to_unit_id` are unit ids (the base game's or a mod's) and must
  differ. They must be in the same category (ground, naval, air, special); ships and aircraft also
  keep their subcategory (a fighter never becomes a bomber), and missiles never convert. A pair that
  breaks this, or an id no unit has, is skipped with a warning when the effect runs.
- **Who.** The country in `target`, else the country the event reached.
- **When.** `months` 0 (the default) converts at once. 1 to 120 starts a **refit programme** for the
  country: on its last day everything in scope *at that moment* converts and is paid for. Until then
  the stacks move and fight as usual. A country runs at most 16 programmes at a time.
- **What it costs.** `cost_per_regiment` (default 0) is paid from the treasury per converted
  regiment, ship or aircraft, booked as recruitment spending. Stacks convert one after another in a
  fixed order while the money lasts; the rest stay as they are.
- **Health.** `preserve_hp_pct` (default 100) is how much of each regiment's damage the new unit
  keeps: 100 keeps the same share (half health stays half health), 0 brings the new units in at full
  health. Converted regiments join the stack's row of the new unit if it has one.
- **Scope.** `province_id`, `region` (the names the `region` condition takes, matched on the
  province's home country) and `wave_id` (a wave a `create_unit` of the same mod names) narrow it;
  together they all apply.
- **"Future production" (`retire_old`).** `retire_old: true` takes the old unit off that country's
  recruit list for good, for the player and the AI alike: recruit panels, quick recruit, templates
  and the AI planner no longer offer it, so new production uses the new unit or any other the
  country has. Units already in the production queue finish as ordered, and a `create_unit` that
  names the old unit still grants it. Without `retire_old` the old unit stays recruitable next to the
  new one. Unlocking a new unit (a tech, a flag, a roster) and replacing an old one are separate:
  `retire_old` only retires.
- **Saves and multiplayer.** Retired units and running programmes are saved and part of the
  multiplayer state check.

#### Shared command

`grant_command_authority` lends a country's armies, fleets and air wings to another country's
command; `revoke_command_authority` takes them back.

```json
{ "type": "grant_command_authority", "source_country": "USA", "controller_country": "TUR",
  "unit_kinds": ["army", "fleet", "air"], "filter": "in_region", "region": "western_asia",
  "months": 6, "locked": false, "keep_after_peace": false }
{ "type": "revoke_command_authority", "source_country": "USA", "controller_country": "TUR" }
```

- **Who.** `controller_country` (required) commands the units of `source_country` (absent = the
  country the event reached). The two must differ. A grant between countries at war with each
  other, or to a country that no longer exists, does nothing (warning at run time).
- **Which units.** `unit_kinds` lists `army`, `fleet` and/or `air` (all three by default).
  `filter` is `all` (default), `in_region` (with `region`), `in_province` (with `province_id`) or
  `wave` (with `wave_id`, a wave a `create_unit` of the same mod names); a lone `region`,
  `province_id` or `wave_id` picks its filter. Missiles are never lent: launching them stays with
  the owner.
- **What the controller gets.** It orders the units like its own (the player through the unit bar,
  or its AI). The owner keeps everything else: it pays their upkeep, takes their losses, and their
  war, access and fog are its own, so the controller can only send them against countries the
  owner is at war with. A lent stack never merges with the owner's other stacks, splits keep the
  authority, and the units cannot be disbanded while lent. The controller also sees what the lent
  units see (they light its fog of war as well as the owner's).
- **The controller's AI.** An AI controller moves lent armies like its own (their paths and access
  stay the owner's). It uses a lent fleet or air wing only while the owner is at war with every
  country the controller fights, so each target it picks is one the owner fights too; otherwise
  the unit waits. It never positions a lent fleet to fire missiles and keeps a lent wing on its
  owner's airfield. The owner's AI leaves its lent units alone.
- **On the HUD.** The controller selects lent units like its own; the unit bar shows "Lent by: …"
  with the days left, and Load / Launch missiles and Disband explain why they are off. The owner
  cannot select a lent unit: its row in Military › Forces reads "Commanded by: …", and clicking it
  shows **Recall** (disabled with the reason when the loan is `locked`). Both sides get a notice
  when a loan starts or ends, and the event popup's option line names who lends what to whom.
- **How it ends.** After `months` (0 = no time limit); when the war the two countries share ends,
  unless `keep_after_peace` (a grant made in peacetime ends after the first war the two then share);
  when either country is gone; when the two go to war with each other; on a revoke; or when the
  owner recalls the units, unless `locked`.
- **Saves and multiplayer.** The authority is saved (the controller by ISO3) and part of the
  multiplayer state check.

#### Covert operations

Events can start, observe and react to the game's espionage missions. There is no hidden
"domestic faction" in the engine: a covert group inside a country is still narrated with events
and [flags and variables](#flags-and-variables); these tools give it real consequences.

```json
{ "type": "start_espionage_mission", "mission_type": "steal_technology", "target": "RUS" }
{ "type": "steal_technology", "target": "RUS" }
{ "type": "sabotage_military", "target": "RUS", "field": "military.tanks", "pct": 10 }
```

- **`start_espionage_mission`.** The country the event reaches launches a real mission against
  `target` (required, except for `counter_intelligence`, which is run against the country itself).
  `mission_type` is one of `gather_intelligence`, `sabotage_economy`, `steal_technology`,
  `influence_government`, `counter_intelligence`, `satellite_surveillance`. It goes through the
  same launch rules as the player's and the AI's missions: it needs an Intelligence HQ, a free
  mission slot, a specialist already deployed in the target country (counter_intelligence: an idle one), a Cyber Operations Center for the cyber kinds,
  and no cooldown running for that kind. When the rules refuse it, the effect is skipped with a
  warning in `Player.log` (it never forces a mission through). Once launched it is an ordinary
  mission: it costs upkeep, can be caught, and its success or failure has the usual consequences.
  `sabotage_infrastructure` and `fund_opposition` are not offered: they need a province or a
  political bloc that an event cannot name.
- **`steal_technology`.** Shorthand for a `steal_technology` mission against `target`.
- **`sabotage_military`.** Immediately destroys `pct` percent (0.1 to 50) of the stock named by
  `field` (`military.manpower`, `military.reserve`, `military.tanks`, `military.aircraft`,
  `military.ships`) in `target`, rounded down. It is not a mission: it cannot be caught and needs no
  Intelligence HQ. Narrate the cost to the saboteur with another effect if you want one.
- **`on_espionage_resolved`.** A reactive trigger raised when a mission reaches an outcome, for the
  country that ran it (`source_country`) against the country it targeted (`target_country`). It is
  raised only while a loaded reactive event lists it. Use `mission_caught_recently` to tell a caught
  mission from a success. There is no script (`gp.*`) hook for it yet.
- **`espionage_active` / `mission_caught_recently`.** Conditions on the country's own missions, see
  the table above. `mission_caught_recently` cannot see missions saved before the feature existed
  (their outcome time was not recorded).
- **Multiplayer and saves.** Effects run on the same tick on every machine; a launched mission is
  saved with the country as before, now with the tick it resolved.
- **Vanilla.** A game with no such event does nothing different: the conditions read the mission list
  only when an event uses them, and the trigger monitor does not run.

#### Military modifiers

`modify_military` changes the military of the country that got the event (the choosing country).

```json
{ "type": "modify_military", "stat": "attack", "value": 0.15, "months": 24 }
{ "type": "modify_military", "stat": "morale", "value": -20 }
```

- **`stat`** (required): `attack` or `defense` add `value` as a fraction to the country's army and
  fleet combat power (0.1 = +10%, -0.2 = -20%; allowed from -0.9 to 5). `morale_recovery` adds
  `value` as a fraction to how fast idle armies regain morale (0.5 = 50% faster; from -1 to 10).
  `morale` adds `value` points once to every army's morale (on the 0-100 scale, from -100 to 100,
  clamped to 0-100); it leaves nothing behind and ignores `months`.
- **`months`** (optional, 0 to 600): how long the change lasts. Empty or 0 is permanent.
- **Stacking.** Modifiers of the same stat add up, so two +10% attack effects give +20%. A country
  holds at most 32 at a time; once full, a new one is skipped with a warning.
- **Where it applies.** Land and naval combat power (`attack` when the country's units attack,
  `defense` when they defend), and the morale recovery of idle armies. It does not change the
  units' own stats.
- **Multiplayer and saves.** Applied on the same tick on every machine, in the order the effects
  are written. The active modifiers are saved with the country and rebuilt on load.
- **Vanilla.** A game without such an effect carries no modifier data and plays exactly as before.

#### Testing your events in the game

The dev console (the backtick key) has commands for checking an event chain without playing months
of game time. They work in the editor, in development builds and, for the read-only ones, in release
builds. The two that change the world (`event fire`, `flag set|clear`) are refused in multiplayer
and in release builds; nothing here is saved by itself.

| Command | What it does |
|---|---|
| `event fire <id> [ISO3]` | Queues the event for the country (default: the player) at once. Conditions, MTTH and cooldowns are not checked, like a script's `fire_event`. A player-only event is refused for an AI country, and an event that is already pending is refused. A `fire_once` event that already fired is refused too. |
| `event fire! <id> [ISO3]` | The same, and a `fire_once` event fires again. |
| `event why <id> [ISO3]` | Judges each of the event's conditions for the country with the game's own code and prints pass or FAIL with the current value (a flag's age, a variable's value, whether a flag is set). It also names the gates that are not conditions: `fire_once`, the event's own cooldown, an event already pending, a player-only event. It changes nothing. |
| `event pending [ISO3]` | The country's events waiting for an answer, its chained events with their due tick and days left, and the cooldowns still running, each by event id. |
| `flags [ISO3]` | The country's flags with the tick they were set and their age, and its event variables. A flag is printed by name when any event file uses the name; a flag set only by a mod script shows as a hex number. |
| `flag set <name> [ISO3]`, `flag clear <name> [ISO3]` | Sets (with the real tick, honouring `events.max_flags_per_country`) or clears a flag. |
| `mod hooks` | Each mod hook that has subscribers and how many, the events waiting to be delivered, and the last 32 hook events delivered (the per-tick and per-month ones are left out). |

Event ids are case-sensitive. There is no command to fast-forward to a date.

#### Errors

Mod events are checked strictly. These problems **skip the whole event**:
- an unknown `type`, `category`, `target`, condition, effect or trigger type;
- an unknown stat `field`;
- a date that isn't `"YYYY-MM"`;
- a province condition whose `value` isn't a whole number of 1 or more;
- an `annex_province` without a land province id (`province_id`, a whole number from 1 to 5000),
  or an `annex_country` without `target_country`;
- a `start_espionage_mission` without a known `mission_type` (or, unless it is `counter_intelligence`,
  without a `target`), a `steal_technology` without a `target`, a `sabotage_military` without a
  `target`, a military stock `field` or a `pct` between 0.1 and 50;
- an `espionage_active` with an unknown `mission_type`, or a `mission_caught_recently` whose `months`
  is not a whole number from 1 to 1200;
- a `modify_military` without a known `stat`, with a `value` outside the range of its stat, or with
  `months` that isn't a whole number from 0 to 600;
- a `create_unit` without `unit_id` or `unit_category` (or with an id longer than 29 bytes, or a
  category that isn't ground, air, naval or special), with a `count` that isn't a
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
- the lighter validation every load runs (see §1): errors in the Loadout error bar and Reload & Test,
  warnings in Reload & Test;
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

#### Editing a mod in a running game

In a **single-player** game with a local mod active, the pause menu has a **Mod Builder** button. Edit the mod, then press
**APPLY TO RUNNING GAME** instead of RELOAD & TEST: it saves your edits and reloads the mod's **events**,
**localization**, **script** and **number settings** into the game you are playing, without a restart.

- Every event that already exists keeps its place (its index), so events a country has pending and chains already scheduled
  keep working. An event you changed is updated in place; one you added goes after the last one; one you deleted (or broke:
  a file that no longer validates) stops firing until it is back, and nothing chains into it.
- A `.wasm` script is rebuilt first and swapped in only when the new module loads (a broken edit leaves the old script running);
  its memory starts fresh and its optional `on_reload` export is called instead of `on_init`. What the mod keeps in the game
  (flags, variables, its `state_*` store) is untouched.
- Settings that are plain numbers take effect at once: the `game_settings.json` sections `population`, `diplomacy`,
  `advanced_diplomacy`, `world_order`, `ai_weights`, `fog_of_war`, `intelligence`, `map_interaction`, `satellite`,
  `step42_diplomacy` and `political_drift`, and everything in `events.json`. They are rebuilt from the values the game started
  with, so a key you delete goes back to its original value. `economy`, `technology`, `nuclear`, `military` and `buildings`
  are not re-applied: the result line names the ones you changed, and a new game picks them up.
- The Events tab's **FIRE NOW** button queues the selected event for your country at once, ignoring its conditions and chance,
  so you can see the popup and try each option.
- **Not reloaded:** C# code (the game keeps a mod's assemblies for the whole run), a changed `mod.json` (permissions, versions,
  scripts, dependencies: save and restart), the settings sections above that are not live, and content such as buildings, units,
  doctrines, laws, resources and goals (new game). The result line says what was done.
- Refused in multiplayer: every player would need the same change at the same moment.

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

### 8.8 Mod research: doctrine branches and research tracks

A mod can add research beside the Knowledge Network without touching the base branches. Two sources feed one engine;
mod research runs in its own slots, so it never takes points from doctrine research.

**New branches and extra tiers (`overrides/doctrines.json`, `"append"`).** The `append` block is read next to the usual
`"mode": "merge" | "replace"` (both modes accept it). Schema: `doctrines.schema.json` (`append`).

```json
{
  "append": {
    "branches": [
      { "id": "atlantis", "name": "Atlantis", "description": "...", "icon": "space_t1_a",
        "tiers": [
          { "name": "Foundations", "question": "Which foundation?", "cost": 400, "months": 6,
            "cards": [ { "id": "crystal_a", "name": "Crystal lattice", "effects": { "research_speed": 0.1 },
                         "ai": { "economy": 0.6 }, "requires_flag": "found_atlantis" } ] } ],
        "milestone": { "name": "Deep knowledge", "effects": { "gdp_modifier": 0.05 } } } ],
    "tiers": [ { "branch": "military", "tiers": [ { "cards": [ { "id": "mil_six", "name": "Sixth doctrine" } ] } ] } ]
  }
}
```

* A tier holds 1-3 cards; the country researches exactly one (like a base tier), tiers in order. `cost` (research points)
  and `months` (minimum duration) default to the base values for the same tier number (tiers above 5 use tier 5's).
* `append.branches` creates branches shown under **Mod research** in the Knowledge Network rail (1-9 tiers, optional milestone
  granted once every tier has a researched card). `append.tiers` extends a base branch: tier numbers continue after 5 (6-9, at most four);
  the first extra tier needs the base branch's tier 5. Hidden pools and directives are not supported on mod branches.
* Ids are 1-24 characters of `a-z`, `0-9`, `_`, unique across every mod card and track node. A card's effects use the same keys as a
  base card (see `doctrines.schema.json`); an unknown key is an error.
* Gate keys content can require in `prerequisites.tech` (buildings, units): `tech:<card or node id>`, `<branch>_t<N>` of a mod branch (N up to 9),
  and `<base branch>_t6`..`t9` for appended tiers. A card can require other cards or base gates in `prerequisites`.
* AI countries choose among the cards they may research from the five `ai` axes, the effect lanes and a national taste.

**Research tracks (`Content/research_tracks.json`).** Free-form nodes with prerequisites and costs; schema `mod_research_tracks.schema.json`.
`settings.slots` (1-4, default 2) and `settings.points_share` (default 0.5: each mod slot receives that fraction of the country's monthly
research points) are file-wide. A node has `cost`, optional `months`, `prerequisites` (all of), `any_of` (at least two), `requires_flag`,
`effects`, `ai`, `ai_weight`, `position` ([column, row]); `starting` lists nodes a country already knows in a new game.

Validation (Mod Builder > Validate Mod, and at load): duplicate or malformed ids, unknown effects, tier and card counts, unresolved
prerequisites, prerequisite cycles, limits (192 nodes, 64 mod tiers). A tree that breaks a rule is dropped with a warning; the mod still loads.
Mod nodes raise the `on_tech_researched` hook, and the reactive event trigger of the same name, with tech index `64 + gate index`
(once per completed node; the trigger is only raised when a loaded event lists it). Events test a mod node with `has_tech` `"tech:<node id>"` (§3 conditions).
Saves store progress by node id; ids a later version of the mod no longer defines are dropped with a warning.

**Tech -> building, end to end (T01 -> B01).** A research node unlocks a building through the building's
`prerequisites.tech`; no flag or event is needed. Two files do it. `Content/research_tracks.json` adds the node:

```json
{ "tracks": [ { "id": "atlantis_lab", "name": "Atlantis lab", "nodes": [
  { "id": "atl_t01", "name": "Orichalcum smelting", "cost": 400, "months": 6, "ai_weight": 1.5 } ] } ] }
```

`Content/buildings.json` (a merge file: a new id is added) gates the building on it:

```json
[
  { "id": "atl_b01", "name": "Orichalcum foundry", "category": "economic",
    "cost": { "money": 900, "build_time_months": 8 },
    "prerequisites": { "tech": "tech:atl_t01", "infrastructure": 20 },
    "effects": { "gdp_modifier": 0.02 } }
]
```

- **Before T01.** B01 is listed in the build picker as locked, with "Requires research: Orichalcum smelting". The build
  command refuses it for the player, for the AI and for every multiplayer peer, and the AI's build planner skips it.
- **After T01.** The node finishes on the monthly research tick, and B01 opens at once for the country that researched
  it (and only that country). The AI builds it like any other building it may build.
- **A story beat** is optional. A monthly event with a `has_tech` condition fires once the node is done:

```json
{ "id": "atl_t01_done", "type": "scripted", "category": "geopolitical_crisis", "target": "player", "fire_once": true,
  "title": "Orichalcum", "description": "Our smelters can work the Atlantean metal.",
  "conditions": [ { "type": "has_tech", "value": "tech:atl_t01" } ],
  "options": [ { "text": "Build the foundries", "effects": [ { "type": "set_flag", "flag_name": "atl_orichalcum" } ] } ] }
```

- A unit uses the same key in its own `prerequisites.tech`, and a building or unit can wait for a mod doctrine tier
  instead (`"atlantis_t2"`; the lock then reads "Requires Atlantis Tier 2").
- The Mod Builder edits both files: Content > Research tracks for the node, and the `prerequisites` field of the
  building's card on the Content tab for the key.

### 8.9 Specialists (`Content/specialists.json`)

Named scientists and engineers a country can employ. Schema: `mod_specialists.schema.json`. The base game has none; every one comes from a mod.

```json
{
  "mode": "merge",
  "settings": { "max_assigned": 2 },
  "specialists": [
    { "id": "dr_vega", "name": "Dr Vega", "description": "...", "role": "scientist",
      "portrait": "portraits/specialists/dr_vega.png", "country": "ATL", "available_from": 1990,
      "hire_cost": 5000000, "upkeep_monthly": 250000, "requires_flag": "found_lab", "ai_weight": 0.4,
      "effects": { "research_speed": 0.05, "construction_speed_mult": 1.1 } } ]
}
```

* A country hires a specialist for `hire_cost` (USD, from the treasury, booked to the political-expense ledger lane) and pays `upkeep_monthly` every
  month while the specialist is employed. `max_assigned` (1-8, default 2) caps how many one country employs. A specialist works for one country at a time.
* `country` (ISO3) employs the specialist at the start of a new game; empty = hireable by anyone. `available_from` is the first year it can be hired (0 = from the start);
  `requires_flag` gates hiring on an event flag.
* `effects` may use only `research_speed`, `construction_speed_mult`, `unit_build_speed_mult`, `production_output_mult` (same meaning as the doctrine lanes). They apply from the
  next monthly update after a hire or dismissal.
* `portrait` is a PNG path relative to the mod folder (it must stay inside it); without one a placeholder is shown. Role (`scientist`, `engineer`, `other`) is display only.
* `mode`: `merge` (default) adds to the roster other mods define - an id an earlier mod already defines keeps that definition - and `replace` discards the roster of the mods loaded before.
* AI countries hire the best specialist they can afford (three times the hire cost in the treasury) once a month, in ISO3 order.
* Event files reward and test specialists: the effects `grant_specialist` (`specialist`: the id; the country the event reached employs it for free, with no hire
  cost, slot limit, year or flag requirement, taking it from another country that employs it) and `remove_specialist` (it stops employing it; nothing is
  refunded), and the condition `has_specialist`. An unknown id does nothing and gets a warning at load.
  ```json
  { "type": "grant_specialist", "specialist": "dr_vega" }
  { "type": "has_specialist", "specialist": "dr_vega" }
  ```

### 8.10 Demography (`Content/demography/seeds.json`, `Content/demography/model.json`)

Schemas: `mod_demography_seeds.schema.json`, `mod_demography_model.schema.json`.

```json
{
  "countries": {
    "TUR": { "bands": [0.2, 0.25, 0.3, 0.25], "region": "Europe", "tfr": 1.6 },
    "ATL": { "template": "NLD", "le": 82 }
  }
}
```

* A row gives a country's starting age pyramid and demographic scalars. The shape is `cohorts` (`male` / `female`, 101 headcounts by age), four `bands` shares
  (0-18, 19-36, 37-56, 57+, summing to 1, spread over single years by the `region` template, default World) or a `template` country; what is missing is inherited from the country's
  shipped row, its template or the region template. Only the shape matters: the pyramid is scaled to the country's population.
* `le` / `le_male` / `le_female`, `tfr`, `sex_ratio_at_birth` (0.9-1.2), `cbr_target` / `cdr_target` and `calibration` (`mortality_child`, `mortality_adult`, `fertility` factors) override the scalars.
  `le` and `tfr` must lie inside the model's life-table and fertility grids; a row that breaks a rule is skipped with a message in the log and the Validate Mod report.
* A scenario nation that names `templateISO3` and has no row here inherits that template's row (only when a mod ships demography).
* `model.json` replaces whole sections of the shipped model: `sex_gap_male_weight`, `mortality`, `fertility`, `migration`, `crisis_excess_shape`, `preston`, `region_templates`, `world_reference_bands`.
  A section must be complete and passes the shipped file's validation; if it is rejected the shipped tables stay.
* Rows apply to a NEW game only (seeds are read at game start); a loaded save keeps its pyramids. With no demography file the shipped model is used unchanged.

### 8.11 Scenario province data (`scenario/provinces_data.json`)

Name the file in `scenario.json`: `"provinceDataFile": "provinces_data.json"` (relative to the scenario folder). Schema: `mod_scenario_provinces_data.schema.json`.

```json
{
  "provinces": {
    "1021": { "population": 250000 },
    "1022": { "terrain": "Mountain", "resources_mode": "add", "resources": [ { "resource": "Iron", "intensity": 0.8 } ] }
  }
}
```

* Keys are land province ids (1-5000). Every field is optional; an unset field keeps the shipped value.
* `population` is written to the province when a new game starts, after the scenario's declared country populations, so a province entry wins over the even spread of a declared country total.
  The owning country's total, GDP per capita and age pyramid follow. A loaded save keeps what it saved.
* `terrain` replaces the province's terrain (movement, combat, building sites, the terrain map mode). The map's terrain colours do not change. `Ocean` is not allowed.
* `resources` lists latent deposits (`resource` name, `intensity` above 0 up to 1, at most 8). `resources_mode` is `replace` (default: exactly these deposits; an empty list removes all)
  or `add` (these join the shipped deposits; the same resource is overwritten). In replace mode the strongest listed resource becomes the province's produced resource in a new game.
  Terrain and resources are static: they are re-applied every time the world starts, so loads see them too.
* Starting buildings are not covered. Unknown province ids, terrains and resources are reported by Validate Mod and the entry is skipped.
* Mod Builder: Provinces > map > **Data** paints these values: edit the selected province, or turn the brush on and click provinces. Provinces that carry data are tinted.

### 8.12 Scenario victories (scenario `victoryFile`)

A scenario can end the game in ways of its own. The header's `victoryFile` names a JSON file (by
default `victories.json` in the scenario folder) with three optional parts:

```json
{
  "disable_base_victories": true,
  "mod_victories": [
    { "id": "atlantis_saved", "title_key": "mymod.end.saved", "description_key": "mymod.end.saved.desc",
      "outcome": "victory", "winner": "player", "min_year": 2040,
      "conditions": [
        { "type": "has_flag", "flag_name": "atlantis_gate_sealed" },
        { "type": "lifetime_lt", "counter": "civilians_affected", "value": 1000000 },
        { "type": "variable_gt", "variable": "refugees_saved", "scope": "mod", "value": 50 } ] },
    { "id": "world_lost", "title_key": "mymod.end.lost", "outcome": "defeat", "winner": "any",
      "conditions": [ { "type": "has_flag", "flag_name": "atlantis_flooded" } ] }
  ],
  "end_screen_rows": [
    { "label_key": "mymod.row.ships", "value": "lifetime.ships_lost" },
    { "label_key": "mymod.row.refugees", "value": "mod_state.refugees" } ]
}
```

- **Endings (`mod_victories`).** Checked once a month, in file order. For each ending the countries
  it names are tried in ISO3 order, and the first country for which **all** the conditions hold is
  the winner: the game ends, the end screen opens with the ending's `title_key` (and the optional
  `description_key` under it), and the `on_game_ended` hook fires. An ending with no conditions holds
  at its first check. `id` must be unique in the file; the saved game remembers the ending by it.
- **Who wins (`winner`).** `"player"` (the default) tries the human players, `"any"` every country
  that still exists, and a three-letter country code only that country.
- **Result (`outcome`).** `"victory"` (the default) shows VICTORY when the winner is the player.
  `"defeat"` shows DEFEAT even though its conditions held, for an ending such as a world that
  ended.
- **`min_year`.** The ending is not checked before this calendar year (0 or absent: no limit).
- **Conditions.** The event conditions of §8.7 with the same fields, limited to `has_flag`,
  `not_has_flag`, `flag_age_months_gt/lt`, `variable_gt/lt/eq` (`scope` `"country"` or `"mod"`),
  `lifetime_gt/lt` and `date_after` / `date_before`. They test the country being tried as the
  winner. A condition with a `target_country`, or of another type, is rejected and the ending is
  dropped (the load log and the validator say which).
- **`disable_base_victories`.** `true` stops the five base victories from being checked in this
  scenario, so only your endings can end the game.
- **End-screen rows (`end_screen_rows`).** Extra lines in the end screen's **mod record**, shown
  on every end screen of this scenario whichever way the game ended. `label_key` is a text key of
  your mod; `value` is `lifetime.<counter>` (a [lifetime counter](#lifetime-counters) of the
  player's country), `mod_state.<key>` (your mod's own saved state), `variable.<name>` (an event
  variable of the player's country) or `wave.<wave id>.remaining` (an [invasion wave](#invasion-waves) of
  your mod: units still alive; also `.remaining_stacks`, `.spawned`, `.spawned_stacks`). Scripts add rows
  with `register_end_screen_row` /
  `IModServices.RegisterEndScreenRow`.
- **Multiplayer.** Every player's game checks the same endings in the same order, so every peer
  picks the same winner on the same tick. The ending reached is saved with the game and in the state hash.

The Mod Builder's **ENDINGS** tab edits the file, and the validator checks it (duplicate ids,
a missing title, a condition a victory cannot use, an unknown lifetime counter in a row). A game
without a victory file runs none of this.

### 8.13 HUD trackers

`Content/ui/hud_trackers.json` puts up to three gauges of your mod on the top bar, after the four national
numbers. It needs the `InjectUI` permission, like the rest of `Content/ui/`, and works with or without a
scenario. It is presentation only: the file is outside the multiplayer content hash, so peers with different
trackers just see different HUDs.

```json
{ "trackers": [ {
  "id": "invasion", "value": "wave.wave_2.remaining", "country": "viewer",
  "label_key": "atlantis.tracker.invasion", "tooltip_key": "atlantis.tracker.invasion.desc",
  "icon": "Content/ui/icons/invasion.png",
  "min": 0, "max": 24, "format": "of_max",
  "bands": [ { "from": 0, "tone": "good" }, { "from": 8, "tone": "warn" }, { "from": 16, "tone": "bad" } ],
  "target": { "low": 0, "high": 6 },
  "visible_when": [ { "type": "has_flag", "flag_name": "invasion_started" } ]
} ] }
```

- **`value`** is named like an end-screen row: `mod_state.<key>`, `variable.<name>`, `lifetime.<counter>`
  or `wave.<wave id>.remaining` (`.remaining_stacks`, `.spawned`, `.spawned_stacks`).
- **`country`** is whose variable or lifetime counter it reads, and whose state `visible_when` tests:
  `viewer` (the local player's country, the default) or an ISO3 code.
- **Text** comes from your mod's own localization rows (`label_key` is the caps label, `tooltip_key` the hover
  text). **`icon`** is a PNG or JPG in your mod (at most 2048 px a side).
- **The gauge.** With `max` above `min` a compact gauge is drawn under the value; without one only the value
  shows. `format` is `number`, `percent` or `of_max` (value / max). `bands` rise: from each band's `from` up to
  the next, the value and the marker take its `tone` (`neutral`, `good`, `warn`, `bad`, `gold`, `amber`,
  `muted`, `accent`; the theme decides the colours). `target` shades the band where the value should be.
- **`visible_when`** lists conditions that must all hold: the victory conditions (`has_flag`, `variable_gt`,
  `lifetime_gt`, `date_after`...) and the wave conditions (`wave_eliminated`, `wave_remaining_gt/lt`).
- A tracker reads its number once per game day (or when the viewer or the language changes) and writes it only
  when it changed. With several mods, the first three trackers in load order show.

The Mod Builder's **Interface › HUD trackers** section edits the file, shows the game's own verdict under each
tracker and a preview gauge you can move with a slider. Validate Mod checks the permission, the schema
(`mod_ui_hud_trackers.schema.json`), each tracker and that each icon exists.

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

### 9.9 Starting diplomacy types
`startingDiplomacy` (section 3.4):

- Organization `type`: `CollectiveDefense` (default), `Economic`, `Political`, `InternationalOrg`.
- Alliance `type`: `Military` (default), `DefensePact`.
- Treaty `type`: `nap`, `truce` (needs `months`), `trade_agreement`, `guarantee`.
- War `casusBelli`: `Scripted` (default), `Territorial`, `Ideological`, `Humiliation`, `Defense`, `Liberation`, `Reconquest`.

`worldCeasefire` (section 3.5): `startDate` / `endDate` are `YYYY-MM-DD` with 30-day months (day 1 to 30);
`countries` are ISO3 codes; `untilFlag` is an event flag name.

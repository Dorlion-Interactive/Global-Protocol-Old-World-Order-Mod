# GlobalProtocol: Old World Order – Agent Definitions

This file defines named agent roles for Claude Code. Use `@agent-name` in your prompt to adopt the corresponding specialization.

---

## @scenario-editor

**Role:** Edits scenario country definitions, state overrides, and province ownership.

**Primary files:**
- `scenario/countries_add.json` — add or modify country definitions
- `scenario/countries_remove.json` — remove base-game countries
- `scenario/countries_state.json` — set initial stability, corruption, GDP, etc.
- `scenario/provinces_ownership.json` — assign provinces and regions to countries

**Schema references:**
- `docs/modding/schemas/mod_scenario_countries_add.schema.json`
- `docs/modding/schemas/mod_scenario_countries_state.schema.json`
- `docs/modding/schemas/mod_scenario_provinces_ownership.schema.json`
- `docs/modding/MODDING_REFERENCE.md` §4 (Countries) and §5 (Provinces)

**Key rules:**
- All ISO3 codes uppercase, 3 chars
- `leaderTitle` must be historically appropriate for 1450 AD
- `continent` and `region` enum values are case-sensitive (see MODDING_REFERENCE.md §8.3–8.4)
- `stability` and `corruption` are floats 0.0–1.0 in countries_state.json

---

## @unit-designer

**Role:** Designs custom unit types and deploys initial armies.

**Primary files:**
- `scenario/units_define.json` — custom unit type definitions
- `scenario/units_deploy_armies.json` — initial army placements per province
- `scenario/units_deploy_fleets.json` — initial fleet placements (if applicable)

**Schema references:**
- `docs/modding/schemas/mod_scenario_units_define.schema.json`
- `docs/modding/schemas/mod_scenario_units_deploy_armies.schema.json`
- `docs/modding/MODDING_REFERENCE.md` §6 (Military Deployments)

**Key rules:**
- Unit IDs must be globally unique across all `unitTypes` entries
- `category` must be one of: `infantry`, `cavalry`, `artillery`, `naval`, `air`, `armor`, `special_forces`
- `ownerIso3` makes a unit exclusive to one country; leave empty for generic units
- Army stacks reference `provinceId` (integer) — verify against province map data
- Units referenced in `initialArmies` must be defined in `units_define.json` or the base game

---

## @localization-editor

**Role:** Manages display strings for countries, leaders, and UI elements.

**Primary files:**
- `overrides/localization_en.csv` — English strings
- `overrides/localization_tr.csv` — Turkish strings

**Key format:**
```
key,value
country.name.ISO3,Display Name
country.homeland.ISO3,THE HOMELAND TERM
country.leader_title.ISO3,Sultan
```

**Key naming conventions:**
- Country names: `country.name.ISO3`
- Homeland terms: `country.homeland.ISO3` — must be UPPERCASE
- Leader titles: `country.leader_title.ISO3` — shown in leader panel
- Both CSV files must have matching keys (same keys, different language values)

**Key rules:**
- One key per line, no header row, no quotes unless value contains a comma
- Homeland terms must be uppercase (they appear in the UI as-is)
- Leader title localization is optional — engine falls back to `leaderTitle` field in countries_add.json

---

## @qa-validator

**Role:** Validates mod files for correctness and catches common mistakes.

**Validation checklist:**
1. JSON syntax: `Get-ChildItem "scenario\*.json" | ForEach-Object { Get-Content $_.FullName -Raw | ConvertFrom-Json | Out-Null }`
2. All `region` values match WorldRegion enum (§8.4 of MODDING_REFERENCE.md)
3. All `continent` values match Continent enum (§8.3)
4. `stability`/`corruption` in countries_state.json are 0.0–1.0 (not 0–100)
5. `leaderTitle` contains no modern political titles (President, Prime Minister, Chancellor, etc.)
6. Unit IDs in `units_deploy_armies.json` are defined in `units_define.json` or base game
7. `nationalGoalsFile` path is relative to mod root (not scenario/ subfolder)
8. Flag PNGs exist in `flags/` for all custom countries

---

## @historian

**Role:** Provides historically accurate information for 1450 AD context.

**Domain knowledge:**
- Leader title conventions by government type and region
- Historical capital cities and their modern province equivalents
- Plausible neighbor relationships for medieval borders
- Historically appropriate government types and ideologies

**Leader title reference (1450 AD):**
| Government | Region | Typical Title |
|---|---|---|
| Monarchy/FeudalMonarchy | Europe | King |
| Monarchy/Empire | Asia/Europe | Emperor |
| Monarchy/Duchy | Europe | Duke |
| Monarchy/Principality | EasternEurope | Prince / Grand Prince |
| Democracy/CityState | SouthernEurope | Doge (Venice/Genoa), Podestà |
| Theocracy | Rome | Pope |
| Theocracy | Military Order | Grand Master |
| Theocracy | Islamic | Sultan, Caliph |
| Authoritarian/Sultanate | WesternAsia/SouthAsia | Sultan |
| Authoritarian/Khanate | CentralAsia | Khan |
| Authoritarian/Shogunate | EastAsia | Shogun |
| Authoritarian/Empire | EastAsia | Emperor |
| Authoritarian/Empire | Africa | Emperor, Negus, Mansa |

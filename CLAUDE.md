# GlobalProtocol: Old World Order – Claude Code Context

## Project Overview

This is a **historical scenario mod** for the game *Global Protocol* (Unity DOTS/ECS), set in 1450 AD. It defines 137 medieval nations with historically accurate governments, armies, fleets and leader titles, and removes all 266 modern countries.

**Mod ID:** `globalprotocol.old_world_order` · **Version:** see `mod.json` · **Needs:** Global Protocol v0.5.10+
**Engine location:** `C:\Personal\Genel\Projeler\NewWorldOrder\GlobalProtocol`

This repo is public. Anything a tool or doc here references must work from a plain GitHub clone, without the engine repo.

---

## Folder Layout

```
mod.json                         ← manifest (scenarioFolder: "scenario", workshopItemId)
scenario/                        ← split scenario files (authoritative)
  scenario.json                  ← header: ids, start date, gdpScale, Florins, override-file names, disabled lists
  countries_add.json             ← 137 country definitions (incl. militaryUnitTypeIds rosters)
  countries_remove.json          ← the 266 base-game countries removed
  countries_state.json           ← stability/corruption/economy overrides
  provinces_ownership.json       ← province + region ownership (authoritative — see Province tools)
  units_define.json              ← 31 unit ids: category + ownerIso3 (stats here are ignored, see below)
  units_override.json            ← unit roster, mode: replace — the 31 units' real stats/costs
  units_deploy_armies.json       ← 42 starting armies
  units_deploy_fleets.json       ← 20 starting fleets
  buildings_override.json        ← building roster, mode: replace (15 kept, 4 disabled)
  resources_override.json        ← 19 modern resources disabled
  currencies.json                ← Florin base currency + period currencies (currenciesFile)
  national_goals.json            ← national goals (nationalGoalsFile) — REPLACES the base goals
Content/
  localization/<lang>.csv        ← 13 locales: cz de en es es-419 fr ja ko pt pt-br ru tr zh
  events/historical_events_1450.json ← 7 engine events (Constantinople, Hundred Years' War, …)
  icons/{buildings,doctrines,resources,units}/ ← runtime icons
  ui/                            ← UI injection: inject.json (3 HUD toolbar buttons + a province row), owo_styles.uss
  shared/OldWorldOrder.cs        ← shared mod logic (briefing / Historian's Archive popups)
  mod-csharp/ wasm-as/ wasm-dotnet/ ← the three runtime variants' sources
overrides/
  doctrines.json                 ← replace-mode doctrine tree (7 branches; cyber/space/energy disabled in scenario.json)
  military_markers.json          ← map-marker overrides
  game_flow.json                 ← ignored by the engine for mods (player settings)
  Art/Units/                     ← map-marker art (install.bat mirrors it to Art/)
icons/{buildings,doctrines,units}/ ← icon art (16 / 47 / 16; mirrored in Content/icons — scripts/process_image.py writes both)
flags/                           ← flag PNGs (128×80, named by ISO3)
docs/modding/                    ← engine reference + schemas — synced copies, never hand-edit
docs/images/screenshots/         ← README screenshots
dev/                             ← gitignored except the tracked tools/data listed in .gitignore
  validate_scenario.ps1          ← fragment-shape check (install.bat + release.yml run it)
  set-runtime-settings.ps1       ← rewrites deployed mod.json runtimePolicy per build variant
  province_registry.json         ← slim engine province table (id, name, country_iso3, area_km2, centroid)
  province_curation.json         ← hand-curated ISO3 → provinceIds (curation source)
  owo_provinces.py, curate_browse.py, audit_ownership.py, build_province_ownership.py
scripts/                         ← audit_inventory.py (missing icons), process_image.py (art → icons)
sdk/                             ← GlobalProtocol.ModSdk (native C# SDK)
install.bat                      ← build + validate + deploy (/local, /workshop, /sdk /as /dotnet, /skip-build)
publish_workshop.bat             ← SteamCMD upload of workshop_content/
workshop_content/                ← gitignored Workshop staging folder (install.bat /workshop)
```

---

## Schema Authority

**Always consult these before editing data files:**

- `docs/modding/MODDING_REFERENCE.md` — complete field reference; enums are in **§9**
- `docs/modding/schemas/README.md` — which schema validates which file
- `mod_scenario_header.schema.json` (scenario.json), `mod_scenario_countries_add.schema.json`,
  `mod_scenario_countries_state.schema.json`, `mod_scenario_provinces_ownership.schema.json`,
  `mod_scenario_units_define.schema.json`, `mod_scenario_units_deploy_armies.schema.json`,
  `mod_scenario_units_deploy_fleets.schema.json`, `mod_currencies.schema.json`,
  `national_goals.schema.json`, `doctrines.schema.json`, `event.schema.json`,
  `mod_content_envelope.schema.json`

`docs/modding/` is refreshed from the engine repo by running
`tools\sync_modding_docs_to_example_mod.bat` there (it also re-exports `dev/province_registry.json`).
Never edit those files here; fix the engine's `docs/modding/` or `.ai/configs/schemas/` and re-sync.

---

## Critical Conventions

### Country ISO3 Codes
All ISO3 codes are **uppercase, 3 characters**. Custom codes avoid conflicts with base-game modern nations:
- MYN = Ming Dynasty (not MNG = Mongolia)
- ARA = Aragon (not ARG = Argentina)
- VNC = Venice (not VEN = Venezuela)
- MVY = Muscovy (not MUS = Mauritius)
- JOS = Joseon (not KOR = South Korea)
- CND = Candarids (not CAN = Canada)

`scenario/countries_add.json` is the list of codes in use.

### Country Fields in countries_add.json
- Only `iso3` is required by the schema.
- `leaderName` — initial leader's name (NOT `rulerName`, which is non-standard)
- `leaderTitle` — historical title string: `"Sultan"`, `"King"`, `"Emperor"`, `"Khan"`, `"Doge"`, `"Shogun"`, `"Pope"`, `"Grand Master"`, `"Duke"`, `"Grand Prince"`, `"Prince"`, `"Mansa"`, etc. (full list in use: AGENTS.md @historian)
- `homelandTerm` — uppercase noun shown in UI (e.g. `"THE SULTANATE"`, `"THE REALM"`)
- `governmentType` — PascalCase schema enum: `Unknown`, `Democracy`, `Authoritarian`, `Hybrid`, `Monarchy`, `Theocracy`, `MilitaryJunta`, `OneParty`, `CommunistState`, `Transitional` (MR §9.1 still prints an old lowercase list — the schema wins)
- `governmentSubtype` — schema enum (this mod uses `FeudalMonarchy`, `AbsoluteMonarchy`, `Empire`, `Duchy`, `Sultanate`, `Emirate`, `Khanate`, `Shogunate`, `CityState`, `Theocracy`, `Tribe`, `Chiefdom`, `FederalRepublic`)
- `continent` — `Africa`, `Americas`, `Antarctica`, `Asia`, `Europe`, `Oceania`, `Unknown`
- `region` — `WesternEurope`, `NorthernEurope`, `SouthernEurope`, `EasternEurope`, `WesternAsia`, `CentralAsia`, `EastAsia`, `SouthAsia`, `SoutheastAsia`, `NorthernAfrica`, `SubSaharanAfrica`, `NorthernAmerica`, `LatinAmericaCaribbean`, `AustraliaNewZealand`, `Melanesia`, `Micronesia`, `Polynesia`, `Unknown`
- There is no religion/culture field — the engine shows its defaults for those.

### Units and Rosters (MR §6.1)
- `units_define.json` supplies each id's `category` and `ownerIso3`. Because `units_override.json` defines all 31 ids, **the stats in `units_define.json` are ignored** — edit stats/costs in `units_override.json`.
- `ownerIso3` makes a unit **exclusive**: only the owner (or a country whose roster lists it) can recruit it. Omit the field for shared units — `""` fails the schema pattern.
- `militaryUnitTypeIds` in `countries_add.json` is an **enforced roster**: a non-empty list means the country recruits only those ids plus the ones it owns. All 137 countries set one; landlocked nations list no ships on purpose.
- `restrictOwnersToOwnedUnits` exists in the header schema but this mod leaves it off (owners keep the shared medieval units).
- Unit ids: unique, at most 29 bytes.

### State Overrides (countries_state.json)
- `stability` and `corruption` are **floats 0.0–1.0** (NOT integers 0–100)

### Money
`gdpScale: 0.001` multiplies every country's GDP, trade and treasury once at game start; `countries_state.json` values are absolute and applied after it. Money is shown in Florins (`economicEraLabel`/`currencySymbol: "fl."`, `currencies.json`).

### Scenario-relative paths
`nationalGoalsFile`, `currenciesFile`, `buildingsOverrideFile`, `unitsOverrideFile` and `resourcesOverrideFile` are **relative to the scenario folder** (MR §3.3). Flag paths are relative to the mod root.

### Localization (MR §8.3)
- `Content/localization/<lang>.csv`, all 13 files, same keys in each. UTF-8, no BOM, **no header row**, `key,value` split at the first comma (no quoting).
- **No cross-language fallback** for keys only the mod defines — a key missing from a locale renders raw.
- Key forms the engine reads: `country.name.<ISO3>`; `country.leader_title.<token>` and `country.homeland.term.<token>`, where token = the `leaderTitle`/`homelandTerm` value lowercased, apostrophes dropped, other non-alphanumerics → `_` (e.g. `grand_prince`, `the_sultanate`). `country.homeland.<ISO3>` is only a fallback for a country with **no** `homelandTerm` — every country here has one, so those rows are currently unused.
- Status: en and tr are real; the other 11 files are English copies (known gap).

### Province tools
`dev/province_curation.json` is the curation source. `build_province_ownership.py` expands it into `scenario/provinces_ownership.json`.

---

## Validation Commands

```powershell
powershell -NoProfile -File dev\validate_scenario.ps1        # fragment shapes (install.bat runs this)
python dev\build_province_ownership.py --check               # curation sanity
python dev\audit_ownership.py                                # area / continent audit
python scripts\audit_inventory.py                            # missing icons (run from repo root)
```

---

## Key Rules

1. **Do not edit `docs/modding/` files** — they are synced from the engine repo
2. **Never use raw integers for stability/corruption** — always 0.0–1.0 floats
3. **Leader titles must be historically plausible for 1450 AD** — no "President", no "Prime Minister"
4. **Enum values must match the schemas exactly** (continent, region, governmentType, governmentSubtype, ideology, unit category)
5. **Unit IDs must be unique** and ≤ 29 bytes; stats go in `units_override.json`
6. **Flag PNGs must be 128×80 pixels** in the `flags/` folder, named `ISO3.png`
7. **Every localization key goes into all 13 CSVs**

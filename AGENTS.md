# GlobalProtocol: Old World Order – Agent Definitions

This file defines named agent roles for Claude Code. Use `@agent-name` in your prompt to adopt the corresponding specialization. `CLAUDE.md` holds the shared conventions; the reference is `docs/modding/MODDING_REFERENCE.md` (MR).

---

## @scenario-editor

**Role:** Edits scenario country definitions, state overrides, province ownership and the scenario-level rosters.

**Primary files:**
- `scenario/scenario.json` — header: start date, `gdpScale`, Florins, override-file names, disabled unit/doctrine lists
- `scenario/countries_add.json` — the 137 country definitions (incl. `militaryUnitTypeIds` rosters)
- `scenario/countries_remove.json` — the 266 base-game countries removed
- `scenario/countries_state.json` — initial stability, corruption, GDP, etc.
- `scenario/provinces_ownership.json` — provinces and regions per country (authoritative)
- `scenario/buildings_override.json` — building roster (mode: replace)
- `scenario/units_override.json` — unit roster with the real stats (mode: replace)
- `scenario/resources_override.json` — disabled modern resources
- `scenario/currencies.json` — Florin base currency + period currencies
- `scenario/national_goals.json` — national goals; replaces the base game's goals

**Schema references:**
- `docs/modding/schemas/mod_scenario_header.schema.json`
- `docs/modding/schemas/mod_scenario_countries_add.schema.json`
- `docs/modding/schemas/mod_scenario_countries_state.schema.json`
- `docs/modding/schemas/mod_scenario_provinces_ownership.schema.json`
- `docs/modding/schemas/mod_currencies.schema.json`, `national_goals.schema.json`
- MR §3.3 (header), §4 (countries), §5 (provinces), §8.1 (rosters), §8.5 (currencies), §8.6 (goals)

**Key rules:**
- All ISO3 codes uppercase, 3 chars; the codes in use are the ones in `countries_add.json`
- `leaderTitle` must be historically appropriate for 1450 AD
- Enum values are case-sensitive in the schema (MR §9): `governmentType` is PascalCase (`Monarchy`, `Theocracy`, …)
- `stability` and `corruption` are floats 0.0–1.0 in countries_state.json
- `nationalGoalsFile` and the other `*File` header fields are relative to the **scenario folder**
- Province ownership: `dev/province_curation.json` is the curation source expanded into `provinces_ownership.json` by `dev/build_province_ownership.py`.

---

## @unit-designer

**Role:** Designs unit types, rosters and initial armies/fleets.

**Primary files:**
- `scenario/units_define.json` — each unit id's `category` and optional `ownerIso3`
- `scenario/units_override.json` — the same 31 ids with their real stats, costs and requirements
- `scenario/units_deploy_armies.json` — 42 initial armies
- `scenario/units_deploy_fleets.json` — 20 initial fleets
- `countries_add.json` → `militaryUnitTypeIds` — per-country rosters

**Schema references:**
- `docs/modding/schemas/mod_scenario_units_define.schema.json`
- `docs/modding/schemas/mod_scenario_units_deploy_armies.schema.json`, `mod_scenario_units_deploy_fleets.schema.json`
- `docs/modding/schemas/unit_type.schema.json` (entries of `units_override.json`)
- MR §6 (military deployments), §8.1 (content rosters)

**Key rules:**
- Unit IDs must be unique and at most 29 bytes
- `category` must be one of: `infantry`, `cavalry`, `artillery`, `armor`, `special_forces`, `naval`, `air` (this mod uses infantry, cavalry, artillery, naval)
- `units_override.json` defines every id, so **stats in `units_define.json` are ignored** — change stats there
- `ownerIso3` makes a unit exclusive to one country; omit the field for shared units (`""` fails the schema)
- A non-empty `militaryUnitTypeIds` roster is enforced: the country recruits only those ids plus the ones it owns. A roster may grant another country's exclusive unit.
- Base-game units are not available: the roster is replace-mode and `scenario.json` disables the modern ids and the Air/Missile/Special categories. Deployments may only reference the mod's 31 ids.
- Army/fleet stacks reference `provinceId` (integer) — look ids up in `docs/modding/PROVINCE_REFERENCE.md` or `python dev/curate_browse.py`

---

## @localization-editor

**Role:** Manages display strings for countries, leaders, doctrines, goals and mod UI.

**Primary files:**
- `Content/localization/<lang>.csv` — 13 files: `cz, de, en, es, es-419, fr, ja, ko, pt, pt-br, ru, tr, zh`

**Format (MR §8.3):**
```
country.name.OTT,Ottoman Empire
country.leader_title.grand_prince,Grand Prince
country.homeland.term.the_sultanate,THE SULTANATE
```
- UTF-8, no BOM, **no header row**; each row is `key,value`, split at the first comma — no quoting needed
- **Every key goes into all 13 files.** There is no fallback between languages for keys only the mod defines; a missing key renders raw.

**Key naming conventions:**
- Country names: `country.name.<ISO3>`
- Leader titles: `country.leader_title.<token>` — token = the `leaderTitle` value lowercased, apostrophes dropped, other non-alphanumerics → `_`
- Homeland terms: `country.homeland.term.<token>` of the `homelandTerm` value (keep values UPPERCASE). `country.homeland.<ISO3>` is only read for a country without a `homelandTerm`; all 137 have one, so the existing `country.homeland.<ISO3>` rows are not shown.
- Mod families: `owo.doctrine.*`, `owo.goal.*`, `owo.task.*`, `mod.ui.*`, `mod.owo.popup.*`; `doctrine.*` rows re-skin the base doctrine cards the mod keeps

**Key rules:**
- Leader title / homeland localization is optional — the engine falls back to the raw `leaderTitle` / `homelandTerm`; the base game already translates common titles such as `king` and `sultan`
- en and tr are translated; the other 11 files are currently English copies — when adding a key, write real translations where you can

---

## @qa-validator

**Role:** Validates mod files for correctness and catches common mistakes.

**Validation checklist:**
1. Fragment shapes: `powershell -NoProfile -File dev\validate_scenario.ps1` (install.bat and the release workflow run it too)
2. All `continent`, `region`, `governmentType`, `governmentSubtype`, `ideology` values match the schema enums (MR §9)
3. `stability`/`corruption` in countries_state.json are 0.0–1.0 (not 0–100)
4. `leaderTitle` contains no modern political titles (President, Prime Minister, Chancellor, etc.)
5. Every unit id in `units_deploy_armies.json` / `units_deploy_fleets.json` and in every `militaryUnitTypeIds` roster is defined in `units_define.json` and `units_override.json`
6. `nationalGoalsFile` / `currenciesFile` / `*OverrideFile` resolve inside `scenario/`
7. Flag PNGs exist in `flags/` for all 137 countries (128×80)
8. Every localization key exists in all 13 `Content/localization/*.csv` files
9. `python scripts\audit_inventory.py` reports no missing icons

---

## @historian

**Role:** Provides historically accurate information for 1450 AD context.

**Domain knowledge:**
- Leader title conventions by government type and region
- Historical capital cities and their modern province equivalents
- Plausible neighbor relationships for medieval borders
- Historically appropriate government types and ideologies

**Leader titles in use (1450 AD)** — `governmentType / governmentSubtype` as authored in `countries_add.json`:
| Government | Titles (examples) |
|---|---|
| Monarchy / FeudalMonarchy | King (FRA, PRT, POL…), Grand Prince (MVY, TVR, RYA), Grand Duke (LTH), Prince (WAL, MOL), Despot (SRB), Regent (HUN), Elector (SAX), Raja/Rajah, Shah, Maharana, Gajapati, Lakan |
| Monarchy / Empire | Emperor (BYZ, VIJ, SON…), Mansa (MAL), Sultan (KBR), King (MAJ) |
| Monarchy / Duchy | Duke (BUR, HAB, MIL…), Margrave (BRG), Elector (PAL), Count (WUR) |
| Monarchy / Sultanate · Emirate · Khanate | Sultan (MOR, HFS, GUJ…), Jam (SND), Emir (JBR), Khan (KZN, KRM, UZB…) |
| Monarchy / Shogunate | Shogun (MRC) |
| Monarchy / Chiefdom · Tribe · CityState | King, Prince, Emir |
| Authoritarian / Empire · Sultanate | Emperor (MYN), Sultan (TIM, MAM, DEL) |
| Democracy / CityState | Doge (VNC, GEN), Gonfaloniere (FLR), Diet (CHE), Mayor (NVD), Posadnik (PSK) |
| Theocracy / Empire | Pope (PAP), Grand Master (TEU), Emperor (AZT), Sapa Inca (INC), Dalai Lama (TIB) |
| Theocracy / Theocracy | Grand Master (LIV, KNI), Prince-Archbishop (COL) |
| Theocracy / Sultanate | Sultan (OTT), Emir (GRN) |

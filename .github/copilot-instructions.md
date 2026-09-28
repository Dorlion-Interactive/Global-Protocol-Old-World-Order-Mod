# GlobalProtocol: Old World Order – GitHub Copilot Workspace Instructions

This workspace is a **historical scenario mod** for *Global Protocol* (Unity DOTS/ECS), set in 1450 AD. It defines 137 medieval nations with historically accurate governments, armies, fleets and leader titles. It needs Global Protocol v0.5.10 or later.

---

## Schema Authority

Before suggesting changes to any data file, consult:
- **`docs/modding/MODDING_REFERENCE.md`** — complete authoritative field reference (enums in §9)
- **`docs/modding/schemas/`** — JSON Schema files for each domain file (`schemas/README.md` maps file → schema)

Do not invent field names. Every field in `scenario/*.json` must appear in the corresponding schema.

---

## File Map

| File | Purpose |
|---|---|
| `mod.json` | Mod manifest — do not remove `scenarioFolder` or `workshopItemId` |
| `scenario/scenario.json` | Header: scenarioId, start date, gdpScale, Florins, override-file names, disabled unit/doctrine lists |
| `scenario/countries_add.json` | The 137 country definitions, incl. `militaryUnitTypeIds` rosters |
| `scenario/countries_remove.json` | The 266 base-game countries removed |
| `scenario/countries_state.json` | Economic/political state overrides |
| `scenario/provinces_ownership.json` | Province + region ownership (authoritative) |
| `scenario/units_define.json` | Unit ids: `category` + optional `ownerIso3` |
| `scenario/units_override.json` | The unit roster with real stats (replace mode) |
| `scenario/units_deploy_armies.json` / `units_deploy_fleets.json` | Initial armies / fleets |
| `scenario/buildings_override.json` / `resources_override.json` | Building roster (replace) / disabled resources |
| `scenario/currencies.json` / `national_goals.json` | Currencies / national goals (both relative to `scenario/`) |
| `overrides/doctrines.json` | Replace-mode doctrine tree |
| `Content/localization/<lang>.csv` | Display strings, 13 locales |
| `Content/events/*.json` | Historical engine events |
| `docs/modding/**` | READ-ONLY — synced engine documentation |

---

## Field Conventions

### Country definitions (`scenario/countries_add.json`)
- `iso3` — uppercase, exactly 3 characters (the only required field)
- `leaderName` — the leader's name (do NOT use `rulerName`)
- `leaderTitle` — historically appropriate title for 1450 AD (e.g. `"Sultan"`, `"King"`, `"Khan"`, `"Emperor"`, `"Doge"`)
- `homelandTerm` — ALL CAPS noun (e.g. `"THE SULTANATE"`, `"THE REALM"`)
- `governmentType` — PascalCase: `Monarchy`, `Theocracy`, `Democracy`, `Authoritarian`, … (see the schema enum)
- `continent` — one of: `Africa`, `Americas`, `Antarctica`, `Asia`, `Europe`, `Oceania`, `Unknown`
- `region` — one of: `WesternEurope`, `NorthernEurope`, `SouthernEurope`, `EasternEurope`, `WesternAsia`, `CentralAsia`, `EastAsia`, `SouthAsia`, `SoutheastAsia`, `NorthernAfrica`, `SubSaharanAfrica`, `NorthernAmerica`, `LatinAmericaCaribbean`, `AustraliaNewZealand`, `Melanesia`, `Micronesia`, `Polynesia`, `Unknown`
- `militaryUnitTypeIds` — enforced roster: the country recruits only these ids plus the units it owns

### State overrides (`scenario/countries_state.json`)
- `stability` — float **0.0–1.0** (NOT an integer, NOT 0–100)
- `corruption` — float **0.0–1.0** (NOT an integer, NOT 0–100)

### Unit definitions (`scenario/units_define.json`)
- `category` — one of: `infantry`, `cavalry`, `artillery`, `armor`, `special_forces`, `naval`, `air`
- Unit IDs must be unique and at most 29 bytes
- `ownerIso3` makes a unit exclusive to one country — omit it for shared units (never `""`)
- Stats here are ignored because `units_override.json` defines every id — edit stats there

### Localization CSVs (`Content/localization/*.csv`)
- 13 files, same keys in each; no header row; `key,value` split at the first comma
- Key forms: `country.name.<ISO3>`, `country.leader_title.<token>`, `country.homeland.term.<token>` (token = the value lowercased, non-alphanumerics → `_`)

---

## Rules for Copilot Suggestions

1. **Do NOT suggest modern political titles** for 1450 AD — no President, Prime Minister, Chancellor, General Secretary
2. **Do NOT change `nationalGoalsFile` / `currenciesFile` / `*OverrideFile` paths** — they are relative to the `scenario/` folder
3. **Do NOT edit files in `docs/modding/`** — they are read-only synced engine documentation
4. **Do NOT use integer values for stability/corruption** — always floats
5. **Do NOT invent ISO3 codes** — `scenario/countries_add.json` is the full list of codes used in this mod
6. **Do NOT add a localization key to only some locales** — all 13 CSVs, or it renders raw

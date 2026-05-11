# GlobalProtocol: Old World Order – GitHub Copilot Workspace Instructions

This workspace is a **historical scenario mod** for *Global Protocol* (Unity DOTS/ECS), set in 1450 AD. It defines ~120 medieval nations with historically accurate governments, armies, and leader titles.

---

## Schema Authority

Before suggesting changes to any data file, consult:
- **`docs/modding/MODDING_REFERENCE.md`** — complete authoritative field reference
- **`docs/modding/schemas/`** — JSON Schema files for each domain file

Do not invent field names. Every field in `scenario/*.json` must appear in the corresponding schema.

---

## File Map

| File | Purpose |
|---|---|
| `mod.json` | Mod manifest — do not remove `scenarioFolder` |
| `scenario/scenario.json` | Header: scenarioId, startYear, gdpScale |
| `scenario/countries_add.json` | ~120 custom country definitions |
| `scenario/countries_remove.json` | Base-game countries to remove |
| `scenario/countries_state.json` | Economic/political state overrides |
| `scenario/provinces_ownership.json` | Province + region ownership |
| `scenario/units_define.json` | Custom unit type definitions |
| `scenario/units_deploy_armies.json` | Initial army stacks |
| `overrides/localization_en.csv` | English display strings |
| `overrides/localization_tr.csv` | Turkish display strings |
| `docs/modding/MODDING_REFERENCE.md` | READ-ONLY — engine documentation |

---

## Field Conventions

### Country definitions (`scenario/countries_add.json`)
- `iso3` — uppercase, exactly 3 characters
- `leaderName` — the leader's name (do NOT use `rulerName`)
- `leaderTitle` — historically appropriate title for 1450 AD (e.g. `"Sultan"`, `"King"`, `"Khan"`, `"Emperor"`, `"Doge"`)
- `homelandTerm` — ALL CAPS noun (e.g. `"THE SULTANATE"`, `"THE REALM"`)
- `continent` — one of: `Africa`, `Americas`, `Asia`, `Europe`, `Oceania`, `Unknown`
- `region` — one of: `WesternEurope`, `NorthernEurope`, `SouthernEurope`, `EasternEurope`, `WesternAsia`, `CentralAsia`, `EastAsia`, `SouthAsia`, `SoutheastAsia`, `NorthernAfrica`, `SubSaharanAfrica`, `NorthernAmerica`, `LatinAmericaCaribbean`, `AustraliaNewZealand`, `Melanesia`, `Micronesia`, `Polynesia`, `Unknown`

### State overrides (`scenario/countries_state.json`)
- `stability` — float **0.0–1.0** (NOT an integer, NOT 0–100)
- `corruption` — float **0.0–1.0** (NOT an integer, NOT 0–100)

### Unit definitions (`scenario/units_define.json`)
- `category` — one of: `infantry`, `cavalry`, `artillery`, `naval`, `air`, `armor`, `special_forces`
- Unit IDs must be globally unique

### Localization CSVs
- Key format: `country.name.ISO3`, `country.homeland.ISO3`, `country.leader_title.ISO3`
- Homeland terms must be UPPERCASE
- No header row in CSV files

---

## Rules for Copilot Suggestions

1. **Do NOT suggest modern political titles** for 1450 AD — no President, Prime Minister, Chancellor, General Secretary
2. **Do NOT change `nationalGoalsFile` path** — it must remain relative to mod root
3. **Do NOT edit files in `docs/modding/`** — they are read-only engine documentation
4. **Do NOT use integer values for stability/corruption** — always floats
5. **Do NOT invent ISO3 codes** — check `overrides/localization_en.csv` for the full list of codes used in this mod

---
applyTo: "scenario/countries_add.json"
---

# Country Editor Instructions

You are editing `scenario/countries_add.json` — the 137 country definitions for the 1450 scenario.

## Schema Reference
Full field list: `docs/modding/schemas/mod_scenario_countries_add.schema.json`
Field descriptions: `docs/modding/MODDING_REFERENCE.md` §4.1 (enums in §9)

## Entry Shape

Only `iso3` is required by the schema; every country in this mod also sets the fields below.
```json
{
  "iso3": "XXX",
  "name": "Display Name",
  "mapColor": "#RRGGBB",
  "capital": "City",
  "capitalProvince": "Province name or id",
  "population": 1000000,
  "areaKm2": 100000,
  "governmentType": "Monarchy",
  "governmentSubtype": "FeudalMonarchy",
  "ideology": "Conservative",
  "militaryUnitTypeIds": ["medieval_infantry", "medieval_cavalry"],
  "flagPngPath": "flags/XXX.png",
  "leaderName": "Name",
  "leaderTitle": "King",
  "continent": "Europe",
  "region": "WesternEurope",
  "homelandTerm": "THE REALM"
}
```

## Enums (PascalCase, from the schema)

- `governmentType`: `Unknown`, `Democracy`, `Authoritarian`, `Hybrid`, `Monarchy`, `Theocracy`, `MilitaryJunta`, `OneParty`, `CommunistState`, `Transitional`
- `governmentSubtype` used here: `FeudalMonarchy`, `AbsoluteMonarchy`, `Empire`, `Duchy`, `Sultanate`, `Emirate`, `Khanate`, `Shogunate`, `CityState`, `Theocracy`, `Tribe`, `Chiefdom` (full list in the schema)
- `ideology` used here: `Conservative`, `Islamist`, `Liberal`
- **Continents:** `Africa`, `Americas`, `Antarctica`, `Asia`, `Europe`, `Oceania`, `Unknown`
- **Regions:**
  - Europe: `WesternEurope`, `NorthernEurope`, `SouthernEurope`, `EasternEurope`
  - Asia: `WesternAsia`, `CentralAsia`, `EastAsia`, `SouthAsia`, `SoutheastAsia`
  - Africa: `NorthernAfrica`, `SubSaharanAfrica`
  - Americas: `NorthernAmerica`, `LatinAmericaCaribbean`
  - Pacific: `AustraliaNewZealand`, `Melanesia`, `Micronesia`, `Polynesia`
  - Fallback: `Unknown`

## Leader Titles (as used in this mod)

| `governmentType` / `governmentSubtype` | `leaderTitle` examples |
|---|---|
| `Monarchy` / `FeudalMonarchy` | `"King"`, `"Grand Prince"` (MVY), `"Grand Duke"` (LTH), `"Prince"`, `"Despot"`, `"Raja"`, `"Shah"` |
| `Monarchy` / `Empire` | `"Emperor"`, `"Mansa"` (MAL) |
| `Monarchy` / `Duchy` | `"Duke"`, `"Margrave"`, `"Elector"`, `"Count"` |
| `Monarchy` / `Sultanate` · `Emirate` · `Khanate` | `"Sultan"`, `"Emir"`, `"Khan"` |
| `Monarchy` / `Shogunate` | `"Shogun"` |
| `Authoritarian` / `Empire` · `Sultanate` | `"Emperor"` (MYN), `"Sultan"` (TIM, MAM, DEL) |
| `Democracy` / `CityState` | `"Doge"` (VNC, GEN), `"Gonfaloniere"` (FLR), `"Diet"` (CHE), `"Posadnik"` (PSK) |
| `Theocracy` / `Empire` | `"Pope"` (PAP), `"Grand Master"` (TEU), `"Sapa Inca"` (INC), `"Dalai Lama"` (TIB) |
| `Theocracy` / `Sultanate` | `"Sultan"` (OTT), `"Emir"` (GRN) |

## Common Country-Region Assignments (1450 AD)

| ISO3 | Country | continent | region |
|---|---|---|---|
| OTT | Ottoman Empire | Asia | WesternAsia |
| MYN | Ming Dynasty | Asia | EastAsia |
| ENG | England | Europe | NorthernEurope |
| FRA | France | Europe | WesternEurope |
| CAS | Castile | Europe | SouthernEurope |
| ARA | Aragon | Europe | SouthernEurope |
| PRT | Portugal | Europe | SouthernEurope |
| POL | Poland | Europe | EasternEurope |
| HUN | Hungary | Europe | EasternEurope |
| MVY | Muscovy | Europe | EasternEurope |
| VNC | Venice | Europe | SouthernEurope |
| GEN | Genoa | Europe | SouthernEurope |
| MAM | Mamluk | Africa | NorthernAfrica |
| TIM | Timurid | Asia | CentralAsia |
| JOS | Joseon | Asia | EastAsia |
| MRC | Muromachi | Asia | EastAsia |
| VIJ | Vijayanagara | Asia | SouthAsia |
| DEL | Delhi | Asia | SouthAsia |
| AYU | Ayutthaya | Asia | SoutheastAsia |
| MAJ | Majapahit | Asia | SoutheastAsia |
| AZT | Aztec | Americas | LatinAmericaCaribbean |
| INC | Inca | Americas | LatinAmericaCaribbean |
| ABY | Ethiopia | Africa | SubSaharanAfrica |
| MAL | Mali | Africa | SubSaharanAfrica |
| SON | Songhai | Africa | SubSaharanAfrica |
| MOR | Morocco | Africa | NorthernAfrica |
| HFS | Hafsid | Africa | NorthernAfrica |
| KZN | Kazan | Europe | EasternEurope |
| KRM | Crimea | Europe | EasternEurope |
| BYZ | Byzantine | Europe | SouthernEurope |

## Important Notes
- `leaderName` (not `rulerName`) sets the starting leader's name
- `homelandTerm` is the uppercase string shown in the UI homeland panel; translate it with `country.homeland.term.<token>` rows in `Content/localization/*.csv`
- `militaryUnitTypeIds` is an **enforced roster**: the country recruits only these ids plus the units it owns (`ownerIso3` in `units_define.json`). Every id must exist in `units_define.json` + `units_override.json` — base-game units are disabled. Unknown ids are reported as warnings at game start.
- A new country also needs `country.name.<ISO3>` in all 13 `Content/localization/*.csv` files and a 128×80 `flags/<ISO3>.png`

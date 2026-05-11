---
applyTo: "scenario/countries_add.json"
---

# Country Editor Instructions

You are editing `scenario/countries_add.json` — the list of all custom country definitions for the 1450 scenario.

## Schema Reference
Full field list: `docs/modding/schemas/mod_scenario_countries_add.schema.json`
Field descriptions: `docs/modding/MODDING_REFERENCE.md` §4.1

## Required Fields Per Entry
```json
{
  "iso3": "XXX",
  "name": "Display Name",
  "mapColor": "#RRGGBB",
  "governmentType": "...",
  "continent": "...",
  "region": "..."
}
```

## Leader Title by Government Type (1450 AD)

| `governmentType` | `governmentSubtype` | Typical `leaderTitle` |
|---|---|---|
| `monarchy` | `FeudalMonarchy` | `"King"` |
| `monarchy` | `AbsoluteMonarchy` | `"King"` |
| `monarchy` | `Empire` | `"Emperor"` |
| `monarchy` | `Duchy` | `"Duke"` |
| `monarchy` | `Principality` | `"Prince"` |
| `monarchy` | `GrandPrincipality` | `"Grand Prince"` |
| `monarchy` | `Shogunate` | `"Shogun"` |
| `authoritarian` | `Sultanate` | `"Sultan"` |
| `authoritarian` | `Emirate` | `"Emir"` |
| `authoritarian` | `Khanate` | `"Khan"` |
| `authoritarian` | `Empire` | `"Emperor"` |
| `theocracy` | *(Rome)* | `"Pope"` |
| `theocracy` | `MilitaryOrder` | `"Grand Master"` |
| `theocracy` | `Sultanate` | `"Sultan"` |
| `democracy` | `CityState` (Venice/Genoa) | `"Doge"` |
| `democracy` | `CityState` (Florence) | `"Gonfaloniere"` |
| `democracy` | `CityState` (Swiss) | `"Diet"` |

## Continent + Region Enum Values

**Continents:** `Africa`, `Americas`, `Asia`, `Europe`, `Oceania`, `Unknown`

**Regions:**
- Europe: `WesternEurope`, `NorthernEurope`, `SouthernEurope`, `EasternEurope`
- Asia: `WesternAsia`, `CentralAsia`, `EastAsia`, `SouthAsia`, `SoutheastAsia`
- Africa: `NorthernAfrica`, `SubSaharanAfrica`
- Americas: `NorthernAmerica`, `LatinAmericaCaribbean`
- Pacific: `AustraliaNewZealand`, `Melanesia`, `Micronesia`, `Polynesia`
- Fallback: `Unknown`

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
- `homelandTerm` is the uppercase string shown in the UI homeland panel (e.g. `"THE SULTANATE"`) — check `overrides/localization_en.csv` for existing values
- `leaderName` (not `rulerName`) sets the starting leader's name
- `militaryUnitTypeIds` must reference IDs defined in `scenario/units_define.json` or the base game

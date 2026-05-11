# GlobalProtocol: Old World Order – Claude Code Context

## Project Overview

This is a **historical scenario mod** for the game *Global Protocol* (Unity DOTS/ECS), set in 1450 AD. It defines ~120 medieval nations with historically accurate governments, armies, and leader titles.

**Mod ID:** `globalprotocol.old_world_order`  
**Engine location:** `C:\Personal\Genel\Projeler\NewWorldOrder\GlobalProtocol`

---

## Folder Layout

```
mod.json                         ← manifest (scenarioFolder: "scenario")
scenario/                        ← split scenario files (authoritative)
  scenario.json                  ← header (scenarioId, startYear, etc.)
  countries_add.json             ← ~120 custom country definitions
  countries_remove.json          ← base-game countries to remove
  countries_state.json           ← stability/corruption overrides
  provinces_ownership.json       ← province + region ownership
  units_define.json              ← custom unit type definitions
  units_deploy_armies.json       ← initial army stacks per province
Content/
  goals_old_world_order.json     ← national goals (path relative to mod root)
overrides/
  localization_en.csv            ← English display strings
  localization_tr.csv            ← Turkish display strings
  military_markers.json          ← UI military marker overrides
  game_flow.json                 ← game flow overrides
  Art/Units/                     ← unit artwork
flags/                           ← flag PNGs (128×80, named by ISO3)
docs/modding/                    ← schema documentation
  MODDING_REFERENCE.md           ← authoritative field reference
  schemas/                       ← JSON Schema files per domain
```

---

## Schema Authority

**Always consult these before editing data files:**

- `docs/modding/MODDING_REFERENCE.md` — complete field reference, all enum values
- `docs/modding/schemas/mod_scenario_countries_add.schema.json` — country fields
- `docs/modding/schemas/mod_scenario_countries_state.schema.json` — state fields
- `docs/modding/schemas/mod_scenario_units_define.schema.json` — unit type fields
- `docs/modding/schemas/mod_scenario_units_deploy_armies.schema.json` — army deployment

---

## Critical Conventions

### Country ISO3 Codes
All ISO3 codes are **uppercase, 3 characters**. Custom codes avoid conflicts with base-game modern nations:
- MYN = Ming Dynasty (not MNG = Mongolia)
- ARA = Aragon (not ARG = Argentina)
- VNC = Venice (not VEN = Venezuela)
- MVY = Muscovy (not MUS = Mauritius)
- JOS = Joseon (not KOR = South Korea)

### Country Fields in countries_add.json
- `leaderName` — initial leader's name (NOT `rulerName`, which is non-standard)
- `leaderTitle` — historical title string: `"Sultan"`, `"King"`, `"Emperor"`, `"Khan"`, `"Doge"`, `"Shogun"`, `"Pope"`, `"Grand Master"`, `"Duke"`, `"Grand Prince"`, `"Prince"`, etc.
- `homelandTerm` — uppercase noun shown in UI (e.g. `"THE SULTANATE"`, `"THE REALM"`)
- `continent` — must be one of: `Africa`, `Americas`, `Antarctica`, `Asia`, `Europe`, `Oceania`, `Unknown`
- `region` — must be one of: `WesternEurope`, `NorthernEurope`, `SouthernEurope`, `EasternEurope`, `WesternAsia`, `CentralAsia`, `EastAsia`, `SouthAsia`, `SoutheastAsia`, `NorthernAfrica`, `SubSaharanAfrica`, `NorthernAmerica`, `LatinAmericaCaribbean`, `AustraliaNewZealand`, `Melanesia`, `Micronesia`, `Polynesia`, `Unknown`

### Government Types (§8.1 of MODDING_REFERENCE.md)
`democracy`, `authoritarian`, `hybrid`, `monarchy`, `theocracy`, `military_junta`, `failed_state`, `city_state`

### State Overrides (countries_state.json)
- `stability` and `corruption` are **floats 0.0–1.0** (NOT integers 0–100)

### GDP Scale
All GDP values use `gdpScale: 0.001` — pre-industrial economics scaled to modern USD equivalents.

---

## Validation Commands

Validate a JSON file (PowerShell):
```powershell
Get-Content "scenario\countries_add.json" -Raw | ConvertFrom-Json
```

Validate all scenario files:
```powershell
Get-ChildItem "scenario\*.json" | ForEach-Object { 
  try { Get-Content $_.FullName -Raw | ConvertFrom-Json | Out-Null; Write-Host "OK: $($_.Name)" }
  catch { Write-Host "ERROR: $($_.Name) - $_" }
}
```

---

## Key Rules

1. **Do not edit `docs/modding/` files** — they are copies from the game engine docs, not mod data
2. **Never use raw integers for stability/corruption** — always 0.0–1.0 floats
3. **leader titles must be historically plausible for 1450 AD** — no "President", no "Prime Minister"
4. **continent and region must match the engine enums exactly** — case-sensitive
5. **Unit IDs must be unique** across all `unitTypes` entries
6. **Flag PNGs must be 128×80 pixels** in the `flags/` folder, named `ISO3.png`

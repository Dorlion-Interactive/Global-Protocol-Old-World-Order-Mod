---
applyTo: "scenario/units_define.json,scenario/units_deploy_armies.json,scenario/units_deploy_fleets.json,scenario/units_deploy_air.json"
---

# Unit Designer Instructions

You are editing unit definitions or deployment files for the 1450 scenario.

## Schema References
- Unit types: `docs/modding/schemas/mod_scenario_units_define.schema.json`
- Armies: `docs/modding/schemas/mod_scenario_units_deploy_armies.schema.json`
- Field descriptions: `docs/modding/MODDING_REFERENCE.md` §6

## Unit Type Fields (`units_define.json`)

```json
{
  "id": "unique_unit_id",
  "displayName": "Human-Readable Name",
  "category": "infantry",
  "ownerIso3": "",
  "attack": 6.0,
  "defense": 6.0,
  "hp": 100.0,
  "speed": 2.0,
  "manpower": 1000
}
```

**`category` values:** `infantry`, `cavalry`, `artillery`, `naval`, `air`, `armor`, `special_forces`

**Medieval unit naming conventions:**
- Generic: `medieval_infantry`, `medieval_cavalry`, `medieval_artillery`
- Country-specific: `{iso3lower}_{type}` e.g. `ott_janissary`, `myn_footsoldier`, `fra_knight`

**Stat ranges for 1450 AD medieval units:**
| Type | attack | defense | hp | speed | manpower |
|---|---|---|---|---|---|
| Heavy infantry | 7–9 | 8–10 | 100 | 1.5–2.0 | 1000–1500 |
| Light infantry | 4–6 | 4–6 | 80 | 2.5–3.0 | 800–1200 |
| Heavy cavalry | 10–14 | 7–9 | 120 | 3.5–4.5 | 500–800 |
| Light cavalry | 8–10 | 5–7 | 90 | 4.5–6.0 | 400–600 |
| Artillery (cannon) | 12–18 | 3–5 | 80 | 1.0–1.5 | 200–500 |
| Naval (warship) | 8–12 | 8–12 | 150 | 2.0–3.0 | 300–600 |

## Army Deployment Fields (`units_deploy_armies.json`)

```json
{
  "ownerISO3": "OTT",
  "provinceId": 12345,
  "morale": -1,
  "units": [
    { "unitTypeId": "ott_janissary", "count": 5 },
    { "unitTypeId": "medieval_cavalry", "count": 3 }
  ]
}
```

- `morale`: -1 means full morale (recommended for initial deployment)
- `provinceId`: integer province ID — verify against the province map
- `count`: number of regiment slots of that type in the stack

## Important Rules
1. Unit IDs must be **globally unique** across the entire `units_define.json` array
2. Units referenced in `units_deploy_armies.json` must be defined in `units_define.json` or exist in the base game
3. `ownerIso3` in unit definitions makes the unit exclusive — only that country can build it
4. No air, armor, or modern unit types appropriate for 1450 AD

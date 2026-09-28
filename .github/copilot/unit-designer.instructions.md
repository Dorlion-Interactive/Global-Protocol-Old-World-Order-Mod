---
applyTo: "scenario/units_define.json,scenario/units_override.json,scenario/units_deploy_armies.json,scenario/units_deploy_fleets.json,scenario/units_deploy_air.json"
---

# Unit Designer Instructions

You are editing unit definitions or deployment files for the 1450 scenario.

## Schema References
- Unit ids: `docs/modding/schemas/mod_scenario_units_define.schema.json`
- Unit roster entries (`units_override.json`): `docs/modding/schemas/unit_type.schema.json`
- Armies / fleets: `mod_scenario_units_deploy_armies.schema.json`, `mod_scenario_units_deploy_fleets.schema.json`
- Field descriptions: `docs/modding/MODDING_REFERENCE.md` §6 and §8.1

## Two Files Per Unit

- `units_define.json` — the unit id, its `category`, and optional `ownerIso3`
- `units_override.json` (replace mode, the scenario's `unitsOverrideFile`) — the same id with its **real** stats, costs and requirements

Because `units_override.json` defines every id, **stats written in `units_define.json` are ignored**. Change stats in `units_override.json`.

```json
{
  "id": "ottoman_janissary",
  "displayName": "Janissary",
  "category": "infantry",
  "ownerIso3": "OTT"
}
```

**`category` values:** `infantry`, `cavalry`, `artillery`, `armor`, `special_forces`, `naval`, `air` — this mod uses only infantry, cavalry, artillery and naval.

**`ownerIso3`:** makes the unit exclusive to that country. Omit the field for shared units — `""` fails the schema.

**Existing ids:** shared `medieval_infantry`, `medieval_cavalry`, `war_elephant`, `med_galley`, `med_cog`, `med_carrack`; country-specific `{nation}_{type}` such as `ottoman_janissary`, `france_knight`, `england_longbowman`, `mrc_samurai`, `ming_treasure_ship`, `portuguese_caravel`. Ids are unique and at most 29 bytes.

## Rosters

Each country's `militaryUnitTypeIds` in `countries_add.json` is an **enforced roster**: the country recruits only those ids plus the units it owns. A roster may grant another country's exclusive unit. A new unit is recruitable only by its owner and by countries whose roster lists it — add it to the right rosters. Landlocked nations deliberately list no ships.

## Army Deployment Fields (`units_deploy_armies.json`)

```json
{
  "ownerISO3": "OTT",
  "provinceId": 12345,
  "morale": -1,
  "units": [
    { "unitTypeId": "ottoman_janissary", "count": 5 },
    { "unitTypeId": "medieval_cavalry", "count": 3 }
  ]
}
```

- `morale`: -1 means full morale (recommended for initial deployment)
- `provinceId`: integer province ID — look it up in `docs/modding/PROVINCE_REFERENCE.md` or with `python dev/curate_browse.py`
- `count`: number of regiment slots of that type in the stack

## Important Rules
1. Unit IDs must be **unique** across `units_define.json`, and each must also exist in `units_override.json`
2. Deployments may only use the mod's own ids — base-game units are disabled by the replace-mode roster and `scenario.json`'s disabled lists
3. The deploying country must be allowed the unit (owner or roster)
4. No air, armor, missile or other modern unit types for 1450 AD

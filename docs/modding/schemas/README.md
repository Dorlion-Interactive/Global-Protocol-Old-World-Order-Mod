# Mod Schema Map

Every JSON Schema (draft-07) the game ships to modders. The same files are staged into
`StreamingAssets/modding/schemas/`, where the in-game **Mod Builder** reads them to generate its
editors — field labels, tooltips, slider bounds and validation all come from these documents, so a
schema and the editor can never disagree.

Source of truth is `.ai/configs/schemas/`. The set is declared once, in `SCHEMAS_TO_SYNC` in
`DataPipeline/sync_streaming_assets_configs.py`; `tools/sync_modding_docs_to_example_mod.ps1` reads
that list to refresh this folder.

## Manifest

| File | Schema |
|---|---|
| `mod.json` | `mod_manifest.schema.json` |

## Scenario (`scenario/`)

| File | Schema |
|---|---|
| `scenario.json` | `mod_scenario_header.schema.json` |
| `countries_add.json` | `mod_scenario_countries_add.schema.json` |
| `countries_remove.json` | `mod_scenario_countries_remove.schema.json` |
| `countries_state.json` | `mod_scenario_countries_state.schema.json` |
| `provinces_ownership.json` | `mod_scenario_provinces_ownership.schema.json` |
| `units_define.json` | `mod_scenario_units_define.schema.json` |
| `units_deploy_armies.json` | `mod_scenario_units_deploy_armies.schema.json` |
| `units_deploy_fleets.json` | `mod_scenario_units_deploy_fleets.schema.json` |
| `units_deploy_air.json` | `mod_scenario_units_deploy_air.schema.json` |

`mod_scenario_header.schema.json` composes the sibling schemas by `$ref`, so a single-file
`scenario.json` carrying inline `addCountries` / `provinceOwnerOverrides` / … validates against it
directly.

## Content overrides (`Content/`)

These four files are **JSON arrays**, merged into the base game by `id`: fields present in your entry
overwrite the base, fields you omit are left alone, and an unknown `id` is appended as a new entry.
The schema below describes **one array element**, not the whole file.

| File | Schema |
|---|---|
| `Content/buildings.json` | `building_type.schema.json` |
| `Content/units.json` | `unit_type.schema.json` |
| `Content/resources.json` | `resource_type.schema.json` |
| `Content/tech_tree.json` | `tech_tree.schema.json` |
| `Content/events/*.json` | `event.schema.json` (one event per file) |

## Config overrides (`overrides/`)

Sparse documents: write only the keys you want to change.

| File | Schema |
|---|---|
| `overrides/game_settings.json` | `game_settings.schema.json` |
| `overrides/doctrines.json` | `doctrines.schema.json` |
| `overrides/game_flow.json` | `game_settings.schema.json` (`game_flow` section) |
| `overrides/events.json` | `game_settings.schema.json` (`events` section) |
| `overrides/envoys.json` | `game_settings.schema.json` (`envoys` section) |

## Reference only

| Schema | Purpose |
|---|---|
| `country.schema.json` | The base game's country record. Not a mod file — read it to see which fields `countries_add.json` mirrors. |
| `laws.schema.json` | Shipped for reference and editor use. **`overrides/laws.json` is not read at runtime yet** — laws are still baked, so a laws override has no effect in-game. |

## Notes

- `game_settings.json`'s `game_flow` section holds autosave interval, autosave on/off, save-slot
  count and the pre-selected country. Those are the **player's own settings** (they live in
  `settings.json` and are edited from the Settings screen), so overriding them does nothing. The Mod
  Builder hides that section for this reason.
- `doctrines.json` overrides are **structure-locked**: branch, tier and doctrine positions are
  save-stable, so you may change values, effects and text, but not add, remove or reorder entries.
- Scenario domain files are optional; a missing file is skipped. Domain arrays are appended on merge.
- The runtime loader requires `scenario.json` to carry a non-empty `scenarioId`.

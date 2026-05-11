# Scenario Schema Map

This folder contains the JSON Schemas for split scenario mod files.

## File-to-Schema Mapping

- mod.json -> mod_manifest.schema.json
- scenario.json -> mod_scenario_header.schema.json
- countries_add.json -> mod_scenario_countries_add.schema.json
- countries_remove.json -> mod_scenario_countries_remove.schema.json
- countries_state.json -> mod_scenario_countries_state.schema.json
- units_define.json -> mod_scenario_units_define.schema.json
- units_deploy_armies.json -> mod_scenario_units_deploy_armies.schema.json
- units_deploy_fleets.json -> mod_scenario_units_deploy_fleets.schema.json
- units_deploy_air.json -> mod_scenario_units_deploy_air.schema.json
- provinces_ownership.json -> mod_scenario_provinces_ownership.schema.json

## Notes

- The runtime loader requires scenario.json with a non-empty scenarioId.
- Domain files are optional; missing files are skipped.
- Domain arrays are appended when merged.

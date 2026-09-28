---
applyTo: "Content/localization/*.csv"
---

# Localization Editor Instructions

You are editing CSV localization files for the 1450 scenario mod (`docs/modding/MODDING_REFERENCE.md` §8.3).

## File Format

- 13 files: `cz, de, en, es, es-419, fr, ja, ko, pt, pt-br, ru, tr, zh` in `Content/localization/`
- UTF-8, no BOM, **no header row** — the file starts directly with data rows
- Format: `key,value` (one per line). A row splits at its **first** comma, so values may contain commas and need no quoting.
- **All 13 files must carry the same keys.** There is no fallback between languages for keys only the mod defines — a key missing from a locale renders as the raw key for those players.

## Key Naming Conventions

| Key Pattern | Example | Description |
|---|---|---|
| `country.name.<ISO3>` | `country.name.OTT` | Country display name |
| `country.leader_title.<token>` | `country.leader_title.grand_prince` | Translation of a `leaderTitle` value |
| `country.homeland.term.<token>` | `country.homeland.term.the_sultanate` | Translation of a `homelandTerm` value (UPPERCASE) |
| `owo.doctrine.*`, `owo.goal.*`, `owo.task.*` | `owo.goal.…` | Mod doctrines and national goals |
| `doctrine.*` | | Re-skins of the base doctrine cards the mod keeps — intended |
| `mod.ui.*`, `mod.owo.popup.*` | `mod.ui.toolbar.welcome_tooltip` | Mod UI |

`<token>` = the value lowercased, apostrophes dropped, every other non-alphanumeric run → `_`. Both title and homeland keys are optional; without one the engine shows the raw value, and the base game already translates common titles such as `king` and `sultan`.

`country.homeland.<ISO3>` is only read for a country **without** a `homelandTerm`. Every country in this mod has one, so the existing `country.homeland.<ISO3>` rows are not shown in game.

## Adding a New Country

Append the name row to ALL 13 files, translated per language:
```
country.name.ISO3,Name in that language
```
If its `leaderTitle` / `homelandTerm` is new to the mod, also add `country.leader_title.<token>` / `country.homeland.term.<token>` rows to all 13.

## Status

en and tr are translated; the other 11 files currently hold English copies. Write real translations for new keys where you can.

## ISO3 Codes

`scenario/countries_add.json` defines all 137 codes the mod uses; every modern base-game country is removed (`countries_remove.json`). Do not invent codes.

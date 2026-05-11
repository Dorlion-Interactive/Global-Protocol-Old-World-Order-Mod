---
applyTo: "overrides/localization_en.csv,overrides/localization_tr.csv"
---

# Localization Editor Instructions

You are editing CSV localization files for the 1450 scenario mod.

## File Format

- **No header row** — the file starts directly with data rows
- Format: `key,value` (one per line)
- Only quote values if they contain a comma
- Both `localization_en.csv` (English) and `localization_tr.csv` (Turkish) must have matching keys

## Key Naming Conventions

| Key Pattern | Example | Description |
|---|---|---|
| `country.name.ISO3` | `country.name.OTT` | Country display name |
| `country.homeland.ISO3` | `country.homeland.OTT` | Homeland noun (UPPERCASE) |
| `country.leader_title.ISO3` | `country.leader_title.OTT` | Leader title displayed in UI |

## Homeland Term Rules
- **Must be UPPERCASE** — they are displayed directly in the UI
- Examples: `THE SULTANATE`, `THE MIDDLE KINGDOM`, `THE REALM`, `MOTHERLAND`, `LA PATRIA`
- If a homeland term is already in the CSV, do not change it without user confirmation

## Adding a New Country

When adding a new country, append three lines to BOTH CSV files:
```
country.name.ISO3,Name in English
country.homeland.ISO3,THE HOMELAND TERM
country.leader_title.ISO3,Sultan
```

For Turkish (`localization_tr.csv`), provide the Turkish equivalents:
```
country.name.ISO3,Türkçe İsim
country.homeland.ISO3,VATAN TERİMİ
country.leader_title.ISO3,Sultan
```

## Existing ISO3 Codes in This Mod

The following codes are currently used (do not invent new ones without updating countries_add.json):
OTT, MYN, ENG, CAS, ARA, MVY, VNC, MAM, TIM, JOS, VIJ, AZT, INC, BUR, PAP, NAP, SCT, HAB, BOH, TEU, DAN, SWD, NVD, GEN, MIL, BYZ, WAL, MOL, LTH, MAL, SON, ABY, BNK, ZIM, AKK, DEL, MAJ, AYU, MRC, TIB, MAY, GRN, FLR, SAV, NAV, SRB, MOR, HFS, KKY, KZN, KRM, GUJ, BAH, BNG, MLC, DVT, KNG, KBR, RYU

Plus base-game codes that remain active: FRA, PRT, CHE, POL, HUN, and others not in `countries_remove.json`.

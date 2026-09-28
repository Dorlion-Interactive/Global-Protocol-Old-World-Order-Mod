# Project Atlantis: example event mod

A minimal data-driven event chain. It has no scripts and needs no permissions.

- **`atlas_01`** is a `scripted` event for the player (`target: "player"`). It fires once
  (`fire_once`), on the first monthly check from June 2026 (`date_after`), with no random roll
  (`immediate`).
  - **Send an expedition** sets the flag `atlantis_investigated` and queues `atlas_02` for one
    month later (a `fire_event` effect with `delay_months: 1`).
  - **Leave it to the scientists** sets `atlantis_ignored`. Nothing else happens.
- **`atlas_02`** is a `reactive` event with no triggers, so only the chain can fire it. When the
  chain comes due, its `has_flag` condition is checked again.

Both events use the `geopolitical_crisis` category, so they show as popups even when the
player's notification setting is "Critical only". The text is in
`Content/localization/en.csv` and `tr.csv`. The `title` / `description` / `text` fields in the
JSON are the fallback for other languages.

## Try it

1. Copy this folder to your mods folder, e.g.
   `%USERPROFILE%/Documents/GlobalProtocol/Mods/example.atlantis/`.
2. Enable **Project Atlantis (example)** on the Loadout screen.
3. Start a 2026 campaign as any country. `atlas_01` appears at the first monthly check in June
   2026 (days 6–8). If another event is still open, or one fired in the last 60 days, it comes
   at the first monthly check after that. `immediate` removes the random roll but not the
   competition: if another event is also eligible at that check, one of them is picked at random,
   weighted by `priority`. `atlas_01` uses `priority: 10` for the best odds; if it still loses,
   it comes at a later check.

See §8.7 of [`MODDING_REFERENCE.md`](../../MODDING_REFERENCE.md) for how events are loaded,
evaluated and chained.

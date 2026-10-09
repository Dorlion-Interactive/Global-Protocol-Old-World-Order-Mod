# NewWorldOrder – HUD Theming Guide

Last updated: 2026-10-08

A mod can recolour and resize the game interface with one file, `Content/ui/theme.json`. The Mod Builder's
**INTERFACE** tab edits it (section **HUD THEME**), and **Validate Mod** checks it. Players who do not use
the mod never see any of it.

The mod needs the `InjectUI` permission (`"permissions": ["InjectUI"]`), exactly like the toolbar injection.
Fonts cannot be changed by a mod.

---

## 1. What a theme can and cannot do

**What it changes.** The HUD is styled through *design tokens*: named values such as `--surface-1`
(a panel colour) or `--t-body` (the body text size) that the style sheets reference with `var(--surface-1)`.
A theme redeclares tokens, so everything styled through a token changes at once, including the hover and
pressed states. The list of tokens is `StreamingAssets/modding/hud_theme_tokens.json` (about 220: colours
and sizes), and the Mod Builder lists them in groups with a search box.

**What it does not change.** Tokens recolour only the part of the interface that is styled through them
today. Two things are outside their reach, and a theme file cannot change either:

- colours the game sets in code (some bars, badges and per-country colours), and the charts, which are drawn
  by code;
- the map itself (country colours, borders, labels).

Large parts of the stylesheets still use literal colours instead of tokens. Moving them onto tokens is
planned work in the game; until it lands, a token you change may recolour only some of a screen. Use
**rules** (section 4) for anything the tokens miss. Expect a theme to look different on different screens,
and check the HUD in a running game.

Inline styles set by the game's code always win over a theme (a theme is a style sheet, and an inline value
beats a sheet value). That is rare for colours and sizes, but it is the reason a rule can fail to take effect.

---

## 2. `Content/ui/theme.json`

```json
{
  "base": "classic",
  "tokens": {
    "--surface-1": "#1b2230",
    "--surface-2": "#232b3d",
    "--color-neon-cyan": "#ffb347",
    "--t-body": "17px"
  },
  "rules": [
    { "selector": "#top-bar", "background-color": "#101820", "border-color": "#ffb347" }
  ]
}
```

| Field | Description |
|---|---|
| `base` | Optional. Id of a built-in theme (§5) the tokens are applied on top of. Leave it out and the player's own theme shows through. With several mods, the last one that names a base wins. |
| `tokens` | Optional. Token name to value. Only tokens listed in `hud_theme_tokens.json` change anything. |
| `rules` | Optional. Extra selector rules (§4), applied after the tokens, in file order. |

**Values.** Colours: `#rgb`, `#rrggbb`, `#rrggbbaa`, `rgb(r, g, b)`, `rgba(r, g, b, a)` (alpha 0 to 1). Sizes:
`12px` or `50%`. Plain numbers for number tokens. Any value may be `var(--other-token)`. A colour token takes a
colour, a size token a size; a wrong kind is a Validate Mod error and is dropped at load.

**Aliases follow.** Some tokens are defined as another token (`--color-cyan` is `var(--color-neon-cyan)`).
Change the one they point at and the alias changes with it.

**Sparse by design.** Write only what you change. The Mod Builder removes a row that returns to the game's own
value, and an untouched token keeps the game's value.

---

## 3. Several mods

Active mods with a theme file are merged in load order: a later token replaces an earlier one with the same
name, rules are concatenated in order, and the last `base` wins. The result is applied once when the player
enters the game and removed when they return to the main menu, so one mod's theme never lingers into another
game.

---

## 4. Rules

A rule is a selector and the properties it sets. The selector is checked by the game's own selector parser
(the Mod Builder shows the parser's message while you type). Use the HUD's element names and classes
(`#top-bar`, `.stat-bar`, `.nav-tab:hover`); `Label` and `Button` select by type. Properties a rule may set:

`color`, `background-color`, `background-image`, `-unity-background-image-tint-color`, `border-color`
(and the four sides), `border-width` (and the four sides), `border-radius` (and the four corners), `opacity`,
`font-size`, `letter-spacing`, `-unity-font-style` (`normal`, `bold`, `italic`, `bold-and-italic`), `margin`,
`padding` (and the four sides of each), `width`, `height`, `min-width`, `min-height`, `max-width`,
`max-height`, `left`, `right`, `top`, `bottom`, `position` (`relative`, `absolute`), `display`
(`flex`, `none`), `flex-direction`.

`background-image` is a path inside the mod folder (png or jpg, 4 MB and 2048 pixels at most). Anything else
is a Validate Mod error and is skipped. Colour properties never take `inherit`, `initial`, `unset`, `auto` or
`none`; write the colour.

Rules cost nothing per frame; the whole theme is one style sheet, built once when the game screen is entered
and restyled once. Keep selectors specific: a `*` rule restyles every element.

---

## 5. Built-in themes (player setting)

The game has a small registry of built-in themes. A built-in theme is one USS file that redeclares `:root`
tokens only, switched by adding or removing a style sheet on the HUD root. The player chooses one with the
`UiTheme` setting in `settings.json`; the Settings screen shows the choice once more than one theme exists.

**Today only `classic` exists.** It is the HUD as it has always looked and adds no sheet, so a mod's
`"base": "classic"` and an absent `base` look the same. Naming a base that is not registered is ignored (Validate
Mod warns). More themes, and the work that makes tokens cover the whole interface, are planned.

---

## 6. Checking your theme

- **Validate Mod** reports unknown tokens (warning), values of the wrong kind (error), unknown bases (warning),
  invalid selectors, unsupported properties and invalid values (errors), and missing, oversized or
  out-of-folder images (warning).
- Problems the game meets while applying a theme are logged (`[ModHud:<mod id>]`) and listed with the mod's
  load errors; the rest of the theme still applies.
- If the engine's internal style API changes in a future Unity version, the game logs one warning, ignores
  mod themes and keeps the normal look. Nothing else breaks.

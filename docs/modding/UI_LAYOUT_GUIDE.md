# NewWorldOrder – HUD Layout Guide (replace or hide a HUD slot)

Last updated: 2026-10-08

A mod can rearrange or remove parts of the game HUD with `Content/ui/layout.json` and small layout files. The Mod
Builder's **INTERFACE** tab edits them (section **HUD SLOTS**), and **Validate Mod** checks them. The mod needs the
`InjectUI` permission. Players who do not use the mod see the HUD exactly as before.

---

## 1. Slots

The HUD is split into ten slots, each a run of the game's top-level HUD elements. The full list, each slot's element
names, which names a replacement must keep and which slots may be hidden is the generated file
`StreamingAssets/modding/hud_slots.json`.

| Slot | Contains | Replace | Hide |
|---|---|---|---|
| `topbar` | stats, date, speed controls | yes | no |
| `alerts` | alert bar, priority strip, pause / autosave ribbons | yes | no |
| `sidebar` | the country panel and its tab content | yes | no |
| `rail` | the domain rail (the ten tabs) | yes | no |
| `mapmodes` | map mode buttons | yes | yes |
| `statusbar` | the bottom status bar | yes | yes |
| `outliner` | the outliner panel | yes | yes |
| `tooltips` | province and army hover cards | no (the game positions them) | no |
| `eventpopup` | the event popup | yes | no |
| `armybar` | the army command bar | yes | no |

---

## 2. `Content/ui/layout.json`

```json
{
  "slots": {
    "mapmodes":  { "mode": "replace" },
    "statusbar": { "mode": "hide" },
    "outliner":  { "mode": "replace", "file": "Content/ui/layouts/my_outliner.uxml" }
  }
}
```

| Field | Description |
|---|---|
| `mode` | `replace` (default) rebuilds the slot from your layout file, `hide` removes it from the screen, `vanilla` leaves it alone. |
| `file` | Replace only. A UXML file inside the mod folder. Defaults to `Content/ui/layouts/<slot id>.uxml`. |

A slot that is not listed is untouched. If an entry is wrong (unknown slot, a slot that cannot be hidden, a missing or
invalid layout file) that slot stays exactly as the game draws it, the problem is logged (`[ModHud:<mod id>]`) and listed
with the mod's load errors, and the other slots still apply. When several mods set the same slot, the one later in load order
wins and the game logs a warning.

---

## 3. A layout file

A layout is a restricted UXML document: a `UXML` root holding `VisualElement`, `Label`, `Button` and `ScrollView`
elements with the attributes `name`, `class`, `text`, `picking-mode`, `focusable`, `style` and (on a `Button`) `hook`.
No `Style`, `Template` or `Instance`, no DTD or external references; at most 256 KB, 32 levels and 2000 elements.

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
  <ui:VisualElement name="mod-mapmodes-column" style="position: absolute; left: 90px; top: 120px; flex-direction: column;">
    <ui:Label text="MAP" style="color: #ffb347;" />
    <ui:Button name="mm-btn-political" />
    <ui:Button name="mm-btn-terrain" />
  </ui:VisualElement>
</ui:UXML>
```

* **Game elements are placed by name.** An element whose `name` is one of the slot's game element names (see
  `hud_slots.json`) is a *placeholder*: the game's own live element, with everything inside it, takes that place. Its
  `text`, `style` and children in the layout are ignored (its `class` is added). The game keeps it working, which is why the
  controllers never break. Each game element can be placed once, and not inside another placed game element.
* **Your own elements** are built fresh. Their names must start with `mod-` (or be left out). `text` may be a plain string or
  `@some.key` (a localization key from `Content/localization/`). `style` takes the properties listed in
  [UI_INJECTION_GUIDE.md](UI_INJECTION_GUIDE.md) §5.1. A `Button`'s `hook` raises `OnUiAction` with that name, like a toolbar
  button.
* **Required elements.** A replacement must place every required game element of its slot (for the top bar the date and the
  four speed buttons, for the rail all ten tabs, ...), or contain the game element that holds it. Otherwise the slot stays
  vanilla.
* **What happens to the rest.** Game elements the layout does not place are *parked*: moved into a hidden holder that stays in
  the tree, so the game can still update them. Hiding a slot parks all of it.

The Mod Builder's **COPY GAME LAYOUT** writes the game's own layout of a slot into your mod as a starting point. An unmodified
copy places every game element and reproduces the vanilla slot exactly; edit it by removing, moving and wrapping the
placeholders. The copies are also in `StreamingAssets/modding/hud_slots/<slot id>.uxml`.

---

## 4. Limits worth knowing

* USS rules that depend on a game parent no longer match an element you moved out from under it (for example a rule written
  as `.top-bar-container .speed-btn`). Restyle with a [theme rule](UI_THEMING_GUIDE.md) on the class you add in the layout.
* The game's own code can still measure or toggle a parked panel (collapsing the sidebar, for example); with the sidebar slot
  replaced those toggles change a hidden panel and nothing visible.
* A replacement is applied when the player enters the game and removed when they return to the main menu; it is not saved
  and does not affect multiplayer state. Layout cost is a few hundred element moves, once.
* The same layout cannot give a slot a different size on different resolutions; position with the style properties
  (`position`, `left`, `top`, ...) like the example.

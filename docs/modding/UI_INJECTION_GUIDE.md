# NewWorldOrder – UI Injection Guide

Last updated: 2026-05-11

Mods with the `InjectUI` permission can add UI elements to the HUD and respond to player interactions via the `OnUiAction` hook event.

---

## 1. Permission Requirement

```json
{ "permissions": ["InjectUI"] }
```

Attempts to inject UI elements without this permission are rejected at load time.

---

## 2. What Can Be Injected

Current runtime support:
- **Custom toolbar buttons** — converted into HUD overlay buttons via `mod-hud-overlay`

Declared but not yet executed by the runtime:
- **Province detail rows**
- **Country panel rows**
- **Notification entries**

Not supported:
- New full-screen panels
- Overriding or hiding existing core HUD elements
- Shader/texture replacement via UI injection (use `Content/ui/` overrides instead)

---

## 3. UI Injection via mod.json

Declare injection points under `entrypoints.ui`:

```json
{
  "entrypoints": {
    "ui": "Content/ui/inject.json"
  }
}
```

---

## 4. inject.json Schema

```json
{
  "toolbarButtons": [
    {
      "id": "my_mod.open_ledger",
      "iconPath": "Content/ui/icons/ledger.png",
      "tooltip": "Open Mod Ledger",
      "hookName": "open_ledger"
    }
  ]
}
```

`provinceDetailRows`, `countryPanelRows`, and notification-style entries are still reserved shapes. They may appear in docs or forward-looking examples, but the current runtime does not build or refresh them.

---

## 5. Toolbar Buttons

| Field | Required | Description |
|---|---|---|
| `id` | ✓ | Unique button ID within the mod |
| `iconPath` | ✓ | Relative path to a 32×32 PNG icon in the mod folder |
| `tooltip` | | Reserved field. The current injector ignores it, so no tooltip is shown yet. |
| `hookName` | ✓ | Name passed to `OnUiAction` when clicked |

When the button is clicked, `ModHookBus.OnUiAction` fires with `(hookName, modId)`. Your WASM `on_ui_action` export or C# delegate receives this.

---

## 6. Province Detail Rows

This shape is documented for the intended ABI, but it is not wired in the current runtime.

Injected rows appear in the Province Detail panel below the standard stat rows.

| Field | Required | Description |
|---|---|---|
| `id` | ✓ | Unique row ID |
| `label` | ✓ | Display label (raw string or localization key) |
| `valueExpression` | ✓ | Data binding expression (see §8) |
| `iconPath` | | Optional 16×16 PNG icon |
| `format` | | Format string, e.g. `"{0:0.0}%"` (default: `"{0}"`) |
| `showWhenZero` | | Show row when value is 0 (default: `false`) |

---

## 7. Country Panel Rows

This shape is documented for the intended ABI, but it is not wired in the current runtime.

Same shape as province rows. `valueExpression` uses `country.` prefix.

---

## 8. Value Expressions

Value expressions are dot-separated paths into a lightweight context object provided at render time.

**Province context (`province.*`):**

| Expression | Type | Description |
|---|---|---|
| `province.id` | int | Province numeric ID |
| `province.owner_iso3` | string | Current owner ISO3 |
| `province.population` | int | Population |
| `province.gdp` | float | Provincial GDP (USD millions) |
| `province.stability` | float | Stability 0–1 |
| `province.tech_level` | int | Provincial tech level |

**Country context (`country.*`):**

| Expression | Type | Description |
|---|---|---|
| `country.iso3` | string | ISO3 |
| `country.treasury` | float | Treasury (USD millions) |
| `country.gdp` | float | Annual GDP (USD millions) |
| `country.stability` | float | Stability 0–1 |
| `country.tech_level` | int | Tech level |
| `country.manpower` | int | Available manpower |
| `country.war_count` | int | Active wars |
| `country.alliance_count` | int | Active alliances |

Custom expressions are not yet supported. If your value needs computation, pre-compute it from a WASM/C# hook and store it in a `ModHookBus`-registered state dictionary, then read it via a `mod_state.*` expression (reserved for future extension).

---

## 9. Icon Assets

All icon PNGs must live under the mod folder. Recommended sizes:
- Toolbar buttons: 32×32
- Panel row icons: 16×16

The game loads them via `ModAssetLoader.LoadFlagSprite()` which caches the result for the session lifetime.

---

## 10. USS Overrides

Place `.uss` files under `Content/ui/` to override or extend existing styles. The game merges USS from all enabled mods in load order. Use `.unity-button--toolbar-mod` and `.unity-label--panel-row-mod` class selectors for injected elements to avoid conflicts with core styles.

Do **not** set `color: inherit` or `color: initial` in mod USS files — these values are unsupported by UI Toolkit and will produce warnings. Use explicit hex colors instead.

---

## 11. Responding to UI Actions (C# path)

```csharp
// In your mod assembly (requires InjectUI permission)
ModHookBus.OnUiAction += (hookName, modId) =>
{
    if (modId != "com.myname.mymod") return;
    if (hookName == "open_ledger")
        MyModLedgerPanel.Show();
};
```

---

## 12. Responding to UI Actions (WASM path)

```wat
(func $on_ui_action (export "on_ui_action")
  (param $hook_name_ptr i32) (param $hook_name_len i32)
  (param $mod_id_ptr i32) (param $mod_id_len i32)
  ;; Compare hook_name to "open_ledger" and react
)
```

---

## 13. Localization for Injected UI

All user-visible strings in `inject.json` (labels, tooltips) may be plain strings or localization keys. Localization keys are resolved via the active language CSV. Add your keys to `Content/localization/en.csv` and `tr.csv` following the standard CSV format used by the base game.

For compatibility, the loader also reads legacy files like `overrides/localization_en.csv`, but new mods should use `Content/localization/<language>.csv`.

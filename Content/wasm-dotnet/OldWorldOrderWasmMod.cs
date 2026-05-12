// GlobalProtocol: Old World Order — WASM .NET Entrypoint
//
// Demonstrates component-model WASM lifecycle mapping.
// Subscribes to engine dispatch hooks and routes them to shared logic.

using GlobalProtocol.ModWasmSdk;
using GlobalProtocol.Mods.OldWorldOrder;

namespace OldWorldOrder;

internal sealed class OldWorldOrderWasmMod : WasmModBase, IModHost
{
    private GlobalProtocol.Mods.OldWorldOrder.OldWorldOrder _shared = null!;

    public void ShowPopup(string title, string body)
    {
        Gp.ShowPopup(title, body);
    }

    public void Log(string message)
    {
        Gp.Log(message);
    }

    public string GetModVersion()
    {
        try
        {
            string[] paths = { "mod.json", "../mod.json", "../../mod.json" };
            foreach (var path in paths)
            {
                if (System.IO.File.Exists(path))
                {
                    string content = System.IO.File.ReadAllText(path);
                    var match = System.Text.RegularExpressions.Regex.Match(content, @"""version""\s*:\s*""([^""]+)""");
                    if (match.Success)
                        return match.Groups[1].Value;
                }
            }
        }
        catch
        {
            // fallback if sandboxing restricts I/O
        }
        return "0.2.2";
    }

    protected override void OnInitialize()
    {
        Gp.KeepHostImportLinks();

        _shared = new GlobalProtocol.Mods.OldWorldOrder.OldWorldOrder(this);
        _shared.OnInitialize();
        Gp.Log("OWO init (.NET WASM SDK hooks abstracted)");
    }

    // Called every game tick.
    // tick = total elapsed ticks, year/month = current in-game date.
    protected override void OnTick(int tick, int year, int month)
    {
        _shared?.OnTick(tick, year, month);
    }

    // Called when a war is declared.
    // attacker / defender are country indices (0 = local player in single-player).
    protected override void OnWarDeclared(int attacker, int defender, int tick)
    {
        _shared?.OnWarDeclared(attacker, defender, tick);
    }

    // Called when peace is signed between two countries.
    protected override void OnPeaceSigned(int proposer, int target)
    {
        _shared?.OnPeaceSigned(proposer, target);
    }

    // Called when a country finishes researching a technology.
    protected override void OnTechResearched(int countryIndex, int techIndex)
    {
        _shared?.OnTechResearched(countryIndex, techIndex);
    }

    // Called when a building finishes construction in a province.
    protected override void OnBuildingCompleted(int provinceId, int buildingDefIndex)
    {
        _shared?.OnBuildingCompleted(provinceId, buildingDefIndex);
    }

    // Called when any scripted event fires for any country.
    protected override void OnEventFired(int countryIndex, int eventIndex)
    {
        _shared?.OnEventFired(countryIndex, eventIndex);
    }

    // Called when a country is fully eliminated from the game.
    protected override void OnCountryEliminated(int countryIndex)
    {
        _shared?.OnCountryEliminated(countryIndex);
    }

    // Called when a toolbar button (registered in mod.json entrypoints.ui) is clicked.
    // Always check modId first — other mods fire this hook too.
    protected override void OnUiAction(string hookName, string modId)
    {
        _shared?.OnUiAction(hookName, modId);
    }
}

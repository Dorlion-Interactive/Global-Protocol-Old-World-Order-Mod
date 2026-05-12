// GlobalProtocol: Old World Order — Mod Entrypoint
//
// This is your mod's main C# file. Override any hook below to react to game events.
// Delete the ones you don't need. That's it — no boilerplate required.
//
// ModHookBus.FireEvent(countryIndex, eventId) — trigger a scripted event
//   countryIndex 0 = the local player's country in single-player
//   eventId      = the event ID from your Content/events/*.json file

using GlobalProtocol.Core.Mods;

namespace GlobalProtocol.Mods.OldWorldOrder;

public sealed class ModEntrypoint : ModBase, IModHost
{
    private OldWorldOrder _shared = null!;

    public void ShowPopup(string title, string body)
    {
        ModHookBus.ShowPopup(OldWorldOrder.ModId, title, body);
    }

    public void Log(string message)
    {
        // Native C# delegate path logs natively or via unity engine if available.
    }

    public string GetModVersion()
    {
        try
        {
            string path = System.IO.Path.Combine(System.IO.Path.GetDirectoryName(typeof(ModEntrypoint).Assembly.Location) ?? "", "..", "mod.json");
            if (System.IO.File.Exists(path))
            {
                string content = System.IO.File.ReadAllText(path);
                var match = System.Text.RegularExpressions.Regex.Match(content, @"""version""\s*:\s*""([^""]+)""");
                if (match.Success)
                    return match.Groups[1].Value;
            }
        }
        catch
        {
            // fallback if pathing fails
        }
        return "0.2.2";
    }

    protected override void OnInitialize(IModServices services)
    {
        _shared = new OldWorldOrder(this);
        _shared.OnInitialize();
    }

    // Called every game tick.
    // tick  = total elapsed ticks, year/month = current in-game date.
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

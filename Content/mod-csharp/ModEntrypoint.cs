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

    private static readonly System.Action<string>? _unityLog = ResolveUnityLog();

    private static System.Action<string>? ResolveUnityLog()
    {
        try
        {
            var debugType = System.Type.GetType("UnityEngine.Debug, UnityEngine.CoreModule")
                         ?? System.Type.GetType("UnityEngine.Debug, UnityEngine");
            if (debugType != null)
            {
                var method = debugType.GetMethod("Log", new[] { typeof(object) });
                if (method != null)
                    return msg => method.Invoke(null, new object[] { msg });
            }
        }
        catch { }
        return null;
    }

    public void Log(string message)
    {
        string formatted = $"[OldWorldOrder:CSharp] {message}";
        if (_unityLog != null)
            _unityLog(formatted);
        else
            System.Console.WriteLine(formatted);
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
        return "unknown";
    }

    protected override void OnInitialize(IModServices services)
    {
        Log("ModEntrypoint.OnInitialize() called by engine runtime!");
        _shared = new OldWorldOrder(this);
        _shared.OnInitialize();
    }

    // Called every game tick.
    // tick  = total elapsed ticks, year/month = current in-game date.
    protected override void OnTick(int tick, int year, int month)
    {
        if (tick <= 5 || tick % 100 == 0)
        {
            Log($"OnTick: tick={tick}, date={year}-{month:D2}");
        }
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

    // Called when two countries form an alliance.
    protected override void OnAllianceFormed(int proposerIndex, int partnerIndex)
    {
        _shared?.OnAllianceFormed(proposerIndex, partnerIndex);
    }

    // Called when an alliance is broken.
    protected override void OnAllianceBroken(int breakerIndex, int partnerIndex)
    {
        _shared?.OnAllianceBroken(breakerIndex, partnerIndex);
    }

    // Called when a bilateral trade agreement is signed.
    protected override void OnTradeAgreementSigned(int country1Index, int country2Index)
    {
        _shared?.OnTradeAgreementSigned(country1Index, country2Index);
    }

    // Called when a province changes ownership.
    protected override void OnProvinceCaptured(int provinceId, int newOwner, int oldOwner)
    {
        _shared?.OnProvinceCaptured(provinceId, newOwner, oldOwner);
    }

    // Called each monthly economy tick.
    protected override void OnEconomyTick(int year, int month)
    {
        _shared?.OnEconomyTick(year, month);
    }

    // Called when a toolbar button (registered in mod.json entrypoints.ui) is clicked.
    // Always check modId first — other mods fire this hook too.
    protected override void OnUiAction(string hookName, string modId)
    {
        Log($"OnUiAction received: hookName='{hookName}', modId='{modId}'");
        _shared?.OnUiAction(hookName, modId);
    }
}

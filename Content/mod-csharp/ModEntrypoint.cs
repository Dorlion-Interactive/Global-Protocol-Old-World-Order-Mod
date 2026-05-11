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

public sealed class ModEntrypoint : ModBase
{
    private const string MOD_ID = "globalprotocol.old_world_order";

    // Called every game tick.
    // tick  = total elapsed ticks, year/month = current in-game date.
    protected override void OnTick(int tick, int year, int month)
    {
    }

    // Called when a war is declared.
    // attacker / defender are country indices (0 = local player in single-player).
    protected override void OnWarDeclared(int attacker, int defender, int tick)
    {
    }

    // Called when peace is signed between two countries.
    protected override void OnPeaceSigned(int proposer, int target)
    {
    }

    // Called when a country finishes researching a technology.
    protected override void OnTechResearched(int countryIndex, int techIndex)
    {
    }

    // Called when a building finishes construction in a province.
    protected override void OnBuildingCompleted(int provinceId, int buildingDefIndex)
    {
    }

    // Called when any scripted event fires for any country.
    protected override void OnEventFired(int countryIndex, int eventIndex)
    {
    }

    // Called when a country is fully eliminated from the game.
    protected override void OnCountryEliminated(int countryIndex)
    {
    }

    // Called when a toolbar button (registered in mod.json entrypoints.ui) is clicked.
    // Always check modId first — other mods fire this hook too.
    protected override void OnUiAction(string hookName, string modId)
    {
        if (modId != MOD_ID) return;

        // if (hookName == "owo.my_button") { ... }
    }
}


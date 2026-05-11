// GlobalProtocol: Old World Order — WASM Hooks (Variant A: .NET-to-WASM / WASI)
//
// This is your mod's main C# file for the WASM variant.
// The engine calls only the hooks you export here. Delete the ones you don't need.
// To call back INTO the game (fire events, log, read state), use Gp.* (see Gp.cs).
//
// Gp.FireEvent(countryIndex, eventId) — trigger a scripted event
//   countryIndex 0 = the local player's country in single-player
//   eventId      = the event ID from your Content/events/*.json file
//
// Build:
//   dotnet workload install wasi-experimental   (once per machine)
//   dotnet publish -c Release
//   → produces Content/mod.wasm

using System.Runtime.InteropServices;

namespace OldWorldOrder;

// Required by the .NET WASI linker. GlobalProtocol does not call _start.
internal static class WasiInit { internal static void Run() { } }

internal static class Hooks
{
    private const string MOD_ID = "globalprotocol.old_world_order";

    // Called every game tick.
    // tick  = total elapsed ticks, year/month = current in-game date.
    [UnmanagedCallersOnly(EntryPoint = "on_game_tick")]
    public static void OnGameTick(int tick, int year, int month)
    {
    }

    // Called when a war is declared.
    // attacker / defender are country indices (0 = local player in single-player).
    [UnmanagedCallersOnly(EntryPoint = "on_war_declared")]
    public static void OnWarDeclared(int attacker, int defender, int tick)
    {
    }

    // Called when peace is signed between two countries.
    [UnmanagedCallersOnly(EntryPoint = "on_peace_signed")]
    public static void OnPeaceSigned(int proposer, int target)
    {
    }

    // Called when a country finishes researching a technology.
    [UnmanagedCallersOnly(EntryPoint = "on_tech_researched")]
    public static void OnTechResearched(int countryIndex, int techIndex)
    {
    }

    // Called when a building finishes construction in a province.
    [UnmanagedCallersOnly(EntryPoint = "on_building_completed")]
    public static void OnBuildingCompleted(int provinceId, int buildingDefIndex)
    {
    }

    // Called when any scripted event fires for any country.
    [UnmanagedCallersOnly(EntryPoint = "on_event_fired")]
    public static void OnEventFired(int countryIndex, int eventIndex)
    {
    }

    // Called when a country is fully eliminated from the game.
    [UnmanagedCallersOnly(EntryPoint = "on_country_eliminated")]
    public static void OnCountryEliminated(int countryIndex)
    {
    }

    // Called when a toolbar button (registered in mod.json entrypoints.ui) is clicked.
    // Always check modId first — other mods fire this hook too.
    [UnmanagedCallersOnly(EntryPoint = "on_ui_action")]
    public static void OnUiAction(
        int hookNamePtr, int hookNameLen,
        int modIdPtr,    int modIdLen)
    {
        if (Gp.DecodeString(modIdPtr, modIdLen) != MOD_ID) return;

        // var hookName = Gp.DecodeString(hookNamePtr, hookNameLen);
        // if (hookName == "owo.my_button") { ... }
    }
}

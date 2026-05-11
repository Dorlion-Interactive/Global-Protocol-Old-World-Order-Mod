// GlobalProtocol: Old World Order — WASM Hooks (Variant A: .NET-to-WASM / WASI)
//
// This is your mod's main C# file for the WASM variant.
// The engine calls only the hooks you export here. Delete the ones you don't need.
// To call back INTO the game (popup, log, read state), use Gp.* (see Gp.cs).
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
    private const string STARTUP_POPUP_TITLE = "Old World Order, 1450";
    private const string TOOLBAR_POPUP_TITLE = "Strategic Briefing";

    private static bool _welcomeShown;

    [UnmanagedCallersOnly(EntryPoint = "on_init")]
    public static void OnInit()
    {
        Gp.Log("OWO init (.NET WASM)");
    }

    // Called every game tick.
    // tick  = total elapsed ticks, year/month = current in-game date.
    [UnmanagedCallersOnly(EntryPoint = "on_game_tick")]
    public static void OnGameTick(int tick, int year, int month)
    {
        if (_welcomeShown) return;

        _welcomeShown = true;
        Gp.ShowPopup(STARTUP_POPUP_TITLE, BuildStartupBody(year, month));
        Gp.Log("OWO: welcome popup shown on first tick via show_mod_popup (.NET WASM)");
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

        var hookName = Gp.DecodeString(hookNamePtr, hookNameLen);
        if (hookName != "owo.welcome") return;

        Gp.ShowPopup(TOOLBAR_POPUP_TITLE, BuildToolbarBody());
        Gp.Log("OWO: welcome popup reopened via toolbar button via show_mod_popup (.NET WASM)");
    }

    private static string BuildStartupBody(int year, int month)
    {
        var monthText = month.ToString("00");
        return $"Date: {year}-{monthText}\n"
            + "\n"
            + "Europe and Asia stand between old feudal orders and rising centralized states.\n"
            + "Trade routes across the Mediterranean, Black Sea, Indian Ocean, and Silk Road are the arteries of power.\n"
            + "Gunpowder armies are emerging, but cavalry, levies, and fortresses still decide most wars.\n"
            + "\n"
            + "You command one of 120+ historical polities with period-appropriate rulers, borders, and military posture.\n"
            + "Use the crown button in the toolbar to reopen this briefing at any time.";
    }

    private static string BuildToolbarBody()
    {
        return "1450 Intelligence Report\n"
            + "\n"
            + "- The Ottoman state is expanding through the Balkans and Anatolia\n"
            + "- The Hundred Years' War era has ended, but Franco-English rivalry remains\n"
            + "- Iberian crowns are consolidating while Atlantic navigation accelerates\n"
            + "- Ming authority dominates East Asia as steppe powers contest the interior\n"
            + "- Regional beyliks, principalities, and sultanates create volatile frontiers\n"
            + "\n"
            + "Model your strategy around legitimacy, supply corridors, and defensible terrain.";
    }
}

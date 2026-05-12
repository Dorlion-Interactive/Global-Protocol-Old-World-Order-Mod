// GlobalProtocol: Old World Order — WASM Hook Exports
//
// This file only exports hook symbols expected by the game runtime.
// Mod logic itself lives in SDK-style classes (WasmModBase + WasmModRuntime).
//
// Build:
//   dotnet workload install wasi-experimental   (once per machine)
//   dotnet publish -c Release
//   → produces Content/mod.wasm

using System.Runtime.InteropServices;
using GlobalProtocol.ModWasmSdk;

namespace OldWorldOrder;

// Required by the .NET WASI linker. GlobalProtocol does not call _start.
internal static class WasiInit
{
    internal static void Run()
    {
        // Intentionally no-op: gameplay hooks must be entered by runtime callbacks only.
    }
}

internal static class Hooks
{
    [UnmanagedCallersOnly(EntryPoint = "on_init")]
    public static void OnInit() => WasmModRuntime.OnInit();

    [UnmanagedCallersOnly(EntryPoint = "on-init")]
    public static void OnInitKebab() => WasmModRuntime.OnInit();

    // Called every game tick.
    // tick  = total elapsed ticks, year/month = current in-game date.
    [UnmanagedCallersOnly(EntryPoint = "on_game_tick")]
    public static void OnGameTick(int tick, int year, int month) => WasmModRuntime.OnTick(tick, year, month);

    [UnmanagedCallersOnly(EntryPoint = "on-game-tick")]
    public static void OnGameTickKebab(int tick, int year, int month) => WasmModRuntime.OnTick(tick, year, month);

    // Called when a war is declared.
    // attacker / defender are country indices (0 = local player in single-player).
    [UnmanagedCallersOnly(EntryPoint = "on_war_declared")]
    public static void OnWarDeclared(int attacker, int defender, int tick) => WasmModRuntime.OnWarDeclared(attacker, defender, tick);

    [UnmanagedCallersOnly(EntryPoint = "on-war-declared")]
    public static void OnWarDeclaredKebab(int attacker, int defender, int tick) => WasmModRuntime.OnWarDeclared(attacker, defender, tick);

    // Called when peace is signed between two countries.
    [UnmanagedCallersOnly(EntryPoint = "on_peace_signed")]
    public static void OnPeaceSigned(int proposer, int target) => WasmModRuntime.OnPeaceSigned(proposer, target);

    [UnmanagedCallersOnly(EntryPoint = "on-peace-signed")]
    public static void OnPeaceSignedKebab(int proposer, int target) => WasmModRuntime.OnPeaceSigned(proposer, target);

    // Called when a country finishes researching a technology.
    [UnmanagedCallersOnly(EntryPoint = "on_tech_researched")]
    public static void OnTechResearched(int countryIndex, int techIndex) => WasmModRuntime.OnTechResearched(countryIndex, techIndex);

    [UnmanagedCallersOnly(EntryPoint = "on-tech-researched")]
    public static void OnTechResearchedKebab(int countryIndex, int techIndex) => WasmModRuntime.OnTechResearched(countryIndex, techIndex);

    // Called when a building finishes construction in a province.
    [UnmanagedCallersOnly(EntryPoint = "on_building_completed")]
    public static void OnBuildingCompleted(int provinceId, int buildingDefIndex) => WasmModRuntime.OnBuildingCompleted(provinceId, buildingDefIndex);

    [UnmanagedCallersOnly(EntryPoint = "on-building-completed")]
    public static void OnBuildingCompletedKebab(int provinceId, int buildingDefIndex) => WasmModRuntime.OnBuildingCompleted(provinceId, buildingDefIndex);

    // Called when any scripted event fires for any country.
    [UnmanagedCallersOnly(EntryPoint = "on_event_fired")]
    public static void OnEventFired(int countryIndex, int eventIndex) => WasmModRuntime.OnEventFired(countryIndex, eventIndex);

    [UnmanagedCallersOnly(EntryPoint = "on-event-fired")]
    public static void OnEventFiredKebab(int countryIndex, int eventIndex) => WasmModRuntime.OnEventFired(countryIndex, eventIndex);

    // Called when a country is fully eliminated from the game.
    [UnmanagedCallersOnly(EntryPoint = "on_country_eliminated")]
    public static void OnCountryEliminated(int countryIndex) => WasmModRuntime.OnCountryEliminated(countryIndex);

    [UnmanagedCallersOnly(EntryPoint = "on-country-eliminated")]
    public static void OnCountryEliminatedKebab(int countryIndex) => WasmModRuntime.OnCountryEliminated(countryIndex);

    // Called when a toolbar button (registered in mod.json entrypoints.ui) is clicked.
    // Always check modId first — other mods fire this hook too.
    [UnmanagedCallersOnly(EntryPoint = "on_ui_action")]
    public static void OnUiAction(
        int hookNamePtr, int hookNameLen,
        int modIdPtr, int modIdLen) => OnUiActionImpl(hookNamePtr, hookNameLen, modIdPtr, modIdLen);

    [UnmanagedCallersOnly(EntryPoint = "on-ui-action")]
    public static void OnUiActionKebab(
        int hookNamePtr, int hookNameLen,
        int modIdPtr, int modIdLen) => OnUiActionImpl(hookNamePtr, hookNameLen, modIdPtr, modIdLen);

    private static void OnUiActionImpl(int hookNamePtr, int hookNameLen, int modIdPtr, int modIdLen)
    {
        var hookName = Gp.DecodeString(hookNamePtr, hookNameLen);
        var modId = Gp.DecodeString(modIdPtr, modIdLen);
        WasmModRuntime.OnUiAction(hookName, modId);
    }
}

// GlobalProtocol: Old World Order — Mod-Hooks Component Export Implementation
//
// Implements IModHooksExports declared in the wit-bindgen generated bindings.
// The generated ModHooksExportsInterop class wraps each method below with
// [UnmanagedCallersOnly(EntryPoint = "globalprotocol:hooks/mod-hooks@1.0.0#...")]
// shims that wit-component lifts into proper component-level interface exports.

#nullable enable

using OldWorldOrder;

namespace GlobalprotocolModWorld.wit.Exports.globalprotocol.hooks.v1_0_0;

public partial class ModHooksExportsImpl : IModHooksExports
{
    public static void OnInit() => WasmModRuntime.OnInit();

    public static void OnGameTick(int tick, int year, int month)
        => WasmModRuntime.OnTick(tick, year, month);

    public static void OnUiAction(string hookName, string modId)
        => WasmModRuntime.OnUiAction(hookName, modId);

    public static void OnCountryEliminated(int countryIndex)
        => WasmModRuntime.OnCountryEliminated(countryIndex);

    public static void OnPeaceSigned(int proposerIndex, int targetIndex)
        => WasmModRuntime.OnPeaceSigned(proposerIndex, targetIndex);

    public static void OnWarDeclared(int attackerIndex, int defenderIndex, int tick)
        => WasmModRuntime.OnWarDeclared(attackerIndex, defenderIndex, tick);

    public static void OnTechResearched(int countryIndex, int techIndex)
        => WasmModRuntime.OnTechResearched(countryIndex, techIndex);

    public static void OnBuildingCompleted(int provinceIndex, int buildingIndex)
        => WasmModRuntime.OnBuildingCompleted(provinceIndex, buildingIndex);

    public static void OnEventFired(int countryIndex, int eventIndex)
        => WasmModRuntime.OnEventFired(countryIndex, eventIndex);
}

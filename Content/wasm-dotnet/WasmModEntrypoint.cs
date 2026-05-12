using GlobalProtocol.ModWasmSdk;

namespace OldWorldOrder;

internal static class WasmModRuntime
{
    private static readonly WasmModBase Entrypoint = new OldWorldOrderWasmMod();
    private static bool _initialized;

    private static void EnsureInitialized()
    {
        if (_initialized)
            return;

        Entrypoint.DispatchInitialize();
        _initialized = true;
    }

    internal static void OnInit()
    {
        EnsureInitialized();
    }

    internal static void OnTick(int tick, int year, int month)
    {
        EnsureInitialized();
        Entrypoint.DispatchTick(tick, year, month);
    }

    internal static void OnWarDeclared(int attacker, int defender, int tick)
    {
        EnsureInitialized();
        Entrypoint.DispatchWarDeclared(attacker, defender, tick);
    }

    internal static void OnPeaceSigned(int proposer, int target)
    {
        EnsureInitialized();
        Entrypoint.DispatchPeaceSigned(proposer, target);
    }

    internal static void OnTechResearched(int countryIndex, int techIndex)
    {
        EnsureInitialized();
        Entrypoint.DispatchTechResearched(countryIndex, techIndex);
    }

    internal static void OnBuildingCompleted(int provinceId, int buildingDefIndex)
    {
        EnsureInitialized();
        Entrypoint.DispatchBuildingCompleted(provinceId, buildingDefIndex);
    }

    internal static void OnEventFired(int countryIndex, int eventIndex)
    {
        EnsureInitialized();
        Entrypoint.DispatchEventFired(countryIndex, eventIndex);
    }

    internal static void OnCountryEliminated(int countryIndex)
    {
        EnsureInitialized();
        Entrypoint.DispatchCountryEliminated(countryIndex);
    }

    internal static void OnUiAction(string hookName, string modId)
    {
        EnsureInitialized();
        Entrypoint.DispatchUiAction(hookName, modId);
    }
}

// GlobalProtocol: Old World Order — Host Import Bridge
//
// Thin wrapper over the wit-bindgen generated GpImportsInterop. The generated
// stubs use [WasmImportLinkage] against module name
// "globalprotocol:hooks/gp@1.0.0", which the engine wires through
// WasmtimeComponentBackend.GpInstanceExportCandidates[0].

#nullable enable

using GlobalprotocolModWorld.wit.Imports.globalprotocol.hooks.v1_0_0;

namespace GlobalProtocol.ModWasmSdk;

public static class Gp
{
    public static int Year => IGpImports.GetYear();

    public static int Month => IGpImports.GetMonth();

    public static int Tick => IGpImports.GetTick();

    public static void Log(string msg) => IGpImports.Log(msg);

    public static void FireEvent(int countryIndex, string eventId)
        => IGpImports.FireEvent(countryIndex, eventId);

    public static void ShowPopup(string title, string body)
        => IGpImports.ShowModPopup(title, body);

    public static double CountryGetGdp(int countryIndex)
        => IGpImports.CountryGetGdp(countryIndex);

    public static double CountryGetTreasury(int countryIndex)
        => IGpImports.CountryGetTreasury(countryIndex);

    public static float CountryGetStability(int countryIndex)
        => IGpImports.CountryGetStability(countryIndex);

    public static int CountryGetTechLevel(int countryIndex)
        => IGpImports.CountryGetTechLevel(countryIndex);

    public static void CountrySetTreasury(int countryIndex, double value)
        => IGpImports.CountrySetTreasury(countryIndex, value);

    public static void AddTreasury(int countryIndex, float amount)
        => IGpImports.AddTreasury(countryIndex, amount);

    public static void FireTrigger(int triggerType, int source, int target)
        => IGpImports.FireTrigger(triggerType, source, target);

    /// <summary>
    /// Belt-and-suspenders: forces every host import to be statically
    /// referenced so neither the IL trimmer nor the linker can drop them.
    /// Always invoked from <c>OldWorldOrderWasmMod.OnInitialize</c> behind a
    /// guaranteed-false branch.
    /// </summary>
    public static void KeepHostImportLinks()
    {
        if (Environment.TickCount == int.MinValue)
        {
            IGpImports.Log(string.Empty);
            IGpImports.AddTreasury(0, 0f);
            IGpImports.FireTrigger(0, 0, 0);
            IGpImports.ShowModPopup(string.Empty, string.Empty);
            IGpImports.FireEvent(0, string.Empty);
            IGpImports.CountrySetTreasury(0, 0d);
            _ = IGpImports.CountryGetGdp(0);
            _ = IGpImports.CountryGetTreasury(0);
            _ = IGpImports.CountryGetStability(0);
            _ = IGpImports.CountryGetTechLevel(0);
            _ = IGpImports.GetTick();
            _ = IGpImports.GetYear();
            _ = IGpImports.GetMonth();
        }
    }
}

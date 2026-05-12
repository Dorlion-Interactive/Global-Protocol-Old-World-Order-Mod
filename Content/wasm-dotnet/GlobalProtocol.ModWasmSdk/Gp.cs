using System.Runtime.InteropServices;
using System.Text;

namespace GlobalProtocol.ModWasmSdk;

internal static class GpHost
{
    [DllImport("gp", EntryPoint = "log_string")]
    internal static extern void LogString(int msgPtr);

    [DllImport("gp", EntryPoint = "get_country_gdp")]
    internal static extern float GetCountryGdp(int countryIndex);

    [DllImport("gp", EntryPoint = "get_country_treasury")]
    internal static extern float GetCountryTreasury(int countryIndex);

    [DllImport("gp", EntryPoint = "get_country_stability")]
    internal static extern float GetCountryStability(int countryIndex);

    [DllImport("gp", EntryPoint = "get_country_manpower")]
    internal static extern int GetCountryManpower(int countryIndex);

    [DllImport("gp", EntryPoint = "get_current_tick")]
    internal static extern int GetCurrentTick();

    [DllImport("gp", EntryPoint = "get_current_year")]
    internal static extern int GetCurrentYear();

    [DllImport("gp", EntryPoint = "get_current_month")]
    internal static extern int GetCurrentMonth();

    [DllImport("gp", EntryPoint = "add_treasury")]
    internal static extern void AddTreasury(int countryIndex, float amount);

    [DllImport("gp", EntryPoint = "fire_trigger")]
    internal static extern void FireTrigger(int countryIndex, int triggerId, int targetIndex);

    [DllImport("gp", EntryPoint = "log")]
    internal static extern void Log(int msgPtr, int msgLen);

    [DllImport("gp", EntryPoint = "get_tick")]
    internal static extern int GetTick();

    [DllImport("gp", EntryPoint = "get_year")]
    internal static extern int GetYear();

    [DllImport("gp", EntryPoint = "get_month")]
    internal static extern int GetMonth();

    [DllImport("gp", EntryPoint = "country_get_gdp")]
    internal static extern double CountryGetGdp(int countryIndex);

    [DllImport("gp", EntryPoint = "country_get_stability")]
    internal static extern float CountryGetStability(int countryIndex);

    [DllImport("gp", EntryPoint = "country_get_treasury")]
    internal static extern double CountryGetTreasury(int countryIndex);

    [DllImport("gp", EntryPoint = "country_set_treasury")]
    internal static extern void CountrySetTreasury(int countryIndex, double amount);

    [DllImport("gp", EntryPoint = "country_get_tech_level")]
    internal static extern int CountryGetTechLevel(int countryIndex);

    [DllImport("gp", EntryPoint = "show_mod_popup")]
    internal static extern void ShowModPopup(int titlePtr, int titleLen, int bodyPtr, int bodyLen);

    [DllImport("gp", EntryPoint = "show-mod-popup")]
    internal static extern void ShowModPopupKebab(int titlePtr, int titleLen, int bodyPtr, int bodyLen);

    [DllImport("gp", EntryPoint = "fire_event")]
    internal static extern void FireEvent(int countryIndex, int eventIdPtr, int eventIdLen);
}

public static class Gp
{
    public static int Year => GpHost.GetYear();

    public static int Month => GpHost.GetMonth();

    public static void Log(string msg)
        => WriteUtf8(msg, (ptr, len) => GpHost.Log(ptr, len));

    public static void FireEvent(int countryIndex, string eventId)
        => WriteUtf8(eventId, (ptr, len) => GpHost.FireEvent(countryIndex, ptr, len));

    public static void ShowPopup(string title, string body)
        => WriteTwoUtf8(title, body, (titlePtr, titleLen, bodyPtr, bodyLen) =>
            GpHost.ShowModPopupKebab(titlePtr, titleLen, bodyPtr, bodyLen));

    public static unsafe string DecodeString(int ptr, int len)
    {
        if (len <= 0) return string.Empty;
        return Encoding.UTF8.GetString((byte*)ptr, len);
    }

    public static void KeepHostImportLinks()
    {
        if (Environment.TickCount == int.MinValue)
        {
            GpHost.LogString(0);
            GpHost.AddTreasury(0, 0.0f);
            GpHost.FireTrigger(0, 0, 0);
            GpHost.Log(0, 0);
            GpHost.ShowModPopup(0, 0, 0, 0);
            GpHost.ShowModPopupKebab(0, 0, 0, 0);
            GpHost.FireEvent(0, 0, 0);
            GpHost.CountrySetTreasury(0, 0.0);

            _ = GpHost.GetCountryGdp(0);
            _ = GpHost.GetCountryTreasury(0);
            _ = GpHost.GetCountryStability(0);
            _ = GpHost.GetCountryManpower(0);
            _ = GpHost.GetCurrentTick();
            _ = GpHost.GetCurrentYear();
            _ = GpHost.GetCurrentMonth();
            _ = GpHost.GetTick();
            _ = GpHost.GetYear();
            _ = GpHost.GetMonth();
            _ = GpHost.CountryGetGdp(0);
            _ = GpHost.CountryGetStability(0);
            _ = GpHost.CountryGetTreasury(0);
            _ = GpHost.CountryGetTechLevel(0);
        }
    }

    private static unsafe void WriteUtf8(string value, Action<int, int> call)
    {
        var bytes = Encoding.UTF8.GetBytes(value);
        fixed (byte* ptr = bytes)
            call((int)ptr, bytes.Length);
    }

    private static unsafe void WriteTwoUtf8(string first, string second, Action<int, int, int, int> call)
    {
        var firstBytes = Encoding.UTF8.GetBytes(first);
        var secondBytes = Encoding.UTF8.GetBytes(second);

        fixed (byte* firstPtr = firstBytes)
        fixed (byte* secondPtr = secondBytes)
            call((int)firstPtr, firstBytes.Length, (int)secondPtr, secondBytes.Length);
    }
}
// GlobalProtocol WASM helper — wraps all low-level host interop.
// Use Gp.* in your Hooks methods instead of touching GpHost directly.
// GpHost is the raw [DllImport] layer; you should not need to touch it.

using System.Runtime.InteropServices;
using System.Text;

namespace OldWorldOrder;

// ─── Raw host imports (do not call these directly) ────────────────────────────

internal static class GpHost
{
    [DllImport("gp", EntryPoint = "log")]
    internal static extern void Log(int msgPtr, int msgLen);

    [DllImport("gp", EntryPoint = "fire_event")]
    internal static extern void FireEvent(int countryIndex, int eventIdPtr, int eventIdLen);

    [DllImport("gp", EntryPoint = "get_year")]
    internal static extern int GetYear();
}

// ─── High-level helper (use this in Hooks.cs) ─────────────────────────────────

/// <summary>
/// Friendly wrappers for all engine host calls.
/// Handles UTF-8 encoding/decoding so your hook code stays readable.
/// </summary>
internal static class Gp
{
    /// <summary>Current in-game year.</summary>
    internal static int Year => GpHost.GetYear();

    /// <summary>Write a message to the Unity console (debug builds; no-op in release).</summary>
    internal static void Log(string msg)
        => WriteUtf8(msg, (ptr, len) => GpHost.Log(ptr, len));

    /// <summary>
    /// Fire a scripted event for a country.
    /// countryIndex 0 = local player in single-player.
    /// Requires "FireTriggers" permission in mod.json.
    /// </summary>
    internal static void FireEvent(int countryIndex, string eventId)
        => WriteUtf8(eventId, (ptr, len) => GpHost.FireEvent(countryIndex, ptr, len));

    /// <summary>
    /// Decode a UTF-8 string passed in from the engine (ptr + len into WASM linear memory).
    /// Use this in [UnmanagedCallersOnly] hooks to read hookName, modId, etc.
    /// </summary>
    internal static unsafe string DecodeString(int ptr, int len)
    {
        if (len <= 0) return string.Empty;
        return Encoding.UTF8.GetString((byte*)ptr, len);
    }

    // ─── Plumbing — nothing below here needs to change ────────────────────────

    private static unsafe void WriteUtf8(string value, Action<int, int> call)
    {
        var bytes = Encoding.UTF8.GetBytes(value);
        fixed (byte* ptr = bytes)
            call((int)ptr, bytes.Length);
    }
}

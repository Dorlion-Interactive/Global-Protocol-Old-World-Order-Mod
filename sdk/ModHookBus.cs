// GlobalProtocol Mod SDK — ModHookBus stub
// In a shipping game build this class is in GlobalProtocol.Core.dll.
// This stub provides IntelliSense and build-time resolution only.
// The real static events are wired up by the engine at runtime.

using System;

namespace GlobalProtocol.Core.Mods
{
    /// <summary>
    /// Central event bus for mod hooks. Subscribe in <see cref="IModEntrypoint.Initialize"/>
    /// and unsubscribe in <see cref="IModEntrypoint.Dispose"/>.
    ///
    /// All delegates are fired on the main thread.
    /// </summary>
    public static class ModHookBus
    {
        // ─── Outbound events (game → mod) ──────────────────────────────────────

        /// <summary>Fired each game tick. Parameters: tick, year, month.</summary>
        public static event Action<int, int, int>? OnGameTick;

        /// <summary>Fired when a war is declared. Parameters: attackerCountryIndex, defenderCountryIndex, tick.</summary>
        public static event Action<int, int, int>? OnWarDeclared;

        /// <summary>Fired when peace is signed. Parameters: proposerCountryIndex, targetCountryIndex.</summary>
        public static event Action<int, int>? OnPeaceSigned;

        /// <summary>Fired when a technology is researched. Parameters: countryIndex, techIndex.</summary>
        public static event Action<int, int>? OnTechResearched;

        /// <summary>Fired when a building is completed. Parameters: provinceId, buildingDefIndex.</summary>
        public static event Action<int, int>? OnBuildingCompleted;

        /// <summary>Fired when a scripted or reactive event fires for any country. Parameters: countryIndex, eventIndex.</summary>
        public static event Action<int, int>? OnEventFired;

        /// <summary>Fired when a country is eliminated. Parameters: countryIndex.</summary>
        public static event Action<int>? OnCountryEliminated;

        /// <summary>Fired when a mod UI button is clicked. Parameters: hookName, modId.</summary>
        public static event Action<string, string>? OnUiAction;

        // ─── Inbound calls (mod → game) ────────────────────────────────────────

        /// <summary>
        /// Fires a scripted event for the specified country.
        /// Requires <c>"FireTriggers"</c> permission in <c>mod.json</c>.
        /// <para>
        /// The event must be defined in the engine's baked EventConfigBlob (imported
        /// via the EventConfigImporterWindow editor tool). Mod JSON event files are not
        /// supported — this is a compile-time-only stub.
        /// </para>
        /// </summary>
        public static void FireEvent(int countryIndex, string eventId)
        {
            // Stub — implemented by the game runtime.
        }

        // ─── Internal — do not call from mod code ──────────────────────────────

        internal static void Clear() { /* runtime stub */ }
    }
}

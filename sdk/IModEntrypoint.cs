// GlobalProtocol Mod SDK — IModEntrypoint and IModServices stubs
// In a shipping game build these interfaces are in GlobalProtocol.Core.dll.
// This file exists so mods can compile and get IntelliSense without a game install.

namespace GlobalProtocol.Core.Mods
{
    /// <summary>
    /// Implement this interface on a public class in your mod assembly.
    /// The engine discovers it via reflection when loading the mod's DLL.
    /// Your class must have a public parameterless constructor.
    /// </summary>
    public interface IModEntrypoint
    {
        /// <summary>
        /// Called once when the mod is loaded. Subscribe to <see cref="ModHookBus"/> events here.
        /// Do not hold a long-lived reference to <paramref name="services"/> — its scope is this call.
        /// </summary>
        void Initialize(IModServices services);

        /// <summary>
        /// Called once when the mod is unloaded (game exit or mod disable).
        /// Unsubscribe from <see cref="ModHookBus"/> events here to avoid memory leaks.
        /// </summary>
        void Dispose();
    }

    /// <summary>
    /// Engine services injected into <see cref="IModEntrypoint.Initialize"/>.
    /// Use to access engine services during initialization.
    /// </summary>
    public interface IModServices
    {
        // Reserved for future service injection (logging, config, asset loading).
        // Check the MODDING_REFERENCE.md for what is available in each engine version.
    }
}

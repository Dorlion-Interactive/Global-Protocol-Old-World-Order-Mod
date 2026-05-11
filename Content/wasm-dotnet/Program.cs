// Required entry point for the .NET WASI runtime.
// The host calls on_game_tick and on_ui_action directly via WASM exports.
// Main() is only invoked if the host calls the _start WASI export,
// which GlobalProtocol does not use — but the .NET runtime linker requires it.
namespace OldWorldOrder;
internal static class Program
{
    internal static void Main() => WasiInit.Run();
}

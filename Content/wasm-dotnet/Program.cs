// Required entry point for the .NET WASI runtime.
// The host runtime dispatches lifecycle hooks; for core-WASM this is via direct exports,
// and for component-WASM this is via the hook world contract.
// Main() is only invoked if the host calls the _start WASI export,
// which GlobalProtocol does not use — but the .NET runtime linker requires it.
namespace OldWorldOrder;
internal static class Program
{
    internal static void Main() => WasiInit.Run();
}

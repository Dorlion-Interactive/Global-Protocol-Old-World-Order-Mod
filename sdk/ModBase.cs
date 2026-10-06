// GlobalProtocol Mod SDK — ModBase
// Convenience base class for Variant C (native C# delegate) mods.
// Extend this instead of IModEntrypoint directly.
// Override only the hooks you need — all others are no-ops by default.

namespace GlobalProtocol.Core.Mods;

/// <summary>
/// Base class for C# delegate mods. Handles event subscribe/unsubscribe
/// automatically so you never have to touch Initialize or Dispose.
///
/// Minimal mod example:
/// <code>
/// public sealed class MyMod : ModBase
/// {
///     protected override void OnTick(int tick, int year, int month)
///     {
///         // runs every game tick
///     }
/// }
/// </code>
/// </summary>
public abstract class ModBase : IModEntrypoint
{
    // Called by the engine — do not override. Use OnInitialize instead.
    public void Initialize(IModServices services)
    {
        ModHookBus.OnGameTick          += OnTick;
        ModHookBus.OnWarDeclared       += OnWarDeclared;
        ModHookBus.OnPeaceSigned       += OnPeaceSigned;
        ModHookBus.OnTechResearched    += OnTechResearched;
        ModHookBus.OnBuildingCompleted += OnBuildingCompleted;
        ModHookBus.OnEventFired        += OnEventFired;
        ModHookBus.OnCountryEliminated += OnCountryEliminated;
        ModHookBus.OnUiAction          += OnUiAction;
        ModHookBus.OnProvinceCaptured      += OnProvinceCaptured;
        ModHookBus.OnAllianceFormed        += OnAllianceFormed;
        ModHookBus.OnAllianceBroken        += OnAllianceBroken;
        ModHookBus.OnEconomyTick           += OnEconomyTick;
        ModHookBus.OnTradeAgreementSigned  += OnTradeAgreementSigned;
        OnInitialize(services);
    }

    // Called by the engine — do not override. Use OnDispose instead.
    public void Dispose()
    {
        ModHookBus.OnGameTick              -= OnTick;
        ModHookBus.OnWarDeclared           -= OnWarDeclared;
        ModHookBus.OnPeaceSigned           -= OnPeaceSigned;
        ModHookBus.OnTechResearched        -= OnTechResearched;
        ModHookBus.OnBuildingCompleted     -= OnBuildingCompleted;
        ModHookBus.OnEventFired            -= OnEventFired;
        ModHookBus.OnCountryEliminated     -= OnCountryEliminated;
        ModHookBus.OnUiAction              -= OnUiAction;
        ModHookBus.OnProvinceCaptured      -= OnProvinceCaptured;
        ModHookBus.OnAllianceFormed        -= OnAllianceFormed;
        ModHookBus.OnAllianceBroken        -= OnAllianceBroken;
        ModHookBus.OnEconomyTick           -= OnEconomyTick;
        ModHookBus.OnTradeAgreementSigned  -= OnTradeAgreementSigned;
        OnDispose();
    }

    // ─── Override these in your mod ───────────────────────────────────────────

    /// <summary>Called after all hooks are subscribed. Use for one-time setup.</summary>
    protected virtual void OnInitialize(IModServices services) { }

    /// <summary>Called before hooks are unsubscribed. Use for cleanup.</summary>
    protected virtual void OnDispose() { }

    /// <summary>Called each game tick.</summary>
    protected virtual void OnTick(int tick, int year, int month) { }

    /// <summary>Called when a war is declared between two countries.</summary>
    protected virtual void OnWarDeclared(int attacker, int defender, int tick) { }

    /// <summary>Called when peace is signed between two countries.</summary>
    protected virtual void OnPeaceSigned(int proposer, int target) { }

    /// <summary>Called when a technology is researched. techIndex is the engine-side tech definition index.</summary>
    protected virtual void OnTechResearched(int countryIndex, int techIndex) { }

    /// <summary>Called when a building finishes construction. buildingDefIndex is the engine-side building type.</summary>
    protected virtual void OnBuildingCompleted(int provinceId, int buildingDefIndex) { }

    /// <summary>Called when a scripted event fires for any country. eventIndex is the event definition index.</summary>
    protected virtual void OnEventFired(int countryIndex, int eventIndex) { }

    /// <summary>Called when a country is fully eliminated from the game.</summary>
    protected virtual void OnCountryEliminated(int countryIndex) { }

    /// <summary>Fired once per province whose owner changes through a peace deal or annexation effect.</summary>
    protected virtual void OnProvinceCaptured(int provinceId, int newOwner, int oldOwner) { }

    /// <summary>Fired when two countries form an alliance.</summary>
    protected virtual void OnAllianceFormed(int proposerIndex, int partnerIndex) { }

    /// <summary>Fired when an alliance is dissolved.</summary>
    protected virtual void OnAllianceBroken(int breakerIndex, int partnerIndex) { }

    /// <summary>Fired each monthly economy tick.</summary>
    protected virtual void OnEconomyTick(int year, int month) { }

    /// <summary>Fired when a bilateral trade agreement is signed.</summary>
    protected virtual void OnTradeAgreementSigned(int country1Index, int country2Index) { }

    /// <summary>
    /// Called when a mod UI button is clicked.
    /// hookName is the hook ID you registered in mod.json.
    /// modId lets you filter for your own mod's buttons.
    /// </summary>
    protected virtual void OnUiAction(string hookName, string modId) { }
}

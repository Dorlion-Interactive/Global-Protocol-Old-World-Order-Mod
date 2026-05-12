namespace GlobalProtocol.ModWasmSdk;

public abstract class WasmModBase
{
    protected virtual void OnInitialize()
    {
    }

    protected virtual void OnTick(int tick, int year, int month)
    {
    }

    protected virtual void OnWarDeclared(int attacker, int defender, int tick)
    {
    }

    protected virtual void OnPeaceSigned(int proposer, int target)
    {
    }

    protected virtual void OnTechResearched(int countryIndex, int techIndex)
    {
    }

    protected virtual void OnBuildingCompleted(int provinceId, int buildingDefIndex)
    {
    }

    protected virtual void OnEventFired(int countryIndex, int eventIndex)
    {
    }

    protected virtual void OnCountryEliminated(int countryIndex)
    {
    }

    protected virtual void OnUiAction(string hookName, string modId)
    {
    }

    public void DispatchInitialize() => OnInitialize();
    public void DispatchTick(int tick, int year, int month) => OnTick(tick, year, month);
    public void DispatchWarDeclared(int attacker, int defender, int tick) => OnWarDeclared(attacker, defender, tick);
    public void DispatchPeaceSigned(int proposer, int target) => OnPeaceSigned(proposer, target);
    public void DispatchTechResearched(int countryIndex, int techIndex) => OnTechResearched(countryIndex, techIndex);
    public void DispatchBuildingCompleted(int provinceId, int buildingDefIndex) => OnBuildingCompleted(provinceId, buildingDefIndex);
    public void DispatchEventFired(int countryIndex, int eventIndex) => OnEventFired(countryIndex, eventIndex);
    public void DispatchCountryEliminated(int countryIndex) => OnCountryEliminated(countryIndex);
    public void DispatchUiAction(string hookName, string modId) => OnUiAction(hookName, modId);
}
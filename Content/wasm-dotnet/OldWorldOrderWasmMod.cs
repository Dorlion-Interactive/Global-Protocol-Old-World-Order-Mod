using GlobalProtocol.ModWasmSdk;

namespace OldWorldOrder;

internal sealed class OldWorldOrderWasmMod : WasmModBase
{
    private const string ModId = "globalprotocol.old_world_order";
    private const string WelcomeHookName = "owo.welcome";
    private const string StartupTitle = "Old World Order, 1450";
    private const string ToolbarTitle = "Strategic Briefing";

    private int _warsObserved;
    private int _techsObserved;
    private int _buildingsObserved;
    private int _eventsObserved;
    private int _lastYear;
    private int _lastMonth;
    private bool _startupShown;

    protected override void OnInitialize()
    {
        Gp.KeepHostImportLinks();

        _warsObserved = 0;
        _techsObserved = 0;
        _buildingsObserved = 0;
        _eventsObserved = 0;
        _lastYear = 0;
        _lastMonth = 0;
        _startupShown = false;

        Gp.Log("OWO init (.NET WASM SDK hooks)");
    }

    protected override void OnTick(int tick, int year, int month)
    {
        _lastYear = year;
        _lastMonth = month;

        if (_startupShown)
            return;

        _startupShown = true;
        ShowStartupBriefing(year, month);
    }

    protected override void OnWarDeclared(int attacker, int defender, int tick)
    {
        _warsObserved++;
    }

    protected override void OnTechResearched(int countryIndex, int techIndex)
    {
        _techsObserved++;
    }

    protected override void OnBuildingCompleted(int provinceId, int buildingDefIndex)
    {
        _buildingsObserved++;
    }

    protected override void OnEventFired(int countryIndex, int eventIndex)
    {
        _eventsObserved++;
    }

    protected override void OnUiAction(string hookName, string modId)
    {
        if (modId != ModId)
            return;

        if (hookName != WelcomeHookName)
            return;

        Gp.ShowPopup(ToolbarTitle, BuildToolbarBody());
        Gp.Log("OWO: toolbar popup shown via on_ui_action (.NET WASM SDK hooks)");
    }

    private void ShowStartupBriefing(int year, int month)
    {
        string monthText = month >= 1 && month <= 12 ? month.ToString("00") : "--";
        string dateLine = year > 0
            ? $"Date: {year}-{monthText}\n"
            : "Date: unknown\n";

        string body = dateLine
            + "\n"
            + "Europe and Asia stand between old feudal orders and rising centralized states.\n"
            + "Trade routes across the Mediterranean, Black Sea, Indian Ocean, and Silk Road are the arteries of power.\n"
            + "Gunpowder armies are emerging, but cavalry, levies, and fortresses still decide most wars.\n"
            + "\n"
            + "Use the crown button in the toolbar to reopen this briefing at any time.";

        Gp.ShowPopup(StartupTitle, body);
        Gp.Log("OWO: startup popup shown via on_game_tick (.NET WASM SDK hooks)");
    }

    private string BuildToolbarBody()
    {
        return "1450 Intelligence Report\n"
            + "\n"
            + $"Observed wars: {_warsObserved}\n"
            + $"Observed technologies: {_techsObserved}\n"
            + $"Observed building completions: {_buildingsObserved}\n"
            + $"Observed scripted events: {_eventsObserved}\n"
            + "\n"
            + $"Current date snapshot: {FormatDate(_lastYear, _lastMonth)}\n"
            + "\n"
            + "Model your strategy around legitimacy, supply corridors, and defensible terrain.";
    }

    private static string FormatDate(int year, int month)
    {
        if (year <= 0)
            return "unknown";

        string monthText = month >= 1 && month <= 12 ? month.ToString("00") : "--";
        return $"{year}-{monthText}";
    }
}

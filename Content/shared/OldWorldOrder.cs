using System;
using System.IO;
using System.Text.RegularExpressions;

namespace GlobalProtocol.Mods.OldWorldOrder;

/// <summary>
/// Host abstraction interface implemented by SDK and WASM.NET entrypoints.
/// Allows shared game logic to trigger UI popups, logging, and read metadata
/// without being coupled to a specific engine integration path.
/// </summary>
public interface IModHost
{
    void ShowPopup(string title, string body);
    void Log(string message);
    string GetModVersion();
}

/// <summary>
/// Shared mod logic and state tracking class.
/// Both SDK and WASM.NET delegate their lifecycle hooks to this instance.
/// </summary>
public sealed class OldWorldOrder
{
    public const string ModId = "globalprotocol.old_world_order";
    public const string WelcomeHook = "owo.welcome";
    public const string ArchiveHook = "owo.archive";
    public const string InfoHook = "owo.info";

    private readonly IModHost _host;
    private int _warsObserved;
    private int _techsObserved;
    private int _buildingsObserved;
    private int _eventsObserved;
    private int _lastYear;
    private int _lastMonth;
    private bool _startupShown;

    public OldWorldOrder(IModHost host)
    {
        _host = host;
    }

    public void OnInitialize()
    {
        _warsObserved = 0;
        _techsObserved = 0;
        _buildingsObserved = 0;
        _eventsObserved = 0;
        _lastYear = 0;
        _lastMonth = 0;
        _startupShown = false;
        _host.Log("OWO initialized shared logic.");
    }

    public void OnTick(int tick, int year, int month)
    {
        _lastYear = year;
        _lastMonth = month;

        if (_startupShown)
            return;

        _startupShown = true;
        _host.ShowPopup("Strategic Briefing: 1450 AD", BuildBriefingBody(year, month));
        _host.Log("OWO: startup popup shown via OnTick");
    }

    public void OnWarDeclared(int attacker, int defender, int tick)
    {
        _warsObserved++;
    }

    public void OnPeaceSigned(int proposer, int target)
    {
        // Showcase hook: triggered when peace is signed between two countries
    }

    public void OnTechResearched(int countryIndex, int techIndex)
    {
        _techsObserved++;
    }

    public void OnBuildingCompleted(int provinceId, int buildingDefIndex)
    {
        _buildingsObserved++;
    }

    public void OnEventFired(int countryIndex, int eventIndex)
    {
        _eventsObserved++;
    }

    public void OnCountryEliminated(int countryIndex)
    {
        // Showcase hook: triggered when a country is fully eliminated from the game
    }

    public void OnUiAction(string hookName, string modId)
    {
        if (modId != ModId)
            return;

        switch (hookName)
        {
            case WelcomeHook:
                _host.ShowPopup("Strategic Briefing: 1450 AD", BuildBriefingBody(_lastYear, _lastMonth));
                _host.Log("OWO: welcome popup shown via UI action");
                break;

            case ArchiveHook:
                _host.ShowPopup("Historian's Archive", BuildArchiveBody());
                _host.Log("OWO: archive popup shown via UI action");
                break;

            case InfoHook:
                _host.ShowPopup("Mod Information", BuildInfoBody());
                _host.Log("OWO: info popup shown via UI action");
                break;
        }
    }

    private string BuildBriefingBody(int year, int month)
    {
        string monthText = (month >= 1 && month <= 12) ? month.ToString("00") : "--";
        return "Date: " + year + "-" + monthText + "\n\n"
             + "Europe and Asia stand between old feudal orders and rising centralized states.\n"
             + "Trade routes across the Mediterranean, Black Sea, Indian Ocean, and Silk Road are the arteries of power.\n"
             + "Gunpowder armies are emerging, but cavalry, levies, and fortresses still decide most wars.\n\n"
             + "Use the buttons in the toolbar to access reports and mod information.";
    }

    private string BuildArchiveBody()
    {
        return "1450 Intelligence Report\n\n"
             + "Observed wars: " + _warsObserved + "\n"
             + "Observed technologies: " + _techsObserved + "\n"
             + "Observed building completions: " + _buildingsObserved + "\n"
             + "Observed scripted events: " + _eventsObserved + "\n\n"
             + "Model your strategy around legitimacy, supply corridors, and defensible terrain.";
    }

    private string BuildInfoBody()
    {
        string version = _host.GetModVersion();
        return "Global Protocol: Old World Order\n"
             + "Version: " + version + "\n\n"
             + "A historical scenario mod focusing on the late medieval era.\n"
             + "Showcasing UI injection across SDK, WASM.NET, and AS paths.\n\n"
             + "Project: Dorlion-Interactive/Global-Protocol-Old-World-Order-Mod";
    }
}

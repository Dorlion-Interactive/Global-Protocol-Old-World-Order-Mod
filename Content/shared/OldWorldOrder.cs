using System;
using System.IO;

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
    private int _alliancesObserved;
    private int _alliancesBroken;
    private int _tradeAgreementsObserved;
    private int _provincesCaptured;
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
        _alliancesObserved = 0;
        _alliancesBroken = 0;
        _tradeAgreementsObserved = 0;
        _provincesCaptured = 0;
        _techsObserved = 0;
        _buildingsObserved = 0;
        _eventsObserved = 0;
        _lastYear = 0;
        _lastMonth = 0;
        _startupShown = false;
        _host.Log("OWO initialized shared logic with ABI 3 diplomacy hooks.");
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

    public void OnAllianceFormed(int proposerIndex, int partnerIndex)
    {
        _alliancesObserved++;
        _host.Log($"OWO: Alliance formed between #{proposerIndex} and #{partnerIndex}");
    }

    public void OnAllianceBroken(int breakerIndex, int partnerIndex)
    {
        _alliancesBroken++;
        _host.Log($"OWO: Alliance dissolved between #{breakerIndex} and #{partnerIndex}");
    }

    public void OnTradeAgreementSigned(int country1Index, int country2Index)
    {
        _tradeAgreementsObserved++;
        _host.Log($"OWO: Trade agreement concluded between #{country1Index} and #{country2Index}");
    }

    public void OnProvinceCaptured(int provinceId, int newOwner, int oldOwner)
    {
        _provincesCaptured++;
        _host.Log($"OWO: Province #{provinceId} transferred from #{oldOwner} to #{newOwner}");
    }

    public void OnEconomyTick(int year, int month)
    {
        _lastYear = year;
        _lastMonth = month;
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
        return "Era: 1450 AD (Current Date: " + year + "-" + monthText + ")\n\n"
             + "THE 1450 DIPLOMATIC WEB:\n"
             + "• The Jagiellonian Union: Poland (POL) and Lithuania (LTH) united under Casimir IV against the Teutonic Order.\n"
             + "• The Auld Alliance: France (FRA) and Scotland (SCT) press the English crown (ENG) in the final stage of the Hundred Years' War.\n"
             + "• The Balkan Bastion: Hungary (HUN), Skanderbeg's Albania (LEZ), and the Papacy (PAP) confront Ottoman expansion (OTT).\n"
             + "• Italian Pentarchy: Maritime rivalry divides Venice (VNC) and Genoa (GEN); Milan (MIL) and Florence (FLR) hold the balance.\n"
             + "• The Iberian Concord: Castile (CAS), Aragon (ARA), and Portugal (PRT) maintain fragile peace on the Granada (GRN) frontier.\n"
             + "• Eastern Pacts: Ming China (MYN) rebuilds after Tumu with Joseon (JOS) tributary support; Vijayanagara (VIJ) contests the Deccan.\n\n"
             + "Use the toolbar buttons to inspect intelligence, military chronicles, and mod status.";
    }

    private string BuildArchiveBody()
    {
        return "1450 Geopolitical & Intelligence Ledger\n\n"
             + "Observed wars declared: " + _warsObserved + "\n"
             + "Observed alliances formed: " + _alliancesObserved + "\n"
             + "Observed alliances dissolved: " + _alliancesBroken + "\n"
             + "Observed trade pacts: " + _tradeAgreementsObserved + "\n"
             + "Observed territorial conquests: " + _provincesCaptured + "\n"
             + "Observed doctrines researched: " + _techsObserved + "\n"
             + "Observed building projects: " + _buildingsObserved + "\n"
             + "Observed scripted events: " + _eventsObserved + "\n\n"
             + "Maintain dynastic legitimacy, secure trade choke points, and honor defensive pacts.";
    }

    private string BuildInfoBody()
    {
        string version = _host.GetModVersion();
        return "Global Protocol: Old World Order\n"
             + "Version: " + version + "\n\n"
             + "A historical scenario mod focusing on the late medieval and early Renaissance era (1450 AD).\n"
             + "Features deep diplomatic networks, cultural affinities, dynamic events, and Knowledge Network doctrines.\n\n"
             + "Project: Dorlion-Interactive/Global-Protocol-Old-World-Order-Mod";
    }
}

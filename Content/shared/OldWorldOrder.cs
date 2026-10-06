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
    public const string ChronicleHook = "owo.chronicle";
    public const string BalanceOfPowerHook = "owo.balance_of_power";
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
    private bool _constantinopleFallen;
    private readonly System.Collections.Generic.Dictionary<int, int> _warAggressors = new();

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
        _constantinopleFallen = false;
        _warAggressors.Clear();
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
        int count = _warAggressors.TryGetValue(attacker, out int existing) ? existing + 1 : 1;
        _warAggressors[attacker] = count;

        if (count >= 3)
        {
            _host.Log($"OWO: Grand Coalition Alert: Nation #{attacker} has initiated {count} aggressive wars!");
        }
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

        // Province 2276 = Constantinople (Istanbul)
        if (provinceId == 2276 && !_constantinopleFallen)
        {
            _constantinopleFallen = true;
            _host.ShowPopup(
                "Geopolitical Shock: Fall of Constantinople",
                "With the fall of Constantinople, the Ottoman Empire secures uncontested mastery over the Bosporus straits.\n\n"
              + "The traditional Silk Road and Levantine spice trade corridors face heavy imperial tariffs and blockades, "
              + "compelling Western European crowns to accelerate oceanic navigation around Africa and across the Atlantic."
            );
            _host.Log("OWO: Constantinople captured! Spice trade disruption bulletin dispatched.");
        }
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

            case ChronicleHook:
                _host.ShowPopup("1450 World Chronicle", BuildChronicleBody());
                _host.Log("OWO: chronicle popup shown via UI action");
                break;

            case BalanceOfPowerHook:
                _host.ShowPopup("Balance of Power & Alliances", BuildBalanceOfPowerBody());
                _host.Log("OWO: balance of power popup shown via UI action");
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

    private string BuildChronicleBody()
    {
        string spiceStatus = _constantinopleFallen
            ? "SEVERED — Constantinople in Ottoman hands; oceanic trade imperative active."
            : "OPEN — Byzantine Bosporus intact; Venetian-Mamluk Alexandria spice route flowing.";

        return "1450 WORLD CHRONICLE\n\n"
             + "• Year of Epoch: 1450 AD\n"
             + "• Levantine Spice Route Status: " + spiceStatus + "\n"
             + "• Continental Campaigns Recorded: " + _warsObserved + "\n"
             + "• Diplomatic Alliances Formed: " + _alliancesObserved + "\n"
             + "• Treaties Dissolved / Broken: " + _alliancesBroken + "\n"
             + "• Commercial Trade Agreements: " + _tradeAgreementsObserved + "\n"
             + "• Provinces Changed Sovereignty: " + _provincesCaptured + "\n\n"
             + "The world transitions from medieval chivalric levies into early modern sovereign states.";
    }

    private string BuildBalanceOfPowerBody()
    {
        return "BALANCE OF POWER & ALLIANCE NETWORKS (1450)\n\n"
             + "1. Western Christendom:\n"
             + "   • Kingdom of France (FRA) & Kingdom of Scotland (SCT) — The Auld Alliance\n"
             + "   • Kingdom of England (ENG) & Duchy of Burgundy (BUR) — Anglo-Burgundian ties\n"
             + "   • Crown of Castile (CAS) & Crown of Aragon (ARA) — Trastámara dynastic accord\n\n"
             + "2. Central & Eastern Europe:\n"
             + "   • Crown of Poland (POL) & Grand Duchy of Lithuania (LTH) — Jagiellonian Union\n"
             + "   • Crown of Hungary (HUN) & League of Lezhë (LEZ) — Anti-Ottoman Danubian front\n"
             + "   • Grand Duchy of Moscow (MVY) & Pskov (PSK) — Defense against the Great Horde (STE)\n\n"
             + "3. Eastern Empires:\n"
             + "   • Ming Dynasty (MYN) & Joseon Dynasty (JOS) — Confucian Tributary Pact\n"
             + "   • Vijayanagara Empire (VIJ) vs. Bahmani Sultanate (BAH) — Deccan balance of power\n\n"
             + "4. Maritime Republics:\n"
             + "   • Republic of Venice (VNC) vs. Republic of Genoa (GEN) — Mediterranean trade rivalry";
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

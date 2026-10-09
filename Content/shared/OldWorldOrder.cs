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
    public const string AmbitionsHook = "owo.ambitions";
    public const string ArchiveHook = "owo.archive";
    public const string ChronicleHook = "owo.chronicle";
    public const string BalanceOfPowerHook = "owo.balance_of_power";
    public const string DynastiesHook = "owo.dynasties";
    public const string FaithsHook = "owo.faiths";
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
    private int _countriesEliminated;
    private int _lastYear;
    private int _lastMonth;
    private bool _startupShown;
    private bool _constantinopleFallen;
    private bool _soundDuesCaptured;
    private bool _malaccaCaptured;
    private bool _gibraltarCaptured;
    private bool _muscatCaptured;
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
        _countriesEliminated = 0;
        _lastYear = 1450;
        _lastMonth = 1;
        _startupShown = false;
        _constantinopleFallen = false;
        _soundDuesCaptured = false;
        _malaccaCaptured = false;
        _gibraltarCaptured = false;
        _muscatCaptured = false;
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
        _host.Log($"OWO: Peace ratified between nation #{proposer} and #{target}");
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

        // Province 2276 = Constantinople (Bosporus & Dardanelles)
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
        // Province 162 = Copenhagen / Zealand (Sound Dues)
        else if (provinceId == 162 && !_soundDuesCaptured)
        {
            _soundDuesCaptured = true;
            _host.ShowPopup(
                "Maritime Chokepoint: Sound Dues Control",
                "Control over the Øresund straits (Zealand/Copenhagen) has shifted!\n\n"
              + "The sovereign master of the Sound commands the maritime tolls between the North Sea and the Baltic, "
              + "deeply influencing Hanseatic merchant profits and Scandinavian naval supremacy."
            );
            _host.Log("OWO: Sound Dues sovereignty altered! Baltic shipping bulletin dispatched.");
        }
        // Province 545 = Malacca (Straits of Malacca)
        else if (provinceId == 545 && !_malaccaCaptured)
        {
            _malaccaCaptured = true;
            _host.ShowPopup(
                "Global Trade Hub: Fall of Malacca",
                "The great maritime emporium of Malacca has been captured!\n\n"
              + "Sitting between the Indian Ocean and the South China Sea, the new conqueror controls the vital choke point "
              + "for the spice fleets of the Moluccas, Persian carpets, and Ming porcelain."
            );
            _host.Log("OWO: Malacca captured! Spice route bulletin dispatched.");
        }
        // Province 1234 or 2289 = Gibraltar (Pillars of Hercules)
        else if ((provinceId == 1234 || provinceId == 2289) && !_gibraltarCaptured)
        {
            _gibraltarCaptured = true;
            _host.ShowPopup(
                "Naval Gateway: Strait of Gibraltar",
                "The Rock of Gibraltar has changed hands!\n\n"
              + "As the gateway between the Mediterranean Sea and the Atlantic Ocean, mastery over the strait controls "
              + "naval access between the Italian maritime republics, Iberia, and the oceanic trade lanes."
            );
            _host.Log("OWO: Gibraltar captured! Mediterranean gateway bulletin dispatched.");
        }
        // Province 2046 = Muscat / Ormuz Gateway
        else if (provinceId == 2046 && !_muscatCaptured)
        {
            _muscatCaptured = true;
            _host.ShowPopup(
                "Maritime Crossroads: Gulf of Oman & Hormuz",
                "The maritime fortress of Muscat commanding the approaches to the Strait of Hormuz has fallen!\n\n"
              + "The conqueror now commands the vital conduit between the Persian Gulf silk markets and Indian Ocean commerce."
            );
            _host.Log("OWO: Muscat / Hormuz gateway captured!");
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
        _countriesEliminated++;
        _host.Log($"OWO: Country #{countryIndex} fully eliminated from the 1450 map.");
        _host.ShowPopup(
            "Dynastic Extinction & Sovereign Annexation",
            "A sovereign crown has been completely erased from the world map of 1450 AD!\n\n"
          + "Its royal lineage has been extinguished or driven into exile, and its provinces have been absorbed into the victor realm."
        );
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

            case AmbitionsHook:
                _host.ShowPopup("Historical Ambitions & Paths to Glory", BuildAmbitionsBody());
                _host.Log("OWO: ambitions popup shown via UI action");
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

            case DynastiesHook:
                _host.ShowPopup("Great Dynasties & Ruling Houses (1450)", BuildDynastiesBody());
                _host.Log("OWO: dynasties popup shown via UI action");
                break;

            case FaithsHook:
                _host.ShowPopup("Holy Sees & Spiritual Centers (1450)", BuildFaithsBody());
                _host.Log("OWO: faiths popup shown via UI action");
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
        return "ERA: 1450 ANNO DOMINI  (Current Date: " + year + "-" + monthText + ")\n\n"
             + "THE SIX SUPRANATIONAL ORDERS:\n"
             + "1. The Kalmar Union: Nordic crown union of Denmark (DAN), Sweden (SWD), and Norway under King Christian I.\n"
             + "2. The Swiss Confederacy: Alpine alliance of cantons (CHE) maintaining staunch armed neutrality.\n"
             + "3. The Holy Roman Empire: Imperial Diet of electors, prince-bishoprics, and free cities under Emperor Friedrich III (HAB).\n"
             + "4. The League of Lezhë: Skanderbeg's Albanian military confederation (LEZ) holding the Danubian-Balkan mountain wall.\n"
             + "5. The Livonian Confederation: Baltic tripartite union of the Livonian Order (LIV), Riga (RIG), and Dorpat.\n"
             + "6. The Ming Tributary Order: East Asian celestial hierarchy uniting Ming China (MYN), Joseon (JOS), and Ryukyu (RYU).\n\n"
             + "ACTIVE DAY-ONE WARS:\n"
             + "• The Hundred Years' War: France (FRA) pressing England (ENG) in Normandy and Gascony.\n"
             + "• First Ottoman-Albanian War: Sultan Murad II (OTT) besieging Krujë against Skanderbeg (LEZ).\n"
             + "• Second Margrave War: Brandenburg (BRG) contesting Franconian Imperial Cities.\n"
             + "• Incan Andean Expansion: Pachacuti (INC) marching north from Cusco against regional polities.\n"
             + "• Deccan Hegemony Contest: Vijayanagara (VIJ) locked in frontier war with the Bahmani Sultanate (BAH).\n\n"
             + "ECONOMIC REALITY:\n"
             + "• Base currency: The Gold Florin (48,000 Florins = 1.0 GDP weight).\n"
             + "• Modern hydrocarbons and synthetic commodities are disabled; economies thrive on grain, wool, timber, spices, and coinage.\n\n"
             + "Use the HUD toolbar crown button to review military chronicles, diplomatic ledgers, and historical victory conditions.";
    }

    private string BuildAmbitionsBody()
    {
        return "HISTORICAL AMBITIONS & PATHS TO GLORY\n\n"
             + "The five modern victories are disabled. Only nine demanding historical achievements can end the campaign:\n\n"
             + "1. IMPERIAL HEGEMONY (Global Hegemon)\n"
             + "   • Requirements: Year >= 1485 | 120+ Provinces Conquered | 10+ Wars Won | <2 Wars Lost | <150 Regiments Lost\n\n"
             + "2. DAWN OF THE AGE OF DISCOVERY (Oceanic Expansion)\n"
             + "   • Requirements: Year >= 1492 | 40+ Provinces Gained | 6+ Wars Won | <2 Wars Lost | <20 Ships Lost\n\n"
             + "3. SULTAN-I RUM & CALIPHATE (Ottoman Realm)\n"
             + "   • Requirements: Year >= 1480 | Flag: Constantinople Conquered | 80+ Provinces Gained | 8+ Wars Won | <2 Wars Lost\n\n"
             + "4. PAX SINICA & CELESTIAL MANDATE (Great Ming)\n"
             + "   • Requirements: Year >= 1490 | Flag: Beijing Defended | 0 Wars Lost | <3 Provinces Lost | 5+ Wars Won\n\n"
             + "5. SOVEREIGN OF THE SEVEN SEAS (Thalassocracy)\n"
             + "   • Requirements: Year >= 1488 | 45+ Coastal Provinces | 7+ Wars Won | <12 Ships Lost | <2 Wars Lost\n\n"
             + "6. CROWN OF SPAIN & RECONQUISTA (Castile & Aragon)\n"
             + "   • Requirements: Year >= 1492 | Flags: Reconquista Completed & Catholic Monarchs United | 50+ Provinces | 6+ Wars Won\n\n"
             + "7. THIRD ROME & TSARDOM OF ALL RUS (Muscovy)\n"
             + "   • Requirements: Year >= 1480 | Flag: Third Rome Proclaimed | 75+ Provinces Gained | 7+ Wars Won | <2 Wars Lost\n\n"
             + "8. TRIUMPH OF THE HUNDRED YEARS (France / England)\n"
             + "   • Requirements: Year >= 1475 | Flag: Hundred Years' War Won | 55+ Provinces Gained | 6+ Wars Won | <2 Wars Lost\n\n"
             + "9. TAWANTINSUYU: REALM OF THE FOUR PARTS (Inca Empire)\n"
             + "   • Requirements: Year >= 1480 | Flag: Tawantinsuyu Proclaimed | 60+ Andean Provinces | 6+ Wars Won | <2 Wars Lost";
    }

    private string BuildArchiveBody()
    {
        return "1450 GEOPOLITICAL & INTELLIGENCE LEDGER\n\n"
             + "Observed Wars Declared: " + _warsObserved + "\n"
             + "Observed Alliances Formed: " + _alliancesObserved + "\n"
             + "Observed Alliances Dissolved: " + _alliancesBroken + "\n"
             + "Observed Commercial Treaties: " + _tradeAgreementsObserved + "\n"
             + "Observed Territorial Conquests: " + _provincesCaptured + "\n"
             + "Observed Dynasties Extinguished: " + _countriesEliminated + "\n"
             + "Observed Doctrines Researched: " + _techsObserved + "\n"
             + "Observed Building Projects: " + _buildingsObserved + "\n"
             + "Observed Scripted Historical Events: " + _eventsObserved + "\n\n"
             + "Maintain dynastic legitimacy, secure global trade chokepoints, and honor treaty obligations.";
    }

    private string BuildChronicleBody()
    {
        string spiceStatus = _constantinopleFallen
            ? "SEVERED — Constantinople under Ottoman control; oceanic exploration imperative active."
            : "OPEN — Byzantine Bosporus intact; Venetian-Mamluk Alexandria spice route flowing.";

        string soundStatus = _soundDuesCaptured
            ? "CONTESTED — Sovereignty over the Øresund has shifted under wartime occupation."
            : "SECURE — Danish Crown collects Sound Dues; Hanseatic Kontors trade freely.";

        string malaccaStatus = _malaccaCaptured
            ? "CONQUERED — Malacca strait seized; Southeast Asian spice fleet flow altered."
            : "FLOURISHING — Sultanate of Malacca welcomes Indian and Ming merchantmen.";

        string gibraltarStatus = _gibraltarCaptured
            ? "CAPTURED — Pillars of Hercules occupied; Mediterranean gateway controlled."
            : "GUARDED — Iberian & Moorish naval squadrons watch the Atlantic strait.";

        string muscatStatus = _muscatCaptured
            ? "SEIZED — Gulf of Oman approaches controlled by foreign conquerors."
            : "UNOPPOSED — Ormuz and Omani dhows navigate Persian Gulf silk waters.";

        return "1450 WORLD CHRONICLE & MARITIME ARTERIES\n\n"
             + "• Current Date: " + _lastYear + " AD\n\n"
             + "STRATEGIC CHOKEPOINTS:\n"
             + "1. Bosporus & Dardanelles (Constantinople): " + spiceStatus + "\n"
             + "2. Øresund Sound Dues (Copenhagen): " + soundStatus + "\n"
             + "3. Straits of Malacca (Malacca): " + malaccaStatus + "\n"
             + "4. Pillars of Hercules (Gibraltar): " + gibraltarStatus + "\n"
             + "5. Strait of Hormuz & Gulf of Oman: " + muscatStatus + "\n\n"
             + "LEDGER OF CAMPAIGNS:\n"
             + "• Continental Wars Observed: " + _warsObserved + "\n"
             + "• Diplomatic Alliances Formed: " + _alliancesObserved + "\n"
             + "• Treaties Dissolved / Broken: " + _alliancesBroken + "\n"
             + "• Commercial Trade Agreements: " + _tradeAgreementsObserved + "\n"
             + "• Provinces Changed Sovereignty: " + _provincesCaptured + "\n"
             + "• Sovereign Realms Eliminated: " + _countriesEliminated + "\n\n"
             + "The world transitions from medieval chivalric levies into early modern sovereign states.";
    }

    private string BuildBalanceOfPowerBody()
    {
        return "BALANCE OF POWER & ALLIANCE NETWORKS (1450)\n\n"
             + "1. Western Christendom:\n"
             + "   • Kingdom of France (FRA) & Kingdom of Scotland (SCT) — The Auld Alliance\n"
             + "   • Kingdom of England (ENG) & Duchy of Burgundy (BUR) — Anglo-Burgundian ties\n"
             + "   • Crown of Castile (CAS) & Crown of Aragon (ARA) — Trastámara dynastic accord\n\n"
             + "2. Central & Northern Europe:\n"
             + "   • Kalmar Union: Denmark (DAN), Sweden (SWD), Norway\n"
             + "   • Swiss Confederacy: Alpine cantons of Switzerland (CHE)\n"
             + "   • Holy Roman Empire: Imperial Diet & Habsburg leadership (HAB)\n"
             + "   • Crown of Poland (POL) & Grand Duchy of Lithuania (LTH) — Jagiellonian Union\n"
             + "   • Crown of Hungary (HUN) & League of Lezhë (LEZ) — Anti-Ottoman Danubian front\n"
             + "   • Livonian Confederation: Livonian Order (LIV), Riga (RIG), Dorpat\n\n"
             + "3. Eastern Empires:\n"
             + "   • Grand Duchy of Moscow (MVY) & Pskov (PSK) — Unification against the Great Horde\n"
             + "   • Ming Dynasty (MYN) & Joseon (JOS) & Ryukyu (RYU) — Confucian Tributary Pact\n"
             + "   • Vijayanagara Empire (VIJ) vs. Bahmani Sultanate (BAH) — Deccan balance of power\n\n"
             + "4. Maritime Republics:\n"
             + "   • Republic of Venice (VNC) vs. Republic of Genoa (GEN) — Mediterranean trade rivalry";
    }

    private string BuildDynastiesBody()
    {
        return "GREAT HOUSES & RULING DYNASTIES (1450 AD)\n\n"
             + "1. Western Christendom:\n"
             + "   • House of Valois (FRA): King Charles VII — Consolidating post-Hundred Years' War royal realm.\n"
             + "   • House of Lancaster vs. York (ENG): King Henry VI & Richard of York — The Wars of the Roses.\n"
             + "   • House of Trastámara (CAS / ARA): King John II & Alfonso V — Divided Iberian crowns approaching union.\n"
             + "   • House of Valois-Burgundy (BUR): Duke Philip the Good — Grand Dukes of the West in the Low Countries.\n\n"
             + "2. Central & Northern Europe:\n"
             + "   • House of Habsburg (HAB): Emperor Friedrich III — Inner Austria and Imperial Roman Crown.\n"
             + "   • House of Jagiellon (POL / LTH): Casimir IV — Dual monarchy across the Baltic to the Black Sea.\n"
             + "   • House of Oldenburg (DAN / SWD): King Christian I — The Scandinavian Kalmar Union.\n\n"
             + "3. Eastern Empires:\n"
             + "   • House of Osman (OTT): Sultan Murad II & Mehmed II — Padishahs of the Ottoman realm.\n"
             + "   • Great Ming (MYN): Emperor Jingtai (Zhu Qiyu) — Ming imperial recovery following Tumu.\n"
             + "   • House of Timur (TIM): Sultan Abu Sa'id — Gurkani sovereignty over Transoxiana and Herat.\n"
             + "   • Sangama Dynasty (VIJ): Deva Raya II / Mallikarjuna Raya — Lords of the Southern Ocean.\n\n"
             + "4. The Americas:\n"
             + "   • Acamapichtli Lineage (AZT): Huey Tlatoani Moctezuma I — Sovereign of Tenochtitlan.\n"
             + "   • Hanan Cusco Dynasty (INC): Sapa Inca Pachacuti — Earthshaker and Architect of Tawantinsuyu.";
    }

    private string BuildFaithsBody()
    {
        return "HOLY SEES & SPIRITUAL AUTHORITIES (1450 AD)\n\n"
             + "1. Western Christendom (Catholicism):\n"
             + "   • Holy See of Rome: Pope Nicholas V — Seat of the Bishop of Rome and St. Peter's Basilica.\n"
             + "   • Pilgrimage Shrines: Santiago de Compostela, Canterbury, Cologne Cathedral of the Three Kings.\n\n"
             + "2. Eastern Christendom (Eastern Orthodoxy):\n"
             + "   • Ecumenical Patriarchate of Constantinople: Hagia Sophia — Imperial Mother Church.\n"
             + "   • Holy Mount Athos & Serbian Peć Patriarchate — Monastic bastions against expansion.\n\n"
             + "3. Dar al-Islam (Sunni & Shia):\n"
             + "   • Holy Sanctuaries of Mecca & Medina: Guarded by the Mamluk Sultanate of Cairo (MAM).\n"
             + "   • Al-Azhar Mosque & Madrasah: Premier seat of Islamic jurisprudence and theology in Cairo.\n"
             + "   • Great Mosque of Samarkand (Bibi-Khanym) & Timbuktu Sankore Mosque — Scholastic centers.\n\n"
             + "4. Dharmic, East Asian & Indigenous Faiths:\n"
             + "   • Varanasi & Hampi Virupaksha: Sacred tirthas along the Ganges and Tungabhadra rivers.\n"
             + "   • Temple of Heaven (Beijing) & Ise Grand Shrine (Japan): Mandate of Heaven and Shinto rites.\n"
             + "   • Potala & Jokhang (Lhasa): Sacred heart of Tibetan Vajrayana Buddhism.\n"
             + "   • Great Teocalli (Tenochtitlan) & Coricancha (Cusco): Solar temples of the Sun Gods.";
    }

    private string BuildInfoBody()
    {
        string version = _host.GetModVersion();
        return "Global Protocol: Old World Order\n"
             + "Version: " + version + "\n\n"
             + "A historical scenario mod focusing on the late medieval and early Renaissance era (1450 AD).\n"
             + "Features 137 historical nations, 4,604 calibrated provinces, deep diplomatic organizations, and 9 authentic victory conditions.\n\n"
             + "Project: Dorlion-Interactive/Global-Protocol-Old-World-Order-Mod";
    }
}

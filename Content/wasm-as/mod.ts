// GlobalProtocol: Old World Order — WASM Entrypoint (Variant B: AssemblyScript)
import { log, showPopup, readString, addTreasury } from "./gp";

const MOD_ID = "globalprotocol.old_world_order";

const WELCOME_HOOK = "owo.welcome";
const AMBITIONS_HOOK = "owo.ambitions";
const ARCHIVE_HOOK = "owo.archive";
const CHRONICLE_HOOK = "owo.chronicle";
const BALANCE_OF_POWER_HOOK = "owo.balance_of_power";
const DYNASTIES_HOOK = "owo.dynasties";
const FAITHS_HOOK = "owo.faiths";
const INFO_HOOK = "owo.info";

let warsObserved = 0;
let techsObserved = 0;
let buildingsObserved = 0;
let eventsObserved = 0;
let provincesCapturedObserved = 0;
let alliancesObserved = 0;
let tradeAgreementsObserved = 0;
let lastYear = 0;
let lastMonth = 0;
let startupShown = false;
let constantinopleFallen = false;
let soundDuesCaptured = false;
let malaccaCaptured = false;
let gibraltarCaptured = false;

export function on_init(): void {
    log("OWO init (AS ABI 3)");
}

export function on_game_tick(tick: i32, year: i32, month: i32): void {
    lastYear = year;
    lastMonth = month;

    if (startupShown) return;

    startupShown = true;
    showPopup("Strategic Briefing: 1450 AD", buildBriefingBody(year, month));
}

export function on_war_declared(attacker: i32, defender: i32, tick: i32): void {
    warsObserved++;
}

export function on_tech_researched(countryIndex: i32, techIndex: i32): void {
    techsObserved++;
}

export function on_building_completed(provinceId: i32, buildingDefIndex: i32): void {
    buildingsObserved++;
}

export function on_event_fired(countryIndex: i32, eventIndex: i32): void {
    eventsObserved++;
}

export function on_province_captured(provinceId: i32, newOwner: i32, oldOwner: i32): void {
    provincesCapturedObserved++;

    if (provinceId == 2276 && !constantinopleFallen) {
        constantinopleFallen = true;
        addTreasury(newOwner, 500.0);
        showPopup(
            "Geopolitical Shock: Fall of Constantinople",
            "With the fall of Constantinople, the Ottoman Empire secures uncontested mastery over the Bosporus straits.\n\n"
            + "The traditional Silk Road and Levantine spice trade corridors face heavy imperial tariffs and blockades."
        );
    } else if (provinceId == 162 && !soundDuesCaptured) {
        soundDuesCaptured = true;
        addTreasury(newOwner, 300.0);
        showPopup(
            "Maritime Chokepoint: Sound Dues Control",
            "Control over the Øresund straits (Zealand/Copenhagen) has shifted!\n\n"
            + "The sovereign master of the Sound commands the maritime tolls between the North Sea and the Baltic."
        );
    } else if (provinceId == 545 && !malaccaCaptured) {
        malaccaCaptured = true;
        addTreasury(newOwner, 400.0);
        showPopup(
            "Global Trade Hub: Fall of Malacca",
            "The great maritime emporium of Malacca has been captured!\n\n"
            + "Sitting between the Indian Ocean and the South China Sea, the new conqueror controls the vital spice fleet choke point."
        );
    } else if (provinceId == 2289 && !gibraltarCaptured) {
        gibraltarCaptured = true;
        addTreasury(newOwner, 250.0);
        showPopup(
            "Naval Gateway: Strait of Gibraltar",
            "The Rock of Gibraltar has changed hands!\n\n"
            + "As the gateway between the Mediterranean Sea and the Atlantic Ocean, mastery over the strait controls naval access."
        );
    }
}

export function on_alliance_formed(country1: i32, country2: i32): void {
    alliancesObserved++;
}

export function on_alliance_broken(country1: i32, country2: i32): void {
    // alliance dissolved
}

export function on_economy_tick(year: i32, month: i32): void {
    // monthly economy tick
}

export function on_trade_agreement_signed(country1: i32, country2: i32): void {
    tradeAgreementsObserved++;
}

export function on_ui_action(
    hookNamePtr: i32, hookNameLen: i32,
    modIdPtr: i32,    modIdLen: i32
): void {
    const modId = readString(modIdPtr, modIdLen);
    if (modId != MOD_ID) return;

    const hookName = readString(hookNamePtr, hookNameLen);

    if (hookName == WELCOME_HOOK) {
        showPopup("Strategic Briefing: 1450 AD", buildBriefingBody(lastYear, lastMonth));
    } else if (hookName == AMBITIONS_HOOK) {
        showPopup("Historical Ambitions & Paths to Glory", buildAmbitionsBody());
    } else if (hookName == ARCHIVE_HOOK) {
        showPopup("Historian's Archive", buildArchiveBody());
    } else if (hookName == CHRONICLE_HOOK) {
        showPopup("1450 World Chronicle", buildChronicleBody());
    } else if (hookName == BALANCE_OF_POWER_HOOK) {
        showPopup("Balance of Power & Alliances", buildBalanceOfPowerBody());
    } else if (hookName == DYNASTIES_HOOK) {
        showPopup("Great Dynasties & Ruling Houses (1450)", buildDynastiesBody());
    } else if (hookName == FAITHS_HOOK) {
        showPopup("Holy Sees & Spiritual Centers (1450)", buildFaithsBody());
    } else if (hookName == INFO_HOOK) {
        showPopup("Mod Information", buildInfoBody());
    }
}

function buildBriefingBody(year: i32, month: i32): string {
    const monthText = month < 10 ? "0" + month.toString() : month.toString();
    return "Era: 1450 AD (Current Date: " + year.toString() + "-" + monthText + ")\n\n"
        + "THE 1450 DIPLOMATIC WEB:\n"
        + "• The Jagiellonian Union: Poland (POL) and Lithuania (LTH) united under Casimir IV against the Teutonic Order.\n"
        + "• The Auld Alliance: France (FRA) and Scotland (SCT) press the English crown (ENG) in the Hundred Years' War.\n"
        + "• The Balkan Bastion: Hungary (HUN), Albania (LEZ), and the Papacy (PAP) confront Ottoman expansion (OTT).\n"
        + "• Italian Pentarchy: Maritime rivalry divides Venice (VNC) and Genoa (GEN); Milan (MIL) and Florence (FLR) balance Lombardy.\n"
        + "• The Iberian Concord: Castile (CAS), Aragon (ARA), and Portugal (PRT) maintain fragile peace on the Granada (GRN) frontier.\n"
        + "• Eastern Pacts: Ming China (MYN) rebuilds after Tumu with Joseon (JOS) tributary support; Vijayanagara (VIJ) contests the Deccan.\n\n"
        + "Use the buttons in the toolbar to access reports and mod information.";
}

function buildArchiveBody(): string {
    return "1450 Intelligence Report\n\n"
        + "Observed wars: " + warsObserved.toString() + "\n"
        + "Observed technologies: " + techsObserved.toString() + "\n"
        + "Observed building completions: " + buildingsObserved.toString() + "\n"
        + "Observed scripted events: " + eventsObserved.toString() + "\n"
        + "Observed territorial changes: " + provincesCapturedObserved.toString() + "\n"
        + "Observed alliances formed: " + alliancesObserved.toString() + "\n"
        + "Observed trade agreements: " + tradeAgreementsObserved.toString() + "\n\n"
        + "Model your strategy around legitimacy, supply corridors, and defensible terrain.";
}

function buildChronicleBody(): string {
    const spiceStatus = constantinopleFallen
        ? "SEVERED — Constantinople in Ottoman hands; oceanic exploration underway."
        : "OPEN — Byzantine Bosporus intact; Alexandria spice corridor active.";

    const soundStatus = soundDuesCaptured
        ? "CONTESTED — Øresund Sound sovereignty has shifted under war."
        : "SECURE — Danish Crown collects tolls; Baltic shipping clear.";

    const malaccaStatus = malaccaCaptured
        ? "CONQUERED — Malacca strait seized by new master."
        : "FLOURISHING — Malacca Sultanate welcomes Asian fleets.";

    const gibraltarStatus = gibraltarCaptured
        ? "CAPTURED — Pillars of Hercules occupied."
        : "GUARDED — Iberian & Moroccan squadrons patrol.";

    return "1450 WORLD CHRONICLE & MARITIME ARTERIES\n\n"
        + "• Year of Epoch: 1450 AD\n\n"
        + "GLOBAL CHOKEPOINTS:\n"
        + "1. Bosporus (Constantinople): " + spiceStatus + "\n"
        + "2. Sound Dues (Copenhagen): " + soundStatus + "\n"
        + "3. Straits of Malacca: " + malaccaStatus + "\n"
        + "4. Gibraltar Gateway: " + gibraltarStatus + "\n\n"
        + "CAMPAIGNS LEDGER:\n"
        + "• Continental Wars: " + warsObserved.toString() + "\n"
        + "• Diplomatic Alliances: " + alliancesObserved.toString() + "\n"
        + "• Commercial Trade Pacts: " + tradeAgreementsObserved.toString() + "\n"
        + "• Provinces Changed Hands: " + provincesCapturedObserved.toString() + "\n\n"
        + "The world transitions from medieval chivalric levies into early modern sovereign states.";
}

function buildBalanceOfPowerBody(): string {
    return "BALANCE OF POWER & ALLIANCE NETWORKS (1450)\n\n"
        + "1. Western Christendom:\n"
        + "   • France (FRA) & Scotland (SCT) — The Auld Alliance\n"
        + "   • England (ENG) & Burgundy (BUR) — Anglo-Burgundian ties\n"
        + "   • Castile (CAS) & Aragon (ARA) — Trastámara accord\n\n"
        + "2. Central & Eastern Europe:\n"
        + "   • Poland (POL) & Lithuania (LTH) — Jagiellonian Union\n"
        + "   • Hungary (HUN) & Albania (LEZ) — Danubian Anti-Ottoman front\n"
        + "   • Moscow (MVY) & Pskov (PSK) — Defense against the Great Horde\n\n"
        + "3. Eastern Empires:\n"
        + "   • Ming (MYN) & Joseon (JOS) — Confucian Tributary Pact\n"
        + "   • Vijayanagara (VIJ) vs. Bahmani (BAH) — Deccan balance of power\n\n"
        + "4. Maritime Republics:\n"
        + "   • Venice (VNC) vs. Genoa (GEN) — Mediterranean trade rivalry";
}

function buildDynastiesBody(): string {
    return "GREAT HOUSES & RULING DYNASTIES (1450 AD)\n\n"
        + "1. Western Christendom:\n"
        + "   • House of Valois (FRA): King Charles VII — Consolidating the French realm.\n"
        + "   • House of Lancaster vs. York (ENG): King Henry VI & Richard of York.\n"
        + "   • House of Trastámara (CAS / ARA): King John II & Alfonso V of Aragon.\n"
        + "   • House of Valois-Burgundy (BUR): Duke Philip the Good — Grand Dukes of the West.\n\n"
        + "2. Central & Northern Europe:\n"
        + "   • House of Habsburg (HAB): Duke Friedrich III — Archduke and Roman King.\n"
        + "   • House of Jagiellon (POL / LTH): Casimir IV — Baltic-Pontic dual monarchy.\n"
        + "   • House of Oldenburg (DAN / SWD): King Christian I — Scandinavian Kalmar Union.\n\n"
        + "3. Eastern Empires:\n"
        + "   • House of Osman (OTT): Sultan Murad II & Mehmed II.\n"
        + "   • Great Ming (MYN): Emperor Jingtai — Imperial recovery.\n"
        + "   • House of Timur (TIM): Sultan Abu Sa'id — Transoxiana sovereignty.\n"
        + "   • Sangama Dynasty (VIJ): Deva Raya II — Lords of the Southern Ocean.\n\n"
        + "4. The Americas:\n"
        + "   • Acamapichtli Lineage (AZT): Moctezuma I of Tenochtitlan.\n"
        + "   • Hanan Cusco Dynasty (INC): Sapa Inca Pachacuti of Tawantinsuyu.";
}

function buildFaithsBody(): string {
    return "HOLY SEES & SPIRITUAL AUTHORITIES (1450 AD)\n\n"
        + "1. Western Christendom:\n"
        + "   • Holy See of Rome: Pope Nicholas V — St. Peter's Basilica.\n"
        + "   • Major Shrines: Santiago de Compostela, Canterbury, Cologne.\n\n"
        + "2. Eastern Christendom:\n"
        + "   • Ecumenical Patriarchate of Constantinople: Hagia Sophia.\n"
        + "   • Holy Mount Athos & Serbian Peć Patriarchate.\n\n"
        + "3. Dar al-Islam:\n"
        + "   • Holy Sanctuaries of Mecca & Medina: Guarded by Cairo Mamluks (MAM).\n"
        + "   • Al-Azhar Mosque & Madrasah: Islamic jurisprudence in Cairo.\n"
        + "   • Great Mosque of Samarkand & Timbuktu Sankore Mosque.\n\n"
        + "4. Eastern & Indigenous Faiths:\n"
        + "   • Varanasi & Hampi Virupaksha: Sacred tirthas along sacred rivers.\n"
        + "   • Temple of Heaven (Beijing) & Ise Grand Shrine (Japan).\n"
        + "   • Potala & Jokhang (Lhasa): Tibetan Vajrayana Buddhism.\n"
        + "   • Great Teocalli (Tenochtitlan) & Coricancha (Cusco): Sun temples.";
}

function buildAmbitionsBody(): string {
    return "PATHS TO GLORY & HISTORICAL AMBITIONS (1450 AD)\n\n"
        + "1. Ottoman Empire (OTT):\n"
        + "   • Fall of Constantinople: Shatter the Theodosian Walls and claim the mantle of the Caesars.\n"
        + "   • Danubian Frontier: Advance into the Balkans against Hungarian bastions.\n\n"
        + "2. Kingdom of France (FRA):\n"
        + "   • Expel the English from Guyenne and Normandy to conclude the Hundred Years' War.\n"
        + "   • Subjugate and absorb the Burgundian appanage to consolidate the French crown.\n\n"
        + "3. Crown of Castile (CAS) & Portugal (PRT):\n"
        + "   • Reconquista: Subjugate the Nasrid Kingdom of Granada and claim Gibraltar.\n"
        + "   • Oceanic Enterprise: Navigate the African littoral and unlock the Ocean Sea.\n\n"
        + "4. Great Ming (MYN):\n"
        + "   • Rebound from the Tumu disaster and reinforce the northern Great Wall garrisons.\n"
        + "   • Preserve the Confucian Tributary Order across maritime and continental Asia.\n\n"
        + "5. Grand Duchy of Moscow (MVY):\n"
        + "   • Gather the Russian lands from Novgorod and Tver.\n"
        + "   • Cast off the Great Horde's yoke and proclaim Moscow the Third Rome.\n\n"
        + "Consult your national agenda panel for country-specific focus tasks and milestone rewards.";
}

function buildInfoBody(): string {
    return "Global Protocol: Old World Order\n"
        + "Version: 0.10.0\n\n"
        + "A historical scenario mod focusing on the late medieval era.\n"
        + "Showcasing UI injection across SDK, WASM.NET, and AS paths.\n\n"
        + "Project: Dorlion-Interactive/Global-Protocol-Old-World-Order-Mod";
}

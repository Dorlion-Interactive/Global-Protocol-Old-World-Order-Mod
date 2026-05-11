// GlobalProtocol: Old World Order — WASM Entrypoint (Variant B: AssemblyScript)
//
// This is your mod's main file for the AssemblyScript variant.
// The engine calls only the hooks you export here. Delete the ones you don't need.
// To call back INTO the game (fire events, log, read state), use gp.* (see gp.ts).
//
// gp.fireEvent(countryIndex, eventId) — trigger a scripted event
//   countryIndex 0 = the local player's country in single-player
//   eventId      = the event ID from your Content/events/*.json file
//
// Build:
//   npm install
//   npx asc mod.ts --target release -o ../mod.wasm

import { log, showPopup, readString } from "./gp";

const MOD_ID = "globalprotocol.old_world_order";
const STARTUP_POPUP_TITLE = "Old World Order, 1450";
const TOOLBAR_POPUP_TITLE = "Strategic Briefing";

let welcomeShown = false;

// Optional initialization hook. The host calls this once at startup if present.
export function on_init(): void {
    // Keep at least one gp host import alive so runtime link binding resolves against module "gp".
    log("OWO init");
}

// Called every game tick.
// tick = total elapsed ticks, year/month = current in-game date.
export function on_game_tick(tick: i32, year: i32, month: i32): void {
    if (welcomeShown) return;

    welcomeShown = true;
    showPopup(STARTUP_POPUP_TITLE, buildStartupBody(year, month));
    log("OWO: welcome popup shown on first tick via show_mod_popup");
}

// Called when a war is declared.
// attacker / defender are country indices (0 = local player in single-player).
export function on_war_declared(attacker: i32, defender: i32, tick: i32): void {
}

// Called when peace is signed between two countries.
export function on_peace_signed(proposer: i32, target: i32): void {
}

// Called when a country finishes researching a technology.
export function on_tech_researched(countryIndex: i32, techIndex: i32): void {
}

// Called when a building finishes construction in a province.
export function on_building_completed(provinceId: i32, buildingDefIndex: i32): void {
}

// Called when any scripted event fires for any country.
export function on_event_fired(countryIndex: i32, eventIndex: i32): void {
}

// Called when a country is fully eliminated from the game.
export function on_country_eliminated(countryIndex: i32): void {
}

// Called when a toolbar button (registered in mod.json entrypoints.ui) is clicked.
// Always check modId first — other mods fire this hook too.
export function on_ui_action(
    hookNamePtr: i32, hookNameLen: i32,
    modIdPtr: i32,    modIdLen: i32
): void {
    if (readString(modIdPtr, modIdLen) != MOD_ID) return;

    const hookName = readString(hookNamePtr, hookNameLen);
    if (hookName != "owo.welcome") return;

    showPopup(TOOLBAR_POPUP_TITLE, buildToolbarBody());
    log("OWO: welcome popup reopened via toolbar button via show_mod_popup");
}

function buildStartupBody(year: i32, month: i32): string {
    const monthText = month < 10 ? "0" + month.toString() : month.toString();
    return "Date: " + year.toString() + "-" + monthText + "\n"
        + "\n"
        + "Europe and Asia stand between old feudal orders and rising centralized states.\n"
        + "Trade routes across the Mediterranean, Black Sea, Indian Ocean, and Silk Road are the arteries of power.\n"
        + "Gunpowder armies are emerging, but cavalry, levies, and fortresses still decide most wars.\n"
        + "\n"
        + "You command one of 120+ historical polities with period-appropriate rulers, borders, and military posture.\n"
        + "Use the crown button in the toolbar to reopen this briefing at any time.";
}

function buildToolbarBody(): string {
    return "1450 Intelligence Report\n"
        + "\n"
        + "- The Ottoman state is expanding through the Balkans and Anatolia\n"
        + "- The Hundred Years' War era has ended, but Franco-English rivalry remains\n"
        + "- Iberian crowns are consolidating while Atlantic navigation accelerates\n"
        + "- Ming authority dominates East Asia as steppe powers contest the interior\n"
        + "- Regional beyliks, principalities, and sultanates create volatile frontiers\n"
        + "\n"
        + "Model your strategy around legitimacy, supply corridors, and defensible terrain.";
}

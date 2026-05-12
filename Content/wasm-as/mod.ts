// GlobalProtocol: Old World Order — WASM Entrypoint (Variant B: AssemblyScript)
import { log, showPopup, readString } from "./gp";

const MOD_ID = "globalprotocol.old_world_order";

const WELCOME_HOOK = "owo.welcome";
const ARCHIVE_HOOK = "owo.archive";
const INFO_HOOK = "owo.info";

let warsObserved = 0;
let techsObserved = 0;
let buildingsObserved = 0;
let eventsObserved = 0;
let lastYear = 0;
let lastMonth = 0;
let startupShown = false;

export function on_init(): void {
    log("OWO init (AS)");
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

export function on_ui_action(
    hookNamePtr: i32, hookNameLen: i32,
    modIdPtr: i32,    modIdLen: i32
): void {
    const modId = readString(modIdPtr, modIdLen);
    if (modId != MOD_ID) return;

    const hookName = readString(hookNamePtr, hookNameLen);

    if (hookName == WELCOME_HOOK) {
        showPopup("Strategic Briefing: 1450 AD", buildBriefingBody(lastYear, lastMonth));
    } else if (hookName == ARCHIVE_HOOK) {
        showPopup("Historian's Archive", buildArchiveBody());
    } else if (hookName == INFO_HOOK) {
        showPopup("Mod Information", buildInfoBody());
    }
}

function buildBriefingBody(year: i32, month: i32): string {
    const monthText = month < 10 ? "0" + month.toString() : month.toString();
    return "Date: " + year.toString() + "-" + monthText + "\n\n"
        + "Europe and Asia stand between old feudal orders and rising centralized states.\n"
        + "Trade routes across the Mediterranean, Black Sea, Indian Ocean, and Silk Road are the arteries of power.\n"
        + "Gunpowder armies are emerging, but cavalry, levies, and fortresses still decide most wars.\n\n"
        + "Use the buttons in the toolbar to access reports and mod information.";
}

function buildArchiveBody(): string {
    return "1450 Intelligence Report\n\n"
        + "Observed wars: " + warsObserved.toString() + "\n"
        + "Observed technologies: " + techsObserved.toString() + "\n"
        + "Observed building completions: " + buildingsObserved.toString() + "\n"
        + "Observed scripted events: " + eventsObserved.toString() + "\n\n"
        + "Model your strategy around legitimacy, supply corridors, and defensible terrain.";
}

function buildInfoBody(): string {
    return "Global Protocol: Old World Order\n"
        + "Version: 0.2.2\n\n"
        + "A historical scenario mod focusing on the late medieval era.\n"
        + "Showcasing UI injection across SDK, WASM.NET, and AS paths.\n\n"
        + "Project: Dorlion-Interactive/Global-Protocol-Old-World-Order-Mod";
}

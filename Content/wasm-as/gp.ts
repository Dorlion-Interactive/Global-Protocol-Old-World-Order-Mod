// GlobalProtocol AssemblyScript helper — wraps all low-level host imports.
// Import from this module in mod.ts instead of calling gp_* functions directly.

// ─── Raw host imports (do not call these directly) ───────────────────────────

@external("gp", "log")
declare function gp_log(msgPtr: i32, msgLen: i32): void;

@external("gp", "show_mod_popup")
declare function gp_show_mod_popup(titlePtr: i32, titleLen: i32, bodyPtr: i32, bodyLen: i32): void;

@external("gp", "fire_event")
declare function gp_fire_event(countryIndex: i32, eventIdPtr: i32, eventIdLen: i32): void;

@external("gp", "get_year")
declare function gp_get_year(): i32;

// ─── High-level helpers (use these in mod.ts) ────────────────────────────────

/** Write a message to the Unity console (debug builds; no-op in release). */
export function log(msg: string): void {
    const b = String.UTF8.encode(msg);
    gp_log(changetype<i32>(b), b.byteLength);
}

/**
 * Fire a scripted event for a country.
 * countryIndex 0 = local player in single-player.
 * Requires "FireTriggers" permission in mod.json.
 */
export function fireEvent(countryIndex: i32, eventId: string): void {
    const b = String.UTF8.encode(eventId);
    gp_fire_event(countryIndex, changetype<i32>(b), b.byteLength);
}

/**
 * Show a direct popup dialog in the game UI.
 * Requires "InjectUI" permission in mod.json.
 */
export function showPopup(title: string, body: string): void {
    const titleBytes = String.UTF8.encode(title);
    const bodyBytes = String.UTF8.encode(body);
    gp_show_mod_popup(
        changetype<i32>(titleBytes),
        titleBytes.byteLength,
        changetype<i32>(bodyBytes),
        bodyBytes.byteLength
    );
}

/**
 * Decode a UTF-8 string passed in from the engine (ptr + len).
 * Use this in on_ui_action to read hookName and modId.
 */
export function readString(ptr: i32, len: i32): string {
    if (len <= 0) return "";
    return String.UTF8.decodeUnsafe(ptr, len);
}

/** Current in-game year. */
export function year(): i32 {
    return gp_get_year();
}

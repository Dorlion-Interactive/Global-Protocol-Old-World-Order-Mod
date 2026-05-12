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

@external("gp", "log_string")
declare function gp_log_string(msgPtr: i32): void;

@external("gp", "get_country_gdp")
declare function gp_get_country_gdp(countryIndex: i32): f32;

@external("gp", "get_country_treasury")
declare function gp_get_country_treasury(countryIndex: i32): f32;

@external("gp", "get_country_stability")
declare function gp_get_country_stability(countryIndex: i32): f32;

@external("gp", "get_country_manpower")
declare function gp_get_country_manpower(countryIndex: i32): i32;

@external("gp", "get_current_tick")
declare function gp_get_current_tick(): i32;

@external("gp", "get_current_year")
declare function gp_get_current_year(): i32;

@external("gp", "get_current_month")
declare function gp_get_current_month(): i32;

@external("gp", "add_treasury")
declare function gp_add_treasury(countryIndex: i32, amount: f32): void;

@external("gp", "fire_trigger")
declare function gp_fire_trigger(countryIndex: i32, triggerId: i32, targetIndex: i32): void;

@external("gp", "get_tick")
declare function gp_get_tick(): i32;

@external("gp", "get_month")
declare function gp_get_month(): i32;

@external("gp", "country_get_gdp")
declare function gp_country_get_gdp(countryIndex: i32): f64;

@external("gp", "country_get_stability")
declare function gp_country_get_stability(countryIndex: i32): f32;

@external("gp", "country_get_treasury")
declare function gp_country_get_treasury(countryIndex: i32): f64;

@external("gp", "country_set_treasury")
declare function gp_country_set_treasury(countryIndex: i32, amount: f64): void;

@external("gp", "country_get_tech_level")
declare function gp_country_get_tech_level(countryIndex: i32): i32;

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

/**
 * Anchor all known host imports in this module so wasm link coverage is explicit.
 * This function is never called by the host, and its guarded branch never runs,
 * so behavior remains unchanged while imports remain visible to the linker.
 */
export function keepHostImportLinks(seed: i32): i32 {
    if (seed == 0x7fffffff) {
        gp_log_string(0);
        gp_add_treasury(0, 0.0);
        gp_fire_trigger(0, 0, 0);
        gp_show_mod_popup(0, 0, 0, 0);
        gp_fire_event(0, 0, 0);
        gp_country_set_treasury(0, 0.0);

        let sum: i32 = 0;
        sum += gp_get_current_tick();
        sum += gp_get_current_year();
        sum += gp_get_current_month();
        sum += gp_get_tick();
        sum += gp_get_year();
        sum += gp_get_month();
        sum += gp_get_country_manpower(0);
        sum += gp_country_get_tech_level(0);

        sum += i32(gp_get_country_gdp(0));
        sum += i32(gp_get_country_treasury(0));
        sum += i32(gp_get_country_stability(0));
        sum += i32(gp_country_get_gdp(0));
        sum += i32(gp_country_get_stability(0));
        sum += i32(gp_country_get_treasury(0));
        return sum;
    }

    return 0;
}

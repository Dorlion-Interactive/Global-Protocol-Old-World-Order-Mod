#include <stdint.h>
#include <string.h>

// Component-lowered host imports (strings are ptr+len in linear memory).
__attribute__((import_module("globalprotocol:hooks/gp@1.0.0"), import_name("log")))
extern void gp_log(const uint8_t* msg_ptr, int32_t msg_len);

__attribute__((import_module("globalprotocol:hooks/gp@1.0.0"), import_name("show-mod-popup")))
extern void gp_show_mod_popup(const uint8_t* title_ptr, int32_t title_len, const uint8_t* body_ptr, int32_t body_len);

static int g_welcome_shown = 0;

static const char MOD_ID[] = "globalprotocol.old_world_order";
static const char HOOK_WELCOME[] = "owo.welcome";

static const char STARTUP_TITLE[] = "Old World Order, 1450";
static const char STARTUP_BODY[] =
    "Europe and Asia stand between old feudal orders and rising centralized states.\n"
    "Trade routes across the Mediterranean, Black Sea, Indian Ocean, and Silk Road are the arteries of power.\n\n"
    "You command one of 120+ historical polities with period-appropriate rulers, borders, and military posture.";

static const char TOOLBAR_TITLE[] = "Strategic Briefing";
static const char TOOLBAR_BODY[] =
    "1450 Intelligence Report\n\n"
    "- The Ottoman state is expanding through the Balkans and Anatolia\n"
    "- Ming authority dominates East Asia as steppe powers contest the interior\n"
    "- Regional beyliks, principalities, and sultanates create volatile frontiers";

static void log_text(const char* text)
{
    if (text == 0) return;
    gp_log((const uint8_t*)text, (int32_t)strlen(text));
}

static int slice_equals(const uint8_t* ptr, int32_t len, const char* text)
{
    if (ptr == 0 || text == 0 || len < 0) return 0;

    int32_t target_len = (int32_t)strlen(text);
    if (len != target_len) return 0;

    return memcmp(ptr, text, (size_t)len) == 0;
}

static void on_init_impl(void)
{
    log_text("OWO init (.native shim)");
}

static void on_game_tick_impl(int32_t tick, int32_t year, int32_t month)
{
    (void)tick;
    (void)year;
    (void)month;

    if (g_welcome_shown) return;

    g_welcome_shown = 1;
    gp_show_mod_popup((const uint8_t*)STARTUP_TITLE, (int32_t)strlen(STARTUP_TITLE),
                      (const uint8_t*)STARTUP_BODY, (int32_t)strlen(STARTUP_BODY));
    log_text("OWO: welcome popup shown on first tick via native shim");
}

static void on_ui_action_impl(const uint8_t* hook_name_ptr, int32_t hook_name_len,
                              const uint8_t* mod_id_ptr, int32_t mod_id_len)
{
    if (!slice_equals(mod_id_ptr, mod_id_len, MOD_ID)) return;
    if (!slice_equals(hook_name_ptr, hook_name_len, HOOK_WELCOME)) return;

    gp_show_mod_popup((const uint8_t*)TOOLBAR_TITLE, (int32_t)strlen(TOOLBAR_TITLE),
                      (const uint8_t*)TOOLBAR_BODY, (int32_t)strlen(TOOLBAR_BODY));
    log_text("OWO: welcome popup reopened via toolbar button via native shim");
}

// Underscore exports (core-runtime compatibility)
__attribute__((export_name("on_init")))
void on_init_export(void) { on_init_impl(); }

__attribute__((export_name("on_game_tick")))
void on_game_tick_export(int32_t tick, int32_t year, int32_t month) { on_game_tick_impl(tick, year, month); }

__attribute__((export_name("on_war_declared")))
void on_war_declared_export(int32_t attacker, int32_t defender, int32_t tick) { (void)attacker; (void)defender; (void)tick; }

__attribute__((export_name("on_peace_signed")))
void on_peace_signed_export(int32_t proposer, int32_t target) { (void)proposer; (void)target; }

__attribute__((export_name("on_tech_researched")))
void on_tech_researched_export(int32_t country_index, int32_t tech_index) { (void)country_index; (void)tech_index; }

__attribute__((export_name("on_building_completed")))
void on_building_completed_export(int32_t province_id, int32_t building_def_index) { (void)province_id; (void)building_def_index; }

__attribute__((export_name("on_country_eliminated")))
void on_country_eliminated_export(int32_t country_index) { (void)country_index; }

__attribute__((export_name("on_event_fired")))
void on_event_fired_export(int32_t country_index, int32_t event_index) { (void)country_index; (void)event_index; }

__attribute__((export_name("on_ui_action")))
void on_ui_action_export(const uint8_t* hook_name_ptr, int32_t hook_name_len,
                         const uint8_t* mod_id_ptr, int32_t mod_id_len)
{
    on_ui_action_impl(hook_name_ptr, hook_name_len, mod_id_ptr, mod_id_len);
}

// Interface-qualified exports (component-world compatibility)
__attribute__((export_name("globalprotocol:hooks/mod-hooks@1.0.0#on-init")))
void on_init_kebab_export(void) { on_init_impl(); }

__attribute__((export_name("globalprotocol:hooks/mod-hooks@1.0.0#on-game-tick")))
void on_game_tick_kebab_export(int32_t tick, int32_t year, int32_t month) { on_game_tick_impl(tick, year, month); }

__attribute__((export_name("globalprotocol:hooks/mod-hooks@1.0.0#on-war-declared")))
void on_war_declared_kebab_export(int32_t attacker, int32_t defender, int32_t tick) { (void)attacker; (void)defender; (void)tick; }

__attribute__((export_name("globalprotocol:hooks/mod-hooks@1.0.0#on-peace-signed")))
void on_peace_signed_kebab_export(int32_t proposer, int32_t target) { (void)proposer; (void)target; }

__attribute__((export_name("globalprotocol:hooks/mod-hooks@1.0.0#on-tech-researched")))
void on_tech_researched_kebab_export(int32_t country_index, int32_t tech_index) { (void)country_index; (void)tech_index; }

__attribute__((export_name("globalprotocol:hooks/mod-hooks@1.0.0#on-building-completed")))
void on_building_completed_kebab_export(int32_t province_id, int32_t building_def_index) { (void)province_id; (void)building_def_index; }

__attribute__((export_name("globalprotocol:hooks/mod-hooks@1.0.0#on-country-eliminated")))
void on_country_eliminated_kebab_export(int32_t country_index) { (void)country_index; }

__attribute__((export_name("globalprotocol:hooks/mod-hooks@1.0.0#on-event-fired")))
void on_event_fired_kebab_export(int32_t country_index, int32_t event_index) { (void)country_index; (void)event_index; }

__attribute__((export_name("globalprotocol:hooks/mod-hooks@1.0.0#on-ui-action")))
void on_ui_action_kebab_export(const uint8_t* hook_name_ptr, int32_t hook_name_len,
                               const uint8_t* mod_id_ptr, int32_t mod_id_len)
{
    on_ui_action_impl(hook_name_ptr, hook_name_len, mod_id_ptr, mod_id_len);
}

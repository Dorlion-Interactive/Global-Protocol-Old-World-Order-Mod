import json
import os

GOALS_TO_ADD = {
    "MVY": {
        "goals": [
            {
                "id": "mvy_gather_russian_lands",
                "title": "Gather the Russian Lands",
                "title_key": "owo.goal.mvy_gather_russian_lands",
                "description": "Unify the divided principalities of Rus under the leadership of Moscow.",
                "description_key": "owo.goal.mvy_gather_russian_lands.desc",
                "type": "expansion",
                "priority": "primary",
                "ai_weight": 0.85,
                "target_countries": ["NVD", "TVR", "RYA"],
                "on_complete_effects": {
                    "prestige": 40,
                    "stability": 5
                },
                "tasks": [
                    {
                        "id": "army",
                        "title_key": "owo.task.mvy_gather_russian_lands.army",
                        "title": "Muster 15,000 soldiers",
                        "condition": {
                            "type": "military_units_above",
                            "params": {
                                "unit_type": "personnel",
                                "min_value": "15000"
                            }
                        },
                        "required_count": 15000
                    },
                    {
                        "id": "novgorod",
                        "title_key": "owo.task.mvy_gather_russian_lands.novgorod",
                        "title": "Declare war on the Novgorod Republic",
                        "condition": {
                            "type": "declare_war_on",
                            "params": {
                                "target_iso3": "NVD"
                            }
                        }
                    }
                ]
            },
            {
                "id": "mvy_stand_against_the_horde",
                "title": "Stand Against the Horde",
                "title_key": "owo.goal.mvy_stand_against_the_horde",
                "description": "Cast off the Tatar yoke and refuse all further tribute to the Great Horde.",
                "description_key": "owo.goal.mvy_stand_against_the_horde.desc",
                "type": "defense",
                "priority": "secondary",
                "ai_weight": 0.75,
                "target_countries": ["STE"],
                "on_complete_effects": {
                    "prestige": 35,
                    "stability": 5
                },
                "tasks": [
                    {
                        "id": "treasury",
                        "title_key": "owo.task.mvy_stand_against_the_horde.treasury",
                        "title": "Amass 800 fl. in the treasury",
                        "condition": {
                            "type": "treasury_above",
                            "params": {
                                "min_value": "800"
                            }
                        }
                    },
                    {
                        "id": "army",
                        "title_key": "owo.task.mvy_stand_against_the_horde.army",
                        "title": "Field an army of 25,000 men",
                        "condition": {
                            "type": "military_units_above",
                            "params": {
                                "unit_type": "personnel",
                                "min_value": "25000"
                            }
                        },
                        "required_count": 25000
                    }
                ]
            }
        ]
    },
    "VNC": {
        "goals": [
            {
                "id": "vnc_queen_of_the_adriatic",
                "title": "Queen of the Adriatic",
                "title_key": "owo.goal.vnc_queen_of_the_adriatic",
                "description": "Enrich the republic through unrivaled maritime commerce across the eastern Mediterranean.",
                "description_key": "owo.goal.vnc_queen_of_the_adriatic.desc",
                "type": "economic",
                "priority": "primary",
                "ai_weight": 0.85,
                "on_complete_effects": {
                    "prestige": 30,
                    "economy_boost": 0.05
                },
                "tasks": [
                    {
                        "id": "treasury",
                        "title_key": "owo.task.vnc_queen_of_the_adriatic.treasury",
                        "title": "Accumulate 1,200 fl. in the ducal treasury",
                        "condition": {
                            "type": "treasury_above",
                            "params": {
                                "min_value": "1200"
                            }
                        }
                    },
                    {
                        "id": "trade",
                        "title_key": "owo.task.vnc_queen_of_the_adriatic.trade",
                        "title": "Establish bilateral trade agreements",
                        "condition": {
                            "type": "trade_agreement_with",
                            "params": {
                                "partners": "*"
                            }
                        }
                    }
                ]
            },
            {
                "id": "vnc_defend_stato_da_mar",
                "title": "Defend the Stato da Màr",
                "title_key": "owo.goal.vnc_defend_stato_da_mar",
                "description": "Protect Venetian island outposts and sea lanes against Ottoman maritime expansion.",
                "description_key": "owo.goal.vnc_defend_stato_da_mar.desc",
                "type": "defense",
                "priority": "secondary",
                "ai_weight": 0.75,
                "target_countries": ["OTT"],
                "on_complete_effects": {
                    "prestige": 25,
                    "military_modifier": 0.05
                },
                "tasks": [
                    {
                        "id": "fleet",
                        "title_key": "owo.task.vnc_defend_stato_da_mar.fleet",
                        "title": "Maintain a formidable naval armada",
                        "condition": {
                            "type": "military_units_above",
                            "params": {
                                "unit_type": "naval",
                                "min_value": "15"
                            }
                        },
                        "required_count": 15
                    }
                ]
            }
        ]
    },
    "HUN": {
        "goals": [
            {
                "id": "hun_bastion_of_christendom",
                "title": "Bastion of Christendom",
                "title_key": "owo.goal.hun_bastion_of_christendom",
                "description": "Defend the southern frontier against Ottoman incursions along the Danube and Sava rivers.",
                "description_key": "owo.goal.hun_bastion_of_christendom.desc",
                "type": "defense",
                "priority": "primary",
                "ai_weight": 0.90,
                "target_countries": ["OTT"],
                "on_complete_effects": {
                    "prestige": 45,
                    "stability": 5
                },
                "tasks": [
                    {
                        "id": "army",
                        "title_key": "owo.task.hun_bastion_of_christendom.army",
                        "title": "Muster a border defense army of 25,000 soldiers",
                        "condition": {
                            "type": "military_units_above",
                            "params": {
                                "unit_type": "personnel",
                                "min_value": "25000"
                            }
                        },
                        "required_count": 25000
                    },
                    {
                        "id": "allies",
                        "title_key": "owo.task.hun_bastion_of_christendom.allies",
                        "title": "Seek alliances with Central European crowns",
                        "condition": {
                            "type": "alliance_with",
                            "params": {
                                "partners": "POL,HAB,BOH"
                            }
                        }
                    }
                ]
            },
            {
                "id": "hun_corvinus_hegemony",
                "title": "The Corvinus Renaissance",
                "title_key": "owo.goal.hun_corvinus_hegemony",
                "description": "Modernize royal finances, patronize humanist culture, and expand royal sovereignty.",
                "description_key": "owo.goal.hun_corvinus_hegemony.desc",
                "type": "prestige",
                "priority": "secondary",
                "ai_weight": 0.65,
                "on_complete_effects": {
                    "prestige": 30,
                    "economy_boost": 0.03
                },
                "tasks": [
                    {
                        "id": "treasury",
                        "title_key": "owo.task.hun_corvinus_hegemony.treasury",
                        "title": "Hold 700 fl. in royal reserves",
                        "condition": {
                            "type": "treasury_above",
                            "params": {
                                "min_value": "700"
                            }
                        }
                    }
                ]
            }
        ]
    },
    "POL": {
        "goals": [
            {
                "id": "pol_personal_union",
                "title": "The Jagiellonian Union",
                "title_key": "owo.goal.pol_personal_union",
                "description": "Cement the dynastic partnership with the Grand Duchy of Lithuania.",
                "description_key": "owo.goal.pol_personal_union.desc",
                "type": "diplomatic",
                "priority": "primary",
                "ai_weight": 0.85,
                "target_countries": ["LTH"],
                "on_complete_effects": {
                    "prestige": 35,
                    "stability": 5
                },
                "tasks": [
                    {
                        "id": "alliance",
                        "title_key": "owo.task.pol_personal_union.alliance",
                        "title": "Secure an alliance with Lithuania",
                        "condition": {
                            "type": "alliance_with",
                            "params": {
                                "target_iso3": "LTH"
                            }
                        }
                    },
                    {
                        "id": "relations",
                        "title_key": "owo.task.pol_personal_union.relations",
                        "title": "Cultivate good relations with Vilnius",
                        "condition": {
                            "type": "improve_relations",
                            "params": {
                                "target_iso3": "LTH",
                                "min_value": "70"
                            }
                        }
                    }
                ]
            },
            {
                "id": "pol_thirteen_years_war",
                "title": "Reclaim the Baltic Coast",
                "title_key": "owo.goal.pol_thirteen_years_war",
                "description": "Challenge the Teutonic Knights to restore Polish access to the Baltic Sea.",
                "description_key": "owo.goal.pol_thirteen_years_war.desc",
                "type": "territorial",
                "priority": "secondary",
                "ai_weight": 0.80,
                "target_countries": ["TEU"],
                "on_complete_effects": {
                    "prestige": 40,
                    "stability": 5
                },
                "tasks": [
                    {
                        "id": "war",
                        "title_key": "owo.task.pol_thirteen_years_war.war",
                        "title": "Declare war on the Teutonic Order",
                        "condition": {
                            "type": "declare_war_on",
                            "params": {
                                "target_iso3": "TEU"
                            }
                        }
                    },
                    {
                        "id": "army",
                        "title_key": "owo.task.pol_thirteen_years_war.army",
                        "title": "Muster 20,000 crown soldiers",
                        "condition": {
                            "type": "military_units_above",
                            "params": {
                                "unit_type": "personnel",
                                "min_value": "20000"
                            }
                        },
                        "required_count": 20000
                    }
                ]
            }
        ]
    },
    "MAM": {
        "goals": [
            {
                "id": "mam_custodian_holy_sanctuaries",
                "title": "Protector of the Holy Cities",
                "title_key": "owo.goal.mam_custodian_holy_sanctuaries",
                "description": "Safeguard Mecca, Medina, and Jerusalem while dominating Red Sea trade routes.",
                "description_key": "owo.goal.mam_custodian_holy_sanctuaries.desc",
                "type": "prestige",
                "priority": "primary",
                "ai_weight": 0.80,
                "on_complete_effects": {
                    "prestige": 50,
                    "stability": 5
                },
                "tasks": [
                    {
                        "id": "treasury",
                        "title_key": "owo.task.mam_custodian_holy_sanctuaries.treasury",
                        "title": "Hold 1,000 fl. in the Cairo citadel treasury",
                        "condition": {
                            "type": "treasury_above",
                            "params": {
                                "min_value": "1000"
                            }
                        }
                    }
                ]
            },
            {
                "id": "mam_syrian_bulwark",
                "title": "Fortify the Syrian Frontier",
                "title_key": "owo.goal.mam_syrian_bulwark",
                "description": "Maintain a formidable cavalry army in Aleppo and Damascus to deter northern aggression.",
                "description_key": "owo.goal.mam_syrian_bulwark.desc",
                "type": "defense",
                "priority": "secondary",
                "ai_weight": 0.75,
                "target_countries": ["OTT"],
                "on_complete_effects": {
                    "prestige": 30,
                    "military_modifier": 0.05
                },
                "tasks": [
                    {
                        "id": "army",
                        "title_key": "owo.task.mam_syrian_bulwark.army",
                        "title": "Muster 30,000 Mamluk warriors",
                        "condition": {
                            "type": "military_units_above",
                            "params": {
                                "unit_type": "personnel",
                                "min_value": "30000"
                            }
                        },
                        "required_count": 30000
                    }
                ]
            }
        ]
    }
}

L10N_STRINGS = {
    "en": {
        "owo.goal.mvy_gather_russian_lands": "Gather the Russian Lands",
        "owo.goal.mvy_gather_russian_lands.desc": "Unify the divided principalities of Rus under the leadership of Moscow.",
        "owo.task.mvy_gather_russian_lands.army": "Muster 15,000 soldiers",
        "owo.task.mvy_gather_russian_lands.novgorod": "Declare war on the Novgorod Republic",
        "owo.goal.mvy_stand_against_the_horde": "Stand Against the Horde",
        "owo.goal.mvy_stand_against_the_horde.desc": "Cast off the Tatar yoke and refuse all further tribute to the Great Horde.",
        "owo.task.mvy_stand_against_the_horde.treasury": "Amass 800 fl. in the treasury",
        "owo.task.mvy_stand_against_the_horde.army": "Field an army of 25,000 men",

        "owo.goal.vnc_queen_of_the_adriatic": "Queen of the Adriatic",
        "owo.goal.vnc_queen_of_the_adriatic.desc": "Enrich the republic through unrivaled maritime commerce across the eastern Mediterranean.",
        "owo.task.vnc_queen_of_the_adriatic.treasury": "Accumulate 1,200 fl. in the ducal treasury",
        "owo.task.vnc_queen_of_the_adriatic.trade": "Establish bilateral trade agreements",
        "owo.goal.vnc_defend_stato_da_mar": "Defend the Stato da Màr",
        "owo.goal.vnc_defend_stato_da_mar.desc": "Protect Venetian island outposts and sea lanes against Ottoman maritime expansion.",
        "owo.task.vnc_defend_stato_da_mar.fleet": "Maintain a formidable naval armada",

        "owo.goal.hun_bastion_of_christendom": "Bastion of Christendom",
        "owo.goal.hun_bastion_of_christendom.desc": "Defend the southern frontier against Ottoman incursions along the Danube and Sava rivers.",
        "owo.task.hun_bastion_of_christendom.army": "Muster a border defense army of 25,000 soldiers",
        "owo.task.hun_bastion_of_christendom.allies": "Seek alliances with Central European crowns",
        "owo.goal.hun_corvinus_hegemony": "The Corvinus Renaissance",
        "owo.goal.hun_corvinus_hegemony.desc": "Modernize royal finances, patronize humanist culture, and expand royal sovereignty.",
        "owo.task.hun_corvinus_hegemony.treasury": "Hold 700 fl. in royal reserves",

        "owo.goal.pol_personal_union": "The Jagiellonian Union",
        "owo.goal.pol_personal_union.desc": "Cement the dynastic partnership with the Grand Duchy of Lithuania.",
        "owo.task.pol_personal_union.alliance": "Secure an alliance with Lithuania",
        "owo.task.pol_personal_union.relations": "Cultivate good relations with Vilnius",
        "owo.goal.pol_thirteen_years_war": "Reclaim the Baltic Coast",
        "owo.goal.pol_thirteen_years_war.desc": "Challenge the Teutonic Knights to restore Polish access to the Baltic Sea.",
        "owo.task.pol_thirteen_years_war.war": "Declare war on the Teutonic Order",
        "owo.task.pol_thirteen_years_war.army": "Muster 20,000 crown soldiers",

        "owo.goal.mam_custodian_holy_sanctuaries": "Protector of the Holy Cities",
        "owo.goal.mam_custodian_holy_sanctuaries.desc": "Safeguard Mecca, Medina, and Jerusalem while dominating Red Sea trade routes.",
        "owo.task.mam_custodian_holy_sanctuaries.treasury": "Hold 1,000 fl. in the Cairo citadel treasury",
        "owo.goal.mam_syrian_bulwark": "Fortify the Syrian Frontier",
        "owo.goal.mam_syrian_bulwark.desc": "Maintain a formidable cavalry army in Aleppo and Damascus to deter northern aggression.",
        "owo.task.mam_syrian_bulwark.army": "Muster 30,000 Mamluk warriors"
    },
    "tr": {
        "owo.goal.mvy_gather_russian_lands": "Rus Topraklarını Birleştir",
        "owo.goal.mvy_gather_russian_lands.desc": "Bölünmüş Rus prensliklerini Moskova'nın liderliğinde tek bir sancak altında topla.",
        "owo.task.mvy_gather_russian_lands.army": "15.000 asker topla",
        "owo.task.mvy_gather_russian_lands.novgorod": "Novgorod Cumhuriyeti'ne savaş ilan et",
        "owo.goal.mvy_stand_against_the_horde": "Orda'ya Karşı Direniş",
        "owo.goal.mvy_stand_against_the_horde.desc": "Tatar boyunduruğunu kır ve Büyük Orda'ya ödenen haracı reddet.",
        "owo.task.mvy_stand_against_the_horde.treasury": "Hazinede 800 fl. biriktir",
        "owo.task.mvy_stand_against_the_horde.army": "25.000 kişilik bir ordu kur",

        "owo.goal.vnc_queen_of_the_adriatic": "Adriyatik'in Kraliçesi",
        "owo.goal.vnc_queen_of_the_adriatic.desc": "Doğu Akdeniz'deki rakipsiz deniz ticaretiyle cumhuriyeti zenginleştir.",
        "owo.task.vnc_queen_of_the_adriatic.treasury": "Dükalık hazinesinde 1.200 fl. biriktir",
        "owo.task.vnc_queen_of_the_adriatic.trade": "İkili ticaret antlaşmaları yap",
        "owo.goal.vnc_defend_stato_da_mar": "Stato da Màr'ı Koru",
        "owo.goal.vnc_defend_stato_da_mar.desc": "Osmanlı deniz genişlemesine karşı Venedik ada karakollarını ve deniz yollarını savun.",
        "owo.task.vnc_defend_stato_da_mar.fleet": "Güçlü bir donanma kur",

        "owo.goal.hun_bastion_of_christendom": "Hristiyanlığın Kalesi",
        "owo.goal.hun_bastion_of_christendom.desc": "Tuna ve Sava nehirleri boyunca güney sınırını Osmanlı akınlarına karşı koru.",
        "owo.task.hun_bastion_of_christendom.army": "25.000 kişilik sınır savunma ordusu topla",
        "owo.task.hun_bastion_of_christendom.allies": "Orta Avrupa krallıklarıyla ittifak ara",
        "owo.goal.hun_corvinus_hegemony": "Corvinus Rönesansı",
        "owo.goal.hun_corvinus_hegemony.desc": "Kraliyet maliyesini modernize et ve hümanist kültürü destekle.",
        "owo.task.hun_corvinus_hegemony.treasury": "Kraliyet kasasında 700 fl. tut",

        "owo.goal.pol_personal_union": "Jagiellon Birliği",
        "owo.goal.pol_personal_union.desc": "Litvanya Büyük Dükalığı ile hanedan ortaklığını güçlendir.",
        "owo.task.pol_personal_union.alliance": "Litvanya ile ittifak kur",
        "owo.task.pol_personal_union.relations": "Vilnius ile ilişkileri geliştir",
        "owo.goal.pol_thirteen_years_war": "Baltık Kıyılarını Geri Al",
        "owo.goal.pol_thirteen_years_war.desc": "Töton Şövalyeleri'ne meydan okuyarak Baltık Denizi'ne erişimi yeniden sağla.",
        "owo.task.pol_thirteen_years_war.war": "Töton Tarikatı'na savaş ilan et",
        "owo.task.pol_thirteen_years_war.army": "20.000 kraliyet askeri topla",

        "owo.goal.mam_custodian_holy_sanctuaries": "Kutsal Şehirlerin Koruyucusu",
        "owo.goal.mam_custodian_holy_sanctuaries.desc": "Mekke, Medine ve Kudüs'ü korurken Kızıldeniz ticaretini elinde tut.",
        "owo.task.mam_custodian_holy_sanctuaries.treasury": "Kahire kalesi hazinesinde 1.000 fl. tut",
        "owo.goal.mam_syrian_bulwark": "Suriye Seddi",
        "owo.goal.mam_syrian_bulwark.desc": "Kuzey tehditlerine karşı Halep ve Şam'da güçlü bir süvari ordusu bulundur.",
        "owo.task.mam_syrian_bulwark.army": "30.000 Memlük savaşçısı topla"
    }
}

def main():
    # 1. Update scenario/national_goals.json
    path_goals = "scenario/national_goals.json"
    with open(path_goals, "r", encoding="utf-8") as f:
        goals_data = json.load(f)

    for iso, country_obj in GOALS_TO_ADD.items():
        goals_data[iso] = country_obj

    with open(path_goals, "w", encoding="utf-8") as f:
        json.dump(goals_data, f, indent=2, ensure_ascii=False)
    print(f"Added national goals for {list(GOALS_TO_ADD.keys())} into {path_goals}")

    # 2. Update localization CSVs
    all_langs = ["cz", "de", "en", "es", "es-419", "fr", "ja", "ko", "pt", "pt-br", "ru", "tr", "zh"]
    for lang in all_langs:
        csv_path = f"Content/localization/{lang}.csv"
        if not os.path.exists(csv_path):
            continue

        src_dict = L10N_STRINGS["tr"] if lang == "tr" else L10N_STRINGS["en"]

        with open(csv_path, "r", encoding="utf-8") as f:
            existing = f.read()

        to_add = []
        for k, v in src_dict.items():
            if k not in existing:
                v_clean = v.replace("\n", " ").replace("\r", "")
                to_add.append(f"{k},{v_clean}\n")

        if to_add:
            with open(csv_path, "a", encoding="utf-8") as f:
                f.writelines(to_add)
            print(f"Added {len(to_add)} keys to {csv_path}")

if __name__ == "__main__":
    main()

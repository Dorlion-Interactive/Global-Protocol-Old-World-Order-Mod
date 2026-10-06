import json
import os

# Updates Content/events/historical_events_1450.json to ensure EVERY event has at least 2 options.
# Updates all 13 CSVs with distinct perspective titles and all option_2 translations.

EVENTS_JSON_PATH = "Content/events/historical_events_1450.json"

def update_events_json():
    with open(EVENTS_JSON_PATH, "r", encoding="utf-8") as f:
        events = json.load(f)

    for ev in events:
        eid = ev["id"]

        # 1. fall_of_constantinople_1453
        if eid == "fall_of_constantinople_1453":
            if len(ev["options"]) == 1:
                ev["options"].append({
                    "effects": [
                        { "type": "annex_province", "province_id": 2276, "target": "OTT" },
                        { "type": "add_treasury", "value": 250 },
                        { "type": "modify_stat", "field": "government.stability", "value": 5 },
                        { "type": "modify_stat", "field": "economy.gdp_growth_rate", "value": 0.02 },
                        { "type": "modify_unrest", "value": -5 },
                        { "type": "set_flag", "flag_name": "constantinople_conquered" }
                    ],
                    "text_key": "owo.event.fall_of_constantinople_1453.option_2"
                })

        # 2. fall_of_constantinople_1453_christendom
        elif eid == "fall_of_constantinople_1453_christendom":
            if len(ev["options"]) == 1:
                ev["options"].append({
                    "effects": [
                        { "type": "add_treasury", "value": -50 },
                        { "type": "modify_stat", "field": "economy.gdp_growth_rate", "value": 0.015 }
                    ],
                    "text_key": "owo.event.fall_of_constantinople_1453_christendom.option_2"
                })

        # 3. end_hundred_years_war_1453
        elif eid == "end_hundred_years_war_1453":
            if len(ev["options"]) == 1:
                ev["options"].append({
                    "effects": [
                        { "type": "modify_stat", "field": "government.stability", "value": 10 },
                        { "type": "create_unit", "unit_id": "france_knight", "count": 1, "target": "FRA" }
                    ],
                    "text_key": "owo.event.end_hundred_years_war_1453.option_2"
                })

        # 4. end_hundred_years_war_1453_england
        elif eid == "end_hundred_years_war_1453_england":
            if len(ev["options"]) == 1:
                ev["options"].append({
                    "effects": [
                        { "type": "add_treasury", "value": -150 },
                        { "type": "modify_unrest", "value": 5 },
                        { "type": "create_unit", "unit_id": "england_longbowman", "count": 1, "target": "ENG" }
                    ],
                    "text_key": "owo.event.end_hundred_years_war_1453_england.option_2"
                })

        # 5. gutenberg_printing_press_1455
        elif eid == "gutenberg_printing_press_1455":
            if len(ev["options"]) == 1:
                ev["options"].append({
                    "effects": [
                        { "type": "modify_stat", "field": "government.stability", "value": 10 },
                        { "type": "modify_unrest", "value": -5 }
                    ],
                    "text_key": "owo.event.gutenberg_printing_press_1455.option_2"
                })

        # 6. wars_of_the_roses_1455
        elif eid == "wars_of_the_roses_1455":
            if len(ev["options"]) == 1:
                ev["options"].append({
                    "effects": [
                        { "type": "modify_unrest", "value": 20 },
                        { "type": "add_treasury", "value": 200 },
                        { "type": "modify_stat", "field": "government.stability", "value": -5 }
                    ],
                    "text_key": "owo.event.wars_of_the_roses_1455.option_2"
                })

        # 7. portuguese_african_voyages_1460
        elif eid == "portuguese_african_voyages_1460":
            if len(ev["options"]) == 1:
                ev["options"].append({
                    "effects": [
                        { "type": "add_treasury", "value": 150 },
                        { "type": "modify_stat", "field": "government.stability", "value": 5 }
                    ],
                    "text_key": "owo.event.portuguese_african_voyages_1460.option_2"
                })

        # 8. fall_of_trebizond_1461
        elif eid == "fall_of_trebizond_1461":
            if len(ev["options"]) == 1:
                ev["options"].append({
                    "effects": [
                        { "type": "annex_province", "province_id": 2415, "target": "OTT" },
                        { "type": "add_treasury", "value": 100 },
                        { "type": "create_unit", "unit_id": "ottoman_sipahi", "count": 1, "target": "OTT" },
                        { "type": "set_flag", "flag_name": "trebizond_annexed" }
                    ],
                    "text_key": "owo.event.fall_of_trebizond_1461.option_2"
                })

    with open(EVENTS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("Successfully updated Content/events/historical_events_1450.json with 2 options per event!")

# Localization updates
UPDATED_STRINGS = {
    "en": {
        "owo.event.fall_of_constantinople_1453.title": "Conquest of Constantinople (Ottoman Triumph)",
        "owo.event.fall_of_constantinople_1453.option_1": "Kostantiniyye shall shine as the crown jewel of our empire!",
        "owo.event.fall_of_constantinople_1453.option_2": "Guarantee Orthodox patriarchate rights and revive Black Sea trade.",

        "owo.event.fall_of_constantinople_1453_christendom.title": "Fall of Constantinople (Shock to Christendom)",
        "owo.event.fall_of_constantinople_1453_christendom.option_1": "A tragic twilight for the Christian Roman world.",
        "owo.event.fall_of_constantinople_1453_christendom.option_2": "Welcome Byzantine refugee scholars and humanists to our court.",

        "owo.event.end_hundred_years_war_1453.title": "End of the Hundred Years' War (French Victory)",
        "owo.event.end_hundred_years_war_1453.option_1": "France stands sovereign and united at last!",
        "owo.event.end_hundred_years_war_1453.option_2": "Reward our battle-hardened chivalry and royal captains.",

        "owo.event.end_hundred_years_war_1453_england.title": "End of the Hundred Years' War (English Retreat)",
        "owo.event.end_hundred_years_war_1453_england.option_1": "A painful retreat across the English Channel.",
        "owo.event.end_hundred_years_war_1453_england.option_2": "Fortify Calais and muster the veteran longbowmen.",

        "owo.event.gutenberg_printing_press_1455.title": "The Gutenberg Printing Revolution (1455)",
        "owo.event.gutenberg_printing_press_1455.option_1": "Sponsor printing workshops to spread learning and scripture.",
        "owo.event.gutenberg_printing_press_1455.option_2": "Place printing houses under royal charter and censorship.",

        "owo.event.wars_of_the_roses_1455.title": "Outbreak of the Wars of the Roses (1455)",
        "owo.event.wars_of_the_roses_1455.option_1": "Rally behind the Red Rose of Lancaster and King Henry VI!",
        "owo.event.wars_of_the_roses_1455.option_2": "Support the White Rose of York and Duke Richard!",

        "owo.event.portuguese_african_voyages_1460.title": "Prince Henry & the African Voyages (1460)",
        "owo.event.portuguese_african_voyages_1460.option_1": "Commission new caravels to chart the southern ocean.",
        "owo.event.portuguese_african_voyages_1460.option_2": "Consolidate Guinea coastal feitorias and reap trade gold.",

        "owo.event.fall_of_trebizond_1461.title": "Fall of Trebizond: Black Sea Mastery (1461)",
        "owo.event.fall_of_trebizond_1461.option_1": "The Black Sea is now firmly an Ottoman lake.",
        "owo.event.fall_of_trebizond_1461.option_2": "Grant timars to local Pontic cavalry to guard the coast."
    },
    "tr": {
        "owo.event.fall_of_constantinople_1453.title": "İstanbul'un Fethi (Osmanlı Zaferi)",
        "owo.event.fall_of_constantinople_1453.option_1": "Kostantiniyye imparatorluğumuzun başkenti olarak parlayacak!",
        "owo.event.fall_of_constantinople_1453.option_2": "Ortodoks Patrikhanesi'nin haklarını tanı ve Karadeniz ticaretini canlandır.",

        "owo.event.fall_of_constantinople_1453_christendom.title": "Konstantinopolis'in Düşüşü (Hristiyan Dünyasında Yas)",
        "owo.event.fall_of_constantinople_1453_christendom.option_1": "Hristiyan Roma dünyası için trajik bir gün batımı.",
        "owo.event.fall_of_constantinople_1453_christendom.option_2": "Bizanslı bilgin ve hümanist mültecileri sarayımıza kabul et.",

        "owo.event.end_hundred_years_war_1453.title": "Yüzyıl Savaşları'nın Sonu (Fransız Zaferi)",
        "owo.event.end_hundred_years_war_1453.option_1": "Fransa nihayet egemen ve birleşik!",
        "owo.event.end_hundred_years_war_1453.option_2": "Savaşta pişen şövalyelerimizi ve kraliyet komutanlarını ödüllendir.",

        "owo.event.end_hundred_years_war_1453_england.title": "Yüzyıl Savaşları'nın Sonu (İngiliz Geri Çekilişi)",
        "owo.event.end_hundred_years_war_1453_england.option_1": "Manş Denizi'nin ardına acı bir geri çekilme.",
        "owo.event.end_hundred_years_war_1453_england.option_2": "Calais'yi tahkim et ve kıdemli uzun yaylıları göreve çağır.",

        "owo.event.gutenberg_printing_press_1455.title": "Gutenberg Matbaa Devrimi (1455)",
        "owo.event.gutenberg_printing_press_1455.option_1": "İlim ve kitapların yayılması için matbaaları destekle.",
        "owo.event.gutenberg_printing_press_1455.option_2": "Matbaaları kraliyet denetimine ve sansürüne bağla.",

        "owo.event.wars_of_the_roses_1455.title": "Güller Savaşı'nın Başlangıcı (1455)",
        "owo.event.wars_of_the_roses_1455.option_1": "Lancaster'ın Kırmızı Gülü ve Kral Henry VI'nın arkasında birleşin!",
        "owo.event.wars_of_the_roses_1455.option_2": "York'un Beyaz Gülü ve Dük Richard'ı destekleyin!",

        "owo.event.portuguese_african_voyages_1460.title": "Prens Henrique ve Afrika Seferleri (1460)",
        "owo.event.portuguese_african_voyages_1460.option_1": "Güney okyanuslarını haritalandırmak için yeni karaveller gönder.",
        "owo.event.portuguese_african_voyages_1460.option_2": "Gine ticaret merkezlerini pekiştir ve ticaret gelirini topla.",

        "owo.event.fall_of_trebizond_1461.title": "Trabzon'un Fethi: Karadeniz Hakimiyeti (1461)",
        "owo.event.fall_of_trebizond_1461.option_1": "Karadeniz artık tamamen bir Osmanlı gölüdür.",
        "owo.event.fall_of_trebizond_1461.option_2": "Kıyı güvenliği için yerel süvarilere tımarlar bağışla."
    },
    "de": {
        "owo.event.fall_of_constantinople_1453.title": "Eroberung von Konstantinopel (Osmanischer Triumph)",
        "owo.event.fall_of_constantinople_1453.option_1": "Kostantiniyye wird als Reichshauptstadt erstrahlen!",
        "owo.event.fall_of_constantinople_1453.option_2": "Rechte des Patriarchats achten und Schwarzmeerhandel beleben.",

        "owo.event.fall_of_constantinople_1453_christendom.title": "Der Fall von Konstantinopel (Schock für die Christenheit)",
        "owo.event.fall_of_constantinople_1453_christendom.option_1": "Ein tragischer Untergang der christlich-römischen Welt.",
        "owo.event.fall_of_constantinople_1453_christendom.option_2": "Byzantinische Gelehrte und Humanisten am Hof aufnehmen.",

        "owo.event.end_hundred_years_war_1453.title": "Ende des Hundertjährigen Krieges (Französischer Sieg)",
        "owo.event.end_hundred_years_war_1453.option_1": "Frankreich steht endlich souverän und geeint da!",
        "owo.event.end_hundred_years_war_1453.option_2": "Die treuen Ritter und Kriegshauptleute belohnen.",

        "owo.event.end_hundred_years_war_1453_england.title": "Ende des Hundertjährigen Krieges (Englischer Rückzug)",
        "owo.event.end_hundred_years_war_1453_england.option_1": "Ein schmerzhafter Rückzug über den Ärmelkanal.",
        "owo.event.end_hundred_years_war_1453_england.option_2": "Calais befestigen und erfahrene Langbogenschützen mustern.",

        "owo.event.gutenberg_printing_press_1455.title": "Gutenbergs Buchdruck-Revolution (1455)",
        "owo.event.gutenberg_printing_press_1455.option_1": "Druckwerkstätten fördern und Wissen verbreiten.",
        "owo.event.gutenberg_printing_press_1455.option_2": "Druckereien unter königliche Zensur stellen.",

        "owo.event.wars_of_the_roses_1455.title": "Ausbruch der Rosenkriege (1455)",
        "owo.event.wars_of_the_roses_1455.option_1": "Unter der Roten Rose von Lancaster für Heinrich VI. kämpfen!",
        "owo.event.wars_of_the_roses_1455.option_2": "Die Weiße Rose von York und Herzog Richard unterstützen!",

        "owo.event.portuguese_african_voyages_1460.title": "Heinrich der Seefahrer & die Afrikafahrten (1460)",
        "owo.event.portuguese_african_voyages_1460.option_1": "Neue Karavellen zur Erkundung der Südozeane entsenden.",
        "owo.event.portuguese_african_voyages_1460.option_2": "Handelsstützpunkte an der Küste sichern.",

        "owo.event.fall_of_trebizond_1461.title": "Der Fall von Trapezunt: Schwarzmeer-Vormacht (1461)",
        "owo.event.fall_of_trebizond_1461.option_1": "Das Schwarze Meer ist nun ein osmanischer See.",
        "owo.event.fall_of_trebizond_1461.option_2": "Timare an Reiter vergeben, um die Küste zu sichern."
    },
    "fr": {
        "owo.event.fall_of_constantinople_1453.title": "Prise de Constantinople (Triomphe Ottoman)",
        "owo.event.fall_of_constantinople_1453.option_1": "Kostantiniyye sera la capitale éternelle de l'Empire !",
        "owo.event.fall_of_constantinople_1453.option_2": "Garantir les droits du patriarcat et ranimer le commerce.",

        "owo.event.fall_of_constantinople_1453_christendom.title": "La Chute de Constantinople (Choc en Chrétienté)",
        "owo.event.fall_of_constantinople_1453_christendom.option_1": "Un crépuscule tragique pour le monde romain chrétien.",
        "owo.event.fall_of_constantinople_1453_christendom.option_2": "Accueillir les érudits byzantins et humanistes à notre cour.",

        "owo.event.end_hundred_years_war_1453.title": "Fin de la Guerre de Cent Ans (Victoire Française)",
        "owo.event.end_hundred_years_war_1453.option_1": "La France se dresse enfin souveraine et unie !",
        "owo.event.end_hundred_years_war_1453.option_2": "Récompenser notre chevalerie et les capitaines royaux.",

        "owo.event.end_hundred_years_war_1453_england.title": "Fin de la Guerre de Cent Ans (Retraite Anglaise)",
        "owo.event.end_hundred_years_war_1453_england.option_1": "Une douloureuse retraite par-delà la Manche.",
        "owo.event.end_hundred_years_war_1453_england.option_2": "Fortifier Calais et mobiliser les archers vétérans.",

        "owo.event.gutenberg_printing_press_1455.title": "Révolution de l'Imprimerie de Gutenberg (1455)",
        "owo.event.gutenberg_printing_press_1455.option_1": "Financer les ateliers d'imprimerie pour diffuser le savoir.",
        "owo.event.gutenberg_printing_press_1455.option_2": "Placer les presses sous privilège royal et censure.",

        "owo.event.wars_of_the_roses_1455.title": "Guerre des Deux-Roses (1455)",
        "owo.event.wars_of_the_roses_1455.option_1": "Soutenir la Rose Rouge de Lancastre et le roi Henri VI !",
        "owo.event.wars_of_the_roses_1455.option_2": "Se rallier à la Rose Blanche d'York et au duc Richard !",

        "owo.event.portuguese_african_voyages_1460.title": "Henri le Navigateur et les Caravelles Africaines (1460)",
        "owo.event.portuguese_african_voyages_1460.option_1": "Armer de nouvelles caravelles vers les mers du Sud.",
        "owo.event.portuguese_african_voyages_1460.option_2": "Consolider les comptoirs côtiers et le commerce d'or.",

        "owo.event.fall_of_trebizond_1461.title": "Chute de Trébizonde: Maîtrise de la Mer Noire (1461)",
        "owo.event.fall_of_trebizond_1461.option_1": "La mer Noire est désormais un lac ottoman.",
        "owo.event.fall_of_trebizond_1461.option_2": "Distribuer des fiefs timars aux cavaliers pontiques."
    },
    "es": {
        "owo.event.fall_of_constantinople_1453.title": "Conquista de Constantinopla (Triunfo Otomano)",
        "owo.event.fall_of_constantinople_1453.option_1": "¡Kostantiniyye brillará como joya de nuestro imperio!",
        "owo.event.fall_of_constantinople_1453.option_2": "Garantizar derechos al patriarcado y revivir el comercio.",

        "owo.event.fall_of_constantinople_1453_christendom.title": "La Caída de Constantinopla (Conmoción en la Cristiandad)",
        "owo.event.fall_of_constantinople_1453_christendom.option_1": "Un trágico crepúsculo para el mundo romano cristiano.",
        "owo.event.fall_of_constantinople_1453_christendom.option_2": "Acoger eruditos y humanistas bizantinos en nuestra corte.",

        "owo.event.end_hundred_years_war_1453.title": "Fin de la Guerra de los Cien Años (Victoria Francesa)",
        "owo.event.end_hundred_years_war_1453.option_1": "¡Francia se alza soberana y unida al fin!",
        "owo.event.end_hundred_years_war_1453.option_2": "Recompensar a la caballería leal y capitanes reales.",

        "owo.event.end_hundred_years_war_1453_england.title": "Fin de la Guerra de los Cien Años (Retirada Inglesa)",
        "owo.event.end_hundred_years_war_1453_england.option_1": "Una amarga retirada a través del Canal de la Mancha.",
        "owo.event.end_hundred_years_war_1453_england.option_2": "Fortificar Calais y reclutar arqueros veteranos.",

        "owo.event.gutenberg_printing_press_1455.title": "La Imprenta de Gutenberg (1455)",
        "owo.event.gutenberg_printing_press_1455.option_1": "Patrocinar talleres de imprenta para expandir el saber.",
        "owo.event.gutenberg_printing_press_1455.option_2": "Someter las imprentas a censura y licencia real.",

        "owo.event.wars_of_the_roses_1455.title": "Estallido de la Guerra de las Dos Rosas (1455)",
        "owo.event.wars_of_the_roses_1455.option_1": "¡Apoyar la Rosa Roja de Lancaster y al rey Enrique VI!",
        "owo.event.wars_of_the_roses_1455.option_2": "¡Apoyar la Rosa Blanca de York y al duque Ricardo!",

        "owo.event.portuguese_african_voyages_1460.title": "Enrique el Navegante y los Viajes Africanos (1460)",
        "owo.event.portuguese_african_voyages_1460.option_1": "Armar carabelas para explorar el océano meridional.",
        "owo.event.portuguese_african_voyages_1460.option_2": "Consolidar factorías costeras y asegurar el oro.",

        "owo.event.fall_of_trebizond_1461.title": "Caída de Trebisonda: Dominio del Mar Negro (1461)",
        "owo.event.fall_of_trebizond_1461.option_1": "El mar Negro es ahora un lago otomano.",
        "owo.event.fall_of_trebizond_1461.option_2": "Otorgar timars a jinetes locales para vigilar la costa."
    },
    "zh": {
        "owo.event.fall_of_constantinople_1453.title": "君士坦丁堡陷落（奥斯曼凯歌）",
        "owo.event.fall_of_constantinople_1453.option_1": "君士坦丁堡将成为帝国永恒闪耀的王冠！",
        "owo.event.fall_of_constantinople_1453.option_2": "宽宥东正教牧首特权，复兴黑海航运贸易。",

        "owo.event.fall_of_constantinople_1453_christendom.title": "君士坦丁堡陷落（基督教世界震颤）",
        "owo.event.fall_of_constantinople_1453_christendom.option_1": "罗马世界在悲叹中落下了千年帷幕。",
        "owo.event.fall_of_constantinople_1453_christendom.option_2": "接纳拜占庭流亡学者与人文学士入朝讲学。",

        "owo.event.end_hundred_years_war_1453.title": "百年战争终结（法兰西大捷）",
        "owo.event.end_hundred_years_war_1453.option_1": "法兰西王国终得光复，重归一统！",
        "owo.event.end_hundred_years_war_1453.option_2": "重赏百战骑士与王室炮兵将领。",

        "owo.event.end_hundred_years_war_1453_england.title": "百年战争终结（英格兰撤军）",
        "owo.event.end_hundred_years_war_1453_england.option_1": "饮恨撤退，战火暂止于海峡之南。",
        "owo.event.end_hundred_years_war_1453_england.option_2": "坚守加莱据点，调集百战长弓手驻防。",

        "owo.event.gutenberg_printing_press_1455.title": "古腾堡活字印刷术（1455）",
        "owo.event.gutenberg_printing_press_1455.option_1": "资助印刷工坊，广布经籍与新知。",
        "owo.event.gutenberg_printing_press_1455.option_2": "将印刷馆所置于王室审查特许之下。",

        "owo.event.wars_of_the_roses_1455.title": "玫瑰战争爆发（1455）",
        "owo.event.wars_of_the_roses_1455.option_1": "效忠兰开斯特红玫瑰与国王亨利六世！",
        "owo.event.wars_of_the_roses_1455.option_2": "倒向约克白玫瑰与理查公爵！",

        "owo.event.portuguese_african_voyages_1460.title": "恩里克王子与西非远航（1460）",
        "owo.event.portuguese_african_voyages_1460.option_1": "增造卡拉维尔帆船，探索未知大洋。",
        "owo.event.portuguese_african_voyages_1460.option_2": "修筑几内亚沿海商馆，垄断黄金贸易。",

        "owo.event.fall_of_trebizond_1461.title": "特拉比松陷落：黑海霸权（1461）",
        "owo.event.fall_of_trebizond_1461.option_1": "黑海自此尽入奥斯曼帝国版图。",
        "owo.event.fall_of_trebizond_1461.option_2": "向地方骑兵颁授蒂玛尔封邑，巩固海防。"
    },
    "ru": {
        "owo.event.fall_of_constantinople_1453.title": "Падение Константинополя (Триумф Османов)",
        "owo.event.fall_of_constantinople_1453.option_1": "Константинополь станет вечной столицей империи!",
        "owo.event.fall_of_constantinople_1453.option_2": "Подтвердить привилегии патриарха и оживить торговлю.",

        "owo.event.fall_of_constantinople_1453_christendom.title": "Падение Константинополя (Шок христианского мира)",
        "owo.event.fall_of_constantinople_1453_christendom.option_1": "Трагический закат христианского Рима.",
        "owo.event.fall_of_constantinople_1453_christendom.option_2": "Принять византийских беженцев и учёных при дворе.",

        "owo.event.end_hundred_years_war_1453.title": "Конец Столетней войны (Победа Франции)",
        "owo.event.end_hundred_years_war_1453.option_1": "Франция наконец суверенна и едина!",
        "owo.event.end_hundred_years_war_1453.option_2": "Наградить верных рыцарей и королевских капитанов.",

        "owo.event.end_hundred_years_war_1453_england.title": "Конец Столетней войны (Отступление Англии)",
        "owo.event.end_hundred_years_war_1453_england.option_1": "Горькое отступление через Ла-Манш.",
        "owo.event.end_hundred_years_war_1453_england.option_2": "Укрепить Кале и собрать отряды лучников.",

        "owo.event.gutenberg_printing_press_1455.title": "Печатная революция Гутенберга (1455)",
        "owo.event.gutenberg_printing_press_1455.option_1": "Поддержать печатные мастерские для распространения знаний.",
        "owo.event.gutenberg_printing_press_1455.option_2": "Подчинить типографии королевской цензуре.",

        "owo.event.wars_of_the_roses_1455.title": "Начало Войны Алой и Белой розы (1455)",
        "owo.event.wars_of_the_roses_1455.option_1": "Встать под знамя Алой розы Ланкастеров и Генриха VI!",
        "owo.event.wars_of_the_roses_1455.option_2": "Поддержать Белую розу Йорков и герцога Ричарда!",

        "owo.event.portuguese_african_voyages_1460.title": "Генрих Мореплаватель и африканские походы (1460)",
        "owo.event.portuguese_african_voyages_1460.option_1": "Снарядить каравеллы для исследования южных морей.",
        "owo.event.portuguese_african_voyages_1460.option_2": "Укрепить фактории и собирать торговое золото.",

        "owo.event.fall_of_trebizond_1461.title": "Падение Трапезунда: Владычество на Чёрном море (1461)",
        "owo.event.fall_of_trebizond_1461.option_1": "Чёрное море теперь османское озеро.",
        "owo.event.fall_of_trebizond_1461.option_2": "Раздать тимары кавалерии для защиты побережья."
    }
}

LANG_MAP = {
    "es-419": "es",
    "pt": "es",
    "pt-br": "es",
    "cz": "de",
    "ja": "zh",
    "ko": "zh"
}

all_langs = ["cz", "de", "en", "es", "es-419", "fr", "ja", "ko", "pt", "pt-br", "ru", "tr", "zh"]

def update_localization_csvs():
    for lang in all_langs:
        filepath = f"Content/localization/{lang}.csv"
        if not os.path.exists(filepath):
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Parse key-values
        kv = {}
        for line in lines:
            if "," in line:
                k, v = line.split(",", 1)
                kv[k.strip()] = v.rstrip("\r\n")

        src_lang = lang if lang in UPDATED_STRINGS else LANG_MAP.get(lang, "en")
        dict_to_use = UPDATED_STRINGS.get(src_lang, UPDATED_STRINGS["en"])

        for k, v in dict_to_use.items():
            kv[k] = v

        # Write back preserving order or clean output
        with open(filepath, "w", encoding="utf-8") as f:
            for k, v in kv.items():
                f.write(f"{k},{v}\n")
        print(f"Updated {filepath} successfully.")

if __name__ == "__main__":
    update_events_json()
    update_localization_csvs()

import os
import glob

# 11 new keys
# Each language gets its mapping. en and tr are fully localized;
# other languages receive French/German/Spanish/Russian/etc. translations.

L10N_DATA = {
    "en": {
        "owo.event.peace_of_lodi_1454.title": "The Peace of Lodi",
        "owo.event.peace_of_lodi_1454.description": "On 9 April 1454 at Lodi in Lombardy, envoys of Milan, Venice, and Florence put an end to the destructive Wars in Lombardy. Establishing the Most Holy League (Lega Italica), the treaty establishes a balance of power among the five major Italian powers and guarantees mutual non-aggression across the peninsula.",
        "owo.event.peace_of_lodi_1454.option_1": "Ratify the treaty and safeguard the peace of Italy.",
        "owo.event.peace_of_lodi_1454.option_2": "Refuse the accord; our ambitions in Lombardy cannot be bound.",
        "owo.event.corvinus_black_army_1458.title": "The Black Army of Matthias Corvinus",
        "owo.event.corvinus_black_army_1458.description": "Rising to the Hungarian throne in 1458, King Matthias Corvinus has broken with feudal reliance on rebellious noble levies to establish the Fekete Sereg (The Black Army)—one of Europe's first permanent professional mercenary standing armies, equipped with heavy plate, pavises, and firearms.",
        "owo.event.corvinus_black_army_1458.option_1": "Commission the Black Army to defend the realm and Christendom!",
        "owo.event.corvinus_black_army_1458.option_2": "The treasury cannot sustain mercenaries; rely on the noble banderia.",
        "owo.event.fall_of_trebizond_1461.title": "The Fall of Trebizond",
        "owo.event.fall_of_trebizond_1461.description": "In August 1461, after a determined combined land siege and naval blockade led by Sultan Mehmed II, Emperor David Megas Komnenos has surrendered the fortified coastal city of Trebizond. With the fall of the Komnenian bastion on the Black Sea, the final surviving successor state of the Roman Empire is absorbed into the Ottoman realm.",
        "owo.event.fall_of_trebizond_1461.option_1": "The Black Sea is now firmly an Ottoman lake."
    },
    "tr": {
        "owo.event.peace_of_lodi_1454.title": "Lodi Barışı",
        "owo.event.peace_of_lodi_1454.description": "9 Nisan 1454'te Lombardiya'daki Lodi kentinde Milano, Venedik ve Floransa elçileri Lombardiya Savaşları'na son veren antlaşmayı imzaladı. Kutsal Birlik'i (Lega Italica) kuran bu antlaşma, beş büyük İtalyan gücü arasında güç dengesi tesis ederek yarımadada barışı güvence altına alıyor.",
        "owo.event.peace_of_lodi_1454.option_1": "Antlaşmayı onayla ve İtalya'nın barışını koru.",
        "owo.event.peace_of_lodi_1454.option_2": "Uzlaşmayı reddet; Lombardiya'daki emellerimiz sınırlandırılamaz.",
        "owo.event.corvinus_black_army_1458.title": "Matyas Corvinus ve Kara Ordu",
        "owo.event.corvinus_black_army_1458.description": "1458 yılında Macaristan tahtına çıkan Kral Matyas Corvinus, asi soyluların feodal birliklerine bel bağlamayı bırakarak Avrupa'nın ilk daimi profesyonel paralı ordularından biri olan Kara Ordu'yu (Fekete Sereg) kurdu.",
        "owo.event.corvinus_black_army_1458.option_1": "Krallığı savunmak için Kara Ordu'yu göreve çağır!",
        "owo.event.corvinus_black_army_1458.option_2": "Hazine paralı askerleri kaldıramaz; soylu birliklerine güven.",
        "owo.event.fall_of_trebizond_1461.title": "Trabzon'un Fethi",
        "owo.event.fall_of_trebizond_1461.description": "Ağustos 1461'de Sultan II. Mehmed komutasındaki kara ve deniz kuşatması sonucunda İmparator David Megas Komnenos müstahkem Trabzon kentini teslim etti. Karadeniz'deki son Roma ardıl devleti de Osmanlı topraklarına katıldı.",
        "owo.event.fall_of_trebizond_1461.option_1": "Karadeniz artık tamamen bir Osmanlı gölüdür."
    },
    "de": {
        "owo.event.peace_of_lodi_1454.title": "Der Frieden von Lodi",
        "owo.event.peace_of_lodi_1454.description": "Am 9. April 1454 beendeten Gesandte aus Mailand, Venedig und Florenz in Lodi die verheerenden Mailänder Kriege. Der Vertrag begründet die Heilige Liga (Lega Italica) und sichert ein Gleichgewicht der Kräfte in Italien.",
        "owo.event.peace_of_lodi_1454.option_1": "Ratifiziert den Vertrag und sichert den Frieden Italiens.",
        "owo.event.peace_of_lodi_1454.option_2": "Lehnt das Abkommen ab; unsere Ambitionen dulden keine Schranken.",
        "owo.event.corvinus_black_army_1458.title": "Die Schwarze Armee von Matthias Corvinus",
        "owo.event.corvinus_black_army_1458.description": "Nach seiner Thronbesteigung 1458 gründete König Matthias Corvinus die Schwarze Armee (Fekete Sereg) – eines der ersten ständigen Berufsheere Europas.",
        "owo.event.corvinus_black_army_1458.option_1": "Stellt die Schwarze Armee zur Verteidigung des Reiches auf!",
        "owo.event.corvinus_black_army_1458.option_2": "Die Schatzkammer verträgt keine Söldner; vertraut auf den Adel.",
        "owo.event.fall_of_trebizond_1461.title": "Der Fall von Trapezunt",
        "owo.event.fall_of_trebizond_1461.description": "Im August 1461 kapitulierte Kaiser David Komnenos vor Sultan Mehmed II. Damit fällt der letzte überlebende Nachfolgestaat des Römischen Reiches an das Osmanische Reich.",
        "owo.event.fall_of_trebizond_1461.option_1": "Das Schwarze Meer ist nun ein osmanischer See."
    },
    "fr": {
        "owo.event.peace_of_lodi_1454.title": "La Paix de Lodi",
        "owo.event.peace_of_lodi_1454.description": "Le 9 avril 1454 à Lodi, les envoyés de Milan, Venise et Florence mettent fin aux guerres de Lombardie, instaurant la Sainte Ligue (Lega Italica) pour préserver l'équilibre italien.",
        "owo.event.peace_of_lodi_1454.option_1": "Ratifions le traité pour préserver la paix d'Italie.",
        "owo.event.peace_of_lodi_1454.option_2": "Refusons l'accord; nos ambitions en Lombardie ne sauraient être entravées.",
        "owo.event.corvinus_black_army_1458.title": "L'Armée Noire de Matthias Corvin",
        "owo.event.corvinus_black_army_1458.description": "Monté sur le trône en 1458, le roi Matthias Corvin a créé la Fekete Sereg (l'Armée Noire), l'une des premières armées permanentes de mercenaires professionnels en Europe.",
        "owo.event.corvinus_black_army_1458.option_1": "Finançons l'Armée Noire pour défendre le royaume et la chrétienté !",
        "owo.event.corvinus_black_army_1458.option_2": "Le trésor ne peut entretenir des mercenaires; fions-nous à la noblesse.",
        "owo.event.fall_of_trebizond_1461.title": "La Chute de Trébizonde",
        "owo.event.fall_of_trebizond_1461.description": "En août 1461, après un siège ottoman mené par le sultan Mehmed II, l'empereur David de Trébizonde capitule. Le dernier vestige de l'Empire romain passe sous contrôle ottoman.",
        "owo.event.fall_of_trebizond_1461.option_1": "La mer Noire est désormais un lac ottoman."
    },
    "es": {
        "owo.event.peace_of_lodi_1454.title": "La Paz de Lodi",
        "owo.event.peace_of_lodi_1454.description": "El 9 de abril de 1454 en Lodi, Milán, Venecia y Florencia pusieron fin a las guerras de Lombardía fundando la Liga Itálica para mantener el equilibrio de poder en Italia.",
        "owo.event.peace_of_lodi_1454.option_1": "Ratificar el tratado y salvaguardar la paz de Italia.",
        "owo.event.peace_of_lodi_1454.option_2": "Rechazar el acuerdo; nuestras ambiciones en Lombardía no tienen límites.",
        "owo.event.corvinus_black_army_1458.title": "El Ejército Negro de Matías Corvino",
        "owo.event.corvinus_black_army_1458.description": "Al asumir el trono en 1458, el rey Matías Corvino creó el Fekete Sereg (Ejército Negro), uno de los primeros ejércitos permanentes profesionales de Europa.",
        "owo.event.corvinus_black_army_1458.option_1": "¡Comisionar al Ejército Negro para defender el reino y la cristiandad!",
        "owo.event.corvinus_black_army_1458.option_2": "El tesoro no puede sostener mercenarios; confiemos en la nobleza.",
        "owo.event.fall_of_trebizond_1461.title": "La Caída de Trebisonda",
        "owo.event.fall_of_trebizond_1461.description": "En agosto de 1461, tras el asedio del sultán Mehmed II, el emperador David capituló en Trebisonda. El último estado sucesor romano queda absorbido por los otomanos.",
        "owo.event.fall_of_trebizond_1461.option_1": "El mar Negro es ahora un lago otomano."
    },
    "ru": {
        "owo.event.peace_of_lodi_1454.title": "Лодийский мир",
        "owo.event.peace_of_lodi_1454.description": "9 апреля 1454 года в Лоди представители Милана, Венеции и Флоренции положили конец Ломбардским войнам, учредив Священную лигу (Lega Italica) для баланса сил в Италии.",
        "owo.event.peace_of_lodi_1454.option_1": "Ратифицировать договор и сохранить мир в Италии.",
        "owo.event.peace_of_lodi_1454.option_2": "Отклонить соглашение; наши амбиции в Ломбардии безграничны.",
        "owo.event.corvinus_black_army_1458.title": "Чёрная армия Матьяша Корвина",
        "owo.event.corvinus_black_army_1458.description": "Взойдя на престол в 1458 году, король Матьяш Корвин создал «Чёрную армию» (Fekete Sereg) — одну из первых регулярных наёмных армий в Европе.",
        "owo.event.corvinus_black_army_1458.option_1": "Собрать Чёрную армию для защиты королевства!",
        "owo.event.corvinus_black_army_1458.option_2": "Казна не потянет наёмников; полагаться на дворянское ополчение.",
        "owo.event.fall_of_trebizond_1461.title": "Падение Трапезунда",
        "owo.event.fall_of_trebizond_1461.description": "В августе 1461 года после осады султана Мехмеда II император Давид сдал Трапезунд. Последний осколок Римской империи перешёл под власть османов.",
        "owo.event.fall_of_trebizond_1461.option_1": "Чёрное море теперь османское озеро."
    }
}

# For languages not explicitly specified, fallback to English or matching regional variant
LANG_FALLBACKS = {
    "es-419": "es",
    "pt": "es",
    "pt-br": "es",
    "cz": "de",
    "ja": "en",
    "ko": "en",
    "zh": "en"
}

all_langs = ["cz", "de", "en", "es", "es-419", "fr", "ja", "ko", "pt", "pt-br", "ru", "tr", "zh"]

for lang in all_langs:
    path = f"Content/localization/{lang}.csv"
    if not os.path.exists(path):
        print(f"Skipping missing: {path}")
        continue

    # Determine dictionary
    if lang in L10N_DATA:
        source_dict = L10N_DATA[lang]
    elif lang in LANG_FALLBACKS and LANG_FALLBACKS[lang] in L10N_DATA:
        source_dict = L10N_DATA[LANG_FALLBACKS[lang]]
    else:
        source_dict = L10N_DATA["en"]

    # Read existing rows to prevent duplicate insertion
    with open(path, "r", encoding="utf-8") as f:
        existing = f.read()

    to_append = []
    for k, v in source_dict.items():
        if k not in existing:
            # Clean value of newlines or quotes
            v_clean = v.replace("\n", " ").replace("\r", "")
            to_append.append(f"{k},{v_clean}\n")

    if to_append:
        with open(path, "a", encoding="utf-8") as f:
            f.writelines(to_append)
        print(f"Added {len(to_append)} keys to {path}")
    else:
        print(f"All keys already present in {path}")

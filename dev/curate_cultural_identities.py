"""
Curate and update dominantReligion, dominantEthnicity, primaryCulture, ethnicHomogeneity,
and neutrality for all 137 historical nations in scenario/countries_add.json.
"""

import json

# ISO3 -> (dominantReligion, dominantEthnicity, primaryCulture, ethnicHomogeneity, is_neutral)
# dominantReligion uses standard labels: Christianity, Islam, Hinduism, Buddhism, Shintoism, Judaism, or period terms (Tengrism, Animism, Mesoamerican, Andean, etc.)
# which map to ReligionFamily in the engine.
CULTURAL_DATA = {
    # Western Europe & Central Europe
    "FRA": ("Christianity", "French", "French", 0.85, False),
    "ENG": ("Christianity", "English", "English", 0.85, False),
    "SCT": ("Christianity", "Scottish", "Scottish", 0.85, False),
    "BUR": ("Christianity", "Burgundian", "Burgundian", 0.75, False),
    "CHE": ("Christianity", "Swiss", "Swiss", 0.80, False),  # In 1450 the Swiss Confederacy was actively expansionist (Burgundian Wars, Italian Wars)
    "HAB": ("Christianity", "German", "Austrian", 0.85, False),
    "BOH": ("Christianity", "Czech", "Bohemian", 0.80, False),
    "SAX": ("Christianity", "German", "Saxon", 0.90, False),
    "BRG": ("Christianity", "German", "Brandenburg", 0.90, False),
    "BAV": ("Christianity", "German", "Bavarian", 0.90, False),
    "PAL": ("Christianity", "German", "Palatine", 0.90, False),
    "COL": ("Christianity", "German", "Rhenish", 0.90, False),
    "WUR": ("Christianity", "German", "Swabian", 0.90, False),

    # Southern Europe
    "CAS": ("Christianity", "Castilian", "Castilian", 0.85, False),
    "ARA": ("Christianity", "Aragonese", "Aragonese", 0.80, False),
    "PRT": ("Christianity", "Portuguese", "Portuguese", 0.90, False),
    "NAV": ("Christianity", "Basque", "Navarrese", 0.80, False),
    "PAP": ("Christianity", "Italian", "Roman", 0.85, False),
    "VNC": ("Christianity", "Venetian", "Venetian", 0.80, False),
    "GEN": ("Christianity", "Genoese", "Genoese", 0.85, False),
    "MIL": ("Christianity", "Lombard", "Lombard", 0.85, False),
    "FLR": ("Christianity", "Tuscan", "Florentine", 0.90, False),
    "NAP": ("Christianity", "Neapolitan", "Neapolitan", 0.85, False),
    "SAV": ("Christianity", "Savoyard", "Savoyard", 0.85, False),
    "GRN": ("Islam", "Andalusian", "Andalusian Arab", 0.75, False),
    "KNI": ("Christianity", "Occitan", "Hospitaller", 0.65, False),
    "LEZ": ("Christianity", "Albanian", "Albanian", 0.90, False),
    "BOS": ("Christianity", "Bosnian", "Bosnian", 0.70, False),
    "SRB": ("Christianity", "Serbian", "Serbian", 0.85, False),
    "BYZ": ("Christianity", "Greek", "Byzantine", 0.85, False),
    "LUS": ("Christianity", "Greek", "Cypriot", 0.70, False),

    # Eastern Europe & Baltic
    "POL": ("Christianity", "Polish", "Polish", 0.85, False),
    "LTH": ("Christianity", "Lithuanian", "Lithuanian", 0.60, False),
    "HUN": ("Christianity", "Hungarian", "Hungarian", 0.80, False),
    "TEU": ("Christianity", "German", "Teutonic", 0.70, False),
    "LIV": ("Christianity", "German", "Livonian", 0.65, False),
    "MVY": ("Christianity", "Russian", "Muscovite", 0.85, False),
    "NVD": ("Christianity", "Russian", "Novgorodian", 0.85, False),
    "TVR": ("Christianity", "Russian", "Tverian", 0.90, False),
    "RYA": ("Christianity", "Russian", "Ryazanian", 0.90, False),
    "PSK": ("Christianity", "Russian", "Pskovian", 0.90, False),
    "WAL": ("Christianity", "Romanian", "Wallachian", 0.85, False),
    "MOL": ("Christianity", "Romanian", "Moldavian", 0.85, False),
    "KZN": ("Islam", "Tatar", "Kazan Tatar", 0.80, False),
    "KRM": ("Islam", "Crimean Tatar", "Crimean", 0.80, False),
    "STE": ("Islam", "Turco-Mongol", "Steppe Nomadic", 0.75, False),

    # Northern Europe
    "DAN": ("Christianity", "Danish", "Danish", 0.90, False),
    "SWD": ("Christianity", "Swedish", "Swedish", 0.90, False),

    # Anatolia & Western Asia
    "OTT": ("Islam", "Turkish", "Ottoman", 0.65, False),
    "KAR": ("Islam", "Turkish", "Karamanid", 0.85, False),
    "CND": ("Islam", "Turkish", "Candarid", 0.85, False),
    "DUL": ("Islam", "Turkish", "Dulkadirid", 0.85, False),
    "RAM": ("Islam", "Turkish", "Ramazanid", 0.85, False),
    "TRE": ("Christianity", "Greek", "Pontic", 0.80, False),
    "GRG": ("Christianity", "Georgian", "Georgian", 0.85, False),
    "AKK": ("Islam", "Turkoman", "Turkoman", 0.75, False),
    "KKY": ("Islam", "Turkoman", "Turkoman", 0.75, False),
    "SHV": ("Islam", "Azerbaijani", "Shirvani", 0.80, False),
    "TAH": ("Islam", "Arab", "Yemeni", 0.85, False),
    "NBH": ("Islam", "Arab", "Omani", 0.85, False),
    "HRM": ("Islam", "Persian", "Hormuzi", 0.75, False),
    "JBR": ("Islam", "Arab", "Jabrid", 0.90, False),

    # Central Asia
    "TIM": ("Islam", "Turco-Mongol", "Persianate", 0.60, False),
    "UZB": ("Islam", "Uzbek", "Uzbek", 0.80, False),
    "MOG": ("Islam", "Turco-Mongol", "Chagatai", 0.75, False),
    "SIB": ("Islam", "Siberian Tatar", "Siberian", 0.75, False),

    # North Africa
    "MAM": ("Islam", "Arab", "Mamluk", 0.75, False),
    "MOR": ("Islam", "Moroccan", "Maghrebi", 0.85, False),
    "HFS": ("Islam", "Tunisian", "Hafsid", 0.85, False),
    "ZAY": ("Islam", "Berber", "Tlemcen", 0.80, False),

    # Sub-Saharan Africa
    "MAL": ("Islam", "Mandinka", "Mandinka", 0.70, False),
    "SON": ("Islam", "Songhai", "Songhai", 0.70, False),
    "ABY": ("Christianity", "Amhara", "Ethiopian", 0.80, False),
    "BNK": ("Animism", "Edo", "Benin", 0.90, False),
    "ZIM": ("Animism", "Shona", "Shona", 0.90, False),
    "KNG": ("Animism", "Kongo", "Kongo", 0.90, False),
    "KBR": ("Islam", "Kanuri", "Kanuri", 0.80, False),
    "MOS": ("Animism", "Mossi", "Mossi", 0.90, False),
    "HAU": ("Islam", "Hausa", "Hausa", 0.80, False),
    "OYO": ("Animism", "Yoruba", "Yoruba", 0.90, False),
    "LUB": ("Animism", "Luba", "Luba", 0.90, False),
    "ADA": ("Islam", "Somali", "Adal", 0.85, False),
    "FNJ": ("Islam", "Nubian", "Funj", 0.80, False),
    "KLW": ("Islam", "Swahili", "Swahili", 0.80, False),
    "BUG": ("Animism", "Ganda", "Ganda", 0.90, False),
    "MAD": ("Animism", "Malagasy", "Malagasy", 0.85, False),

    # South Asia
    "DEL": ("Islam", "Hindustani", "Indo-Muslim", 0.50, False),
    "VIJ": ("Hinduism", "Kannada", "Vijayanagara", 0.85, False),
    "GUJ": ("Islam", "Gujarati", "Gujarati", 0.60, False),
    "BAH": ("Islam", "Deccani", "Deccani", 0.55, False),
    "BNG": ("Islam", "Bengali", "Bengali", 0.65, False),
    "MLW": ("Islam", "Malwi", "Malwi", 0.55, False),
    "MEW": ("Hinduism", "Rajput", "Rajput", 0.90, False),
    "JNP": ("Islam", "Hindustani", "Jaunpuri", 0.55, False),
    "ORI": ("Hinduism", "Odia", "Gajapati", 0.85, False),
    "KSH": ("Islam", "Kashmiri", "Kashmiri", 0.70, False),
    "NEP": ("Hinduism", "Newar", "Nepali", 0.85, False),
    "KOT": ("Buddhism", "Sinhalese", "Sinhalese", 0.85, False),
    "MLD": ("Islam", "Maldivian", "Dhivehi", 0.95, False),
    "SND": ("Islam", "Sindhi", "Sindhi", 0.80, False),

    # East Asia
    "MYN": ("Buddhism", "Han", "Chinese", 0.95, False),
    "JOS": ("Buddhism", "Korean", "Joseon", 0.95, False),
    "MRC": ("Shintoism", "Japanese", "Japanese", 0.95, False),
    "TIB": ("Buddhism", "Tibetan", "Tibetan", 0.95, False),
    "RYU": ("Buddhism", "Ryukyuan", "Ryukyuan", 0.95, False),
    "MGL": ("Tengrism", "Oirat", "Oirat Mongol", 0.90, False),
    "MID": ("Animism", "Papora", "Formosan", 0.90, True),

    # Southeast Asia
    "MAJ": ("Hinduism", "Javanese", "Javanese", 0.80, False),
    "AYU": ("Buddhism", "Thai", "Siamese", 0.85, False),
    "DVT": ("Buddhism", "Vietnamese", "Dai Viet", 0.90, False),
    "MLC": ("Islam", "Malay", "Melayu", 0.85, False),
    "AVA": ("Buddhism", "Burmese", "Burmese", 0.85, False),
    "PEG": ("Buddhism", "Mon", "Mon", 0.85, False),
    "ARK": ("Buddhism", "Rakhine", "Arakanese", 0.80, False),
    "LNA": ("Buddhism", "Lanna Thai", "Lan Na", 0.90, False),
    "LXG": ("Buddhism", "Lao", "Lan Xang", 0.90, False),
    "KMR": ("Buddhism", "Khmer", "Khmer", 0.90, False),
    "CPA": ("Hinduism", "Cham", "Champa", 0.80, False),
    "BRU": ("Islam", "Bruneian", "Bruneian", 0.85, False),
    "PSI": ("Islam", "Acehnese", "Pasai", 0.90, False),
    "SUL": ("Islam", "Tausug", "Sulu", 0.90, False),
    "TND": ("Hinduism", "Tagalog", "Luzon", 0.85, False),
    "CEB": ("Hinduism", "Cebuano", "Visayan", 0.85, False),
    "MGD": ("Islam", "Maguindanao", "Moro", 0.90, False),

    # Americas
    "AZT": ("Mesoamerican", "Nahua", "Aztec", 0.85, False),
    "INC": ("Andean", "Quechua", "Inca", 0.85, False),
    "MAY": ("Mesoamerican", "Maya", "Maya", 0.90, False),
    "TAR": ("Mesoamerican", "Purepecha", "Tarascan", 0.90, False),
    "TLX": ("Mesoamerican", "Nahua", "Tlaxcalan", 0.95, False),
    "ZAP": ("Mesoamerican", "Zapotec", "Zapotec", 0.90, False),
    "CHM": ("Andean", "Chimu", "Chimu", 0.85, False),
    "MUI": ("Chibchan", "Muisca", "Muisca", 0.90, False),
    "MAP": ("Animism", "Mapuche", "Mapuche", 0.95, False),
    "IRO": ("Animism", "Iroquois", "Haudenosaunee", 0.95, False),
    "PUE": ("Animism", "Pueblo", "Puebloan", 0.95, True),
    "CAH": ("Animism", "Mississippian", "Cahokian", 0.90, False),
    "TAI": ("Animism", "Taino", "Taino", 0.95, True),
}

def main():
    with open("scenario/countries_add.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    missing = []
    for c in data["addCountries"]:
        iso = c["iso3"]
        if iso in CULTURAL_DATA:
            rel, eth, cult, homo, neutral = CULTURAL_DATA[iso]
            c["dominantReligion"] = rel
            c["dominantEthnicity"] = eth
            c["primaryCulture"] = cult
            c["ethnicHomogeneity"] = round(float(homo), 2)
            if neutral:
                c["neutral"] = True
            else:
                c.pop("neutral", None)
            updated += 1
        else:
            missing.append(iso)

    print(f"Updated {updated} / {len(data['addCountries'])} countries.")
    if missing:
        print(f"Missing ISOs: {missing}")

    with open("scenario/countries_add.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Saved scenario/countries_add.json successfully.")

if __name__ == "__main__":
    main()

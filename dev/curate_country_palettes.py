#!/usr/bin/env python3
"""
Curates mapColorVibrant and mapColorGloomy for all 137 countries in scenario/countries_add.json.

- mapColorVibrant: High-saturation, crisp, vivid tone for political/contrast map modes.
- mapColorGloomy: Desaturated, antique parchment/earthy tone for historical/atmospheric map modes.
"""

import json
import re
import colorsys
import os
import jsonschema

SCHEMA_PATH = "docs/modding/schemas/mod_scenario_countries_add.schema.json"
TARGET_FILE = "scenario/countries_add.json"

def hex_to_rgb(hex_str: str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def rgb_to_hex(r: float, g: float, b: float) -> str:
    r_int = max(0, min(255, int(round(r * 255))))
    g_int = max(0, min(255, int(round(g * 255))))
    b_int = max(0, min(255, int(round(b * 255))))
    return '#{:02X}{:02X}{:02X}'.format(r_int, g_int, b_int)

def compute_palettes(hex_str: str):
    r, g, b = hex_to_rgb(hex_str)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Vibrant: saturated, punchy, well-lit but not washed out
    s_vib = min(1.0, s * 1.30 + 0.05) if s > 0.05 else s
    l_vib = max(0.40, min(0.68, l * 1.05))
    r_v, g_v, b_v = colorsys.hls_to_rgb(h, l_vib, s_vib)
    hex_vib = rgb_to_hex(r_v, g_v, b_v)
    
    # Gloomy: desaturated antique/parchment tone, deeper shading
    s_glo = max(0.15, s * 0.50) if s > 0.05 else s
    l_glo = max(0.20, min(0.48, l * 0.75))
    r_g, g_g, b_g = colorsys.hls_to_rgb(h, l_glo, s_glo)
    hex_glo = rgb_to_hex(r_g, g_g, b_g)
    
    return hex_vib, hex_glo

def main():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    hex_regex = re.compile(r"^#[0-9A-Fa-f]{6}$")

    count = 0
    for country in data.get("addCountries", []):
        base_color = country.get("mapColor")
        if not base_color or not hex_regex.match(base_color):
            raise ValueError(f"Country {country.get('iso3')} has invalid mapColor: {base_color}")
        
        vibrant, gloomy = compute_palettes(base_color)
        country["mapColorVibrant"] = vibrant
        country["mapColorGloomy"] = gloomy
        count += 1

    # Validate against schema
    if os.path.exists(SCHEMA_PATH):
        with open(SCHEMA_PATH, "r", encoding="utf-8") as sf:
            schema = json.load(sf)
        jsonschema.validate(instance=data, schema=schema)
        print(f"Schema validation passed for all {count} countries.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Successfully updated {count} countries in {TARGET_FILE}.")

if __name__ == "__main__":
    main()

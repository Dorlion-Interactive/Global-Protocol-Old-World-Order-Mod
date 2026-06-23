"""Shared helpers for province ownership curation tooling (Old World Order mod).

Read-only access to the engine's province registry plus the mod's curation source.
Nothing here writes to the engine/vanilla data — only the mod repo is ever written
(by build_province_ownership.py).
"""
import json
import os
import sys

# Province names contain accents (Québec, Entre Ríos…); force UTF-8 stdout on Windows.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

MOD_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_PATH = os.environ.get(
    "OWO_REGISTRY",
    r"C:/Personal/Genel/Projeler/NewWorldOrder/.ai/configs/data/provinces/province_registry.json",
)
CURATION_PATH = os.path.join(MOD_ROOT, "dev", "province_curation.json")
COUNTRIES_PATH = os.path.join(MOD_ROOT, "scenario", "countries_add.json")
OWNERSHIP_PATH = os.path.join(MOD_ROOT, "scenario", "provinces_ownership.json")


def load_registry():
    """Return {provinceId: record} from the engine province registry (read-only)."""
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        data = json.load(f)
    provs = data if isinstance(data, list) else data.get("provinces") or next(iter(data.values()))
    return {p["id"]: p for p in provs}


def load_countries():
    """Return {iso3: country dict} from the mod's countries_add.json."""
    with open(COUNTRIES_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return {c["iso3"]: c for c in data["addCountries"]}


def load_curation():
    """Return {iso3: [provinceId, ...]} from the hand-curated source (or {} if absent)."""
    if not os.path.exists(CURATION_PATH):
        return {}
    with open(CURATION_PATH, encoding="utf-8") as f:
        data = json.load(f)
    # Allow an optional "_comment" / metadata keys prefixed with underscore.
    return {k: v for k, v in data.items() if not k.startswith("_")}


def continent_of(lat, lon):
    """Rough geographic continent from a centroid — for audit sanity checks only."""
    if -170 <= lon <= -25 and -60 <= lat <= 85:
        return "Americas"
    if -25 < lon <= 60 and lat >= 35:
        return "Europe"
    if -20 < lon <= 52 and -40 <= lat < 35:
        return "Africa"
    if 26 <= lon <= 63 and 12 <= lat < 42:
        return "MiddleEast"
    if 60 < lon <= 180 and lat >= 5:
        return "Asia"
    if 110 <= lon <= 180 and lat < 5:
        return "Oceania"
    if lat < -50:
        return "Antarctica"
    return "Other"

"""Audit the current curation: per-nation area vs declared, continent spread, unowned.

Reads dev/province_curation.json (preferred) or falls back to the built
scenario/provinces_ownership.json, and reports:
  - owned-area / declared areaKm2 ratio (flags > 2.5x or < 0.3x)
  - geographic continent spread per nation (flags nations on >1 continent)
  - total unowned province count

Usage: python dev/audit_ownership.py
"""
import json
import math
from collections import defaultdict

from owo_provinces import (
    OWNERSHIP_PATH,
    load_countries,
    load_curation,
    load_registry,
)

SPAN_FLAG_KM = 3500  # bounding-box diagonal above this = geographic sprawl


def owner_map():
    cur = load_curation()
    if cur:
        m = {}
        for iso3, ids in cur.items():
            for pid in ids:
                m[pid] = iso3
        return m, "curation"
    with open(OWNERSHIP_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return {o["provinceId"]: o["ownerISO3"] for o in data["provinceOwnerOverrides"]}, "ownership.json"


def main():
    registry = load_registry()
    countries = load_countries()
    omap, src = owner_map()

    area = defaultdict(float)
    count = defaultdict(int)
    pts = defaultdict(list)
    for pid, iso3 in omap.items():
        p = registry.get(pid)
        if not p:
            continue
        area[iso3] += p["area_km2"]
        count[iso3] += 1
        pts[iso3].append((p["centroid"]["lat"], p["centroid"]["lon"]))

    def span_km(points):
        if len(points) < 2:
            return 0.0
        lats = [a for a, _ in points]
        lons = [b for _, b in points]
        midlat = (min(lats) + max(lats)) / 2
        dy = (max(lats) - min(lats)) * 111.0
        dx = (max(lons) - min(lons)) * 111.0 * math.cos(math.radians(midlat))
        return math.hypot(dx, dy)

    print(f"=== Audit (source: {src}) ===")
    print(f"{'ISO':4} {'prov':>4} {'ownedMkm2':>9} {'declared':>9} {'ratio':>6}  flags")
    flagged = []
    for iso3 in sorted(area, key=lambda k: -area[k]):
        dec = (countries.get(iso3, {}) or {}).get("areaKm2") or 0
        ratio = area[iso3] / dec if dec else 0
        flags = []
        if dec and (ratio > 2.5 or ratio < 0.3):
            flags.append(f"AREA {ratio:.1f}x")
        span = span_km(pts[iso3])
        if span > SPAN_FLAG_KM:
            flags.append(f"SPAN {span:.0f}km")
        if flags:
            flagged.append(iso3)
        print(f"{iso3:4} {count[iso3]:4} {area[iso3]/1e6:9.2f} {dec:9.0f} {ratio:6.1f}  {'; '.join(flags)}")

    total = len(registry)
    assigned = len(omap)
    print(f"\nNations: {len(area)} | assigned provinces: {assigned} | "
          f"unowned: {total-assigned} | flagged nations: {len(flagged)}")
    if flagged:
        print("Flagged:", ", ".join(flagged))


if __name__ == "__main__":
    main()

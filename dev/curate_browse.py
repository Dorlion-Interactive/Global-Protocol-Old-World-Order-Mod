"""Browse the province registry to support hand-curation (read-only).

Examples:
  python dev/curate_browse.py iso USA CAN          # provinces in modern USA + Canada
  python dev/curate_browse.py name york            # provinces whose name contains 'york'
  python dev/curate_browse.py box 35 50 -90 -65    # latmin latmax lonmin lonmax
  python dev/curate_browse.py near 1249 600        # within 600 km of province 1249's centroid
  python dev/curate_browse.py free iso RUS         # like 'iso' but only UNassigned provinces

Output columns: id  name  modernISO  lat  lon  area_km2  [owner-if-curated]
"""
import math
import sys

from owo_provinces import load_curation, load_registry


def _curated_owner():
    m = {}
    for iso3, ids in load_curation().items():
        for pid in ids:
            m[pid] = iso3
    return m


def _print(rows, owned):
    rows.sort(key=lambda p: (p["country_iso3"], p["centroid"]["lat"]))
    for p in rows:
        c = p["centroid"]
        tag = owned.get(p["id"], "")
        print(f"{p['id']:5} {p['name'][:26]:26} {p['country_iso3']:4} "
              f"{c['lat']:7.2f} {c['lon']:8.2f} {p['area_km2']:9.0f}  {tag}")
    print(f"-- {len(rows)} provinces")


def main():
    reg = load_registry()
    owned = _curated_owner()
    args = sys.argv[1:]
    free = False
    if args and args[0] == "free":
        free = True
        args = args[1:]
    if not args:
        print(__doc__)
        return
    mode, rest = args[0], args[1:]

    if mode == "iso":
        isos = {s.upper() for s in rest}
        rows = [p for p in reg.values() if p["country_iso3"] in isos]
    elif mode == "name":
        sub = rest[0].lower()
        rows = [p for p in reg.values() if sub in p["name"].lower()]
    elif mode == "box":
        latmin, latmax, lonmin, lonmax = map(float, rest)
        rows = [p for p in reg.values()
                if latmin <= p["centroid"]["lat"] <= latmax
                and lonmin <= p["centroid"]["lon"] <= lonmax]
    elif mode == "near":
        pid, km = int(rest[0]), float(rest[1])
        c0 = reg[pid]["centroid"]
        rows = []
        for p in reg.values():
            c = p["centroid"]
            dlat = (c["lat"] - c0["lat"]) * 111.0
            dlon = (c["lon"] - c0["lon"]) * 111.0 * math.cos(math.radians(c0["lat"]))
            if math.hypot(dlat, dlon) <= km:
                rows.append(p)
    else:
        print(__doc__)
        return

    if free:
        rows = [p for p in rows if p["id"] not in owned]
    _print(rows, owned)


if __name__ == "__main__":
    main()

"""Expand the hand-curated province lists into scenario/provinces_ownership.json.

Source of truth : dev/province_curation.json  ->  { "ISO3": [provinceId, ...], ... }
Output          : scenario/provinces_ownership.json

Any province NOT listed in the curation is intentionally left unowned (the engine
renders it neutral gray and excludes it from country labels). This script validates
the curation and refuses to write a broken ownership file.

Usage:
    python dev/build_province_ownership.py            # validate + write
    python dev/build_province_ownership.py --check    # validate only, no write
"""
import json
import sys

from owo_provinces import (
    OWNERSHIP_PATH,
    load_countries,
    load_curation,
    load_registry,
)


def validate(curation, registry, countries):
    errors = []
    seen = {}  # provinceId -> owner (to catch double assignment)
    valid_owners = set(countries)

    for iso3, ids in curation.items():
        if iso3 not in valid_owners:
            errors.append(f"owner {iso3!r} is not defined in countries_add.json")
        if not isinstance(ids, list):
            errors.append(f"{iso3}: province list must be an array")
            continue
        for pid in ids:
            if pid not in registry:
                errors.append(f"{iso3}: province id {pid} not found in registry")
                continue
            if pid in seen and seen[pid] != iso3:
                errors.append(
                    f"province {pid} ({registry[pid]['name']}) assigned to both "
                    f"{seen[pid]} and {iso3}"
                )
            seen[pid] = iso3

        # Capital province (by name) should belong to its own nation.
        cap_name = (countries.get(iso3, {}) or {}).get("capitalProvince")
        if cap_name:
            cap_ids = [p for p in ids if registry.get(p, {}).get("name") == cap_name]
            if not cap_ids:
                # Only a warning-level issue; capital province name may differ from
                # the registry naming. Report but do not fail the build.
                errors.append(
                    f"WARN {iso3}: capitalProvince {cap_name!r} not in its own list"
                )
    return errors


def main():
    check_only = "--check" in sys.argv
    verbose = "--verbose" in sys.argv
    registry = load_registry()
    countries = load_countries()
    curation = load_curation()

    if not curation:
        print("No curation found at dev/province_curation.json — nothing to build.")
        return 1

    errors = validate(curation, registry, countries)
    hard = [e for e in errors if not e.startswith("WARN")]
    warns = [e for e in errors if e.startswith("WARN")]

    if verbose:
        for w in warns:
            print(w)
    elif warns:
        print(f"({len(warns)} capital-province warnings; run --verbose to see them)")
    if hard:
        print(f"\nVALIDATION FAILED — {len(hard)} error(s):")
        for e in hard:
            print("  -", e)
        return 2

    overrides = []
    for iso3, ids in curation.items():
        for pid in sorted(set(ids)):
            overrides.append({"provinceId": pid, "ownerISO3": iso3})
    overrides.sort(key=lambda o: o["provinceId"])

    total = len(registry)
    assigned = len(overrides)
    print(
        f"OK: {assigned} provinces assigned across {len(curation)} nations | "
        f"{total - assigned} unowned ({100*(total-assigned)/total:.0f}% wilderness)"
    )

    if check_only:
        print("(--check) not writing.")
        return 0

    out = {"regionOwnerOverrides": [], "provinceOwnerOverrides": overrides}
    with open(OWNERSHIP_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Wrote {OWNERSHIP_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

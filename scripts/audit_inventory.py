import json
import os
import glob

def audit():
    print("=" * 60)
    print("GLOBAL PROTOCOL: HISTORICAL MOD - INVENTORY AUDIT")
    print("=" * 60)

    # 1. BUILDINGS
    with open('scenario/buildings_override.json', 'r', encoding='utf-8') as f:
        bld_data = json.load(f)
    bld_existing = {os.path.splitext(f)[0] for f in os.listdir('icons/buildings') if f.endswith('.png')}
    buildings = bld_data.get('buildings', [])
    print(f"\n1. BUILDINGS ({len(buildings)} defined, {len(bld_existing)} icons on disk):")
    bld_missing = []
    for b in buildings:
        bid = b.get('id')
        icon = b.get('icon') or bid
        if icon in bld_existing:
            print(f"  [OK] {bid:22} -> icon: {icon}")
        else:
            print(f"  [MISSING] {bid:22} -> icon: {icon}")
            bld_missing.append((bid, icon))

    # 2. UNITS
    with open('scenario/units_define.json', 'r', encoding='utf-8') as f:
        unit_data = json.load(f)
    unit_existing = {os.path.splitext(f)[0] for f in os.listdir('icons/units') if f.endswith('.png')}
    units = unit_data.get('unitTypes', [])

    generic_units = [u for u in units if not u.get('ownerIso3')]
    country_units = [u for u in units if u.get('ownerIso3')]

    print(f"\n2. GENERIC / ALL-COUNTRY UNITS ({len(generic_units)} defined):")
    gen_missing = []
    for u in generic_units:
        uid = u.get('id')
        name = u.get('displayName') or uid
        cat = u.get('category')
        if uid in unit_existing:
            print(f"  [OK]      {uid:22} ({name:18}) [{cat}]")
        else:
            print(f"  [MISSING] {uid:22} ({name:18}) [{cat}]")
            gen_missing.append(u)

    print(f"\n3. COUNTRY-SPECIFIC UNITS ({len(country_units)} defined):")
    cntry_missing = []
    for u in country_units:
        uid = u.get('id')
        name = u.get('displayName') or uid
        cat = u.get('category')
        owner = u.get('ownerIso3')
        if uid in unit_existing:
            print(f"  [OK]      {uid:25} ({name:20}) [{owner}] [{cat}]")
        else:
            print(f"  [MISSING] {uid:25} ({name:20}) [{owner}] [{cat}]")
            cntry_missing.append(u)

    # 3. DOCTRINES
    with open('overrides/doctrines.json', 'r', encoding='utf-8') as f:
        doc_data = json.load(f)
    doc_existing = {os.path.splitext(f)[0] for f in os.listdir('icons/doctrines') if f.endswith('.png')}
    branches = doc_data.get('branches', [])

    print(f"\n4. DOCTRINES BY BRANCH (Total 7 branches, {len(doc_existing)} doctrine icons on disk):")
    doc_branch_summary = {}
    for b in branches:
        b_id = b.get('id')
        tiers = b.get('tiers', [])
        b_total = 0
        b_ok = 0
        b_miss = []
        for t in tiers:
            for d in t.get('doctrines', []):
                b_total += 1
                did = d.get('id')
                icon = d.get('icon') or did
                if icon in doc_existing:
                    b_ok += 1
                else:
                    b_miss.append((did, icon, d.get('name_key')))
        doc_branch_summary[b_id] = {
            'total': b_total,
            'ok': b_ok,
            'missing': b_miss
        }
        status_str = f"COMPLETED ({b_ok}/{b_total})" if b_ok == b_total else f"NEEDS ART ({b_ok}/{b_total})"
        print(f"  Branch: {b_id:15} -> {status_str}")

    # Check milestone badges
    print("\n5. BRANCH MILESTONE BADGES:")
    for b in branches:
        bid = b.get('id')
        m_name = f"{bid}_milestone"
        if m_name in doc_existing:
            print(f"  [OK] {m_name}")
        else:
            print(f"  [MISSING] {m_name}")

    # 4. RESOURCES
    if os.path.exists('scenario/resources_override.json'):
        with open('scenario/resources_override.json', 'r', encoding='utf-8') as f:
            res_data = json.load(f)
        res_existing = {os.path.splitext(f)[0] for f in os.listdir('icons/resources') if f.endswith('.png')} if os.path.exists('icons/resources') else set()
        print(f"\n6. RESOURCES:")
        commodities = res_data.get('commodities', [])
        for c in commodities:
            cid = c.get('id')
            cicon = c.get('icon') or cid
            status = "[OK]" if cicon in res_existing else "[NO ICON - USING DEFAULT/TEXT]"
            print(f"  {status} Resource: {cid} (icon: {cicon})")

    # 5. CODE / RUNTIME WIRING CHECK
    print("\n7. RUNTIME WIRING & LOGIC CHECK:")
    print("Checking C# and JS/WASM source files for unit, building, and doctrine references...")

if __name__ == '__main__':
    audit()

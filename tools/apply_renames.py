import os, re, glob

MOD = r"D:/WorkSpace/V3/daoyu_cheat"

# whole-word replacements applied to common/**.txt and events/**.txt
RENAMES = {
    # buildings - regular plural -> singular
    "building_artillery_foundries": "building_artillery_foundry",
    "building_barracks": "building_barrack",
    "building_chemical_plants": "building_chemical_plant",
    "building_gold_fields": "building_gold_field",
    "building_munition_plants": "building_munition_plant",
    "building_paper_mills": "building_paper_mill",
    "building_shipyards": "building_shipyard",
    "building_steel_mills": "building_steel_mill",
    "building_subsistence_farms": "building_subsistence_farm",
    "building_subsistence_fishing_villages": "building_subsistence_fishing_village",
    "building_subsistence_orchards": "building_subsistence_orchard",
    "building_subsistence_pastures": "building_subsistence_pasture",
    "building_synthetics_plants": "building_synthetics_plant",
    "building_textile_mills": "building_textile_mill",
    "building_tooling_workshops": "building_tooling_workshop",
    # buildings - confirmed non-regular renames
    "building_arts_academy": "building_art_academy",
    "building_furniture_manufacturies": "building_furniture_manufactory",
    "building_subsistence_rice_paddies": "building_subsistence_rice_farm",
    "building_vineyard_plantation": "building_vineyard",
    # buildings - 1.13 semantic restructure (review)
    "building_military_shipyards": "building_shipyard",
    "building_naval_base": "building_port",
    "building_war_machine_industry": "building_arms_industry",
    # technology
    "dreadnought": "dreadnought_tech",
}

# order matters: do NOT let a short key clobber inside a longer key.
# sort by length desc so e.g. building_subsistence_fishing_villages handled before building... (safe anyway via \b)
keys = sorted(RENAMES, key=len, reverse=True)
patterns = [(re.compile(r"(?<![\w-])" + re.escape(k) + r"(?![\w-])"), RENAMES[k]) for k in keys]

files = glob.glob(os.path.join(MOD, "common", "**", "*.txt"), recursive=True) + \
        glob.glob(os.path.join(MOD, "events", "**", "*.txt"), recursive=True)

total = {}
for fp in files:
    txt = open(fp, encoding="utf-8-sig").read()
    orig = txt
    fcount = {}
    for pat, repl in patterns:
        txt, n = pat.subn(repl, txt)
        if n:
            fcount[pat.pattern] = n
    if txt != orig:
        # preserve original encoding (write utf-8 without BOM to be safe for pdx)
        open(fp, "w", encoding="utf-8").write(txt)
        rel = os.path.relpath(fp, MOD)
        for k, n in fcount.items():
            total[k] = total.get(k, 0) + n
        print(f"[edit] {rel}: {sum(fcount.values())} replacements")

print("\n=== totals per token ===")
for k in sorted(total):
    # show the human key, not the regex
    name = re.sub(r"\(\?<!\[\\w-\]\)|\(\?!\[\\w-\]\)|\\", "", k)
    print(f"  {name}: {total[k]}")
print(f"\ntotal replacements: {sum(total.values())}")

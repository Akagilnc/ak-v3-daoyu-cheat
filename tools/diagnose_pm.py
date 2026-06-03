import re, glob, os

GAME = r"G:/SteamLibrary/steamapps/common/Victoria 3/game"
MOD  = r"D:/WorkSpace/V3/daoyu_cheat"

def read(p): return open(p, encoding="utf-8-sig", errors="replace").read()

# game pm ids
g_pm = set()
for fp in glob.glob(os.path.join(GAME, "common/production_methods", "**", "*.txt"), recursive=True):
    for m in re.finditer(r"^(pm_[a-z0-9_]+)\s*=\s*\{", read(fp), re.M):
        g_pm.add(m.group(1))

# mod pm references
m_pm = set()
for fp in glob.glob(os.path.join(MOD, "**", "*.txt"), recursive=True):
    for m in re.finditer(r"\b(pm_[a-z0-9_]+)", read(fp)):
        m_pm.add(m.group(1))

# building-name renames that appear embedded in pm names
RN = {
    "building_steel_mills":"building_steel_mill","building_textile_mills":"building_textile_mill",
    "building_paper_mills":"building_paper_mill","building_chemical_plants":"building_chemical_plant",
    "building_munition_plants":"building_munition_plant","building_synthetics_plants":"building_synthetics_plant",
    "building_artillery_foundries":"building_artillery_foundry","building_tooling_workshops":"building_tooling_workshop",
    "building_furniture_manufacturies":"building_furniture_manufactory","building_automotive_industry":"building_motor_industry",
    "building_subsistence_farms":"building_subsistence_farm","building_subsistence_fishing_villages":"building_subsistence_fishing_village",
    "building_subsistence_orchards":"building_subsistence_orchard","building_subsistence_pastures":"building_subsistence_pasture",
    "building_subsistence_rice_paddies":"building_subsistence_rice_farm","building_arts_academy":"building_art_academy",
    "building_barracks":"building_barrack","building_shipyards":"building_shipyard","building_gold_fields":"building_gold_field",
}

broken = sorted(p for p in m_pm if p not in g_pm)
auto, manual = {}, []
for p in broken:
    fixed = p
    for a, b in RN.items():
        if a in fixed:
            fixed = fixed.replace(a, b)
    if fixed != p and fixed in g_pm:
        auto[p] = fixed
    else:
        manual.append(p)

print(f"游戏 pm: {len(g_pm)} | MOD 引用 pm: {len(m_pm)} | broken: {len(broken)}")
print(f"\n-- 可自动修(建筑名单数化, {len(auto)}) --")
for k, v in sorted(auto.items()): print(f"   {k}  ->  {v}")
print(f"\n-- 需手工/核对 ({len(manual)}) --")
for p in manual: print(f"   {p}")

import json
json.dump(auto, open(r"D:/WorkSpace/V3/tools/pm_rename.json", "w"), indent=2)

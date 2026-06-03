import re

MOD = r"D:/WorkSpace/V3/daoyu_cheat"

# --- 1) add missing negative legitimacy static_modifier ---
sm = MOD + r"/common/static_modifiers/daoyu_modifiers.txt"
t = open(sm, encoding="utf-8-sig").read()
anchor = """daoyu_country_legitimacy_base_add = {
	icon = gfx/interface/icons/timed_modifier_icons/modifier_statue_positive.dds
	country_legitimacy_base_add = 2
}"""
addition = anchor + """
daoyu_negative_country_legitimacy_base_add = {
	icon = gfx/interface/icons/timed_modifier_icons/modifier_statue_negative.dds
	country_legitimacy_base_add = -2
}"""
assert anchor in t, "legitimacy anchor not found"
t = t.replace(anchor, addition, 1)
open(sm, "w", encoding="utf-8", newline="\n").write(t)
print("[1] added daoyu_negative_country_legitimacy_base_add")

# --- 2) move_pop_religion_slaves: strip illegal args on the no-arg scripted effect ---
ev = MOD + r"/events/daoyu_events.txt"
t = open(ev, encoding="utf-8-sig").read()
t, n = re.subn(r"daoyu_move_pop_religion_slaves_effect\s*=\s*\{\s*RELIGION\s*=\s*[a-z_]+\s*\}",
               "daoyu_move_pop_religion_slaves_effect = yes", t)
open(ev, "w", encoding="utf-8", newline="\n").write(t)
print(f"[2] move_pop_religion_slaves calls fixed: {n}")

# --- 3) force_resource_discovery: building_group -> building (1.13) ---
bg2building = {
    "bg_rubber": "building_rubber_plantation",
    "bg_oil_extraction": "building_oil_rig",
    "bg_banana_plantations": "building_banana_plantation",
    "bg_gold_mining": "building_gold_mine",
    "bg_opium_plantations": "building_opium_plantation",
    "bg_tobacco_plantations": "building_tobacco_plantation",
}
t = open(ev, encoding="utf-8-sig").read()
total = 0
for bg, bld in bg2building.items():
    # only the argument of force_resource_discovery, NOT has_potential_resource
    t, n = re.subn(r"(force_resource_discovery\s*=\s*)" + bg + r"\b", r"\g<1>" + bld, t)
    total += n
open(ev, "w", encoding="utf-8", newline="\n").write(t)
print(f"[3] force_resource_discovery args fixed: {total}")

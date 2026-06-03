import re

MOD = r"D:/WorkSpace/V3/daoyu_cheat"

# ---- 1) num_effect: comment out the urban_center build entry (auto-placed, can't create) ----
nf = MOD + r"/common/scripted_effects/daoyu_num_effect.txt"
t = open(nf, encoding="utf-8-sig").read()
old = 'daoyu_create_building = { TYPE = "building_urban_center" LEVEL = $NUM$ }#城镇中心'
new = '#building_urban_center 是1.13自动放置建筑,无法手动create_building,已禁用# ' + old
assert old in t, "urban_center num_effect line not found"
t = t.replace(old, new, 1)
open(nf, "w", encoding="utf-8", newline="\n").write(t)
print("[1] num_effect urban_center entry disabled")

# ---- 2) events: skyscraper journal cheat — drop the two urban_center create_building ----
ev = MOD + r"/events/daoyu_events.txt"
t = open(ev, encoding="utf-8-sig").read()
cb = "create_building = { building = building_urban_center level = 20 }"
cnt = t.count(cb)
# replace with a no-op comment so surrounding blocks stay valid
t = t.replace(cb, "tooltip = no # 1.13: urban_center 自动管理,无法手动建造(原作弊已失效)")
open(ev, "w", encoding="utf-8", newline="\n").write(t)
print(f"[2] events urban_center create_building removed: {cnt}")

# ---- 3) RESTORE reserves = 1 on all legit create_building (undo the earlier wrong deletion) ----
# match create_building blocks that have building+level and NO nested braces (i.e. not add_ownership form),
# and currently lack reserves -> append reserves = 1
import glob, os
files = glob.glob(os.path.join(MOD, "common", "**", "*.txt"), recursive=True) + \
        glob.glob(os.path.join(MOD, "events", "**", "*.txt"), recursive=True)
pat = re.compile(r"(create_building\s*=\s*\{[^{}]*?\blevel\s*=\s*[A-Za-z0-9_$]+)(\s*\})")
total = 0
for fp in files:
    s = open(fp, encoding="utf-8-sig").read()
    def repl(m):
        global total
        if "reserves" in m.group(1):
            return m.group(0)
        total += 1
        return m.group(1) + " reserves = 1" + m.group(2)
    s2 = pat.sub(repl, s)
    if s2 != s:
        open(fp, "w", encoding="utf-8", newline="\n").write(s2)
print(f"[3] reserves = 1 restored on {total} create_building calls")

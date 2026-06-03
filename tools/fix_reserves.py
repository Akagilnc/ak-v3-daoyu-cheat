import os, re, glob

MOD = r"D:/WorkSpace/V3/daoyu_cheat"

# 1.13 removed the `reserves` parameter from create_building.
# Delete `reserves = <int>` tokens. Word-boundary guard avoids cash_reserves/army_reserves/gold_reserves.
pat = re.compile(r"(?<![\w])reserves\s*=\s*\d+\s*")

files = glob.glob(os.path.join(MOD, "common", "**", "*.txt"), recursive=True) + \
        glob.glob(os.path.join(MOD, "events", "**", "*.txt"), recursive=True)

total = 0
for fp in files:
    txt = open(fp, encoding="utf-8-sig").read()
    new, n = pat.subn("", txt)
    if n:
        open(fp, "w", encoding="utf-8", newline="\n").write(new)
        total += n
        print(f"[edit] {os.path.relpath(fp, MOD)}: removed {n}")
print(f"\ntotal `reserves` params removed: {total}")

# sanity: confirm none of the legit *_reserves words were touched
import subprocess

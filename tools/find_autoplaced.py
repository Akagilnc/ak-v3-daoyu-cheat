import os, re, glob

GAME = r"G:/SteamLibrary/steamapps/common/Victoria 3/game"
MOD  = r"D:/WorkSpace/V3/daoyu_cheat"

def read(p): return open(p, encoding="utf-8-sig", errors="replace").read()

# --- parse building_groups: name -> (parent, auto_place flag if explicitly set) ---
groups = {}
for fp in glob.glob(os.path.join(GAME, "common/building_groups", "**", "*.txt"), recursive=True):
    txt = read(fp)
    # split top-level bg blocks
    for m in re.finditer(r"^(bg_[a-z0-9_]+)\s*=\s*\{", txt, re.M):
        name = m.group(1)
        # grab block body (rough: until next top-level bg or EOF)
        start = m.end()
        nxt = re.search(r"^bg_[a-z0-9_]+\s*=\s*\{", txt[start:], re.M)
        body = txt[start: start + (nxt.start() if nxt else len(txt))]
        parent = re.search(r"parent_group\s*=\s*(bg_[a-z0-9_]+)", body)
        ap = re.search(r"auto_place_buildings\s*=\s*(yes|no)", body)
        groups[name] = {"parent": parent.group(1) if parent else None,
                        "ap": (ap.group(1) == "yes") if ap else None}

def auto_placed(bg):
    seen = set()
    while bg and bg not in seen:
        seen.add(bg)
        g = groups.get(bg)
        if not g: return False
        if g["ap"] is not None: return g["ap"]   # nearest explicit setting wins
        bg = g["parent"]
    return False

# --- parse buildings: building -> building_group ---
b2g = {}
for fp in glob.glob(os.path.join(GAME, "common/buildings", "**", "*.txt"), recursive=True):
    txt = read(fp)
    for m in re.finditer(r"^(building_[a-z0-9_]+)\s*=\s*\{", txt, re.M):
        name = m.group(1); start = m.end()
        nxt = re.search(r"^building_[a-z0-9_]+\s*=\s*\{", txt[start:], re.M)
        body = txt[start: start + (nxt.start() if nxt else len(txt))]
        bg = re.search(r"building_group\s*=\s*(bg_[a-z0-9_]+)", body)
        if bg: b2g[name] = bg.group(1)

# --- MOD building types passed to create_building paths ---
mod_types = set()
for fp in glob.glob(os.path.join(MOD, "**", "*.txt"), recursive=True):
    for m in re.finditer(r"\b(building_[a-z0-9_]+)", read(fp)):
        mod_types.add(m.group(1))

ap_buildings = {b for b, g in b2g.items() if auto_placed(g)}
print(f"游戏 auto-placed 建筑总数: {len(ap_buildings)}")
for b in sorted(ap_buildings): print("   ", b, " <-", b2g[b])

hit = sorted(b for b in mod_types if b in ap_buildings)
print(f"\n★ MOD 引用且是 auto-placed 的建筑(create_building 会报错): {len(hit)}")
for b in hit: print("   ", b, " <-", b2g[b])

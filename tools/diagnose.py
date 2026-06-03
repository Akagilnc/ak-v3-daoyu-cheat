import os, re, sys, glob, json

GAME = r"G:/SteamLibrary/steamapps/common/Victoria 3/game"
MOD  = r"D:/WorkSpace/V3/daoyu_cheat"

def read(p):
    try:
        return open(p, encoding="utf-8-sig", errors="replace").read()
    except Exception:
        return ""

def game_top_ids(subdir, prefix=""):
    """Collect top-level (column-0) `id = {` definitions from game files in subdir."""
    ids = set()
    for fp in glob.glob(os.path.join(GAME, subdir, "**", "*.txt"), recursive=True):
        for line in read(fp).splitlines():
            m = re.match(r"^([a-z][a-z0-9_]+)\s*=\s*\{", line)
            if m and (not prefix or m.group(1).startswith(prefix)):
                ids.add(m.group(1))
    return ids

def mod_tokens(pattern):
    toks = set()
    for fp in glob.glob(os.path.join(MOD, "**", "*.txt"), recursive=True):
        for m in re.finditer(pattern, read(fp)):
            toks.add(m.group(1))
    return toks

# ---- game legal sets ----
g_build = game_top_ids("common/buildings", "building_")
g_tech  = game_top_ids("common/technology/technologies")
g_law   = game_top_ids("common/laws", "law_")
g_cult  = game_top_ids("common/cultures")

# ---- mod references ----
m_build = mod_tokens(r"\b(building_[a-z0-9_]+)")
m_tech  = mod_tokens(r"(?:add|has|can_research)_technology(?:_researched)?\s*=\s*([a-z0-9_]+)") \
          | mod_tokens(r"\btechnology\s*=\s*([a-z0-9_]+)")
m_law   = mod_tokens(r"law_type:(law_[a-z0-9_]+)")
m_cult  = mod_tokens(r"\bcu:([a-z0-9_]+)") | mod_tokens(r"culture\s*=\s*cu:([a-z0-9_]+)")

def singular_candidates(t):
    c = []
    if t.endswith("ies"): c.append(t[:-3] + "y")
    if t.endswith("s"):   c.append(t[:-1])
    if t.endswith("es"):  c.append(t[:-2])
    return c

def report(name, gset, mset, try_singular=False):
    missing_in_game = sorted(mset - gset)   # mod uses, game lacks -> broken
    rename = {}
    unresolved = []
    for t in missing_in_game:
        hit = None
        if try_singular:
            for c in singular_candidates(t):
                if c in gset:
                    hit = c; break
        if hit: rename[t] = hit
        else: unresolved.append(t)
    print(f"\n===== {name} =====")
    print(f"game defines: {len(gset)} | mod references: {len(mset)} | broken(mod uses/game lacks): {len(missing_in_game)}")
    if rename:
        print(f"-- auto-rename map ({len(rename)}) --")
        for k,v in sorted(rename.items()): print(f"   {k}  ->  {v}")
    if unresolved:
        print(f"-- UNRESOLVED ({len(unresolved)}) [need manual: deleted/renamed/noise] --")
        for t in unresolved: print(f"   {t}")
    return rename

maps = {}
maps["building"] = report("BUILDINGS", g_build, m_build, try_singular=True)
maps["tech"]     = report("TECHNOLOGY", g_tech, m_tech, try_singular=True)
maps["law"]      = report("LAWS", g_law, m_law, try_singular=False)
report("CULTURES", g_cult, m_cult, try_singular=False)

json.dump(maps, open(r"D:/WorkSpace/V3/tools/rename_map.json","w"), indent=2)
print("\n[written] tools/rename_map.json")

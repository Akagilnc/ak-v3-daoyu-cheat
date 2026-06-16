#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""静态回归门 —— 全自动、零误报(只查自洽 + 确认死名,不依赖不完整的 modifier oracle)。

三类检查:
  1. 花括号平衡           —— 每个脚本文件 { 与 } 配平(剥注释)
  2. modifier 开关接线一致 —— 每个 BUFFVAR 的 daoyu_<X> / daoyu_negative_<X> 都有定义
  3. 死名黑名单           —— 本季确认在 1.13 报错的名字不再出现(锁死已修 bug)

不查的(故意):modifier 类型是否 1.13 合法 —— 无完整 oracle,会误报;那一类交给 check_errorlog.py(游戏才是权威)。

退出码 0 = 通过;1 = 有问题。
用法: python tools/check.py
"""
import re, sys, pathlib

MOD = pathlib.Path(__file__).resolve().parent.parent / "daoyu_cheat"
SCRIPT_DIRS = [MOD / "common", MOD / "events"]

def script_files():
    for d in SCRIPT_DIRS:
        yield from d.rglob("*.txt")

def read(p):
    return p.read_text(encoding="utf-8-sig", errors="replace")

def strip_comment(line):
    h = line.find("#")
    return line if h < 0 else line[:h]

# ---- 1. 花括号平衡 ----
def check_braces():
    bad = []
    for p in script_files():
        o = c = 0
        for line in read(p).splitlines():
            s = strip_comment(line)
            o += s.count("{"); c += s.count("}")
        if o != c:
            bad.append(f"{p.relative_to(MOD)}: {{={o} }}={c}")
    return bad

# ---- 2. modifier 开关接线 ----
def check_wiring():
    eff = read(MOD / "common" / "scripted_effects" / "daoyu_effects.txt")
    buffvars = sorted(set(re.findall(r"BUFFVAR = ([a-z_0-9]+)", eff)))
    defined = set()
    for f in [MOD / "common" / "modifiers" / "daoyu_modifiers.txt",
              MOD / "common" / "static_modifiers" / "daoyu_modifiers.txt"]:
        defined |= set(re.findall(r"^(daoyu_[a-z_0-9]+) = \{", read(f), re.M))
    bad = []
    for b in buffvars:
        if f"daoyu_{b}" not in defined:
            bad.append(f"BUFFVAR {b}: 缺正面 modifier daoyu_{b}")
        if f"daoyu_negative_{b}" not in defined:
            bad.append(f"BUFFVAR {b}: 缺负面 modifier daoyu_negative_{b}")
    return buffvars, bad

# ---- 3. 死名黑名单(本季确认 1.13 报错过的,用具体模式避免误伤合法用法)----
BLOCKLIST = [
    (r"country_convoys_capacity_add",            "1.13 已删 modifier(→ goods_output_merchant_marine_add)"),
    (r"political_movement_radicalism_mult",      "1.13 无此 modifier(→ _add)"),
    (r"should_be_pinned_by_default",             "1.13 已删 JE 字段"),
    (r"\bexpecting_riches_less\b",               "modifier 不存在(→ expecting_riches)"),
    (r"has_pop_culture = scope:",                "has_pop_culture 不接受 scope(→ culture = scope:)"),
    (r"placement = daoyu_cheat",                 "placement 要 scope 不是 title key(→ ROOT)"),
    (r"has_journal_entry = je_coup",             "je_coup 1.13 不存在"),
    (r"has_discrimination_trait = (lusophone|hispanophone|francophone|anglophone)\b", "语言特征要加 language_ 前缀"),
    (r"STATE_(SILESIA|GAMBIA|GHANA|CUBA|CHUBU|ANDALUSIA|CASTILE|TOLEDO|NAVARRA|GRANADA|BADAJOZ|BALEARES|WEST_SLOVAKIA|EAST_SLOVAKIA|NORTHERN_SERBIA|SOUTHERN_SERBIA)\b", "1.13 已改名/拆分的州"),
]

def check_blocklist():
    hits = []
    pats = [(re.compile(p), why) for p, why in BLOCKLIST]
    for p in script_files():
        for i, line in enumerate(read(p).splitlines(), 1):
            s = strip_comment(line)
            for rx, why in pats:
                if rx.search(s):
                    hits.append(f"{p.relative_to(MOD)}:{i}  [{rx.pattern[:30]}] {why}")
    return hits

def main():
    ok = True
    braces = check_braces()
    print(f"[1] 花括号平衡: {'OK' if not braces else '❌ '+str(len(braces))+' 个文件不配平'}")
    for b in braces: print(f"      {b}");
    ok &= not braces

    buffvars, wiring = check_wiring()
    print(f"[2] 开关接线: 检查 {len(buffvars)} 个 BUFFVAR — {'OK' if not wiring else '❌ '+str(len(wiring))+' 处断线'}")
    for w in wiring: print(f"      {w}")
    ok &= not wiring

    block = check_blocklist()
    print(f"[3] 死名黑名单: {'OK 无死名' if not block else '❌ '+str(len(block))+' 处死名复发'}")
    for h in block: print(f"      {h}")
    ok &= not block

    print("\n" + ("✅ 全部通过" if ok else "❌ 有问题,见上"))
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())

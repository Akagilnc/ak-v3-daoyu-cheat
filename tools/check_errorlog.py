#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""权威回归门 —— 解析游戏 error.log,断言无「真·结构性报错」。

游戏引擎是 modifier/trigger/state 等是否合法的唯一完整判据。流程:
  纯 daoyu 启动 → 主菜单 → 退出 → python tools/check_errorlog.py

把报错分两类:
  - 真错(应为 0):Unknown/Invalid/Unexpected/Failed/No default option/Flavor 重复
  - 不可约噪音(忽略):Unrecognized loc key、investment_pool(vanilla)、
    Missing expected culture static modifier(占位 hack 文化,见 ADR/CONTEXT)

退出码 0 = 干净(只剩噪音);1 = 有真错。
用法: python tools/check_errorlog.py [可选 error.log 路径]
"""
import re, sys, pathlib

DEFAULT_LOG = pathlib.Path.home() / "Documents" / "Paradox Interactive" / "Victoria 3" / "logs" / "error.log"

# 不可约噪音:出现这些子串的行直接忽略
NOISE = [
    "Unrecognized loc key",
    "custom_tooltip effect [ Unknown loc key",   # 字面 label(日期/ep1_content),纯显示
    "directly_controlled_investment_pool",
    "autonomous_investment_pool",
    "Missing expected culture static modifier",
]

# 真错签名:命中即计入(全类扫,不只挑几个——本季教训)。
# 不收 "Script system error" 头行(冗余),只认其后的 Error: 明细 + 解析错。
REAL = [
    "Unknown trigger type", "Unknown effect type", "Unknown modifier type",
    "Invalid database object", "Invalid production method",
    "Unexpected token", "Failed to find a valid event target", "Failed to read",
    "No default option", "Flavor description already read",
    "create_pop effect [ Missing culture",
    "create_building effect [ Both levels",
    "Not found in database",        # add_modifier name / diplomatic pact type
]

def main():
    log = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_LOG
    if not log.exists():
        print(f"找不到 error.log: {log}\n（先进游戏跑一次,或把路径作参数传入）")
        return 2
    real = {}
    total_lines = 0
    for line in log.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        total_lines += 1
        if any(n in line for n in NOISE):
            continue
        for sig in REAL:
            if sig in line:
                real.setdefault(sig, []).append(line.strip()[:160])
                break
    print(f"error.log: {total_lines} 行,已忽略不可约噪音")
    if not real:
        print("✅ 无真·结构性报错(只剩噪音)")
        return 0
    n = sum(len(v) for v in real.values())
    print(f"\n❌ {n} 条真报错,按类:")
    for sig, lines in sorted(real.items(), key=lambda x: -len(x[1])):
        print(f"  [{len(lines):3}] {sig}")
        for l in lines[:3]:
            print(f"        {l}")
        if len(lines) > 3:
            print(f"        … 还有 {len(lines)-3} 条")
    return 1

if __name__ == "__main__":
    sys.exit(main())

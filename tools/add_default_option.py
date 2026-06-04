#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给缺少 default_option 的事件块安全添加 default_option=yes。
逐事件块(顶层 X = { ... })解析:
  - 该块含至少一个 option = {  且  全块不含 default_option = yes  -> 需要加
  - 优先加在 RESIGN 选项的 name 行后(取消项=最安全默认),否则加在第一个 option 的 name 行后
已有 default_option 的事件跳过,避免双默认。
注释(# 后)在计算花括号深度时剥离。
用法: python add_default_option.py <file> [--apply]
"""
import re, sys

def strip_comment(line):
    # Paradox 用 # 起注释;假定不在引号内出现(本mod路径/颜色无#)
    h = line.find('#')
    return line if h < 0 else line[:h]

def brace_delta(line):
    s = strip_comment(line)
    return s.count('{') - s.count('}')

EVENT_HEAD = re.compile(r'^\s*[\w.]+\s*=\s*\{')
OPTION_HEAD = re.compile(r'^\s*option\s*=\s*\{')
DEFAULT_OPT = re.compile(r'\bdefault_option\s*=\s*yes\b')
NAME_RESIGN = re.compile(r'^\s*name\s*=\s*RESIGN\b')
NAME_ANY    = re.compile(r'^\s*name\s*=')

def find_event_blocks(lines):
    """返回顶层事件块 [(start_idx, end_idx_inclusive)]"""
    blocks = []
    depth = 0
    start = None
    for i, line in enumerate(lines):
        d = brace_delta(line)
        if depth == 0 and start is None and EVENT_HEAD.search(line) and d > 0:
            start = i
        depth += d
        if start is not None and depth == 0:
            blocks.append((start, i))
            start = None
    return blocks

def process(path, apply):
    with open(path, encoding='utf-8-sig') as f:
        lines = f.readlines()
    blocks = find_event_blocks(lines)
    insert_after = []  # 行号(0-based),在其后插入
    for s, e in blocks:
        body = lines[s:e+1]
        has_option = any(OPTION_HEAD.search(l) for l in body)
        has_default = any(DEFAULT_OPT.search(l) for l in body)
        if not has_option or has_default:
            continue
        # 选插入位置:优先 RESIGN 的 name 行,否则第一个 option 的 name 行
        target = None
        for idx in range(s, e+1):
            if NAME_RESIGN.search(lines[idx]):
                target = idx
                break
        if target is None:
            in_opt = False
            for idx in range(s, e+1):
                if OPTION_HEAD.search(lines[idx]):
                    in_opt = True
                if in_opt and NAME_ANY.search(lines[idx]):
                    target = idx
                    break
        if target is None:
            print(f"  [跳过] 块 {lines[s].strip()[:40]} 有option但找不到name行")
            continue
        insert_after.append(target)
    # 报告
    head = lambda i: next((lines[j].strip() for j in range(i,-1,-1) if EVENT_HEAD.search(lines[j])), '?')
    print(f"{path}: 需添加 {len(insert_after)} 处")
    for t in insert_after:
        print(f"  事件 {head(t)[:34]:36} <- 在第{t+1}行 ({lines[t].strip()}) 后加 default_option")
    if apply and insert_after:
        # 从后往前插,避免行号位移
        for t in sorted(insert_after, reverse=True):
            indent = re.match(r'^(\s*)', lines[t]).group(1)
            lines.insert(t+1, f"{indent}default_option = yes\n")
        with open(path, 'w', encoding='utf-8-sig', newline='') as f:
            f.writelines(lines)
        print(f"  -> 已写入 {len(insert_after)} 处")

if __name__ == '__main__':
    files = [a for a in sys.argv[1:] if not a.startswith('--')]
    apply = '--apply' in sys.argv
    for p in files:
        process(p, apply)

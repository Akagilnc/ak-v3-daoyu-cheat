import re, glob, os

MOD = r"D:/WorkSpace/V3/daoyu_cheat"

# 具体 scope(scope:xxx / owner / capital / this / root / prev / overlord) 里直接用 limit 当守卫,
# 1.13 不合法(报 Unknown effect limit)。改成 scope = { if = { limit = {...} <effects> } }
SCOPE_PAT = re.compile(r'(?:scope:[\w.:]+|ig:[\w]+|cu:[\w]+|rel:[\w]+|owner|capital|this|root|prev|overlord)\s*=\s*\{')

def fix_text(text):
    inserts = []  # (pos, str)
    for m in SCOPE_PAT.finditer(text):
        bo = m.end() - 1  # '{' 位置
        # 跳过空白看第一个子句是否 limit
        j = bo + 1
        while j < len(text) and text[j] in ' \t\r\n': j += 1
        if text[j:j+5] != 'limit' or (j+5 < len(text) and (text[j+5].isalnum() or text[j+5]=='_')):
            continue
        # 括号匹配找 scope 块闭合 }
        depth = 1; k = bo + 1
        while k < len(text) and depth > 0:
            if text[k] == '{': depth += 1
            elif text[k] == '}': depth -= 1
            k += 1
        bc = k - 1  # 闭合 '}' 位置
        inserts.append((bo + 1, ' if = {'))   # '{' 后插入
        inserts.append((bc, ' }'))            # '}' 前插入
    # 从后往前插入避免位移
    for pos, s in sorted(inserts, key=lambda x: -x[0]):
        text = text[:pos] + s + text[pos:]
    return text, len(inserts)//2

total = 0
for fp in glob.glob(os.path.join(MOD, "**", "*.txt"), recursive=True):
    s = open(fp, encoding="utf-8").read()
    new, n = fix_text(s)
    if n:
        # brace 平衡校验(插入成对,应保持平衡)
        if new.count('{') == new.count('}'):
            open(fp, "w", encoding="utf-8", newline="\n").write(new)
            total += n
            print(f"  {os.path.relpath(fp, MOD)}: 包裹 {n} 处")
        else:
            print(f"  ★ {os.path.relpath(fp, MOD)}: brace不平衡,跳过!")
print(f"\n共包裹 scope内limit: {total}")

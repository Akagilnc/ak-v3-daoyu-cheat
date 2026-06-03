import re, glob, os

MOD = r"D:/WorkSpace/V3/daoyu_cheat"

# 1.13 removed is_ruler / is_heir triggers -> use has_role = character_role_*
# X = yes  -> has_role = character_role_X
# X = no   -> NOT = { has_role = character_role_X }
subs = [
    (re.compile(r"\bis_ruler\s*=\s*yes\b"), "has_role = character_role_ruler"),
    (re.compile(r"\bis_ruler\s*=\s*no\b"),  "NOT = { has_role = character_role_ruler }"),
    (re.compile(r"\bis_heir\s*=\s*yes\b"),  "has_role = character_role_heir"),
    (re.compile(r"\bis_heir\s*=\s*no\b"),   "NOT = { has_role = character_role_heir }"),
]

total = 0
for fp in glob.glob(os.path.join(MOD, "**", "*.txt"), recursive=True):
    s = open(fp, encoding="utf-8").read()
    o = s
    for pat, repl in subs:
        s, n = pat.subn(repl, s)
        total += n
    if s != o:
        open(fp, "w", encoding="utf-8", newline="\n").write(s)

# sanity
left = 0
for fp in glob.glob(os.path.join(MOD, "**", "*.txt"), recursive=True):
    left += len(re.findall(r"\bis_(ruler|heir)\s*=", open(fp, encoding="utf-8").read()))
print(f"is_ruler/is_heir 替换: {total}, 残留: {left}")

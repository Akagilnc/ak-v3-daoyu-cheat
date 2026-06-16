# Domain Docs

工程类 skill 探索代码前,该如何消费本仓库的领域文档。

## 探索前先读

- 根目录 **`CONTEXT.md`**
- **`docs/adr/`** —— 读与当前改动相关区域的 ADR

文件不存在就静默继续,别提示缺失(`/grill-with-docs` 会在术语/决策真正定下来时按需创建)。

## 文件结构(单上下文)

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-convoy-cheat-goods-output.md
│   ├── 0002-naming-convention-daoyu-ak.md
│   └── 0003-removed-content-deletion-strategy.md
├── daoyu_cheat/        ← mod 本体(真相源)
└── tools/              ← python 诊断脚本
```

## 用术语表的词汇

输出里命名领域概念(issue 标题、重构提案、假设、测试名)时,用 `CONTEXT.md` 里定义的词。概念不在术语表里 = 信号:要么你在造项目不用的说法(重新考虑),要么是真缺口(记给 `/grill-with-docs`)。

## ADR 冲突要明说

输出若和现有 ADR 矛盾,显式指出,别静默推翻:

> _与 ADR-0001(convoy 用 goods_output)冲突,但值得重开因为……_

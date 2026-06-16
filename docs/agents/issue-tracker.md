# Issue tracker: GitHub

Issues 和 PRD 以 GitHub issues 形式存放于 `Akagilnc/ak-v3-daoyu-cheat`。所有操作用 `gh` CLI(在 clone 内运行时自动识别仓库)。

## Conventions

- **建 issue**:`gh issue create --title "..." --body "..."`(多行 body 用 heredoc)
- **读 issue**:`gh issue view <number> --comments`
- **列 issue**:`gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`,按需加 `--label` / `--state`
- **评论**:`gh issue comment <number> --body "..."`
- **加/去标签**:`gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **关闭**:`gh issue close <number> --comment "..."`

## When a skill says "publish to the issue tracker"

建一个 GitHub issue。

## When a skill says "fetch the relevant ticket"

`gh issue view <number> --comments`。

## 本项目补充

- Bug 来源常是玩家在 Steam Workshop / P社评论区反馈,或自己实玩抓 `error.log`。把这类反馈整理成 issue 时,贴上原始报错行 + 触发的作弊功能。
- 加载期报错 vs 运行期报错要区分(见 `CONTEXT.md`),issue 里注明是哪类。

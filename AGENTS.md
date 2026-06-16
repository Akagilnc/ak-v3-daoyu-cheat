# ak-v3-daoyu-cheat — Agent Guide

Victoria 3 作弊 MOD **「Daoyu Cheat 刀鱼作弊」** 的社区维护版,适配 **1.13.x (Matcha)**。
纯脚本(无 DLL)。原作者:刀鱼作弊 / 贴心小D.VA(已停更)。本仓库由 **akagilnc** 接手维护。

- **真相源**:`daoyu_cheat/`(mod 本体)。`game_docs_113/`(1.13 script_docs 导出参考)和 `.claude/` 已 git 忽略。
- **领域语言、子系统、工作流**:见 `CONTEXT.md`
- **架构/设计决策**:见 `docs/adr/`

## Agent skills

### Issue tracker

Issues 和 PRD 以 **GitHub issues** 形式存放于 `Akagilnc/ak-v3-daoyu-cheat`,统一用 `gh` CLI 操作。见 `docs/agents/issue-tracker.md`。

### Triage labels

实际启用 4 个标签:`needs-triage` / `needs-info` / `ready-for-agent` / `wontfix`。
`ready-for-human` 单人项目不用(无对应 GitHub 标签)。见 `docs/agents/triage-labels.md`。

### Domain docs

单上下文:根目录一份 `CONTEXT.md` + `docs/adr/`。见 `docs/agents/domain.md`。

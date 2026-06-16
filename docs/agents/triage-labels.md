# Triage Labels

skills 用五个标准 triage 角色;下表映射到本仓库实际使用的标签。

| Role in mattpocock/skills | 本仓库标签 | 含义 |
| --- | --- | --- |
| `needs-triage` | `needs-triage` | 维护者待评估 |
| `needs-info` | `needs-info` | 等报告者补充信息 |
| `ready-for-agent` | `ready-for-agent` | 规格齐全,AFK agent 可直接接手 |
| `ready-for-human` | **(不用)** | 单人项目,「需人工」即维护者本人,不单设标签 |
| `wontfix` | `wontfix` | 不予处理 |

skill 提到某角色时,用上表对应的标签字符串。

**`ready-for-human` 说明**:本仓库单人维护,「需人工实现」和「维护者自己做」是一回事,故未在 GitHub 建此标签。真遇到只能人工判断、AFK agent 接不了的活,留 `needs-triage` 或直接处理,别去贴一个不存在的标签。

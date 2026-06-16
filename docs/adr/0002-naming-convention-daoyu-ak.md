# ADR-0002 — 命名约定 daoyu_ / ak_ 与共享 modifier 引擎

状态:已采纳(2026-06-16)

## 背景

原作者所有标识符用 `daoyu_` 前缀。akagilnc 接手后想区分自己的改动。同时存在一个核心共享宏 `daoyu_add_or_remove_single_modifiers`。

## 共享引擎是什么

`common/scripted_effects/daoyu_effects.txt` 的 `daoyu_add_or_remove_single_modifiers` 是「同构数值开关作弊」的**表驱动引擎**:
- 参数 `BUFFVAR`(modifier 名后缀)+ `MULTIPLIER`(叠加量)。
- 读控制旗标全局变量决定加/删,操作三样:`daoyu_$BUFFVAR$`(正)、`daoyu_negative_$BUFFVAR$`(负)、`daoyu_$BUFFVAR$`(选中标记全局变量)。
- 包装 `daoyu_all_country_modifiers_effect` 对全部 ~15 个 modifier 各调一次;玩家选哪个就给哪个打标,只有被选中的生效。
- **`daoyu_` 在引擎里硬编码约 8 处**(has/add/remove_modifier、has/remove_global_variable)。
- 目的:DRY + 行为统一(开关/叠加/正负/一键全清)+ 极低扩展成本(加 1 行 vs 复制 15 行)。

## 决策

- **新增独立功能**(新事件/机制/文件)→ `ak_` 前缀,天然区分。
- **嵌在 daoyu_ 命名体系/共享宏里的**(凡走上面那个引擎的 modifier)→ 保持 `daoyu_`。改名会和硬编码的 `daoyu_$BUFFVAR$` 脱钩、整条作弊失效。
- 「区分」的价值在「新子系统 = ak_」,不是把别人架构里的螺丝逐个改名。

## 加新作弊的两条路径

- **同构数值开关**(给某 country/state modifier 加值)→ 进引擎(加 1 行 BUFFVAR + 配套),保持 daoyu_。
- **异构/一次性**(新机制、复杂逻辑、非 modifier 动作)→ 独立写(Option C),叫 ak_,不碰引擎。

## 暂不做:全量 daoyu_→ak_ 改名

有内在矛盾:「ak_ 区分我的改动」需要 daoyu_ 还在;「全换 ak_」会让区分消失。且和「社区维护版、保留原作者署名」的定性冲突。**目前不做**;真要做,等 mod 稳定后一次性脚本改 + 全验证。

## Option A 触发条件(待办)

若将来要加**走这引擎的 ak_ modifier 作弊**,再把引擎参数化前缀(加 `$PREFIX$` 参数,8 处硬编码 daoyu_ 改 `$PREFIX$`,全部现有调用补 `PREFIX=daoyu_`)。**在此之前不做**(YAGNI + 不在发布后求稳期动核心引擎)。

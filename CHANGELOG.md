# Changelog

All notable changes to this community-maintained 1.13.x port.
本社区维护版(Victoria 3 1.13.x)的更新记录。

---

## 2026.06.24 (1.13)

**English**
- **National Power Blocs — major additions.**
  - New: **Form your own power bloc** from the cheat menu and instantly become its leader — pick any of 5 identities, including the new **Cultural Commonwealth** (1.13). (Previously the `create_power_bloc` effect existed but was never wired to a menu.)
  - Principles now cover **all 23 vanilla groups** (added **Shared Canon** and **Maritime Supremacy**).
  - Principle menu now **paginates** (Next / Previous page) instead of one over-long list.
- **New-version content.**
  - Technology: added **Pre-Dreadnought**.
  - Cultures: added **13 missing cultures** (Filipino group, Iberian group, Ryukyuan, Scottish Gaelic, Griqua, Promethean, etc.).
- **Quality of life.**
  - **Expand-Factory** menu now paginates — the buildings at the bottom are reachable again.
  - Cleaner main-menu header (dropped stale leftover text).
- **Fixes.**
  - **Supply-Ship Construction cheat** was the allocation **ratio** (only reassigns existing ship construction); now boosts supply-ship construction **efficiency** so supply ships actually build faster.
  - Stopped a power-bloc naming error-log flood; fixed culture-menu `Unknown trigger type` errors.

**中文**
- **国家集团 — 大改。**
  - 新增 **「组建国家集团」**:从作弊菜单凭空建集团并当领袖,5 种认同任选(含 1.13 新增 **「文化共同体」**)。(原 `create_power_bloc` 效果已存在却从未接进菜单。)
  - 集团原则补全:现覆盖 **vanilla 全部 23 组**(补 **「共同准则」** 和 **「海上霸权」**)。
  - 原则菜单改 **翻页**(下一页/上一页),不再一长条排不下。
- **新版本内容补全。**
  - 科技:补 **「前无畏舰」**。
  - 文化:补 **13 个新文化**(菲律宾系、伊比利亚系、琉球、盖尔、格里夸、普罗米修斯等)。
- **体验改进。**
  - **「扩建工厂」** 菜单改翻页,底部工厂够得着了。
  - 主菜单说明精简(去掉过时遗留文字)。
- **修复。**
  - **「补给船建造力」** 原来加的是**分配比例**(只是把现有船舶建造力重新分配),改为**建造效率**,补给船真正造得更快。
  - 集团命名导致的 error.log 刷屏;文化菜单 `Unknown trigger type` 报错。

---

## 2026.06.17 (1.13)

**English**
- **New cheat — Supply Ship Construction.** Massively boost navy supply-ship construction (country-wide) from the Country Modifiers menu.
- **Restored the Automotive Industry building** (a separate building in 1.13) across all cheat menus: expand / remove / monopoly / nationalize / state trait / build / production methods.
- **Removed the "Add Merchant Ships / Convoys" cheat.** 1.13 has no clean cheat-modifier way to boost convoys, and the existing Throughput state cheat already raises port output.
- **Publishing cleanup**: ASCII mod folder, identity aligned to the Workshop title, multiplayer_synchronized enabled.
- **New thumbnail artwork**; English-friendly store title + full bilingual description.
- Several cheat values buffed.

**中文**
- **新增作弊 —「补给船建造力」。** 在「国家修正」菜单大幅提升海军补给船建造(全国生效)。
- **补回「汽车厂」建筑**(1.13 独立建筑),补全扩建/移除/垄断/国有化/状态特征/建造/生产方式各菜单。
- **移除「增加商船(护航舰队)」作弊。** 1.13 没有干净的作弊修正能提升护航舰队,且现有「吞吐量」地区作弊已能提港口产出。
- **发布规范化**:mod 目录改纯 ASCII、身份对齐线上标题、开启 multiplayer_synchronized。
- **更换封面图**;英文友好商店标题 + 双语描述。
- 部分作弊数值增强。

---

## 2026.06.04 (1.13) — Initial 1.13.x port / 首个 1.13 适配版

**English**
- Community-maintained port of **"Daoyu Cheat - Achievement Available Cheat Tool"** (original author: 刀鱼作弊 / 贴心小D.VA) to Victoria 3 1.13.x.
- The original no longer loaded on 1.13; this version restores load-time compatibility: fixed parser errors, renamed/split states, removed/renamed production methods, modifiers, triggers, discrimination traits, and journal entries.
- Loads cleanly on 1.13. Script-only, no DLL. All original design and credit retained.

**中文**
- 将 **「Daoyu Cheat - Achievement Available Cheat Tool」**(原作者:刀鱼作弊 / 贴心小D.VA)社区维护移植到 Victoria 3 1.13.x。
- 原版已无法在 1.13 加载;本版恢复加载期兼容:修复解析错误、改名/拆分的州、移除/改名的生产方式、modifier、trigger、歧视特征、日志条目等。
- 1.13 加载干净。纯脚本,无 DLL。保留原作者全部设计与署名。

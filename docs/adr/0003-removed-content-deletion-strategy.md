# ADR-0003 — 1.13 已删内容的处理:整套删除,不强行 merge

状态:已采纳(2026-06)

## 背景

1.13 删除/改名了一批 vanilla 对象,原 mod 深度集成了它们,加载报 `Invalid database object` / `Invalid production method` / `Unknown trigger` 等。

## 决策

按对象类型分别处理:

### 已删的独立建筑 → 整套删除集成
- `building_naval_base`、`building_military_shipyard` 1.13 已删,其 PM 组(`pmg_naval_theory` / `pmg_military_base`)无任何建筑引用。
- 把 mod 里对这些建筑的 PM 激活**整段删除**,不 merge 到别的建筑(避免重复触发)。
- 注意:`building_automotive_industry` 在 1.13 **仍存在**(早期误判为已删);`pm_automobile_production` 属于它,不是 motor_industry。

### 改名/拆分的州 → 映射到 1.13 现存州(按历史首府就近取一个)
SILESIA→LOWER_SILESIA、WEST/EAST_SLOVAKIA→SLOVAKIA、NORTHERN_SERBIA→WESTERN_SERBIA、SOUTHERN_SERBIA→EASTERN_SERBIA、GAMBIA→SENEGAL、GHANA→GOLD_COAST、CUBA→WESTERN_CUBA、CHUBU→TOKAI、ANDALUSIA→LOWER_ANDALUSIA、CASTILE→OLD_CASTILE、TOLEDO→NEW_CASTILE、NAVARRA→BASQUE_COUNTRY、GRANADA→UPPER_ANDALUSIA、BADAJOZ→EXTREMADURA、BALEARES→BALEARIC_ISLANDS。

### 改名的 trigger/effect/modifier → 换 1.13 名
语言歧视特征加 `language_` 前缀;`south_asian_heritage`→`has_discrimination_trait_group=heritage_group_south_asian`;`je_coup`(1.13 无)→删该选项;等等。

### 已删的 JE/功能 → 删对应菜单选项
没有替代品的(如 je_coup)直接删选项,相关惰性 var 引用无害留存。

## 后果

- 加载期结构性报错基本清零。
- 原则:**深度集成的旧版独立内容被新版删除时,整体删除,不勉强嫁接**。嫁接会带来重复触发/语义错位。

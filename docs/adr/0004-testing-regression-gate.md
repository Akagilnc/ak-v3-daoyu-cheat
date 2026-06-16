# ADR-0004 — 测试策略:回归门,不是 TDD

状态:已采纳(2026-06-16)

## 背景

想给改动(如 convoy 作弊)补测试,并评估能否走 TDD。

## 关键判定

1. **V3 脚本 mod 无传统单元测试**:引擎不暴露测试 API,运行期效果(「应用作弊后商船真 +1000」)只能进游戏肉眼看,无法程序化断言。
2. **严格 TDD(先写失败测试→改绿)不成立**:改动前写不出能跑的失败断言。
3. **「modifier 类型是否 1.13 合法」没有完整静态 oracle**——实测:script_docs 导出的 `modifiers.log` 和 vanilla `modifier_type_definitions` **都不全**。大量合法类型(scope 前缀变体 `state_/country_/building_`、per-good `goods_output_X`、per-culture 等)是**运行时按模板动态生成**的,任何静态文件都列不全。拿它当判据会误报(实测 8 报 7 错)。**唯一完整 oracle 是游戏引擎自己(error.log)。**

## 决策:两道「回归门」

### 门 1 — 静态自洽(`tools/check.py`,全自动零误报)
只查**不依赖外部 oracle**的东西:
- 花括号平衡
- modifier 开关系统接线一致(每个 BUFFVAR 的 `daoyu_<X>` / `daoyu_negative_<X>` 都有定义)
- 死名黑名单(本季确认报错过的名字不复发——锁死已修 bug)

### 门 2 — 游戏权威(`tools/check_errorlog.py`,半自动)
纯 daoyu 启动→退出后解析 error.log,断言无真结构错;自动滤掉不可约噪音。这是 modifier/state/trigger 合法性的唯一可靠判据。

## 后果

- 这套覆盖了本季踩的几乎所有加载期 bug 类型,但**不是 TDD**——是「改完先跑两道门」的回归防线。
- convoy 改动的可测部分(接线一致 + 不用死名)被门 1 覆盖;运行期商船数值只能门 2 + 肉眼。
- **教训**:别迷信单一静态 oracle。script_docs/vanilla 定义都不全,游戏才是权威。这也是为什么先做了可行性验证才下结论(naive 校验器当场被自己的误报推翻)。

# CONTEXT — ak-v3-daoyu-cheat

Victoria 3 作弊 MOD「Daoyu Cheat 刀鱼作弊」的 1.13.x 社区维护版。本文件是领域语言 + 子系统地图,给后续维护(人或 agent)对齐用。

## 是什么 / 不是什么

- **是**:纯脚本作弊 MOD(common/ events/ gfx/ localization/),通过菜单事件给玩家施加 modifier、造国、改文化、加钱科技法律等。无 DLL、无 C++。
- **不是**:平衡/历史向 mod。它是开发者/玩家用的「秀肌肉」工具,大量 trait 用 `age > 999` 保证永不自然触发。
- 原作者刀鱼作弊已停更;本版仅做 1.13 兼容性修复,保留原设计与署名。已发布:Steam Workshop item `3742679779` + P社各一份。

## 仓库结构

| 路径 | 说明 |
| --- | --- |
| `daoyu_cheat/` | **真相源**。mod 全部内容 |
| `game_docs_113/` | 游戏控制台 `script_docs` 导出的 1.13 完整 effect/trigger/event_target/modifier 文档。**查任何 1.13 API 签名先 grep 这里,比 Wiki 可靠。** git 忽略 |
| `tools/` | python 诊断脚本(如 `add_default_option.py` 逐事件块加默认项) |

vanilla 1.13 游戏文件在 `G:\SteamLibrary\steamapps\common\Victoria 3\game`(改名/改值映射一律以 vanilla 文件为准)。

## 工作流(铁律)

1. 只改 `daoyu_cheat/`
2. `git commit`(每类一个,中文 message)
3. `cp -rf` 同步到**两个**目标:
   - 测试:`G:\SteamLibrary\steamapps\workshop\content\529340\2882576273`(原 item 的本地下载,测试用)
   - 发布:`C:\Users\Administrator\Documents\Paradox Interactive\Victoria 3\mod\Daoyu Cheat 刀鱼作弊  1.13 社区适配版`(启动器从这里上传更新)
4. 重启**纯 daoyu**(禁用其它 mod 排噪)→ 主菜单 → 退出 → 看 `Documents\...\Victoria 3\logs\error.log`
5. 沙箱会拦 cp 到仓库外目录,需用户显式授权

## 关键子系统

### modifier 开关引擎(核心)
`common/scripted_effects/daoyu_effects.txt` 里的 `daoyu_add_or_remove_single_modifiers`(表驱动)。详见 ADR-0002。
- 一大批「同构数值开关」作弊(加钱/官僚/威望/商船…)共用它。
- 加一个这类作弊 = 1 行 `BUFFVAR` + 正/负 modifier 定义 + static 标记 + loc + 菜单按钮。
- **`daoyu_` 前缀在宏里硬编码**,走这引擎的 modifier 必须叫 `daoyu_<BUFFVAR>`。

### 占位 hack 文化 `daoyu_nonexistent`
`common/cultures/00_daoyu_cultures.txt`。用于「文化清洗/标记」作弊(create_pop 造 pop + change_pop_culture 标记)。
- **已知不可约小瑕疵**:引擎不为这种纯占位文化生成 per-culture 动态 modifier 类型(`state_<culture>_standard_of_living_add` 等),所以 6 条 `Missing expected culture static modifier` 警告无法消除(手动补 static modifier 反而触发 `Unknown modifier type`,别碰)。

### 造国 `daoyu_create_country_effect.txt`
`daoyu_single_create_country_effect = { TAG STATE }` 批量造架空国。STATE 名要用 1.13 现存州(见 ADR-0003 的州改名记录)。

### 建筑作弊 `daoyu_building_effect.txt`
拉满生产方式、增删建筑。PM/建筑名随 1.13 变动(见 ADR-0003)。

## 命名约定

- **`daoyu_`** = 原作者体系 + 共享宏(硬编码,不动)
- **`ak_`** = akagilnc 后续新增的**独立**功能(新事件/机制/文件)
- 详见 ADR-0002。

## 术语表(glossary)

| 词 | 含义 |
| --- | --- |
| **BUFFVAR** | 开关引擎的参数,是 modifier 名后缀,用来拼 `daoyu_<BUFFVAR>` |
| **MULTIPLIER** | 作弊叠加倍数(玩家选的量) |
| **控制旗标** | `daoyu_add_country_modifiers` / `daoyu_remove_single_country_modifiers` / `daoyu_negative` 等全局变量,驱动引擎加还是删 |
| **加载期报错** | mod 载入时校验出的错(解析/Invalid database object/PostValidate)。本版已基本清零 |
| **运行期报错** | 实际点作弊执行 effect 时才触发的错。靠实玩/玩家反馈抓 |
| **不可约噪音** | 改不动也无害的:6 条文化 static modifier、~11 条 vanilla `investment_pool`、上千条字面 loc key(`+500`/`1x`/`80%` 等当 loc key,含特殊字符无法定义,纯显示) |

## 1.13 移植经验(踩过的坑)

- 报错**层层递进**:解析错误会淹没下游错误,修一批重启冒一批,总数往下掉。
- `s:STATE_X` scope link **不能带引号**(`s:"STATE_X"` 1.13 报 `Unknown trigger type: s:`)。
- decision 的 `ai_chance` 用 `value`;event option 的 `ai_chance` 用 `base`(两个 DB 语法不同)。
- 语言歧视特征加 `language_` 前缀;heritage 用 `has_discrimination_trait_group`。
- 多个 vanilla 州在 1.13 改名/拆分(见 ADR-0003)。
- **签名 grep 会漏整类**:抓报错要全扫 `Script system error` / `Failed` / `Missing` / `Invalid` / `Unexpected`,别只挑几个签名。
- 不确定的 API 先 grep `game_docs_113/` 或 vanilla 文件坐实,别凭记忆改。

## 检查(回归门)

V3 mod 无传统单元测试/无离线运行期断言(游戏是唯一权威校验器)。所以不是 TDD,是「回归门」。详见 ADR-0004。两道门:

- **`python tools/check.py`** —— 静态、全自动、**零误报**。查:① 花括号平衡 ② modifier 开关接线一致(15 个 BUFFVAR 的正/负 modifier 都有定义)③ 死名黑名单(本季确认 1.13 报错过的名字不复发)。改完随手跑。
- **`python tools/check_errorlog.py`** —— 权威。纯 daoyu 启动→主菜单→退出后跑,解析 error.log 断言无真结构错(自动滤掉不可约噪音:loc key / investment_pool / 6 条文化 modifier)。

**不查 modifier 类型是否 1.13 合法** —— 无完整 oracle(类型大量运行时动态生成),静态查必误报;那一类只能靠 `check_errorlog.py`(游戏说了算)。

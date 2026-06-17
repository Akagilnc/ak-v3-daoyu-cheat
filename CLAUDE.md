# CLAUDE.md — ak-v3-daoyu-cheat 关键须知

Victoria 3 作弊 MOD「Daoyu Cheat 刀鱼作弊」1.13 社区维护版(akagilnc 维护,原作者刀鱼/贴心小D.VA 已停更)。纯脚本无 DLL。**真相源 = `daoyu_cheat/`**。
入口文档:`AGENTS.md`(代理指引)、`CONTEXT.md`(领域语言/子系统/工作流)、`docs/adr/`(设计决策)。本文件只记**容易踩的坑和硬结论**,别重复那些。

回复用户一律中文。

---

## 发布身份(权威,别再混淆)

- 线上 Workshop item:**`3742679779`**(作者 Akagilnc)。原作者旧 item 是 `2882576273`,两码事。
- mod 真名:**`Daoyu Cheat (1.13 Community Port) 刀鱼作弊`**
- mod id:**`akagilnc@gmail.com-daoyu-cheat-113`**
- 中文招牌只放 metadata.json 的 `name` 字段,**不进路径**。

## 路径铁律:一律纯 ASCII 无空格

- Documents 上传目录 = `...\Victoria 3\mod\daoyu-cheat-113`(**ASCII**)。
- **非 ASCII/空格路径是 Vic3 加载地雷**:启动器看得见,但**游戏 exe 静默打不开** → 决议/探针全不出、error.log 也空(打不开不报错)。
- 历史事故:旧目录名带中文+双空格 → 决议一直不加载,排查绕了一大圈才发现根因是路径。**改 ASCII 是真修复。**
- 建任何目录/文件用 ASCII slug,中文只进内容字段(metadata name、loc、文档标题)。

## 启动器/加载机制(别对着 DB 字段瞎猜)

- 游戏靠 **`...\Victoria 3\content_load.json`** 的 `enabledMods[].path` 按**路径**加载 mod,**不是** gameRegistryId。
- launcher-v2.sqlite 里 mod 行的 `gameRegistryId=None`、`isMetadataApplied=0` 是**这台机器的常态,不是 bug**(2025 备份 DB 里正常 mod 也都是 None/0)。**别再把它们当故障去删行重建。**
- 缩略图:本地 mod 在启动器列表显示占位图是常态(云端缩略图来自 Steam CDN 链接);Workshop 页面缩略图正常即可,不影响加载。

## metadata.json 要手动双向同步

- cp 工作流只同步 `events/ common/ localization/`,**不碰 `.metadata/`**。
- 所以仓库 `daoyu_cheat/.metadata/metadata.json` 与 Documents `daoyu-cheat-113/.metadata/metadata.json` 容易漂。改 metadata 必须**两边都改**,保持一致(name/id/version/thumbnail/game_custom_data.multiplayer_synchronized=true)。

## 修正(modifier)双文件夹陷阱 ★

- **`add_modifier` 同时在 `common/modifiers/` 和 `common/static_modifiers/` 两个文件夹查名**(证据:负向修正 `daoyu_negative_*` 只定义在 static_modifiers/ 却能生效)。
- 约定:**正向**修正在 `modifiers/`,**负向**只在 `static_modifiers/`。
- **同一个名字别在两个文件夹各定义一份** —— 否则 `add_modifier` 的效果预览会把它**列两遍**(实际只生效一份,修正面板只有一条,但预览/tooltip 重复)。
- 已修事故:`daoyu_goods_output_merchant_marine_add`(增加商船)曾在 static_modifiers/ 多了个无效果空壳 → 预览重复,删空壳解决。**注意:关税/国家建造力等正向修正目前也都双注册,同样隐患,待统一清理。**

## modifier 能不能 add_modifier:先查 Mask(血泪教训)★

- 用任何 modifier 前,**先 grep `game_docs_113/modifiers.log` 看它的 `Mask:`**。
- **`Mask: goods`(`goods_output_*`、`goods_input_*`)不能用于 add_modifier 作弊产出**,两个变体都废:
  - `_mult` 变体很多货物**根本不存在**(加载期报 `Unknown modifier type`,如 `goods_output_merchant_marine_mult`)。
  - `_add` 变体能加载、tooltip 会显示「+X 商船产出」**幻影**,但**引擎不把它算进真实产出**(跑几周产量纹丝不动)—— 即「goods 修正在生产方式之外不生效」的官方限制。显示有、实际无。
- **能 add_modifier 真生效的是 `building` / `state` / `country` / `character` / `interest_group` 等 Mask**。
- ★**文件夹规矩**:`building_*` / `state_*` 类修正定义**必须放 `common/static_modifiers/`**,放 `common/modifiers/` 会 `Failed to obtain modifier from script`(modifiers/ 只认 `country_*` 类给国家用)。能用的 `daoyu_throughput_add`(building_throughput_add)就在 static_modifiers/。
- 事故(空转 4 轮才定):convoy 提港口商船产出,先后试 goods `_add`(国家)/goods 州级/building_port 在 modifiers/,全失败。**终解 = `daoyu_goods_output_merchant_marine_mult` 定义在 `static_modifiers/`、内层用 `building_port_throughput_add`(Mask building,港口专属,vanilla 公司就用它)**,挂进 `daoyu_state_add_modifier_effect` 走州级菜单 daoyu.650。代价:throughput 连带提投入(多吃货),作弊无所谓;Vic3 没有「能 add_modifier 又只提产出还真生效」的商船修正。
- 经验:**别照名字猜,先看 Mask + 确认文件夹;goods 类直接放弃,选 building_/state_ 类放 static_modifiers/。**

## loc 写法:简洁原生,先验概念键存在

- 学 vanilla:**一个干净名词 + 合法 `$concept_x$` / `@icon!` / `[GetGoods('x').GetName]`**。别堆「增加…(……产出)」这种冗余,别加解释性括号(一眼 AI 味,用户反感)。
- **写 `$concept_xxx$` 前先确认 1.13 真有这个键**(grep `game_docs_113/` 或 vanilla `localization/`)。例:`concept_convoys` **不存在**,商船是商品 `merchant_marine`,图标用 `@convoys!`。
- loc 文件必须 **utf-8 with BOM**(culture 文件尤其);用 Edit 改(保留 BOM),别用会丢 BOM 的写法。

## 诊断纪律(本项目反复栽的教训)

- **先拿基线/日志/实验坐实,再下结论。** 本会话多次凭 DB 字段、凭推断下定论,都被实验推翻(isMetadataApplied 当 bug、steam 链接当根因…)。
- 根因常在**环境**(路径编码、启动器 DB、同名两份),不在 `common/decisions` 代码。改前先看 error.log 的 Error 详情行,别只看 PostValidate。

## 改动后验证

- 改 loc / 修正定义后,游戏内**旧脚本是缓存的**,要**重启游戏 / 重载存档**(或调试 console reload)才看得到。
- 加载期看 `...\Victoria 3\logs\error.log`;实玩点作弊抓运行期错(`tools/check_errorlog.py`)。

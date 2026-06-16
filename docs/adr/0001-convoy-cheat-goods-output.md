# ADR-0001 — 商船作弊改用 goods_output_merchant_marine_add

状态:已采纳(2026-06-16)

## 背景

「+商船」作弊原用 `country_convoys_capacity_add = 10000`(country 级直接加 convoy 容量)。1.13 **移除了**这个 modifier 类型(只剩 `character_convoy_protection_mult` / `character_convoy_raiding_mult`),加载报 `Unknown modifier type`。

## 候选

1. **`building_port_throughput_add`** —— 提升港口吞吐。但 throughput **同时放大港口的产出和消耗**:港口会狂吃 steamers/oil/coal(~按倍数),货价暴涨、港口巨亏。隐藏大副作用,不合产品质量。
2. **`goods_output_merchant_marine_add`** —— 直接加港口商船(merchant marine = convoy)产出,**不增加任何输入消耗**。干净。

scope 已坐实:vanilla tech 用 `goods_output_hardwood_mult`、laws 用 `building_group_*_throughput_add`,证明建筑级 modifier 能从 country scope 下沉到全国对应建筑。

## 决策

用 **`goods_output_merchant_marine_add = 1000`**。干净产出、无副作用。应用后游戏的 modifier 提示会自动显示「+1000 商船产出」。

## 后果

- 作弊干净:只多商船,不连累经济。
- 内部标识符随之统一为 `daoyu_goods_output_merchant_marine_add`(合宏惯例,见 ADR-0002)。
- 显示文字:「增加商船(港口商船产出)」/「More Convoys (Port Output)」。
- **教训**:作弊不只看「功能可用」,要看它对经济的真实加成/副作用,描述要如实写。throughput 那条就是「能用但有暗坑」的反例。

<!-- About 简介（推送后填写到仓库 About 栏）：
跨境选品专家：目标市场→五维打分表→供应链 checklist→风险清单 ｜ 一键安装：/plugin marketplace add lhg-plugs/lhg-product-pick
-->
<!-- topics（推送后打）：claude-code, claude-plugin, agent-skills, cross-border, ecommerce, product-selection -->

# lhg-product-pick：跨境选品专家，框架打分一条龙

> ⚠️ **声明（首屏置顶）**：**实时市场数据是本插件短板**——插件只提供**评估框架与打分表**，**销量/竞争数据需用户自行从平台后台核实**，**不做选品成败承诺**。
>
> **一句话介绍**：给 AI 编程助手装上"跨境选品专家"——目标市场定位 → 五维选品打分表 → 供应链 checklist → 禁售/合规风险清单 → 输出可审计的选品评估报告；**承诺话术写入即拦截，6 条确定性规则兜底**。
>
> **一键安装**：在 Claude Code 里运行
> ```
> /plugin marketplace add lhg-plugs/lhg-product-pick
> /plugin install lhg-product-pick@lhg-plugs
> ```

## 它是什么

`lhg-product-pick` 是一个 Claude Code 插件（plugin 为主、skill 为辅）：

- **4 个命令**（小白入口）：`product-pick` 选品一条龙，`product-score` 五维打分，`product-risk` 风险清单，`product-audit` 选品体检
- **4 个平台中立 skill**（方法论，可移植到豆包/Workbuddy 等 agent 平台）：目标市场定位四问、五维打分表、供应链 checklist、风险与合规清单
- **2 个专家 agent**：选品分析师、选品审计员
- **1 个承诺硬门 hook**：写入文件命中选品承诺关键词（保证爆款/必赚/稳赚/月入百万/闭眼入/零风险等）直接拦截，可一键关闭
- **6 条确定性审计规则**：纯 Python 标准库、零第三方依赖，含打分维度完整性、利润公式完整性、物流标注、禁售合规、承诺拦截、数据声明检查

## 合规设计：三层防护

1. **声明置顶**：README 首屏、每个 SKILL.md 开头、每条命令输出末尾，都有显著的数据声明（不做选品成败承诺）。
2. **写入硬门**：hook 在文件写入前扫描选品承诺关键词，命中即拦截（exit 2）；`LHG_PRODUCTPICK_PROMISE_OFF=1` 可关闭。
3. **审计兜底**：`pick_audit.py` 的 6 条规则全是 blocker，`product-audit` 命令逐条清零。

## 4 个命令用法

| 命令 | 作用 | 示例 |
|---|---|---|
| `/lhg-product-pick:product-pick` | 市场→打分→供应链→风险一条龙，输出评估报告 | `/lhg-product-pick:product-pick "厨房收纳盒，美国亚马逊"` |
| `/lhg-product-pick:product-score` | 五维打分，输出 pick.json 与 Go/Caution/No-Go | `/lhg-product-pick:product-score "硅胶折叠水杯" "TikTok 东南亚"` |
| `/lhg-product-pick:product-risk` | 下单前风险体检，输出带应对动作的风险清单 | `/lhg-product-pick:product-risk "儿童磁力片" "美国亚马逊"` |
| `/lhg-product-pick:product-audit` | 体检：打分维度/利润公式/物流标注/合规/承诺/声明 | `/lhg-product-pick:product-audit ./我的选品` |

## 目录结构

```
lhg-product-pick/
├── .claude-plugin/          # plugin.json（插件清单）+ marketplace.json（本仓即市场）
├── commands/                # 4 个命令：product-pick / product-score / product-risk / product-audit
├── skills/                  # 4 个平台中立 skill（市场/打分/供应链/风险，声明置顶）
├── agents/                  # 2 个专家 agent（scout / auditor）
├── hooks/                   # 选品承诺关键词拦截 hook（fail-open，可一键关闭）
├── scripts/audit/           # 确定性审计：pick_audit.py（零第三方依赖）
├── fixtures/                # 好/坏对照用例
├── smoke_test.py            # 冒烟测试
├── ATTRIBUTION.md           # 灵感来源声明
└── LICENSE                  # MIT
```

## 什么时候用 / 什么时候不用（FAQ）

**什么时候用**
- 想做跨境电商，不知道卖什么 → `product-pick` 一条龙
- 手里有几个候选产品，拿不准选哪个 → `product-score` 横向打分
- 打分通过、准备下单前 → `product-risk` 过一遍风险清单
- 选品报告写完了，不确定全不全 → `product-audit` 体检

**什么时候不用**
- 想要"实时销量数据/热卖榜" → 本插件**不提供**，请去平台后台或第三方数据工具查
- 想要"保证爆款"的承诺 → 本插件**不给**，只给评估框架与风险提示
- 已经确定产品、只想做 listing 优化 → 那是另一个环节，本插件不管
- 纠纷已发生（如被平台下架、被投诉侵权）→ 请咨询专业服务商/律师

## 自检与反馈

本插件自带质检：每次使用后可跑 `python3 smoke_test.py` 一键验证（JSON 合法、skill/command/agent 完整性、6 条规则、fixtures 命中、hooks 行为）。

发现 bug 或有改进建议，以 `[QC] <一句话问题>` 为标题提交到 https://github.com/lhg-plugs/lhg-product-pick/issues，正文写清"复现步骤 → 实际表现 → 期望表现"。

| 插件 | 一句话 | 安装 |
|---|---|---|
| [lhg-fullstack](https://github.com/lhg-plugs/lhg-fullstack) | 小白一句话 → 高质量全栈应用 | `/plugin install lhg-fullstack@lhg-plugs` |
| *（后续插件在此追加，保持表格格式一致）* | | |

## 出品：刘洪光

本插件由真人出镜 IP「刘洪光」（安徽合肥）出品，归属 [lhg-skills](https://github.com/lhg-skills)。

- GitHub 主页：https://github.com/lhg-skills —— 全部 skill 开源在此，欢迎 star
- 视频号：搜「刘洪光实名上网」
- 微信：lhgsmsw

# 灵感来源与致谢（Attribution）

本插件的**方法论灵感**来自以下项目，**所有实现代码、检测规则与文案均为原创**，未复制任何第三方的原文案或代码。

| 项目 | 作者 / 组织 | 许可（2026-10-11 核实） | 链接 | 借鉴了什么思路 |
|---|---|---|---|---|
| ecommerce-product-scout-agent（海购选品助手） | xiaolu7586 | **未声明**（仓库无 LICENSE 文件；star 数 66，2026-10-11 实查，不保证后续不变） | https://github.com/xiaolu7586/ecommerce-product-scout-agent | 仅借鉴"多维评分+利润模型+Go/No-Go 决策"的高层思路；**该项目的原文案、代码一律未复制**，本插件不依赖其任何服务 |
| cross-border-ecommerce-skills（58 个跨境电商 skill 模板） | noique（另有 tobiaslau-lab fork） | **NOASSERTION 未声明**（2026-10-11 实查） | https://github.com/noique/cross-border-ecommerce-skills | 仅借鉴"选品→调研→合规分阶段"的高层思路；文案与实现均为原创 |
| TikTok/亚马逊选品方法论博客 | 紫鸟浏览器（公开博客文章） | 公开文章（非代码许可） | https://www.ziniao.com/blog/5518.html | 仅借鉴"目标市场→数据验证→小批量试销"的通用选品常识；表述为原创 |

## 声明

1. **借鉴思路，实现与文案均为原创**：以上项目的具体文案、提示词原文、代码实现均未被复制。本插件的 skill 方法论文案、审计规则、命令流程均为独立撰写。特别说明：xiaolu7586 与 noique 的项目许可未声明，本插件与其无任何代码或文案上的派生关系，也不调用其服务。
2. **许可合规**：本插件审计脚本与 hook 仅使用 Python 标准库，未捆绑任何第三方包。
3. **商标与归属**：各项目名称与作者署名归其各自所有者所有；Amazon/TikTok Shop/Shopee 等平台名称归其各自所有者所有。
4. **数据边界**：本插件不提供实时市场数据；销量/竞争数据需用户自行从平台后台核实，不做选品成败承诺。

## 本插件自身的许可

本插件原创部分采用 MIT 许可（见 `LICENSE` 文件），版权所有：刘洪光（https://github.com/lhg-skills）。

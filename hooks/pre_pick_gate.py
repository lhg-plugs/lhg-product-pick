#!/usr/bin/env python3
"""lhg-product-pick 硬门：选品成败承诺表述拦截。

触发：PreToolUse / Edit|Write。扫描本次写入/编辑的文件内容，
若命中选品承诺关键词（保证爆款/必赚/稳赚/月入百万/闭眼入/零风险等），
以 exit code 2 拦截该操作，并给出改写指引。

逃生方式（按推荐度排序）：
  1. LHG_PRODUCTPICK_PROMISE_OFF=1（环境变量，当前会话有效；关闭后
     关键词拦截不再触发，但审计脚本的 NO-GUARANTEE-001 仍会在
     product-audit 时报 blocker）。
  2. /plugin disable lhg-product-pick（整个插件停用，hooks 不再触发）。

设计原则：只有“命中关键词”才拦截；内部出错一律 fail-open
（直接放行，不报错）；零第三方依赖。

注意：本 hook 只做关键词层面的硬拦截，真正的合规判断
（上下文、语气、数据是否经平台后台核实）仍由 agent 按 skill 规范负责。
"""

import json
import os
import sys

# 选品承诺关键词表（原创整理：常见选品“保底话术”）
PROMISE_KEYWORDS = [
    "保证爆款", "必赚", "稳赚", "稳赚不赔", "月入百万", "闭眼入",
    "零风险", "包赚", "必定爆单", "躺着赚钱", "稳出单",
    "一定大卖", "保证出单",
]

REWRITE_GUIDE = (
    "改写指引：删除对选品结果的成败承诺（保证爆款/必赚/稳赚等）；"
    "只保留评估框架、打分过程与风险提示；如需谈销量前景，用标准话术替代："
    "“实时市场数据是本插件短板，销量/竞争数据需您自行从平台后台核实，"
    "本插件不做选品成败承诺。”"
)


def extract_text(tool_input):
    """从 Edit/Write 的输入中抽取待写入文本。"""
    parts = []
    for key in ("content", "new_string", "old_string", "file_text"):
        v = tool_input.get(key)
        if isinstance(v, str) and v:
            parts.append(v)
    return "\n".join(parts)


def find_hits(text):
    hits = []
    for kw in PROMISE_KEYWORDS:
        if kw in text:
            hits.append(kw)
    return hits


def main() -> int:
    if os.environ.get("LHG_PRODUCTPICK_PROMISE_OFF") == "1":
        return 0  # 逃生开关

    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        return 0  # 输入解析失败：fail-open

    tool_input = payload.get("tool_input", {}) or {}
    text = extract_text(tool_input)
    if not text:
        return 0

    try:
        hits = find_hits(text)
    except Exception:
        return 0  # 内部错误：fail-open

    if not hits:
        return 0

    msg = (
        "⛔ 承诺硬门（lhg-product-pick）：本次写入内容命中选品承诺关键词：%s。\n"
        "本插件只提供评估框架与打分表，不做选品成败承诺。\n%s\n"
        "确认为合规内容但被误拦：export LHG_PRODUCTPICK_PROMISE_OFF=1 后重试。"
        % ("、".join(hits), REWRITE_GUIDE)
    )
    sys.stderr.write(msg + "\n")
    return 2  # exit 2 = 拦截本次工具调用


if __name__ == "__main__":
    sys.exit(main())

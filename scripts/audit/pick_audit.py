#!/usr/bin/env python3
"""lhg-product-pick 确定性审计：选品评估单体检。

扫描目标目录下的 pick.json（选品评估单）与 *.md（选品报告），
按规则注册表逐项检查。零第三方依赖。

规则（rule_id / 级别 / 含义）：
  SCORE-DIM-001  blocker  打分表维度不完整（缺 5 维之一或分数不在 1~5）
  PROFIT-001     blocker  利润测算公式不完整（缺 售价/采购成本/平台佣金/物流成本/退货损耗）
  LOGISTICS-001  blocker  物流时效与运费标注缺失（缺 头程运费/尾程运费/配送时效）
  BANLIST-001    blocker  命中高风险/禁售类目词且无合规表述
  NO-GUARANTEE-001 blocker 选品报告含成败承诺表述（保证爆款/必赚/稳赚等）
  DATA-DISC-001  blocker  报告缺数据来源声明（销量/竞争数据需自行从平台后台核实）

用法：
  python3 pick_audit.py --target <目录> [--format json|text]
退出码：0=无问题，1=有 blocker，2=只有 warning。
"""

import argparse
import json
import os
import re
import sys

# ---------------------------------------------------------------- 规则注册表
SCORE_DIMENSIONS = ["市场需求", "竞争烈度", "利润空间", "物流适配", "合规风险"]
PROFIT_FIELDS = ["售价", "采购成本", "平台佣金", "物流成本", "退货损耗"]
LOGISTICS_FIELDS = ["头程运费", "尾程运费", "配送时效"]

# 高风险/禁售类目关键词（原创整理：跨境平台常见高风险类目）
RISKY_CATEGORY_KEYWORDS = [
    "儿童", "婴幼儿", "玩具", "食品接触", "医疗器械", "化妆品",
    "充电宝", "锂电池", "激光", "无人机", "减肥", "壮阳",
    "电子烟", "刀具", "仿真枪",
]
# 合规表述（出现任意一个即视为已做合规提示）
COMPLIANCE_MARKERS = [
    "认证", "合规", "禁售", "3C", "CE", "FCC", "CPC", "CPSC",
    "UL", "FDA", "许可", "备案", "专利", "商标",
]
# 选品承诺表述
PROMISE_WORDS = [
    "保证爆款", "必赚", "稳赚", "月入百万", "闭眼入",
    "零风险", "包赚", "躺着赚钱", "稳出单", "一定大卖", "保证出单",
]
# 数据来源声明
DATA_DISC_MARKERS = ["自行核实", "平台后台核实", "平台后台查询"]


class Finding:
    def __init__(self, rule_id, level, message, location=""):
        self.rule_id = rule_id
        self.level = level
        self.message = message
        self.location = location

    def to_dict(self):
        return {"rule_id": self.rule_id, "level": self.level,
                "message": self.message, "location": self.location}


# ---------------------------------------------------------------- 检查逻辑
def check_pick_json(path, findings):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        findings.append(Finding("SCORE-DIM-001", "blocker",
                                "目标目录缺少 pick.json（选品评估单）", path))
        return
    except json.JSONDecodeError as e:
        findings.append(Finding("SCORE-DIM-001", "blocker",
                                "pick.json 不是合法 JSON：%s" % e, path))
        return

    dims = data.get("dimensions", {})
    missing = [d for d in SCORE_DIMENSIONS if d not in dims]
    if missing:
        findings.append(Finding("SCORE-DIM-001", "blocker",
                                "打分表缺失维度：%s（必需 5 维：%s）"
                                % ("、".join(missing), "、".join(SCORE_DIMENSIONS)),
                                path))
    for d in SCORE_DIMENSIONS:
        v = dims.get(d)
        if v is not None and not (isinstance(v, (int, float)) and 1 <= v <= 5):
            findings.append(Finding("SCORE-DIM-001", "blocker",
                                    "维度“%s”分数非法（应为 1~5）：%r" % (d, v),
                                    path))

    calc = data.get("price_calc", {})
    missing = [k for k in PROFIT_FIELDS if k not in calc]
    if missing:
        findings.append(Finding("PROFIT-001", "blocker",
                                "利润测算公式不完整，缺失字段：%s（完整公式=售价−采购成本−平台佣金−物流成本−退货损耗）"
                                % "、".join(missing), path))

    lg = data.get("logistics", {})
    missing = [k for k in LOGISTICS_FIELDS if k not in lg]
    if missing:
        findings.append(Finding("LOGISTICS-001", "blocker",
                                "物流标注缺失：%s（需标注头程运费/尾程运费/配送时效）"
                                % "、".join(missing), path))


def check_report_md(path, findings):
    with open(path, encoding="utf-8") as f:
        text = f.read()

    risky = [w for w in RISKY_CATEGORY_KEYWORDS if w in text]
    compliant = any(m in text for m in COMPLIANCE_MARKERS)
    if risky and not compliant:
        findings.append(Finding("BANLIST-001", "blocker",
                                "命中高风险类目词（%s）但全文无合规表述（认证/禁售/3C/CE/FCC/CPC 等）"
                                % "、".join(risky), path))

    hits = [w for w in PROMISE_WORDS if w in text]
    if hits:
        findings.append(Finding("NO-GUARANTEE-001", "blocker",
                                "报告含选品成败承诺表述：%s（改写为框架评估+风险提示）"
                                % "、".join(hits), path))

    if not any(m in text for m in DATA_DISC_MARKERS):
        findings.append(Finding("DATA-DISC-001", "blocker",
                                "报告缺数据来源声明：须写明“销量/竞争数据需自行从平台后台核实”",
                                path))


def audit(target):
    findings = []
    check_pick_json(os.path.join(target, "pick.json"), findings)
    for name in sorted(os.listdir(target)):
        if name.endswith(".md"):
            check_report_md(os.path.join(target, name), findings)
    return findings


# ---------------------------------------------------------------- 输出
def main():
    ap = argparse.ArgumentParser(description="lhg-product-pick 选品评估单审计")
    ap.add_argument("--target", required=True, help="待审计目录（含 pick.json 与报告 .md）")
    ap.add_argument("--format", choices=["json", "text"], default="text")
    args = ap.parse_args()

    if not os.path.isdir(args.target):
        print("目标目录不存在：%s" % args.target, file=sys.stderr)
        return 1

    findings = audit(args.target)
    blockers = sum(1 for f in findings if f.level == "blocker")
    warnings = sum(1 for f in findings if f.level == "warning")
    summary = {"blocker": blockers, "warning": warnings,
               "total": len(findings)}

    if args.format == "json":
        print(json.dumps({"summary": summary,
                          "findings": [f.to_dict() for f in findings]},
                         ensure_ascii=False, indent=2))
    else:
        print("选品审计：blocker=%d warning=%d" % (blockers, warnings))
        for f in findings:
            loc = " [%s]" % f.location if f.location else ""
            print("[%s] %s%s: %s" % (f.level.upper(), f.rule_id, loc, f.message))
        if not findings:
            print("全部通过。")

    if blockers:
        return 1
    if warnings:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

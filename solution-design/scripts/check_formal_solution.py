#!/usr/bin/env python3
"""Flag wording that should not appear in formal solution proposal bodies."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


@dataclass(frozen=True)
class Rule:
    phrase: str
    category: str
    suggestion: str


ZH_RULES = [
    Rule("根据用户要求", "用户提示痕迹", "改为项目目标或方案约束的客观表达。"),
    Rule("按照用户要求", "用户提示痕迹", "改为项目目标或方案约束的客观表达。"),
    Rule("按照要求", "过程性表达", "直接陈述方案内容。"),
    Rule("本次生成", "生成过程", "删除生成过程描述。"),
    Rule("下面将", "生成过程", "直接给出正式内容。"),
    Rule("预计", "虚拟结果", "改写为验证设计、指标体系或输出要求。"),
    Rule("预期", "虚拟结果", "改写为验证设计、指标体系或输出要求。"),
    Rule("后续可", "后续展望", "改写为适用条件、模块边界或工程流程。"),
    Rule("后续将", "后续展望", "改写为适用条件、模块边界或工程流程。"),
    Rule("只是", "自我削弱", "改为客观的适用范围或建模假设。"),
    Rule("简化演示", "自我削弱", "改为客观的适用范围或建模假设。"),
    Rule("不涉及复杂算法", "自我削弱", "改为算法边界和适用条件。"),
    Rule("当前阶段", "过程性表达", "删除阶段性口吻。"),
    Rule("手动插入", "制作过程", "只保留图号、图题和图示内容。"),
    Rule("使用 pandoc", "导出过程", "从正式方案正文中删除。"),
    Rule("转换为 Word", "导出过程", "从正式方案正文中删除。"),
    Rule("Markdown", "文件过程", "从正式方案正文中删除。"),
    Rule("AI", "AI 过程", "从正式方案正文中删除。"),
    Rule("提示词", "用户提示痕迹", "从正式方案正文中删除。"),
]

EN_RULES = [
    Rule("according to the user's request", "prompt trace", "State the project objective or constraint directly."),
    Rule("in this generation", "generation process", "Remove generation-process wording."),
    Rule("this document will", "process wording", "State the proposal content directly."),
    Rule("expected to", "unsupported expected result", "Use validation design, metrics, or output requirements."),
    Rule("it is expected that", "unsupported expected result", "Use validation design, metrics, or output requirements."),
    Rule("future work", "future-work section", "Use applicability, module boundaries, or engineering process."),
    Rule("will be inserted manually", "production process", "Keep only figure number, title, and content note."),
    Rule("just a simplified demo", "self-weakening", "Use scope, assumptions, and applicability."),
    Rule("does not involve complex algorithms", "self-weakening", "Use algorithm boundaries and applicability."),
    Rule("using pandoc", "export process", "Remove from the formal proposal body."),
    Rule("convert to Word", "export process", "Remove from the formal proposal body."),
    Rule("Markdown", "file process", "Remove from the formal proposal body."),
    Rule("AI prompt", "prompt trace", "Remove from the formal proposal body."),
]


def scan(path: Path, lang: str) -> list[tuple[int, Rule, str]]:
    text = path.read_text(encoding="utf-8")
    rules = ZH_RULES if lang == "zh" else EN_RULES
    findings: list[tuple[int, Rule, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        haystack = line if lang == "zh" else line.lower()
        for rule in rules:
            needle = rule.phrase if lang == "zh" else rule.phrase.lower()
            if needle in haystack:
                findings.append((line_number, rule, line.strip()))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Check formal solution wording.")
    parser.add_argument("markdown_file", type=Path)
    parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    args = parser.parse_args()

    if not args.markdown_file.exists():
        print(f"File not found: {args.markdown_file}")
        return 2

    findings = scan(args.markdown_file, args.lang)
    if not findings:
        print("未发现疑似禁用表达。" if args.lang == "zh" else "No suspicious formal-proposal wording found.")
        return 0

    if args.lang == "zh":
        print("发现疑似不适合正式方案正文的表达：")
        for line_number, rule, original in findings:
            print(f"第 {line_number} 行：{rule.phrase}")
            print(f"  原文：{original}")
            print(f"  类型：{rule.category}")
            print(f"  建议：{rule.suggestion}")
    else:
        print("Suspicious wording found in the formal proposal body:")
        for line_number, rule, original in findings:
            print(f"Line {line_number}: {rule.phrase}")
            print(f"  Original: {original}")
            print(f"  Category: {rule.category}")
            print(f"  Suggestion: {rule.suggestion}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

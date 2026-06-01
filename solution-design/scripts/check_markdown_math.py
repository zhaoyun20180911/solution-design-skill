#!/usr/bin/env python3
"""Flag likely mathematical variables that are not marked with Markdown math."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


FUNCTION_VAR_RE = re.compile(r"\b[A-Za-z](?:_[A-Za-z0-9]+)?\([A-Za-z0-9,+\-_\s]+\)")
SUBSCRIPT_RE = re.compile(r"\b[A-Za-z]_[A-Za-z0-9]+\b")
GREEK_RE = re.compile(
    r"\b(alpha|beta|gamma|theta|lambda|mu|sigma|omega|phi|kappa|epsilon)\b",
    re.IGNORECASE,
)
METRIC_RE = re.compile(r"\b(RMSE|STD|mean error)\b", re.IGNORECASE)


def mask_inline_math(line: str, in_display: bool) -> tuple[str, bool]:
    masked: list[str] = []
    i = 0
    in_inline = False
    while i < len(line):
        if line.startswith("$$", i):
            in_display = not in_display
            masked.extend("  ")
            i += 2
            continue
        if line[i] == "$" and not in_display:
            in_inline = not in_inline
            masked.append(" ")
            i += 1
            continue
        masked.append(" " if in_inline or in_display else line[i])
        i += 1
    return "".join(masked), in_display


def find_candidates(path: Path) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    in_display = False
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        masked, in_display = mask_inline_math(line, in_display)
        seen: set[str] = set()
        for regex in (FUNCTION_VAR_RE, SUBSCRIPT_RE, GREEK_RE, METRIC_RE):
            for match in regex.finditer(masked):
                token = match.group(0).strip()
                if token and token not in seen:
                    seen.add(token)
                    findings.append((line_number, token, f"${token}$"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Markdown math notation.")
    parser.add_argument("markdown_file", type=Path)
    parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    args = parser.parse_args()

    if not args.markdown_file.exists():
        print(f"File not found: {args.markdown_file}")
        return 2

    findings = find_candidates(args.markdown_file)
    if not findings:
        print("未发现疑似未标记数学变量。" if args.lang == "zh" else "No likely unmarked math variables found.")
        return 0

    if args.lang == "zh":
        print("疑似未标记数学变量：")
        for line_number, token, suggestion in findings:
            print(f"第 {line_number} 行：{token}")
            print(f"  建议：{suggestion}")
    else:
        print("Likely unmarked math variables:")
        for line_number, token, suggestion in findings:
            print(f"Line {line_number}: {token}")
            print(f"  Suggestion: {suggestion}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

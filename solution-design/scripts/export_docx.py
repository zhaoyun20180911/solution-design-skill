#!/usr/bin/env python3
"""Export a formal solution Markdown file to Word via pandoc."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def sanitize_project_name(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", name.strip())
    cleaned = re.sub(r"\s+", "_", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned).strip("._ ")
    return cleaned or "solution_design"


def default_output(markdown_file: Path, project_name: str | None, lang: str) -> Path:
    safe_name = sanitize_project_name(project_name or markdown_file.parent.name.replace("_solution_design", ""))
    filename = f"{safe_name}_方案设计.docx" if lang == "zh" else f"{safe_name}_solution_design.docx"
    return markdown_file.parent / "exports" / filename


def print_missing_pandoc(lang: str, output: Path, markdown_file: Path) -> None:
    if lang == "zh":
        print("未检测到 pandoc，暂不能生成 Word 文件。")
        print("安装提示：Windows 可安装 .msi，macOS 可安装 .pkg 或使用 Homebrew，Linux 可使用系统包管理器。")
        print(f"最终 Word 文件（尚未生成）：{output}")
        print(f"Markdown 源文件：{markdown_file}")
    else:
        print("Pandoc is not installed, so the Word file cannot be generated yet.")
        print("Install hint: use the .msi installer on Windows, .pkg or Homebrew on macOS, or a package manager on Linux.")
        print(f"Final Word file (not generated): {output}")
        print(f"Markdown source file: {markdown_file}")


def print_success(lang: str, output: Path, markdown_file: Path) -> None:
    if lang == "zh":
        print("Word 正式方案文档已生成：")
        print(f"路径：{output}")
        print("作用：这是本次方案设计的最终 Word 交付文件，可直接打开查看和继续编辑。")
        print("\nMarkdown 源文件也已保留：")
        print(f"路径：{markdown_file}")
        print("作用：这是 Word 文档的源文件，后续如需大幅修改方案，建议先修改该文件后重新导出 Word。")
        print(f"\n最终 Word 文件位置：{output}")
    else:
        print("Formal Word proposal generated:")
        print(f"Path: {output}")
        print("Purpose: this is the final Word deliverable for the solution-design task.")
        print("\nMarkdown source retained:")
        print(f"Path: {markdown_file}")
        print("Purpose: use this source file for major revisions before exporting Word again.")
        print(f"\nFinal Word file: {output}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export solution-design Markdown to Word.")
    parser.add_argument("markdown_file", type=Path)
    parser.add_argument("--project-name")
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    args = parser.parse_args()

    markdown_file = args.markdown_file.resolve()
    if not markdown_file.exists():
        print(f"File not found: {markdown_file}")
        return 2

    output = (args.output.resolve() if args.output else default_output(markdown_file, args.project_name, args.lang).resolve())
    pandoc = shutil.which("pandoc")
    if not pandoc:
        print_missing_pandoc(args.lang, output, markdown_file)
        return 2

    output.parent.mkdir(parents=True, exist_ok=True)
    command = [pandoc, str(markdown_file), "-o", str(output)]
    if args.reference:
        reference = args.reference.resolve()
        if reference.exists():
            command.append(f"--reference-doc={reference}")
        else:
            print(f"Reference docx not found, continuing without it: {reference}")

    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        return result.returncode

    print_success(args.lang, output, markdown_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

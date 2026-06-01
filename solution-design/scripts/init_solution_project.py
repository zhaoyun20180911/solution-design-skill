#!/usr/bin/env python3
"""Initialize a compact solution-design project folder."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


PROCESS_FILES = [
    "project_anchor.md",
    "confirmed_framework.md",
    "solution_design.md",
]


ZH_PURPOSES = {
    "project_anchor.md": ("保存前期调研、项目画像和用户重点要求的第一锚点", "否"),
    "confirmed_framework.md": ("保存用户确认后的技术路线和方案框架的第二锚点", "否"),
    "solution_design.md": ("正式 Word 方案的 Markdown 源文件", "否"),
    "exports/": ("保存最终 Word 正式方案", "是"),
}

EN_PURPOSES = {
    "project_anchor.md": ("First anchor for research, project image, and user priorities", "No"),
    "confirmed_framework.md": ("Second anchor for the user-confirmed route and framework", "No"),
    "solution_design.md": ("Markdown source for the final Word proposal", "No"),
    "exports/": ("Stores final Word proposal files", "Yes"),
}


def sanitize_project_name(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", name.strip())
    cleaned = re.sub(r"\s+", "_", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned).strip("._ ")
    if not cleaned:
        raise ValueError("project name cannot be empty")
    return cleaned


def skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def template_for(file_name: str, lang: str) -> str:
    mapping = {
        "project_anchor.md": f"project_anchor_template.{lang}.md",
        "confirmed_framework.md": f"confirmed_framework_template.{lang}.md",
        "solution_design.md": "../references/default_solution_template.md",
    }
    template_name = mapping[file_name]
    if template_name.startswith("../"):
        return read_text(skill_dir() / template_name[3:])
    return read_text(skill_dir() / "templates" / template_name)


def create_project(project_name: str, lang: str, output_root: Path) -> Path:
    safe_name = sanitize_project_name(project_name)
    project_dir = output_root / f"{safe_name}_solution_design"
    if project_dir.exists():
        raise FileExistsError(f"project directory already exists: {project_dir}")

    project_dir.mkdir(parents=True)
    (project_dir / "exports").mkdir()

    for file_name in PROCESS_FILES:
        target = project_dir / file_name
        target.write_text(template_for(file_name, lang), encoding="utf-8")

    return project_dir


def print_summary(project_dir: Path, lang: str) -> None:
    purposes = ZH_PURPOSES if lang == "zh" else EN_PURPOSES
    if lang == "zh":
        print("已创建方案项目目录：")
        print(project_dir)
        print("\n已生成文件：")
        for file_name in PROCESS_FILES:
            purpose, final = purposes[file_name]
            print(f"- {file_name}：{project_dir / file_name}；作用：{purpose}；最终交付物：{final}")
        purpose, final = purposes["exports/"]
        print(f"- exports/：{project_dir / 'exports'}；作用：{purpose}；最终交付物：{final}")
    else:
        print("Created solution project directory:")
        print(project_dir)
        print("\nGenerated files:")
        for file_name in PROCESS_FILES:
            purpose, final = purposes[file_name]
            print(f"- {file_name}: {project_dir / file_name}; purpose: {purpose}; final deliverable: {final}")
        purpose, final = purposes["exports/"]
        print(f"- exports/: {project_dir / 'exports'}; purpose: {purpose}; final deliverable: {final}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a solution-design project.")
    parser.add_argument("project_name")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    parser.add_argument("--output-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    try:
        project_dir = create_project(
            args.project_name,
            args.lang,
            args.output_root.resolve(),
        )
    except Exception as exc:
        print(f"Error: {exc}")
        return 1

    print_summary(project_dir, args.lang)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

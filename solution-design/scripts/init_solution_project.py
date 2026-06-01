#!/usr/bin/env python3
"""Initialize a solution-design project folder."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


PROCESS_FILES = [
    "project_profile.md",
    "project_research_pack.md",
    "solution_outline.md",
    "solution_design.md",
    "change_log.md",
]


ZH_PURPOSES = {
    "project_profile.md": ("记录项目画像和用户需求", "否"),
    "project_research_pack.md": ("记录调研资料、算法路线和学习资料", "否"),
    "solution_outline.md": ("记录方案章节结构和技术框架", "否"),
    "solution_design.md": ("正式方案的源文件", "否"),
    "change_log.md": ("记录多轮修改意见和框架调整", "否"),
    "exports/": ("保存最终 Word 正式方案", "是"),
}

EN_PURPOSES = {
    "project_profile.md": ("Records project profile and user requirements", "No"),
    "project_research_pack.md": ("Records research material, routes, and learning resources", "No"),
    "solution_outline.md": ("Records proposal sections and technical framework", "No"),
    "solution_design.md": ("Source file for the formal proposal", "No"),
    "change_log.md": ("Records revisions and framework changes", "No"),
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


def read_template(template_name: str) -> str:
    template_path = skill_dir() / "templates" / template_name
    return template_path.read_text(encoding="utf-8")


def template_for(file_name: str, lang: str) -> str:
    mapping = {
        "project_profile.md": f"project_profile_template.{lang}.md",
        "project_research_pack.md": f"research_pack_template.{lang}.md",
        "solution_outline.md": f"solution_outline_template.{lang}.md",
        "change_log.md": f"change_log_template.{lang}.md",
        "solution_design.md": "../references/default_solution_template.md",
    }
    template_name = mapping[file_name]
    if template_name.startswith("../"):
        return (skill_dir() / template_name[3:]).read_text(encoding="utf-8")
    return read_template(template_name)


def create_project(project_name: str, mode: str, lang: str, output_root: Path) -> tuple[Path, Path]:
    safe_name = sanitize_project_name(project_name)
    project_dir = output_root / f"{safe_name}_solution_design"
    if project_dir.exists():
        raise FileExistsError(f"project directory already exists: {project_dir}")

    process_dir = project_dir if mode == "full" else project_dir / ".solution-design"
    process_dir.mkdir(parents=True)
    (project_dir / "exports").mkdir()

    for file_name in PROCESS_FILES:
        target = process_dir / file_name
        target.write_text(template_for(file_name, lang), encoding="utf-8")

    return project_dir, process_dir


def print_summary(project_dir: Path, process_dir: Path, mode: str, lang: str) -> None:
    purposes = ZH_PURPOSES if lang == "zh" else EN_PURPOSES
    if lang == "zh":
        print("已创建方案项目目录：")
        print(project_dir)
        if mode == "clean":
            print(f"中间过程文件保存到：{process_dir}")
        print("\n已生成文件：")
        for file_name in PROCESS_FILES:
            purpose, final = purposes[file_name]
            print(f"- {file_name}：{process_dir / file_name}；作用：{purpose}；最终交付物：{final}")
        purpose, final = purposes["exports/"]
        print(f"- exports/：{project_dir / 'exports'}；作用：{purpose}；最终交付物：{final}")
    else:
        print("Created solution project directory:")
        print(project_dir)
        if mode == "clean":
            print(f"Intermediate process files are stored in: {process_dir}")
        print("\nGenerated files:")
        for file_name in PROCESS_FILES:
            purpose, final = purposes[file_name]
            print(f"- {file_name}: {process_dir / file_name}; purpose: {purpose}; final deliverable: {final}")
        purpose, final = purposes["exports/"]
        print(f"- exports/: {project_dir / 'exports'}; purpose: {purpose}; final deliverable: {final}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a solution-design project.")
    parser.add_argument("project_name")
    parser.add_argument("--mode", choices=["full", "clean"], default="full")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    parser.add_argument("--output-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    try:
        project_dir, process_dir = create_project(
            args.project_name,
            args.mode,
            args.lang,
            args.output_root.resolve(),
        )
    except Exception as exc:
        print(f"Error: {exc}")
        return 1

    print_summary(project_dir, process_dir, args.mode, args.lang)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

---
name: solution-design
description: Use when a user asks to design, write, or prepare an algorithm, research, engineering, or technical solution proposal/report; asks for 方案, 技术方案, 算法方案, 方案框架, Word 方案, route selection, project profile, research pack, solution outline, formal proposal draft, or proposal Word export preparation.
---

# Solution Design

## Overview

Use this skill for the solution-design stage before implementation. It helps Codex guide users from an initial project topic to a confirmed technical route, a frozen solution outline, a formal proposal draft, and a Word-exportable deliverable.

Do not use this skill to directly develop algorithm code, simulation scripts, test plans, test reports, fabricated results, or long formal proposals before the technical route and outline are confirmed.

## Startup Language

Detect the user's input language and keep using it unless the user asks otherwise.

For Chinese requests, first say exactly:

```text
本次对话已激活 `solution-design` Skill。该 Skill 面向算法类、科研类和工程类技术方案设计任务，将通过‘调研—解释—提问—路线收敛—框架确认—正文生成—Markdown 转 Word’的方式，帮助您逐步形成正式技术方案。在方案框架和技术路线未确认前，本 Skill 不会直接进入算法实现、仿真脚本或测试报告撰写阶段。
```

For English requests, first say exactly:

```text
This conversation has activated the `solution-design` Skill. This Skill is designed for algorithm, research, and engineering technical solution design tasks. It will help you gradually form a formal technical proposal through research, explanation, questioning, route convergence, framework confirmation, draft generation, and Markdown-to-Word export. Before the solution framework and technical route are confirmed, this Skill will not proceed directly to algorithm implementation, simulation scripting, or test report writing.
```

Do not put startup text, AI process text, prompts, file paths, Markdown/Word conversion notes, or pandoc details into the formal proposal body.

## Workflow

Read `references/workflow.md` for the full workflow. Follow these gates:

1. Build or update `project_profile.md` from the user's topic, goals, inputs, outputs, constraints, and unknowns.
2. Build or update `project_research_pack.md` after research. If live research is needed and no sources are available, ask for sources or search keywords instead of inventing citations.
3. Ask confirmation question 1: the user must confirm the technical route before outline generation.
4. Build or update `solution_outline.md` with chapters, module boundaries, inputs/outputs, indicators, verification logic, and page-count guidance.
5. Ask confirmation question 2: the user must confirm the outline and technical framework before formal draft generation.
6. Generate `solution_design.md` as the formal proposal source only after the outline is confirmed.
7. Run or remind the user to run `scripts/check_formal_solution.py` and `scripts/check_markdown_math.py`.
8. Ask confirmation question 3: the user must confirm the Markdown draft before Word export.
9. Export Word with `scripts/export_docx.py` when pandoc is available, then clearly report the final Word path.

## Output Modes

Default to full mode because solution design needs traceable research, outline, and confirmation artifacts.

- Full mode: write process files directly under `{project_name}_solution_design/` and final Word files under `exports/`.
- Clean mode: if the user asks for only Word or no visible intermediate files, place process files under `.solution-design/` and final Word files under `exports/`.

Use `scripts/init_solution_project.py` to initialize either mode.

## Runtime Dependencies

The conversation workflow itself does not require extra software. The bundled helper scripts require a Python 3 interpreter available to Codex as `python`, `python3`, `py`, or a runtime-provided Python executable.

The helper scripts use only the Python standard library. Do not ask the user to install PyYAML, python-docx, pypandoc, or other Python packages for normal use of this skill.

If Python is unavailable, do not fail the workflow. Treat the scripts as convenience helpers: create or update the project folders and Markdown files directly, apply the reference rules manually, and export Word with a direct pandoc command after the Markdown draft is confirmed.

Pandoc is required only for the final Markdown-to-Word export. If pandoc is unavailable, keep the confirmed Markdown source and tell the user that Word export is blocked until pandoc is installed.

## Reference Files

- `references/workflow.md`: stage-by-stage process and confirmation gates.
- `references/research_pack_rules.md`: research-pack structure, citation integrity, and source handling.
- `references/route_selection_rules.md`: technical-route comparison and convergence rules.
- `references/solution_outline_rules.md`: outline, page-count, module, and indicator-system rules.
- `references/formal_solution_rules.zh.md`: Chinese formal proposal writing constraints.
- `references/formal_solution_rules.en.md`: English formal proposal writing constraints.
- `references/markdown_math_rules.md`: Markdown math notation rules.
- `references/word_export_rules.md`: Word export and final-path reporting rules.
- `references/default_solution_template.md`: starter formal proposal scaffold.

## Scripts

```bash
python scripts/init_solution_project.py "项目名称" --mode full --lang zh
python scripts/check_formal_solution.py solution_design.md --lang zh
python scripts/check_markdown_math.py solution_design.md --lang zh
python scripts/export_docx.py solution_design.md --project-name "项目名称" --lang zh
```

All scripts support `--lang zh` and `--lang en`.

## File Feedback Rule

Whenever a key file is created or updated, tell the user:

- file name
- full or relative path
- purpose
- whether it is a final deliverable
- how it will be used next

After Word export, always report the final Word path as a separate, prominent line.

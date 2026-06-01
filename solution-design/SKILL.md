---
name: solution-design
description: Use when a user asks to design, write, or prepare an algorithm, research, engineering, or technical solution proposal/report; asks for 方案, 技术方案, 算法方案, 方案框架, Word 方案, route selection, project anchor, framework confirmation, formal proposal draft, or proposal Word export preparation.
---

# Solution Design

## Overview

Use this skill for discussion-driven technical solution design before implementation. It helps Codex move from an initial topic to a researched project anchor, an interactive route/framework discussion, a confirmed framework anchor, and a final Markdown-to-Word proposal.

Do not use this skill to directly develop algorithm code, simulation scripts, test plans, test reports, fabricated results, or long formal proposals before the technical route and framework are confirmed.

## Startup Language

Detect the user's input language and keep using it unless the user asks otherwise.

For Chinese requests, first say exactly:

```text
本次对话已激活 `solution-design` Skill。该 Skill 面向算法类、科研类和工程类技术方案设计任务。工作方式是：先进行调研与项目画像，保存一个本地锚点；随后在对话中解释、比较和收敛技术路线；用户确认方案框架后保存第二个本地锚点；当用户要求生成最终 Word 方案时，直接生成 Markdown 初稿并导出 Word。方案框架和技术路线确认前，本 Skill 不进入算法实现、仿真脚本或测试报告撰写。
```

For English requests, first say exactly:

```text
This conversation has activated the `solution-design` Skill. This Skill is designed for algorithm, research, and engineering technical solution design tasks. It first saves a researched project anchor, then discusses and converges the technical route in chat, saves a confirmed framework anchor after user confirmation, and directly generates a Markdown draft and Word proposal when the user asks for the final Word document. Before the framework and technical route are confirmed, this Skill will not proceed to algorithm implementation, simulation scripting, or test report writing.
```

Do not put startup text, AI process text, prompts, file paths, Markdown/Word conversion notes, or pandoc details into the formal proposal body.

## Workflow

Read `references/workflow.md` for the full workflow. Follow these gates:

1. Create or update `project_anchor.md` after the initial understanding and research. This is the first memory anchor and should capture the project image, user priorities, constraints, research basis, candidate routes, and unresolved questions.
2. Discuss routes and framework in the chat. Do not create local discussion logs for ordinary back-and-forth.
3. Ask a focused confirmation question when the route/framework is ready to converge.
4. Create or update `confirmed_framework.md` only after the user confirms the route and framework. This is the second memory anchor and should capture the frozen route, module boundaries, inputs/outputs, indicators, verification logic, and proposal chapter framework.
5. When the user asks for the final Word proposal, directly generate `solution_design.md`, run or remind the user to run the checks, and export Word with `scripts/export_docx.py` if pandoc is available. Do not add another Markdown confirmation gate unless the user explicitly asks to review the Markdown first.

## Output Files

Use this compact project structure by default:

```text
{project_name}_solution_design/
├── project_anchor.md
├── confirmed_framework.md
├── solution_design.md
└── exports/
    └── {project_name}_方案设计.docx
```

Create files when their stage is reached. `scripts/init_solution_project.py` can initialize the folder and empty scaffolds when useful.

## Runtime Dependencies

The conversation workflow itself does not require extra software. The bundled helper scripts require a Python 3 interpreter available to Codex as `python`, `python3`, `py`, or a runtime-provided Python executable.

The helper scripts use only the Python standard library. Do not ask the user to install PyYAML, python-docx, pypandoc, or other Python packages for normal use of this skill.

If Python is unavailable, do not fail the workflow. Treat the scripts as convenience helpers: create or update the project folders and Markdown files directly, apply the reference rules manually, and export Word with a direct pandoc command after the final Markdown source is generated.

Pandoc is required only for the final Markdown-to-Word export. If pandoc is unavailable, keep the generated Markdown source and tell the user that Word export is blocked until pandoc is installed.

## Reference Files

- `references/workflow.md`: stage-by-stage process and confirmation gates.
- `references/project_anchor_rules.md`: first-anchor structure, research integrity, and source handling.
- `references/route_selection_rules.md`: technical-route comparison and convergence rules.
- `references/confirmed_framework_rules.md`: second-anchor structure for the confirmed technical framework.
- `references/formal_solution_rules.zh.md`: Chinese formal proposal writing constraints.
- `references/formal_solution_rules.en.md`: English formal proposal writing constraints.
- `references/markdown_math_rules.md`: Markdown math notation rules.
- `references/word_export_rules.md`: direct final draft and Word export rules.
- `references/default_solution_template.md`: starter formal proposal scaffold.

## Scripts

```bash
python scripts/init_solution_project.py "项目名称" --lang zh
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

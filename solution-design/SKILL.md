---
name: solution-design
description: Use when a user asks to design, write, or prepare an algorithm, research, engineering, or technical solution proposal/report; asks for 方案, 技术方案, 算法方案, 方案框架, Word 方案, route selection, project anchor, framework confirmation, formal proposal draft, or proposal Word export preparation.
---

# Solution Design

## Overview

Use this skill for discussion-driven technical solution design before implementation. The conversation is the primary user interface: show enough information in chat for the user to judge the solution without opening local Markdown files. Local files are memory anchors and final deliverables, not substitutes for explanation.

Do not use this skill to directly develop algorithm code, simulation scripts, test plans, test reports, fabricated results, or long formal proposals before the technical route and framework are confirmed.

## Startup Language

Detect the user's input language and keep using it unless the user asks otherwise.

For Chinese requests, first say exactly:

```text
本次对话已激活 `solution-design` Skill。我会按“深度调研 - 给出候选方案 - 讨论方案 - 确定方案 - 讨论框架 - 确定框架 - 生成最终 Word”的流程推进。过程中我会优先把调研结论、技术路线、关键问题、方案框架和每轮最新总结展示在对话里，本地 Markdown 文件只作为防遗忘锚点和最终 Word 的写作依据。方案和框架确认前，我不会进入算法实现、仿真脚本或测试报告撰写。
```

For English requests, first say exactly:

```text
This conversation has activated the `solution-design` Skill. I will proceed through deep research, candidate solution proposal, solution discussion, solution confirmation, framework discussion, framework confirmation, and final Word generation. I will show research findings, route options, key questions, framework drafts, and the latest summary in chat first; local Markdown files are only memory anchors and writing sources, not replacements for explanation. Before the solution and framework are confirmed, this Skill will not proceed to algorithm implementation, simulation scripting, or test report writing.
```

Do not put startup text, AI process text, prompts, file paths, Markdown/Word conversion notes, or pandoc details into the formal proposal body.

## Conversation-First Rule

Never make a local file the only place where important information appears. If research, route comparison, framework structure, assumptions, questions, or final export statistics are written to a file, also show the useful content in the chat.

When the content is long, show the complete version if it fits comfortably in the conversation. If it is too long, show a structured high-detail version with all decisions, route options, module names, assumptions, and questions preserved.

Do not answer a design-stage turn with only a file card, file path, or short note such as "created project_anchor.md" or "created confirmed_framework.md".

## Workflow

Read `references/workflow.md` for the full workflow. Follow these gates:

1. Initial research: show the workflow introduction, then provide a substantial in-chat research summary, candidate routes, recommended starting route if possible, and key questions. Create or update `project_anchor.md` only after the in-chat content has been shown.
2. Solution discussion: after every user instruction, summarize the latest overall route and solution in chat, then ask whether to use this solution direction to begin framework design. Do not write `confirmed_framework.md` at this stage.
3. Framework drafting: only after the user agrees to begin framework design, generate the proposal framework in chat first. Ask whether the user approves this framework or wants changes.
4. Framework confirmation: revise the framework in chat until the user clearly agrees to the latest version. Only then create or update `confirmed_framework.md`.
5. Final Word: when the user asks for the final Word proposal, directly generate `solution_design.md`, run or remind the user to run checks, export Word with `scripts/export_docx.py` if pandoc is available, and report final Word statistics in chat.

## Required User Guidance

After the first research and route proposal, ask focused questions that materially affect the proposal, such as:

- expected Word length or page range
- preferred method difficulty: simple and robust, moderate, or advanced
- required parameters, operating conditions, input data, output products, and constraints
- preferred or excluded technical routes
- whether figures, tables, formulas, or engineering implementation details are expected

Ask only useful questions. If the user gives a direction, proceed with reasonable assumptions and state them.

## Output Files

Use this compact project structure by default:

```text
{project_name}_solution_design/
|-- project_anchor.md
|-- confirmed_framework.md
|-- solution_design.md
`-- exports/
    `-- {project_name}_方案设计.docx
```

Create files when their stage is reached. `scripts/init_solution_project.py` can initialize the folder and empty scaffolds when useful.

## Word Formatting Requirements

Final Word output must be document-style conservative:

- use `assets/reference.docx` as the default pandoc reference document when no user reference docx is provided
- all visible text must be black
- level 1, 2, 3, 4, and deeper headings must use SimSun/宋体 where possible
- all table cells must have no shading, including header cells
- paragraphs inside table cells must not use body-style first-line indentation
- do not perform page PNG visual rendering QA after export unless the user explicitly asks

After Word export, report in chat:

- final Word path
- Markdown source path
- page count when available
- number of tables
- number of figure placeholders
- figure placeholder names

## Runtime Dependencies

The conversation workflow itself does not require extra software. The bundled helper scripts require a Python 3 interpreter available to Codex as `python`, `python3`, `py`, or a runtime-provided Python executable.

The helper scripts use only the Python standard library. Do not ask the user to install PyYAML, python-docx, pypandoc, or other Python packages for normal use of this skill.

If Python is unavailable, do not fail the workflow. Treat the scripts as convenience helpers: create or update the project folders and Markdown files directly, apply the reference rules manually, and export Word with a direct pandoc command after the final Markdown source is generated.

Pandoc is required only for the final Markdown-to-Word export. If pandoc is unavailable, keep the generated Markdown source and tell the user that Word export is blocked until pandoc is installed.

## Reference Files

- `references/workflow.md`: stage-by-stage process and confirmation gates.
- `references/project_anchor_rules.md`: first-anchor structure, research integrity, source handling, and chat display requirements.
- `references/route_selection_rules.md`: technical-route comparison and convergence rules.
- `references/confirmed_framework_rules.md`: framework drafting and second-anchor confirmation rules.
- `references/formal_solution_rules.zh.md`: Chinese formal proposal writing constraints.
- `references/formal_solution_rules.en.md`: English formal proposal writing constraints.
- `references/markdown_math_rules.md`: Markdown math notation rules.
- `references/word_export_rules.md`: final draft, Word formatting, and export feedback rules.
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

This file feedback must come after the useful content has been shown in chat.

# solution-design

`solution-design` is a Codex Skill for algorithm, research, and engineering technical solution design. It is a conversation-first workflow, not a generic writing template.

The skill must show enough information in chat for the user to judge the solution without opening local Markdown files. Local files are memory anchors and final writing sources.

The skill includes `assets/reference.docx` as the default pandoc Word template. Edit this file in Word to tune title, heading, body, table, margin, and spacing styles.

## Use Cases

Use this skill for:

- technical solution proposals
- algorithm solution proposals
- engineering solution reports
- research proposal frameworks
- route comparison and route selection
- Word proposal preparation

Do not use it for direct algorithm implementation, simulation scripting, test-plan generation, test-report generation, fabricated results, automatic plotting, or page PNG visual QA unless the user explicitly asks.

## Workflow

1. Introduce the workflow: deep research, candidate solution, solution discussion, solution confirmation, framework discussion, framework confirmation, final Word.
2. Show research findings, candidate routes, route trade-offs, recommended starting direction, and key questions in chat.
3. Save `project_anchor.md` as a memory anchor after the useful content has appeared in chat.
4. During solution discussion, end every response with the latest overall route and solution summary, then ask whether to begin framework design.
5. After the user agrees, generate the proposal framework in chat first.
6. Revise the framework in chat until the user approves the latest version.
7. Save the approved framework to `confirmed_framework.md`.
8. When the user asks for the final Word proposal, generate `solution_design.md` and export Word.

## Output Files

```text
{project_name}_solution_design/
|-- project_anchor.md
|-- confirmed_framework.md
|-- solution_design.md
`-- exports/
    `-- {project_name}_solution_design.docx
```

For Chinese proposals, the default Word file name is:

```text
{project_name}_方案设计.docx
```

## Word Output

The Word export helper applies these rules where possible:

- use `assets/reference.docx` first when no user `--reference` is provided
- all visible text black
- heading levels use SimSun/宋体
- all table cells have no shading, including header cells
- paragraphs inside table cells have no body-style first-line indentation
- no page PNG visual rendering QA unless explicitly requested

After export, report:

- final Word path
- Markdown source path
- page count when available
- table count
- figure placeholder count
- figure placeholder names

## Install

Copy or sync the `solution-design/` folder into a Codex skills directory, for example:

```text
~/.codex/skills/solution-design/
```

The skill body files should not be copied into each individual user project.

## Runtime Dependencies

From the user's first request through the generated Markdown proposal source, this skill does not require extra software beyond Codex itself.

To run the bundled helper scripts, Codex needs access to a Python 3 interpreter. This may be available as `python`, `python3`, `py`, or a runtime-provided Python executable. The scripts use only the Python standard library, so normal use does not require installing PyYAML, python-docx, pypandoc, or any other Python package.

If Python is unavailable, the workflow should still continue. The scripts are convenience helpers, not a hard runtime gate: create or update the project folder and Markdown files directly, apply the reference rules manually, and use a direct pandoc command after the final Markdown source is generated.

For final Word output, pandoc is required for Markdown-to-Word conversion. If pandoc is unavailable, the skill keeps the generated Markdown source and reports that Word export is blocked until pandoc is installed.

## Trigger Examples

```text
写一个技术方案
帮我设计项目方案框架
我要生成一个 Word 方案
design a solution proposal
write a technical proposal framework
```

## Scripts

Initialize a project:

```bash
python scripts/init_solution_project.py "Project Name" --lang en
python scripts/init_solution_project.py "项目名称" --lang zh
```

Check formal proposal wording:

```bash
python scripts/check_formal_solution.py solution_design.md --lang en
```

Check Markdown math notation:

```bash
python scripts/check_markdown_math.py solution_design.md --lang en
```

Export Word:

```bash
python scripts/export_docx.py solution_design.md --project-name "Project Name" --lang en
python scripts/export_docx.py solution_design.md --reference path/to/reference.docx --project-name "Project Name" --lang en
```

The first command automatically uses `assets/reference.docx` when it exists.

If Python is unavailable but pandoc is installed, export directly:

```bash
pandoc solution_design.md -o exports/Project_Name_solution_design.docx
```

Pandoc is required for Word export. Install the `.msi` package on Windows, the `.pkg` package or Homebrew package on macOS, or use the system package manager on Linux.

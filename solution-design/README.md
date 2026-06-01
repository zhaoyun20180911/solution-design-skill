# solution-design

`solution-design` is a Codex Skill for algorithm, research, and engineering technical solution design. It is a discussion-driven workflow, not a generic writing template.

The skill keeps only two durable local anchors during the design process: one researched project anchor at the beginning, and one confirmed framework anchor after the user has converged the route. Ordinary route discussion happens in chat. When the user asks for the final Word proposal, the skill directly generates the formal Markdown source and exports Word.

## Use Cases

Use this skill for:

- technical solution proposals
- algorithm solution proposals
- engineering solution reports
- research proposal frameworks
- route comparison and route selection
- Word proposal preparation

Do not use it for direct algorithm implementation, simulation scripting, test-plan generation, test-report generation, fabricated results, automatic plotting, or complex docx format QA.

## Workflow

1. Detect user language and print the matching startup message.
2. Build `project_anchor.md` from initial understanding, research, user priorities, constraints, candidate routes, and open questions.
3. Discuss route choices and framework details in chat without saving local discussion logs.
4. Ask the user to confirm the selected route and framework.
5. Save `confirmed_framework.md` with the confirmed route, module boundaries, inputs/outputs, indicators, verification logic, and proposal framework.
6. When the user asks for the final Word proposal, generate `solution_design.md`, run or remind the user to run the checks, and export Word with pandoc.

## Output Files

```text
{project_name}_solution_design/
├── project_anchor.md
├── confirmed_framework.md
├── solution_design.md
└── exports/
    └── {project_name}_solution_design.docx
```

For Chinese proposals, the default Word file name is:

```text
{project_name}_方案设计.docx
```

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

If Python is unavailable but pandoc is installed, export directly:

```bash
pandoc solution_design.md -o exports/Project_Name_solution_design.docx
```

Pandoc is required for Word export. Install the `.msi` package on Windows, the `.pkg` package or Homebrew package on macOS, or use the system package manager on Linux.

## File Feedback

Whenever a key file is created or updated, the assistant must report:

- file name
- path
- purpose
- whether it is the final deliverable
- next use

After Word export, the assistant must separately report:

```text
Final Word file: {project_dir}/exports/{project_name}_solution_design.docx
```

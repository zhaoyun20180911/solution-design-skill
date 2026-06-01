# solution-design

`solution-design` is a Codex Skill for algorithm, research, and engineering technical solution design. It is a discussion-driven workflow, not a generic writing template.

The skill helps users move from an initial topic to a confirmed technical route, a frozen solution outline, a formal Markdown proposal source, and a Word-exportable final document.

## Use Cases

Use this skill for:

- technical solution proposals
- algorithm solution proposals
- engineering solution reports
- research proposal frameworks
- route comparison and route selection
- Word proposal preparation after Markdown draft confirmation

Do not use it for direct algorithm implementation, simulation scripting, test-plan generation, test-report generation, fabricated results, automatic plotting, or complex docx format QA.

## Workflow

1. Detect user language and print the matching startup message.
2. Create a project profile.
3. Create a research pack with candidate routes and learning resources.
4. Ask the user to confirm the technical route.
5. Create a solution outline and technical framework.
6. Ask the user to confirm the outline.
7. Create the formal proposal Markdown source.
8. Run formal-wording and Markdown-math checks.
9. Ask the user to confirm the Markdown source.
10. Export Word with pandoc and report the final Word path.

## Output Modes

Full mode is the default because solution design needs traceable research, outline, and confirmation files:

```text
{project_name}_solution_design/
├── project_profile.md
├── project_research_pack.md
├── solution_outline.md
├── solution_design.md
├── change_log.md
└── exports/
    └── {project_name}_solution_design.docx
```

Clean mode keeps intermediate files under `.solution-design/` and only highlights the Word file:

```text
{project_name}_solution_design/
├── exports/
└── .solution-design/
    ├── project_profile.md
    ├── project_research_pack.md
    ├── solution_outline.md
    ├── solution_design.md
    └── change_log.md
```

## Install

Copy or sync the `solution-design/` folder into a Codex skills directory, for example:

```text
~/.codex/skills/solution-design/
```

The skill body files should not be copied into each individual user project.

## Runtime Dependencies

From the user's first request through the confirmed Markdown proposal, this skill does not require extra software beyond Codex itself.

To run the bundled helper scripts, Codex needs access to a Python 3 interpreter. This may be available as `python`, `python3`, `py`, or a runtime-provided Python executable. The scripts use only the Python standard library, so normal use does not require installing PyYAML, python-docx, pypandoc, or any other Python package.

If Python is unavailable, the workflow should still continue. The scripts are convenience helpers, not a hard runtime gate: create or update the project folders and Markdown files directly, apply the reference rules manually, and use a direct pandoc command after the Markdown draft is confirmed.

For final Word output, pandoc is required for Markdown-to-Word conversion. If pandoc is unavailable, the skill keeps the confirmed Markdown source and reports that Word export is blocked until pandoc is installed.

## Trigger Examples

```text
写一个某工程系统的技术方案
帮我设计某科研项目的方案框架
我要做一个 XXX 的 Word 方案
design a solution proposal for an engineering system
write a technical proposal for a research prototype
```

## Scripts

Initialize a project:

```bash
python scripts/init_solution_project.py "Project Name" --mode full --lang en
python scripts/init_solution_project.py "项目名称" --mode clean --lang zh
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

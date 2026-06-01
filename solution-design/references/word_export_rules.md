# Word Export Rules

The final proposal is drafted as Markdown source and exported to Word in one final step after the user asks for the final Word proposal.

## Preconditions

Before export:

1. `project_anchor.md` exists or its content has been incorporated in the conversation.
2. The solution direction has been discussed and confirmed.
3. The framework has been shown in chat and approved by the user.
4. `confirmed_framework.md` exists or has just been updated from the approved framework.
5. The user has asked to generate the final Word proposal.

Do not add a separate Markdown confirmation gate unless the user explicitly asks to review the Markdown source before export.

## Final Draft

Create `solution_design.md` from the confirmed anchors and discussion. The formal proposal body must not contain:

- AI process text
- user prompt traces
- local file paths
- Markdown or pandoc process notes
- self-weakening statements
- fabricated results, citations, metrics, datasets, or conclusions

Run or remind the user to run:

```bash
python scripts/check_formal_solution.py solution_design.md --lang en
python scripts/check_markdown_math.py solution_design.md --lang en
```

Use `--lang zh` for Chinese proposals.

## Word Style Requirements

Final Word output must use conservative proposal formatting:

- use the bundled `assets/reference.docx` as the default pandoc reference document when no user reference docx is provided
- all visible text black
- all heading levels use SimSun/宋体 where possible
- all table cells have no shading, including header cells
- paragraphs inside table cells have no first-line indentation
- no page PNG visual rendering QA unless the user explicitly asks

Use `scripts/export_docx.py`; it first uses `assets/reference.docx` where available, then post-processes the generated `.docx` with standard-library XML operations to apply these rules where possible.

## Pandoc Check

Run:

```bash
pandoc --version
```

If pandoc is not installed, provide installation guidance:

- Windows: install the `.msi` package.
- macOS: install the `.pkg` package or use Homebrew.
- Linux: use the system package manager.

Do not put pandoc installation instructions into the formal proposal body.

## Export Command

Without a reference docx:

```bash
python scripts/export_docx.py solution_design.md --project-name "Project Name" --lang en
```

This automatically uses the bundled `assets/reference.docx` when it exists.

With a user-provided reference docx:

```bash
python scripts/export_docx.py solution_design.md --project-name "Project Name" --reference path/to/reference.docx --lang en
```

If Python is unavailable but pandoc is installed, bypass the helper script:

```bash
pandoc solution_design.md -o exports/Project_Name_solution_design.docx
```

For Chinese output:

```bash
pandoc solution_design.md -o exports/项目名称_方案设计.docx
```

## Final Feedback

After Word generation, clearly report:

- final Word path
- Markdown source path
- page count when available
- number of tables
- number of figure placeholders
- figure placeholder names
- whether the Word file is the final deliverable

Use an explicit final line:

```text
最终 Word 文件位置：{project_dir}/exports/{project_name}_方案设计.docx
```

For English:

```text
Final Word file: {project_dir}/exports/{project_name}_solution_design.docx
```

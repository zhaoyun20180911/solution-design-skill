# Word Export Rules

The formal proposal is drafted as Markdown source first, then exported to Word after user confirmation.

## Preconditions

Before export:

1. The technical route is confirmed.
2. The solution outline is confirmed.
3. The Markdown source is confirmed.
4. `check_formal_solution.py` and `check_markdown_math.py` have been run or the user has been reminded to run them.

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
- file purpose
- whether the Word file is the final deliverable

Use an explicit final line:

```text
最终 Word 文件位置：{project_dir}/exports/{project_name}_方案设计.docx
```

For English:

```text
Final Word file: {project_dir}/exports/{project_name}_solution_design.docx
```

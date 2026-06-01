# Solution-Design Workflow

## Stage 0: Activation

Detect the user's language and print the matching startup message from `SKILL.md`. Explain only the active workflow boundary: this skill designs a technical solution and does not enter algorithm implementation, simulation scripting, test-plan writing, or test-report writing before the route and outline are confirmed.

## Stage 1: Project Profile

Create or update `project_profile.md` with:

- project topic and intended application scenario
- user goals and expected decision support
- known inputs, outputs, constraints, and existing materials
- unknowns that block route selection
- first-round questions for the user

Do not create a long formal proposal in this stage.

## Stage 2: Research Pack

Create or update `project_research_pack.md` after research or source collection. Include route candidates, relevant algorithms, standards, documentation, papers, open-source projects, search keywords, and the relationship between each source and the user's project.

Do not invent papers, authors, journals, DOI values, standards, links, datasets, or results.

## Confirmation Gate 1: Route Confirmation

Before creating the solution outline, ask the user to confirm the technical route. If the user is unsure, compare routes by function, applicability, implementation difficulty, verification difficulty, input needs, output quality, and risk.

## Stage 3: Solution Outline

Create or update `solution_outline.md` with:

- chapter structure and estimated page allocation
- selected route and route alternatives not selected
- module boundaries, inputs, outputs, and dependencies
- indicator system and verification logic
- figure placeholders that are meaningful to the proposal content

## Confirmation Gate 2: Outline Confirmation

Only generate `solution_design.md` after the user explicitly confirms the outline and technical framework.

## Stage 4: Formal Markdown Draft

Create `solution_design.md` as the formal proposal source. Use real project-proposal language. Do not include AI process text, user prompt traces, Markdown/Word/pandoc process notes, file paths, or self-weakening statements.

After drafting, run:

```bash
python scripts/check_formal_solution.py solution_design.md --lang zh
python scripts/check_markdown_math.py solution_design.md --lang zh
```

Use `--lang en` for English proposals.

## Confirmation Gate 3: Draft Confirmation

Only export Word after the user confirms that the Markdown draft is an acceptable basis for the formal proposal.

## Stage 5: Word Export

Check pandoc availability and export:

```bash
python scripts/export_docx.py solution_design.md --project-name "Project Name" --lang en
```

Use a user-provided reference docx when available. If no real reference docx exists, export without `--reference` and tell the user where to provide one later.

## File Feedback

Whenever a key file is created or updated, tell the user the file name, path, purpose, whether it is a final deliverable, and how it will be used next. After Word export, report the final Word path separately and visibly.

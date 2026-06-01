# Solution-Design Workflow

## Stage 0: Activation

Detect the user's language and print the matching startup message from `SKILL.md`. Explain only the active workflow boundary: this skill designs a technical solution and does not enter algorithm implementation, simulation scripting, test-plan writing, or test-report writing before the route and framework are confirmed.

## Stage 1: First Anchor

Create or update `project_anchor.md` after the initial understanding and research. This file is the durable memory anchor for later discussion and final writing.

Include:

- project topic and application scenario
- user's priority requirements and non-negotiable constraints
- known inputs, outputs, available materials, and assumptions
- research basis, search keywords, candidate technologies, standards, papers, documentation, or open-source references when available
- candidate routes and trade-offs
- unknowns that still affect route selection

Do not write a long formal proposal in this stage. Ask only the questions that materially change route selection or proposal scope.

## Stage 2: Chat Discussion

Discuss the route and framework in the conversation. Explain options, compare trade-offs, and converge the direction with the user.

Do not create local discussion logs for ordinary back-and-forth. Use `project_anchor.md` as the shared reference point when the discussion becomes long or complex.

If live research is needed and no sources are available, ask for sources or search keywords instead of inventing citations.

## Confirmation Gate: Framework Confirmation

Before final proposal drafting, ask the user to confirm the selected route and framework. If the user is unsure, compare routes by function, applicability, implementation difficulty, verification difficulty, input needs, output quality, and risk.

## Stage 3: Second Anchor

Create or update `confirmed_framework.md` only after the user confirms the route and framework.

Include:

- confirmed technical route and rationale
- routes rejected or retained only as comparisons
- module boundaries, inputs, outputs, and dependencies
- indicator system and verification logic
- expected figures or tables needed in the proposal
- final proposal chapter framework and page-count guidance when useful

If the user later changes the route or framework, update `confirmed_framework.md` before drafting the final proposal.

## Stage 4: Final Markdown And Word

When the user asks for the final Word proposal, directly create `solution_design.md` as the formal proposal source from `project_anchor.md`, `confirmed_framework.md`, and the confirmed discussion outcome.

Use real project-proposal language. Do not include AI process text, user prompt traces, Markdown/Word/pandoc process notes, file paths, or self-weakening statements in the formal proposal body.

Run or remind the user to run:

```bash
python scripts/check_formal_solution.py solution_design.md --lang zh
python scripts/check_markdown_math.py solution_design.md --lang zh
```

Use `--lang en` for English proposals.

Export Word immediately after the Markdown source is generated unless the user explicitly asks to review Markdown first:

```bash
python scripts/export_docx.py solution_design.md --project-name "Project Name" --lang en
```

Use a user-provided reference docx when available. If no real reference docx exists, export without `--reference` and tell the user where to provide one later.

## File Feedback

Whenever a key file is created or updated, tell the user the file name, path, purpose, whether it is a final deliverable, and how it will be used next. After Word export, report the final Word path separately and visibly.

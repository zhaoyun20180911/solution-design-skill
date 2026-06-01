# Solution-Design Workflow

## Stage 0: Activation

Detect the user's language and print the matching startup message from `SKILL.md`. Explain the workflow briefly as:

1. deep research
2. candidate solution proposal
3. solution discussion
4. solution confirmation
5. framework discussion
6. framework confirmation
7. final Word generation

The user should understand that chat is the main place to inspect the solution. Local files are anchors and final sources.

## Stage 1: Research And First Anchor

After initial understanding and research, show substantial content in chat before creating or updating `project_anchor.md`.

The chat response must include:

- researched project image and core problem
- major assumptions and known constraints
- research findings or source leads
- candidate technical routes with trade-offs
- recommended starting route when evidence supports one
- key questions that affect proposal depth and route selection

Then create or update `project_anchor.md` as a memory anchor. Do not tell the user to open the file to understand the content.

Ask focused questions such as expected page count, method difficulty, important parameters, input data, output products, operating conditions, preferred or excluded routes, and figure/table expectations.

## Stage 2: Solution Discussion

Discuss solution routes in chat. Each response in this stage must end with:

- a concise but complete latest solution summary
- the current recommended route
- current assumptions
- the next decision question

Ask whether the user wants to use the latest solution direction to begin proposal framework design. Do not create `confirmed_framework.md` yet.

If the user changes a route, constraint, page target, difficulty preference, or deliverable expectation, update the summary in chat before asking for the next decision.

## Stage 3: Framework Draft In Chat

Only after the user agrees to begin framework design, generate the framework in chat first.

The framework shown in chat should include:

- proposed chapter structure
- section and subsection titles
- what each chapter proves
- core module boundaries
- inputs, outputs, and dependencies
- indicator and verification design
- table plan
- figure placeholders and names
- page allocation when relevant

Ask whether the user approves the framework or wants modifications. If the user requests changes, revise the framework in chat and ask again.

## Stage 4: Framework Confirmation And Second Anchor

Only after the user clearly approves the latest framework, create or update `confirmed_framework.md`.

The file must reflect the approved framework, not an earlier version. After saving, show a short confirmation in chat and state that it will be used as the writing basis for `solution_design.md`.

## Stage 5: Final Markdown And Word

When the user asks for the final Word proposal, directly create `solution_design.md` from:

- `project_anchor.md`
- `confirmed_framework.md`
- the confirmed discussion outcome

Do not add a new Markdown confirmation gate unless the user explicitly asks to review Markdown first.

Use real project-proposal language. Do not include AI process text, user prompt traces, Markdown/Word/pandoc process notes, file paths, or self-weakening statements in the formal proposal body.

Run or remind the user to run:

```bash
python scripts/check_formal_solution.py solution_design.md --lang zh
python scripts/check_markdown_math.py solution_design.md --lang zh
```

Use `--lang en` for English proposals.

Export Word:

```bash
python scripts/export_docx.py solution_design.md --project-name "Project Name" --lang en
```

Use a user-provided reference docx when available. If no real reference docx exists, export without `--reference`.

Do not perform page PNG visual rendering QA after export unless the user explicitly asks.

After export, report:

- final Word path
- Markdown source path
- page count when available
- table count
- figure placeholder count
- figure placeholder names

## File Feedback

Whenever a key file is created or updated, tell the user the file name, path, purpose, whether it is a final deliverable, and how it will be used next. This feedback must not replace the substantive in-chat content.

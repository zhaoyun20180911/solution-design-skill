# Project Anchor Rules

`project_anchor.md` is the first durable memory anchor. It preserves the initial research, project image, and user priorities so long discussions do not lose the original requirements.

The anchor does not replace the chat response. Show the research and route content in chat first, then save the anchor.

## Required Chat Display

Before or while saving `project_anchor.md`, show the user:

1. project understanding
2. research findings or source leads
3. candidate routes and trade-offs
4. recommended starting route if there is enough basis
5. key questions that affect route and proposal scope

The user should be able to decide the next step from the chat alone.

## Required Anchor Sections

Use these sections unless the user's task clearly needs a simpler structure:

1. Project topic and application scenario
2. User goals and priority requirements
3. Known inputs, outputs, materials, and constraints
4. Research basis and source notes
5. Candidate technical routes
6. Route-selection uncertainties
7. Next discussion focus

## Research Integrity

Do not invent papers, authors, journals, DOI values, standards, links, datasets, source code repositories, benchmarks, or results.

When no verified sources are available, write source needs explicitly, such as:

```text
Source needed: authoritative documentation, representative papers, standards, or user-provided materials for this route.
```

Search keywords are allowed when they are clearly marked as keywords rather than evidence.

## User Priority Requirements

Capture the user's emphasis in concrete terms:

- mandatory deliverable form
- expected Word length or page range
- preferred method difficulty
- required parameters, operating conditions, input data, and output products
- preferred or excluded technical directions
- figure, table, formula, and engineering detail expectations
- constraints on questioning, local files, and final Word output

Do not paste long raw prompts into the anchor. Summarize them as stable requirements.

## Candidate Routes

For each route, record and show in chat:

- what the route does
- why it may fit the project
- required inputs and assumptions
- expected outputs
- implementation difficulty
- verification difficulty
- major risks

End with a short list of questions that materially affect route selection.

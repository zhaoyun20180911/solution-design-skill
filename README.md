# solution-design Codex Skill

This repository contains the `solution-design` Codex Skill.

The skill folder is:

```text
solution-design/
```

## What It Does

`solution-design` helps Codex guide algorithm, research, and engineering solution-design work through a conversation-first process:

- deep research shown in chat
- candidate solution routes shown and compared in chat
- guided questions about parameters, page target, difficulty, inputs, outputs, figures, and tables
- repeated solution summaries until the user agrees to begin framework design
- framework drafts shown and revised in chat
- approved framework saved as a local anchor
- final Markdown and Word proposal generation

Local Markdown files are memory anchors and writing sources. They are not meant to replace the in-chat explanation.

The skill includes `solution-design/assets/reference.docx` as the default pandoc Word template. Users can edit this file in Word to tune the final proposal style.

## Install With Codex

Ask Codex to install the skill from this repository:

```text
Please install the skill from https://github.com/<owner>/<repo>/tree/main/solution-design
```

Or use the Codex skill installer:

```bash
python <path-to-skill-installer>/install-skill-from-github.py --repo <owner>/<repo> --path solution-design
```

Restart Codex after installation so the new skill is loaded.

## Runtime Notes

The discussion workflow does not require extra Python packages. Helper scripts use only the Python standard library. Pandoc is required only for final Markdown-to-Word export.

The Word export helper uses the bundled `reference.docx` first, then post-processes the `.docx` to keep visible text black, heading fonts in SimSun/宋体 where possible, table cells without shading, and table-cell paragraphs without body-style first-line indentation. It also reports table count and figure placeholder names, and reports page count when the local system can determine it.

See `solution-design/README.md` and `solution-design/README.zh-CN.md` for usage details.

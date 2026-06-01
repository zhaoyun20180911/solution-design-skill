# solution-design Codex Skill

This repository contains the `solution-design` Codex Skill.

The skill folder is:

```text
solution-design/
```

## What It Does

`solution-design` helps Codex guide algorithm, research, and engineering solution-design work from an initial topic to a confirmed technical route, a frozen outline, a formal Markdown proposal, and Word export preparation.

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

The solution-design workflow itself does not require extra Python packages. Helper scripts use only the Python standard library. Pandoc is required only for final Markdown-to-Word export.

See `solution-design/README.md` and `solution-design/README.zh-CN.md` for full usage details.

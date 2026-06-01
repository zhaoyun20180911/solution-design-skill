# Default Reference Placeholder

This MVP does not include a real `default_reference.docx`.

Users may provide their own Word reference template and pass it to:

```bash
python scripts/export_docx.py solution_design.md --reference path/to/reference.docx --lang en
```

If no reference docx is provided, export without `--reference`.

#!/usr/bin/env python3
"""Export a formal solution Markdown file to Word via pandoc."""

from __future__ import annotations

import argparse
import math
import os
import re
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ET.register_namespace("w", W_NS)


def qn(tag: str) -> str:
    return f"{{{W_NS}}}{tag}"


def sanitize_project_name(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", name.strip())
    cleaned = re.sub(r"\s+", "_", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned).strip("._ ")
    return cleaned or "solution_design"


def default_output(markdown_file: Path, project_name: str | None, lang: str) -> Path:
    safe_name = sanitize_project_name(project_name or markdown_file.parent.name.replace("_solution_design", ""))
    filename = f"{safe_name}_方案设计.docx" if lang == "zh" else f"{safe_name}_solution_design.docx"
    return markdown_file.parent / "exports" / filename


def bundled_reference_docx() -> Path:
    return Path(__file__).resolve().parents[1] / "assets" / "reference.docx"


def remove_descendants(parent: ET.Element, tag: str) -> None:
    for child in list(parent):
        if child.tag == tag:
            parent.remove(child)
        else:
            remove_descendants(child, tag)


def ensure_child(parent: ET.Element, tag: str, *, first: bool = False) -> ET.Element:
    child = parent.find(qn(tag))
    if child is not None:
        return child
    child = ET.Element(qn(tag))
    if first:
        parent.insert(0, child)
    else:
        parent.append(child)
    return child


def set_black_color(rpr: ET.Element) -> None:
    color = ensure_child(rpr, "color")
    color.attrib.clear()
    color.set(qn("val"), "000000")


def set_simsun_fonts(rpr: ET.Element) -> None:
    fonts = ensure_child(rpr, "rFonts")
    for attr in ("ascii", "hAnsi", "eastAsia", "cs"):
        fonts.set(qn(attr), "SimSun")


def is_heading_style(style_id: str | None, style_name: str | None = None) -> bool:
    values = [value for value in (style_id, style_name) if value]
    for value in values:
        lowered = value.lower()
        if lowered.startswith("heading"):
            return True
        if value.startswith("标题"):
            return True
    return False


def patch_styles_xml(data: bytes) -> bytes:
    root = ET.fromstring(data)
    remove_descendants(root, qn("shd"))

    for color in root.iter(qn("color")):
        color.attrib.clear()
        color.set(qn("val"), "000000")

    for style in root.iter(qn("style")):
        style_type = style.get(qn("type"))
        style_id = style.get(qn("styleId"))
        name = style.find(qn("name"))
        style_name = name.get(qn("val")) if name is not None else None
        if style_type == "paragraph" and is_heading_style(style_id, style_name):
            rpr = ensure_child(style, "rPr")
            set_simsun_fonts(rpr)
            set_black_color(rpr)

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def paragraph_is_heading(paragraph: ET.Element) -> bool:
    ppr = paragraph.find(qn("pPr"))
    if ppr is None:
        return False
    pstyle = ppr.find(qn("pStyle"))
    if pstyle is None:
        return False
    return is_heading_style(pstyle.get(qn("val")))


def clear_table_cell_paragraph_indents(root: ET.Element) -> None:
    for cell in root.iter(qn("tc")):
        for paragraph in cell.iter(qn("p")):
            ppr = ensure_child(paragraph, "pPr", first=True)
            ind = ensure_child(ppr, "ind")
            for attr in ("left", "right", "firstLine", "hanging"):
                ind.set(qn(attr), "0")
            for attr in ("firstLineChars", "hangingChars"):
                ind.attrib.pop(qn(attr), None)


def patch_document_xml(data: bytes) -> bytes:
    root = ET.fromstring(data)
    remove_descendants(root, qn("shd"))

    for color in root.iter(qn("color")):
        color.attrib.clear()
        color.set(qn("val"), "000000")

    for run in root.iter(qn("r")):
        rpr = ensure_child(run, "rPr", first=True)
        set_black_color(rpr)

    for paragraph in root.iter(qn("p")):
        if paragraph_is_heading(paragraph):
            for run in paragraph.iter(qn("r")):
                rpr = ensure_child(run, "rPr", first=True)
                set_simsun_fonts(rpr)
                set_black_color(rpr)

    clear_table_cell_paragraph_indents(root)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def patch_docx_formatting(docx_path: Path) -> None:
    tmp_path = docx_path.with_suffix(docx_path.suffix + ".tmp")
    with zipfile.ZipFile(docx_path, "r") as src, zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as dst:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "word/document.xml":
                data = patch_document_xml(data)
            elif info.filename == "word/styles.xml":
                data = patch_styles_xml(data)
            dst.writestr(info, data)
    for attempt in range(5):
        try:
            tmp_path.replace(docx_path)
            return
        except PermissionError:
            if attempt == 4:
                raise
            time.sleep(0.4)


def count_docx_tables(docx_path: Path) -> int:
    try:
        with zipfile.ZipFile(docx_path, "r") as package:
            data = package.read("word/document.xml")
        root = ET.fromstring(data)
        return len(list(root.iter(qn("tbl"))))
    except Exception:
        return 0


def extract_pages_from_app_xml(docx_path: Path) -> int | None:
    try:
        with zipfile.ZipFile(docx_path, "r") as package:
            data = package.read("docProps/app.xml")
        root = ET.fromstring(data)
        for elem in root.iter():
            if elem.tag.endswith("Pages") and elem.text and elem.text.strip().isdigit():
                pages = int(elem.text.strip())
                return pages if pages > 0 else None
    except Exception:
        return None
    return None


def exact_page_count_with_word(docx_path: Path) -> int | None:
    if os.name != "nt":
        return None
    script = r"""
$ErrorActionPreference = 'Stop'
$path = $args[0]
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
  $doc = $word.Documents.Open($path, $false, $true)
  $pages = $doc.ComputeStatistics(2)
  $doc.Close($false)
  Write-Output $pages
}
finally {
  $word.Quit()
}
"""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script, str(docx_path)],
            text=True,
            capture_output=True,
            timeout=45,
        )
    except Exception:
        return None
    if result.returncode != 0:
        return None
    match = re.search(r"\d+", result.stdout)
    return int(match.group(0)) if match else None


def estimate_pages_from_markdown(markdown_file: Path) -> int:
    text = markdown_file.read_text(encoding="utf-8", errors="ignore")
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    cjk_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    ascii_words = len(re.findall(r"\b[A-Za-z0-9][A-Za-z0-9_\-]*\b", text))
    tables = len(re.findall(r"^\s*\|.*\|\s*$", text, flags=re.M))
    units = cjk_chars + ascii_words * 2 + tables * 20
    return max(1, math.ceil(units / 950))


def page_count_summary(docx_path: Path, markdown_file: Path, lang: str) -> str:
    exact = exact_page_count_with_word(docx_path)
    if exact is not None:
        return f"页数：{exact} 页" if lang == "zh" else f"Pages: {exact}"

    metadata_pages = extract_pages_from_app_xml(docx_path)
    if metadata_pages is not None:
        return f"页数：{metadata_pages} 页（来自文档元数据）" if lang == "zh" else f"Pages: {metadata_pages} (from document metadata)"

    estimated = estimate_pages_from_markdown(markdown_file)
    return (
        f"页数：约 {estimated} 页（未能自动读取 Word 精确页数）"
        if lang == "zh"
        else f"Pages: about {estimated} (exact Word page count unavailable)"
    )


def extract_figure_placeholders(markdown_file: Path) -> list[str]:
    text = markdown_file.read_text(encoding="utf-8", errors="ignore")
    figures: list[str] = []
    seen: set[str] = set()
    in_code = False
    patterns = [
        re.compile(r"^\s*(?:图|圖)\s*([0-9一二三四五六七八九十]+)[\s:：、.-]*(.+?)\s*$"),
        re.compile(r"^\s*(?:Figure|Fig\.)\s*([0-9]+)[\s:：.-]*(.+?)\s*$", re.I),
    ]
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not stripped or stripped.startswith("!"):
            continue
        for pattern in patterns:
            match = pattern.match(stripped)
            if match:
                title = match.group(2).strip(" ：:.-")
                if title and not title.startswith("备注") and title not in seen:
                    seen.add(title)
                    figures.append(title)
                break
    return figures


def print_missing_pandoc(lang: str, output: Path, markdown_file: Path) -> None:
    if lang == "zh":
        print("未检测到 pandoc，暂不能生成 Word 文件。")
        print("安装提示：Windows 可安装 .msi，macOS 可安装 .pkg 或使用 Homebrew，Linux 可使用系统包管理器。")
        print(f"最终 Word 文件（尚未生成）：{output}")
        print(f"Markdown 源文件：{markdown_file}")
    else:
        print("Pandoc is not installed, so the Word file cannot be generated yet.")
        print("Install hint: use the .msi installer on Windows, .pkg or Homebrew on macOS, or a package manager on Linux.")
        print(f"Final Word file (not generated): {output}")
        print(f"Markdown source file: {markdown_file}")


def print_success(lang: str, output: Path, markdown_file: Path) -> None:
    tables = count_docx_tables(output)
    figures = extract_figure_placeholders(markdown_file)
    pages = page_count_summary(output, markdown_file, lang)

    if lang == "zh":
        print("Word 正式方案文档已生成：")
        print(f"路径：{output}")
        print("作用：这是本次方案设计的最终 Word 交付文件，可直接打开查看和继续编辑。")
        print("格式处理：已优先使用 reference.docx 模板，并尽量兜底修正为全文黑色、各级标题宋体、表格无底纹、表格单元格无首行缩进。")
        print("\nMarkdown 源文件也已保留：")
        print(f"路径：{markdown_file}")
        print("作用：这是 Word 文档的源文件，后续如需大幅修改方案，建议先修改该文件后重新导出 Word。")
        print("\n文档统计：")
        print(f"- {pages}")
        print(f"- 表格数量：{tables}")
        print(f"- 图位数量：{len(figures)}")
        if figures:
            print("- 图位名称：")
            for figure in figures:
                print(f"  - {figure}")
        else:
            print("- 图位名称：无")
        print(f"\n最终 Word 文件位置：{output}")
    else:
        print("Formal Word proposal generated:")
        print(f"Path: {output}")
        print("Purpose: this is the final Word deliverable for the solution-design task.")
        print("Formatting: reference.docx was used first when available; fallback cleanup sets visible text to black, heading fonts to SimSun where possible, removes table shading, and removes first-line indentation inside table cells.")
        print("\nMarkdown source retained:")
        print(f"Path: {markdown_file}")
        print("Purpose: use this source file for major revisions before exporting Word again.")
        print("\nDocument statistics:")
        print(f"- {pages}")
        print(f"- Tables: {tables}")
        print(f"- Figure placeholders: {len(figures)}")
        if figures:
            print("- Figure placeholder names:")
            for figure in figures:
                print(f"  - {figure}")
        else:
            print("- Figure placeholder names: none")
        print(f"\nFinal Word file: {output}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export solution-design Markdown to Word.")
    parser.add_argument("markdown_file", type=Path)
    parser.add_argument("--project-name")
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    args = parser.parse_args()

    markdown_file = args.markdown_file.resolve()
    if not markdown_file.exists():
        print(f"File not found: {markdown_file}")
        return 2

    output = (args.output.resolve() if args.output else default_output(markdown_file, args.project_name, args.lang).resolve())
    pandoc = shutil.which("pandoc")
    if not pandoc:
        print_missing_pandoc(args.lang, output, markdown_file)
        return 2

    output.parent.mkdir(parents=True, exist_ok=True)
    command = [pandoc, str(markdown_file), "-o", str(output)]
    default_reference = bundled_reference_docx()
    if args.reference:
        reference = args.reference.resolve()
        if reference.exists():
            command.append(f"--reference-doc={reference}")
        else:
            print(f"Reference docx not found, continuing without it: {reference}")
    elif default_reference.exists():
        command.append(f"--reference-doc={default_reference}")

    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        return result.returncode

    patch_docx_formatting(output)
    print_success(args.lang, output, markdown_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

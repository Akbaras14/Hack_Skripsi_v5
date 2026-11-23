"""Penyusun DOCX/PDF dari bab Markdown dan registri sumber yang sudah diaudit."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from storage import ThesisError, local_attachment, read_json, read_text, sha256_file, timestamp, write_json
from audit import CITE_PATTERN, CLAIM_PATTERN

INLINE_PATTERN = re.compile(r"(\[cite:SRC-\d{3,}\]|\[claim:CLM-\d{3,}\]|\*\*[^*]+\*\*|\*[^*]+\*)")
IMAGE_PATTERN = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$")
TABLE_SEPARATOR = re.compile(r"^\s*\|?(?:\s*:?-{3,}:?\s*\|)+\s*:?-{3,}:?\s*\|?\s*$")


def name_for_citation(author: str) -> str:
    """Mendapatkan nama keluarga dari metadata manusia; perlu telaah untuk nama non-Barat."""
    cleaned = author.strip()
    if "," in cleaned:
        return cleaned.split(",", 1)[0].strip()
    return cleaned.split()[-1] if cleaned else "[Penulis belum diverifikasi]"


def cite_label(source: dict[str, Any]) -> str:
    """Menghasilkan teks sitasi penulis-tahun dari registry tanpa mencipta metadata."""
    authors = [name_for_citation(name) for name in source.get("authors", [])]
    if not authors:
        raise ThesisError(f"Penulis sumber belum tersedia: {source.get('id')}")
    lead = authors[0] if len(authors) == 1 else f"{authors[0]} & {authors[1]}" if len(authors) == 2 else f"{authors[0]} et al."
    return f"({lead}, {source['year']})"


def bibliography_entry(source: dict[str, Any]) -> str:
    """Membentuk draf daftar pustaka penulis-tahun; validasi APA 7 akhir tetap manual."""
    names = ", ".join(source.get("authors", []))
    year = source.get("year", "n.d.")
    venue = source.get("venue", "")
    title = str(source.get("title", "")).rstrip(".")
    identifier = f"https://doi.org/{source['doi']}" if source.get("doi") else source.get("url", "")
    return f"{names}. ({year}). {title}. {venue}. {identifier}".strip()


def replace_tokens(value: str, sources: dict[str, dict[str, Any]]) -> str:
    """Mengganti ID sitasi, menghilangkan tag internal klaim, dan menolak sumber tak dikenal."""
    def change(match: re.Match[str]) -> str:
        source_id = match.group(1)
        if source_id not in sources:
            raise ThesisError(f"Sitasi tidak terdaftar: {source_id}")
        return cite_label(sources[source_id])
    without_claims = CLAIM_PATTERN.sub("", value)
    return CITE_PATTERN.sub(change, without_claims)


def append_inline(paragraph: Any, text: str, sources: dict[str, dict[str, Any]]) -> None:
    """Mengonversi sintaks tebal/miring sederhana tanpa merusak penanda sitasi."""
    for part in INLINE_PATTERN.split(text):
        if not part:
            continue
        resolved = replace_tokens(part, sources)
        if part.startswith("**") and part.endswith("**"):
            paragraph.add_run(resolved[2:-2]).bold = True
        elif part.startswith("*") and part.endswith("*"):
            paragraph.add_run(resolved[1:-1]).italic = True
        else:
            paragraph.add_run(resolved)


def render_markdown(doc: Any, text: str, workspace: Path, sources: dict[str, dict[str, Any]]) -> None:
    """Menambahkan heading, paragraf, daftar, tabel, dan gambar lokal ke dokumen Word."""
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index].rstrip()
        if not line.strip():
            index += 1
            continue
        image = IMAGE_PATTERN.match(line)
        if image:
            alt, raw_path = image.groups()
            image_file = local_attachment(workspace, raw_path)
            if not image_file.is_file() or image_file.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
                raise ThesisError(f"Gambar lokal tidak tersedia/format tidak didukung: {raw_path}")
            from docx.shared import Inches
            doc.add_picture(str(image_file), width=Inches(5.4))
            if alt:
                doc.add_paragraph(alt, style="Caption")
            index += 1
            continue
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            if 1 <= level <= 3 and len(line) > level and line[level] == " ":
                paragraph = doc.add_heading(level=level)
                append_inline(paragraph, line[level + 1:].strip(), sources)
                index += 1
                continue
        if line.startswith("|") and index + 1 < len(lines) and TABLE_SEPARATOR.match(lines[index + 1]):
            headers = [column.strip() for column in line.strip("|").split("|")]
            index += 2
            body: list[list[str]] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                body.append([column.strip() for column in lines[index].strip().strip("|").split("|")])
                index += 1
            table = doc.add_table(rows=1, cols=len(headers))
            table.style = "Table Grid"
            for cell, header in zip(table.rows[0].cells, headers):
                append_inline(cell.paragraphs[0], header, sources)
            for values in body:
                row = table.add_row()
                for col_index, cell in enumerate(row.cells):
                    append_inline(cell.paragraphs[0], values[col_index] if col_index < len(values) else "", sources)
            continue
        match_bullet = re.match(r"^\s*[-*]\s+(.*)", line)
        match_number = re.match(r"^\s*\d+\.\s+(.*)", line)
        if match_bullet or match_number:
            paragraph = doc.add_paragraph(style="List Bullet" if match_bullet else "List Number")
            append_inline(paragraph, (match_bullet or match_number).group(1), sources)
            index += 1
            continue
        if line.startswith("> "):
            paragraph = doc.add_paragraph(style="Quote")
            append_inline(paragraph, line[2:], sources)
            index += 1
            continue
        # Gabungkan wrapped lines hingga baris kosong/heading/daftar/tabel baru.
        paragraph_lines = [line]
        index += 1
        while index < len(lines):
            next_line = lines[index]
            if not next_line.strip() or re.match(r"^(#|\||[-*]\s|\d+\.\s|!\[|>\s)", next_line):
                break
            paragraph_lines.append(next_line.strip())
            index += 1
        paragraph = doc.add_paragraph()
        append_inline(paragraph, " ".join(paragraph_lines), sources)


def add_field(paragraph: Any, instruction: str) -> None:
    """Memasukkan Word field (page number/daftar isi) agar dapat diperbarui Word."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    code = OxmlElement("w:instrText")
    code.set(qn("xml:space"), "preserve")
    code.text = instruction
    middle = OxmlElement("w:fldChar")
    middle.set(qn("w:fldCharType"), "separate")
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for element in (begin, code, middle, end):
        run._r.append(element)


def render_docx(workspace: Path, destination: Path, mode: str) -> list[str]:
    """Menyusun DOCX menggunakan python-docx; mengembalikan ID sumber yang dirujuk."""
    try:
        from docx import Document
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.shared import Cm, Pt
    except ImportError as exc:
        raise ThesisError("Paket python-docx tidak tersedia. Instal: python -m pip install python-docx") from exc
    project = read_json(workspace / "project.json")
    source_items = read_json(workspace / "registry" / "sources.json", [])
    sources = {str(source["id"]): source for source in source_items}
    used_sources: set[str] = set()
    document = Document()
    section = document.sections[0]
    fmt = project.get("formatting", {})
    section.left_margin = Cm(float(fmt.get("margin_left_cm", 4.0)))
    section.right_margin = Cm(float(fmt.get("margin_right_cm", 3.0)))
    section.top_margin = Cm(float(fmt.get("margin_top_cm", 3.5)))
    section.bottom_margin = Cm(float(fmt.get("margin_bottom_cm", 3.0)))
    body_style = document.styles["Normal"]
    body_style.font.name = str(fmt.get("font", "Times New Roman"))
    body_style.font.size = Pt(float(fmt.get("font_size_pt", 12)))
    body_style.paragraph_format.line_spacing = float(fmt.get("line_spacing", 1.5))
    body_style.paragraph_format.space_after = Pt(6)
    for heading_style in ("Heading 1", "Heading 2", "Heading 3", "Title"):
        document.styles[heading_style].font.name = body_style.font.name
        from docx.shared import RGBColor
        document.styles[heading_style].font.color.rgb = RGBColor(0, 0, 0)

    # Status dipasang pada kepala halaman untuk mencegah preview draf dikira final.
    header = section.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    label = {"draft": "DRAF — BUKAN DOKUMEN FINAL", "review": "SIAP DITINJAU — BELUM DISAHKAN", "final": "VERSI FINAL — SESUAI CATATAN PERSETUJUAN"}[mode]
    header.add_run(label).bold = True
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_field(footer, " PAGE ")

    title = str(project.get("title", "[JUDUL BELUM DIISI]")) or "[JUDUL BELUM DIISI]"
    document.add_heading(title.upper(), level=0)
    for key, label_key in (("student_name", "Peneliti"), ("student_id", "NIM"), ("program", "Program studi"), ("university", "Perguruan tinggi"), ("year", "Tahun")):
        document.add_paragraph(f"{label_key}: {project.get(key) if project.get(key) not in (None, '') else '[BELUM DIISI]'}")
    document.add_paragraph("Status: " + label)
    document.add_page_break()

    # Lembar pengesahan hanya diikutkan jika diisi secara eksplisit.
    for front_name in ("lembar-pengesahan.md", "abstrak-id.md", "abstract-en.md"):
        front_path = workspace / "frontmatter" / front_name
        if front_path.is_file():
            body = read_text(front_path)
            used_sources.update(CITE_PATTERN.findall(body))
            render_markdown(document, body, workspace, sources)
            document.add_page_break()

    document.add_heading("Daftar Isi", level=1)
    document.add_paragraph("Nomor halaman disusun saat ekspor PDF; jika naskah diubah di Word, periksa kembali daftar isi.")
    # Setiap heading bab/subbab diberi entri, lalu nomor halaman diisi berdasarkan PDF render.
    toc_number = 0
    for number in range(1, 6):
        chapter_path = workspace / "chapters" / f"bab-{number}.md"
        if not chapter_path.is_file():
            continue
        for line in read_text(chapter_path).splitlines():
            match = re.match(r"^(#{1,2})\s+(.+)$", line)
            if not match:
                continue
            toc_number += 1
            heading_level = len(match.group(1))
            paragraph = document.add_paragraph()
            paragraph.paragraph_format.left_indent = Cm(0 if heading_level == 1 else 0.6)
            heading = replace_tokens(match.group(2).strip(), sources)
            paragraph.add_run(heading)
            paragraph.add_run(f"  [[TOC-PAGE-{toc_number:03d}]]")
    document.add_page_break()

    for number in range(1, 6):
        chapter_file = workspace / "chapters" / f"bab-{number}.md"
        if chapter_file.is_file():
            body = read_text(chapter_file)
            used_sources.update(CITE_PATTERN.findall(body))
            render_markdown(document, body, workspace, sources)
            document.add_page_break()

    if used_sources:
        document.add_heading("Daftar Pustaka", level=1)
        for source_id in sorted(used_sources, key=lambda ident: (name_for_citation(sources[ident]["authors"][0]).lower(), str(sources[ident].get("year")))):
            paragraph = document.add_paragraph()
            paragraph.paragraph_format.left_indent = Cm(1.1)
            paragraph.paragraph_format.first_line_indent = Cm(-1.1)
            paragraph.add_run(bibliography_entry(sources[source_id]))
    appendices = sorted((workspace / "appendices").glob("*.md"))
    if appendices:
        document.add_page_break()
        document.add_heading("Lampiran", level=1)
        for appendix in appendices:
            render_markdown(document, read_text(appendix), workspace, sources)

    # Meminta aplikasi pengolah dokumen memperbarui field saat berkas dibuka.
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    settings = document.settings.element
    update_fields = OxmlElement("w:updateFields")
    update_fields.set(qn("w:val"), "true")
    settings.append(update_fields)
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        document.save(destination)
    except (OSError, ValueError) as exc:
        raise ThesisError(f"Gagal membuat DOCX {destination}: {exc}") from exc
    return sorted(used_sources)


def convert_pdf(docx: Path, output_dir: Path) -> Path:
    """Mengonversi dokumen lewat LibreOffice; kegagalan selalu dihentikan eksplisit."""
    executable = shutil.which("libreoffice") or shutil.which("soffice")
    if not executable:
        raise ThesisError("LibreOffice tidak terpasang; instal untuk mengaktifkan ekspor PDF.")
    profile = output_dir / ".lo-profile"
    profile.mkdir(parents=True, exist_ok=True)
    command = [executable, f"-env:UserInstallation=file://{profile.resolve()}", "--headless", "--convert-to", "pdf:writer_pdf_Export", "--outdir", str(output_dir), str(docx)]
    try:
        process = subprocess.run(command, capture_output=True, text=True, timeout=90, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ThesisError(f"Ekspor PDF gagal: {exc}") from exc
    result = output_dir / f"{docx.stem}.pdf"
    if process.returncode != 0 or not result.is_file() or result.stat().st_size == 0:
        raise ThesisError(f"LibreOffice gagal membuat PDF (exit={process.returncode}): {process.stdout} {process.stderr}")
    return result


def fill_toc_page_numbers(workspace: Path, word_path: Path, pdf_path: Path) -> dict[str, int]:
    """Mengisi nomor halaman daftar isi berdasarkan posisi heading pada PDF hasil render."""
    try:
        from docx import Document
        from pypdf import PdfReader
    except ImportError as exc:
        raise ThesisError("Paket pypdf diperlukan untuk daftar isi otomatis: pip install pypdf") from exc
    reader = PdfReader(str(pdf_path))
    normalized_pages = [re.sub(r"\s+", " ", (page.extract_text() or "")).strip() for page in reader.pages]
    toc_index = next((i for i, page in enumerate(normalized_pages) if "Daftar Isi" in page), -1)
    if toc_index < 0:
        raise ThesisError("Halaman daftar isi tidak ditemukan setelah konversi PDF.")
    # Halaman daftar isi dapat lebih dari satu; cari halaman BAB I asli sebagai batas.
    # Pada hasil DOCX standar, dua baris pertama adalah kepala halaman dan nomor halaman.
    chapter_start = -1
    for i in range(toc_index + 1, len(reader.pages)):
        lines = [line.strip() for line in (reader.pages[i].extract_text() or "").splitlines() if line.strip()]
        if len(lines) >= 3 and re.match(r"^BAB\s+(?:I|1)\b", lines[2], re.IGNORECASE):
            chapter_start = i
            break
    if chapter_start < 0:
        raise ThesisError("Halaman Bab I asli tidak ditemukan; nomor halaman daftar isi tidak dapat dihitung dengan aman.")
    headings: list[tuple[str, str]] = []
    toc_number = 0
    for chapter_number in range(1, 6):
        chapter_path = workspace / "chapters" / f"bab-{chapter_number}.md"
        if not chapter_path.is_file():
            continue
        for line in read_text(chapter_path).splitlines():
            match = re.match(r"^(#{1,2})\s+(.+)$", line)
            if match:
                toc_number += 1
                headings.append((f"[[TOC-PAGE-{toc_number:03d}]]", match.group(2).strip()))
    resolved: dict[str, int] = {}
    for marker, original_heading in headings:
        target = re.sub(r"\s+", " ", original_heading).strip()
        for index in range(chapter_start, len(normalized_pages)):
            if target in normalized_pages[index]:
                resolved[marker] = index + 1
                break
    doc = Document(str(word_path))
    for paragraph in doc.paragraphs:
        for marker, heading in headings:
            # Penanda awal dan halaman dari iterasi sebelumnya sama-sama dapat diganti.
            if not paragraph.text.startswith(heading + "  "):
                continue
            if not paragraph.runs:
                continue
            paragraph.runs[-1].text = "  " + str(resolved.get(marker, "?"))
            break
    doc.save(word_path)
    return resolved


def build_documents(workspace: Path, mode: str, docx_only: bool = False) -> dict[str, Any]:
    """Mengekspor DOCX/PDF, menyelaraskan daftar isi, dan merekam manifest audit."""
    output_dir = workspace / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = f"skripsi-{mode}"
    word_path = output_dir / f"{slug}.docx"
    if mode == "final" and docx_only:
        raise ThesisError("Mode final mewajibkan PDF untuk menghitung dan memeriksa daftar isi; jangan gunakan --docx-only.")
    used_sources = render_docx(workspace, word_path, mode)
    page_map: dict[str, int] = {}
    pdf_path = None
    if docx_only:
        # Hindari penanda internal pada berkas yang langsung dibuka peneliti.
        from docx import Document
        word_document = Document(str(word_path))
        for paragraph in word_document.paragraphs:
            for run in paragraph.runs:
                run.text = re.sub(r"\[\[TOC-PAGE-\d{3}\]\]", "—", run.text)
        word_document.save(word_path)
    else:
        first_pdf = convert_pdf(word_path, output_dir)
        page_map = fill_toc_page_numbers(workspace, word_path, first_pdf)
        heading_total = sum(1 for chapter in (workspace / "chapters").glob("bab-*.md")
                            for line in read_text(chapter).splitlines() if re.match(r"^#{1,2}\s+", line))
        if mode != "draft" and len(page_map) != heading_total:
            raise ThesisError(f"Nomor halaman daftar isi tidak lengkap ({len(page_map)}/{heading_total}); periksa heading dan hasil PDF.")
        # Iterasi untuk kasus halaman daftar isi bergeser karena panjang digit berubah.
        first_pdf.unlink(missing_ok=True)
        pdf_path = convert_pdf(word_path, output_dir)
        for _ in range(3):
            latest_map = fill_toc_page_numbers(workspace, word_path, pdf_path)
            if latest_map == page_map:
                break
            page_map = latest_map
            pdf_path.unlink(missing_ok=True)
            pdf_path = convert_pdf(word_path, output_dir)
        else:
            if mode != "draft":
                raise ThesisError("Nomor halaman daftar isi tidak stabil setelah beberapa render. Periksa secara manual.")
    generated = [{"path": word_path.relative_to(workspace).as_posix(), "sha256": sha256_file(word_path)}]
    if pdf_path is not None:
        generated.append({"path": pdf_path.relative_to(workspace).as_posix(), "sha256": sha256_file(pdf_path)})
    manifest = {
        "generated_at": timestamp(), "mode": mode, "files": generated,
        "source_ids_used": used_sources, "toc_entries_resolved": len(page_map),
        "notes": ["Bibliografi APA 7 merupakan draf berbasis metadata yang harus ditelaah manual.",
                  "Daftar isi PDF memiliki entri dan nomor halaman dari hasil render, tetapi tetap perlu audit visual.",
                  "DOCX tanpa PDF mungkin menampilkan penanda nomor halaman yang perlu diisi setelah dirender.",
                  "Status final bukan pengesahan independen; periksa autentisitas persetujuan."],
    }
    write_json(output_dir / f"manifest-{mode}.json", manifest)
    return manifest

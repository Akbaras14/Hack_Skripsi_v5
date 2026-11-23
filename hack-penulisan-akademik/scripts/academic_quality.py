"""Audit mutu akademik non-determinatif: keterbacaan, frasa berulang, kemiripan sumber, dan jejak peninjauan.

Modul ini sengaja tidak menghitung probabilitas penulis AI, skor plagiarisme,
atau mengesahkan isi sitasi secara otomatis. Seluruh ambang adalah petunjuk editorial.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from storage import ThesisError, local_attachment, read_json, read_text, sha256_file, timestamp, write_json

WORD_RE = re.compile(r"[^\W_]+(?:[-’'][^\W_]+)*", re.UNICODE)
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-ZÀ-Ý0-9])")
CITE_RE = re.compile(r"\[cite:(SRC-\d{3,})\]")
GENERIC = (
    "di era digital yang semakin berkembang",
    "seiring dengan perkembangan teknologi yang semakin pesat",
    "memainkan peran yang sangat penting",
    "hal ini menunjukkan bahwa penelitian ini sangat penting",
    "dengan demikian dapat disimpulkan bahwa",
)
REVIEW_DOMAINS = ("human_writing", "citation_integrity", "patchwriting", "original_contribution", "readability")


@dataclass(frozen=True)
class QualityFinding:
    """Hasil pemeriksaan yang selalu memerlukan konteks manusia."""

    code: str
    category: str
    level: str
    location: str
    observation: str
    suggestion: str
    evidence: str = ""


def normalize_tokens(raw: str) -> list[str]:
    """Memisahkan kata Unicode dengan tetap mempertahankan urutan untuk audit frasa."""
    return [match.group(0).casefold() for match in WORD_RE.finditer(raw)]


def manuscript_digest(workspace: Path) -> str:
    """Mengikat persetujuan pada versi naskah dan registri bukti/substansi utama."""
    digest = hashlib.sha256()
    for chapter in sorted((workspace / "chapters").glob("bab-[1-5].md")):
        digest.update(chapter.name.encode("utf-8"))
        digest.update(chapter.read_bytes())
    for front in sorted((workspace / "frontmatter").glob("*.md")):
        digest.update(front.name.encode("utf-8"))
        digest.update(front.read_bytes())
    # Perubahan metadata penelitian, sumber, hasil, atau kontribusi wajib
    # memicu pemeriksaan ulang bahkan jika paragraf belum berubah.
    for filename in ("project.json", "registry/sources.json", "registry/evidence.json",
                     "registry/claims.json", "registry/contributions.json", "registry/source_texts.json"):
        source = workspace / filename
        if source.is_file():
            digest.update(filename.encode("utf-8"))
            digest.update(source.read_bytes())
    return digest.hexdigest()


def citation_digest(workspace: Path) -> str:
    """Mengikat review sitasi pada teks bab dan metadata sumber, bukan kontribusi yang tak terkait."""
    digest = hashlib.sha256()
    for chapter in sorted((workspace / "chapters").glob("bab-[1-5].md")):
        digest.update(chapter.name.encode("utf-8"))
        digest.update(chapter.read_bytes())
    source_registry = workspace / "registry" / "sources.json"
    if source_registry.is_file():
        digest.update(source_registry.read_bytes())
    return digest.hexdigest()


def paragraphs_from_markdown(markdown: str) -> list[tuple[int, str]]:
    """Mengambil paragraf prosa beserta nomor baris, mengecualikan kode dan tabel Markdown."""
    paragraphs: list[tuple[int, str]] = []
    pending: list[str] = []
    first_line = 1
    code_fence = False
    def flush() -> None:
        """Menutup satu paragraf prosa bila buffer berisi kalimat biasa."""
        nonlocal pending
        if pending:
            paragraphs.append((first_line, " ".join(pending)))
            pending = []
    for line_number, raw in enumerate(markdown.splitlines(), start=1):
        stripped = raw.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            flush()
            code_fence = not code_fence
            continue
        if code_fence or not stripped or stripped.startswith(("#", "|", "- ", "* ", ">", "![", "---")):
            flush()
            continue
        if not pending:
            first_line = line_number
        pending.append(re.sub(r"\[claim:CLM-\d{3,}\]|\[cite:SRC-\d{3,}\]", "", stripped))
    flush()
    return paragraphs


def readability_findings(chapter: Path) -> list[QualityFinding]:
    """Menandai masalah keterbacaan dan pola klise yang memerlukan inspeksi editor."""
    findings: list[QualityFinding] = []
    paragraphs = paragraphs_from_markdown(read_text(chapter))
    previous_starts: Counter[str] = Counter()
    for line_no, paragraph in paragraphs:
        words = normalize_tokens(paragraph)
        location = f"{chapter.name}:baris {line_no}"
        if len(words) >= 175:
            findings.append(QualityFinding("READ-001", "readability", "REVIEW", location,
                f"Paragraf cukup padat ({len(words)} kata).", "Evaluasi pemecahan paragraf hanya bila alur gagasan terbantu."))
        sentences = [s.strip() for s in SENTENCE_RE.split(paragraph) if s.strip()]
        for sentence in sentences:
            count = len(normalize_tokens(sentence))
            if count > 48:
                findings.append(QualityFinding("READ-002", "readability", "REVIEW", location,
                    f"Kalimat panjang ({count} kata).", "Periksa subjek, predikat, klausa, dan hubungan logis; jangan memecah secara acak.", sentence[:135]))
        lower = paragraph.casefold()
        for phrase in GENERIC:
            if phrase in lower:
                findings.append(QualityFinding("HAW-001", "human_writing", "INFO", location,
                    "Ditemukan frasa umum yang mungkin kurang spesifik.", "Pertahankan bila bermakna; bila tidak, ganti dengan fakta atau konteks penelitian.", phrase))
        prefix = " ".join(words[:4])
        if len(words) > 10:
            previous_starts[prefix] += 1
    for prefix, count in previous_starts.items():
        if count >= 3:
            findings.append(QualityFinding("HAW-002", "human_writing", "INFO", chapter.name,
                f"Pembukaan paragraf serupa muncul {count} kali.", "Nilai apakah pengulangan diperlukan untuk kohesi; revisi hanya jika redundan.", prefix))
    return findings


def matching_phrases(paragraph: str, source_text: str, min_tokens: int = 9) -> list[str]:
    """Mencari rangkaian kata sama yang panjang sebagai petunjuk review; bukan skor plagiarisme."""
    # Indeks n-gram memberi kompleksitas yang lebih terkontrol daripada
    # perbandingan karakter penuh pada sumber panjang atau repetitif.
    a = normalize_tokens(paragraph)
    b = normalize_tokens(source_text)
    if len(a) < min_tokens or len(b) < min_tokens:
        return []
    index: dict[tuple[str, ...], list[int]] = {}
    for position in range(len(b) - min_tokens + 1):
        key = tuple(b[position:position + min_tokens])
        slots = index.setdefault(key, [])
        if len(slots) < 3:
            slots.append(position)
    found: set[str] = set()
    for position in range(len(a) - min_tokens + 1):
        key = tuple(a[position:position + min_tokens])
        for candidate in index.get(key, []):
            start, source_start = position, candidate
            while start > 0 and source_start > 0 and a[start - 1] == b[source_start - 1]:
                start -= 1
                source_start -= 1
            finish, source_finish = position + min_tokens, candidate + min_tokens
            while finish < len(a) and source_finish < len(b) and a[finish] == b[source_finish]:
                finish += 1
                source_finish += 1
            found.add(" ".join(a[start:finish]))
    return sorted(found, key=lambda phrase: -len(phrase.split()))[:3]


def patchwriting_findings(workspace: Path, chapter: Path) -> list[QualityFinding]:
    """Membandingkan prosa dengan berkas teks sumber yang dilampirkan dan terdaftar."""
    findings: list[QualityFinding] = []
    sources = {s["id"]: s for s in read_json(workspace / "registry" / "sources.json", [])}
    snippets = read_json(workspace / "registry" / "source_texts.json", [])
    paragraphs = paragraphs_from_markdown(read_text(chapter))
    for record in snippets:
        sid = str(record.get("source_id", ""))
        try:
            path = local_attachment(workspace, str(record.get("file_path", "")))
            accessible = path.is_file() and sha256_file(path) == record.get("sha256")
        except (ThesisError, OSError):
            accessible = False
        if sid not in sources or not accessible:
            findings.append(QualityFinding("PAT-000", "patchwriting", "REVIEW", sid,
                "Teks pembanding sumber tidak ditemukan, sumber ID salah, atau hash berubah.",
                "Pulihkan sumber dan lakukan pemeriksaan manual sebelum menyimpulkan."))
            continue
        source_text = path.read_text(encoding="utf-8")
        if len(source_text) > 250_000:
            findings.append(QualityFinding("PAT-003", "patchwriting", "INFO", sid,
                "Teks pembanding lebih dari 250.000 karakter; perbandingan dilewati demi keamanan kinerja.",
                "Gunakan kutipan atau bagian sumber yang relevan dan terverifikasi."))
            continue
        for line, paragraph in paragraphs:
            matches = matching_phrases(paragraph, source_text)
            if not matches:
                continue
            findings.append(QualityFinding("PAT-001", "patchwriting", "REVIEW", f"{chapter.name}:baris {line}",
                f"Ada kemiripan berurutan dengan {sid}; belum dapat disimpulkan sebagai plagiarisme.",
                "Periksa kutipan langsung, sitasi, istilah baku, dan kesetiaan parafrase terhadap sumber asli.", matches[0][:160]))
            if len(findings) >= 25:
                return findings
    return findings


def review_state(workspace: Path) -> dict[str, dict[str, Any]]:
    """Mengembalikan review manual terbaru per domain dengan status kesegaran."""
    digest = manuscript_digest(workspace)
    reviews = read_json(workspace / "registry" / "quality_reviews.json", [])
    latest: dict[str, dict[str, Any]] = {}
    for review in reviews:
        latest[review.get("domain", "")] = {**review, "current": review.get("manuscript_sha256") == digest}
    return latest


def quality_audit(workspace: Path) -> dict[str, Any]:
    """Menjalankan pemeriksaan mekanis dan melaporkan item yang belum bisa diverifikasi."""
    findings: list[QualityFinding] = []
    chapters = sorted((workspace / "chapters").glob("bab-[1-5].md"))
    for chapter in chapters:
        findings.extend(readability_findings(chapter))
        findings.extend(patchwriting_findings(workspace, chapter))
    sources = {x["id"]: x for x in read_json(workspace / "registry" / "sources.json", [])}
    citations_by_chapter: set[tuple[int, str]] = set()
    for chapter in chapters:
        number = int(chapter.stem.split("-")[-1])
        for source_id in CITE_RE.findall(read_text(chapter)):
            citations_by_chapter.add((number, source_id))
    citation_reviews = read_json(workspace / "registry" / "citation_reviews.json", [])
    for chapter, sid in sorted(citations_by_chapter):
        if sid not in sources:
            findings.append(QualityFinding("CIV-001", "citation_integrity", "BLOCK", f"Bab {chapter}:{sid}",
                "Sitasi mengacu ke sumber yang tidak terdaftar.", "Registrasikan dan periksa publikasi asli."))
            continue
        matching_by_claim = {
            str(x.get("claim_text", "")): x
            for x in citation_reviews
            if x.get("chapter") == chapter and x.get("source_id") == sid
        }
        matching = list(matching_by_claim.values())
        if not matching:
            findings.append(QualityFinding("CIV-002", "citation_integrity", "REVIEW", f"Bab {chapter}:{sid}",
                "Belum tersedia berita acara pemeriksaan hubungan sumber-klaim.",
                "Baca teks lengkap dan catat klaim, lokasi sumber, kutipan pendukung, serta hasil peninjauan."))
        elif any(x.get("verdict") != "supported" or
                 x.get("manuscript_sha256") != citation_digest(workspace) for x in matching):
            findings.append(QualityFinding("CIV-003", "citation_integrity", "BLOCK", f"Bab {chapter}:{sid}",
                "Terdapat klaim yang ditandai tidak sesuai atau belum pasti.", "Perbaiki klaim atau sitasi dan perbarui catatan review."))
    contributions = read_json(workspace / "registry" / "contributions.json", [])
    supported_contributions = [c for c in contributions if c.get("status") == "supported" and c.get("evidence_ids")]
    if not supported_contributions:
        findings.append(QualityFinding("OCV-001", "original_contribution", "REVIEW", "registry/contributions.json",
            "Belum ada kontribusi peneliti yang didokumentasikan dengan bukti.",
            "Tuliskan apa yang benar-benar dikerjakan, pembandingnya, batasan, dan ID bukti nyata."))
    for item in contributions:
        if not item.get("distinction") or not item.get("limitations"):
            findings.append(QualityFinding("OCV-002", "original_contribution", "REVIEW", item.get("id", ""),
                "Pembeda dengan karya sebelumnya atau keterbatasannya belum dijelaskan.",
                "Jelaskan kontribusi tanpa mengklaim kebaruan yang belum diverifikasi."))
    state = review_state(workspace)
    return {
        "generated_at": timestamp(), "manuscript_sha256": manuscript_digest(workspace),
        "scope": "screening editorial, bukan penetapan AI/plagiarisme atau verifikasi isi publikasi",
        "summary": {"chapters": len(chapters), "findings": len(findings), "sources_with_citation": len(citations_by_chapter), "contributions_supported_declared": len(supported_contributions)},
        "findings": [asdict(f) for f in findings],
        "review_status": {domain: state.get(domain, {"decision": "missing", "current": False}) for domain in REVIEW_DOMAINS},
        "warnings": [
            "Kemiripan token bukan skor Turnitin dan tidak membuktikan patchwriting/plagiarisme.",
            "Keterbacaan dan pola bahasa bukan bukti atau prediksi kepengarangan AI.",
            "Persetujuan review merupakan deklarasi pengguna, bukan verifikasi independen.",
            "Pemeriksaan kesesuaian klaim per sumber memerlukan pembacaan artikel asli secara manual.",
        ],
    }


def save_quality_report(workspace: Path, report: dict[str, Any]) -> Path:
    """Mengarsipkan laporan mutu ke JSON dan Markdown untuk diperiksa editor."""
    target = workspace / "audit"
    target.mkdir(parents=True, exist_ok=True)
    write_json(target / "quality-report.json", report)
    rows = ["# Audit Kualitas Akademik (v5)", "", f"Fingerprint naskah: `{report['manuscript_sha256']}`", "", "## Status review manual", ""]
    for domain, review in report["review_status"].items():
        rows.append(f"- {domain}: {review.get('decision', 'missing')}; cocok dengan naskah kini: {review.get('current', False)}")
    rows += ["", "## Temuan editorial", "", "| ID | Dimensi | Status | Lokasi | Observasi | Tindakan |", "|---|---|---|---|---|---|"]
    for item in report["findings"]:
        vals = [item[k] for k in ("code", "category", "level", "location", "observation", "suggestion")]
        rows.append("| " + " | ".join(str(x).replace("|", "\\|").replace("\n", " ") for x in vals) + " |")
    rows.extend(["", "## Batasan", ""] + [f"- {warning}" for warning in report["warnings"]])
    path = target / "quality-report.md"
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return path

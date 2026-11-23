"""Audit struktural: registry, kontinuitas bab, sumber, bukti, dan gerbang final."""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from storage import ThesisError, local_attachment, read_json, read_text, sha256_file, timestamp, write_json
from academic_quality import REVIEW_DOMAINS, citation_digest, quality_audit, save_quality_report

CITE_PATTERN = re.compile(r"\[cite:(SRC-\d{3,})\]")
CLAIM_PATTERN = re.compile(r"\[claim:(CLM-\d{3,})\]")
PLACEHOLDER_PATTERN = re.compile(r"\[(?:PERLU[^\]]*|BELUM[^\]]*|ISI[^\]]*|TBD|TODO|PLACEHOLDER)\]", re.IGNORECASE)
MANUAL_CITATION_PATTERN = re.compile(r"\([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .,&-]{1,80},\s*(?:19|20)\d{2}[a-z]?\)")


@dataclass(frozen=True)
class Issue:
    """Satu masalah audit yang berisi lokasi, tingkat, dan tindakan."""

    code: str
    severity: str
    location: str
    explanation: str
    action: str


def problem(issues: list[Issue], code: str, severity: str, location: str, explanation: str, action: str) -> None:
    """Menambahkan temuan dengan struktur seragam untuk laporan CLI maupun Markdown."""
    issues.append(Issue(code, severity, location, explanation, action))


def audit_project(workspace: Path, mode: str) -> dict[str, Any]:
    """Memeriksa bukti-bukti struktural dan menyusun laporan, tanpa mengklaim audit semantik."""
    if mode not in {"draft", "review", "final"}:
        raise ThesisError(f"Mode tidak dikenal: {mode}")
    project = read_json(workspace / "project.json")
    sources = read_json(workspace / "registry" / "sources.json", [])
    evidence = read_json(workspace / "registry" / "evidence.json", [])
    claims = read_json(workspace / "registry" / "claims.json", [])
    approvals = read_json(workspace / "registry" / "approvals.json", [])
    issues: list[Issue] = []
    source_map = {str(item.get("id")): item for item in sources}
    evidence_map = {str(item.get("id")): item for item in evidence}
    claim_map = {str(item.get("id")): item for item in claims}
    chapter_texts: dict[int, str] = {}
    citations: set[str] = set()
    claim_tokens: set[str] = set()

    # Identitas dan kontrak penelitian harus berasal dari data yang diberikan pengguna.
    required_project = ("title", "university", "program", "student_name", "student_id", "method", "research_object")
    for field in required_project:
        if not str(project.get(field, "")).strip():
            problem(issues, "PRJ-001", "HIGH", f"project.json:{field}", "Metadata penelitian belum dilengkapi.", "Isi dari data asli peneliti.")
    questions = project.get("research_questions", [])
    objectives = project.get("objectives", [])
    if not isinstance(questions, list) or not questions:
        problem(issues, "PRJ-002", "HIGH", "project.json:research_questions", "Rumusan masalah belum tersedia.", "Masukkan rumusan masalah yang telah disepakati.")
        questions = []
    if not isinstance(objectives, list) or not objectives:
        problem(issues, "PRJ-003", "HIGH", "project.json:objectives", "Tujuan penelitian belum tersedia.", "Masukkan tujuan penelitian yang sesuai dengan masalah.")
        objectives = []
    q_ids = {q.get("id") for q in questions if isinstance(q, dict)}
    o_ids = {o.get("id") for o in objectives if isinstance(o, dict)}
    alignments = project.get("alignment", [])
    for q_id in q_ids:
        if q_id and not any(a.get("question_id") == q_id and a.get("objective_id") in o_ids and str(a.get("method", "")).strip() for a in alignments if isinstance(a, dict)):
            problem(issues, "PRJ-004", "HIGH", "project.json:alignment", f"Tidak ada pemetaan lengkap untuk {q_id}.", "Pasangkan Q → O → metode yang benar.")

    # Keterlacakan naskah setiap bab dan sitasi terstruktur.
    for number in range(1, 6):
        chapter = workspace / "chapters" / f"bab-{number}.md"
        if not chapter.is_file():
            problem(issues, "CHP-001", "HIGH", str(chapter), "Berkas bab tidak ditemukan.", "Buat naskah bab menggunakan template.")
            continue
        body = read_text(chapter)
        chapter_texts[number] = body
        if len(body.strip()) < 180 or not re.search(r"(?m)^#{1,3}\s+", body):
            problem(issues, "CHP-002", "HIGH", chapter.name, "Bab belum mempunyai isi substantif dan heading yang cukup.", "Lengkapi pembahasan dan struktur bab.")
        placeholders = PLACEHOLDER_PATTERN.findall(body)
        if placeholders and mode != "draft":
            problem(issues, "CHP-003", "HIGH", chapter.name, f"Masih ada {len(placeholders)} placeholder, misalnya {placeholders[0]}.", "Ganti hanya dengan fakta terverifikasi atau tetap dalam mode draft.")
        citations.update(CITE_PATTERN.findall(body))
        claim_tokens.update(CLAIM_PATTERN.findall(body))
        manual = MANUAL_CITATION_PATTERN.findall(body)
        if manual:
            problem(issues, "CIT-004", "MEDIUM", chapter.name, "Ditemukan pola sitasi penulis-tahun manual yang tidak dapat dicocokkan otomatis.", "Gunakan token [cite:SRC-001] atau cocokkan secara manual pada audit akademik.")
    for front in ("abstrak-id.md", "abstract-en.md"):
        front_path = workspace / "frontmatter" / front
        if not front_path.is_file() or len(read_text(front_path).strip()) < 100:
            problem(issues, "FRT-001", "HIGH", f"frontmatter/{front}", "Abstrak belum lengkap.", "Tulis abstrak hanya setelah hasil benar-benar tersedia.")
        elif mode != "draft" and PLACEHOLDER_PATTERN.search(read_text(front_path)):
            problem(issues, "FRT-002", "HIGH", f"frontmatter/{front}", "Abstrak masih mengandung placeholder.", "Isi dari hasil penelitian nyata.")

        if front_path.is_file():
            citations.update(CITE_PATTERN.findall(read_text(front_path)))
            claim_tokens.update(CLAIM_PATTERN.findall(read_text(front_path)))

    if not sources:
        problem(issues, "SRC-001", "HIGH", "registry/sources.json", "Belum ada daftar sumber ilmiah.", "Daftarkan sumber yang benar-benar digunakan.")
    if not citations:
        problem(issues, "CIT-001", "HIGH", "chapters/", "Belum ada token sitasi terstruktur.", "Tambahkan [cite:SRC-001] sesuai klaim.")
    for source_id in citations:
        src = source_map.get(source_id)
        if src is None:
            problem(issues, "CIT-002", "CRITICAL", "chapters/", f"Sitasi {source_id} tidak mempunyai metadata sumber.", "Daftarkan sumber asli atau hapus klaim yang tidak didukung.")
            continue
        if not src.get("authors") or not src.get("title") or not src.get("year") or not src.get("venue") or not (src.get("doi") or src.get("url")):
            problem(issues, "SRC-002", "HIGH", f"sources:{source_id}", "Metadata sumber tidak lengkap.", "Periksa penulis, judul, tahun, DOI/URL pada publikasi.")
        if mode != "draft" and (src.get("access_status") != "fulltext_checked" or not src.get("metadata_checked") or not src.get("verification_note")):
            problem(issues, "SRC-003", "HIGH", f"sources:{source_id}", "Teks lengkap/metadata belum ditandai telah diperiksa dengan catatan.", "Baca sumber, cocokkan klaim, dan catat proses pemeriksaan.")
        if src.get("file_path"):
            path = local_attachment(workspace, str(src["file_path"]))
            if not path.is_file() or sha256_file(path) != src.get("sha256"):
                problem(issues, "SRC-004", "CRITICAL", f"sources:{source_id}", "Berkas sumber hilang atau hash berubah.", "Pulihkan berkas asli dan registrasikan ulang secara sah.")

    if not evidence:
        problem(issues, "EVD-001", "HIGH", "registry/evidence.json", "Belum ada bukti penelitian terdaftar.", "Daftarkan data, log, berkas observasi, atau dokumen asli.")
    for item in evidence:
        evidence_id = str(item.get("id"))
        file_path = str(item.get("file_path", ""))
        try:
            path = local_attachment(workspace, file_path)
            if not path.is_file() or sha256_file(path) != item.get("sha256"):
                problem(issues, "EVD-002", "CRITICAL", f"evidence:{evidence_id}", "Bukti hilang atau isi berubah dari hash tercatat.", "Tinjau perubahan, simpan versi asli, lalu registrasikan versi baru.")
        except ThesisError as exc:
            problem(issues, "EVD-003", "CRITICAL", f"evidence:{evidence_id}", str(exc), "Perbaiki lokasi bukti di dalam workspace.")
        if item.get("permission") == "pending":
            problem(issues, "EVD-004", "CRITICAL", f"evidence:{evidence_id}", "Perizinan penggunaan bukti masih menunggu.", "Peroleh izin sebelum memakai data dalam hasil atau naskah publik.")

    result_claims = [x for x in claims if x.get("kind") == "result" and x.get("status") == "supported"]
    if not result_claims:
        problem(issues, "CLM-001", "HIGH", "registry/claims.json", "Belum ada klaim hasil yang didukung bukti.", "Catat hasil uji nyata dan relasikan dengan file bukti.")
    for item in claims:
        claim_id = str(item.get("id"))
        refs = list(item.get("source_ids", []))
        eids = list(item.get("evidence_ids", []))
        if item.get("status") != "supported" and mode != "draft":
            problem(issues, "CLM-002", "HIGH", f"claims:{claim_id}", "Ada klaim yang belum didukung.", "Verifikasi klaim atau hilangkan dari naskah final.")
        if not refs and not eids:
            problem(issues, "CLM-003", "HIGH", f"claims:{claim_id}", "Klaim tidak menautkan sumber atau bukti.", "Tambahkan referensi yang benar atau bukti aktual.")
        for source_id in refs:
            if source_id not in source_map:
                problem(issues, "CLM-004", "CRITICAL", f"claims:{claim_id}", f"Referensi {source_id} tidak ditemukan.", "Perbaiki sumber klaim.")
        for evidence_id in eids:
            if evidence_id not in evidence_map:
                problem(issues, "CLM-005", "CRITICAL", f"claims:{claim_id}", f"Bukti {evidence_id} tidak ditemukan.", "Perbaiki bukti klaim.")
        if item.get("kind") == "result" and not eids:
            problem(issues, "CLM-006", "HIGH", f"claims:{claim_id}", "Klaim hasil tidak ditautkan ke bukti primer.", "Tambahkan log, dataset, atau hasil pengujian yang benar.")
        if item.get("kind") == "conclusion" and not eids:
            problem(issues, "CLM-007", "HIGH", f"claims:{claim_id}", "Kesimpulan belum ditautkan ke bukti hasil.", "Tautkan data/hasil yang mendasari kesimpulan.")
    for claim_id in claim_tokens:
        if claim_id not in claim_map:
            problem(issues, "CLM-008", "HIGH", "chapters/", f"Token {claim_id} tidak memiliki entri registry.", "Daftarkan klaim tersebut.")
    for mapping in alignments:
        if not isinstance(mapping, dict):
            continue
        if mode != "draft" and not mapping.get("result_claim_ids"):
            problem(issues, "PRJ-005", "HIGH", "project.json:alignment", "Ada pertanyaan penelitian yang belum dihubungkan dengan hasil.", "Tautkan hasil nyata yang menjawab pertanyaan.")
        for cid in mapping.get("result_claim_ids", []):
            if cid not in claim_map:
                problem(issues, "PRJ-006", "HIGH", "project.json:alignment", f"Klaim {cid} tidak ada dalam registry.", "Perbaiki pemetaan Q→hasil.")

    # Periksa kualitas akademik secara diagnostik; hanya persyaratan bukti dan
    # review manual terdokumentasi yang bisa memblokir final, bukan skor gaya.
    quality = quality_audit(workspace)
    save_quality_report(workspace, quality)
    if mode == "final":
        for domain in REVIEW_DOMAINS:
            review = quality["review_status"].get(domain, {})
            if review.get("decision") != "approved" or not review.get("current"):
                problem(issues, "QAL-001", "HIGH", f"quality_reviews:{domain}",
                    "Persetujuan editorial belum dicatat, belum disetujui, atau sudah kedaluwarsa setelah revisi.",
                    "Jalankan quality-audit, lakukan peninjauan nyata, lalu catat quality-review-add dengan catatan.")
        if quality["summary"]["contributions_supported_declared"] == 0:
            problem(issues, "QAL-002", "HIGH", "registry/contributions.json",
                "Belum ada kontribusi ilmiah yang dinyatakan didukung bukti nyata.",
                "Daftarkan kontribusi yang benar-benar dikerjakan dan bandingkan dengan studi terdahulu.")
        current_fingerprint = citation_digest(workspace)
        for finding in quality["findings"]:
            if finding["code"] == "CIV-001" or finding["code"] == "CIV-002" or finding["code"] == "CIV-003":
                problem(issues, "QAL-003", "HIGH", finding["location"],
                    finding["observation"], finding["suggestion"])
        citation_reviews = read_json(workspace / "registry" / "citation_reviews.json", [])
        latest_review_per_claim = {
            (x.get("chapter"), x.get("source_id"), x.get("claim_text")): x for x in citation_reviews
        }
        for citation_review in latest_review_per_claim.values():
            if citation_review.get("manuscript_sha256") != current_fingerprint:
                problem(issues, "QAL-004", "HIGH", f"citation-review:{citation_review.get('id')}",
                    "Review kesesuaian klaim terhadap sumber berasal dari versi naskah sebelumnya.",
                    "Periksa ulang klaim sumber setelah perubahan, lalu catat review terbaru.")
        review_path = workspace / "audit" / "manual-review.md"
        review_body = read_text(review_path) if review_path.is_file() else ""
        if not review_body or re.search(r"(?im)^\s*-\s*\[\s\]", review_body) or PLACEHOLDER_PATTERN.search(review_body):
            problem(issues, "FIN-006", "HIGH", "audit/manual-review.md", "Checklist manual belum dinyatakan selesai dan tercatat.", "Lakukan tiap pemeriksaan, lalu isi catatan, pemeriksa, dan tanggal yang sebenarnya.")
        if not project.get("visual_review_confirmed", False):
            problem(issues, "FIN-001", "HIGH", "project.json:visual_review_confirmed", "Audit visual dokumen belum diakui selesai.", "Periksa seluruh halaman hasil review dan catat konfirmasi.")
        for role in ("researcher", "supervisor"):
            matching = [x for x in approvals if x.get("role") == role and x.get("decision") == "approved"]
            if not matching:
                problem(issues, "FIN-002", "CRITICAL", "registry/approvals.json", f"Bukti persetujuan peran '{role}' belum tercatat.", "Catat persetujuan nyata beserta berkas bukti.")
            else:
                for app in matching:
                    try:
                        path = local_attachment(workspace, str(app.get("file_path", "")))
                        if not path.is_file() or sha256_file(path) != app.get("sha256"):
                            problem(issues, "FIN-003", "CRITICAL", f"approval:{role}", "Berkas persetujuan hilang/berubah.", "Periksa keaslian dan registrasikan ulang dokumen yang sah.")
                    except ThesisError as exc:
                        problem(issues, "FIN-004", "CRITICAL", f"approval:{role}", str(exc), "Perbaiki berkas persetujuan.")
        sheet = workspace / "frontmatter" / "lembar-pengesahan.md"
        if not sheet.is_file() or len(read_text(sheet).strip()) < 70 or PLACEHOLDER_PATTERN.search(read_text(sheet)):
            problem(issues, "FIN-005", "HIGH", "frontmatter/lembar-pengesahan.md", "Lembar pengesahan final tidak tersedia/lengkap.", "Gunakan dokumen resmi yang sudah disetujui, tanpa memalsukan tanda tangan.")

    # Tidak menganggap hasil otomatis sebagai pemeriksaan isi 232 aturan atau autentikasi eksternal.
    blocking = [x for x in issues if x.severity in ({"CRITICAL", "HIGH", "MEDIUM"} if mode == "final" else {"CRITICAL", "HIGH"})]
    if mode == "draft":
        status = "DRAFT"
    elif blocking:
        status = "TERHALANG_BUKTI" if any(x.code.startswith(("SRC", "EVD", "CLM", "FIN")) for x in blocking) else "PERLU_REVISI"
    elif mode == "review":
        status = "SIAP_DITINJAU"
    else:
        status = "FINAL_DISETUJUI_SECARA_ADMINISTRATIF"
    return {
        "timestamp": timestamp(), "mode": mode, "status": status, "can_build": mode == "draft" or not blocking,
        "summary": {"sources": len(sources), "evidence": len(evidence), "claims": len(claims), "citations_used": len(citations), "chapters_present": len(chapter_texts), "critical": sum(x.severity == "CRITICAL" for x in issues), "high": sum(x.severity == "HIGH" for x in issues), "medium": sum(x.severity == "MEDIUM" for x in issues)},
        "issues": [asdict(issue) for issue in issues],
        "manual_review_required": ["Periksa kecocokan klaim terhadap teks lengkap jurnal", "Audit EYD V, KBBI, TBBBI dan 232 entri kontrol dengan konteks", "Verifikasi perhitungan dan izin penelitian", "Periksa setiap halaman DOCX/PDF terhadap template kampus", "Periksa kualitas bahasa dengan Human Academic Writing Quality dan Readability Auditor", "Bandingkan paragraf dengan teks sumber jika tersedia, lalu periksa patchwriting secara manual", "Dokumentasikan dan verifikasi kontribusi orisinal peneliti", "Jika ada laporan Turnitin, interpretasikan secara kontekstual tanpa menjadikan skor sebagai vonis", "Validasi autentisitas persetujuan pembimbing (bukan dari hash saja)"],
        "warning": "Audit struktural + petunjuk editorial lokal; tidak membuktikan asal tulisan, kebenaran referensi, atau autentikasi persetujuan.",
    }


def save_report(workspace: Path, report: dict[str, Any]) -> Path:
    """Menyimpan JSON dan Markdown audit agar dapat dikaji atau dibawa ke sesi lain."""
    folder = workspace / "audit"
    folder.mkdir(parents=True, exist_ok=True)
    write_json(folder / "report.json", report)
    lines = [f"# Hasil audit {report['mode']}", "", f"Status: **{report['status']}**", "", f"Boleh ekspor pada mode ini: **{'Ya' if report['can_build'] else 'Tidak'}**", "", "## Temuan", "", "| ID | Tingkat | Lokasi | Masalah | Tindakan |", "|---|---|---|---|---|"]
    for issue in report["issues"]:
        fields = [issue[k] for k in ("code", "severity", "location", "explanation", "action")]
        lines.append("| " + " | ".join(str(x).replace("|", "\\|").replace("\n", " ") for x in fields) + " |")
    lines.extend(["", "## Pemeriksaan manual yang tetap wajib", ""] + [f"- {item}" for item in report["manual_review_required"]] + ["", f"> {report['warning']}", ""])
    path = folder / "report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path

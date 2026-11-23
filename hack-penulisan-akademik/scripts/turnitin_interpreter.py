"""Pembaca data laporan Turnitin yang ditranskripsikan secara manual.

Tidak mengakses layanan Turnitin, tidak menguji naskah, tidak memprediksi skor,
dan tidak menentukan plagiarisme maupun kepengarangan AI.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from storage import ThesisError, read_json, timestamp, write_json

VALID_TYPES = {"similarity", "ai_writing"}
VALID_MATCHES = {"quoted_cited", "paraphrased_cited", "bibliography", "possibly_uncited", "unknown"}


def parse_report_input(data: dict[str, Any]) -> dict[str, Any]:
    """Memvalidasi angka dan asal laporan yang disalin oleh pengguna dari UI Turnitin."""
    if not isinstance(data, dict):
        raise ThesisError("Data laporan harus objek JSON.")
    kind = data.get("report_type")
    score = data.get("score_percent")
    if kind not in VALID_TYPES:
        raise ThesisError("report_type harus similarity atau ai_writing.")
    if isinstance(score, bool) or not isinstance(score, (float, int)) or not 0 <= score <= 100:
        raise ThesisError("score_percent harus angka 0–100 yang disalin dari laporan sebenarnya.")
    for key in ("report_date", "document_title", "transcribed_by", "language"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ThesisError(f"Field {key} wajib diisi agar konteks laporan dapat ditelusuri.")
    if data.get("source") != "user_supplied_report":
        raise ThesisError("source harus user_supplied_report. Laporan sintetis tidak dapat disamarkan sebagai hasil nyata.")
    matches = data.get("matches", [])
    if not isinstance(matches, list):
        raise ThesisError("matches harus berupa daftar.")
    for match in matches:
        if not isinstance(match, dict) or match.get("category") not in VALID_MATCHES:
            raise ThesisError("Kategori match tidak dikenal.")
        if not str(match.get("location", "")).strip():
            raise ThesisError("Setiap match memerlukan lokasi naskah.")
    return data


def interpret_report(workspace: Path, report: dict[str, Any]) -> dict[str, Any]:
    """Memberi konteks dari skor nyata tanpa menyimpulkan pelanggaran atau kelulusan."""
    data = parse_report_input(report)
    kind = data["report_type"]
    recommendations: list[str] = []
    if kind == "similarity":
        recommendations += [
            "Periksa setiap kecocokan pada teks sumber serta konteks naskah, bukan persentase total saja.",
            "Bedakan kutipan yang diberi atribusi, daftar pustaka, istilah baku, dan bagian yang mungkin tidak disitasi.",
            "Periksa apakah pengecualian kutipan/daftar pustaka berlaku pada laporan resmi yang dilihat pembimbing.",
            "Kemiripan tinggi tidak otomatis plagiarisme; kemiripan rendah tidak membuktikan seluruh sumber benar.",
        ]
    else:
        recommendations += [
            "Skor AI Writing merupakan keluaran probabilistik alat, bukan bukti pasti kepengarangan.",
            "Pastikan bahasa dan jenis dokumen memenuhi dukungan/ketentuan model Turnitin yang digunakan.",
            "Telaah bukti proses penulisan, draf, catatan riset, revisi, dan kebijakan institusi; jangan merekayasa tulisan untuk menurunkan skor.",
        ]
        if data["language"].casefold() in {"id", "id-id", "indonesia", "bahasa indonesia", "indonesian"}:
            recommendations.append("Bahasa Indonesia tidak tercantum dalam daftar bahasa yang didukung pada panduan persyaratan AI Writing Report Turnitin yang diperiksa 23 November 2026; cocokkan ulang jenis laporan/produk, bahasa naskah dan angka dari dokumen asli.")
    items = data.get("matches", [])
    if kind == "similarity":
        for match in items:
            if match.get("category") in {"possibly_uncited", "unknown"}:
                recommendations.append(f"Tinjau manual bagian {match.get('location')}: kecocokan belum dapat dipastikan status atribusinya.")
    path = workspace / "audit"
    path.mkdir(parents=True, exist_ok=True)
    interpretation = {
        "created_at": timestamp(), "type": kind,
        "reported_score_percent": data["score_percent"], "report_date": data["report_date"],
        "document_title": data["document_title"], "language": data["language"],
        "provenance": "ditranskripsikan pengguna; belum diverifikasi independen oleh Turnitin",
        "context": data.get("notes", ""), "matches": items,
        "recommendations": recommendations,
        "conclusion": "Tidak ada penetapan 'lolos', plagiarisme, atau penulisan AI berdasarkan skor.",
        "official_guides": [
            "https://guides.turnitin.com/hc/en-us/articles/23435833938701-Understanding-the-similarity-score",
            "https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report",
            "https://guides.turnitin.com/hc/en-us/articles/28234943089933-File-requirements-for-an-AI-Writing-Report",
        ],
    }
    write_json(path / "turnitin-interpretation.json", interpretation)
    lines = ["# Interpretasi laporan Turnitin", "", f"Jenis: **{kind}**", f"Skor yang dicatat pengguna: **{data['score_percent']}%**", f"Bahasa naskah: {data['language']}", f"Tanggal laporan: {data['report_date']}", "", "> Data ini belum dibandingkan secara independen dengan dokumen asli Turnitin.", "", "## Tindak lanjut", ""]
    lines.extend(f"- {x}" for x in recommendations)
    lines += ["", f"**Kesimpulan:** {interpretation['conclusion']}", ""]
    (path / "turnitin-interpretation.md").write_text("\n".join(lines), encoding="utf-8")
    return interpretation

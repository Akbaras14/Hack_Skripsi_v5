#!/usr/bin/env python3
"""CLI lokal Hack Skripsi v5.0: penulisan, sumber, bukti, mutu akademik, dan ekspor."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

from audit import audit_project, save_report
from academic_quality import REVIEW_DOMAINS, manuscript_digest, citation_digest, quality_audit, save_quality_report
from turnitin_interpreter import interpret_report
from exporter import build_documents
from storage import ThesisError, append_decision, import_attachment, next_id, read_json, timestamp, write_json

ROOT = Path(__file__).resolve().parent.parent
PHASES = ("INIT", "DESIGN", "LITERATURE", "PROPOSAL", "DATA", "ANALYSIS", "CHAPTERS", "AUDIT", "REVIEW", "APPROVAL", "FINAL")
PHASE_AGENTS = {"INIT": "Research", "DESIGN": "Research", "LITERATURE": "Research", "PROPOSAL": "Writing", "DATA": "Research", "ANALYSIS": "Research", "CHAPTERS": "Writing", "AUDIT": "Audit", "REVIEW": "Audit", "APPROVAL": "Audit", "FINAL": "Audit"}


def workspace_path(raw: str) -> Path:
    """Memastikan workspace tersedia untuk perintah selain init."""
    target = Path(raw).expanduser().resolve()
    if not (target / "project.json").is_file():
        raise ThesisError(f"Workspace tidak ditemukan/belum diinisialisasi: {target}")
    return target


def init_workspace(args: argparse.Namespace) -> None:
    """Membuat ruang kerja yang memiliki template dan registry kosong tanpa data rekaan."""
    workspace = Path(args.workspace).expanduser().resolve()
    if (workspace / "project.json").exists():
        raise ThesisError("Workspace sudah diinisialisasi; init tidak boleh menimpa data.")
    workspace.mkdir(parents=True, exist_ok=True)
    for section in ("chapters", "frontmatter", "registry", "attachments", "logs", "audit", "output", "appendices"):
        (workspace / section).mkdir(exist_ok=True)
    for index in range(1, 6):
        shutil.copy2(ROOT / "templates" / f"bab-{index}.md", workspace / "chapters" / f"bab-{index}.md")
    for file in ("abstrak-id.md", "abstract-en.md", "lembar-pengesahan.md"):
        shutil.copy2(ROOT / "templates" / file, workspace / "frontmatter" / file)
    for name in ("sources", "evidence", "claims", "approvals", "source_texts", "citation_reviews", "contributions", "quality_reviews"):
        write_json(workspace / "registry" / f"{name}.json", [])
    config = {
        "title": args.title, "university": "", "program": "", "student_name": "", "student_id": "", "year": None,
        "method": "", "research_object": "", "research_questions": [], "objectives": [], "alignment": [],
        "citation_style": "APA7", "visual_review_confirmed": False,
        "formatting": {"font": "Times New Roman", "font_size_pt": 12, "line_spacing": 1.5, "margin_left_cm": 4, "margin_right_cm": 3, "margin_top_cm": 3.5, "margin_bottom_cm": 3},
        "formatting_warning": "Nilai contoh bukan template resmi universitas; sesuaikan sebelum submit.",
    }
    write_json(workspace / "project.json", config)
    write_json(workspace / "state.json", {"created_at": timestamp(), "phase": "INIT", "status": "DRAFT", "last_checked": None})
    (workspace / "audit" / "manual-review.md").write_text((ROOT / "templates" / "manual-review.md").read_text(encoding="utf-8"), encoding="utf-8")
    append_decision(workspace, "Workspace dibuat; data, hasil, dan persetujuan belum diisi.", "system")
    print(f"Workspace dibuat: {workspace}")


def registry_add(workspace: Path, registry: str, payload: dict[str, Any], prefix: str) -> str:
    """Menambahkan record unik tanpa mengubah ID record yang telah ada."""
    filename = workspace / "registry" / f"{registry}.json"
    items: list[dict[str, Any]] = read_json(filename, [])
    identity = next_id(items, prefix)
    payload = {"id": identity, "created_at": timestamp(), **payload}
    items.append(payload)
    write_json(filename, items)
    return identity


def add_source(args: argparse.Namespace) -> None:
    """Mencatat bibliografi; flag telah dibaca merupakan deklarasi peneliti, bukan verifikasi jaringan."""
    workspace = workspace_path(args.workspace)
    if args.year < 1500 or args.year > 2200 or not (args.doi or args.url):
        raise ThesisError("Tahun tidak valid atau DOI/URL kosong.")
    if args.access_status == "fulltext_checked" and not args.verification_note:
        raise ThesisError("Status fulltext_checked wajib disertai --verification-note.")
    items = read_json(workspace / "registry" / "sources.json", [])
    source_id = next_id(items, "SRC")
    file_path = None
    sha256 = None
    if args.file:
        file_path, sha256 = import_attachment(workspace, Path(args.file).expanduser().resolve(), "sources", source_id)
    payload = {"id": source_id, "created_at": timestamp(), "title": args.title, "authors": args.author, "year": args.year, "venue": args.venue,
               "doi": args.doi, "url": args.url, "access_status": args.access_status, "metadata_checked": args.metadata_checked,
               "verification_note": args.verification_note, "file_path": file_path, "sha256": sha256}
    items.append(payload)
    write_json(workspace / "registry" / "sources.json", items)
    print(f"Sumber terdaftar: {source_id}. Validasi metadata eksternal tetap menjadi kewajiban peneliti.")


def add_evidence(args: argparse.Namespace) -> None:
    """Mengimpor bukti lokal, menyimpan metadata izin dan checksum."""
    workspace = workspace_path(args.workspace)
    items = read_json(workspace / "registry" / "evidence.json", [])
    item_id = next_id(items, "EVD")
    file_path, digest = import_attachment(workspace, Path(args.file).expanduser().resolve(), "evidence", item_id)
    items.append({"id": item_id, "created_at": timestamp(), "kind": args.kind, "description": args.description, "file_path": file_path,
                  "sha256": digest, "permission": args.permission, "sensitivity": args.sensitivity, "provenance": args.provenance})
    write_json(workspace / "registry" / "evidence.json", items)
    print(f"Bukti tersimpan: {item_id} (SHA-256={digest[:14]}…)")


def add_claim(args: argparse.Namespace) -> None:
    """Menyimpan klaim/hasil dengan relasi eksplisit ke sumber dan/atau bukti."""
    workspace = workspace_path(args.workspace)
    source_ids = set(x["id"] for x in read_json(workspace / "registry" / "sources.json", []))
    evidence_ids = set(x["id"] for x in read_json(workspace / "registry" / "evidence.json", []))
    for value in args.source:
        if value not in source_ids:
            raise ThesisError(f"Sumber klaim tidak ditemukan: {value}")
    for value in args.evidence:
        if value not in evidence_ids:
            raise ThesisError(f"Bukti klaim tidak ditemukan: {value}")
    if args.status == "supported" and not (args.source or args.evidence):
        raise ThesisError("Klaim didukung harus memiliki rujukan sumber atau bukti.")
    item_id = registry_add(workspace, "claims", {"chapter": args.chapter, "kind": args.kind, "statement": args.statement, "status": args.status,
                                                 "source_ids": args.source, "evidence_ids": args.evidence}, "CLM")
    print(f"Klaim terdaftar: {item_id}")


def add_approval(args: argparse.Namespace) -> None:
    """Merekam deklarasi persetujuan dengan berkas, tanpa mengautentikasi penandatangan."""
    workspace = workspace_path(args.workspace)
    items = read_json(workspace / "registry" / "approvals.json", [])
    approval_id = next_id(items, "APR")
    path, digest = import_attachment(workspace, Path(args.file).expanduser().resolve(), "approvals", approval_id)
    items.append({"id": approval_id, "created_at": timestamp(), "role": args.role, "decision": args.decision,
                  "file_path": path, "sha256": digest, "note": args.note, "authenticity": "user-declared; not cryptographically verified"})
    write_json(workspace / "registry" / "approvals.json", items)
    print(f"Catatan persetujuan terdaftar: {approval_id}. Keaslian dan kewenangan penanda tangan wajib diperiksa manual.")


def add_source_text(args: argparse.Namespace) -> None:
    """Mendaftarkan teks sumber milik pengguna untuk mendeteksi overlap frasa lokal."""
    workspace = workspace_path(args.workspace)
    sources = {item["id"] for item in read_json(workspace / "registry" / "sources.json", [])}
    if args.source not in sources:
        raise ThesisError("Sumber belum terdaftar; lakukan source-add terlebih dahulu.")
    file = Path(args.file).expanduser().resolve()
    if file.suffix.lower() not in {".txt", ".md"}:
        raise ThesisError("Hanya teks .txt/.md yang diterima; jangan gunakan PDF hasil OCR sembarangan.")
    if file.stat().st_size > 600_000:
        raise ThesisError("Berkas teks terlalu besar; gunakan kutipan relevan hingga 600 KB.")
    file.read_text(encoding="utf-8")
    items = read_json(workspace / "registry" / "source_texts.json", [])
    ident = next_id(items, "TXT")
    file_path, digest = import_attachment(workspace, file, "source_texts", ident)
    items.append({"id": ident, "source_id": args.source, "file_path": file_path,
                  "sha256": digest, "description": args.note, "created_at": timestamp()})
    write_json(workspace / "registry" / "source_texts.json", items)
    print(f"Teks sumber tersimpan: {ident}; evaluasi kemiripan tetap kontekstual.")


def add_citation_review(args: argparse.Namespace) -> None:
    """Merekam pemeriksaan manual kecocokan klaim dan sumber beserta lokasi kutipannya."""
    workspace = workspace_path(args.workspace)
    sources = {item["id"] for item in read_json(workspace / "registry" / "sources.json", [])}
    if args.source not in sources:
        raise ThesisError("Sumber sitasi tidak terdaftar.")
    if not args.reviewer.strip() or not args.locator.strip() or not args.claim_text.strip():
        raise ThesisError("Perlu reviewer, lokasi dalam sumber, dan klaim yang diuji.")
    ident = registry_add(workspace, "citation_reviews", {
        "chapter": args.chapter, "source_id": args.source, "claim_text": args.claim_text,
        "source_locator": args.locator, "source_excerpt": args.excerpt, "verdict": args.verdict,
        "reviewer": args.reviewer, "note": args.note,
        "manuscript_sha256": citation_digest(workspace),
        "attestation": "manual_user_declaration_not_independently_verified",
    }, "CRV")
    print(f"Review sitasi dicatat: {ident}; isi sumber tetap perlu diperiksa oleh peneliti.")


def add_contribution(args: argparse.Namespace) -> None:
    """Merekam kontribusi penelitian yang dapat ditautkan ke pertanyaan dan bukti nyata."""
    workspace = workspace_path(args.workspace)
    evidence_ids = {x["id"] for x in read_json(workspace / "registry" / "evidence.json", [])}
    question_ids = {x.get("id") for x in read_json(workspace / "project.json").get("research_questions", [])}
    if args.question not in question_ids:
        raise ThesisError("ID rumusan masalah tidak ada dalam project.json.")
    if any(e not in evidence_ids for e in args.evidence):
        raise ThesisError("Ada ID bukti kontribusi yang tidak terdaftar.")
    if args.status == "supported" and not args.evidence:
        raise ThesisError("Kontribusi didukung wajib menautkan bukti yang terdaftar.")
    ident = registry_add(workspace, "contributions", {
        "kind": args.kind, "statement": args.statement, "question_id": args.question,
        "distinction": args.distinction, "limitations": args.limitations,
        "evidence_ids": args.evidence, "status": args.status, "reviewer": args.reviewer,
        "note": args.note, "attestation": "declared_by_user_not_peer_reviewed",
    }, "CON")
    print(f"Kontribusi tercatat: {ident}; klaim kebaruan tetap perlu pembanding literatur.")


def add_quality_review(args: argparse.Namespace) -> None:
    """Merekam pemeriksaan editorial per domain yang mengikat versi naskah tertentu."""
    workspace = workspace_path(args.workspace)
    if not args.reviewer.strip() or not args.note.strip():
        raise ThesisError("Review manual memerlukan nama pemeriksa dan catatan substantif.")
    ident = registry_add(workspace, "quality_reviews", {
        "domain": args.domain, "decision": args.decision,
        "reviewer": args.reviewer, "note": args.note,
        "manuscript_sha256": manuscript_digest(workspace),
        "attestation": "manual_declaration_not_independent_assessment",
    }, "REV")
    print(f"Review editorial {ident} dicatat untuk fingerprint naskah saat ini.")


def quality_audit_command(args: argparse.Namespace) -> None:
    """Menghasilkan laporan kualitas diagnostik tanpa mengubah teks pengguna."""
    workspace = workspace_path(args.workspace)
    report = quality_audit(workspace)
    path = save_quality_report(workspace, report)
    print(f"Quality audit: {len(report['findings'])} temuan editorial; {path}")


def turnitin_interpret_command(args: argparse.Namespace) -> None:
    """Menafsirkan input JSON yang disalin pengguna dari laporan aktual."""
    workspace = workspace_path(args.workspace)
    raw = Path(args.file).expanduser().resolve()
    if not raw.is_file():
        raise ThesisError("File data laporan Turnitin tidak ditemukan.")
    data = json.loads(raw.read_text(encoding="utf-8"))
    result = interpret_report(workspace, data)
    print(f"Interpretasi tersimpan: audit/turnitin-interpretation.md ({result['type']}, {result['reported_score_percent']}%).")
    print("Tidak menyimpulkan lolos, pelanggaran, atau kepengarangan AI.")


def decision_add(args: argparse.Namespace) -> None:
    """Mencatat keputusan atau perubahan metodologi agar dapat dipulihkan antarsesi."""
    workspace = workspace_path(args.workspace)
    append_decision(workspace, args.note, args.actor)
    print("Keputusan dicatat pada logs/decisions.jsonl")


def perform_check(workspace: Path, mode: str) -> dict[str, Any]:
    """Menjalankan audit dan memperbarui status operasional workspace."""
    report = audit_project(workspace, mode)
    save_report(workspace, report)
    state = read_json(workspace / "state.json", {})
    state["status"] = report["status"]
    state["last_checked"] = timestamp()
    write_json(workspace / "state.json", state)
    print(f"Audit: {report['status']} | critical={report['summary']['critical']} high={report['summary']['high']} medium={report['summary']['medium']}")
    print(f"Laporan: {workspace / 'audit' / 'report.md'}")
    return report


def check_command(args: argparse.Namespace) -> None:
    """Meminta status audit dalam mode draft/review/final."""
    report = perform_check(workspace_path(args.workspace), args.mode)
    if not report["can_build"]:
        raise ThesisError("Gerbang " + args.mode + " belum lolos. Lihat audit/report.md")


def build_command(args: argparse.Namespace) -> None:
    """Menghasilkan DOCX/PDF hanya bila gerbang mode yang dipilih mengizinkan."""
    workspace = workspace_path(args.workspace)
    report = perform_check(workspace, args.mode)
    if not report["can_build"]:
        raise ThesisError("Ekspor ditolak: gerbang " + args.mode + " belum terpenuhi.")
    manifest = build_documents(workspace, args.mode, docx_only=args.docx_only)
    print("Dokumen diekspor (periksa tampilan tiap halaman):")
    for file in manifest["files"]:
        print(" - " + str(workspace / file["path"]))


def status_command(args: argparse.Namespace) -> None:
    """Menampilkan ringkasan fase dan jumlah item tanpa mengubah workspace."""
    workspace = workspace_path(args.workspace)
    state = read_json(workspace / "state.json")
    counts = {name: len(read_json(workspace / "registry" / f"{name}.json", [])) for name in ("sources", "evidence", "claims", "approvals", "source_texts", "citation_reviews", "contributions", "quality_reviews")}
    print(json.dumps({"workspace": str(workspace), "state": state, "counts": counts}, ensure_ascii=False, indent=2))


def advance_command(args: argparse.Namespace) -> None:
    """Memindahkan satu fase setelah prasyarat deterministik tercapai, atau kembali untuk revisi."""
    workspace = workspace_path(args.workspace)
    state = read_json(workspace / "state.json")
    current = str(state.get("phase", "INIT"))
    destination = args.to
    if current not in PHASES:
        raise ThesisError(f"Fase saat ini tidak dikenal: {current}")
    if PHASES.index(destination) > PHASES.index(current) + 1:
        raise ThesisError("Tidak boleh melompat beberapa fase. Lengkapi tahap secara berurutan.")
    project = read_json(workspace / "project.json")
    sources = read_json(workspace / "registry" / "sources.json", [])
    evidence = read_json(workspace / "registry" / "evidence.json", [])
    claims = read_json(workspace / "registry" / "claims.json", [])
    if PHASES.index(destination) > PHASES.index(current):
        if destination == "DESIGN" and not project.get("title"):
            raise ThesisError("Judul harus ditetapkan sebelum fase DESIGN.")
        if destination == "LITERATURE" and (not project.get("research_questions") or not project.get("objectives") or not project.get("alignment") or not project.get("method")):
            raise ThesisError("Pertanyaan, tujuan, metode dan alignment wajib sebelum fase LITERATURE.")
        if destination == "PROPOSAL" and not sources:
            raise ThesisError("Registri sumber belum diisi untuk proposal.")
        if destination == "DATA":
            from audit import PLACEHOLDER_PATTERN
            for number in (1, 2, 3):
                chapter = workspace / "chapters" / f"bab-{number}.md"
                if PLACEHOLDER_PATTERN.search(chapter.read_text(encoding="utf-8")):
                    raise ThesisError(f"Bab {number} masih memiliki placeholder; proposal belum selesai.")
        if destination == "ANALYSIS" and (not evidence or any(item.get("permission") == "pending" for item in evidence)):
            raise ThesisError("Bukti dan hak penggunaan belum siap untuk analisis.")
        if destination == "CHAPTERS" and not any(item.get("kind") == "result" and item.get("status") == "supported" and item.get("evidence_ids") for item in claims):
            raise ThesisError("Hasil penelitian yang didukung bukti belum didaftarkan.")
        if destination in {"AUDIT", "REVIEW", "APPROVAL"} and not audit_project(workspace, "review")["can_build"]:
            raise ThesisError("Gerbang review belum terpenuhi; selesaikan audit sebelum maju.")
        if destination == "FINAL" and not audit_project(workspace, "final")["can_build"]:
            raise ThesisError("Gerbang final belum terpenuhi; tidak dapat menaikkan status fase.")
    state["phase"] = destination
    state["updated_at"] = timestamp()
    write_json(workspace / "state.json", state)
    append_decision(workspace, f"Fase {current} → {destination}: {args.note}", args.actor)
    print(f"Fase sekarang: {destination} (agen berikutnya: {PHASE_AGENTS[destination]})")


def handoff_command(args: argparse.Namespace) -> None:
    """Menyimpan ringkasan konteks agar agen AI dapat melanjutkan tanpa API atau tebakan."""
    workspace = workspace_path(args.workspace)
    project = read_json(workspace / "project.json")
    state = read_json(workspace / "state.json")
    phase = str(state.get("phase", "INIT"))
    if phase not in PHASE_AGENTS:
        raise ThesisError(f"Fase tidak dikenal: {phase}")
    counts = {name: len(read_json(workspace / "registry" / f"{name}.json", [])) for name in ("sources", "evidence", "claims", "approvals", "source_texts", "citation_reviews", "contributions", "quality_reviews")}
    report = audit_project(workspace, "review")
    missing = [f"- {issue['code']}: {issue['explanation']} ({issue['location']})" for issue in report["issues"] if issue["severity"] in {"CRITICAL", "HIGH"}]
    agent = PHASE_AGENTS[phase]
    lines = ["# Handoff Hack Skripsi — melanjutkan penelitian", "", f"Fase: **{phase}**", f"Peran berikutnya: **{agent} Agent**", f"Judul: **{project.get('title') or '[BELUM DIISI]'}**", f"Metode: **{project.get('method') or '[BELUM DIISI]'}**", f"Objek: **{project.get('research_object') or '[BELUM DIISI]'}**", "", "## Status registri", ""]
    lines += [f"- {name}: {count}" for name, count in counts.items()]
    lines += ["", "## Hambatan struktural saat ini", ""] + (missing or ["- Tidak ada isu tingkat tinggi; lakukan audit substansi manual."])
    lines += ["", "## Instruksi agen", "", f"Jalankan peran {agent} berdasarkan `agents/{agent.lower()}-agent.md`, `orchestration/workflow.md`, dan seluruh aturan mutu relevan. Gunakan isi berkas aktual dalam workspace, jangan menebak atau membuat data, sumber, hasil, tanda tangan, atau izin. Tulis perubahan substantif ke bab/registry sesuai kebutuhan dan catat keputusan melalui `decision-add`.", "", "## Langkah berikutnya", "", "Setelah menyelesaikan tugas fase, jalankan `check --mode review`. Jika belum lengkap, lanjutkan draf dengan status transparan.", ""]
    output = workspace / "audit" / "handoff.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Handoff dibuat: {output}")


def make_parser() -> argparse.ArgumentParser:
    """Mendeklarasikan antarmuka perintah yang dapat digunakan tanpa API AI."""
    parser = argparse.ArgumentParser(description="Hack Skripsi v5.0 — Orkestrator dan audit akademik lokal")
    actions = parser.add_subparsers(dest="command", required=True)
    init = actions.add_parser("init", help="Buat workspace baru dengan template bab")
    init.add_argument("--workspace", required=True)
    init.add_argument("--title", required=True)
    init.set_defaults(handler=init_workspace)
    source = actions.add_parser("source-add", help="Registrasi referensi ilmiah")
    source.add_argument("--workspace", required=True)
    source.add_argument("--title", required=True)
    source.add_argument("--author", action="append", required=True, help="Boleh diulang menurut urutan penulis")
    source.add_argument("--year", required=True, type=int)
    source.add_argument("--venue", default="")
    source.add_argument("--doi", default="")
    source.add_argument("--url", default="")
    source.add_argument("--file", help="File sumber asli opsional")
    source.add_argument("--access-status", choices=["not_accessed", "abstract_checked", "fulltext_checked"], default="not_accessed")
    source.add_argument("--metadata-checked", action="store_true", help="Hanya jika metadata benar-benar diperiksa")
    source.add_argument("--verification-note", default="")
    source.set_defaults(handler=add_source)
    evidence = actions.add_parser("evidence-add", help="Registrasi file data/bukti beserta checksum")
    evidence.add_argument("--workspace", required=True)
    evidence.add_argument("--file", required=True)
    evidence.add_argument("--kind", choices=["dataset", "document", "experiment", "interview", "observation", "code", "analysis"], required=True)
    evidence.add_argument("--permission", choices=["authorized", "not_required", "pending"], default="pending")
    evidence.add_argument("--sensitivity", choices=["public", "internal", "restricted"], default="internal")
    evidence.add_argument("--description", required=True)
    evidence.add_argument("--provenance", default="")
    evidence.set_defaults(handler=add_evidence)
    claim = actions.add_parser("claim-add", help="Kaitkan klaim dengan sumber dan bukti")
    claim.add_argument("--workspace", required=True)
    claim.add_argument("--chapter", type=int, choices=range(1, 6), required=True)
    claim.add_argument("--kind", choices=["background", "method", "result", "conclusion"], required=True)
    claim.add_argument("--statement", required=True)
    claim.add_argument("--status", choices=["draft", "needs_verification", "supported"], default="draft")
    claim.add_argument("--source", action="append", default=[])
    claim.add_argument("--evidence", action="append", default=[])
    claim.set_defaults(handler=add_claim)
    approval = actions.add_parser("approval-add", help="Catat bukti persetujuan nyata")
    approval.add_argument("--workspace", required=True)
    approval.add_argument("--role", choices=["researcher", "supervisor"], required=True)
    approval.add_argument("--decision", choices=["approved", "rejected", "revision_required"], required=True)
    approval.add_argument("--file", required=True)
    approval.add_argument("--note", default="")
    approval.set_defaults(handler=add_approval)
    decision = actions.add_parser("decision-add", help="Catat keputusan dan revisi")
    decision.add_argument("--workspace", required=True)
    decision.add_argument("--note", required=True)
    decision.add_argument("--actor", default="researcher")
    decision.set_defaults(handler=decision_add)
    for command, callback in (("check", check_command), ("build", build_command)):
        child = actions.add_parser(command, help="Periksa gerbang" if command == "check" else "Ekspor Word/PDF")
        child.add_argument("--workspace", required=True)
        child.add_argument("--mode", choices=["draft", "review", "final"], default="draft")
        if command == "build":
            child.add_argument("--docx-only", action="store_true")
        child.set_defaults(handler=callback)
    phase = actions.add_parser("advance", help="Pindah satu fase dengan pemeriksaan prasyarat")
    phase.add_argument("--workspace", required=True)
    phase.add_argument("--to", choices=PHASES, required=True)
    phase.add_argument("--note", required=True)
    phase.add_argument("--actor", default="researcher")
    phase.set_defaults(handler=advance_command)
    handoff = actions.add_parser("handoff", help="Buat ringkasan untuk sesi AI/agen berikutnya")
    handoff.add_argument("--workspace", required=True)
    handoff.set_defaults(handler=handoff_command)
    status = actions.add_parser("status", help="Ringkasan workspace")
    status.add_argument("--workspace", required=True)
    status.set_defaults(handler=status_command)
    source_text = actions.add_parser("source-text-add", help="Daftarkan teks sumber lokal untuk review patchwriting")
    source_text.add_argument("--workspace", required=True)
    source_text.add_argument("--source", required=True)
    source_text.add_argument("--file", required=True)
    source_text.add_argument("--note", default="")
    source_text.set_defaults(handler=add_source_text)
    citation_review = actions.add_parser("citation-review-add", help="Catat pemeriksaan manual klaim dan teks sumber")
    citation_review.add_argument("--workspace", required=True)
    citation_review.add_argument("--chapter", type=int, choices=range(1, 6), required=True)
    citation_review.add_argument("--source", required=True)
    citation_review.add_argument("--claim-text", required=True)
    citation_review.add_argument("--locator", required=True, help="Halaman/bagian sumber yang sudah dibaca")
    citation_review.add_argument("--excerpt", default="", help="Kutipan pendek untuk audit internal")
    citation_review.add_argument("--verdict", choices=["supported", "contradicted", "uncertain"], required=True)
    citation_review.add_argument("--reviewer", required=True)
    citation_review.add_argument("--note", default="")
    citation_review.set_defaults(handler=add_citation_review)
    contribution = actions.add_parser("contribution-add", help="Catat kontribusi ilmiah dan bukti terkait")
    contribution.add_argument("--workspace", required=True)
    contribution.add_argument("--kind", choices=["empirical", "methodological", "artifact", "analysis", "replication"], required=True)
    contribution.add_argument("--statement", required=True)
    contribution.add_argument("--question", required=True)
    contribution.add_argument("--distinction", required=True)
    contribution.add_argument("--limitations", required=True)
    contribution.add_argument("--evidence", action="append", default=[])
    contribution.add_argument("--status", choices=["draft", "needs_verification", "supported"], default="draft")
    contribution.add_argument("--reviewer", required=True)
    contribution.add_argument("--note", default="")
    contribution.set_defaults(handler=add_contribution)
    quality_review = actions.add_parser("quality-review-add", help="Berita acara peninjauan akademik manual, mengikat fingerprint")
    quality_review.add_argument("--workspace", required=True)
    quality_review.add_argument("--domain", choices=REVIEW_DOMAINS, required=True)
    quality_review.add_argument("--decision", choices=["approved", "needs_revision"], required=True)
    quality_review.add_argument("--reviewer", required=True)
    quality_review.add_argument("--note", required=True)
    quality_review.set_defaults(handler=add_quality_review)
    quality = actions.add_parser("quality-audit", help="Jalankan diagnostik keterbacaan, sitasi, patchwriting dan kontribusi")
    quality.add_argument("--workspace", required=True)
    quality.set_defaults(handler=quality_audit_command)
    turnitin = actions.add_parser("turnitin-interpret", help="Baca JSON transkripsi laporan Turnitin yang disediakan pengguna")
    turnitin.add_argument("--workspace", required=True)
    turnitin.add_argument("--file", required=True)
    turnitin.set_defaults(handler=turnitin_interpret_command)
    return parser


def main() -> int:
    """Memproses perintah dan mengembalikan kode kegagalan agar mudah diuji di CI."""
    parser = make_parser()
    args = parser.parse_args()
    try:
        args.handler(args)
    except ThesisError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"ERROR: input/berkas tidak valid: {exc}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

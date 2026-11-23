"""Uji regresi CLI dan batas final dengan dataset demonstrasi sintetis."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMAND = [sys.executable, str(ROOT / "scripts" / "thesis.py")]


class ThesisCliTests(unittest.TestCase):
    """Memastikan mesin menolak final tanpa bukti dan dapat mengekspor draf."""

    def setUp(self) -> None:
        """Membuat workspace temporer yang aman dari data asli."""
        self.temporary = tempfile.TemporaryDirectory(prefix="hackskripsi-test-")
        self.root = Path(self.temporary.name)
        self.workspace = self.root / "skripsi-contoh"
        self.call("init", "--title", "ILUSTRASI PENELITIAN SINTETIS")

    def tearDown(self) -> None:
        """Membersihkan seluruh artefak uji."""
        self.temporary.cleanup()

    def call(self, command: str, *arguments: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        """Menjalankan CLI sebagai proses nyata dan memeriksa status eksekusinya."""
        result = subprocess.run(COMMAND + [command, "--workspace", str(self.workspace), *arguments], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, expected, msg=result.stdout + "\n" + result.stderr)
        return result

    def test_init_templates_and_registry(self) -> None:
        """Workspace baru harus memiliki lima bab dan registri kosong."""
        self.assertEqual(len(list((self.workspace / "chapters").glob("bab-*.md"))), 5)
        self.assertEqual(json.loads((self.workspace / "registry" / "sources.json").read_text()), [])

    def test_final_rejected_when_missing_evidence(self) -> None:
        """Finalisasi harus ditolak saat bukti, sumber dan persetujuan tidak ada."""
        self.call("check", "--mode", "final", expected=2)
        report = json.loads((self.workspace / "audit" / "report.json").read_text())
        self.assertIn(report["status"], ["TERHALANG_BUKTI", "PERLU_REVISI"])
        self.assertFalse(report["can_build"])
        self.assertTrue(any(item["code"] == "FIN-002" for item in report["issues"]))
        self.call("build", "--mode", "final", expected=2)
        self.assertFalse((self.workspace / "output" / "skripsi-final.docx").exists())

    def test_provenance_hash_and_citation(self) -> None:
        """Sitasi dan data uji harus ditautkan ke ID yang dapat ditemukan."""
        source_pdf = self.root / "bacaan-ilustrasi.txt"
        source_pdf.write_text("SIMULASI BERKAS REFERENSI - BUKAN SUMBER ILMIAH", encoding="utf-8")
        self.call("source-add", "--title", "Judul sumber ilustrasi", "--author", "Penulis Uji", "--year", "2025", "--venue", "Jurnal Ilustratif", "--url", "https://example.org/ilustrasi", "--file", str(source_pdf), "--access-status", "abstract_checked")
        data = self.root / "data-sintetis.csv"
        data.write_text("id,nilai\n1,1\n", encoding="utf-8")
        self.call("evidence-add", "--file", str(data), "--kind", "dataset", "--permission", "not_required", "--description", "Data sintetis uji CLI")
        self.call("claim-add", "--chapter", "4", "--kind", "result", "--statement", "Hasil uji ilustratif", "--evidence", "EVD-001", "--status", "supported")
        evidence = json.loads((self.workspace / "registry" / "evidence.json").read_text())
        self.assertEqual(evidence[0]["id"], "EVD-001")
        from hashlib import sha256
        self.assertEqual(evidence[0]["sha256"], sha256(data.read_bytes()).hexdigest())
        chapter = self.workspace / "chapters" / "bab-2.md"
        chapter.write_text("# BAB II — TINJAUAN PUSTAKA\n\n## 2.1 Kajian\n\nContoh teks yang jelas diberi label ilustrasi dan tidak berisi hasil penelitian nyata. [cite:SRC-001]\n", encoding="utf-8")
        self.call("build", "--mode", "draft", "--docx-only")
        from docx import Document
        document = Document(str(self.workspace / "output" / "skripsi-draft.docx"))
        joined = "\n".join(paragraph.text for paragraph in document.paragraphs)
        self.assertIn("(Uji, 2025)", joined)
        self.assertIn("Judul sumber ilustrasi", joined)
        self.assertNotIn("[cite:SRC-001]", joined)
        self.assertTrue(any("DRAF" in paragraph.text for paragraph in document.sections[0].header.paragraphs))

    @unittest.skipUnless(shutil.which("libreoffice"), "LibreOffice wajib untuk final")
    def test_full_synthetic_review_and_final_workflow(self) -> None:
        """Menguji mekanik final dengan artefak uji yang secara eksplisit tidak sah akademik."""
        source_file = self.root / "sumber-sintetis.txt"
        source_file.write_text("INI HANYA SUMBER UJI TERBUAT, BUKAN ARTIKEL AKADEMIK.\n" * 8, encoding="utf-8")
        data_file = self.root / "hasil-uji-sintetis.csv"
        data_file.write_text("id,status\n1,success\n2,success\n", encoding="utf-8")
        self.call("source-add", "--title", "Publikasi ilustrasi untuk unit test", "--author", "Penulis Uji", "--year", "2026", "--venue", "Jurnal Sintetis (bukan nyata)", "--url", "https://example.org/test-sintetis", "--file", str(source_file), "--access-status", "fulltext_checked", "--metadata-checked", "--verification-note", "Berkas sintetis telah dibaca sebagai bagian dari unit test, bukan verifikasi akademik.")
        self.call("evidence-add", "--file", str(data_file), "--kind", "dataset", "--permission", "not_required", "--sensitivity", "public", "--description", "Data sintetis untuk pengujian generator")
        self.call("claim-add", "--chapter", "4", "--kind", "result", "--statement", "Dua record sintetis ditandai success.", "--evidence", "EVD-001", "--status", "supported")
        self.call("claim-add", "--chapter", "5", "--kind", "conclusion", "--statement", "Pengujian contoh mengandung dua record.", "--evidence", "EVD-001", "--status", "supported")
        project_file = self.workspace / "project.json"
        project = json.loads(project_file.read_text(encoding="utf-8"))
        project.update({"university": "Institusi Simulasi (tidak nyata)", "program": "Program Uji", "student_name": "Penguji Sintetis", "student_id": "TEST-001", "year": 2026, "method": "Pemeriksaan mekanik CLI", "research_object": "Berkas uji ilustratif", "visual_review_confirmed": True,
                        "research_questions": [{"id": "Q1", "text": "Apakah berkas dapat diekspor?"}],
                        "objectives": [{"id": "O1", "text": "Menguji ekspor berkas."}],
                        "alignment": [{"question_id": "Q1", "objective_id": "O1", "method": "Pembuatan dan pembacaan berkas", "result_claim_ids": ["CLM-001"]}]})
        project_file.write_text(json.dumps(project, ensure_ascii=False, indent=2), encoding="utf-8")
        for number in range(1, 6):
            content = (f"# BAB {number} - BAGIAN UJI SINTETIS\n\n## {number}.1 Prosedur dan Catatan\n\n"
                       + "Seluruh informasi dalam bab ini adalah teks simulasi untuk pengujian perangkat lunak, bukan materi akademik yang dapat dikutip. " * 3
                       + "[cite:SRC-001]\n\n"
                       + ("Rujukan klaim hasil internal [claim:CLM-001].\n" if number == 4 else ""))
            (self.workspace / "chapters" / f"bab-{number}.md").write_text(content, encoding="utf-8")
        for name in ("abstrak-id.md", "abstract-en.md"):
            (self.workspace / "frontmatter" / name).write_text("# ABSTRAK DEMO\n\n" + "Teks sintetis untuk menguji kelengkapan dan ketahanan generator dokumen; bukan klaim akademik. " * 3, encoding="utf-8")
        self.call("check", "--mode", "review")
        review = json.loads((self.workspace / "audit" / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(review["status"], "SIAP_DITINJAU")
        self.call("check", "--mode", "final", expected=2)
        checklist = self.workspace / "audit" / "manual-review.md"
        raw = checklist.read_text(encoding="utf-8")
        checklist.write_text(raw.replace("- [ ]", "- [x]").replace("[PERLU CATATAN REVIEW NYATA]", "Catatan uji perangkat lunak sintetis: bukan review akademik sungguhan."), encoding="utf-8")
        (self.workspace / "frontmatter" / "lembar-pengesahan.md").write_text("# LEMBAR PENGESAHAN UJI SINTETIS\n\n" + "BERKAS DUMMY UNTUK TEST; TIDAK MENGANDUNG PERSETUJUAN AKADEMIK YANG SAH. " * 2, encoding="utf-8")
        fake = self.root / "bukan-persetujuan.txt"
        fake.write_text("NOT VALID ACADEMIC APPROVAL; SOFTWARE TEST ONLY", encoding="utf-8")
        self.call("approval-add", "--role", "researcher", "--decision", "approved", "--file", str(fake), "--note", "Persetujuan sintetis; hanya untuk uji mekanik")
        self.call("approval-add", "--role", "supervisor", "--decision", "approved", "--file", str(fake), "--note", "Persetujuan sintetis; hanya untuk uji mekanik")
        # Simulasi catatan audit editorial dan kontribusi bukan bukti akademik nyata.
        for chapter_number in range(1, 6):
            self.call("citation-review-add", "--chapter", str(chapter_number), "--source", "SRC-001",
                      "--claim-text", f"Pernyataan demonstrasi pada Bab {chapter_number}",
                      "--locator", "Baris sintetis", "--verdict", "supported", "--reviewer", "Unit test")
        self.call("contribution-add", "--kind", "artifact", "--statement", "Perangkat lunak uji sintetis",
                  "--question", "Q1", "--distinction", "Hanya simulasi antarmuka CLI",
                  "--limitations", "Tidak memberikan bukti akademik", "--evidence", "EVD-001",
                  "--status", "supported", "--reviewer", "Unit test")
        for domain in ("human_writing", "citation_integrity", "patchwriting", "original_contribution", "readability"):
            self.call("quality-review-add", "--domain", domain, "--decision", "approved",
                      "--reviewer", "Unit test", "--note", "Review dummy untuk menguji state machine, bukan evaluasi ilmiah")
        self.call("check", "--mode", "final")
        self.call("build", "--mode", "final")
        self.assertTrue((self.workspace / "output" / "skripsi-final.docx").is_file())
        self.assertTrue((self.workspace / "output" / "skripsi-final.pdf").is_file())
        self.assertTrue((self.workspace / "output" / "manifest-final.json").is_file())
        manifest = json.loads((self.workspace / "output" / "manifest-final.json").read_text())
        self.assertGreater(manifest["toc_entries_resolved"], 5)

    @unittest.skipUnless(shutil.which("libreoffice"), "LibreOffice tidak tersedia")
    def test_draft_pdf_export(self) -> None:
        """Membuat PDF draf untuk menguji alur render yang sebenarnya."""
        self.call("build", "--mode", "draft")
        pdf = self.workspace / "output" / "skripsi-draft.pdf"
        self.assertGreater(pdf.stat().st_size, 1024)
        from pypdf import PdfReader
        reader = PdfReader(str(pdf))
        self.assertGreaterEqual(len(reader.pages), 5)


if __name__ == "__main__":
    unittest.main()

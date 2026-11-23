"""Uji modul mutu akademik v5.0, memakai input sintetis yang bukan karya ilmiah nyata."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, str(ROOT / "scripts" / "thesis.py")]
sys.path.insert(0, str(ROOT / "scripts"))
from academic_quality import quality_audit, review_state


class QualityModulesTests(unittest.TestCase):
    """Menilai alur review dan validasi yang dapat dijalankan tanpa koneksi internet."""

    def setUp(self) -> None:
        """Menyiapkan satu workspace sintetis baru untuk setiap pengujian."""
        self.temp = tempfile.TemporaryDirectory(prefix="hack-v5-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.ws = self.root / "skripsi"
        self.run_cli("init", "--title", "DRAF TEST SINTETIS")

    def run_cli(self, cmd: str, *args: str, code: int = 0) -> str:
        """Memanggil CLI sungguhan dan memvalidasi kode keluar yang diharapkan."""
        p = subprocess.run(CLI + [cmd, "--workspace", str(self.ws), *args],
                           capture_output=True, text=True, check=False)
        self.assertEqual(p.returncode, code, f"{p.stdout}\n{p.stderr}")
        return p.stdout

    def source(self) -> None:
        """Mendaftarkan sumber contoh untuk relasi bibliografi saat unit test."""
        self.run_cli("source-add", "--title", "Sumber contoh", "--author", "Penulis Sintetis",
                     "--year", "2026", "--url", "https://example.com/only-test",
                     "--venue", "Jurnal Sintetis")

    def test_human_and_readability_indicators_are_not_ai_scores(self) -> None:
        """Temuan gaya dan panjang kalimat adalah rekomendasi, bukan vonis AI."""
        text = "# Bab I\n\n## Latar Belakang\n\n" + "Di era digital yang semakin berkembang, " + "informasi ini dipaparkan secara runtut " * 22 + ".\n"
        (self.ws / "chapters" / "bab-1.md").write_text(text, encoding="utf-8")
        self.run_cli("quality-audit")
        result = json.loads((self.ws / "audit" / "quality-report.json").read_text())
        self.assertTrue(any(x["code"] == "HAW-001" for x in result["findings"]))
        self.assertTrue(any(x["code"] == "READ-002" for x in result["findings"]))
        self.assertNotIn("ai_probability", result)

    def test_patchwriting_points_to_review_not_plagiarism_score(self) -> None:
        """Frasa sama pada teks sumber ditandai tanpa mengukur kemiripan Turnitin."""
        self.source()
        phrase = "analisis keamanan kode sumber memerlukan pemeriksaan aturan secara sistematis sebelum dilakukan pelaporan hasil akhir"
        source_file = self.root / "example.txt"
        source_file.write_text(phrase, encoding="utf-8")
        self.run_cli("source-text-add", "--source", "SRC-001", "--file", str(source_file))
        (self.ws / "chapters" / "bab-1.md").write_text("# Bab I\n\n## Uji\n\n" + phrase + ".\n", encoding="utf-8")
        findings = quality_audit(self.ws)["findings"]
        self.assertTrue(any(f["code"] == "PAT-001" for f in findings))
        self.assertFalse(any("persen plagiarisme" in f["observation"] for f in findings))

    def test_citation_review_needs_actual_source_and_expires_on_revision(self) -> None:
        """Catatan pemeriksaan sumber-klaim hanya berlaku bagi fingerprint naskah terkait."""
        self.source()
        chap = self.ws / "chapters" / "bab-2.md"
        chap.write_text("# Bab II\n\n## Literatur\n\nKlaim ilustratif mengacu ke sumber. [cite:SRC-001]\n", encoding="utf-8")
        self.assertTrue(any(f["code"] == "CIV-002" for f in quality_audit(self.ws)["findings"]))
        self.run_cli("citation-review-add", "--chapter", "2", "--source", "SRC-001",
                     "--claim-text", "Klaim ilustratif", "--locator", "Halaman 1",
                     "--verdict", "supported", "--reviewer", "Penguji", "--note", "Hanya simulasi")
        self.assertFalse(any(f["code"] == "CIV-002" for f in quality_audit(self.ws)["findings"]))
        chap.write_text(chap.read_text(encoding="utf-8") + "\nRevisi baru.\n", encoding="utf-8")
        self.assertTrue(any(f["code"] == "CIV-003" for f in quality_audit(self.ws)["findings"]))

    def test_contribution_requires_evidence_and_question(self) -> None:
        """Kontribusi yang didukung tidak dapat dicatat tanpa bukti dan Q yang terdaftar."""
        result = self.run_cli("contribution-add", "--kind", "analysis", "--statement", "Uji",
                              "--question", "Q1", "--distinction", "Perbedaan", "--limitations", "Batas",
                              "--reviewer", "Penguji", "--status", "supported", code=2)
        self.assertEqual(result, "")
        project = json.loads((self.ws / "project.json").read_text())
        project["research_questions"] = [{"id": "Q1", "text": "Pertanyaan sintetis"}]
        (self.ws / "project.json").write_text(json.dumps(project), encoding="utf-8")
        # Masih ditolak tanpa bukti ketika meminta status supported.
        self.run_cli("contribution-add", "--kind", "analysis", "--statement", "Uji",
                     "--question", "Q1", "--distinction", "Perbedaan", "--limitations", "Batas",
                     "--reviewer", "Penguji", "--status", "supported", code=2)
        data = self.root / "data.txt"
        data.write_text("Hanya data sintetis", encoding="utf-8")
        self.run_cli("evidence-add", "--file", str(data), "--kind", "analysis", "--description", "Uji sintetis",
                     "--permission", "not_required")
        self.run_cli("contribution-add", "--kind", "analysis", "--statement", "Uji",
                     "--question", "Q1", "--distinction", "Perbedaan", "--limitations", "Batas",
                     "--reviewer", "Penguji", "--status", "supported", "--evidence", "EVD-001")
        self.assertEqual(quality_audit(self.ws)["summary"]["contributions_supported_declared"], 1)

    def test_quality_review_expires_after_manuscript_changes(self) -> None:
        """Review editor yang berlaku pada revisi lama tidak dihitung untuk finalisasi baru."""
        self.run_cli("quality-review-add", "--domain", "readability", "--decision", "approved",
                     "--reviewer", "Penguji", "--note", "Hanya unit test")
        self.assertTrue(review_state(self.ws)["readability"]["current"])
        with (self.ws / "chapters" / "bab-3.md").open("a", encoding="utf-8") as f:
            f.write("\nRevisi.\n")
        self.assertFalse(review_state(self.ws)["readability"]["current"])

    def test_turnitin_report_interpretation_and_validation(self) -> None:
        """Skor bersumber dari input pengguna, tanpa klasifikasi lolos atau kepengarangan."""
        sample = {"source": "user_supplied_report", "report_type": "similarity", "score_percent": 23,
                  "report_date": "2026-11-23", "document_title": "Skripsi Sintetis", "transcribed_by": "Penguji",
                  "language": "id", "matches": [{"category": "possibly_uncited", "location": "Bab II"}]}
        path = self.root / "report.json"
        path.write_text(json.dumps(sample), encoding="utf-8")
        self.run_cli("turnitin-interpret", "--file", str(path))
        interpretation = json.loads((self.ws / "audit" / "turnitin-interpretation.json").read_text())
        self.assertEqual(interpretation["reported_score_percent"], 23)
        self.assertIn("Tidak ada penetapan", interpretation["conclusion"])
        sample["score_percent"] = 150
        path.write_text(json.dumps(sample), encoding="utf-8")
        self.run_cli("turnitin-interpret", "--file", str(path), code=2)


if __name__ == "__main__":
    unittest.main()

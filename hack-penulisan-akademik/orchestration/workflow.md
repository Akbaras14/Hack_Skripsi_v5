# Thesis Orchestrator: end-to-end workflow

Tahapan: `INIT → DESIGN → LITERATURE → PROPOSAL → DATA → ANALYSIS → CHAPTERS → AUDIT → REVIEW → APPROVAL → FINAL`.

**Sifat eksekusi:** satu AI dapat menjalankan tiga peran secara bergilir, dengan berkas di `workspace/` sebagai memori transaksional. Jangan mengaku menjalankan agen paralel jika tidak dilakukan.

## Gerbang fase
| Fase | Input wajib | Keluaran | Kondisi pindah |
|---|---|---|---|
| INIT | Judul, kampus, peneliti, izin | `project.json` | metadata utama diisi |
| DESIGN | Masalah, pertanyaan, tujuan, metode | Peta keselarasan | validasi supervisor jika perlu |
| LITERATURE | Sumber primer | `sources.json`, matriks | klaim pustaka diperiksa |
| PROPOSAL | Hasil perencanaan | Bab I–III | audit akademik proposal |
| DATA | Izin dan instrumen | berkas dan hash | provenance serta akses sah |
| ANALYSIS | Data nyata | klaim hasil dan tabel | analisis dapat direproduksi |
| CHAPTERS | Kumpulan hasil | Bab IV–V | simpulan sesuai hasil |
| AUDIT | Semua naskah | laporan struktural + manual | seluruh isu material diselesaikan |
| REVIEW | audit bersih secara struktural | DOCX/PDF review | telaah manusia dilakukan |
| APPROVAL | persetujuan nyata | berkas bukti persetujuan | status terverifikasi administratif |
| FINAL | review visual, persetujuan | DOCX/PDF dan manifest | tidak ada gate yang gagal |

Jika sumber, izin, atau hasil belum ada, berikan tugas terarah kepada pengguna dan lanjutkan bagian lain yang aman, tidak mengisi kekosongan secara spekulatif.

## Pemulihan
Sebelum melanjutkan: baca `state.json`, `project.json`, `logs/decisions.jsonl`, `registry/*.json`, bab terkait, dan laporan `audit/report.md` terbaru. Perubahan judul/metode harus dicatat sebagai keputusan; jangan diam-diam mengubah kontrak penelitian.

## Runbook
```
python scripts/thesis.py init --workspace ./skripsi-proyek --title "Judul penelitian"
python scripts/thesis.py source-add --workspace ./skripsi-proyek --title "Judul publikasi" --author "Nama Penulis" --year 2025 --url https://contoh.org --access-status abstract_checked
python scripts/thesis.py evidence-add --workspace ./skripsi-proyek --file ./data/hasil.csv --kind dataset --permission authorized --description "Hasil pengumpulan data aktual"
python scripts/thesis.py claim-add --workspace ./skripsi-proyek --chapter 4 --kind result --statement "..." --evidence EVD-001 --status supported
python scripts/thesis.py check --workspace ./skripsi-proyek --mode review
python scripts/thesis.py build --workspace ./skripsi-proyek --mode draft
```
Perintah contoh menggunakan metadata ilustratif. `build --mode final` tidak boleh dijalankan sampai audit dan bukti persetujuan tersedia.


## Perluasan v5

Jalankan `quality-audit` pada akhir setiap draf bab yang signifikan. Sebelum final, periksa `orchestration/quality-v5.md` dan catat review manual berikat fingerprint untuk HAW, CIV, PAT, OCV, READ. Audit Turnitin bersifat opsional dan hanya atas data laporan asli.

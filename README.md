# Hack Skripsi v5.0 — End-to-End Thesis + Academic Quality Assurance

**Rilis 23 November 2026.** Upgrade dari paket v4.0 (yang dibangun dari v3.0) yang mempertahankan 5 referensi aturan dan 7 aset asli **byte-identik**. Mode baru menyusun alur Bab I–V dengan Research Agent, Writing Agent, Audit Agent, registry bukti, audit struktural, dan generator DOCX/PDF.

> Mesin ini **bukan generator yang boleh menciptakan hasil ilmiah**. Penulisan substantif dilakukan melalui agen ChatGPT/Codex/Claude/Gemini atau secara manual dengan merujuk sumber dan bukti nyata. Python CLI berjalan **tanpa API LLM** untuk manajemen berkas, pengujian struktural, ekspor, dan checksum. Ia tidak memverifikasi kualitas sumber secara otomatis dari internet, ketepatan hasil statistik, atau autentisitas persetujuan.

## Paket

- `hack-penulisan-akademik/SKILL.md` — entri skill
- `references/` — **232 entri** v3.0: HP60, P25, S35, LPA50, PPS12, BI50
- `agents/` — tiga peran dengan kontrak input/output berbeda
- `orchestration/` — workflow, gerbang final, kebijakan sumber, pemulihan, ekspor
- `scripts/` — CLI Python modular, registri dan pembuat DOCX/PDF
- `templates/` — Bab I–V, abstrak, lembar pengesahan, checklist manual
- `schemas/` — contoh metadata; bukan data penelitian
- `tests/` — uji otomatis dan smoke test ekspor

## Kebutuhan

- Python **3.11+** (digunakan fungsi `Path.is_relative_to`)
- `pip install -r requirements.txt` untuk DOCX dan pemetaan nomor halaman daftar isi PDF
- LibreOffice untuk PDF (`--docx-only` tersedia jika belum terinstal)
- **Tidak membutuhkan Docker, cloud, server, API key, ataupun koneksi jaringan** untuk alur lokal.

## Langkah 1 — Inisialisasi

```bash
cd hack-penulisan-akademik
python scripts/thesis.py init --workspace ./workspace-vibesec --title "Judul penelitian yang telah disetujui"
```

Isi `workspace-vibesec/project.json` menggunakan **data penelitian sebenarnya**, termasuk `research_questions`, `objectives`, dan `alignment`. Semua bagian belum diketahui sengaja dibiarkan kosong. Template BAB I–V dibuat sebagai kerangka dengan placeholder transparan.

## Langkah 2 — Registrasi literatur dan bukti

```bash
python scripts/thesis.py source-add --workspace ./workspace-vibesec \
  --title "Judul publikasi sesuai sumber" --author "Nama penulis sesuai sumber" \
  --year 2025 --venue "Nama jurnal" --url "https://alamat-artikel-yang-benar" \
  --access-status abstract_checked

python scripts/thesis.py evidence-add --workspace ./workspace-vibesec \
  --file /lokasi/data-asli/hasil-uji.csv --kind experiment \
  --permission authorized --sensitivity internal \
  --description "Log uji asli" --provenance "Prosedur dan tanggal pengambilan"

python scripts/thesis.py claim-add --workspace ./workspace-vibesec --chapter 4 \
  --kind result --statement "Pernyataan hasil yang sudah diperiksa" \
  --evidence EVD-001 --status supported
```

`source-add --access-status fulltext_checked` hanya setelah **membaca sumber asli**, dengan `--metadata-checked` dan `--verification-note` yang menjelaskan pemeriksaan. Metadata dan isi sumber tetap harus divalidasi secara akademik.

## Langkah 3 — Tulis dengan tiga agen

Baca `agents/research-agent.md`, `agents/writing-agent.md`, dan `agents/audit-agent.md` secara berurutan, lalu isi `chapters/bab-1.md` ... `bab-5.md`. Sitasi dari registry memakai `[cite:SRC-001]`, yang saat ekspor berubah menjadi `(Penulis, tahun)`; klaim dapat ditautkan melalui `[claim:CLM-001]`. Penanda klaim tidak akan ditampilkan dalam DOCX.

Untuk sesi berikutnya, baca `workspace/state.json`, `project.json`, `registry/*.json`, `logs/decisions.jsonl`, dan `audit/report.md`. Catat keputusan baru:

```bash
python scripts/thesis.py decision-add --workspace ./workspace-vibesec \
  --actor "dosen pembimbing" --note "Revisi desain pengujian sesuai catatan rapat ..."
```

## Langkah 4 — Cek dan ekspor

```bash
python scripts/thesis.py status --workspace ./workspace-vibesec
python scripts/thesis.py check --workspace ./workspace-vibesec --mode review
python scripts/thesis.py build --workspace ./workspace-vibesec --mode draft
```

Keluaran: `output/skripsi-draft.docx`, `output/skripsi-draft.pdf`, `output/manifest-draft.json`, serta `audit/report.md`. Draf **selalu** berlabel belum final. Untuk mode review, placeholder dan isu material memblokir ekspor.

## Langkah 5 — Finalisasi yang terkendali

Lengkapi lima bab, hasil berbasis bukti, abstrak, sumber primer, checklist `audit/manual-review.md`, serta lembar pengesahan resmi. Set `visual_review_confirmed: true` **hanya setelah** mengecek seluruh halaman; kemudian daftarkan berkas persetujuan sah melalui `approval-add` untuk peneliti dan pembimbing.

```bash
python scripts/thesis.py approval-add --workspace ./workspace-vibesec \
  --role researcher --decision approved --file /lokasi/berkas-persetujuan-peneliti.pdf
python scripts/thesis.py approval-add --workspace ./workspace-vibesec \
  --role supervisor --decision approved --file /lokasi/berkas-persetujuan-pembimbing.pdf
python scripts/thesis.py check --workspace ./workspace-vibesec --mode final
python scripts/thesis.py build --workspace ./workspace-vibesec --mode final
```

**Penting:** CLI tidak dapat memastikan persetujuan itu benar-benar dari penandatangan berwenang; catatan yang diisikan pengguna tetap harus diautentikasi. Lembar pengesahan dan template akhir perlu disesuaikan manual dengan kampus. Hasil daftar pustaka adalah **draf**, bukan implementasi penuh seluruh kasus APA 7. Daftar isi PDF dihitung otomatis dari halaman yang dirender; setelah perubahan manual di Word, periksa ulang semua nomor halaman. DOCX/PDF tetap wajib diperiksa secara visual.

## Uji

```bash
cd hack-penulisan-akademik
python -m unittest discover -s tests -v
```

## Instalasi skill

Salin direktori `hack-penulisan-akademik/` ke `.agents/skills/hack-penulisan-akademik/` untuk Codex/Gemini/Antigravity, atau `.claude/skills/hack-penulisan-akademik/` untuk Claude Code. Di ChatGPT gunakan fitur Skills jika akun mendukung atau unggah referensi ke Project. Tidak ada instalasi atau sinkronisasi GitHub otomatis pada pembuatan paket ini.

## Kebijakan kerahasiaan

`workspace` adalah folder **yang menampung file bukti asli**, mungkin mengandung data internal/rahasia. Jangan commit `workspace/` ke GitHub publik, jangan memasukkan berkas pasien, kode perusahaan atau kredensial ke chat tanpa izin dan penyamaran data. Bukti hash mendeteksi perubahan byte, bukan membuktikan kebenaran data atau persetujuan.

## Orkestrasi fase dan handoff antar-sesi

```bash
python scripts/thesis.py advance --workspace ./workspace-vibesec \
  --to DESIGN --actor "peneliti" --note "Judul dan rancangan awal telah dikaji"
python scripts/thesis.py handoff --workspace ./workspace-vibesec
```

`advance` hanya mengizinkan perpindahan satu fase ke depan setelah prasyarat minimal terpenuhi, atau mundur untuk revisi. Ini bukan mekanisme persetujuan otomatis. `handoff` membuat `audit/handoff.md` berisi ringkasan fase, peran agen, sumber, bukti, dan daftar masalah struktural. Berkas ini dapat dipakai sebagai konteks untuk melanjutkan pengerjaan pada sesi ChatGPT/Codex/Claude/Gemini lain tanpa API key.


## Upgrade v5.0 — enam modul pemeriksaan akademik

Semua 232 entri aturan/gerbang (HP60, P25, S35, LPA50, PPS12, BI50) dipertahankan. Enam modul baru berada di `hack-penulisan-akademik/modules/` dan terhubung ke `orchestration/quality-v5.md`.

| Modul | Hasil otomatis | Apa yang tetap harus diperiksa peneliti |
|---|---|---|
| Human Academic Writing Quality | Indikator frasa generik dan pembukaan paragraf repetitif | Relevansi argumen, nada ilmiah, dan suara peneliti |
| Citation Integrity Validator | ID sitasi, catatan review per pasangan bab–sumber, fingerprint | Klaim, teks lengkap, lokasi, konteks, dan APA 7 |
| Patchwriting Detector | Rangkaian minimal 9 token sama dengan teks sumber lokal | Kutipan sah, istilah baku, kepengarangan, dan parafrase |
| Original Contribution Validator | Keberadaan deskripsi kontribusi, relasi Q–EVD, perbandingan/keterbatasan | Kebaruan, ketepatan metode, substansi hasil |
| Academic Readability Auditor | Kalimat >48 token, paragraf >175 token sebagai indikator | Keefektifan kalimat sesuai EYD/KBBI dan ilmu terkait |
| Turnitin Report Interpreter | Interpretasi data laporan JSON yang diberikan pengguna | Keaslian laporan, konteks kecocokan, kebijakan kampus |

### Alur CLI v5.0

Jalankan contoh berikut dari folder `hack-penulisan-akademik/` setelah `init`, `source-add`, dan `evidence-add`.

```bash
python scripts/thesis.py source-text-add --workspace ./workspace-vibesec \
  --source SRC-001 --file /path/teks-referensi-yang-sah.txt \
  --note "Cuplikan sumber untuk pemeriksaan parafrase"

python scripts/thesis.py citation-review-add --workspace ./workspace-vibesec \
  --chapter 2 --source SRC-001 --claim-text "Klaim yang ditulis pada Bab II" \
  --locator "Bagian 3.2, halaman 6" --verdict supported \
  --reviewer "Peneliti" --note "Dibaca pada naskah asli"

python scripts/thesis.py contribution-add --workspace ./workspace-vibesec \
  --kind analysis --statement "Kontribusi yang benar-benar dihasilkan" \
  --question Q1 --distinction "Perbedaan terhadap publikasi pembanding" \
  --limitations "Batas dataset dan pengujian" --evidence EVD-001 \
  --status supported --reviewer "Peneliti"

python scripts/thesis.py quality-audit --workspace ./workspace-vibesec
```

Setelah benar-benar meninjau naskah dan laporan audit, tandai **lima domain** (jalankan perintah terpisah untuk setiap domain). Contoh:

```bash
python scripts/thesis.py quality-review-add --workspace ./workspace-vibesec \
  --domain citation_integrity --decision approved \
  --reviewer "Peneliti" --note "Seluruh klaim yang dikutip telah dicocokkan dengan sumber asli"
```

Domain yang diizinkan: `human_writing`, `citation_integrity`, `patchwriting`, `original_contribution`, `readability`. Saat bab atau frontmatter berubah, persetujuan editorial dan review sitasi menjadi kedaluwarsa. **Satu review bab–sumber adalah kelengkapan minimum mesin; pengguna tetap harus memeriksa setiap klaim secara substantif.**

### Jika tersedia laporan Turnitin nyata

Salin `schemas/turnitin-report.example.json` menjadi file JSON lain, isi **hanya dari laporan asli**, dan jalankan:

```bash
python scripts/thesis.py turnitin-interpret --workspace ./workspace-vibesec \
  --file /path/laporan-yang-disalin-manual.json
```

Hasil ada di `workspace-vibesec/audit/turnitin-interpretation.md`. Skor pada JSON contoh hanyalah data sintetis, **bukan hasil pengujian**. Fitur tidak mengakses Turnitin dan tidak menyatakan lulus/gagal. Bahasa Indonesia tidak tercantum sebagai bahasa yang didukung di halaman persyaratan AI Writing Report Turnitin yang diperiksa 23 November 2026; kemampuan produk dapat berubah. Periksa [ketentuan bahasa terbaru](https://guides.turnitin.com/hc/en-us/articles/28234943089933-File-requirements-for-an-AI-Writing-Report).

### Catatan keamanan dan keterbatasan

- Berkas teks sumber dan data penelitian disalin ke workspace privat dengan checksum. Jangan mendistribusikan sumber berlisensi atau informasi rahasia.
- CLI hanya melakukan pemeriksaan deterministik/heuristik. Persetujuan editorial bersifat deklaratif dan **tidak membuktikan pemeriksaan akademik secara independen**.
- Jangan memakai persentase similarity atau AI Writing sebagai target yang dikejar, bukti pelanggaran, atau jaminan lolos. Simpan catatan revisi dan ikuti prosedur institusi.
- Pengujian sintetik menguji mekanisme kode, bukan menjamin kualitas sebuah skripsi sungguhan.

### Pengujian

```bash
python -m unittest discover -s tests -v
```

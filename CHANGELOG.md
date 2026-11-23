# v5.0 — 23 November 2026

- Enam modul Academic Quality Assurance (HAW/CIV/PAT/OCV/READ/TRI).
- `academic_quality.py`: audit frasa, keterbacaan, kemiripan teks lokal, registri tinjauan sitasi dan kontribusi.
- `turnitin_interpreter.py`: penafsiran input JSON dari laporan asli pengguna, tanpa akses layanan/prediksi/label lolos.
- CLI menambah enam perintah dan gerbang persetujuan manual yang terikat checksum naskah terbaru.
- Dua daftar sumber normatif: APA 7 dan Purdue OWL serta dokumentasi Turnitin.
- Tes unit baru untuk setiap modul dan regresi finalisasi sintetis; aturan terdahulu byte-identik.
- Batasan: heuristik bukan deteksi AI, plagiarisme, validasi ilmiah, atau autentikasi institusi.

# Changelog — Hack Skripsi v4.0

- Mempertahankan berkas `references/` dan `assets/` v3.0 tanpa perubahan byte.
- Menambahkan orkestrasi siklus penelitian Bab I–V dan tiga peran agen (Research, Writing, Audit).
- Menambahkan sumber ilmiah dengan status pemeriksaan (bukan klaim verifikasi otomatis).
- Menambahkan evidence registry dengan salinan lokal, SHA-256 dan metadata perizinan.
- Menambahkan claim registry, mapping pertanyaan–tujuan–metode–hasil, serta log keputusan sesi.
- Menambahkan audit struktural dan status draft/review/final yang memblokir pelanggaran.
- Menambahkan DOCX/PDF builder dengan daftar pustaka draf dan manifest checksum.
- Menambahkan template lima bab, abstrak, lembar pengesahan dan manual review.
- Menambahkan unittest, smoke test, serta dokumentasi instalasi tanpa LLM API.

**Limitasi utama:** pembuatan isi substantif memerlukan agen/peneliti, validasi ilmu dan bahasa secara manual, serta template kampus yang sah. Tidak ada jaminan penerimaan skripsi atau integritas data di luar bukti yang disediakan.

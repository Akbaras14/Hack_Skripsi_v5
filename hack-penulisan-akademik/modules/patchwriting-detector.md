# Patchwriting Detector (PAT)

**Tujuan:** menemukan frasa yang mungkin terlalu dekat dengan sumber lalu meminta pemeriksaan kutipan dan parafrase.

## Cara kerja
- Pengguna menyertakan teks sumber `.txt` atau `.md` yang memang berhak diakses melalui `source-text-add`; disalin dan diberi SHA-256.
- `quality-audit` membandingkan urutan kata (default 9 token beruntun) pada prosa bab dengan teks sumber lokal.
- Periksa kemunculan dalam kutipan langsung, nomenklatur, definisi baku, rumus, atau templat institusi sebelum memutuskan perlu revisi.
- Untuk paragraf yang terlalu dekat, baca sumber, tutup sumber, tulis ulang dari pemahaman, lalu tambahkan atribusi. Jangan menggunakan substitusi sinonim mekanis.

**Batasan:** Ini perbandingan *exact phrase* sederhana, bukan detektor plagiarisme, bukan Turnitin, tidak mencari teks internet, tidak memahami semantik, serta dapat menghasilkan false positive/false negative. Ketiadaan temuan bukan bukti bebas plagiarisme. Teks sumber yang bukan publik jangan diunggah/diterbitkan tanpa izin.

**Kode:** `PAT-001` kesamaan frasa perlu konteks; `PAT-000` sumber tak dapat diverifikasi; `PAT-003` pembanding terlalu panjang.
**Dasar:** https://owl.purdue.edu/owl/research_and_citation/using_research/quoting_paraphrasing_and_summarizing/paraphrasing.html

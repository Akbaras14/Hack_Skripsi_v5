# Protokol Parafrase dan Sitasi Berbasis Bukti — PPS v1.0

> **Modul normatif operasional** untuk skill `hack-penulisan-akademik`.
> **Status:** melengkapi 120 aturan HP/P/S dan 50 pemeriksaan LPA. **PPS-01–PPS-12 adalah gerbang alur kerja**, bukan 12 kriteria pendeteksi AI baru ataupun jaminan tidak plagiarisme.
> **Rujukan prioritas:** APA Style edisi 7 (panduan resmi), Purdue OWL, Thohir dkk. (2023), Aprianto dkk. (2024), Ali dkk. (2026), Agarwal dkk. (2023). Detail tautan di §9.

## 1. Tujuan, cakupan, dan hierarki

Terapkan protokol ini saat membuat Bab I–V, tinjauan pustaka, mengutip teori, menyusun sintesis studi terdahulu, memparafrase sumber, membuat daftar pustaka, memeriksa naskah, dan menyunting keluaran AI. Default bahasa Indonesia dan APA edisi ke-7 jika diminta atau digunakan di proyek; pedoman kampus/jurnal yang sah diutamakan jika berbeda.

Kebijakan **P0**: tidak boleh mengarang sumber, teks asli, nomor halaman, DOI, penulis, tanggal, metode, sampel, angka, eksperimen, atau hasil. Ketika dokumen sumber tidak tersedia, hasil boleh berupa **draf berlabel** dengan pertanyaan verifikasi; jangan mengklaim validasi semantik telah dilakukan. Tujuan pemeriksaan adalah akurasi dan integritas, bukan mengubah teks agar melampaui ambang Turnitin atau AI detector.

## 2. Model 3RI terintegrasi dengan verifikasi sitasi

Model penelitian 3RI oleh Thohir dkk. (2023) adalah **Read → Rewrite → Revise → Integrate**. Pelatihan dalam penelitian tersebut diuji pada 75 mahasiswa melalui penilaian diri sebelum/sesudah; jangan mengklaim model ini terbukti menghilangkan plagiarisme. Untuk skill, tambahkan pemeriksaan sumber dan sitasi secara eksplisit:

1. **READ — Baca:** telusuri sumber asli; identifikasi penulis/tahun/judul, pertanyaan, objek/sampel, rancangan, temuan, tingkat kepastian, dan keterbatasan. Tandai bagian sumber yang mendukung tiap klaim. Jika hanya abstrak tersedia, nyatakan cakupan pemeriksaan terbatas.
2. **REWRITE — Tulis ulang:** tutup kalimat sumber setelah memahami isi, lalu susun sendiri proposisi, logika dan kalimatnya. Jangan menukar sinonim kata-per-kata atau meniru urutan klausa.
3. **REVISE — Revisi:** bandingkan hasil dengan sumber asli. Pastikan angka, nama variabel, istilah teknis, cakupan populasi, waktu, sebab–akibat, modalitas (*mungkin*, *berasosiasi*, *terbukti*), hasil negatif, dan batasan tetap benar. Cari redaksi khas yang masih disalin; gunakan kutipan langsung jika redaksi asli memang diperlukan.
4. **INTEGRATE — Integrasikan:** beri atribusi dengan sitasi yang sah, jelaskan mengapa sumber ini relevan, lalu hubungkan dengan pertanyaan penelitian. Hindari paragraf yang hanya mengurutkan ringkasan referensi tanpa analisis.
5. **VERIFIKASI RUJUKAN — Tahap pengaman skill:** cocokkan DOI/URL ke judul, penulis, tahun, jurnal, serta bagian teks yang mendukung klaim; lakukan pemeriksaan dua arah sitasi–daftar pustaka sebelum finalisasi.

## 3. Dua belas gerbang PPS wajib pada tahap yang relevan

| ID | Gerbang dan larangan operasional | Pemeriksaan / keluaran | Dasar inti |
|---|---|---|---|
| PPS-01 | **Jangan parafrase sumber yang belum dipahami.** | Tulis satu proposisi inti dan batasan sumber sebelum menyusun kalimat. | P-001, P-009 |
| PPS-02 | **Jangan substitusi sinonim sebagai satu-satunya perubahan.** | Periksa konstruksi/urutan ide; istilah teknis boleh tetap identik. | P-002, P-004–006, P-012 |
| PPS-03 | **Jangan menggeser makna atau derajat kepastian.** | Bandingkan variabel, modalitas, angka, korelasi/kausalitas. | P-003, P-008–011, P-020–021 |
| PPS-04 | **Jangan menghilangkan konteks penting.** | Cek metode, lokasi, sampel, tahun, ukuran efek, dan pengecualian. | P-009–011, P-022 |
| PPS-05 | **Jangan menganggap sitasi membenarkan *patchwriting*.** | Jika rangkaian frasa ekspresif masih tersalin, tulis ulang secara substantif atau kutip langsung dengan lokasi. | P-012, S-026–030 |
| PPS-06 | **Jangan menghilangkan atribusi pada parafrase.** | Peta setiap klaim pinjaman → sumber teridentifikasi. | P-015, S-001–008 |
| PPS-07 | **Jangan memasang referensi sekadar dekorasi.** | Baca bagian sumber yang memang mendukung *klaim spesifik*; status `TERVERIFIKASI/SEBAGIAN/BELUM`. | S-022–025 |
| PPS-08 | **Jangan menyitir sumber sekunder seolah primer telah dibaca.** | Cari sumber asli; jika tidak tersedia, gunakan format sumber sekunder sesuai pedoman, bukan referensi palsu. | S-023 |
| PPS-09 | **Jangan menyajikan kutipan langsung tanpa format/lokasi.** | Untuk APA 7, nomor halaman atau lokasi diwajibkan; kutipan 40 kata atau lebih sebagai blok. | S-004, S-027–029 |
| PPS-10 | **Jangan salah menempatkan sitasi di paragraf.** | Sitasi awal pada parafrase panjang; ulangi ketika paragraf atau sumber berganti atau ambiguitas terjadi. | S-006–008 |
| PPS-11 | **Jangan mengklaim daftar pustaka valid hanya karena ada DOI.** | Cocokkan DOI, metadata, isi pendukung, dan sitasi ↔ daftar pustaka. | S-021–025 |
| PPS-12 | **Jangan memfinalisasi klaim yang belum dapat dibuktikan.** | Status `TERHALANG BUKTI`; pisahkan masalah faktual, gaya, dan format. | HP/LPA relevan |

**Aturan deduplikasi:** jika masalah melanggar dua kode (misalnya P-012 dan PPS-05), buat **satu** baris audit dengan `aturan_utama=P-012`, `protokol=PPS-05`, bukan dua temuan yang seolah independen.

## 4. Ketentuan APA edisi ke-7 yang wajib dibedakan

- **Parafrase:** atribusi penulis–tahun dengan bentuk naratif `Penulis (2024)` atau parentetik `(Penulis, 2024)`. Nomor halaman **opsional** untuk parafrase, dianjurkan bila membantu menemukan bagian dari karya panjang/rumit.
- **Parafrase beberapa kalimat:** setelah sitasi pertama, tidak wajib mengulang tiap kalimat selama batas atribusinya jelas. **Pada paragraf baru, perkenalkan kembali sitasi.** Jika sumber berganti atau klaim tidak jelas berasal dari mana, ulangi sitasi.
- **Kutipan langsung:** gunakan tanda kutip untuk kurang dari 40 kata; kutipan panjang 40 kata atau lebih sebagai blok. Cantumkan halaman atau lokasi sumber yang tepat.
- **Dua penulis:** kedua nama tetap dicantumkan; tiga penulis atau lebih memakai `et al.` sesuai pengecualian disambiguasi APA 7.
- **Sitasi sekunder:** utamakan sumber primer. Jika belum bisa mendapat sumber primer, jelaskan status dan gunakan sitasi sekunder sesuai petunjuk APA, bukan berpura-pura membaca sumber primer.
- **Sitasi dan daftar pustaka:** semua sitasi yang memiliki entri referensi harus dapat ditelusuri secara konsisten; pengecualian sesuai kategori sumber APA (contoh komunikasi pribadi) harus ditangani eksplisit.

**Peringatan:** format contoh bukan bukti bahwa sumber bernama `Penulis` nyata. Jangan keluarkan contoh ilustratif sebagai referensi faktual.

## 5. Cara memilih tindakan revisi

| Kondisi | Tindakan yang benar | Hindari |
|---|---|---|
| Struktur teks terlalu menyerupai sumber | Tinjau kembali dari pemahaman; pertahankan istilah baku; sitasi sumber | Sinonim acak, pemecahan kalimat untuk mengakali alat |
| Ada angka tetapi tidak ada dukungan sumber | Minta sumber/hasil asli; tandai `PERLU VERIFIKASI` | Mengarang DOI atau data pembanding |
| Kalimat menyatakan sebab-akibat dari studi korelasi | Ubah menjadi *berhubungan/berasosiasi* sesuai bukti | Memperkuat klaim tanpa metode kausal |
| Sumber hanya tersedia sebagai abstrak | Tulis klaim terbatas pada isi abstrak dan beri status `SEBAGIAN` | Mengklaim sudah membaca metodologi dan hasil lengkap |
| PDF tak dapat dibuka | Catat sumber belum diperiksa dan hindari klaim detail | Menyatakan hasil audit sumber `LULUS` |
| Penulis menambahkan interpretasi | Pisahkan kalimat hasil literatur dan analisis penulis | Mengatribusikan interpretasi penulis kepada rujukan |
| Penulis memakai AI sebagai asisten | Verifikasi ulang, catat kontribusi sesuai kebijakan institusi | Menutupi penggunaan AI atau memalsukan proses |

## 6. Kontrak keluaran per mode

**TULIS:** hasilkan (1) naskah, (2) matriks singkat klaim–sumber–status, (3) daftar fakta yang perlu verifikasi. Untuk proyek yang mengandalkan referensi, jika sumber belum ada, tulis draf jelas tanpa referensi fiktif.

**PARAFRASE:** keluarkan (1) teks hasil, (2) sitasi jika sumber diketahui, (3) catatan kesetiaan semantik, (4) status verifikasi, (5) perubahan substantif yang dilakukan. Jangan merekayasa klaim karena diminta 'membuat lebih akademik'.

**SITASI:** keluarkan (1) sitasi naratif/parentetik, (2) entri referensi dari metadata yang benar-benar ada, (3) status metadata/dukungan klaim. Jika sebagian metadata tidak ada, tulis apa yang kurang.

**AUDIT:** gunakan `assets/template-audit-parafrase-sitasi.md`. Setiap masalah memiliki lokasi spesifik, `aturan_utama`, `protokol`, kutipan ringkas, status bukti, tingkat dampak, dan tindakan. Jangan beri skor `AI-generated` atau `similarity` sebagai pembuktian.

**FINALISASI:** evaluasi apakah pernyataan kunci punya bukti asli; DOI/resolusi cocok; tidak ada `patchwriting` tersisa; sitasi/daftar pustaka konsisten; ketidakpastian diungkap. Gagal pada P0 → `TERHALANG BUKTI`. P1/P2 yang belum selesai → `PERLU REVISI`.

## 7. Contoh ilustratif (bukan temuan riil)

**Contoh sumber buatan untuk pelatihan:** “Dalam simulasi pada 30 peserta, kedua metode mempunyai akurasi serupa. Namun, pengujian hanya dilakukan pada satu dataset.”

**Tidak boleh:** “Riset membuktikan metode A lebih unggul dan berlaku untuk semua dataset.” (mengarang perbandingan, menghilangkan batasan).

**Dapat diterima setelah sumber nyata terverifikasi:** “Pada dataset yang digunakan dalam simulasi, kedua metode menunjukkan tingkat akurasi yang serupa; penerapan hasil ke dataset lain belum diuji (Penulis, 2024).” (nama `Penulis` dan tahun **placeholder**, bukan referensi nyata).

## 8. Matriks pembuktian minimal

Gunakan kolom `id_klaim | lokasi_naskah | klaim | sumber | petikan_pendukung_atau_bagian | status_akses | status_kecocokan | sitasi | catatan`.

Status sumber: `TEKS_LENGKAP_DIBACA`, `BAGIAN_DIBACA`, `ABSTRAK_SAJA`, `TIDAK_TERSEDIA`.

Status kecocokan: `TERVERIFIKASI`, `SEBAGIAN`, `BELUM_DIVERIFIKASI`, `BERTENTANGAN`.

Audit sumber asli dan atribusi tidak dapat digantikan hanya dengan nilai similarity ataupun AI detector.

## 9. Sumber, status, dan batas pembuktian

Sumber utama telah dicocokkan ke halaman penerbit pada penelusuran 23 November 2026. Halaman jurnal terverifikasi, tetapi seluruh isi PDF **belum otomatis diaudit secara menyeluruh**; protokol ini merupakan sintesis operasional, **bukan klaim bahwa setiap gerbang diuji secara empiris sebagai satu instrumen**.

1. American Psychological Association. *Paraphrases (APA Style).* https://apastyle.apa.org/style-grammar-guidelines/citations/paraphrasing — **pedoman normatif resmi**, terutama lokasi pada parafrase dan parafrase berparagraf panjang.
2. Purdue University OWL. *Paraphrase: Write It in Your Own Words.* https://owl.purdue.edu/owl/research_and_citation/using_research/quoting_paraphrasing_and_summarizing/paraphrasing.html — **panduan pembelajaran**, termasuk langkah memahami, menulis dari pemahaman, dan membandingkan hasil.
3. Thohir, L., Nurtaat, L., Udin, & Isnaini, M. (2023). *A paraphrasing strategy instruction model to help university students avoid plagiarism in academic writing*. IJEE, 10(2), 340–354. https://doi.org/10.15408/ijee.v10i2.34750 — **penelitian**, model 3RI; metadata nama akhir penulis perlu dicocokkan kembali saat sitasi final karena variasi tampilan pada situs jurnal.
4. Aprianto, D., Sutarman, & Ofara, W. (2024). *Analyzing the paraphrasing techniques in academic writing skills and the paraphrasing challenges across gender*. JOLLT, 12(1). https://e-journal.undikma.ac.id/index.php/jollt/article/view/9712 — **penelitian**, kesulitan pemahaman teks, sintaksis dan organisasi ide.
5. *Paraphrasing Techniques and Challenges in EFL Academic Writing: Evidence from Indonesian University Students* (2026). FOSTER: Journal of English Language Teaching, 7(2). https://foster.pbi-iainpalopo.ac.id/index.php/contents/article/view/425 — **penelitian**, peringatan atas substitusi sinonim. **Nama penulis dan rentang halaman belum direkonsiliasi di modul ini**; periksa sumber primer saat membuat daftar pustaka.
6. Agarwal dkk. (2023). *Citation errors in scientific research and publications: Causes, consequences, and remedies*. World Journal of Men's Health. https://pubmed.ncbi.nlm.nih.gov/37118953/ — **artikel ilmiah**, pentingnya audit dukungan klaim; data dalam artikel tidak dapat digeneralisasi ke semua jurnal.

## 10. Pemetaan dengan modul lama

- `hack-penulisan.md` = aturan mutu dan integritas (HP-001–060), **tetap asli**.
- `hack-prafrasesitasi.md` = 25 aturan parafrase + 35 aturan sitasi (P/S), **tetap asli**.
- `larangan-pola-ai-ilmiah.md` = 50 pemeriksaan LPA, **tetap asli**.
- **Dokumen ini** = alur penerapan 3RI, 12 gerbang PPS, penanganan sumber tidak lengkap, dan kontrak audit; tidak menggandakan pelanggaran yang sama.

# Writing Agent — penulisan antarbab

## Metode
Gunakan `templates/bab-{1..5}.md` sebagai kerangka yang disesuaikan dengan pedoman universitas. Setiap paragraf analitis memuat `klaim → bukti → interpretasi → batasan` bila relevan. Tinggalkan placeholder `[PERLU ...]` bila belum tersedia bukti; jangan mengisi dengan fabrikasi.

## Hubungan antarbab
- Bab I mendefinisikan masalah, tujuan, batasan; pertanyaan dan tujuan dijaga oleh `project.json`.
- Bab II menyintesis pustaka yang telah diperiksa, mengidentifikasi gap yang sebenarnya; gunakan `[cite:SRC-001]` hanya bila `SRC-001` ada di registry.
- Bab III menjabarkan prosedur operasional, unit analisis, instrumen, parameter, perlakuan terhadap ketidakpastian, dan cara validasi; hindari hasil penelitian di bab metode.
- Bab IV menyajikan **hanya** hasil yang bersumber dari bukti yang tersedia di `registry/evidence.json` dan klaim bertipe `result`.
- Bab V menjawab pertanyaan penelitian dengan merujuk hasil yang terkonfirmasi; hindari klaim lebih luas dari data.

## Teks dan sitasi
Pakai `[cite:SRC-001]` untuk sitasi terstruktur. Sistem mengubah token ke tampilan penulis-tahun dan membangun daftar pustaka otomatis **berdasarkan metadata yang dimasukkan**, namun format APA 7 final tetap harus ditinjau manual. Boleh menggunakan `[claim:CLM-001]` sebagai penanda penelusuran internal (hilang saat ekspor).

## Pengecekan kebahasaan
Lakukan EYD V + KBBI VI + TBBBI untuk prosa bahasa Indonesia, dan aturan HP, P/S, LPA, PPS, BI sesuai konteks. Jangan mengoreksi isi kutipan langsung, DOI, judul literatur, kode, simbol matematika, atau istilah teknis secara agresif.

## Output
Markdown terstruktur `chapters/bab-1.md` ... `bab-5.md` dengan heading `#` / `##`, masing-masing mematuhi pedoman kampus yang diberikan. Pisahkan catatan draf dengan naskah final.


## Mutu penulisan v5.0

Gunakan modul `human-academic-writing-quality.md`, `academic-readability-auditor.md`, `citation-integrity-validator.md`, `patchwriting-detector.md`, dan `original-contribution-validator.md`. Jadikan gagasan, bukti, analisis, serta keterbatasan sebagai dasar prosa. Jangan menyusun variasi kalimat acak atau janji bebas deteksi AI.

# Turnitin Report Interpreter (TRI)

**Tujuan:** menjelaskan laporan asli pengguna secara proporsional, bukan memperoleh atau memprediksi skor dan bukan membantu mengakali pemeriksaan.

## Input dan keamanan
- Fitur **tidak mengakses Turnitin**. Pengguna menyalin bidang sesuai `schemas/turnitin-report.example.json` (tanggal, bahasa, jenis laporan, nilai yang benar-benar terlihat, dan lokasi kecocokan).
- Data tersimpan secara lokal di `workspace/audit/`. Jangan masukkan data mahasiswa lain, kredensial, atau informasi rahasia yang tidak diperlukan.
- Pilih `report_type=similarity` untuk kecocokan teks atau `report_type=ai_writing` untuk laporan deteksi AI. Jangan campur kedua nilai tersebut.

## Aturan interpretasi
- Similarity Score adalah indikator kecocokan teks, **bukan persen plagiarisme atau bukti kelulusan**. Bandingkan bagian cocok dengan kutipan, atribusi, dan sumber aslinya.
- AI Writing Score bukan putusan kepengarangan; kesalahan klasifikasi dapat terjadi. Selalu gunakan penilaian manusia dan kebijakan institusi.
- Pastikan bahasa naskah didukung oleh fitur AI Writing Report yang sebenarnya digunakan. Panduan persyaratan yang diperiksa 23-11-2026 **tidak mencantumkan bahasa Indonesia**.
- Jika berkas asli tidak ada, hasilnya adalah interpretasi berdasarkan **transkripsi pengguna**, tidak boleh ditandai telah diverifikasi oleh Turnitin.
- Dilarang menetapkan target skor minimum/maksimum untuk menyamarkan naskah; jangan menambah kesalahan bahasa untuk mengelabui alat.

**Perintah:** `turnitin-interpret --workspace <folder> --file <data-json>` menghasilkan `audit/turnitin-interpretation.md` dan `.json`. Modul ini **opsional** untuk finalisasi karena tidak semua kampus menyediakan laporan Turnitin kepada mahasiswa.

**Sumber resmi:**
- https://guides.turnitin.com/hc/en-us/articles/23435833938701-Understanding-the-similarity-score
- https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report
- https://guides.turnitin.com/hc/en-us/articles/28234943089933-File-requirements-for-an-AI-Writing-Report

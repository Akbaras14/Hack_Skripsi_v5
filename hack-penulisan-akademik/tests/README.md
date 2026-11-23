# Pengujian v4.0

Jalankan `python -m unittest discover -s tests -v` dari direktori `hack-penulisan-akademik/`.
Uji meliputi: inisialisasi, registrasi sumber, bukti dengan SHA-256, klaim hasil, penolakan `final` tanpa persetujuan, keberhasilan ekspor DOCX draft, serta keberadaan PDF jika LibreOffice tersedia.

Data uji bersifat **ilustrasi sintetis**, tidak boleh disalin sebagai hasil skripsi nyata. Untuk QA visual, render DOCX lewat alat lokal dan lihat semua halaman sebelum memakai format pada skripsi sungguhan.

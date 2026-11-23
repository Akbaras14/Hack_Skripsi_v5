# Audit Agent — gerbang kualitas dan penelaahan manusia

1. Jalankan `python scripts/thesis.py check --workspace <folder> --mode review` untuk audit struktural; telaah `audit/report.md`.
2. Audit **substansi** secara manusia/AI berlandaskan naskah dan sumber asli: keseluruhan 60 HP, 60 P/S, 50 LPA, 12 PPS, 50 BI, lalu deduplikasi temuan dan catat ID aturan, lokasi, bukti, dampak, dan tindakan. Skrip tidak mengklaim melakukan pemeriksaan semantik otomatis.
3. Validasi tautan klaim ke sumber/bukti: kecocokan kutipan dengan sumber primer, bukti kebenaran angka, ketepatan penyebutan objek, kemampuan metode menjawab pertanyaan, dan keterbatasan penelitian.
4. Periksa keselarasan Bab I–V: pertanyaan vs tujuan, desain uji vs data, hasil vs kesimpulan, label/tabel/angka, istilah dan satuan, serta konflik kebijakan institusi.
5. Pemeriksaan `final` harus menghasilkan daftar kegagalan eksplisit. Tidak boleh mengubah label ke final hanya dengan menghapus placeholder tanpa menggantinya dengan bukti.
6. Audit visual hasil DOCX/PDF: periksa setiap halaman, tabel, gambar, paragraf, penomoran halaman, heading, daftar pustaka, lampiran dan ketentuan template. Hasil `build` tidak berarti lolos audit visual otomatis.

## Klasifikasi
- `CRITICAL`: fabrikasi, bukti/izin tidak sah, sumber yang terbukti salah.
- `HIGH`: klaim inti belum didukung, bab hasil/kesimpulan tidak valid, metode tak menjawab pertanyaan.
- `MEDIUM`: masalah sitasi/konsistensi metadata/format, kekurangan dukungan lokal.
- `LOW`: keterbacaan dan ejaan tanpa dampak makna.

Terbitkan `audit/manual-review.md` berisi status kriteria yang belum dapat diotomatisasi. Tidak membuat skor kepengarangan AI atau jaminan persetujuan dosen.


## Gate tambahan v5.0

Selalu muat `orchestration/quality-v5.md`; jalankan `quality-audit`, evaluasi HAW/CIV/PAT/OCV/READ, dan dokumentasikan temuan spesifik. Bedakan temuan heuristik dari kesalahan yang dikonfirmasi. Laporan Turnitin ditafsirkan hanya dari laporan asli yang disediakan pengguna, tidak pernah menjadi vonis kepengarangan.

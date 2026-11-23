# Prosedur penyusunan dokumen final

1. Lengkapi `project.json`, lima bab, abstrak, dan lampiran yang diwajibkan template kampus.
2. Jalankan `check --mode review` dan selesaikan seluruh masalah struktural.
3. Jalankan Audit Agent untuk menilai ketepatan referensi/semantik/metode; catat dalam `audit/manual-review.md`.
4. Jalankan `build --mode review` untuk menghasilkan DOCX dan PDF dengan watermark teks status `SIAP DITINJAU`, bukan pengesahan.
5. Lakukan review visual seluruh halaman. Ekspor PDF menghitung nomor halaman daftar isi secara otomatis, namun angka harus dicek setelah revisi dokumen. Cocokkan margin, spasi, font, halaman, tabel, lampiran dengan template resmi. DOCX ini memakai format default yang dapat diubah melalui `project.json`, **bukan** klaim otomatis memenuhi panduan universitas tertentu.
6. Jika telah memperoleh persetujuan administratif, catat berkas autentik dengan `approval-add`, dan set `visual_review_confirmed=true` pada `project.json` setelah pemeriksaan visual.
7. Baru kemudian `build --mode final`. CLI memblokir operasi jika bukti atau informasi wajib tidak memenuhi gate struktural. Kebenaran dan keaslian persetujuan tetap memerlukan konfirmasi manusia.

`build --mode draft` tetap diperbolehkan saat isi belum lengkap, dengan label jelas **DRAF / BUKAN HASIL PENELITIAN FINAL**. Ini memungkinkan preview tata letak tanpa membenarkan fabrikasi.

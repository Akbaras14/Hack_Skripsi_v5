# Riwayat revisi dan memori berbasis berkas

- Gunakan `decision-add` untuk menyimpan ringkasan keputusan yang benar-benar terjadi beserta pengusul/peninjau. Log bersifat append-only pada penggunaan CLI normal, tetapi karena berkas lokal dapat diedit, ini **bukan** jejak audit anti-manipulasi.
- Setiap perubahan pada judul, pertanyaan penelitian, metodologi, instrumen, atau batasan harus ditulis ke log; sinkronkan `project.json` dan bab terdampak.
- Ketika pindah sesi atau agen, baca log, cek hash bukti, lakukan `check`, dan uraikan perbedaan dari keputusan terakhir.
- Jangan menyimpan data pribadi atau kode sumber rahasia ke repositori publik. Gunakan penyimpanan lokal dan hak akses yang tepat; pengarsipan di luar paket adalah tanggung jawab pengguna.

# Kebijakan sumber dan klaim

Sumber dibagi `not_accessed`, `abstract_checked`, `fulltext_checked`; metadata boleh diperiksa manual dengan sumber primer dan dicatat `metadata_checked: true`. Setiap sumber harus memiliki penulis, judul, tahun, penerbit/venue dan URL atau DOI. Keteraksesan tautan **bukan bukti** dukungan klaim.

Untuk klaim penelitian, gunakan `registry/claims.json` dan tautkan `source_ids` dan/atau `evidence_ids` sesuai sifat klaim. Bukti mengandung checksum SHA-256, status izin, kategori kerahasiaan, lokasi file dan waktu pengumpulan. Hash mendeteksi perubahan byte setelah registrasi, tetapi tidak membuktikan data tersebut asli atau benar.

Kebijakan sitasi: semua kutipan sumber ditulis sebagai `[cite:SRC-001]` agar dapat diperiksa keberadaannya, lalu diekspor dalam format author-year. Daftar pustaka hasil skrip adalah **bantuan awal APA 7** dan perlu telaah manual (nama penulis lintas budaya, editor, e-location, artikel tanpa DOI, badan hukum, urutan atau kapitalisasi judul). Mengutip kutipan langsung wajib menyimpan lokasi sumber; sistem token sederhana tidak menambahkan nomor halaman otomatis. Hindari kutipan langsung tanpa lokasi.

Tidak boleh menuliskan pernyataan `telah divalidasi` sebelum membaca isi sumber dan merekam prosedurnya. Apabila publikasi tidak dapat diakses atau klaim tidak dapat diperiksa, status tetap `needs_verification` dan naskah tidak boleh final.

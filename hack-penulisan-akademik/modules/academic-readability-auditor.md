# Academic Readability Auditor (READ)

**Tujuan:** mengurangi ambiguitas, pemborosan, dan kalimat yang terlalu padat tanpa merusak ketepatan metodologis.

## Prosedur
- Periksa keberadaan subjek, predikat, rujukan kata tunjuk, urutan informasi, hubungan antarparagraf, dan keselarasan istilah.
- Untuk kalimat sangat panjang (indikasi >48 token) dan paragraf padat (>175 token), evaluasi kebutuhan pemisahan berdasarkan makna, bukan angka semata.
- Periksa EYD V, KBBI, dan TBBBI; koreksi imbuhan, kata depan, konjungsi, tanda baca dan penggunaan istilah asing jika benar-benar salah.
- Lindungi notasi matematis, kode, identitas sumber, istilah keilmuan, dan kutipan langsung dari perubahan otomatis.

**Automasi:** `READ-001` paragraf padat; `READ-002` kalimat panjang. Ambang hanya heuristik untuk antrean editor, bukan hukum EYD maupun kriteria kelulusan.
**Tinjauan:** catat bukti lokasi dan alasan revisi. Gunakan `quality-review-add --domain readability` setelah diperiksa manusia.

**Acuan normatif:** https://ejaan.kemendikdasmen.go.id/ dan https://kbbi.kemendikdasmen.go.id/

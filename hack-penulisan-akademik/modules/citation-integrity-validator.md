# Citation Integrity Validator (CIV)

**Tujuan:** memastikan setiap gagasan atau temuan eksternal diberi atribusi dan klaim tidak melampaui dukungan referensi.

## Pemeriksaan wajib
1. Setiap ID sitasi `[cite:SRC-nnn]` harus ada dalam `registry/sources.json` dan memiliki metadata dapat dilacak.
2. Baca **teks lengkap** yang relevan; validasi nama penulis, tahun, judul, penerbit/jurnal, DOI/URL, konteks, metode, dan batasan.
3. Untuk setiap klaim faktual penting, catat **kalimat klaim**, `source_locator` (halaman atau seksi), cuplikan pendek bila diperbolehkan, status `supported` / `uncertain` / `contradicted`.
4. Pastikan sumber primer dan angka tidak dipelintir. Jika hanya abstrak yang tersedia, jangan menyatakan verifikasi teks lengkap.
5. Gunakan APA 7 bila diwajibkan; pedoman institusi mengatur konflik format, bukan membolehkan sitasi fiktif.

**Automasi:** CLI memeriksa keberadaan ID, metadata, checksum, dan ada/tidaknya *review* sumber per bab. CLI **tidak dapat membuktikan** kesesuaian klaim dengan isi jurnal. Verifikasi manual per klaim tetap wajib meskipun rekam `citation-review-add` sudah ada.
**Kode:** `CIV-001` ID hilang; `CIV-002` review belum tercatat; `CIV-003` review tidak mendukung atau kedaluwarsa. Review lama untuk klaim yang sama dapat diganti dengan catatan baru, tanpa menghapus audit trail.

**Dasar:** https://apastyle.apa.org/style-grammar-guidelines/citations dan https://apastyle.apa.org/instructional-aids/in-text-citation-checklist.pdf

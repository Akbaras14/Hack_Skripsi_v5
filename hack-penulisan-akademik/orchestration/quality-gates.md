# Quality Gate Skripsi

## Mesin cek struktural (otomatis)
- Profil minimal, pertanyaan dan tujuan, metode, objek, pemetaan Q→O→metode→hasil.
- Lima berkas bab, heading dan konten nyata, tanpa placeholder pada mode review/final.
- Semua `[cite:SRC-nnn]` merujuk sumber terdaftar dan sudah diperiksa full text untuk review/final.
- Semua `[claim:CLM-nnn]` merujuk klaim terdaftar; semua klaim didukung sumber/bukti dengan referensi valid.
- Berkas bukti ada, hash cocok, dan izin tidak `pending`; hasil memerlukan klaim berjenis `result` dengan bukti.
- Kelengkapan metadata sumber; daftar pustaka dibentuk dari sumber yang benar-benar digunakan.
- Mode final: bukti persetujuan peneliti dan pembimbing (dengan path file yang dicek hash), serta deklarasi telaah format visual.

## Gerbang manual (tidak dapat dipastikan dari skrip)
- Validitas dan kualitas metodologi, representativitas dataset, etika dan izin penelitian.
- Konten PDF jurnal dan kesesuaian klaim-sitasi serta nomor halaman kutipan langsung.
- EYD V, KBBI, TBBBI, APA 7 secara menyeluruh, ketepatan istilah dan parafrase substantif.
- Konsistensi hasil numerik dengan perhitungan asli, tidak hanya keberadaan CSV.
- Pemeriksaan tampilan setiap halaman DOCX/PDF dan kesesuaian template kampus.
- Keaslian persetujuan dan keabsahan tanda tangan. File persetujuan terlampir bukan validasi autentikasi.

## Status
`DRAFT` = naskah dapat berkembang; `TERHALANG_BUKTI` = tidak dapat dinyatakan lengkap; `PERLU_REVISI` = masalah dalam bagian tersedia; `SIAP_DITINJAU` = lolos cek struktural review dan wajib telaah manual; `FINAL_DISETUJUI` = hanya diadministrasikan setelah audit manual dan persetujuan sah dinyatakan dengan bukti. Jangan klaim kelulusan skripsi.

## Gate tambahan v5.0

- Diagnostic CLI `quality-audit` mengeluarkan temuan HAW, CIV, PAT, OCV, READ; kategori INFO/REVIEW bukan vonis plagiarisme/AI.
- Untuk final administratif, wajib ada review manual dengan keputusan `approved` pada lima domain dan fingerprint cocok dengan naskah terbaru.
- Sitasi per pasangan bab–sumber memerlukan catatan pemeriksaan; ini tidak menggantikan pemeriksaan manual **setiap** klaim.
- Kontribusi perlu jejak EVD dan relasi pertanyaan penelitian, bukan klaim kebaruan otomatis.
- `turnitin-interpret` tidak termasuk gerbang wajib dan tidak menentukan lulus.
- Persetujuan pengguna serta metadata input bisa keliru; tidak menjamin kebenaran bukti atau autentisitas institusional.

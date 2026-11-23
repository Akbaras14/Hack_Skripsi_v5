# Human Academic Writing Quality (HAW)

**Tujuan:** memperkuat kejelasan tulisan, konsistensi sudut pandang, penguasaan istilah, argumentasi, dan hubungan klaim dengan penelitian nyata; **bukan menyamarkan penggunaan AI**.

## Prosedur agen
1. Pastikan setiap paragraf menyumbang definisi, bukti, pembandingan, analisis, atau implikasi yang berhubungan dengan masalah penelitian.
2. Bandingkan pembukaan dan penutup paragraf; tandai kalimat generik, frasa klise, redundansi, dan perpindahan topik tidak logis.
3. Konfirmasi secara manual alasan memilih diksi, istilah teknis, dan pernyataan kausal. Jangan mengubah gaya hanya agar tidak terdeteksi AI.
4. Bedakan tulisan peneliti, kutipan langsung, parafrase, tabel, kode, dan contoh. Jangan ubah kutipan verbatim.
5. Catat temuan yang memiliki kutipan/lokasi; kesimpulan hanya terkait **mutu editorial**, bukan identitas penulis.

**Automasi:** `quality-audit` memberi peringatan `HAW-001`/`HAW-002`. Metode ini bukan analisis kepengarangan atau model ML.
**Sign-off:** `quality-review-add --domain human_writing ...` setelah tinjauan manual terdokumentasi; berlaku hanya untuk hash naskah saat dicatat.

**Contoh:** Alih-alih "teknologi memiliki peranan yang sangat penting dalam berbagai aspek", jelaskan teknologi spesifik, masalah nyata, dampak terukur dan sumber yang mendukung.

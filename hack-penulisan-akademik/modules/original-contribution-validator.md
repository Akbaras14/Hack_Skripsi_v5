# Original Contribution Validator (OCV)

**Tujuan:** meminta peneliti menjelaskan kontribusi yang dapat diperiksa, bukan memaksa klaim "pertama di dunia" atau kebaruan palsu.

## Pemetaan substantif
1. Kaitkan kontribusi dengan satu rumusan masalah `Q`, metode yang benar-benar dipakai, dan bukti `EVD`.
2. Bedakan kontribusi artefak perangkat lunak, validasi empiris, replikasi terkontrol, perbandingan metode, atau analisis baru.
3. Bandingkan dengan studi terdahulu dan jelaskan **apa yang sama, berbeda, alasan perbedaannya, dan batasannya**.
4. Untuk Bab IV, pastikan eksperimen benar-benar telah dijalankan; untuk Bab V, kesimpulan hanya berasal dari hasil teruji.
5. Bukti sintetis hanya untuk tes perangkat lunak; tidak boleh dipakai sebagai bukti skripsi final.

**Automasi:** `contribution-add` menolak status `supported` tanpa `evidence_ids` yang telah didaftarkan dan `question_id` yang ada. Audit memeriksa adanya entri, bukan menilai kebaruan ilmiah.
**Kode:** `OCV-001` belum ada kontribusi didukung; `OCV-002` pembeda dan batasan belum lengkap.

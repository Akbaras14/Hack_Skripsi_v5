# Research Agent — manajemen sumber, bukti, dan metodologi

## Input
`project.json`, pertanyaan riset, arahan pembimbing, dokumen pedoman kampus, hasil penelusuran literatur, bukti penelitian pengguna. Jangan menganggap metadata contoh sebagai penelitian yang nyata.

## Langkah
1. Definisikan objek/unit analisis, tujuan, pertanyaan, metode, batasan dan rencana instrumentasi; simpan di `project.json`.
2. Daftarkan sumber dengan `source-add` atau secara terstruktur dalam `registry/sources.json`. Catat metadata asli, DOI/URL, dan **status pemeriksaan**: `not_accessed`, `abstract_checked`, atau `fulltext_checked`. Status fulltext hanya boleh diberikan jika sumber benar-benar dibaca; catat `verification_note` dan `metadata_checked`. Periksa resolusi DOI melalui kanal yang tersedia; CLI offline **tidak** membuktikan DOI valid secara eksternal.
3. Daftarkan dokumen/dataset/log/hasil uji sebagai bukti melalui `evidence-add`; skrip menghitung SHA-256. Catat sumber, izin, sensitivitas, dan prosedur pengumpulan. Jangan menyisipkan berkas rahasia perusahaan ke dokumen final tanpa otorisasi.
4. Susun matriks `question_id → objective_id → method → result_claim_ids` dan `claim_id → source_ids/evidence_ids`. Bedakan laporan observasi, inferensi, dan asumsi.
5. Buat daftar kekosongan bukti. Bila belum ada hasil penelitian, Bab IV wajib tetap draf dengan status `BELUM_ADA_BUKTI`.

## Keluaran
- `registry/sources.json`: bibliografi dan status pemeriksaan
- `registry/evidence.json`: daftar bukti dan hash
- `registry/claims.json`: keterlacakan klaim
- `project.json`: kontrak penelitian
- `state.json` dan `logs/decisions.jsonl`: keputusan yang dapat dilacak

## Larangan
Tidak membuat hasil penelitian, DOI, nomor halaman, wawancara, izin, referensi, atau tingkat keparahan sebagai fakta tanpa bukti. Jangan melabeli klaim penelitian sebagai terkonfirmasi hanya karena terlihat masuk akal.

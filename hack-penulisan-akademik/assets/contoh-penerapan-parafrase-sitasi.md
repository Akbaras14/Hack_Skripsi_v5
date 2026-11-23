# Skenario Pelatihan: Parafrase, Sitasi, dan Revisi

> Semua contoh pada berkas ini **ilustrasi buatan** untuk menguji agen, bukan temuan penelitian atau referensi nyata.

## Skenario 1 — *Patchwriting*

**Sumber simulasi:** "Survei terhadap 40 peserta menemukan adanya keterkaitan antara intensitas latihan dan hasil tes pada kelas yang diamati."

**Buruk:** "Survei pada 40 orang mendapati hubungan antara tingkat latihan dan nilai ujian di kelas yang ditinjau."  
**Masalah:** hanya mengganti sinonim serta mempertahankan struktur proposisi tanpa dukungan atribusi.  
**Respons yang diminta:** pahami informasi, ubah fokus kalimat jika tepat, lalu berikan sitasi **hanya jika sumber bibliografi tersedia**; pertahankan jumlah 40, status hubungan, dan konteks satu kelas. Jangan memberikan sitasi fiktif.

## Skenario 2 — Eskalasi kausalitas

**Sumber simulasi:** "Penggunaan perangkat A berkorelasi dengan waktu penyelesaian yang lebih singkat pada sampel uji."  
**Buruk:** "Perangkat A menyebabkan semua pekerjaan selesai lebih cepat."  
**Respons:** koreksi `menyebabkan` menjadi `berkorelasi/berasosiasi`, hilangkan generalisasi, jelaskan batas sampel.

## Skenario 3 — Abstrak saja

**Kondisi:** pengguna memberikan abstrak penelitian tetapi tidak memiliki PDF.  
**Respons:** hanya parafrase temuan yang disebut secara jelas dalam abstrak. Hindari mengklaim telah memeriksa tabel, variabel pengendali, atau diskusi lengkap. Status `ABSTRAK_SAJA`.

## Skenario 4 — Parafrase lintas paragraf

**Kondisi:** satu sumber dibahas selama dua paragraf penuh dengan APA 7.  
**Respons:** sumber yang sama boleh diatribusikan sekali pada awal rangkaian kalimat dalam paragraf pertama selama tidak ambigu. **Pada paragraf kedua perkenalkan kembali sumber**; tambahkan sitasi bila beralih sumber.

## Skenario 5 — DOI tidak cocok

**Kondisi:** DOI pada daftar pustaka menuju artikel berbeda.  
**Respons:** status `TERKONFIRMASI` bila resolusi DOI benar-benar diperiksa. Jika belum ada akses, `PERLU VERIFIKASI`; jangan mengarang DOI pengganti.

# Larangan Pola Tulisan AI dan Kendali Mutu Akademik (LPA-001–LPA-050)

**Modul untuk:** `hack-penulisan-akademik` (Hack Skripsi)  
**Versi modul:** 1.0.0  
**Bahasa:** Indonesia  
**Cakupan:** skripsi, tesis, artikel jurnal, laporan penelitian, makalah, proposal akademik  
**Jenis:** overlay pengendalian mutu yang memetakan temuan literatur ke aturan `HP`, `P`, dan `S` yang sudah ada.

## Tujuan, batasan, dan prinsip pembacaan

Modul ini menerjemahkan ciri yang sering didiskusikan terkait teks AI menjadi **larangan atas kelemahan kualitas akademik**, bukan larangan terhadap gaya penulisan manusia dan bukan pendeteksi kepengarangan. Semua aturan dibaca secara kontekstual, proporsional, dan berbasis bukti. **Kerapian bahasa, pilihan kata formal, repetisi yang sah, istilah teknis, skor detektor, Markdown yang memang dibutuhkan, atau penggunaan AI yang diizinkan tidak otomatis merupakan kesalahan.**

- **Jangan mengklaim:** naskah pasti ditulis AI, naskah pasti ditulis manusia, lolos AI detector, lolos Turnitin, atau memenuhi kebijakan universitas tertentu tanpa memeriksanya.
- **Jangan membuat kesalahan buatan:** typo, sinonim tidak alami, angka acak, susunan kalimat janggal, atau variasi yang sengaja diciptakan untuk mengelabui alat.
- **Kecualikan secara eksplisit:** kutipan langsung, definisi baku, format tabel, terminologi teknis, transisi akademik yang tepat, gaya selingkung, dan contoh output AI yang menjadi data penelitian.
- **Status bukti:** `TERKONFIRMASI` jika masalah dapat ditunjukkan pada lokasi dan bukti; `PERLU VERIFIKASI` jika memerlukan sumber/artefak; `TIDAK DITEMUKAN` hanya untuk bagian yang diperiksa; `TIDAK DAPAT DINILAI` jika materi tidak tersedia.
- **Sumber bukti:** jurnal empiris dan dokumen primer untuk klaim ilmiah; Wikipedia dan media hanya sebagai konteks, bukan sebagai bukti eksperimen. Daftar di bawah tidak berarti setiap aturan adalah fitur deteksi yang tervalidasi secara independen.

## Prioritas dan konsekuensi

| Prioritas | Cakupan | Aturan keputusan |
|---|---|---|
| P0 — Kritis | Fabrikasi, referensi fiktif, data palsu, kebohongan proses, sitasi menyesatkan yang terverifikasi | **Blokir FINALISASI** sampai diperbaiki atau secara eksplisit dinyatakan belum dapat diselesaikan |
| P1 — Tinggi | Klaim di luar metode, generalisasi, kausalitas palsu, kontradiksi metodologis | Wajib koreksi substansi sebelum final |
| P2 — Sedang | Argumen umum, struktur tidak logis, konteks dan definisi lemah | Revisi bagian yang berdampak nyata pada pemahaman |
| P3 — Rendah | Repetisi retoris, transisi berlebihan, pilihan kata, format tidak relevan | Perbaiki hanya bila mutu meningkat; jangan menghukum gaya sah |

## Alur kerja wajib

1. **Saat TULIS:** buat peta `pertanyaan → klaim → bukti → penalaran → batasan → sitasi` sebelum menulis tiap subbagian substansial.
2. **Saat REVISI/PARAFRASE:** pertahankan arti sumber, istilah teknis, angka, hubungan sebab-akibat, batasan; ubah hanya kelemahan terlokalisasi.
3. **Saat SITASI:** verifikasi metadata, keberadaan sumber, dan apakah isi sumber mendukung proposisi yang dikutip.
4. **Saat AUDIT:** baca seluruh LPA-001–050 bersama HP-001–060 dan P/S-001–060; tunjukkan lokasi tepat, kutipan, status bukti, dampak, perbaikan, tanpa persentase kepengarangan.
5. **Saat FINALISASI:** hentikan jika ada fabrikasi yang sudah terbukti; jangan menyembunyikan sumber atau hasil yang belum diperiksa. Status yang disarankan: `LAYAK DITINJAU`, `PERLU REVISI`, `TERHALANG BUKTI`.

## Katalog larangan


### A. Bahasa, sintaksis, dan pilihan kata


**LPA-001 — Repetisi pola kalimat**  
- **Larangan:** DILARANG mempertahankan pola sintaksis identik yang berulang dan membuat penjelasan monoton.
- **Periksa:** Bandingkan susunan klausa pada beberapa paragraf sejenis.
- **Tindakan:** Variasikan struktur hanya jika memperjelas hubungan gagasan.
- **Pemetaan aturan lama:** `HP-001, HP-003`.


**LPA-002 — Panjang kalimat seragam**  
- **Larangan:** DILARANG memaksakan semua kalimat ke panjang atau irama yang hampir sama bila mengurangi keterbacaan.
- **Periksa:** Amati variasi panjang dan fungsi kalimat, bukan angka universal.
- **Tindakan:** Sesuaikan panjang kalimat dengan kompleksitas gagasan.
- **Pemetaan aturan lama:** `HP-002, HP-003`.


**LPA-003 — Pembuka paragraf formulaik**  
- **Larangan:** DILARANG membuka banyak paragraf dengan pola atau frasa identik tanpa alasan organisasi naskah.
- **Periksa:** Tinjau kalimat pertama 5–10 paragraf yang berurutan.
- **Tindakan:** Mulai paragraf dari proposisi atau bukti yang memang dibahas.
- **Pemetaan aturan lama:** `HP-006`.


**LPA-004 — Penutup paragraf klise**  
- **Larangan:** DILARANG menutup setiap paragraf dengan pernyataan umum yang tidak menambah inferensi.
- **Periksa:** Tandai kalimat akhir yang hanya mengulang pembuka.
- **Tindakan:** Tutup dengan implikasi yang benar-benar mengikuti isi.
- **Pemetaan aturan lama:** `HP-007, HP-029`.


**LPA-005 — Penanda wacana mekanis**  
- **Larangan:** DILARANG menambahkan “selain itu”, “lebih lanjut”, atau “dengan demikian” ketika hubungan logisnya tidak nyata.
- **Periksa:** Periksa apakah penanda menyatakan tambahan, kontras, sebab, atau kesimpulan yang benar.
- **Tindakan:** Hapus atau ganti dengan transisi yang sesuai hubungan bukti.
- **Pemetaan aturan lama:** `HP-004, HP-023`.


**LPA-006 — Redundansi semantis**  
- **Larangan:** DILARANG menulis beberapa kalimat yang hanya mengulang makna dengan sinonim tanpa informasi baru.
- **Periksa:** Petakan proposisi tiap kalimat; identifikasi duplikasi.
- **Tindakan:** Gabungkan klaim dan tambahkan analisis atau data baru hanya jika tersedia.
- **Pemetaan aturan lama:** `HP-005`.


**LPA-007 — Konstruksi retoris formulaik**  
- **Larangan:** DILARANG memaksakan pola “bukan X, melainkan Y” atau daftar tiga unsur berulang untuk setiap bahasan.
- **Periksa:** Periksa fungsi argumentatif pola kontras dan triad.
- **Tindakan:** Gunakan hanya saat benar-benar membantu perbandingan.
- **Pemetaan aturan lama:** `HP-010, HP-018`.


**LPA-008 — Kosakata abstrak kosong**  
- **Larangan:** DILARANG menggunakan istilah seperti “transformasi”, “optimalisasi”, atau “komprehensif” tanpa makna operasional.
- **Periksa:** Periksa definisi, ukuran, dan contoh kontekstual setiap istilah abstrak kunci.
- **Tindakan:** Definisikan variabel atau jelaskan mekanisme konkret.
- **Pemetaan aturan lama:** `HP-012, HP-013`.


**LPA-009 — Penekanan signifikansi berlebihan**  
- **Larangan:** DILARANG menyebut topik “sangat krusial”, “revolusioner”, atau “berdampak besar” tanpa pembuktian.
- **Periksa:** Cari klaim urgensi yang tidak diikuti data atau landasan teori.
- **Tindakan:** Tulis urgensi yang spesifik pada masalah, populasi, dan bukti.
- **Pemetaan aturan lama:** `HP-014`.


**LPA-010 — Penggunaan sinonim tidak akurat**  
- **Larangan:** DILARANG mengganti istilah teknis demi variasi sehingga maknanya berubah; dilarang pula hiperkoreksi yang mengganggu ketepatan.
- **Periksa:** Cocokkan sinonim dengan definisi bidang ilmu dan sumber primer.
- **Tindakan:** Konsisten gunakan istilah teknis yang tepat.
- **Pemetaan aturan lama:** `HP-017, HP-020, HP-048`.


### B. Paragraf, organisasi, dan wacana


**LPA-011 — Pendahuluan generik**  
- **Larangan:** DILARANG memperpanjang latar belakang dengan definisi atau sejarah yang tidak mengarah ke persoalan penelitian.
- **Periksa:** Uji kontribusi setiap paragraf pada gap, objek, atau tujuan penelitian.
- **Tindakan:** Susun konteks → bukti masalah → gap → tujuan.
- **Pemetaan aturan lama:** `HP-022`.


**LPA-012 — Paragraf templatis**  
- **Larangan:** DILARANG memakai pola pembuka–uraian–simpulan seragam jika tidak sesuai kebutuhan argumentasi.
- **Periksa:** Bandingkan fungsi dan alur beberapa paragraf.
- **Tindakan:** Susun berdasarkan klaim, bukti, dan analisis yang diperlukan.
- **Pemetaan aturan lama:** `HP-021, HP-030`.


**LPA-013 — Daftar menggantikan analisis**  
- **Larangan:** DILARANG mengganti pembahasan substantif dengan poin atau subjudul tanpa penjelasan dan sintesis.
- **Periksa:** Periksa apakah tiap daftar menjelaskan hubungan atau sekadar inventaris.
- **Tindakan:** Tambahkan narasi analitis dengan rujukan terkait.
- **Pemetaan aturan lama:** `HP-026`.


**LPA-014 — Judul tidak sesuai isi**  
- **Larangan:** DILARANG membuat subbab dengan isi tidak menjawab subjudul, pertanyaan, atau tujuan.
- **Periksa:** Bandingkan setiap subjudul dengan proposisi utama paragraf.
- **Tindakan:** Pindahkan, ringkas, atau perbaiki cakupan pembahasannya.
- **Pemetaan aturan lama:** `HP-028`.


**LPA-015 — Transisi artifisial**  
- **Larangan:** DILARANG berpindah topik memakai kata penghubung dekoratif yang menyamarkan lompatan logika.
- **Periksa:** Uji apakah kesimpulan paragraf sebelumnya relevan ke klaim berikutnya.
- **Tindakan:** Nyatakan jembatan konsep atau atur ulang urutan paragraf.
- **Pemetaan aturan lama:** `HP-023, HP-027`.


**LPA-016 — Kesimpulan berulang**  
- **Larangan:** DILARANG mengulang seluruh uraian dalam simpulan tanpa sintesis yang menjawab pertanyaan penelitian.
- **Periksa:** Cocokkan tiap kalimat simpulan dengan hasil dan kontribusinya.
- **Tindakan:** Tulis jawaban, dukungan data, keterbatasan, dan implikasi sesuai bukti.
- **Pemetaan aturan lama:** `HP-024`.


**LPA-017 — Duplikasi penjelasan**  
- **Larangan:** DILARANG menyalin kembali bagian definisi atau konteks yang sudah lengkap tanpa kebutuhan analitis.
- **Periksa:** Temukan paragraf dengan substansi identik antarbagian.
- **Tindakan:** Pakai rujukan silang atau ringkasan proporsional.
- **Pemetaan aturan lama:** `HP-025`.


**LPA-018 — Hilangnya konteks objek**  
- **Larangan:** DILARANG membuat uraian yang dapat dipasang ke penelitian apa pun tanpa menunjukkan kaitan ke objek dan masalah yang diteliti.
- **Periksa:** Cari nama objek, ruang lingkup, data, dan kaitan teori dengan penelitian.
- **Tindakan:** Tambahkan konteks yang benar-benar tersedia; tandai jika data belum tersedia.
- **Pemetaan aturan lama:** `HP-011, HP-031, HP-049`.


### C. Argumentasi dan integritas penalaran


**LPA-019 — Klaim tanpa bukti**  
- **Larangan:** DILARANG menyatakan hasil atau fakta empiris tanpa rujukan atau data yang dapat ditelusuri.
- **Periksa:** Identifikasi kalimat faktual dan cari bukti primernya.
- **Tindakan:** Tambahkan sumber asli yang sudah diperiksa atau ubah klaim menjadi pertanyaan/asumsi.
- **Pemetaan aturan lama:** `HP-033`.


**LPA-020 — Generalisasi di luar sampel**  
- **Larangan:** DILARANG menyimpulkan karakter semua populasi dari sampel kecil atau kasus terbatas.
- **Periksa:** Cocokkan populasi, sampel, konteks, dan bahasa kesimpulan.
- **Tindakan:** Batasi simpulan pada data dan kondisi pengamatan.
- **Pemetaan aturan lama:** `HP-032`.


**LPA-021 — Kontribusi atau kebaruan palsu**  
- **Larangan:** DILARANG mengklaim metode, aplikasi, atau topik pertama di dunia tanpa penelusuran literatur yang memadai.
- **Periksa:** Periksa penelitian pembanding, cakupan, tahun, dan kontribusi nyata.
- **Tindakan:** Nyatakan kebaruan pada perbedaan yang dibuktikan.
- **Pemetaan aturan lama:** `HP-031, HP-033`.


**LPA-022 — Tinjauan pustaka satu sisi**  
- **Larangan:** DILARANG hanya mengutip temuan yang sejalan sambil menghilangkan keterbatasan atau hasil yang bertentangan ketika relevan.
- **Periksa:** Periksa cakupan studi pembanding dan batasan masing-masing.
- **Tindakan:** Sintesis persamaan, perbedaan, dan keterbatasan dengan proporsional.
- **Pemetaan aturan lama:** `HP-019, HP-038`.


**LPA-023 — Definisi tanpa analisis**  
- **Larangan:** DILARANG menjadikan Bab II hanya kumpulan definisi tanpa menjelaskan kaitannya dengan rumusan masalah.
- **Periksa:** Uji adanya perbandingan, sintesis, atau model konseptual.
- **Tindakan:** Tambahkan analisis berbasis studi yang dibaca.
- **Pemetaan aturan lama:** `HP-034`.


**LPA-024 — Kausalitas yang tidak diuji**  
- **Larangan:** DILARANG menulis “menyebabkan”, “membuktikan”, atau “akibat” ketika desain hanya menunjukkan korelasi atau deskripsi.
- **Periksa:** Periksa rancangan uji dan bukti hubungan sebab-akibat.
- **Tindakan:** Pilih bahasa “berhubungan”, “berasosiasi”, atau “diduga” sesuai desain.
- **Pemetaan aturan lama:** `HP-009, HP-037`.


**LPA-025 — Kontradiksi konsep**  
- **Larangan:** DILARANG menggunakan istilah atau definisi yang berubah antarbab tanpa penjelasan.
- **Periksa:** Bandingkan definisi variabel, indikator, dan klaim pada seluruh dokumen.
- **Tindakan:** Tetapkan definisi operasional konsisten atau jelaskan perubahannya.
- **Pemetaan aturan lama:** `HP-035, HP-053`.


**LPA-026 — Keterbatasan disembunyikan**  
- **Larangan:** DILARANG menyajikan hasil sebagai berlaku umum tanpa menyebut batasan data, alat, sampel, dan metode yang relevan.
- **Periksa:** Cari keterbatasan sampel, validitas, dan kondisi pengujian.
- **Tindakan:** Nyatakan keterbatasan yang benar-benar terjadi, tanpa merekayasa.
- **Pemetaan aturan lama:** `HP-038`.


**LPA-027 — Simpulan tautologis**  
- **Larangan:** DILARANG menyimpulkan “hasil membuktikan penelitian berhasil” tanpa indikator, nilai, atau bukti yang jelas.
- **Periksa:** Tautkan setiap simpulan dengan rumusan masalah dan tabel/hasil.
- **Tindakan:** Nyatakan capaian berdasarkan metrik yang benar-benar diukur.
- **Pemetaan aturan lama:** `HP-031, HP-054`.


### D. Sitasi, referensi, dan kebenaran fakta


**LPA-028 — Referensi fiktif**  
- **Larangan:** DILARANG membuat jurnal, judul, penulis, penerbit, ataupun tautan yang tidak dapat ditemukan di sumber tepercaya.
- **Periksa:** Telusuri penerbit, jurnal, indeks, atau dokumen asli.
- **Tindakan:** Hapus klaim referensi palsu; cari sumber nyata yang relevan.
- **Pemetaan aturan lama:** `HP-039`.


**LPA-029 — DOI tidak cocok**  
- **Larangan:** DILARANG memasangkan DOI ke artikel yang tidak sesuai dengan judul dan penulisnya.
- **Periksa:** Resolusi DOI dan bandingkan metadata publikasi.
- **Tindakan:** Perbaiki ke DOI yang terkonfirmasi atau hilangkan bila tidak ada.
- **Pemetaan aturan lama:** `HP-040`.


**LPA-030 — Metadata bibliografi tidak akurat**  
- **Larangan:** DILARANG mengarang tahun, volume, nomor, halaman, atau identitas penulis.
- **Periksa:** Cocokkan seluruh metadata ke PDF atau penerbit.
- **Tindakan:** Pertahankan hanya informasi yang terverifikasi.
- **Pemetaan aturan lama:** `HP-041, HP-042, HP-043`.


**LPA-031 — Kutipan langsung direkayasa**  
- **Larangan:** DILARANG menulis teks berformat kutipan langsung yang tidak ada dalam sumber asli.
- **Periksa:** Cocokkan kata demi kata serta lokasi kutipan.
- **Tindakan:** Parafrase jujur dengan sitasi tepat jika kutipan langsung tidak tersedia.
- **Pemetaan aturan lama:** `HP-044`.


**LPA-032 — Sitasi tidak mendukung klaim**  
- **Larangan:** DILARANG menempel sitasi yang membahas hal lain untuk memberi kesan klaim didukung.
- **Periksa:** Bandingkan proposisi dengan hasil dan batasan sumber.
- **Tindakan:** Perbaiki klaim atau ganti dengan sumber relevan yang benar-benar dibaca.
- **Pemetaan aturan lama:** `HP-045`.


**LPA-033 — Mengaku telah membaca sumber**  
- **Larangan:** DILARANG mengklaim sudah memeriksa teks lengkap, data, atau PDF hanya berdasarkan abstrak atau cuplikan.
- **Periksa:** Catat level akses: metadata, abstrak, teks lengkap, data mentah.
- **Tindakan:** Sampaikan lingkup verifikasi secara eksplisit.
- **Pemetaan aturan lama:** `HP-060`.


**LPA-034 — Angka tanpa asal**  
- **Larangan:** DILARANG mencantumkan persentase, sampel, nilai uji, atau statistik tanpa asal data dan cara perhitungan.
- **Periksa:** Telusuri angka ke tabel, dataset, atau penelitian.
- **Tindakan:** Verifikasi perhitungan atau beri status belum teruji.
- **Pemetaan aturan lama:** `HP-046`.


**LPA-035 — Informasi versi/standar usang**  
- **Larangan:** DILARANG mengutip standar, peraturan, atau teknologi seolah masih berlaku tanpa memeriksa tanggal dan versinya.
- **Periksa:** Periksa tanggal publikasi, versi, dan tanggal berlaku.
- **Tindakan:** Perbarui dengan sumber resmi atau jelaskan konteks historisnya.
- **Pemetaan aturan lama:** `HP-047`.


**LPA-036 — Placeholder sitasi**  
- **Larangan:** DILARANG meninggalkan teks seperti “(Nama, Tahun)”, “[perlu jurnal]”, atau DOI contoh dalam naskah final.
- **Periksa:** Cari seluruh placeholder dan sitasi tanpa entri pustaka.
- **Tindakan:** Lengkapi berdasarkan sumber terverifikasi atau pindahkan ke daftar isu.
- **Pemetaan aturan lama:** `HP-057`.


### E. Metodologi dan keterlacakan penelitian


**LPA-037 — Objek penelitian tidak terdefinisi**  
- **Larangan:** DILARANG menulis metode tanpa objek, unit analisis, kriteria inklusi, atau cakupan penelitian yang jelas.
- **Periksa:** Bandingkan tujuan dengan objek dan pengambilan sampel.
- **Tindakan:** Definisikan cakupan aktual dan batasan pemilihan data.
- **Pemetaan aturan lama:** `HP-049`.


**LPA-038 — Metode hanya definisi umum**  
- **Larangan:** DILARANG menuliskan metode tanpa prosedur, parameter, tahapan, instrumen, dan cara evaluasi yang akan diterapkan.
- **Periksa:** Minta urutan kerja yang dapat direplikasi.
- **Tindakan:** Rinci proses nyata atau rencana yang masih akan dilakukan.
- **Pemetaan aturan lama:** `HP-050`.


**LPA-039 — Hasil penelitian dibuat-buat**  
- **Larangan:** DILARANG mengisi Bab IV dengan hasil, wawancara, pengujian, atau eksperimen yang belum dilakukan.
- **Periksa:** Minta artefak uji dan bukti pelaksanaan.
- **Tindakan:** Pisahkan ilustrasi, rencana, dan hasil faktual.
- **Pemetaan aturan lama:** `HP-033, HP-060`.


**LPA-040 — Asal dataset tidak jelas**  
- **Larangan:** DILARANG mengklaim validitas dataset tanpa mencatat sumber, izin, prosedur pengambilan, dan versi data yang relevan.
- **Periksa:** Periksa manifest dataset, log, atau dokumentasi pengumpulan.
- **Tindakan:** Catat provenans yang benar dan batas penggunaannya.
- **Pemetaan aturan lama:** `HP-051`.


**LPA-041 — Kesimpulan di luar metode**  
- **Larangan:** DILARANG mengklaim suatu sistem aman, efektif, atau unggul bila pengujian tidak mengukur klaim tersebut.
- **Periksa:** Bandingkan variabel, instrumen, hasil, dan simpulan.
- **Tindakan:** Batasi klaim pada skenario dan metrik yang diuji.
- **Pemetaan aturan lama:** `HP-052, HP-054`.


### F. Artefak chatbot, format, dan proses penyusunan


**LPA-042 — Sisa instruksi chatbot**  
- **Larangan:** DILARANG membiarkan teks instruksi asisten atau balasan dialog masuk ke naskah final tanpa status kutipan penelitian.
- **Periksa:** Cari instruksi peran, frasa respons chatbot, serta bahasa sapaan asisten.
- **Tindakan:** Hapus artefak nonilmiah atau beri penanda eksplisit jika merupakan objek penelitian.
- **Pemetaan aturan lama:** `HP-055, HP-056`.


**LPA-043 — Placeholder tidak terselesaikan**  
- **Larangan:** DILARANG menyerahkan naskah final dengan TODO, TBD, [masukkan data], atau contoh fiktif sebagai data nyata.
- **Periksa:** Jalankan pencarian placeholder dan periksa semua tabel/gambar.
- **Tindakan:** Selesaikan dengan bukti atau tempatkan pada daftar isu yang belum final.
- **Pemetaan aturan lama:** `HP-057`.


**LPA-044 — Markup keluaran mentah**  
- **Larangan:** DILARANG membiarkan Markdown seperti **tebal**, heading bergaya chatbot, atau karakter escape yang tidak sesuai format dokumen.
- **Periksa:** Periksa markup dan gaya dokumen terhadap pedoman kampus.
- **Tindakan:** Konversi ke format final yang diminta; Markdown sah bila memang format yang dipilih.
- **Pemetaan aturan lama:** `HP-058`.


**LPA-045 — Riwayat proses penelitian palsu**  
- **Larangan:** DILARANG mengklaim telah melakukan revisi, pengujian, observasi, penelusuran, atau wawancara yang tidak pernah dilakukan.
- **Periksa:** Cocokkan dengan log kerja, catatan penelitian, atau versi dokumen.
- **Tindakan:** Nyatakan kegiatan sebagai rencana jika memang belum dilaksanakan.
- **Pemetaan aturan lama:** `HP-060`.


### G. Kehati-hatian deteksi AI dan etika


**LPA-046 — Vonis berdasarkan skor AI detector**  
- **Larangan:** DILARANG menganggap skor AI detector sebagai bukti pasti kepengarangan atau sebagai target agar naskah dinyatakan “manusia”.
- **Periksa:** Catat model, bahasa, panjang naskah, ambang, dan tingkat kesalahannya bila dipakai.
- **Tindakan:** Gunakan hanya sebagai sinyal yang perlu ditinjau bersama bukti substantif.
- **Pemetaan aturan lama:** `HP-059`.


**LPA-047 — Larangan kata/tanda baca universal**  
- **Larangan:** DILARANG menghapus kata seperti “selain itu”, tanda em dash, atau bentuk tiga unsur semata karena dianggap “ciri AI”.
- **Periksa:** Tinjau konteks, norma bahasa, dan fungsi kalimat.
- **Tindakan:** Pertahankan bentuk yang tepat; sunting hanya bila ada masalah kualitas nyata.
- **Pemetaan aturan lama:** `HP-004, HP-010, HP-018`.


**LPA-048 — Manipulasi untuk mengelabui detektor**  
- **Larangan:** DILARANG mengacak struktur, menyisipkan typo, mengubah metrik stilometri, atau memalsukan jejak kerja agar lolos deteksi.
- **Periksa:** Identifikasi revisi yang tidak memperbaiki makna ataupun keterbacaan.
- **Tindakan:** Terapkan penyuntingan berbasis akurasi, bukan target skor.
- **Pemetaan aturan lama:** `HP-001, HP-059`.


**LPA-049 — Parafrase untuk menyamarkan plagiarisme**  
- **Larangan:** DILARANG memparafrase secara mekanis dengan mengganti sinonim sambil mempertahankan ide tanpa atribusi.
- **Periksa:** Bandingkan gagasan, susunan argumen, dan kewajiban sitasi.
- **Tindakan:** Tulis sintesis berdasarkan pemahaman sendiri dengan atribusi sumber.
- **Pemetaan aturan lama:** `P-001–P-025, S-001–S-035`.


**LPA-050 — Menyembunyikan bantuan AI yang wajib diungkap**  
- **Larangan:** DILARANG memberikan pernyataan kepengarangan atau penggunaan AI yang bertentangan dengan fakta dan kebijakan perguruan tinggi/jurnal.
- **Periksa:** Periksa kebijakan institusi dan log penggunaan alat bila tersedia.
- **Tindakan:** Ungkapkan bantuan AI sesuai aturan yang berlaku; jangan mengarang pengakuan.
- **Pemetaan aturan lama:** `HP-060`.


## Kontrak pelaporan audit

Gunakan kolom berikut; satu baris hanya jika benar-benar ditemukan persoalan:

| ID LPA / HP | Bab, halaman, paragraf, kutipan | Kelemahan teramati | Bukti atau sumber pembanding | Status | Prioritas | Koreksi yang menjaga makna |
|---|---|---|---|---|---|---|

**TIDAK BOLEH:** mengubah daftar ciri menjadi skor “AI 87%”, menyamakan plagiarisme dengan penggunaan AI, atau menyatakan ketidaksesuaian karena sebuah kalimat “terlalu sempurna”.

### Gerbang finalisasi (harus terjawab)

- [ ] Seluruh data, kutipan langsung, dan metadata bibliografi yang diklaim benar telah diperiksa atau diidentifikasi sebagai belum diverifikasi.
- [ ] Tidak ada referensi fiktif, angka buatan, atau kegiatan penelitian yang diklaim pernah terjadi padahal belum.
- [ ] Alur rumusan masalah–tujuan–metode–hasil–simpulan konsisten.
- [ ] Setiap temuan kebahasaan disertai lokasi dan alasan dampaknya pada mutu; tidak dipakai untuk vonis AI.
- [ ] Naskah mengikuti gaya selingkung dan kebijakan penggunaan AI yang benar-benar berlaku.
- [ ] Revisi tidak merusak akurasi teknis, sitasi sah, atau makna.

## Basis literatur dan batas interpretasi

Sumber berikut dipakai sebagai titik awal pemetaan indikator, **bukan** klaim bahwa semua 50 aturan telah diuji sebagai pendeteksi tulisan AI:

1. Habiburrahman & Harsono (2026), *Pola Kebahasaan AI Generatif dalam Karya Ilmiah Mahasiswa* — artikel jurnal Indonesia: https://www.online-journal.unja.ac.id/pena/article/view/56207
2. Kobak dkk. (2025), studi pergeseran kosakata dalam abstrak biomedis, *Science Advances* — teks lengkap: https://pmc.ncbi.nlm.nih.gov/articles/PMC12219543/
3. Liang dkk. (2023), *GPT Detectors Are Biased Against Non-Native English Writers*, *Patterns* — teks lengkap: https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961/
4. Wikipedia (panduan komunitas), *Signs of AI Writing* — sumber sekunder, bukan studi eksperimen: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
5. UNESCO (2023), *Guidance for Generative AI in Education and Research* — kebijakan/etika, bukan instrumen deteksi: https://unesdoc.unesco.org/ark:/48223/pf0000386693

**Aturan pemanfaatan referensi:** buka dan baca naskah asli sebelum memasukkannya ke daftar pustaka; cocokkan judul, tahun, penulis, metodologi, dan kesimpulan. Jangan mengekstrapolasi hasil korpus berbahasa Inggris ke seluruh naskah bahasa Indonesia tanpa validasi tambahan. Media massa dan Wikipedia hanya boleh menjadi konteks atau sumber eksplorasi, bukan satu-satunya bukti hipotesis ilmiah.

## Contoh prompt pengguna

```text
Gunakan skill hack-penulisan-akademik mode TULIS untuk Bab II.
Terapkan aturan inti HP, P, S dan seluruh LPA yang relevan.
Tuliskan argumen berbasis bukti; jangan membuat data atau referensi baru.
Jangan mengganti istilah teknis hanya untuk variasi gaya.
```

```text
Audit Bab I–III saya dengan 120 aturan inti dan LPA-001–050.
Laporkan hanya masalah yang didukung kutipan/lokasi, bukti, prioritas, dan revisi.
Jangan memvonis naskah dibuat AI atau menjanjikan kelulusan AI detector.
```

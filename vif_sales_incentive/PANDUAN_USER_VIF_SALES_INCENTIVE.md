# Panduan User — VIF Sales Incentive

Dokumen ini dibuat untuk user operasional seperti Finance, Admin Sales, Manager, dan Salesperson. Bahasa yang digunakan sengaja dibuat sederhana dan berfokus pada cara memakai modul, bukan penjelasan teknis.

---

## 1. Fungsi Modul

Modul **VIF Sales Incentive** digunakan untuk menghitung insentif sales setiap bulan berdasarkan:

- Target sales per cabang dan per individu
- Pencapaian penjualan
- Invoice yang sudah lunas
- Tier pencapaian
- Bonus dari target tambahan
- Branch payout untuk tim cabang
- Kondisi khusus seperti resign, new hire, DP invoice, partial payment, dan refund

Hasil akhir dari modul ini adalah nilai payout yang bisa dicek, disetujui, lalu dikunci oleh Finance/Admin.

---

## 2. Siapa yang Menggunakan Modul Ini?

### Salesperson

Salesperson dapat melihat insentif miliknya sendiri melalui menu **My Incentive**.

### Sales Manager

Sales Manager dapat melihat insentif diri sendiri dan tim/bawahan.

### Finance / Admin Incentive

Finance atau Admin dapat:

- Mengatur target
- Mengatur periode insentif
- Menjalankan perhitungan
- Mengecek hasil payout
- Approve dan lock payout
- Melihat transaksi insentif
- Menangani perubahan karena resign, new hire, refund, dan koreksi

---

## 3. Menu Utama yang Digunakan

Setelah modul terpasang, menu utama yang digunakan adalah **Sales Incentive**.

| Menu | Digunakan Untuk |
|---|---|
| **My Incentive** | Melihat insentif milik user sendiri |
| **Incentive Periods** | Membuat dan menjalankan periode insentif bulanan |
| **Branch Targets** | Mengisi target cabang per bulan |
| **Targets** | Melihat target per karyawan |
| **Cascade Branch Target** | Membagikan target cabang ke masing-masing sales |
| **Payouts** | Melihat hasil insentif yang dihitung |
| **Transactions** | Melihat invoice/retur yang masuk perhitungan |
| **Sales Branches** | Mengatur cabang sales |
| **FTE Designations** | Mengatur bobot role seperti Lead, Team, Support |
| **Rules & Tiers** | Mengatur skema tier dan rate insentif |
| **Refund Policies** | Mengatur kebijakan refund |

---

## 4. Alur Besar Setiap Bulan

Secara sederhana, proses bulanan adalah:

1. Pastikan data karyawan sudah benar
2. Buat atau buka periode insentif bulan tersebut
3. Isi target cabang
4. Jalankan cascade target ke masing-masing sales
5. Pastikan invoice sudah dibuat, diposting, dan status pembayaran benar
6. Jalankan perhitungan insentif
7. Review hasil payout
8. Approve hasil payout
9. Lock periode jika sudah final

Setelah periode di-lock, angka payout tidak bisa diubah lagi.

---

## 5. Setup Karyawan

Sebelum perhitungan insentif dijalankan, setiap karyawan sales harus diisi data insentifnya.

Buka menu **Employees**, pilih karyawan, lalu buka tab **Sales Incentive**.

Isi data berikut:

| Field | Penjelasan |
|---|---|
| **Sales Branch** | Cabang tempat karyawan berada, misalnya Jakarta, Bandung, Surabaya |
| **Business Type** | Pilih B2B atau B2C |
| **FTE Designation** | Pilih role karyawan, misalnya Lead, Team, atau Support |
| **Effective Target Start** | Diisi jika karyawan mulai aktif di tengah bulan |
| **Resignation Date** | Diisi jika karyawan resign |
| **Vacant Position** | Dicentang jika record ini hanya untuk posisi kosong |
| **Global Branch Member** | Dicentang untuk karyawan seperti Pak Kenny yang ikut branch payout di semua cabang |

### Catatan Penting

- Sales harus terhubung ke user Odoo agar dapat melihat menu **My Incentive**.
- Role **Support** tidak mendapat target individual, tetapi tetap bisa mendapat branch payout.
- Karyawan yang sudah resign sebelum periode berjalan tidak ikut perhitungan tim bulan tersebut.
- Jika karyawan resign di tengah bulan, targetnya dihitung prorata sesuai hari aktif.

---

## 6. Role dan FTE

FTE adalah bobot kontribusi orang dalam tim. User cukup memahami bahwa setiap role punya bobot berbeda.

| Role | Bobot untuk Branch | Bobot untuk Individual | Keterangan |
|---|---:|---:|---|
| **Lead** | 1,5 | 1,5 | Lead mendapat bagian lebih besar |
| **Team** | 1,0 | 1,0 | Sales team biasa |
| **Support** | 0,25 | 0 | Support ikut branch payout, tapi tidak punya target individual |

Contoh:

Jika dalam satu tim ada:

- 1 Lead
- 3 Team
- 1 Support

Maka pembagian branch payout akan mengikuti bobot masing-masing role.

---

## 7. Pak Kenny / Global Branch Member

Untuk kebutuhan Pak Kenny, sistem menyediakan pilihan **Global Branch Member** di data karyawan.

Jika field ini dicentang:

- Pak Kenny akan ikut branch payout di setiap cabang
- Pak Kenny ikut untuk B2B dan B2C
- Pak Kenny tidak mendapat target individual dari masing-masing cabang
- Bagian Pak Kenny dihitung dari bobot FTE branch miliknya

Contoh:

Jika Pak Kenny diberi role Lead, maka bobotnya 1,5 untuk branch payout.

---

## 8. Membuat Periode Insentif

Buka menu:

**Sales Incentive → Incentive Periods**

Klik **New**, lalu isi:

| Field | Contoh |
|---|---|
| **Name** | Jan 2026 |
| **Start Date** | 01/01/2026 |
| **End Date** | 31/01/2026 |
| **Rule Version** | Pilih skema insentif yang berlaku |

Setelah selesai, klik **Open**.

Periode harus berstatus **Open** sebelum target dan perhitungan dijalankan.

---

## 9. Mengisi Target Cabang

Buka menu:

**Sales Incentive → Branch Targets**

Buat target untuk setiap kombinasi:

- Periode
- Cabang
- Business Type B2B atau B2C

Contoh:

| Periode | Cabang | Business Type | Target |
|---|---|---|---:|
| Jan 2026 | Jakarta | B2B | 500.000.000 |
| Jan 2026 | Jakarta | B2C | 300.000.000 |
| Jan 2026 | Bandung | B2B | 250.000.000 |

Target cabang ini digunakan untuk:

- Menentukan target per individu
- Menentukan pencapaian branch payout

---

## 10. Membagikan Target Cabang ke Sales

Setelah target cabang dibuat, target tersebut perlu dibagikan ke masing-masing sales.

Buka menu:

**Sales Incentive → Cascade Branch Target**

Isi:

| Field | Penjelasan |
|---|---|
| **Period** | Pilih periode yang sedang dihitung |
| **Branches** | Pilih cabang yang akan diproses |
| **Business Type** | Pilih B2B atau B2C |
| **Scope** | Biasanya pilih Individual Target |
| **Redistribute Vacant Slots** | Centang agar porsi posisi kosong dibagikan ke tim aktif |
| **Overwrite Existing Targets** | Centang jika ingin mengganti target yang sudah ada |

Klik **Preview** untuk melihat hasil pembagian target.

Jika angka sudah benar, klik **Apply**.

Setelah **Apply**, sistem akan membuat target per karyawan.

---

## 11. Cara Membaca Preview Cascade

Di layar preview, user akan melihat beberapa kolom penting:

| Kolom | Arti |
|---|---|
| **Employee** | Nama karyawan |
| **Designation** | Role karyawan |
| **FTE** | Bobot role karyawan |
| **Proration** | Persentase hari aktif dalam bulan tersebut |
| **Base Incentive** | Target dasar dari pembagian target cabang |
| **Carry-Forward** | Tambahan target dari kekurangan bulan sebelumnya |
| **Total Incentive** | Target akhir karyawan |
| **Bonus** | Target bonus dari porsi resign/vacant |

Jika ada karyawan resign atau join di tengah bulan, kolom **Proration** akan kurang dari 100%.

---

## 12. Invoice yang Masuk Perhitungan

Invoice akan masuk perhitungan jika:

- Invoice sudah **Posted**
- Invoice adalah invoice customer
- Invoice memiliki salesperson / incentive salesperson yang benar
- Invoice berada di periode yang sesuai

Namun payout hanya dibayarkan jika invoice sudah **lunas**.

### Partial Payment

Jika invoice baru dibayar sebagian, invoice tersebut belum masuk payout.

Contoh:

- Invoice 100 juta
- Customer baru bayar 50 juta
- Status masih partial

Maka invoice tersebut belum dihitung untuk payout.

Invoice baru dihitung saat sudah lunas.

---

## 13. Down Payment Invoice

Down Payment atau DP memiliki perlakuan khusus.

DP bisa mempengaruhi pencapaian tier di bulan invoice DP dibuat, tetapi DP tidak langsung menghasilkan payout.

Payout baru dihitung saat final invoice sudah dibuat dan invoice tersebut lunas.

Contoh sederhana:

- Order 100 juta
- DP 50 juta dibuat di Januari
- Final invoice dibuat di Februari

Maka:

- DP Januari bisa membantu menentukan tier Januari
- Tetapi payout atas order tersebut dibayarkan saat final invoice lunas
- Payout tidak dihitung dua kali

---

## 14. Diskon Invoice

Baris invoice dengan diskon lebih dari batas yang ditentukan tidak masuk payout.

Saat ini batas diskon adalah **35%**.

Contoh:

| Baris Invoice | Diskon | Masuk Payout? |
|---|---:|---|
| Produk A | 10% | Ya |
| Produk B | 35% | Ya |
| Produk C | 40% | Tidak |

Penting: pengecekan diskon dilakukan per baris invoice, bukan per invoice secara keseluruhan.

---

## 15. Tier Insentif

Tier menentukan rate payout yang digunakan.

Untuk skema 2H, tier umum adalah:

| Pencapaian | Tier | Rate Payout |
|---:|---|---:|
| Kurang dari 75% | Tier 0 | 0% |
| 75% – 84,9% | Tier 1 | 0,30% |
| 85% – 89,9% | Tier 2 | 0,60% |
| 90% – 99,9% | Tier 3 | 0,675% |
| 100% – 109,9% | Tier 4 | 0,75% |
| 110% ke atas | Tier 5 | 0,7875% |

Untuk skema Jan–Jun, aturan flat rate berlaku:

| Pencapaian | Rate |
|---:|---:|
| Kurang dari 75% | 0% |
| 75% ke atas | 0,75% |

---

## 16. Menjalankan Perhitungan Insentif

Setelah target dan invoice siap, buka:

**Sales Incentive → Incentive Periods**

Pilih periode, lalu klik **Calculate**.

Sistem akan menghitung:

- Net sales
- Achievement
- Tier
- Invoice yang eligible
- Invoice yang sudah lunas
- Incentive payout
- Bonus payout
- Branch payout
- Total payout

Setelah selesai, status periode menjadi **Calculated**.

---

## 17. Membaca Hasil Payout

Buka menu:

**Sales Incentive → Payouts**

Kolom penting:

| Kolom | Arti |
|---|---|
| **Employee** | Nama karyawan |
| **Target Incentive** | Target utama karyawan |
| **Target Bonus** | Target bonus jika ada |
| **Net Sales** | Penjualan bersih yang dipakai untuk menentukan tier |
| **Achievement** | Persentase pencapaian terhadap target |
| **Tier** | Tier yang didapat |
| **Incentive Payout** | Total payout incentive dari prior + current |
| **Bonus Payout** | Payout dari target bonus |
| **Branch Payout** | Payout dari pencapaian branch/team |
| **Total Payout** | Total akhir yang dibayarkan |

Rumus sederhananya:

```text
Total Payout = Incentive Payout + Bonus Payout + Branch Payout
```

---

## 18. Penjelasan Komponen Payout

### Incentive Payout

Ini adalah insentif utama sales dari invoice yang eligible dan sudah lunas.

### Bonus Payout

Ini adalah tambahan payout dari bonus target, biasanya berasal dari redistribusi target karena vacant/resign.

### Branch Payout

Ini adalah payout dari pencapaian cabang/tim.

Branch payout bisa diterima oleh:

- Lead
- Team
- Support
- Global Branch Member seperti Pak Kenny

### Total Payout

Ini adalah total keseluruhan yang menjadi nilai payout final.

---

## 19. Approve dan Lock

Setelah payout dicek dan benar, Finance/Admin dapat melanjutkan proses.

### Approve

Klik **Approve** jika hasil sudah disetujui.

Status berubah menjadi **Approved**.

### Lock

Klik **Lock** jika angka sudah final.

Setelah lock:

- Payout tidak bisa dihitung ulang
- Target tidak bisa diubah untuk periode tersebut
- Koreksi harus dilakukan di periode berikutnya

Gunakan **Lock** hanya jika angka benar-benar sudah final.

---

## 20. Jika Ada Karyawan Resign

Jika karyawan resign:

1. Buka data karyawan
2. Isi **Resignation Date**
3. Jalankan ulang **Cascade Branch Target** untuk periode tersebut
4. Review target hasil cascade
5. Klik **Apply**
6. Jalankan **Calculate** ulang

Jika karyawan resign di tengah bulan, targetnya akan dihitung prorata berdasarkan jumlah hari aktif.

Contoh:

Karyawan resign tanggal 20 pada bulan yang memiliki 31 hari.

Maka karyawan tersebut dihitung aktif 20 dari 31 hari.

Sisa target akan dialihkan sesuai aturan redistribusi.

---

## 21. Jika Ada Karyawan Baru

Jika karyawan baru masuk di tengah bulan:

1. Buat atau update data karyawan
2. Isi **Effective Target Start** sesuai tanggal mulai aktif
3. Isi cabang, business type, dan designation
4. Jalankan ulang cascade target
5. Review hasil target prorata
6. Klik **Apply**
7. Jalankan **Calculate** ulang jika diperlukan

Contoh:

Karyawan masuk tanggal 18 Agustus.

Jika Agustus memiliki 31 hari, maka karyawan dihitung aktif 14 hari.

Targetnya akan mengikuti 14/31 dari porsi normal.

---

## 22. Jika Ada Posisi Kosong / Vacant

Jika ada posisi yang belum terisi, user bisa membuat record employee sebagai **Vacant Position**.

Fungsinya agar sistem tahu ada kursi kosong di tim tersebut.

Porsi posisi kosong dapat dialihkan ke tim aktif sebagai bonus jika opsi **Redistribute Vacant Slots** dicentang saat cascade.

---

## 23. Population Changed / Perlu Re-Cascade

Kadang sistem memberi tanda bahwa komposisi tim berubah.

Biasanya terjadi karena:

- Ada karyawan resign
- Ada karyawan baru masuk
- Tanggal join/resign diubah
- Ada orang baru yang belum punya target

Jika muncul tanda seperti ini, jalankan ulang **Cascade Branch Target** terlebih dahulu.

Sistem akan menolak perhitungan jika data tim berubah tetapi target belum diperbarui.

Tujuannya agar payout tidak dihitung dari target lama yang sudah tidak sesuai.

---

## 24. Refund / Retur

Jika ada refund atau credit note, sistem akan mengurangi dasar perhitungan insentif.

User perlu memastikan credit note dibuat dengan benar dari invoice asal.

Jika credit note dibuat dari invoice asal, sistem bisa mengenali hubungan antara invoice dan refund tersebut.

Contoh:

- Invoice 10 juta sudah lunas
- Kemudian dibuat credit note 3 juta
- Maka dasar payout menjadi 7 juta

Jika credit note dibuat manual tanpa hubungan ke invoice asal, user perlu berhati-hati karena sistem mungkin tidak bisa menghubungkan otomatis.

---

## 25. Kasus yang Sering Ditanyakan

### Kenapa payout 0 padahal ada sales?

Kemungkinan penyebab:

- Achievement masih di bawah 75%
- Invoice belum lunas
- Invoice masih partial payment
- Diskon baris invoice lebih dari 35%
- Karyawan belum punya target di periode tersebut
- Salesperson di invoice belum benar

### Kenapa invoice partial tidak masuk payout?

Karena aturan modul hanya membayar invoice yang sudah lunas.

Invoice partial belum dianggap final untuk payout.

### Kenapa DP tidak langsung menghasilkan payout?

Karena DP hanya membantu menentukan tier, bukan dasar payout.

Payout dibayarkan saat final invoice lunas.

### Kenapa perlu lock periode?

Lock digunakan untuk memastikan angka payout final dan tidak berubah lagi.

### Apakah periode yang sudah lock bisa dihitung ulang?

Tidak. Jika ada koreksi setelah lock, koreksi dilakukan di periode berikutnya.

### Kenapa sales tidak bisa melihat My Incentive?

Kemungkinan data employee belum terhubung ke user Odoo.

### Kenapa calculate ditolak?

Kemungkinan:

- Periode belum Open
- Periode sudah Locked
- Ada perubahan tim yang belum di-cascade ulang
- Target belum lengkap

---

## 26. Checklist Sebelum Calculate

Sebelum klik **Calculate**, pastikan:

- Periode sudah Open
- Rule Version sudah dipilih
- Branch Target sudah dibuat
- Target sudah di-cascade dan di-apply
- Data karyawan sudah benar
- Tidak ada warning perubahan tim
- Invoice sudah Posted
- Invoice memiliki salesperson yang benar
- Payment status invoice sudah benar
- Refund/credit note sudah dibuat dengan benar

---

## 27. Checklist Sebelum Lock

Sebelum klik **Lock**, pastikan:

- Semua payout sudah dicek Finance/Admin
- Salesperson dan Manager sudah melakukan review jika diperlukan
- Tidak ada invoice penting yang belum masuk
- Tidak ada refund yang tertinggal
- Tidak ada target yang salah
- Total payout sudah sesuai
- Approval internal sudah selesai

Setelah lock, angka dianggap final.

---

## 28. Ringkasan Proses Cepat

```text
1. Setup karyawan
2. Buat periode
3. Isi branch target
4. Cascade target
5. Pastikan invoice dan pembayaran benar
6. Calculate
7. Review payout
8. Approve
9. Lock
```

---

## 29. Catatan untuk User

- Jangan langsung lock jika angka belum direview.
- Jika ada resign/new hire, selalu lakukan cascade ulang.
- Jika invoice masih partial, jangan berharap payout muncul.
- Jika menggunakan DP, payout baru muncul saat final invoice lunas.
- Jika ada refund, pastikan credit note dibuat dari invoice asal.
- Jika ada perubahan data karyawan, jalankan ulang cascade dan calculate.

---

## 30. Penutup

Modul **VIF Sales Incentive** membantu menghitung insentif dengan lebih rapi, transparan, dan dapat diaudit.

Kunci utama penggunaan modul ini adalah mengikuti urutan proses:

**Target benar → Invoice benar → Payment benar → Calculate → Review → Approve → Lock**

Jika urutan ini diikuti, hasil payout akan lebih mudah diperiksa dan lebih aman untuk digunakan sebagai dasar pembayaran insentif.

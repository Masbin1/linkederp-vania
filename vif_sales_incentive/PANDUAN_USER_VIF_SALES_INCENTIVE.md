# Panduan User — VIF Sales Incentive

Dokumen ini dibuat untuk user operasional seperti Finance, Admin Sales, Manager, dan Salesperson. Bahasa yang digunakan sengaja dibuat sederhana dan berfokus pada cara memakai modul, bukan penjelasan teknis.

---

## 1. Fungsi Modul

Modul **VIF Sales Incentive** digunakan untuk menghitung insentif sales setiap bulan berdasarkan:

- Target sales per cabang dan per individu
- Pencapaian penjualan
- Invoice yang sudah lunas
- Pembagian komisi per **Project** (PM, Salesperson 2, Salesperson 3)
- Transaksi kasir di **Point of Sale (POS)**
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
| **Transactions** | Melihat invoice, transaksi POS, dan retur yang masuk perhitungan |
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
   - Untuk order yang punya project, pastikan orang dan persen komisi di project sudah benar
6. Pastikan sesi POS bulan tersebut sudah ditutup dan kasir di setiap order sudah benar
7. Jalankan perhitungan insentif
8. Review hasil payout
9. Approve hasil payout
10. Lock periode jika sudah final

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
- Semua orang yang bisa mendapat kredit penjualan wajib punya **Sales Branch** dan **Business Type**. Ini termasuk salesperson di invoice, PM / Salesperson 2 / Salesperson 3 di project, dan kasir POS. Jika ada yang kosong, **Calculate** akan ditolak dan menyebutkan nama orangnya (lihat bagian 18).
- Sales yang berjualan di POS wajib memiliki **Sales Branch**. Jika kosong, transaksi POS miliknya tidak akan tercatat di insentif. Setup POS lengkapnya ada di bagian **Transaksi dari POS**.
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
- Invoice memiliki project yang benar (lihat bagian 13), atau jika tanpa project, memiliki salesperson / incentive salesperson yang benar
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

## 13. Pembagian Komisi per Project

Kredit penjualan **tidak otomatis 100% ke salesperson di Sales Order**. Sistem mengecek dulu **Project** yang terpasang di Sales Order.

Jika Sales Order punya project, kredit dibagi ke orang-orang yang ada di project tersebut sesuai persen komisinya.

### 13.1 Data yang Diisi di Project

Buka **Project**, pilih project, lalu isi:

| Field | Penjelasan |
|---|---|
| **Project Manager** | PM project |
| **Salesperson 2** | Sales kedua yang ikut di project |
| **Salesperson 3** | Sales ketiga yang ikut di project |
| **Komisi PM** | Persen bagian PM |
| **Komisi Salesperson 2** | Persen bagian Salesperson 2 |
| **Komisi Salesperson 3** | Persen bagian Salesperson 3 |

Total ketiga persen sebaiknya **100%**.

Setiap orang di project harus memiliki data **Employee** yang terhubung ke user-nya dan sudah diisi tab **Sales Incentive** (lihat bagian 5).

Salesperson 2 dan Salesperson 3 hanya mendapat bagiannya jika:

- sudah punya **Sales Branch** dan **Business Type**, **dan**
- sudah punya **target** di periode invoice tersebut (hasil cascade target).

Jika salah satu belum terpenuhi, bagiannya **dialihkan ke PM** (lihat 13.4).

### 13.2 Contoh

Project **ABORE LIVING**:

| Posisi | Orang | Komisi |
|---|---|---:|
| Project Manager | Agus Dwipayana | 20% |
| Salesperson 2 | Aditya Rachman | 40% |
| Salesperson 3 | Bagus Prasetyo | 40% |

Invoice dari project ini senilai **100 juta**. Maka:

| Orang | Kredit Penjualan |
|---|---:|
| Agus Dwipayana | 20 juta |
| Aditya Rachman | 40 juta |
| Bagus Prasetyo | 40 juta |

Nilai ini dipakai untuk **achievement/tier** dan juga untuk **payout** masing-masing orang.

Jika **Bagus Prasetyo belum punya Sales Branch** (atau belum punya target di periode itu), bagian 40%-nya dialihkan ke PM:

| Orang | Kredit Penjualan |
|---|---:|
| Agus Dwipayana (PM) | 60 juta (20% + 40% dari Bagus) |
| Aditya Rachman | 40 juta |
| Bagus Prasetyo | 0 |

### 13.3 Salesperson di Sales Order Tidak Ada di Project

Jika salesperson di Sales Order **tidak** tercantum di project (bukan PM, bukan Salesperson 2, bukan Salesperson 3), maka **salesperson tersebut tidak mendapat komisi** dari transaksi itu.

Komisinya masuk ke orang-orang yang ada di project.

Jika salesperson tersebut memang ikut menangani project, tambahkan dia di project sebagai Salesperson 2 atau 3, lalu jalankan **Calculate** ulang.

### 13.4 Aturan Khusus

| Kondisi di Project | Hasil |
|---|---|
| Semua persen komisi kosong / 0 | PM mendapat **100%** |
| Persen diisi, tapi orangnya kosong (contoh: Komisi Salesperson 3 = 100% tapi Salesperson 3 kosong) | Porsi tersebut **dialihkan ke PM** |
| Total persen kurang dari 100% | Sisanya **dialihkan ke PM** |
| Total persen lebih dari 100% | Dibagi ulang secara proporsional agar totalnya 100% |
| Satu orang mengisi dua posisi | Persennya dijumlahkan |
| Orang di project tidak punya data Employee | Porsinya dialihkan ke PM |
| Salesperson 2 / 3 belum punya **Sales Branch** atau **Business Type** | Porsinya dialihkan ke PM |
| Salesperson 2 / 3 belum punya **target** di periode invoice | Porsinya dialihkan ke PM |

PM selalu mendapat bagiannya sendiri, walaupun PM belum punya branch atau target. Tetapi PM seperti itu tidak akan menghasilkan payout, dan **Calculate** akan menolak sampai data PM dilengkapi (lihat bagian 18).

### 13.5 Invoice Tanpa Project / Project Tanpa PM

Jika Sales Order tidak punya project (atau invoice dibuat manual, atau invoice dari POS), sistem memakai cara lama:

- **Incentive Salesperson** di invoice mendapat **100%**
- Untuk invoice dari POS, Incentive Salesperson adalah kasirnya (lihat bagian 14)

Cara yang sama juga dipakai jika project **ada**, tetapi tidak ada satu pun orang di project yang bisa menerima kredit. Jika PM kosong, kredit tidak punya tempat untuk dialihkan, sehingga kembali ke Incentive Salesperson di invoice:

| Kondisi Project | Kredit Masuk ke |
|---|---|
| PM, Salesperson 2, Salesperson 3 **semua kosong** | **Incentive Salesperson** invoice 100% |
| PM kosong, Salesperson 2/3 kosong, tetapi persen komisi diisi | **Incentive Salesperson** invoice 100% |
| PM kosong, Salesperson 2 terisi tetapi belum punya **Sales Branch / Business Type** atau **target** | **Incentive Salesperson** invoice 100% |
| PM kosong, Salesperson 2 terisi dan sudah lengkap datanya | **Salesperson 2 100%**. Sisa persen yang biasanya dialihkan ke PM dibagi ulang ke orang yang ada |
| PM terisi, Salesperson 2/3 kosong | **PM 100%**. Salesperson di Sales Order tidak mendapat apa-apa (bagian 13.3) |

Incentive Salesperson di invoice otomatis diisi dari **Salesperson** invoice. Untuk invoice yang dibuat dari Sales Order, orangnya sama dengan salesperson di Sales Order. Jika Salesperson atau Incentive Salesperson di invoice diubah manual, yang mendapat kredit adalah orang yang tertulis di invoice.

Catatan: field **Incentive Salesperson** di invoice hanya berpengaruh untuk invoice **tanpa project**, atau project yang tidak punya orang penerima kredit seperti tabel di atas. Selain itu, pembagian selalu mengikuti data project.

### 13.6 Jika Data Project Diubah

Jika PM, Salesperson 2/3, atau persen komisi di project diubah, atau Sales Branch / target salah satu orangnya baru dilengkapi:

1. Simpan perubahan di project
2. Jalankan **Calculate** ulang di periode yang belum di-Lock

Sistem akan menyesuaikan pembagian dan menghapus kredit orang yang sudah tidak ada di project.

Periode yang sudah di-**Lock** tidak berubah.

### 13.7 Refund / Credit Note pada Invoice Project

Refund dari invoice project juga dibagi dengan persen yang sama.

Contoh: invoice project 100 juta (PM 25%, Salesperson 2 75%) lalu dibuat credit note 10 juta. Maka kredit PM berkurang 2,5 juta dan Salesperson 2 berkurang 7,5 juta.

Pengecekan branch/target untuk credit note memakai **periode invoice asalnya**, bukan periode credit note. Jadi pembagian refund selalu sama dengan pembagian penjualan awalnya.

Saat memakai tombol **Create Credit Note / Refund** dari menu Transactions, nilai yang diisi adalah nilai refund **untuk seluruh baris invoice**, bukan hanya bagian satu orang. Sistem akan membagikannya otomatis.

### 13.8 Cara Mengecek Pembagian

1. Buka **Sales Incentive → Transactions**
2. Gunakan **Group By → Project** untuk melihat transaksi per project
3. Perhatikan kolom:

| Kolom | Arti |
|---|---|
| **Project** | Project asal transaksi |
| **Credit Role** | Posisi orang tersebut: Project Manager, Salesperson 2, Salesperson 3, atau Salesperson / Cashier (jika tanpa project) |
| **Share** | Persen bagian orang tersebut |
| **Line Amount** | Nilai kredit yang sudah dikalikan persen |

Satu baris invoice bisa muncul lebih dari satu kali di menu Transactions, sekali untuk setiap orang di project.

---

## 14. Transaksi dari POS (Point of Sale)

Selain dari Sales Order dan Invoice, penjualan di **POS** juga masuk ke perhitungan insentif.

Bedanya, di POS tidak ada kolom salesperson. Sistem memakai **Cashier (Employee)**, yaitu karyawan yang sedang login di layar kasir saat order dibuat. Karyawan inilah yang mendapat kredit penjualan di insentif.

### 14.1 Setup POS (sekali saja, oleh Admin)

Agar kasir bisa tercatat per karyawan, POS harus memakai login karyawan.

1. Buka **Point of Sale → Configuration → Settings**
2. Pilih POS yang digunakan (misalnya Toko Jakarta)
3. Di bagian **PoS Interface**, centang **Log in with Employees**
4. Klik **Save**, lalu buka halaman ini lagi
5. Tambahkan karyawan sales yang boleh memakai POS tersebut di daftar employee (**Advanced rights**, **Basic rights**, atau **Minimal rights** sesuai kebutuhan)
6. Klik **Save**

Lalu untuk setiap karyawan sales yang berjualan di POS:

1. Buka **Employees**, pilih karyawan
2. Di tab **HR Settings**, isi **PIN Code** (dan/atau **Badge ID**) untuk login di POS
3. Di tab **Sales Incentive**, pastikan **Sales Branch**, **Business Type**, dan **FTE Designation** sudah terisi (sama seperti bagian 5)

> Jika **Log in with Employees** tidak diaktifkan, order POS tidak punya data kasir per karyawan sehingga tidak bisa masuk ke insentif siapa pun.

### 14.2 Cara Berjualan di POS agar Tercatat

1. Buka sesi POS
2. Di layar login POS, sales memilih namanya sendiri lalu memasukkan PIN (atau scan badge)
3. Lakukan transaksi seperti biasa sampai pembayaran selesai
4. Jika sales lain bergantian memakai kasir yang sama, **ganti kasir terlebih dahulu** (klik nama kasir di pojok layar POS → pilih karyawan lain → masukkan PIN)
5. Di akhir hari, tutup sesi POS

Penting: penjualan dicatat atas nama **siapa yang sedang login di kasir**, bukan siapa yang membuka sesi. Jika sales A melayani customer tetapi yang login adalah sales B, maka insentifnya masuk ke sales B.

### 14.3 Order POS yang Masuk Perhitungan

Order POS akan masuk perhitungan jika:

- Order sudah dibayar (status **Paid**, **Posted**, atau **Invoiced**)
- Tanggal order berada di dalam periode insentif
- Order memiliki **Cashier** (employee)
- Cashier tersebut sudah memiliki **Sales Branch**
- Order berasal dari company yang sama dengan periode insentif

Transaksi POS diambil otomatis saat Finance/Admin klik **Calculate** di periode insentif. Tidak ada langkah tambahan.

### 14.4 Perbedaan POS dengan Invoice Biasa

| Hal | Invoice Biasa | POS |
|---|---|---|
| Siapa yang dapat kredit | Salesperson / Incentive Salesperson di invoice | Cashier yang login saat order dibuat |
| Kapan dianggap lunas | Saat invoice sudah lunas | Langsung, karena customer sudah bayar di kasir |
| Periode payout | Periode saat invoice lunas | Periode yang sama dengan tanggal order |
| Partial payment | Belum masuk payout | Tidak ada (POS selalu bayar penuh) |
| Down Payment | Ada perlakuan khusus | Tidak ada DP di POS |
| Batas diskon 35% per baris | Berlaku | Berlaku |

### 14.5 Order POS yang Diminta Invoice

Jika customer minta invoice di POS (tombol **Invoice** saat pembayaran), sistem akan membuat invoice dari order tersebut.

Dalam kasus ini:

- Order dihitung **lewat invoice-nya**, bukan sebagai transaksi POS, sehingga tidak dihitung dua kali
- **Incentive Salesperson** di invoice otomatis diisi dengan **Cashier** dari order POS
- Aturan invoice biasa berlaku (harus Posted dan lunas)

### 14.6 Retur di POS

Jika ada retur/refund barang di POS, sistem melakukan dua hal:

1. **Mengurangi net sales (achievement) kasir yang mencatat retur** pada periode retur dibuat.
2. **Mengurangi dasar payout penjualan awalnya**, jika retur dibuat dari order asal (tombol **Refund** di POS lalu memilih order yang diretur). Payout hanya dihitung dari barang yang benar-benar dibeli customer.

Contoh:

- Order POS 10 barang × 148.000 = 1.480.000
- Customer mengembalikan 5 barang (retur 740.000)
- Net sales kasir berkurang 740.000
- Dasar payout order tersebut menjadi 740.000

Di menu **Transactions**, baris retur tampil sebagai **Credit Note / Refund** dengan nilai **minus**. Buka baris retur tersebut: field **Reversal Of** di bagian **Adjustment Trail** menunjukkan transaksi penjualan asalnya.

Hal yang perlu diperhatikan:

- Retur sebaiknya diproses oleh kasir (login) yang **sama** dengan penjualan awal. Jika berbeda, pengurangan net sales masuk ke kasir yang memproses retur.
- Jika penjualan awal tidak tercatat di insentif (misalnya kasirnya belum punya Sales Branch), retur tetap mengurangi net sales kasir yang memproses retur.

### 14.7 Cara Mengecek Transaksi POS

**Dari menu Transactions**

1. Buka **Sales Incentive → Transactions**
2. Gunakan filter **From POS** untuk melihat transaksi POS saja (atau **From Invoice** untuk invoice saja)
3. Gunakan **Group By → Source Type** untuk melihat total per sumber
4. Kolom **POS Order** menunjukkan nomor order POS asal

**Dari order POS**

1. Buka **Point of Sale → Orders → Orders**
2. Buka order yang ingin dicek
3. Di bawah kolom **Cashier**, akan muncul daftar transaksi insentif dari order tersebut (periode, nilai, status)

Jika daftar ini tidak muncul setelah **Calculate**, berarti order belum masuk perhitungan. Cek kembali syarat di bagian 14.3.

### 14.8 Salah Kasir, Bagaimana?

Jika order tercatat atas nama kasir yang salah, laporkan ke Finance/Admin **sebelum** periode di-**Lock**.

Admin cukup memperbaiki **Cashier** di order POS tersebut, lalu klik **Calculate** ulang di periode insentif. Sistem akan memindahkan transaksi ke kasir yang benar dan menghapus transaksi lama atas nama kasir yang salah.

Catatan: jika periode sudah di-**Lock**, transaksi yang sudah dibayarkan tidak berubah lagi. Koreksi dilakukan di periode berikutnya.

---

## 15. Down Payment Invoice

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

## 16. Diskon Invoice

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

## 17. Tier Insentif

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

## 18. Menjalankan Perhitungan Insentif

Setelah target, invoice, dan transaksi POS siap, buka:

**Sales Incentive → Incentive Periods**

Pilih periode, lalu klik **Calculate**.

Sistem akan menghitung:

- Net sales
- Achievement
- Tier
- Invoice yang eligible
- Invoice yang sudah lunas
- Transaksi POS di periode tersebut
- Incentive payout
- Bonus payout
- Branch payout
- Total payout

Setelah selesai, status periode menjadi **Calculated**.

### Calculate Ditolak karena Data Karyawan Belum Lengkap

Sebelum menghitung payout, sistem mengecek semua orang yang mendapat kredit penjualan di periode tersebut. Orang-orang ini adalah salesperson invoice, PM / Salesperson 2 / Salesperson 3 project, dan kasir POS.

Jika ada yang **tidak akan mendapat payout** karena datanya belum lengkap, Calculate ditolak dengan pesan seperti:

```
These people have sales in Sept 26 but would get no payout:

- No Sales Branch / Business Type: Agus Dwipayana, yael@linkederp.com
- No target in Sept 26: Yoppi Liehanto

Fill in their employee incentive settings and run the target cascade, then calculate again.
```

Cara memperbaiki:

| Pesan | Tindakan |
|---|---|
| **No Sales Branch / Business Type** | Buka **Employees** → tab **Sales Incentive**, isi **Sales Branch**, **Business Type**, dan **FTE Designation** |
| **No target in [periode]** | Jalankan **Cascade Branch Target** untuk periode tersebut (bagian 10), atau isi target orang itu di menu **Targets** |

Jika orang tersebut memang bukan sales (misalnya user admin yang kebetulan tercatat sebagai salesperson invoice), ganti **Incentive Salesperson** di invoice, atau ganti **Cashier** di order POS, ke sales yang benar.

Setelah diperbaiki, klik **Calculate** lagi. Selama Calculate ditolak, tidak ada data yang berubah.

Pengecekan yang sama juga berlaku saat Calculate dari **Branch Targets**. Yang dicek adalah tim cabang tersebut, ditambah orang yang belum punya cabang sama sekali.

---

## 19. Membaca Hasil Payout

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

## 20. Penjelasan Komponen Payout

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

## 21. Approve dan Lock

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

## 22. Jika Ada Karyawan Resign

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

## 23. Jika Ada Karyawan Baru

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

## 24. Jika Ada Posisi Kosong / Vacant

Jika ada posisi yang belum terisi, user bisa membuat record employee sebagai **Vacant Position**.

Fungsinya agar sistem tahu ada kursi kosong di tim tersebut.

Porsi posisi kosong dapat dialihkan ke tim aktif sebagai bonus jika opsi **Redistribute Vacant Slots** dicentang saat cascade.

---

## 25. Population Changed / Perlu Re-Cascade

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

## 26. Refund / Retur

Jika ada refund atau credit note, sistem akan mengurangi dasar perhitungan insentif.

User perlu memastikan credit note dibuat dengan benar dari invoice asal.

Jika credit note dibuat dari invoice asal, sistem bisa mengenali hubungan antara invoice dan refund tersebut.

Contoh:

- Invoice 10 juta sudah lunas
- Kemudian dibuat credit note 3 juta
- Maka dasar payout menjadi 7 juta

Jika credit note dibuat manual tanpa hubungan ke invoice asal, user perlu berhati-hati karena sistem mungkin tidak bisa menghubungkan otomatis.

Untuk retur di POS, aturannya sama: retur yang dibuat dari order asal akan mengurangi dasar payout order tersebut. Detailnya ada di bagian 14.6.

---

## 27. Kasus yang Sering Ditanyakan

### Kenapa payout 0 padahal ada sales?

Kemungkinan penyebab:

- Achievement masih di bawah 75%
- Invoice belum lunas
- Invoice masih partial payment
- Diskon baris invoice lebih dari 35%
- Karyawan belum punya target di periode tersebut
- Salesperson di invoice belum benar
- Invoice punya project, dan salesperson tersebut tidak tercantum di project
- Untuk POS: sales tidak login atas namanya sendiri di kasir, atau belum punya Sales Branch

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

### Kenapa saya yang buat Sales Order, tapi komisinya masuk ke orang lain?

Karena Sales Order tersebut punya project, dan komisi dibagi ke orang-orang yang ada di project (PM, Salesperson 2, Salesperson 3). Jika Anda tidak tercantum di project, Anda tidak mendapat bagian. Minta Admin menambahkan Anda di project jika memang ikut menangani.

### Kenapa bagian saya di project malah masuk ke PM?

Karena saat Calculate, Anda belum punya **Sales Branch / Business Type**, atau belum punya **target** di periode invoice tersebut. Bagian Salesperson 2 / 3 yang tidak memenuhi syarat otomatis dialihkan ke PM. Minta Admin melengkapi data Anda (dan menjalankan cascade target), lalu **Calculate** ulang sebelum periode di-Lock.

### Kenapa satu invoice muncul beberapa kali di Transactions?

Karena invoice tersebut dari project yang dibagi ke beberapa orang. Setiap orang mendapat satu baris sesuai persennya.

### Kenapa penjualan POS saya tidak masuk insentif?

Kemungkinan penyebab:

- POS belum mengaktifkan **Log in with Employees**
- Saat transaksi, yang login di kasir adalah karyawan lain
- Data karyawan belum diisi **Sales Branch**
- Tanggal order di luar periode yang dihitung
- **Calculate** belum dijalankan ulang setelah transaksi terjadi

### Kenapa transaksi POS langsung masuk payout, tidak menunggu lunas?

Karena di POS customer sudah membayar penuh di kasir. Jadi transaksi POS langsung dianggap lunas di bulan order tersebut.

### Order POS saya ada invoice-nya, apakah dihitung dua kali?

Tidak. Order POS yang dibuatkan invoice hanya dihitung lewat invoice-nya.

### Kenapa sales tidak bisa melihat My Incentive?

Kemungkinan data employee belum terhubung ke user Odoo.

### Kenapa calculate ditolak?

Kemungkinan:

- Periode belum Open
- Periode sudah Locked
- Ada perubahan tim yang belum di-cascade ulang
- Target belum lengkap
- Ada orang dengan penjualan di periode itu yang belum punya **Sales Branch / Business Type** atau belum punya **target**. Pesan error menyebutkan nama-namanya (lihat bagian 18)

---

## 28. Checklist Sebelum Calculate

Sebelum klik **Calculate**, pastikan:

- Periode sudah Open
- Rule Version sudah dipilih
- Branch Target sudah dibuat
- Target sudah di-cascade dan di-apply
- Data karyawan sudah benar
- Semua salesperson invoice, PM / Salesperson 2 / 3 project, dan kasir POS sudah punya **Sales Branch**, **Business Type**, dan **target** di periode ini
- Tidak ada warning perubahan tim
- Invoice sudah Posted
- Invoice memiliki salesperson yang benar
- Project di Sales Order sudah berisi PM, Salesperson 2/3, dan persen komisi yang benar (total 100%)
- Payment status invoice sudah benar
- Refund/credit note sudah dibuat dengan benar
- Semua sesi POS di periode tersebut sudah ditutup
- Order POS tercatat atas nama kasir (sales) yang benar

---

## 29. Checklist Sebelum Lock

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

## 30. Ringkasan Proses Cepat

```text
1. Setup karyawan
2. Buat periode
3. Isi branch target
4. Cascade target
5. Pastikan invoice dan pembayaran benar
6. Pastikan sesi POS sudah ditutup dan kasir benar
7. Calculate
8. Review payout
9. Approve
10. Lock
```

---

## 31. Catatan untuk User

- Jangan langsung lock jika angka belum direview.
- Jika ada resign/new hire, selalu lakukan cascade ulang.
- Jika invoice masih partial, jangan berharap payout muncul.
- Jika menggunakan DP, payout baru muncul saat final invoice lunas.
- Jika ada refund, pastikan credit note dibuat dari invoice asal.
- Jika ada perubahan data karyawan, jalankan ulang cascade dan calculate.
- Jika ada perubahan orang atau persen komisi di project, jalankan ulang calculate.
- Di POS, selalu login dengan nama dan PIN sendiri sebelum melayani customer.

---

## 32. Contoh Perhitungan Lengkap (B2B)

Bagian ini menjelaskan alur perhitungan dari awal sampai akhir dengan satu contoh nyata. Datanya **sudah ada di database** sehingga setiap angka di bawah bisa dicek langsung di Odoo.

### 32.1 Data Contoh di Database

Semua data contoh diberi nama **Demo** / **[DEMO]** agar mudah dicari:

| Data | Nama di Odoo |
|---|---|
| Cabang | **Demo B2B** (kode DEMO), Business Type **B2B** |
| Rule | **Demo Scheme Q4 2026** (tier sama dengan skema 2H, lihat bagian 17) |
| Periode | **Demo Okt 2026** dan **Demo Nov 2026** (status **Calculated**) |
| Karyawan | **[DEMO] Andi**, **[DEMO] Bella**, **[DEMO] Candra**, **[DEMO] Dewi**, **[DEMO] Eko** |
| Customer / Produk | **[DEMO] PT Contoh Pelanggan** / **[DEMO] Sofa Kantor** |
| Project | **[DEMO] Proyek Interior Kantor** |

Cara melihatnya:

- **Sales Incentive → Incentive Periods** → buka **Demo Okt 2026**
- **Sales Incentive → Payouts** → filter Period = Demo Okt 2026
- **Sales Incentive → Transactions** → filter Period = Demo Okt 2026
- Di setiap payout, tab **Computation Log** berisi jejak perhitungan orang tersebut

Data ini dibuat dengan script `seed_incentive_demo_b2b_2026.py` (di folder repository).

### 32.2 Tim Demo B2B

| Karyawan | Role | FTE Branch | FTE Individual | Keterangan |
|---|---|---:|---:|---|
| [DEMO] Andi | Lead | 1,5 | 1,5 | |
| [DEMO] Bella | Team | 1,0 | 1,0 | |
| [DEMO] Candra | Team | 1,0 | 1,0 | |
| [DEMO] Dewi | Team | 1,0 | 1,0 | **Karyawan baru**, Effective Target Start **16 Okt 2026** |
| [DEMO] Eko | Support | 0,25 | 0 | Tidak punya target individual |
| Kenny Nathaniel Wahyudi | Head | 2,0 | – | **Global Branch Member** (bagian 7) |

Branch Target Oktober: **Demo B2B / B2B = 1.000.000.000**.

### 32.3 Langkah 1 — Cascade Target

Target cabang dibagi ke setiap kursi (seat) sesuai **FTE Individual**:

```text
Target dasar per orang = Target cabang × FTE orang ÷ Total FTE tim
```

Total FTE individual = 1,5 + 1 + 1 + 1 = **4,5**. Eko (Support) tidak dihitung karena FTE individualnya 0.

Dewi baru masuk 16 Oktober. Dia aktif 16 dari 31 hari, jadi **prorata = 16/31 = 51,61%**.

| Karyawan | Perhitungan | Target Incentive |
|---|---|---:|
| Andi | 1.000.000.000 × 1,5 ÷ 4,5 | 333.333.333,33 |
| Bella | 1.000.000.000 × 1 ÷ 4,5 | 222.222.222,22 |
| Candra | 1.000.000.000 × 1 ÷ 4,5 | 222.222.222,22 |
| Dewi | 222.222.222,22 × 16/31 | 114.695.340,50 |

Kursi Dewi kosong 15 hari (15/31). Karena **Redistribute Vacant Slots** dicentang, porsi kosong itu menjadi **target bonus**:

```text
Porsi kosong = 222.222.222,22 × 15/31 = 107.526.881,72
```

Porsi ini dibagikan ke orang yang bekerja **penuh sebulan**, sesuai FTE. Orangnya Andi 1,5, Bella 1, dan Candra 1, jadi totalnya 3,5:

| Karyawan | Perhitungan | Target Bonus |
|---|---|---:|
| Andi | 107.526.881,72 × 1,5 ÷ 3,5 | 46.082.949,31 |
| Bella | 107.526.881,72 × 1 ÷ 3,5 | 30.721.966,21 |
| Candra | 107.526.881,72 × 1 ÷ 3,5 | 30.721.966,21 |

Hasilnya bisa dicek di **Sales Incentive → Targets**. Source target incentive = *Rolling Forecast Cascade*, source target bonus = *Vacancy Redistribution*.

> Orang yang punya **target bonus** masuk kategori **mixed**. Aturannya dibahas di Langkah 3 dan 4.

### 32.4 Langkah 2 — Transaksi Bulan Oktober

Semua invoice berikut sudah **Posted**:

| Invoice | Tanggal | Credit ke | Nilai | Catatan | Lunas |
|---|---|---|---:|---|---|
| INV/2026/04594 | 5 Okt | Andi | 380.000.000 | | 15 Okt |
| INV/2026/04595 | 8 Okt | Bella | 150.000.000 | | 20 Okt |
| INV/2026/04596 | 25 Okt | Bella | 50.000.000 | | **Belum lunas di Oktober** (lunas 10 Nov) |
| INV/2026/04597 baris 1 | 12 Okt | Candra | 170.000.000 | | 22 Okt |
| INV/2026/04597 baris 2 | 12 Okt | Candra | 30.000.000 | 50.000.000 dengan **diskon 40%** | 22 Okt |
| RINV/2026/00016 | 28 Okt | Candra | −10.000.000 | Credit note dari INV/2026/04597 | – |
| INV/2026/04598 | 20 Okt | Dewi | 60.000.000 | | 27 Okt |
| INV/2026/04599 | 18 Okt | Andi (PM 30%) | 30.000.000 | Invoice project 100.000.000 | 30 Okt |
| INV/2026/04599 | 18 Okt | Dewi (Salesperson 2, 70%) | 70.000.000 | Invoice project 100.000.000 | 30 Okt |

Catatan invoice project **[DEMO] Proyek Interior Kantor**: Sales Order-nya dibuat oleh **Bella**. Bella tidak tercantum di project, jadi dia **tidak mendapat bagian** (bagian 13.3). Kreditnya dibagi ke PM Andi 30% dan Salesperson 2 Dewi 70%.

Di **Transactions**, invoice project muncul dua baris, satu untuk Andi dan satu untuk Dewi.

### 32.5 Langkah 3 — Achievement dan Tier (per orang)

Tier ditentukan dari **semua** penjualan bulan itu: lunas maupun belum, termasuk baris dengan diskon besar. Nilai retur mengurangi penjualan.

```text
Net Sales   = Penjualan (invoice) − Retur (credit note)
Achievement = Net Sales ÷ Target Incentive
```

| Karyawan | Penjualan | Retur | Net Sales | Target Incentive | Achievement | Tier |
|---|---:|---:|---:|---:|---:|---|
| Andi | 410.000.000 | 0 | 410.000.000 | 333.333.333,33 | 123,00% | Tier 5 → **dibatasi Tier 4 (0,75%)** |
| Bella | 200.000.000 | 0 | 200.000.000 | 222.222.222,22 | 90,00% | **Tier 3 (0,675%)** |
| Candra | 200.000.000 | 10.000.000 | 190.000.000 | 222.222.222,22 | 85,50% | **Tier 2 (0,60%)** |
| Dewi | 130.000.000 | 0 | 130.000.000 | 114.695.340,50 | 113,34% | **Tier 5 (0,7875%)** |

Penjelasan:

- **Andi** mencapai Tier 5, tetapi dia punya target bonus (mixed). Pada skema mixed, tier **dibatasi maksimal Tier 4**. Rate-nya menjadi 0,75%.
- **Bella**: invoice 50 juta yang belum lunas **tetap dihitung** untuk tier. Tanpa invoice itu, achievement-nya hanya 67,5% (Tier 0).
- **Candra**: baris diskon 40% tetap dihitung untuk tier. Credit note 10 juta mengurangi net sales.
- **Dewi**: targetnya kecil karena prorata, dan dia tidak punya target bonus. Jadi dia mendapat Tier 5 penuh.

Tier yang didapat **dibekukan** ke setiap transaksi bulan itu (kolom *Tier Payout Rate* di Transactions). Rate ini dipakai lagi kalau invoice-nya baru lunas di bulan berikutnya (Langkah 8).

### 32.6 Langkah 4 — Dasar Payout yang Eligible

Tidak semua penjualan boleh dibayarkan. Yang **tidak** masuk dasar payout:

- Baris invoice dengan diskon **lebih dari 35%** (bagian 16)
- Baris **Down Payment** (bagian 15)
- Credit note (hanya mengurangi, lihat Langkah 5)

| Karyawan | Eligible | Dikeluarkan (diskon > 35%) |
|---|---:|---:|
| Andi | 410.000.000 | 0 |
| Bella | 200.000.000 | 0 |
| Candra | 170.000.000 | 30.000.000 |
| Dewi | 130.000.000 | 0 |

Untuk orang **mixed** (punya target bonus), dasar eligible dibagi ke dua keranjang (bucket):

```text
Bucket Incentive = maksimal sebesar Target Incentive
Bucket Bonus     = sisa di atas Target Incentive (tidak dibatasi)
```

Pengisian dilakukan **berurutan berdasarkan tanggal invoice**. Invoice yang lebih awal mengisi bucket incentive lebih dulu.

**Andi** (target incentive 333.333.333,33):

| Invoice | Nilai | Masuk Bucket Incentive | Masuk Bucket Bonus |
|---|---:|---:|---:|
| INV/2026/04594 (5 Okt) | 380.000.000 | 333.333.333,33 | 46.666.666,67 |
| INV/2026/04599 (18 Okt, project) | 30.000.000 | 0 | 30.000.000 |
| **Total** | 410.000.000 | **333.333.333,33** | **76.666.666,67** |

Bella dan Candra juga mixed, tetapi eligible-nya di bawah target incentive, jadi bucket bonus mereka 0. Dewi tidak mixed, jadi semua eligible-nya masuk bucket incentive.

### 32.7 Langkah 5 — Hanya yang Sudah Lunas yang Dibayar

Dari dasar eligible, yang dibayar hanya invoice yang **lunas di bulan ini**. Jika ada credit note yang terhubung ke invoice asal, nilainya dikurangkan dulu.

```text
Incentive Payout (current) = Bucket incentive yang lunas × Rate tier
Bonus Payout               = Bucket bonus yang lunas     × Bonus rate (1%)
```

| Karyawan | Bucket Incentive Lunas | × Rate | Payout Current | Bucket Bonus Lunas | × 1% | Bonus Payout |
|---|---:|---:|---:|---:|---:|---:|
| Andi | 333.333.333,33 | 0,75% | 2.500.000,00 | 76.666.666,67 | 1% | 766.666,67 |
| Bella | 150.000.000 | 0,675% | 1.012.500,00 | 0 | | 0 |
| Candra | 160.000.000 | 0,60% | 960.000,00 | 0 | | 0 |
| Dewi | 130.000.000 | 0,7875% | 1.023.750,00 | 0 | | 0 |

Penjelasan:

- **Bella**: invoice 50 juta belum lunas, jadi yang dibayar baru 150 juta. Sisanya menunggu lunas (Langkah 8).
- **Candra**: baris 170 juta dikurangi credit note 10 juta = **160 juta**. Baris diskon 40% tidak dibayar sama sekali.

### 32.8 Langkah 6 — Branch Payout

Branch payout menghitung pencapaian **cabang** secara keseluruhan.

**a. Tier cabang**

```text
Net sales cabang = 410 + 200 + 190 + 130 juta = 930.000.000
Achievement      = 930.000.000 ÷ 1.000.000.000 = 93%  →  Tier 3 (0,675%)
```

Batasan Tier 4 untuk mixed **tidak** berlaku di level cabang.

**b. Siapa yang ikut**

Yang ikut adalah anggota tim yang eligible branch dan **aktif pada tanggal 1** periode, ditambah Global Branch Member:

| Orang | FTE Branch | Ikut? |
|---|---:|---|
| Andi | 1,5 | Ya |
| Bella | 1,0 | Ya |
| Candra | 1,0 | Ya |
| Eko (Support) | 0,25 | Ya, walaupun tidak punya target |
| Kenny (Global) | 2,0 | Ya |
| Dewi | – | **Tidak**, karena baru mulai 16 Okt (belum aktif tanggal 1) |
| **Total FTE** | **5,75** | |

**c. Pool dan pembagian**

```text
Pool          = jumlah Payout Current anggota yang ikut
              = 2.500.000 + 1.012.500 + 960.000 + 0 (Eko) + 0 (Kenny) = 4.472.500
Branch Payout = Pool × (FTE orang ÷ Total FTE) × Rate tier cabang
```

Pool hanya dari **Payout Current**. Bonus Payout dan Payout Prior tidak ikut dihitung. Payout Dewi juga tidak masuk pool karena dia tidak ikut branch bulan ini.

| Orang | Perhitungan | Branch Payout |
|---|---|---:|
| Andi | 4.472.500 × 1,5/5,75 × 0,675% | 7.875,49 |
| Bella | 4.472.500 × 1/5,75 × 0,675% | 5.250,33 |
| Candra | 4.472.500 × 1/5,75 × 0,675% | 5.250,33 |
| Eko | 4.472.500 × 0,25/5,75 × 0,675% | 1.312,58 |
| Kenny | 4.472.500 × 2/5,75 × 0,675% | 10.500,65 |

### 32.9 Langkah 7 — Total Payout Oktober

```text
Total Payout = Payout Current + Payout Prior + Bonus Payout + Branch Payout
```

| Karyawan | Current | Prior | Bonus | Branch | **Total** |
|---|---:|---:|---:|---:|---:|
| Andi | 2.500.000,00 | 0 | 766.666,67 | 7.875,49 | **3.274.542,16** |
| Bella | 1.012.500,00 | 0 | 0 | 5.250,33 | **1.017.750,33** |
| Candra | 960.000,00 | 0 | 0 | 5.250,33 | **965.250,33** |
| Dewi | 1.023.750,00 | 0 | 0 | 0 | **1.023.750,00** |
| Eko | 0 | 0 | 0 | 1.312,58 | **1.312,58** |
| Kenny | 0 | 0 | 0 | 10.500,65 | **10.500,65** |
| **Total Oktober** | | | | | **6.293.106,05** |

### 32.10 Langkah 8 — November: Invoice Oktober yang Baru Lunas

Invoice Bella **INV/2026/04596** (50 juta, tanggal 25 Okt) baru lunas **10 November**.

Di **Demo Nov 2026**:

- Branch Target November 1.000.000.000 di-cascade ulang. Dewi sekarang aktif penuh, jadi semua mendapat target normal (Andi 333.333.333,33; lainnya 222.222.222,22) dan **tidak ada target bonus**.
- Tidak ada penjualan baru di November, jadi tier November semuanya **Tier 0**.
- Invoice Bella tetap dibayar dengan rate tier **bulan asal invoice** (Tier 3 Oktober = 0,675%), **bukan** tier November:

```text
Payout Prior Bella = 50.000.000 × 0,675% = 337.500
```

| Karyawan | Current | Prior | Bonus | Branch | **Total November** |
|---|---:|---:|---:|---:|---:|
| Bella | 0 | 337.500 | 0 | 0 | **337.500** |
| Lainnya | 0 | 0 | 0 | 0 | 0 |

Branch payout November = 0, karena net sales cabang November 0 (Tier 0). Payout Prior juga tidak ikut pool branch.

### 32.11 Ringkasan Alur

```text
1. Cascade      Target cabang × FTE ÷ total FTE × prorata  → Target Incentive
                Porsi kursi kosong → Target Bonus (untuk yang full sebulan)
2. Transaksi    Invoice posted di bulan itu (split project, POS, retur)
3. Tier (SQ1)   Net sales (semua invoice, lunas/belum) ÷ Target Incentive
                Mixed → tier maksimal Tier 4
4. Eligible     Buang diskon > 35% dan DP
   (SQ2)        Isi bucket incentive (sampai target) lalu bucket bonus, urut tanggal
5. Lunas (SQ3)  Current = bucket incentive lunas bulan ini × rate tier
                Bonus   = bucket bonus lunas × 1%
                Prior   = invoice bulan lalu yang lunas bulan ini × rate tier bulan asalnya
6. Branch       Tier dari net sales cabang ÷ target cabang
                Pool = total Payout Current tim yang aktif tanggal 1 (+ Global member)
                Branch payout = Pool × FTE ÷ total FTE × rate tier cabang
7. Total        Current + Prior + Bonus + Branch
```

---

## 33. Rumus Setiap Angka dan Contohnya

Bagian ini adalah **kamus rumus**. Setiap angka yang muncul di layar **Targets**, **Payouts**, dan **Transactions** dijelaskan dari mana asalnya, lengkap dengan contoh angka.

Semua contoh memakai data **Demo Okt 2026** dan **Demo Nov 2026** dari bagian 32, jadi bisa langsung dicocokkan di Odoo. Contoh yang bukan dari data demo diberi tanda *(contoh ilustrasi)*.

Gunakan bagian ini jika ada pertanyaan **"kenapa hasil saya seperti ini?"**.

### 33.1 Angka di Menu Targets

| Kolom | Rumus | Contoh |
|---|---|---|
| **Amount** (Target Type = Incentive) | Target cabang × FTE orang ÷ total FTE tim × Proration + Carry-Forward | Dewi: 1.000.000.000 × 1 ÷ 4,5 × 16/31 = **114.695.340,50** |
| **Amount** (Target Type = Bonus) | Porsi kursi kosong × FTE orang ÷ total FTE orang yang bekerja penuh sebulan | Andi: 107.526.881,72 × 1,5 ÷ 3,5 = **46.082.949,31** |
| **FTE Used** | FTE Individual dari role (FTE Designation) | Andi (Lead) = **1,5** |
| **Proration** | Hari aktif ÷ jumlah hari di bulan itu | Dewi masuk 16 Okt: 16 ÷ 31 = **0,5161** |
| **Source** | Asal target | *Rolling Forecast Cascade* = hasil cascade; *Vacancy Redistribution* = target bonus dari kursi kosong |
| **Shortfall** | Target Incentive − Net Sales (jika hasilnya positif). Diisi saat periode di-**Lock** | lihat contoh di bawah |
| **Months Remaining** | Jumlah bulan setelah periode ini sampai akhir Rule | lihat contoh di bawah |
| **Carry-Forward / Month** | Shortfall ÷ Months Remaining | lihat contoh di bawah |

**Contoh Carry-Forward** *(contoh ilustrasi: data demo belum di-Lock)*

Misalkan **Demo Okt 2026** di-Lock. Rule *Demo Scheme Q4 2026* berlaku sampai Desember 2026.

```text
Bella: Target Incentive Okt = 222.222.222,22, Net Sales Okt = 200.000.000
Shortfall             = 222.222.222,22 − 200.000.000 = 22.222.222,22
Months Remaining      = November, Desember           = 2
Carry-Forward / Month = 22.222.222,22 ÷ 2            = 11.111.111,11
```

Saat cascade November dijalankan setelah Oktober di-Lock:

```text
Target Incentive Bella Nov = 222.222.222,22 (dasar) + 11.111.111,11 (carry-forward) = 233.333.333,33
```

Desember juga mendapat tambahan 11.111.111,11 yang sama.

Aturan carry-forward:

- Hanya dari periode yang sudah **Locked** dan memakai **Rule yang sama**
- Hanya **target incentive**. Target bonus tidak dibawa ke bulan berikutnya
- Yang dibawa hanya **target**. Payout tidak dibawa
- Di Branch Target, kolom **Carry-Forward** = total carry-forward seluruh tim cabang itu

### 33.2 Angka di Payout — Bagian Individual

Contoh memakai **Andi** dan **Candra** di Demo Okt 2026.

| Kolom | Rumus | Andi | Candra |
|---|---|---:|---:|
| **Target Incentive** | Target incentive orang itu di periode ini | 333.333.333,33 | 222.222.222,22 |
| **Target Bonus** | Target bonus orang itu | 46.082.949,31 | 30.721.966,21 |
| **Target Total** | Target Incentive + Target Bonus | 379.416.282,64 | 252.944.188,43 |
| **Mixed Scenario** | Dicentang jika punya Target Bonus | ✓ | ✓ |
| **Gross Sales** | Jumlah semua baris invoice bulan ini: lunas/belum, termasuk DP dan diskon besar | 410.000.000 | 200.000.000 |
| **Sales Return** | Jumlah credit note / retur bulan ini | 0 | 10.000.000 |
| **Net Sales** | Gross Sales − Sales Return | 410.000.000 | 190.000.000 |
| **Achievement** | Net Sales ÷ Target Incentive | 123,00% | 85,50% |
| **Tier** | Tier yang cocok dengan Achievement (bagian 17). Jika Mixed, maksimal Tier 4 | Tier 4 (seharusnya Tier 5, dibatasi) | Tier 2 |
| **Payout Rate** | Allocation tier × Base Rate (0,75%) | 1,0 × 0,75% = 0,75% | 0,8 × 0,75% = 0,60% |
| **Eligible Achievement Incentive** | Dasar eligible (tanpa diskon > 35% dan tanpa DP), maksimal sebesar Target Incentive | 333.333.333,33 | 170.000.000 |
| **Eligible Achievement Bonus** | Sisa dasar eligible di atas Target Incentive (hanya jika Mixed) | 76.666.666,67 | 0 |
| **Excluded (Discount > cap)** | Baris invoice dengan diskon lebih dari 35% | 0 | 30.000.000 |
| **Paid Current Month** | Bagian incentive dari invoice bulan ini yang **lunas bulan ini**, dikurangi credit note yang terhubung | 333.333.333,33 | 160.000.000 |
| **Paid Prior Month** | Bagian incentive dari invoice **bulan sebelumnya** yang baru lunas bulan ini | 0 | 0 |
| **Paid Bonus** | Bagian bonus yang lunas bulan ini | 76.666.666,67 | 0 |
| **Incentive Payout Current Month** | Paid Current Month × Payout Rate | 2.500.000,00 | 960.000,00 |
| **Incentive Payout Previous Month** | Setiap invoice bulan lalu × **rate tier bulan asal invoice itu** | 0 | 0 |
| **Incentive Payout** | Current Month + Previous Month | 2.500.000,00 | 960.000,00 |
| **Bonus Payout** | Paid Bonus × Bonus Rate (1%) | 766.666,67 | 0 |

Contoh **Incentive Payout Previous Month** (Bella di Demo Nov 2026):

```text
Invoice INV/2026/04596 tanggal 25 Okt, 50.000.000, lunas 10 Nov
Rate yang dipakai   = Tier 3 Oktober (0,675%), bukan tier November (Tier 0)
Paid Prior Month    = 50.000.000
Payout Prev. Month  = 50.000.000 × 0,675% = 337.500
```

### 33.3 Angka di Payout — Bagian Branch

Contoh memakai **Andi** di Demo Okt 2026.

| Kolom | Rumus | Andi |
|---|---|---:|
| **Branch Target** | Total Target di Branch Target (dasar + carry-forward) | 1.000.000.000 |
| **Branch Net Sales** | Net Sales semua orang di cabang × business type itu | 930.000.000 |
| **Branch Achievement** | Branch Net Sales ÷ Branch Target | 93,00% |
| **Branch Tier** | Tier yang cocok dengan Branch Achievement. Batas Tier 4 untuk Mixed **tidak** berlaku di sini | Tier 3 |
| **Branch Payout Rate** | Rate Branch Tier | 0,675% |
| **Branch Pool / Branch Eligible Base** | Jumlah **Incentive Payout Current Month** semua anggota tim yang ikut branch | 4.472.500,00 |
| **Branch FTE Weight** | FTE Branch orang itu | 1,5 |
| **Branch FTE Share** | FTE orang ÷ total FTE yang ikut (termasuk Global Branch Member) | 1,5 ÷ 5,75 = 26,09% |
| **Branch Paid Base** | Branch Pool × Branch FTE Share | 1.166.739,13 |
| **Branch Payout** | Branch Paid Base × Branch Payout Rate | 7.875,49 |

Yang **ikut** branch payout adalah anggota tim yang eligible branch dan **sudah aktif pada tanggal 1** periode, ditambah Global Branch Member. Karyawan yang baru masuk di tengah bulan (seperti Dewi) belum ikut di bulan itu.

### 33.4 Total dan Status Payout

| Kolom | Rumus | Andi |
|---|---|---:|
| **Total Payout** | Incentive Payout + Bonus Payout + Branch Payout | 2.500.000 + 766.666,67 + 7.875,49 = **3.274.542,16** |
| **Eligible Month** | Dicentang jika Tier individual atau Branch Tier di atas Tier 0 | ✓ |
| **Is Frozen** | Dicentang setelah periode / branch di-**Lock**. Angkanya tidak berubah lagi | – |

### 33.5 Angka di Menu Transactions

Satu baris Transactions = satu baris invoice (atau baris POS) untuk satu orang.

| Kolom | Arti / Rumus | Contoh |
|---|---|---|
| **Line Amount** | Nilai baris × Share. Credit note / retur bernilai **minus** | Andi di invoice project INV/2026/04599: 100.000.000 × 30% = **30.000.000** |
| **Share** / **Credit Role** | Persen bagian orang itu dan posisinya (PM, Salesperson 2/3, Salesperson / Cashier) | Dewi: 70%, Salesperson 2 |
| **Discount Eligible** | Dicentang jika diskon baris ≤ 35% | Candra baris diskon 40%: **tidak** dicentang |
| **Fully Paid** / **Fully Paid On** | Invoice sudah lunas penuh, dan tanggal lunasnya | Bella INV/2026/04596: lunas 10 Nov |
| **Source Period** | Bulan **invoice dibuat**. Menentukan tier | Oktober |
| **Payment Period** | Bulan **invoice lunas**. Menentukan kapan dibayar | November |
| **Is Prior Period** | Dicentang jika Payment Period lebih lambat dari Source Period | Bella INV/2026/04596: ✓ |
| **Incentive Allocation** / **Bonus Allocation** | Bagian baris ini yang masuk bucket incentive / bonus. Diisi urut tanggal invoice | Andi INV/2026/04594: 333.333.333,33 / 46.666.666,67 |
| **Bucket** | *Incentive* jika Incentive Allocation sama dengan atau lebih besar dari Bonus Allocation; *Bonus* jika bagian bonus yang lebih besar; *Excluded* jika keduanya 0 | Andi INV/2026/04599: Bonus |
| **Tier (snapshot)** / **Payout Rate (snapshot)** | Tier bulan asal invoice, dibekukan saat Calculate | Candra: Tier 2 / 0,60% |
| **Payout Amount** | Incentive Allocation × Payout Rate (snapshot) + Bonus Allocation × 1%. Jika ada credit note yang terhubung, kedua allocation dikurangi dulu secara proporsional. Hanya untuk baris yang lunas, eligible, dan bukan DP | lihat di bawah |

Contoh **Payout Amount**:

```text
Andi   INV/2026/04594 : 333.333.333,33 × 0,75% + 46.666.666,67 × 1% = 2.966.666,67
Andi   INV/2026/04599 : 0 × 0,75%              + 30.000.000    × 1% =   300.000,00
Candra INV/2026/04597 : (170.000.000 − 10.000.000) × 0,60%           =   960.000,00
Candra baris diskon 40% : tidak eligible                             =         0
```

Jumlah Payout Amount per orang = Incentive Payout + Bonus Payout-nya. Andi: 2.966.666,67 + 300.000 = 3.266.666,67 = 2.500.000 + 766.666,67. Branch Payout tidak tercatat di Transactions.

### 33.6 Cara Membaca Computation Log

Di form Payout, tab **Computation Log** menyimpan jejak perhitungan. Contoh log **Andi** (Demo Okt 2026):

```text
Target incentive=333333333.33 bonus=46082949.31 mixed=True
SQ1 net=410000000.0 / target=333333333.33 => 1.2300 => Tier 4 (rate 0.007500)
SQ2 eligible=410000000.0 excluded=0 -> incentive=333333333.33 bonus=76666666.67
SQ3 paid_current=333333333.33 x 0.007500 = 2500000.0
SQ3 paid_prior=0 (own frozen rates) = 0.0
Bonus 76666666.67 x 0.010000 = 766666.67
```

| Baris | Artinya |
|---|---|
| `Target ... mixed=True` | Target incentive 333,3 jt dan target bonus 46,1 jt, jadi Andi masuk skema mixed |
| `SQ1 net=... => 1.2300 => Tier 4` | Net sales 410 jt ÷ target 333,3 jt = 123%. Tier dibatasi ke Tier 4 karena mixed, rate 0,75% |
| `SQ2 eligible=... excluded=0` | Semua 410 jt eligible: 333,3 jt masuk bucket incentive, 76,7 jt masuk bucket bonus |
| `SQ3 paid_current=... = 2500000.0` | Bucket incentive yang lunas × 0,75% = 2,5 jt |
| `SQ3 paid_prior=0` | Tidak ada invoice bulan lalu yang lunas bulan ini |
| `Bonus ... = 766666.67` | Bucket bonus yang lunas × 1% |

Angka di log memakai titik sebagai desimal (format sistem). Contoh: `0.007500` = 0,75%.

### 33.7 Kenapa Hasilnya Begini?

| Pertanyaan | Penyebab | Contoh |
|---|---|---|
| Ada sales, tapi Incentive Payout 0 | Achievement di bawah 75% (Tier 0) | Tanpa invoice 50 jt, Bella hanya 150 jt ÷ 222,2 jt = 67,5% → Tier 0 → payout 0 |
| Achievement tepat 90%, kenapa Tier 3 bukan Tier 2? | Tier berlaku jika **batas bawah ≤ achievement < batas atas**. Angka yang tepat di batas masuk ke tier atas | Bella 90,00% → Tier 3 (90%–99,9%) |
| Achievement 123% tapi Tier 4, bukan Tier 5 | Punya target bonus (mixed), sehingga tier dibatasi maksimal Tier 4 | Andi |
| Net Sales besar tapi payout kecil | Sebagian invoice **belum lunas**. Tier dihitung dari semua invoice, payout hanya dari yang lunas | Bella: net 200 jt, dibayar dari 150 jt |
| Invoice lunas bulan ini, tapi rate-nya beda dengan tier bulan ini | Invoice bulan lalu dibayar dengan **rate bulan asal invoice** | Bella November dibayar 0,675% (tier Oktober) |
| Satu baris invoice tidak menghasilkan payout | Diskon baris lebih dari 35% | Candra, baris 30 jt diskon 40% |
| Setelah credit note, tier dan payout turun | Credit note mengurangi Net Sales (tier) dan dasar payout invoice asalnya | Candra: net 200 → 190 jt (Tier 2), dasar 170 → 160 jt |
| DP tidak menghasilkan payout | DP hanya dihitung untuk tier. Payout menunggu invoice final lunas | lihat contoh di bawah |
| Target orang baru lebih kecil | Target dihitung prorata sesuai hari aktif | Dewi 16/31 → 114,7 jt |
| Orang baru tidak dapat Branch Payout | Belum aktif pada tanggal 1 periode | Dewi, Oktober |
| Support / Pak Kenny dapat payout tanpa sales | Mereka ikut Branch Payout sesuai FTE branch | Eko 1.312,58; Kenny 10.500,65 |
| Target bulan ini lebih besar dari pembagian biasa | Ada carry-forward dari kekurangan bulan lalu yang sudah Locked | 33.1 |
| Saya yang buat Sales Order, tapi tidak dapat apa-apa | SO punya project, dan Anda tidak tercantum di project | Bella pada Proyek Interior Kantor |
| Total payout satu cabang kecil padahal tim besar | Branch Payout dihitung dari **Incentive Payout Current Month** tim, bukan dari nilai sales | Pool 4,47 jt × 0,675% |

**Contoh DP** *(contoh ilustrasi)*

Order 100 juta dengan Down Payment 50 juta. Tier bulan itu 0,75%.

| Bulan | Baris Invoice | Gross Sales (untuk tier) | Dasar Payout (setelah lunas) |
|---|---|---:|---:|
| Januari | DP 50 jt | +50 jt | 0 (DP tidak dibayar) |
| Februari | Produk 100 jt dan potongan DP −50 jt | +100 jt − 50 jt = +50 jt | 100 jt |

Jadi order ini menambah achievement Januari 50 jt dan Februari 50 jt. Payout-nya satu kali, **100 jt × rate tier Februari**, setelah invoice final lunas. Order tidak dihitung dua kali.

---

## 34. Contoh 3 Bulan: Juni, Juli, Agustus 2027 (B2B)

Contoh ini menunjukkan bagaimana perhitungan **bersambung dari bulan ke bulan**: kekurangan target dibawa ke bulan berikutnya, invoice yang baru lunas di bulan berikutnya, karyawan resign lalu diganti, dan Down Payment yang dilunasi di bulan lain. Rumus setiap kolom ada di bagian 33.

### 34.1 Data Contoh di Database

| Data | Nama di Odoo |
|---|---|
| Cabang | **Demo B2B 2027** (kode DEMO27), Business Type **B2B** |
| Rule | **Demo Scheme Jun-Agu 2027**, berlaku 1 Juni – 31 Agustus 2027 (tier sama dengan bagian 17) |
| Periode | **Demo Jun 2027** (Locked), **Demo Jul 2027** (Locked), **Demo Agu 2027** (Calculated) |
| Karyawan | **[DEMO27] Rudi**, **[DEMO27] Sari**, **[DEMO27] Tono**, **[DEMO27] Wati**, **[DEMO27] Umar** |
| Project | **[DEMO27] Proyek Kantor Cabang** |

Buka **Sales Incentive → Payouts**, lalu **Group By → Period** untuk melihat ketiga bulan sekaligus. Data dibuat dengan script `seed_incentive_demo_b2b_2027.py`.

### 34.2 Tim dan Kejadian per Bulan

| Karyawan | Role | FTE Branch / Individual | Juni | Juli | Agustus |
|---|---|---|---|---|---|
| Rudi | Lead | 1,5 / 1,5 | aktif | aktif, ada **invoice DP** | aktif, **DP dilunasi**, PM project 40% |
| Sari | Team | 1,0 / 1,0 | aktif, invoice **baru dibayar sebagian** | aktif, invoice Juni **lunas** | aktif |
| Tono | Team | 1,0 / 1,0 | aktif | **resign 15 Juli** | sudah keluar |
| Wati | Team | 1,0 / 1,0 | belum masuk | belum masuk | **masuk 1 Agustus** (pengganti Tono), Salesperson 2 project 60% |
| Umar | Support | 0,25 / 0 | aktif | aktif | aktif |
| Kenny | Head (Global) | 2,0 / – | ikut branch | ikut branch | ikut branch |

Branch Target setiap bulan: **800.000.000**.

---

### 34.3 Juni 2027

**a. Target (cascade)**

Total FTE individual = Rudi 1,5 + Sari 1 + Tono 1 = **3,5**.

| Karyawan | Perhitungan | Target Incentive |
|---|---|---:|
| Rudi | 800.000.000 × 1,5 ÷ 3,5 | 342.857.142,86 |
| Sari | 800.000.000 × 1 ÷ 3,5 | 228.571.428,57 |
| Tono | 800.000.000 × 1 ÷ 3,5 | 228.571.428,57 |

**b. Transaksi**

| Invoice | Tanggal | Karyawan | Nilai | Pembayaran |
|---|---|---|---:|---|
| INV/2027/00001 | 8 Jun | Rudi | 360.000.000 | lunas 20 Jun |
| INV/2027/00002 | 10 Jun | Sari | 200.000.000 | **dibayar 100 jt tanggal 25 Jun** (partial), sisanya 10 Jul |
| INV/2027/00003 | 12 Jun | Tono | 240.000.000 | lunas 28 Jun |

**c. Payout individual**

| Karyawan | Net Sales | Achievement | Tier / Rate | Lunas Juni | Incentive Payout |
|---|---:|---:|---|---:|---:|
| Rudi | 360.000.000 | 105,00% | Tier 4 / 0,75% | 360.000.000 | 2.700.000,00 |
| Sari | 200.000.000 | 87,50% | Tier 2 / 0,60% | **0** | **0** |
| Tono | 240.000.000 | 105,00% | Tier 4 / 0,75% | 240.000.000 | 1.800.000,00 |

**Sari** sudah mencapai Tier 2, karena invoice yang belum lunas tetap dihitung untuk tier. Tetapi invoice-nya baru dibayar sebagian, jadi **belum ada yang dibayarkan** di bulan Juni.

**d. Branch payout**

```text
Net sales cabang = 360 + 200 + 240 juta = 800.000.000
Achievement      = 800.000.000 ÷ 800.000.000 = 100%  →  Tier 4 (0,75%)
Total FTE branch = Rudi 1,5 + Sari 1 + Tono 1 + Umar 0,25 + Kenny 2 = 5,75
Pool             = 2.700.000 + 0 + 1.800.000 = 4.500.000
```

| Orang | Perhitungan | Branch Payout |
|---|---|---:|
| Rudi | 4.500.000 × 1,5/5,75 × 0,75% | 8.804,35 |
| Sari | 4.500.000 × 1/5,75 × 0,75% | 5.869,57 |
| Tono | 4.500.000 × 1/5,75 × 0,75% | 5.869,57 |
| Umar | 4.500.000 × 0,25/5,75 × 0,75% | 1.467,39 |
| Kenny | 4.500.000 × 2/5,75 × 0,75% | 11.739,13 |

**e. Total Juni**

| Karyawan | Incentive | Bonus | Branch | **Total** |
|---|---:|---:|---:|---:|
| Rudi | 2.700.000,00 | 0 | 8.804,35 | **2.708.804,35** |
| Sari | 0 | 0 | 5.869,57 | **5.869,57** |
| Tono | 1.800.000,00 | 0 | 5.869,57 | **1.805.869,57** |
| Umar | 0 | 0 | 1.467,39 | **1.467,39** |
| Kenny | 0 | 0 | 11.739,13 | **11.739,13** |
| **Total Juni** | | | | **4.533.750,01** |

**f. Lock Juni → kekurangan target dibawa ke bulan berikutnya**

Saat Juni di-**Lock**, sistem menghitung kekurangan target (kolom di menu **Targets**):

| Karyawan | Target | Net Sales | Shortfall | Months Remaining | Carry-Forward / Month |
|---|---:|---:|---:|---:|---:|
| Rudi | 342.857.142,86 | 360.000.000 | 0 | 2 | 0 |
| **Sari** | 228.571.428,57 | 200.000.000 | **28.571.428,57** | 2 (Juli, Agustus) | **14.285.714,29** |
| Tono | 228.571.428,57 | 240.000.000 | 0 | 2 | 0 |

Kekurangan Sari dibagi ke **2 bulan tersisa** dalam Rule. Juli dan Agustus masing-masing mendapat tambahan target 14.285.714,29.

---

### 34.4 Juli 2027

**a. Target (cascade)**

Tiga hal berubah di bulan Juli:

1. **Tono resign 15 Juli**, jadi dia aktif 15 dari 31 hari (prorata **48,39%**).
2. Sisa kursi Tono selama 16 hari menjadi **target bonus** untuk orang yang bekerja penuh sebulan (Rudi dan Sari).
3. Target Sari **bertambah carry-forward** dari Juni.

```text
Target dasar per kursi Team = 800.000.000 × 1 ÷ 3,5 = 228.571.428,57
Tono      = 228.571.428,57 × 15/31                 = 110.599.078,34
Sari      = 228.571.428,57 + 14.285.714,29 (carry) = 242.857.142,86
Porsi kosong kursi Tono = 228.571.428,57 × 16/31   = 117.972.350,23
  Bonus Rudi = 117.972.350,23 × 1,5 ÷ 2,5          =  70.783.410,14
  Bonus Sari = 117.972.350,23 × 1   ÷ 2,5          =  47.188.940,09
```

| Karyawan | Target Incentive | Target Bonus |
|---|---:|---:|
| Rudi | 342.857.142,86 | 70.783.410,14 |
| Sari | 242.857.142,86 (termasuk carry 14.285.714,29) | 47.188.940,09 |
| Tono | 110.599.078,34 | – |

Branch Target Juli ikut bertambah: 800.000.000 + carry-forward tim 14.285.714,29 = **814.285.714,29**.

**b. Transaksi**

| Invoice | Tanggal | Karyawan | Nilai | Catatan | Pembayaran |
|---|---|---|---:|---|---|
| INV/2027/00007 | 5 Jul | Tono | 60.000.000 | | lunas 12 Jul |
| INV/2027/00004 | 6 Jul | Rudi | 300.000.000 | | lunas 16 Jul |
| INV/2027/00006 | 9 Jul | Sari | 260.000.000 | | lunas 19 Jul |
| INV/2027/00005 | 20 Jul | Rudi | 100.000.000 | **Down Payment** | lunas 22 Jul |
| INV/2027/00002 | (10 Jun) | Sari | 200.000.000 | invoice **Juni** | **sisa dibayar 10 Jul → lunas** |

**c. Payout individual**

| Karyawan | Net Sales | Achievement | Tier / Rate | Dasar Lunas | Payout |
|---|---:|---:|---|---|---:|
| Rudi | 400.000.000 | 116,67% | Tier 5 → **dibatasi Tier 4** / 0,75% | 300.000.000 (DP tidak dibayar) | Current 2.250.000,00 |
| Sari | 260.000.000 | 107,06% | Tier 4 / 0,75% | incentive 242.857.142,86 + bonus 17.142.857,14 | Current 1.821.428,57 + Bonus 171.428,57 |
| Sari (invoice Juni) | | | rate **Juni** Tier 2 / 0,60% | 200.000.000 | **Prior 1.200.000,00** |
| Tono | 60.000.000 | 54,25% | **Tier 0** / 0% | 60.000.000 | 0 |

Penjelasan:

- **Rudi**: invoice DP 100 jt **menaikkan tier**. Tanpa DP, achievement-nya hanya 300 ÷ 342,9 = 87,5% (Tier 2). Dengan DP menjadi 116,7%. Karena Rudi punya target bonus (mixed), tier dibatasi di Tier 4. DP-nya sendiri **tidak dibayar**; yang dibayar hanya invoice 300 jt.
- **Sari**:
  - Penjualan Juli 260 jt melewati target 242,9 jt. Bagian sampai target masuk **bucket incentive** (× 0,75%), sisanya 17,1 jt masuk **bucket bonus** (× 1%).
  - Invoice Juni 200 jt baru **lunas** di Juli, jadi dibayar sekarang sebagai **Incentive Payout Previous Month**. Rate-nya memakai tier **bulan asal invoice** (Juni, Tier 2 = 0,60%), bukan tier Juli: 200.000.000 × 0,60% = **1.200.000**. Seluruh 200 jt dibayar di Juli, karena pembayaran sebagian di Juni tidak dihitung.
- **Tono**: achievement 54% (di bawah 75%), sehingga Tier 0 dan payout 0 walaupun invoice-nya lunas.

**d. Branch payout**

```text
Net sales cabang = 400 + 260 + 60 juta          = 720.000.000
Achievement      = 720.000.000 ÷ 814.285.714,29 = 88,42%  →  Tier 2 (0,60%)
Total FTE branch = Rudi 1,5 + Sari 1 + Tono 1 + Umar 0,25 + Kenny 2 = 5,75
Pool             = 2.250.000 + 1.821.428,57 + 0 = 4.071.428,57
```

Catatan:

- Tono masih ikut branch karena dia **aktif pada tanggal 1 Juli**.
- Branch Target naik karena carry-forward Sari. Tanpa carry-forward, achievement cabang 90% (Tier 3). Dengan carry-forward menjadi 88,42% (Tier 2).
- Pool hanya dari **Payout Current**. Payout Prior Sari (1,2 jt) dan Bonus Payout **tidak** ikut pool.

| Orang | Perhitungan | Branch Payout |
|---|---|---:|
| Rudi | 4.071.428,57 × 1,5/5,75 × 0,60% | 6.372,67 |
| Sari | 4.071.428,57 × 1/5,75 × 0,60% | 4.248,45 |
| Tono | 4.071.428,57 × 1/5,75 × 0,60% | 4.248,45 |
| Umar | 4.071.428,57 × 0,25/5,75 × 0,60% | 1.062,11 |
| Kenny | 4.071.428,57 × 2/5,75 × 0,60% | 8.496,89 |

**e. Total Juli**

| Karyawan | Current | Prior | Bonus | Branch | **Total** |
|---|---:|---:|---:|---:|---:|
| Rudi | 2.250.000,00 | 0 | 0 | 6.372,67 | **2.256.372,67** |
| Sari | 1.821.428,57 | 1.200.000,00 | 171.428,57 | 4.248,45 | **3.197.105,59** |
| Tono | 0 | 0 | 0 | 4.248,45 | **4.248,45** |
| Umar | 0 | 0 | 0 | 1.062,11 | **1.062,11** |
| Kenny | 0 | 0 | 0 | 8.496,89 | **8.496,89** |
| **Total Juli** | | | | | **5.467.285,71** |

**f. Lock Juli**

| Karyawan | Target | Net Sales | Shortfall | Carry-Forward / Month (1 bulan tersisa) |
|---|---:|---:|---:|---:|
| Rudi | 342.857.142,86 | 400.000.000 | 0 | 0 |
| Sari | 242.857.142,86 | 260.000.000 | 0 | 0 |
| Tono | 110.599.078,34 | 60.000.000 | 50.599.078,34 | 50.599.078,34 |

Kekurangan Tono tercatat, tetapi Tono sudah keluar dan **tidak ikut cascade Agustus**. Karena itu carry-forward-nya **tidak dibebankan ke siapa pun**. Carry-forward selalu melekat ke orangnya sendiri, tidak dipindah ke penggantinya.

---

### 34.5 Agustus 2027

**a. Target (cascade)**

Tono sudah keluar, dan **Wati masuk 1 Agustus** sebagai pengganti. Tidak ada kursi kosong, jadi **tidak ada target bonus** bulan ini.

| Karyawan | Perhitungan | Target Incentive |
|---|---|---:|
| Rudi | 800.000.000 × 1,5 ÷ 3,5 | 342.857.142,86 |
| Sari | 228.571.428,57 + 14.285.714,29 (cicilan ke-2 dari Juni) | 242.857.142,86 |
| Wati | 800.000.000 × 1 ÷ 3,5 (aktif penuh sejak tanggal 1) | 228.571.428,57 |

**b. Transaksi**

| Invoice | Tanggal | Credit ke | Nilai | Catatan | Lunas |
|---|---|---|---:|---|---|
| INV/2027/00008 | 5 Agu | Rudi | 250.000.000 dan **−100.000.000** | Pelunasan order DP Juli: baris produk 250 jt + baris potongan DP | 15 Agu |
| INV/2027/00009 | 10 Agu | Rudi | 200.000.000 | | 20 Agu |
| INV/2027/00010 | 12 Agu | Sari | 150.000.000 | | 22 Agu |
| INV/2027/00011 | 14 Agu | Wati | 180.000.000 | | 24 Agu |
| INV/2027/00012 | 18 Agu | Rudi (PM 40%) | 40.000.000 | Invoice project 100 jt | 28 Agu |
| INV/2027/00012 | 18 Agu | Wati (Salesperson 2, 60%) | 60.000.000 | Invoice project 100 jt | 28 Agu |

**c. Payout individual**

| Karyawan | Net Sales | Achievement | Tier / Rate | Dasar Lunas | Incentive Payout |
|---|---:|---:|---|---:|---:|
| Rudi | 390.000.000 | 113,75% | **Tier 5** / 0,7875% | 490.000.000 | 3.858.750,00 |
| Sari | 150.000.000 | 61,76% | **Tier 0** / 0% | 150.000.000 | 0 |
| Wati | 240.000.000 | 105,00% | Tier 4 / 0,75% | 240.000.000 | 1.800.000,00 |

Penjelasan:

- **Rudi — Net Sales 390 jt, tetapi dasar payout 490 jt.** Dua angka ini memang berbeda:

  ```text
  Net Sales (untuk tier) = 250 − 100 (potongan DP) + 200 + 40 (project) = 390.000.000
  Dasar payout           = 250 (produk, tanpa baris DP) + 200 + 40     = 490.000.000
  ```

  Nilai order-nya 250 jt: DP 100 jt ditagih di Juli, dan sisanya 150 jt ditagih di invoice pelunasan (baris produk 250 jt − potongan DP 100 jt). Achievement order ini terbagi dua: **+100 jt di Juli** dan **+150 jt di Agustus**, total 250 jt. Payout-nya dibayar **sekali di Agustus** dari baris produk 250 jt. DP 100 jt tidak pernah dibayar terpisah, jadi tidak ada yang dihitung dua kali.
- **Rudi** tidak punya target bonus di Agustus (tidak mixed), sehingga Tier 5 tidak dibatasi.
- **Sari**: target Agustus lebih tinggi karena cicilan carry-forward kedua (242,9 jt). Penjualan 150 jt = 61,8%, jadi Tier 0.
- **Wati** (karyawan baru) langsung mendapat target penuh karena mulai tanggal 1. Dia juga mendapat 60% dari invoice project sebagai Salesperson 2.

**d. Branch payout**

```text
Net sales cabang = 390 + 150 + 240 juta         = 780.000.000
Achievement      = 780.000.000 ÷ 814.285.714,29 = 95,79%  →  Tier 3 (0,675%)
Total FTE branch = Rudi 1,5 + Sari 1 + Wati 1 + Umar 0,25 + Kenny 2 = 5,75
Pool             = 3.858.750 + 0 + 1.800.000    = 5.658.750
```

Wati ikut branch payout, karena dia sudah aktif pada tanggal 1 Agustus.

| Orang | Perhitungan | Branch Payout |
|---|---|---:|
| Rudi | 5.658.750 × 1,5/5,75 × 0,675% | 9.964,32 |
| Sari | 5.658.750 × 1/5,75 × 0,675% | 6.642,88 |
| Wati | 5.658.750 × 1/5,75 × 0,675% | 6.642,88 |
| Umar | 5.658.750 × 0,25/5,75 × 0,675% | 1.660,72 |
| Kenny | 5.658.750 × 2/5,75 × 0,675% | 13.285,76 |

**e. Total Agustus**

| Karyawan | Incentive | Bonus | Branch | **Total** |
|---|---:|---:|---:|---:|
| Rudi | 3.858.750,00 | 0 | 9.964,32 | **3.868.714,32** |
| Sari | 0 | 0 | 6.642,88 | **6.642,88** |
| Wati | 1.800.000,00 | 0 | 6.642,88 | **1.806.642,88** |
| Umar | 0 | 0 | 1.660,72 | **1.660,72** |
| Kenny | 0 | 0 | 13.285,76 | **13.285,76** |
| **Total Agustus** | | | | **5.696.946,56** |

Agustus masih berstatus **Calculated**, jadi masih bisa di-Calculate ulang, di-Approve, lalu di-Lock.

---

### 34.6 Ringkasan 3 Bulan

| Karyawan | Juni | Juli | Agustus | **Total 3 Bulan** |
|---|---:|---:|---:|---:|
| Rudi | 2.708.804,35 | 2.256.372,67 | 3.868.714,32 | **8.833.891,34** |
| Sari | 5.869,57 | 3.197.105,59 | 6.642,88 | **3.209.618,04** |
| Tono | 1.805.869,57 | 4.248,45 | – | **1.810.118,02** |
| Wati | – | – | 1.806.642,88 | **1.806.642,88** |
| Umar | 1.467,39 | 1.062,11 | 1.660,72 | **4.190,22** |
| Kenny | 11.739,13 | 8.496,89 | 13.285,76 | **33.521,78** |
| **Total** | **4.533.750,01** | **5.467.285,71** | **5.696.946,56** | **15.697.982,28** |

### 34.7 Yang Bisa Dipelajari dari Contoh Ini

| Kejadian | Bulan | Pelajaran |
|---|---|---|
| Invoice Sari dibayar sebagian | Juni → Juli | Invoice partial tetap dihitung untuk tier, tetapi baru dibayar setelah **lunas penuh**, memakai rate tier **bulan asal invoice** |
| Sari di bawah target | Juni → Juli, Agustus | Kekurangan target dibagi ke bulan tersisa dalam Rule, dan baru terbawa setelah bulan itu di-**Lock** |
| Carry-forward menaikkan target cabang | Juli, Agustus | Branch Target = target dasar + carry-forward tim, sehingga tier cabang bisa turun |
| Tono resign di tengah bulan | Juli | Target prorata. Sisa kursinya menjadi target bonus untuk orang yang bekerja penuh sebulan |
| Carry-forward Tono | Juli → Agustus | Carry-forward hanya untuk orangnya sendiri. Jika orangnya sudah keluar, carry-forward hilang |
| DP Rudi | Juli → Agustus | DP menaikkan tier bulan DP, tidak dibayar sendiri. Payout dibayar sekali dari baris produk invoice pelunasan |
| Rudi mixed | Juli | Punya target bonus, sehingga tier maksimal Tier 4 |
| Wati masuk tanggal 1 | Agustus | Karyawan yang mulai tanggal 1 mendapat target penuh dan langsung ikut branch payout |
| Project Rudi 40% / Wati 60% | Agustus | Kredit dibagi sesuai persen di project |
| Umar & Kenny | Semua bulan | Tanpa penjualan pun tetap mendapat branch payout sesuai FTE |

---

## 35. Penutup

Modul **VIF Sales Incentive** membantu menghitung insentif dengan lebih rapi, transparan, dan dapat diaudit.

Kunci utama penggunaan modul ini adalah mengikuti urutan proses:

**Target benar → Project & Invoice & POS benar → Payment benar → Calculate → Review → Approve → Lock**

Jika urutan ini diikuti, hasil payout akan lebih mudah diperiksa dan lebih aman untuk digunakan sebagai dasar pembayaran insentif.

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

### 13.5 Invoice Tanpa Project

Jika Sales Order tidak punya project (atau invoice dibuat manual, atau invoice dari POS), sistem memakai cara lama:

- **Incentive Salesperson** di invoice mendapat **100%**
- Untuk invoice dari POS, Incentive Salesperson adalah kasirnya (lihat bagian 14)

Catatan: field **Incentive Salesperson** di invoice hanya berpengaruh untuk invoice **tanpa project**. Untuk invoice dengan project, pembagian selalu mengikuti data project.

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

## 32. Penutup

Modul **VIF Sales Incentive** membantu menghitung insentif dengan lebih rapi, transparan, dan dapat diaudit.

Kunci utama penggunaan modul ini adalah mengikuti urutan proses:

**Target benar → Project & Invoice & POS benar → Payment benar → Calculate → Review → Approve → Lock**

Jika urutan ini diikuti, hasil payout akan lebih mudah diperiksa dan lebih aman untuk digunakan sebagai dasar pembayaran insentif.

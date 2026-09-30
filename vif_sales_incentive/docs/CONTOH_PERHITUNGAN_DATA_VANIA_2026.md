# Contoh Perhitungan dengan Data Asli — Jan, Feb, Jun, Jul, Agu 2026

Dokumen ini menjawab pertanyaan **"angka insentif yang benar seharusnya berapa?"** dengan memakai data asli di database **vanialook**: invoice, pembayaran, project, dan data karyawan yang ada sekarang.

Rumus lengkap setiap kolom ada di **PANDUAN_USER_VIF_SALES_INCENTIVE.md**. Contoh perhitungan langkah demi langkah ada di §32 dan §34, dan kamus rumus di §33. Dokumen ini fokus pada **data Vania yang sebenarnya**.

---

## 1. Ringkasan untuk Owner

**Kenapa angka yang dihitung sebelumnya salah?**

Di Jan 2026, **semua 707 invoice** belum punya **Incentive Salesperson**. Akibatnya **630 invoice (±2,16 miliar)** tidak masuk perhitungan siapa pun. Yang terhitung hanya invoice project yang punya PM.

Langkah **VIF: Backfill Invoice Salesperson** belum dijalankan. Langkah ini wajib dijalankan sekali untuk setiap periode (README Odoo Online §11 langkah 3).

**Total payout seharusnya:**

| Bulan | Total Payout Seharusnya | Keterangan |
|---|---:|---|
| Jan 2026 | **8.505.915,39** | Di layar saat ini hanya 2.169.322,53 |
| Feb 2026 | **9.720.916,69** | |
| Jun 2026 | **8.486.663,77** | |
| Jul 2026 | **4.586.445,18** | Di layar saat ini 3.444.038,02 (lihat §7) |
| Agu 2026 | **4.006.735,46** | |

Angka di atas adalah **simulasi** dengan asumsi di bagian 2. Angka resmi di Odoo baru sama setelah langkah perbaikan di bagian 8 dijalankan.

---

## 2. Asumsi dan Batasan

| No | Asumsi / Batasan | Dampak |
|---|---|---|
| 1 | **Branch Target** Feb dan Jun = Branch Target Jan 2026. Jul = target Jul yang sudah diisi (Jakarta, Bandung) + target Jan untuk Bali, Medan, Surabaya. Agu = sama dengan Jul | Kalau angka rolling forecast sebenarnya berbeda, tier dan payout ikut berubah |
| 2 | **5 orang dikeluarkan** karena belum punya Sales Branch / Business Type: Yogi Mulia, Nurul F Ningsih, Dzulfikcar, Karina E Sudarwati, Deriansyah Drajat Sales (bagian 6) | Penjualan mereka tidak dihitung. Karena mereka tidak masuk cabang mana pun, angka orang lain tidak terpengaruh, **kecuali** nanti mereka ditempatkan di cabang yang sama |
| 3 | Hanya **B2B**. Belum ada Branch Target B2C | Karyawan B2C (Gregonsa, Nur Suci, Vivie, dll.) belum dihitung |
| 4 | Periode **belum di-Lock** | Belum ada **carry-forward** (kekurangan target yang dibawa ke bulan berikutnya) |
| 5 | Periode **Mar, Apr, Mei 2026 belum ada** | Invoice yang lunas di Mar–Mei **tidak pernah dibayar**, karena tidak ada periode pembayarannya (contoh di §5.2) |
| 6 | Target individual memakai hasil cascade yang sudah ada | Jan dan Jul memakai target yang sudah diisi. Feb, Jun, dan Agu hasil cascade baru |

---

## 3. Aturan yang Berlaku

| Periode | Rule | Aturan Tier |
|---|---|---|
| Jan, Feb, Jun 2026 | **2026 First Half** | **Flat**: achievement < 75% = 0%; achievement ≥ 75% = **0,75%** |
| Jul, Agu 2026 | **2026 Second Half** | Bertingkat: Tier 1 (75%) 0,30%, Tier 2 (85%) 0,60%, Tier 3 (90%) 0,675%, Tier 4 (100%) 0,75%, Tier 5 (110%) 0,7875%. Punya target bonus → maksimal Tier 4 |

Aturan lain (bagian 12–17 panduan user):

- **Tier** dihitung dari semua invoice bulan itu, lunas maupun belum.
- **Payout** hanya dari invoice yang **lunas penuh**, dan baris dengan **diskon > 35% tidak dibayar**.
- Invoice yang lunas di bulan berikutnya dibayar di bulan lunasnya, dengan **rate tier bulan asal invoice** (*Payout Prior*).
- **Branch payout** = Pool (total Payout Current tim) × FTE orang ÷ total FTE tim × rate tier cabang.

Jumlah invoice per bulan:

| Bulan | Invoice & Credit Note (posted) | Nilai (untaxed) | Rule |
|---|---:|---:|---|
| Jan 2026 | 707 | 3.973.462.681 | 2026 First Half |
| Feb 2026 | 650 | 1.865.800.023 | 2026 First Half |
| Jun 2026 | 690 | 2.770.983.809 | 2026 First Half |
| Jul 2026 | 746 | 2.785.523.653 | 2026 Second Half |
| Agu 2026 | 638 | 2.197.447.272 | 2026 Second Half |

---

## 4. Januari 2026

### 4.1 Hasil per Cabang

| Cabang (B2B) | Branch Target | Net Sales Cabang | Achievement | Branch Tier | Rate | Pool (Payout Current tim) |
|---|---:|---:|---:|---|---:|---:|
| Bali | 2.100.000.000 | 2.170.290.149 | 103,35% | Tier 1 | 0,75% | 5.325.267,93 |
| Bandung | 109.000.000 | 99.030.382 | 90,85% | Tier 1 | 0,75% | 427.761,43 |
| Jakarta | 1.500.000.000 | 981.708.959 | 65,45% | Tier 0 | 0% | 1.468.077,66 |
| Medan | 32.000.000 | 79.496.444 | 248,43% | Tier 1 | 0,75% | 384.499,20 |
| Surabaya | 470.000.000 | 334.741.857 | 71,22% | Tier 0 | 0% | 854.277,70 |

Jakarta (65%) dan Surabaya (71%) berada di bawah 75%, sehingga **tidak ada branch payout**. Siti Rosnia tetap mendapat payout individual karena achievement pribadinya 164,6%.

### 4.2 Hasil per Orang

| Karyawan | Cabang | Role | Target Incentive | Net Sales | Achievement | Tier | Payout Current | Payout Prior | Bonus | Branch | **Total** |
|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|
| Ritya Novita Irianti Kekung | Bali | Lead | 572.727.273 | 738.201.554 | 128,89% | Tier 1 | 2.747.671,90 | 0,00 | 0,00 | 10.892,59 | **2.758.564,50** |
| Ni Komang Dewi Suryani | Bali | Team | 381.818.182 | 844.553.748 | 221,19% | Tier 1 | 1.483.435,20 | 0,00 | 0,00 | 7.261,73 | **1.490.696,93** |
| Donny Iswahyudi | Bali | Team | 381.818.182 | 427.208.622 | 111,89% | Tier 1 | 1.094.160,83 | 0,00 | 0,00 | 7.261,73 | **1.101.422,55** |
| Agus Dwipayana | Bali | Team | 381.818.182 | 80.901.350 | 21,19% | Tier 0 | 0,00 | 0,00 | 0,00 | 7.261,73 | **7.261,73** |
| Ni Wayan Ariyoshi S Ningsih | Bali | Team | 381.818.182 | 79.424.875 | 20,80% | Tier 0 | 0,00 | 0,00 | 0,00 | 7.261,73 | **7.261,73** |
| Indri Rubiantini | Bandung | Team | 43.600.000 | 99.030.382 | 227,13% | Tier 1 | 427.761,43 | 0,00 | 0,00 | 1.283,28 | **429.044,72** |
| Lauwra Kuncoro | Bandung | Lead | 65.400.000 | 0 | 0,00% | Tier 0 | 0,00 | 0,00 | 0,00 | 1.924,93 | **1.924,93** |
| Siti Rosnia Apriliyanti | Jakarta | Team | 272.727.273 | 449.016.740 | 164,64% | Tier 1 | 1.468.077,66 | 0,00 | 0,00 | 0,00 | **1.468.077,66** |
| Aditya Rachman | Jakarta | Team | 272.727.273 | 120.092.610 | 44,03% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Ika Kurniati | Jakarta | Lead | 409.090.909 | 281.891.885 | 68,91% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Resti D Shaskiya | Jakarta | Team | 272.727.273 | 34.501.875 | 12,65% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Yoppi Liehanto | Jakarta | Team | 272.727.273 | 96.205.849 | 35,28% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Asnita S Rangkuti | Medan | Team | 12.800.000 | 66.228.050 | 517,41% | Tier 1 | 384.499,20 | 0,00 | 0,00 | 1.153,50 | **385.652,70** |
| Richard Wahyudi W (Medan) | Medan | Lead | 19.200.000 | 0 | 0,00% | Tier 0 | 0,00 | 0,00 | 0,00 | 1.730,25 | **1.730,25** |
| Felicia Pranata | Surabaya | Team | 134.285.714 | 102.506.144 | 76,33% | Tier 1 | 540.781,45 | 0,00 | 0,00 | 0,00 | **540.781,45** |
| Richard Wahyudi Wiatmodjo | Surabaya | Lead | 201.428.571 | 163.532.999 | 81,19% | Tier 1 | 313.496,25 | 0,00 | 0,00 | 0,00 | **313.496,25** |
| Melisa Kurniawan | Surabaya | Team | 134.285.714 | 68.702.714 | 51,16% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| **Total** | | | | | | | | | | | **8.505.915,39** |

### 4.3 Perbandingan dengan Angka di Layar Sekarang

| Karyawan | Net Sales di layar | Net Sales seharusnya | Total di layar | **Total seharusnya** |
|---|---:|---:|---:|---:|
| Ritya Novita Irianti Kekung | 500.090.245 | 738.201.554 | 1.269.476,32 | **2.758.564,50** |
| Ni Komang Dewi Suryani | 679.136.488 | 844.553.748 | 816.660,15 | **1.490.696,93** |
| Siti Rosnia Apriliyanti | 5.490.000 | 449.016.740 | 0,00 | **1.468.077,66** |
| Donny Iswahyudi | 206.961.585 | 427.208.622 | 0,00 | **1.101.422,55** |
| Felicia Pranata | 17.295.251 | 102.506.144 | 0,00 | **540.781,45** |
| Indri Rubiantini | 16.027.924 | 99.030.382 | 0,00 | **429.044,72** |
| Asnita S Rangkuti | 20.610.025 | 66.228.050 | 83.186,06 | **385.652,70** |
| Richard Wahyudi Wiatmodjo | 62.736.382 | 163.532.999 | 0,00 | **313.496,25** |
| Agus Dwipayana | 79.613.450 | 80.901.350 | 0,00 | **7.261,73** |
| Ni Wayan Ariyoshi S Ningsih | 51.985.280 | 79.424.875 | 0,00 | **7.261,73** |
| Lauwra Kuncoro | 0 | 0 | 0,00 | **1.924,93** |
| Richard Wahyudi W (Medan) | 0 | 0 | 0,00 | **1.730,25** |
| Aditya Rachman | 27.158.292 | 120.092.610 | 0,00 | **0,00** |
| Ika Kurniati | 91.975.415 | 281.891.885 | 0,00 | **0,00** |
| Resti D Shaskiya | 21.483.705 | 34.501.875 | 0,00 | **0,00** |
| Yoppi Liehanto | 4.504.505 | 96.205.849 | 0,00 | **0,00** |
| Melisa Kurniawan | 0 | 68.702.714 | 0,00 | **0,00** |
| **Total** | | | 2.169.322,53 | **8.505.915,39** |

### 4.4 Contoh Detail: Asnita S Rangkuti (Medan B2B)

| Langkah | Perhitungan | Hasil |
|---|---|---:|
| Target | Branch Target Medan 32.000.000 × 1 ÷ 2,5 FTE (Asnita 1 + Richard Medan 1,5) | 12.800.000 |
| Gross Sales | 21 invoice di mana Asnita adalah salesperson (45.618.025) + 5 project di mana Asnita adalah PM (20.610.025) | 66.228.050 |
| Achievement | 66.228.050 ÷ 12.800.000 | 517,41% → Tier 1 (0,75%) |
| Dikeluarkan (diskon 90%) | INV/2026/00093 688.540 + INV/2026/00475 (1 baris) 323.400 | −1.011.940 |
| Belum lunas di Jan | INV/2026/00071, 00595, 00410, 00354 (lunas Februari) | −13.949.550 |
| Lunas Januari | 66.228.050 − 1.011.940 − 13.949.550 | 51.266.560 |
| **Payout Current** | 51.266.560 × 0,75% | **384.499,20** |
| Branch Payout | Pool Medan 384.499,20 × 1/2,5 × 0,75% | 1.153,50 |
| **Total** | | **385.652,70** |

Di layar saat ini hanya **83.186,06**, karena 21 invoice di mana Asnita adalah salesperson belum punya Incentive Salesperson.

### 4.5 Contoh Detail: Ni Komang Dewi Suryani (Bali B2B) — ada retur

| Langkah | Hasil |
|---|---:|
| Target Incentive | 381.818.181,82 |
| Gross Sales | 1.024.053.748 |
| Sales Return (credit note) | −179.500.000 |
| Net Sales → Achievement | 844.553.748 → 221,19% → Tier 1 |
| Eligible (tanpa diskon > 35% dan DP) | 642.209.178 |
| **Lunas Januari** | **197.791.360** |
| Payout Current = 197.791.360 × 0,75% | 1.483.435,20 |
| Branch Payout (Bali 103,35% → Tier 1) = 5.325.267,93 × 18,18% × 0,75% | 7.261,73 |
| **Total** | **1.490.696,93** |

Walaupun net sales-nya 844 jt, yang lunas di Januari hanya 197,8 jt. Sisanya akan dibayar di bulan invoice itu lunas, dengan rate Januari. Syaratnya, periode bulan pelunasan itu harus sudah ada di Odoo.

---

## 5. Februari 2026

### 5.1 Hasil per Cabang dan per Orang

| Cabang (B2B) | Branch Target | Net Sales Cabang | Achievement | Branch Tier | Rate | Pool (Payout Current tim) |
|---|---:|---:|---:|---|---:|---:|
| Bali | 2.100.000.000 | 898.777.211 | 42,80% | Tier 0 | 0% | 2.545.054,39 |
| Bandung | 109.000.000 | 46.835.045 | 42,97% | Tier 0 | 0% | 349.999,24 |
| Jakarta | 1.500.000.000 | 555.208.023 | 37,01% | Tier 0 | 0% | 0,00 |
| Medan | 32.000.000 | 42.481.788 | 132,76% | Tier 1 | 0,75% | 96.871,12 |
| Surabaya | 470.000.000 | 188.786.848 | 40,17% | Tier 0 | 0% | 0,00 |

| Karyawan | Cabang | Role | Target Incentive | Net Sales | Achievement | Tier | Payout Current | Payout Prior | Bonus | Branch | **Total** |
|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|
| Ni Komang Dewi Suryani | Bali | Team | 381.818.182 | 447.863.872 | 117,30% | Tier 1 | 2.545.054,39 | 1.504.628,63 | 0,00 | 0,00 | **4.049.683,01** |
| Ritya Novita Irianti Kekung | Bali | Lead | 572.727.273 | 240.933.175 | 42,07% | Tier 0 | 0,00 | 1.711.231,54 | 0,00 | 0,00 | **1.711.231,54** |
| Donny Iswahyudi | Bali | Team | 381.818.182 | 151.745.089 | 39,74% | Tier 0 | 0,00 | 1.509.429,85 | 0,00 | 0,00 | **1.509.429,85** |
| Agus Dwipayana | Bali | Team | 381.818.182 | 9.256.050 | 2,42% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Ni Wayan Ariyoshi S Ningsih | Bali | Team | 381.818.182 | 48.979.025 | 12,83% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Indri Rubiantini | Bandung | Team | 43.600.000 | 46.835.045 | 107,42% | Tier 1 | 349.999,24 | 237.233,33 | 0,00 | 0,00 | **587.232,56** |
| Lauwra Kuncoro | Bandung | Lead | 65.400.000 | 0 | 0,00% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Siti Rosnia Apriliyanti | Jakarta | Team | 272.727.273 | 144.915.838 | 53,14% | Tier 0 | 0,00 | 1.612.992,95 | 0,00 | 0,00 | **1.612.992,95** |
| Aditya Rachman | Jakarta | Team | 272.727.273 | 110.664.710 | 40,58% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Ika Kurniati | Jakarta | Lead | 409.090.909 | 152.235.062 | 37,21% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Resti D Shaskiya | Jakarta | Team | 272.727.273 | 16.630.306 | 6,10% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Yoppi Liehanto | Jakarta | Team | 272.727.273 | 130.762.107 | 47,95% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Asnita S Rangkuti | Medan | Team | 12.800.000 | 36.522.250 | 285,33% | Tier 1 | 96.871,12 | 104.621,62 | 0,00 | 290,61 | **201.783,36** |
| Richard Wahyudi W (Medan) | Medan | Lead | 19.200.000 | 0 | 0,00% | Tier 0 | 0,00 | 0,00 | 0,00 | 435,92 | **435,92** |
| Richard Wahyudi Wiatmodjo | Surabaya | Lead | 201.428.571 | 109.138.125 | 54,18% | Tier 0 | 0,00 | 24.761,25 | 0,00 | 0,00 | **24.761,25** |
| Felicia Pranata | Surabaya | Team | 134.285.714 | 47.410.828 | 35,31% | Tier 0 | 0,00 | 23.366,25 | 0,00 | 0,00 | **23.366,25** |
| Melisa Kurniawan | Surabaya | Team | 134.285.714 | 32.237.895 | 24,01% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| **Total** | | | | | | | | | | | **9.720.916,69** |

Februari sepi: hampir semua cabang di bawah 75%. Tetapi **banyak orang tetap mendapat payout**. Itu berasal dari **invoice Januari yang baru lunas di Februari** (kolom Payout Prior), yang dibayar dengan rate Januari.

### 5.2 Contoh Detail: Donny Iswahyudi — Tier 0, tapi tetap dapat payout

| Langkah | Hasil |
|---|---:|
| Target Feb | 381.818.181,82 |
| Net Sales Feb | 151.745.089 → 39,74% → **Tier 0** |
| Payout Current (invoice Feb) | 0 (Tier 0) |
| Invoice **Januari** yang lunas di Februari | 201.257.313 |
| **Payout Prior** = 201.257.313 × 0,75% (rate Tier 1 Januari) | **1.509.429,85** |
| **Total Februari** | **1.509.429,85** |

Jadi Tier 0 di Februari tidak menghapus hak atas penjualan Januari. Invoice Januari tetap dibayar dengan tier Januari.

### 5.3 Contoh Detail: Asnita S Rangkuti — invoice yang lunas di April

| Langkah | Hasil |
|---|---:|
| Net Sales Feb | 36.522.250 → 285,33% → Tier 1 |
| Dikeluarkan (6 baris diskon 90%) | 6.764.400 |
| Lunas Februari (invoice Feb) → Payout Current | 12.916.150 × 0,75% = 96.871,12 |
| Invoice **Januari** yang lunas Februari (INV/2026/00071, 00595, 00410, 00354) → Payout Prior | 13.949.550 × 0,75% = 104.621,62 |
| Branch Payout Medan (132,76% → Tier 1) | 290,61 |
| **Total Februari** | **201.783,36** |

**Perhatian:** 8 baris invoice Februari Asnita (INV/2026/00809, 01142, 01155, 01227, 01291) baru **lunas 7 April 2026**. Karena periode April belum dibuat, invoice ini **tidak akan pernah dibayar** sampai periode April ada dan dihitung.

---

## 6. Data yang Harus Dilengkapi

Kelima orang berikut punya kredit penjualan tetapi belum punya **Sales Branch / Business Type**. Selama belum dilengkapi, **Calculate akan ditolak** di bulan-bulan berikut:

| Bulan | Karyawan | Kredit Penjualan yang Tertahan |
|---|---|---:|
| Jan 2026 | Nurul F Ningsih | 75.000.000 |
| Jan 2026 | Yogi Mulia | 42.457.643 |
| Feb 2026 | Dzulfikcar | 0 |
| Feb 2026 | Karina E Sudarwati | 1.286.400 |
| Feb 2026 | Yogi Mulia | 43.307.355 |
| Jun 2026 | Dzulfikcar | 16.761.000 |
| Jun 2026 | Yogi Mulia | 18.706.032 |
| Agu 2026 | Deriansyah Drajat Sales | 244.800 |
| Agu 2026 | Dzulfikcar | 65.148.235 |

Dzulfikcar di Februari hanya punya 2 invoice senilai **Rp 0**, tetapi tetap memblokir Calculate karena tercatat sebagai penerima kredit.

Cara memperbaiki:

- Kalau mereka **sales**: isi Sales Branch, Business Type, dan FTE Designation di tab Sales Incentive, lalu cascade ulang.
- Kalau mereka **bukan sales** (misalnya admin / CS yang tercatat sebagai salesperson): ganti **Incentive Salesperson** di invoice mereka ke sales yang benar. Untuk invoice project, ganti PM / Salesperson 2 / Salesperson 3 di project-nya.

Data lain yang **perlu dicek**:

| Temuan | Kenapa Perlu Dicek |
|---|---|
| **Mentari D Silalahi**: Effective Target Start 1 Juli 2026, tetapi punya invoice di **Feb dan Jun 2026** | Penjualannya ikut menambah Net Sales cabang Medan, tetapi dia sendiri tidak dibayar. Kemungkinan tanggal mulainya salah, atau salesperson di invoice-invoice itu salah orang |
| **Ika Kurniati** ada 2 record: Jakarta (Lead) dan "Ika Kurniati (Bandung)" (Lead, mulai 1 Jul 2026) | Semua penjualan Juli–Agustus masuk ke record **Jakarta**. Record Bandung mendapat target Bandung, tetapi penjualannya 0 |
| **Richard Wahyudi** ada 2 record: "Richard Wahyudi W (Medan)" (Lead, tanpa penjualan) dan "Richard Wahyudi Wiatmodjo" (Surabaya) | Record Medan mendapat target 19,2 jt dan branch payout Medan tanpa penjualan. Pastikan ini memang disengaja |
| **Vacant Surabaya B2B** mulai 1 Jul 2026 | Kursi kosong ini membuat target Surabaya turun (dibagi 4,5 FTE) dan muncul target bonus. Lihat §8.2 |

---

## 7. Juni dan Juli 2026

### 7.1 Juni 2026

| Cabang (B2B) | Branch Target | Net Sales Cabang | Achievement | Branch Tier | Rate | Pool (Payout Current tim) |
|---|---:|---:|---:|---|---:|---:|
| Bali | 2.100.000.000 | 1.075.792.395 | 51,23% | Tier 0 | 0% | 4.224.188,14 |
| Bandung | 109.000.000 | 101.992.171 | 93,57% | Tier 1 | 0,75% | 723.973,54 |
| Jakarta | 1.500.000.000 | 1.012.184.109 | 67,48% | Tier 0 | 0% | 2.306.742,28 |
| Medan | 32.000.000 | 30.820.090 | 96,31% | Tier 1 | 0,75% | 0,00 |
| Surabaya | 470.000.000 | 343.039.965 | 72,99% | Tier 0 | 0% | 1.226.330,01 |

| Karyawan | Cabang | Role | Target Incentive | Net Sales | Achievement | Tier | Payout Current | Payout Prior | Bonus | Branch | **Total** |
|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|
| Donny Iswahyudi | Bali | Team | 381.818.182 | 336.410.735 | 88,11% | Tier 1 | 2.444.943,90 | 0,00 | 0,00 | 0,00 | **2.444.943,90** |
| Ni Komang Dewi Suryani | Bali | Team | 381.818.182 | 546.852.386 | 143,22% | Tier 1 | 1.779.244,24 | 0,00 | 0,00 | 0,00 | **1.779.244,24** |
| Agus Dwipayana | Bali | Team | 381.818.182 | 127.317.500 | 33,35% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Ni Wayan Ariyoshi S Ningsih | Bali | Team | 381.818.182 | 0 | 0,00% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Ritya Novita Irianti Kekung | Bali | Lead | 572.727.273 | 65.211.774 | 11,39% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Indri Rubiantini | Bandung | Team | 43.600.000 | 101.992.171 | 233,93% | Tier 1 | 723.973,54 | 0,00 | 0,00 | 2.171,92 | **726.145,46** |
| Lauwra Kuncoro | Bandung | Lead | 65.400.000 | 0 | 0,00% | Tier 0 | 0,00 | 0,00 | 0,00 | 3.257,88 | **3.257,88** |
| Ika Kurniati | Jakarta | Lead | 409.090.909 | 374.496.711 | 91,54% | Tier 1 | 1.490.332,69 | 0,00 | 0,00 | 0,00 | **1.490.332,69** |
| Aditya Rachman | Jakarta | Team | 272.727.273 | 370.958.352 | 136,02% | Tier 1 | 816.409,59 | 0,00 | 0,00 | 0,00 | **816.409,59** |
| Resti D Shaskiya | Jakarta | Team | 272.727.273 | 35.543.296 | 13,03% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Siti Rosnia Apriliyanti | Jakarta | Team | 272.727.273 | 152.352.975 | 55,86% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Yoppi Liehanto | Jakarta | Team | 272.727.273 | 78.832.775 | 28,91% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Asnita S Rangkuti | Medan | Team | 12.800.000 | 0 | 0,00% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Richard Wahyudi W (Medan) | Medan | Lead | 19.200.000 | 0 | 0,00% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Felicia Pranata | Surabaya | Team | 134.285.714 | 184.364.098 | 137,29% | Tier 1 | 1.226.330,01 | 0,00 | 0,00 | 0,00 | **1.226.330,01** |
| Melisa Kurniawan | Surabaya | Team | 134.285.714 | 15.173.410 | 11,30% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Richard Wahyudi Wiatmodjo | Surabaya | Lead | 201.428.571 | 143.502.457 | 71,24% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| **Total** | | | | | | | | | | | **8.486.663,77** |

Catatan Juni:

- **Asnita** masih punya target (resign 30 Jun), tetapi penjualannya di Juni 0.
- **Net Sales cabang Medan 30,8 jt berasal dari Mentari**, yang secara data belum aktif (baru mulai 1 Juli). Tier cabang Medan menjadi Tier 1, tetapi pool-nya 0, sehingga branch payout Medan 0.

### 7.2 Juli 2026 (rule Second Half, bertingkat)

| Cabang (B2B) | Branch Target | Net Sales Cabang | Achievement | Branch Tier | Rate | Pool (Payout Current tim) |
|---|---:|---:|---:|---|---:|---:|
| Bali | 2.100.000.000 | 1.496.570.922 | 71,27% | Tier 0 | 0% | 2.779.572,00 |
| Bandung | 550.527.716 | 81.808.767 | 14,86% | Tier 0 | 0% | 0,00 |
| Jakarta | 2.179.353.680 | 673.027.385 | 30,88% | Tier 0 | 0% | 0,00 |
| Medan | 32.000.000 | 28.488.275 | 89,03% | Tier 2 | 0,6% | 147.516,67 |
| Surabaya | 470.000.000 | 242.481.291 | 51,59% | Tier 0 | 0% | 516.064,25 |

| Karyawan | Cabang | Role | Target Incentive | Net Sales | Achievement | Tier | Payout Current | Payout Prior | Bonus | Branch | **Total** |
|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|
| Donny Iswahyudi | Bali | Team | 420.000.000 | 410.589.160 | 97,76% | Tier 3 | 2.779.572,00 | 102.768,00 | 0,00 | 0,00 | **2.882.340,00** |
| Agus Dwipayana | Bali | Team | 420.000.000 | 98.794.192 | 23,52% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Indri Rubiantini | Bandung | Team | 220.211.086 | 81.808.767 | 37,15% | Tier 0 | 0,00 | 9.686,25 | 0,00 | 0,00 | **9.686,25** |
| Ika Kurniati (Bandung) | Bandung | Lead | 330.316.630 | 0 | 0,00% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Ika Kurniati | Jakarta | Lead | 594.369.186 | 332.817.478 | 56,00% | Tier 0 | 0,00 | 684.337,50 | 0,00 | 0,00 | **684.337,50** |
| Aditya Rachman | Jakarta | Team | 396.246.124 | 26.943.116 | 6,80% | Tier 0 | 0,00 | 177.042,00 | 0,00 | 0,00 | **177.042,00** |
| Siti Rosnia Apriliyanti | Jakarta | Team | 396.246.124 | 150.579.534 | 38,00% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Sylvia Hidajat | Jakarta | Team | 396.246.124 | 2.065.500 | 0,52% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Yoppi Liehanto | Jakarta | Team | 396.246.124 | 147.515.630 | 37,23% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Mentari D Silalahi | Medan | Team | 12.800.000 | 28.488.275 | 222,56% | Tier 5 | 147.516,67 | 0,00 | 0,00 | 354,04 | **147.870,71** |
| Richard Wahyudi W (Medan) | Medan | Lead | 19.200.000 | 0 | 0,00% | Tier 0 | 0,00 | 0,00 | 0,00 | 531,06 | **531,06** |
| Felicia Pranata | Surabaya | Team | 104.444.444 | 90.945.908 | 87,08% | Tier 2 | 516.064,25 | 168.573,41 | 0,00 | 0,00 | **684.637,66** |
| Melisa Kurniawan | Surabaya | Team | 104.444.444 | 43.315.147 | 41,47% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Richard Wahyudi Wiatmodjo | Surabaya | Lead | 156.666.667 | 108.220.235 | 69,08% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| **Total** | | | | | | | | | | | **4.586.445,18** |

Branch Target Jakarta (2,18 M) dan Bandung (550,5 jt) di bulan Juli jauh lebih besar dari penjualan (31% dan 15%). Akibatnya hampir seluruh tim berada di Tier 0. **Pastikan angka Branch Target Juli ini benar.**

**Angka Juli di layar sekarang (3.444.038,02) berbeda dengan tabel di atas (4.586.445,18).** Juli sudah di-Calculate sebelum Juni dihitung, sehingga invoice Juni yang lunas di Juli belum ikut dibayar sebagai Payout Prior (Donny, Ika, Aditya, Felicia, Indri). Setelah Juni di-Calculate, **Juli harus di-Calculate ulang**.

**Contoh Mentari D Silalahi (Medan), Juli:**

| Langkah | Hasil |
|---|---:|
| Target | 32.000.000 × 1 ÷ 2,5 = 12.800.000,00 |
| Net Sales | 28.488.275 → 222,56% → **Tier 5 (0,7875%)** |
| Dikeluarkan (diskon 40–50%) | 5.590.050 |
| Lunas Juli | 18.732.275 |
| Payout Current = 18.732.275 × 0,7875% | 147.516,67 |
| Branch: Medan 89,03% → Tier 2 (0,60%); 147.516,67 × 1/2,5 × 0,60% | 354,04 |
| **Total** | **147.870,71** |

Invoice Juni Mentari yang lunas di Juli (INV/2026/03226, 03361, 03668) **tidak dibayar**. Pada bulan Juni dia belum aktif, jadi tidak punya tier, dan rate snapshot-nya 0.

---

## 8. Agustus 2026

### 8.1 Hasil per Cabang dan per Orang

| Cabang (B2B) | Branch Target | Net Sales Cabang | Achievement | Branch Tier | Rate | Pool (Payout Current tim) |
|---|---:|---:|---:|---|---:|---:|
| Bali | 2.100.000.000 | 694.596.342 | 33,08% | Tier 0 | 0% | 0,00 |
| Bandung | 550.527.716 | 64.972.690 | 11,80% | Tier 0 | 0% | 0,00 |
| Jakarta | 2.179.353.680 | 814.246.969 | 37,36% | Tier 0 | 0% | 1.751.388,18 |
| Medan | 32.000.000 | 80.286.650 | 250,90% | Tier 5 | 0,7875% | 430.130,73 |
| Surabaya | 470.000.000 | 354.878.383 | 75,51% | Tier 1 | 0,3% | 1.256.056,16 |

| Karyawan | Cabang | Role | Target Incentive | Net Sales | Achievement | Tier | Payout Current | Payout Prior | Bonus | Branch | **Total** |
|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|
| Donny Iswahyudi | Bali | Team | 420.000.000 | 308.639.223 | 73,49% | Tier 0 | 0,00 | 55.082,29 | 0,00 | 0,00 | **55.082,29** |
| Agus Dwipayana | Bali | Team | 420.000.000 | 168.073.125 | 40,02% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Ika Kurniati (Bandung) | Bandung | Lead | 330.316.630 | 0 | 0,00% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Indri Rubiantini | Bandung | Team | 220.211.086 | 64.972.690 | 29,50% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Aditya Rachman | Jakarta | Team | 396.246.124 | 322.980.119 | 81,51% | Tier 1 | 1.751.388,18 | 0,00 | 0,00 | 0,00 | **1.751.388,18** |
| Ika Kurniati | Jakarta | Lead | 594.369.186 | 188.740.129 | 31,75% | Tier 0 | 0,00 | 201.525,00 | 0,00 | 0,00 | **201.525,00** |
| Siti Rosnia Apriliyanti | Jakarta | Team | 396.246.124 | 226.772.647 | 57,23% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Sylvia Hidajat | Jakarta | Team | 396.246.124 | 15.431.750 | 3,89% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Yoppi Liehanto | Jakarta | Team | 396.246.124 | 60.322.324 | 15,22% | Tier 0 | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** |
| Mentari D Silalahi | Medan | Team | 12.800.000 | 80.286.650 | 627,24% | Tier 5 | 430.130,73 | 32.806,86 | 0,00 | 1.354,91 | **464.292,50** |
| Richard Wahyudi W (Medan) | Medan | Lead | 19.200.000 | 0 | 0,00% | Tier 0 | 0,00 | 0,00 | 0,00 | 2.032,37 | **2.032,37** |
| Felicia Pranata | Surabaya | Team | 104.444.444 | 125.381.853 | 120,05% | Tier 4 | 741.798,33 | 21.499,95 | 79.517,59 | 1.076,62 | **843.892,50** |
| Richard Wahyudi Wiatmodjo | Surabaya | Lead | 156.666.667 | 184.380.844 | 117,69% | Tier 4 | 514.257,82 | 0,00 | 171.573,25 | 1.614,93 | **687.446,00** |
| Melisa Kurniawan | Surabaya | Team | 104.444.444 | 45.115.685 | 43,20% | Tier 0 | 0,00 | 0,00 | 0,00 | 1.076,62 | **1.076,62** |
| **Total** | | | | | | | | | | | **4.006.735,46** |

### 8.2 Contoh Detail: Felicia Pranata (Surabaya) — ada kursi kosong

Surabaya punya record **Vacant Surabaya B2B** (1 kursi kosong). Target cabang 470 jt dibagi ke 4,5 FTE (Richard 1,5 + Felicia 1 + Melisa 1 + kursi kosong 1). Porsi kursi kosong dibagikan sebagai **target bonus** ke tim yang aktif.

| Langkah | Hasil |
|---|---:|
| Target Incentive = 470.000.000 × 1 ÷ 4,5 | 104.444.444,44 |
| Target Bonus (porsi kursi kosong × 1 ÷ 3,5) | 29.841.269,84 |
| Net Sales | 125.381.853 → 120,05% → **Tier 4 (0,75%)**. Mixed → maksimal Tier 4 |
| Eligible: bucket incentive / bucket bonus | 104.444.444 / 20.937.409 |
| Lunas Agustus: incentive × 0,75% | 98.906.444 × 0,75% = 741.798,33 |
| Lunas Agustus: bonus × 1% | 7.951.759 × 1% = 79.517,59 |
| Invoice Juli yang lunas Agustus (rate Juli) | 21.499,95 |
| Branch: Surabaya 75,51% → Tier 1 (0,30%); 1.256.056,16 × 1/3,5 × 0,30% | 1.076,62 |
| **Total** | **843.892,50** |

### 8.3 Contoh Detail: Mentari D Silalahi (Medan), Agustus

| Langkah | Hasil |
|---|---:|
| Net Sales | 80.286.650 → 627,24% → Tier 5 (0,7875%) |
| Dikeluarkan (diskon 40%) | 18.612.000 |
| Lunas Agustus → Payout Current | 54.619.775 × 0,7875% = 430.130,73 |
| Invoice Juli yang lunas Agustus → Payout Prior (rate Juli 0,7875%) | 4.165.950 × 0,7875% = 32.806,86 |
| Branch: Medan 250,90% → Tier 5; 430.130,73 × 1/2,5 × 0,7875% | 1.354,91 |
| **Total** | **464.292,50** |

Invoice Juni Mentari yang lunas di Agustus (INV/2026/03661, 03731) juga tidak dibayar, karena bulan Juni tidak punya tier untuknya. Invoice Agustus yang lunas di September (INV/2026/04835, 04834, 04827, 04949, 05251) akan dibayar di periode September.

---

## 9. Status Data di vanialook Sekarang

| Periode | Status | Isi |
|---|---|---|
| Jan 2026 | Calculated (**hitungan lama**) | Backfill sudah jalan, tetapi Calculate ulang **ditolak** (Yogi, Nurul). Angka di layar masih yang lama |
| Feb 2026 | Open | Periode, Branch Target (asumsi), cascade, dan backfill sudah dibuat. Calculate ditolak (Dzulfikcar, Yogi, Karina) |
| Jun 2026 | Open | Sama seperti Februari. Calculate ditolak (Dzulfikcar, Yogi) |
| Jul 2026 | **Calculated** | Rule Second Half diisi, Branch Target Bali/Medan/Surabaya (asumsi) ditambahkan. Payout Prior dari Juni belum masuk (§7.2) |
| Agu 2026 | Open | Periode, Branch Target (asumsi), cascade, dan backfill sudah dibuat. Calculate ditolak (Deriansyah, Dzulfikcar) |

## 10. Langkah Perbaikan (berurutan)

1. Lengkapi data 5 orang di bagian 6, dan cek temuan lain di tabel yang sama.
2. Pastikan **Branch Target** setiap bulan sesuai rolling forecast yang sebenarnya, terutama Jakarta dan Bandung di bulan Juli.
3. Buat periode **Mar, Apr, Mei 2026**: isi Branch Target, cascade, lalu backfill.
4. Jalankan **Calculate berurutan dari bulan paling awal**: Jan → Feb → Mar → Apr → Mei → Jun → Jul → Agu. Urutan ini penting, karena rate bulan asal invoice harus sudah ada sebelum bulan pelunasannya dihitung.
5. Review, **Approve**, lalu **Lock** setiap bulan sebelum menghitung bulan berikutnya, supaya carry-forward ikut terbawa.

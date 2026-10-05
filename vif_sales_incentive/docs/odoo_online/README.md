# Memindahkan VIF Sales Incentive ke Odoo Online (Studio + Execute Code)

Panduan ini memindahkan modul Python `vif_sales_incentive` ke **Odoo Online (SaaS, Odoo 19)**. Di Odoo Online tidak bisa memasang modul Python sendiri, jadi:

| Di modul Python | Di Odoo Online |
|---|---|
| Model `incentive.*` | Model custom `x_incentive_*` (Settings → Technical → Models) |
| Field Python | Field custom `x_*` |
| Method / tombol (`action_calculate`, dst.) | **Server Action → Execute Code** |
| `@api.constrains`, `_sql_constraints` | **Automation Rule → Execute Code** (raise `UserError`) |
| Override `_post`, `_generate_pos_order_invoice` | Automation Rule, atau diambil saat Calculate |
| XML view / menu / security | Dibuat dari menu Technical (XML disediakan), lalu dirapikan dengan Studio |

Semua kode dan XML di folder ini **sudah diuji** di salinan database klien (`vaniaeut_online`): model dibuat persis seperti langkah di bawah, lalu hasilnya dibandingkan dengan modul Python pada periode Sept 26. Detailnya ada di [bagian 13](#13-hasil-uji-yang-sudah-dilakukan).

---

## Isi Folder

```
docs/odoo_online/
├── README.md              <- panduan ini
├── FIELDS.md              <- daftar lengkap model & field (checklist pembuatan)
├── spec.py                <- sumber data FIELDS.md + daftar action / view / menu / security
├── compute/*.py           <- kode untuk field Compute
├── actions/*.py           <- kode Server Action (tombol)
├── automations/*.py       <- kode Automation Rule (validasi & otomatisasi)
├── views/*.xml            <- XML view form / list / search
├── data/*.csv             <- template import data awal
├── build_test_db.py       <- membangun semua ini otomatis di DATABASE UJI (odoo shell)
└── render_fields_md.py    <- generate ulang FIELDS.md dari spec.py
```

---

## 0. Aturan Penting Odoo Online (baca dulu)

Kode "Execute Code" dijalankan dengan `safe_eval`, yang **lebih ketat** dari Python biasa. Semua kode di folder ini sudah mematuhi aturan berikut. Kalau Anda mengubah kodenya nanti, tetap patuhi aturan ini:

1. **Tidak boleh `record.field = nilai`.** Odoo 19 menolak opcode `STORE_ATTR`. Pakai:
   - `record.write({'x_field': nilai})`, atau
   - `record['x_field'] = nilai` (dipakai di kode Compute).
2. **Di dalam `def`, jangan pakai `lambda`, list comprehension, atau generator yang membaca variabel lokal `def` tersebut.** Error-nya `forbidden opcode(s): LOAD_CLOSURE, MAKE_CELL`. Di luar `def` (kode level atas) semua itu boleh. Di dalam `def` pakai `for` biasa.
3. **Tidak ada `import`.** Yang tersedia:
   - Server Action / Automation: `env`, `record`, `records`, `model`, `UserError`, `Command`, `float_compare`, `datetime`, `dateutil`, `time`, `log`, `_logger`.
   - Compute: `self`, `datetime`, `dateutil`, `time` (`env` diakses lewat `self.env`).
4. **Nilai kembali Server Action** disimpan di variabel `action = {...}`, misalnya untuk membuka form.
5. **Satu kode Compute = satu field.** Kode yang mengisi dua field akan error selama field kedua belum dibuat.
6. **`x_name` dibuat otomatis** oleh Odoo di setiap model baru. Kalau `x_name` perlu Compute, *edit* field yang sudah ada.
7. **Many2one yang Required** harus memakai On Delete **Restrict** atau **Cascade** (Set Null ditolak).
8. **Jangan membuat field Compute tersimpan di tabel besar** seperti `account.move`. Odoo akan langsung menghitungnya untuk semua record, dan ini bisa timeout. Karena itu "Incentive Salesperson" di invoice diisi oleh Automation Rule.
9. **Siapkan field Compute sebelum data diinput.** Mengubah kode Compute pada field yang sudah punya data tidak menghitung ulang data lama.

---

## 1. Persiapan

1. **Uji di database duplikat dulu.** Di [odoo.com/my/databases](https://www.odoo.com/my/databases), pilih database → **Duplicate**. Kerjakan semua langkah di duplikat, uji, baru ulangi di database produksi.
2. Pastikan app berikut terpasang: **Employees, Sales, Project, Invoicing/Accounting, Point of Sale, Studio**. Di POS, aktifkan **Log in with Employees** (lihat panduan user §14.1).
3. Aktifkan **Developer Mode**: Settings → paling bawah → *Activate the developer mode*. Menu **Settings → Technical** baru muncul setelah ini.
4. **Cek model lama.** Database klien saat ini sudah punya model Studio `x_incentive_tiering`, `x_incentive_tiering_pe`, `x_incentive_tiering_line_8f5fd`, dan `x_incentive_tracker`. Kemungkinan ini percobaan sebelumnya. Namanya **tidak bentrok** dengan model baru, jadi biarkan saja. Tanyakan ke tim apakah model itu masih dipakai sebelum ada yang menghapusnya.
5. Field Studio di Project (`x_studio_salesperson_2`, `x_studio_salesperson_3`, `x_studio_komisi_pm`, `x_studio_komisi_salesperson_2`, `x_studio_komisi_salesperson_3`) **sudah ada** dan langsung dipakai engine. Jika nama teknisnya berbeda di database produksi, ubah `PROJECT_SLOTS` di bagian atas `actions/sa_engine_calculate.py`.

---

## 2. Membuat Model

**Menu:** Settings → Technical → Database Structure → **Models** → **New**

Untuk setiap model di [FIELDS.md](FIELDS.md), dengan urutan yang sama:

1. **Model Description**: isi label, misalnya `Incentive Period`
2. **Model**: isi nama teknis persis, misalnya `x_incentive_period`
3. **Chatter** (sama seperti modul): centang **Has Mail Thread** di model berikut. Kalau modelnya sudah terlanjur dibuat, buka lagi dan centang sekarang, karena data lama tetap aman. Setelah dicentang, Odoo tidak mengizinkannya dimatikan lagi.

   | Model | Has Mail Thread | Has Mail Activity |
   |---|---|---|
   | `x_incentive_period` | ✓ | ✓ |
   | `x_incentive_payout` | ✓ | |
   | `x_incentive_target` | ✓ | |
   | `x_incentive_target_movement` | ✓ | |
4. **Save**. Odoo otomatis menambahkan field `x_name`.
5. Buka tab **Fields**, lalu tambah field sesuai tabel (lihat bagian 3)
6. **Order** (urutan default list, sama dengan `_order` modul): setelah **semua** field model itu dibuat, isi field **Order** di form Model sesuai baris *Order* di `FIELDS.md`. Contohnya `x_date_start desc` untuk Period. Odoo menolak Order yang menyebut field yang belum ada.

Urutan pembuatan (sesuai `FIELDS.md`):
1. `x_incentive_designation`
2. `x_incentive_branch`
3. field di `hr.employee` (bagian 4)
4. field di `account.move` dan `account.move.line`
5. `x_incentive_rule`
6. `x_incentive_rule_tier`
7. `x_incentive_period`
8. `x_incentive_branch_target`
9. `x_incentive_target`
10. `x_incentive_target_movement`
11. `x_incentive_transaction`
12. `x_incentive_payout`
13. `x_incentive_cascade`
14. `x_incentive_cascade_line`
15. `x_incentive_refund`
16. `x_incentive_refund_policy`
17. terakhir: tabel **"One2many & field yang membacanya"** di `FIELDS.md`, dari atas ke bawah. Field Compute di tabel itu (jumlah & FTE di Branch; total & jumlah Targets/Payouts/Transactions di Period) membaca One2many di atasnya, jadi harus dibuat sesudahnya.

---

## 3. Membuat Field

**Menu:** di form Model → tab **Fields** → *Add a line*. Bisa juga lewat Settings → Technical → Database Structure → **Fields** → New.

Isi sesuai kolom di `FIELDS.md`:

| Kolom FIELDS.md | Diisi di form Field |
|---|---|
| Field Name | **Field Name** (harus diawali `x_`) |
| Label | **Field Label** |
| Type | **Field Type** |
| Model: `...` | **Related Model** (untuk Many2one / One2many / Many2many) |
| Field relasi: `...` | **Relation Field** (khusus One2many) |
| On Delete | **On Delete** |
| Nilai: `a`=A, ... | tab **Selection Options**: satu baris per nilai (Value = `a`, Name = `A`) |
| Related: `x.y` | **Related Field** (tab Advanced Properties). Centang **Stored** jika tertulis Stored |
| Compute `compute/xxx.py` | tab **Advanced Properties** → **Dependencies** = isi *Depends*, **Compute** = isi file `compute/xxx.py`. **Stored** sesuai tabel. Jika tertulis *editable*, matikan **Readonly** |
| Required / Readonly / Indexed | centang yang sesuai |
| Currency field: `x_currency_id` | **Currency field** = `x_currency_id` (buat `x_currency_id` lebih dulu) |
| Tracking: `10` | **Enable Ordered Tracking** = angka tersebut (urutan tampil di chatter). Hanya di model yang Has Mail Thread |

Tips:
- **Many2many** `x_incentive_cascade.x_branch_ids`: biarkan Odoo mengisi Relation Table otomatis, atau isi `x_incentive_branch_x_incentive_cascade_rel`.
- Setelah Save, pastikan field muncul tanpa error. Kalau ada error di kode Compute, Odoo akan menolak saat Save.

---

## 4. Field di Model Standar

Masih lewat Settings → Technical → Fields → New, dengan **Model** = model standar:

- **Employee (`hr.employee`)**: 9 field incentive. Dua di antaranya Compute (`x_branch_incentive_eligible`, `x_individual_incentive_eligible`) dengan **Stored** dan **Readonly OFF**.
- **Journal Entry (`account.move`)**: `x_incentive_employee_id` (Many2one ke Employee, **bukan** Compute) dan `x_incentive_full_payment_date` (Compute, **Not stored**).
- **Journal Item (`account.move.line`)**: `x_incentive_eligible` (Compute, **Not stored**), kolom "Inc. Eligible" di baris invoice.
- Kedua Compute di tabel besar ini sengaja **tidak disimpan** (Stored OFF). Kalau Stored dicentang, Odoo menghitungnya untuk semua journal entry sekaligus dan bisa timeout (aturan 8).
- Setelah semua model ada: field One2many di `account.move`, `pos.order`, dan `hr.employee` (tabel "One2many" di akhir `FIELDS.md`).

---

## 5. Default Value dan Sequence

1. **Default value**: Settings → Technical → Actions → **User-defined Defaults** → New (Field, Default Value dalam JSON, misalnya `"draft"`, `0.0075`, `true`). Bisa juga lewat Studio: klik field → *Default value*. Daftarnya ada di akhir `FIELDS.md`. Ingat default `x_company_id` = company Anda.
2. **Sequence** untuk nomor Target Movement: Settings → Technical → Sequences & Identifiers → **Sequences** → New
   - Name: `Incentive Target Movement`
   - Sequence Code: `x_incentive_target_movement`
   - Prefix: `TMV/%(year)s/`
   - Padding: `5`

---

## 6. Server Action (tombol)

**Menu:** Settings → Technical → Actions → **Server Actions** → New

Untuk setiap baris di tabel berikut:

1. **Action Name**: persis seperti kolom Name. Beberapa action mencari action lain berdasarkan nama.
2. **Model**: sesuai kolom Model
3. **Type** (*Action To Do*): **Execute Code**
4. **Code**: paste isi file dari folder `actions/`
5. Save, lalu **catat ID-nya**. ID terlihat di URL (`.../server-action/123`) atau lewat ikon bug → *View Metadata*.

| Name | Model | File | Tombol di |
|---|---|---|---|
| `VIF: Engine Calculate` | `x_incentive_period` | `sa_engine_calculate.py` | Period → Calculate |
| `VIF: Period Open` | `x_incentive_period` | `sa_period_open.py` | Period → Open |
| `VIF: Period Approve` | `x_incentive_period` | `sa_period_approve.py` | Period → Approve |
| `VIF: Period Lock` | `x_incentive_period` | `sa_period_lock.py` | Period → Lock |
| `VIF: Period Reset to Open` | `x_incentive_period` | `sa_period_reset.py` | Period → Reset |
| `VIF: Period Generate Next` | `x_incentive_period` | `sa_period_generate_next.py` | Period → Create Next Month |
| `VIF: Period View Targets` | `x_incentive_period` | `sa_period_view_targets.py` | Period → smart button Targets |
| `VIF: Period View Transactions` | `x_incentive_period` | `sa_period_view_transactions.py` | Period → smart button Transactions |
| `VIF: Period View Payouts` | `x_incentive_period` | `sa_period_view_payouts.py` | Period → smart button Payouts |
| `VIF: Payout Recompute` | `x_incentive_payout` | `sa_payout_recompute.py` | Payout → Recompute |
| `VIF: Payout View Transactions` | `x_incentive_payout` | `sa_payout_view_transactions.py` | Payout → smart button Transactions |
| `VIF: Branch Target Calculate` | `x_incentive_branch_target` | `sa_bt_calculate.py` | Branch Target → Calculate |
| `VIF: Branch Target Approve` | `x_incentive_branch_target` | `sa_bt_approve.py` | Branch Target → Approve |
| `VIF: Branch Target Lock` | `x_incentive_branch_target` | `sa_bt_lock.py` | Branch Target → Lock |
| `VIF: Branch Target Reset to Draft` | `x_incentive_branch_target` | `sa_bt_reset.py` | Branch Target → Reset |
| `VIF: Cascade Preview` | `x_incentive_cascade` | `sa_cascade_preview.py` | Cascade → Preview |
| `VIF: Cascade Apply` | `x_incentive_cascade` | `sa_cascade_apply.py` | Cascade → Apply |
| `VIF: Target Movement Apply` | `x_incentive_target_movement` | `sa_movement_apply.py` | Movement → Apply |
| `VIF: Transaction Refund` | `x_incentive_transaction` | `sa_tx_open_refund.py` | Transaction → Create Credit Note |
| `VIF: Refund Confirm` | `x_incentive_refund` | `sa_refund_confirm.py` | Refund → Create Credit Note |
| `VIF: Backfill Invoice Salesperson` | `x_incentive_period` | `sa_backfill_incentive_employee.py` | dijalankan sekali (bagian 11) |

Untuk `VIF: Backfill Invoice Salesperson`, klik **Create Contextual Action** supaya muncul di menu ⚙ Actions pada list Period.

### Apa isi Engine Calculate?

`sa_engine_calculate.py` adalah pengganti seluruh mesin modul Python, dalam satu action. Urutannya sama persis:

1. **Guard**: periode harus Open, punya Rule, tidak Locked, dan tidak ada tim yang perlu di-cascade ulang.
2. **Transaksi invoice**: satu baris per invoice line per orang yang dapat kredit.
   - **Split project** PM / SP2 / SP3 sesuai persen komisi.
   - Bagian SP2/SP3 yang belum punya branch atau target **dialihkan ke PM**.
   - Credit note dibagi sama seperti invoice asalnya.
   - Stempel pembayaran (lunas di periode mana), lalu menghubungkan credit note ke invoice asalnya.
3. **Transaksi POS**: order yang tidak dibuatkan invoice.
   - Retur bernilai minus dan terhubung ke penjualan asalnya.
   - Order di **tanggal terakhir periode ikut terhitung** (lihat bagian 14).
4. **Blokir**: Calculate ditolak jika ada orang dengan penjualan tanpa Sales Branch atau target.
5. **Payout individual**:
   - SQ1: tier dari semua invoice
   - SQ2: base yang eligible, diisi ke bucket incentive dulu lalu bonus
   - SQ3: hanya yang lunas; invoice periode lalu memakai rate tier periode asalnya
6. **Payout branch**: pool dibagi berdasarkan FTE × rate tier branch; global member ikut di semua branch.
7. Hitung total, lalu ubah status menjadi **Calculated**.

Tombol **Recompute** di Payout memakai engine yang sama dengan context `vif_recompute_payout_id`. Engine hanya menjalankan langkah 5 untuk orang itu, ditambah totalnya. Transaksi tidak dibuat ulang, branch payout tidak dihitung, dan status tidak berubah. Perilakunya sama dengan `action_recompute` di modul.

---

## 7. Automation Rule (validasi & otomatisasi)

**Menu:** Settings → Technical → Automation → **Automation Rules** → New

Untuk setiap baris:
- **Model**
- **Trigger** = *On create and edit* (atau *On create*)
- **When updating** = field pada kolom Trigger Fields
- **Actions To Do** → Add → **Execute Code** → paste isi file dari folder `automations/`

| Name | Model | Trigger | Trigger Fields | File |
|---|---|---|---|---|
| `VIF: Check Target` | `x_incentive_target` | On create and edit | Period, Employee, Bucket, Amount | `au_check_target.py` |
| `VIF: Check Branch Target` | `x_incentive_branch_target` | On create and edit | Period, Branch, Business Type | `au_check_branch_target.py` |
| `VIF: Check Period` | `x_incentive_period` | On create and edit | Start Date, End Date, Company | `au_check_period.py` |
| `VIF: Check Tier Ranges` | `x_incentive_rule_tier` | On create and edit | Achievement From, Achievement To, Rule | `au_check_tier.py` |
| `VIF: Check Same-Day Handover` | Employee | On create and edit | Sales Branch, Business Type, Effective Target Start, Resignation Date | `au_check_employee.py` |
| `VIF: Target Movement Reference` | `x_incentive_target_movement` | On create | – | `au_movement_name.py` |
| `VIF: Invoice Incentive Salesperson` | Journal Entry | On create and edit | Salesperson (`invoice_user_id`) | `au_move_incentive_employee.py` |
| `VIF: POS Invoice Cashier` | Point of Sale Orders | On create and edit | Invoice (`account_move`) | `au_pos_invoice_cashier.py` |
| `VIF: POS Journal Analytic Tags` | Point of Sale Orders | On create and edit | Invoice (`account_move`) | `au_pos_journal_analytic.py` |

`au_pos_journal_analytic.py` is **not** part of the Sales Incentive engine -- it
just lives here because this folder is the Odoo Online Execute Code reference.
It fixes the gap where a POS-generated Journal Entry has no Analytic
Distribution (Project / Branch / Business Type), unlike a Sales Order invoice
tagged by hand. Tested 2026-10-02 against `vaniaeut_online` via `odoo-bin
shell` (ran the real code on a POS invoice, rolled back): tags every
previously-empty line correctly, is idempotent on a second run, never
overwrites a line already tagged by hand, and skips safely (no crash) when
the Branch field is empty. See the comment header in the file for the
confirmed field/account IDs for that database -- re-check them if this runs
anywhere else.

---

## 8. View (form, list, search, pivot, graph)

**Menu:** Settings → Technical → User Interface → **Views** → New

Setiap file di `views/` adalah terjemahan **1:1** dari view modul (`vif_sales_incentive/views/*.xml` dan `wizards/*_views.xml`). Field, kolom, tombol, smart button, tab, filter, group by, dekorasi warna, dan chatter-nya sama; yang berbeda hanya awalan `x_` dan tombol yang memanggil server action.

1. **View Name** dan **View Type** (Form / List / Search / Pivot / Graph) sesuai tabel
2. **Model**: nama teknis model
3. **Architecture**: paste isi file dari folder `views/`
4. **Ganti setiap `[ID Nama Action]`** dengan ID server action dari bagian 6. Contoh: `name="[ID VIF: Engine Calculate]"` menjadi `name="512"`.
5. Untuk view **inherit** (baris dengan kolom Inherit terisi): isi **Inherited View** sesuai kolom Inherit. View ini menambah tab "Sales Incentive" di form Employee; field "Incentive Salesperson", "Fully Paid On", dan kolom "Inc. Eligible" di invoice; serta daftar transaksi insentif di bawah Cashier pada order POS.

| File | Model | Type | Inherit |
|---|---|---|---|
| `period_form.xml` / `period_list.xml` | `x_incentive_period` | form / list | |
| `branch_target_form.xml` / `branch_target_list.xml` / `branch_target_search.xml` | `x_incentive_branch_target` | form / list / search | |
| `cascade_form.xml` / `cascade_list.xml` | `x_incentive_cascade` | form / list | |
| `target_list.xml` / `target_search.xml` | `x_incentive_target` | list (editable) / search | |
| `movement_form.xml` / `movement_list.xml` | `x_incentive_target_movement` | form / list | |
| `transaction_form.xml` / `transaction_list.xml` / `transaction_search.xml` / `transaction_pivot.xml` | `x_incentive_transaction` | form / list / search / pivot | |
| `payout_form.xml` / `payout_list.xml` / `payout_search.xml` / `payout_pivot.xml` / `payout_graph.xml` | `x_incentive_payout` | form / list / search / pivot / graph | |
| `refund_form.xml` | `x_incentive_refund` | form | |
| `rule_form.xml` / `rule_list.xml` | `x_incentive_rule` | form / list | |
| `branch_form.xml` / `branch_list.xml` | `x_incentive_branch` | form / list | |
| `designation_list.xml` | `x_incentive_designation` | list (editable) | |
| `refund_policy_list.xml` | `x_incentive_refund_policy` | list (editable) | |
| `employee_form_inherit.xml` | `hr.employee` | form | `hr.employee.form` (hr.view_employee_form) |
| `move_form_inherit.xml` | `account.move` | form | `account.move.form` (account.view_move_form) |
| `pos_order_form_inherit.xml` | `pos.order` | form | `pos.order.form` (point_of_sale.view_pos_pos_form) |

Setelah view ada, **Studio** bisa dipakai untuk merapikan tampilan (pindah kolom, ganti label). Studio menyimpan perubahannya sebagai view turunan, jadi view di atas tetap aman.

---

## 9. Window Action & Menu

1. **Window Actions**: Settings → Technical → Actions → **Window Actions** → New. Isi Action Name, **Model** (Object), View Mode, dan Domain/Context:

   | Action Name | Model | View Mode | Domain | Context |
   |---|---|---|---|---|
   | Incentive Periods | `x_incentive_period` | list,form | | |
   | Branch Targets | `x_incentive_branch_target` | list,form | | |
   | Cascade Branch Target | `x_incentive_cascade` | list,form | | |
   | Incentive Targets | `x_incentive_target` | list,form | | |
   | Target Movements | `x_incentive_target_movement` | list,form | | |
   | Incentive Payouts | `x_incentive_payout` | list,pivot,graph,form | | |
   | My Incentive | `x_incentive_payout` | list,form | `[('x_user_id', '=', uid)]` | |
   | Incentive Transactions | `x_incentive_transaction` | list,pivot,form | | |
   | Incentive Rules | `x_incentive_rule` | list,form | | |
   | Sales Branches | `x_incentive_branch` | list,form | | |
   | FTE Designations | `x_incentive_designation` | list,form | | |
   | Refund Policies | `x_incentive_refund_policy` | list,form | | |

   Search view tidak perlu dipilih di action. Setiap model hanya punya satu search view, dan Odoo otomatis memakainya.

2. **Menu**: Settings → Technical → User Interface → **Menu Items** → New. Susunan, urutan (Sequence), dan Groups-nya sama dengan modul:

   ```
   Sales Incentive  (seq 85, Groups: VIF Incentive / Salesperson)
   ├── Operations  (seq 10)
   │   ├── My Incentive           (5)  -> My Incentive
   │   ├── Incentive Periods      (10) -> Incentive Periods        [Administrator]
   │   ├── Targets                (20) -> Incentive Targets
   │   ├── Cascade Branch Target  (25) -> Cascade Branch Target    [Administrator]
   │   ├── Branch Targets         (27) -> Branch Targets           [Administrator]
   │   └── Target Movements       (30) -> Target Movements         [Administrator]
   ├── Reporting  (seq 20)
   │   ├── Payouts                (10) -> Incentive Payouts
   │   └── Transactions           (20) -> Incentive Transactions
   └── Configuration  (seq 90, Groups: VIF Incentive / Administrator)
       ├── Rules & Tiers          (10) -> Incentive Rules
       ├── Sales Branches         (20) -> Sales Branches
       ├── FTE Designations       (30) -> FTE Designations
       └── Refund Policies        (40) -> Refund Policies
   ```
   `[Administrator]` = isi **Groups** menu itu dengan `VIF Incentive / Administrator`. Group baru dibuat di bagian 10, jadi isi Groups menu setelah bagian 10 selesai.

---

## 10. Security

1. **Groups**: Settings → Users & Companies → **Groups** → New
   - `VIF Incentive / Salesperson`
   - `VIF Incentive / Manager`: tab *Inherited* = Salesperson
   - `VIF Incentive / Administrator`: tab *Inherited* = Manager
2. **Access Rights**: di form group → tab **Access Rights**
   - **Administrator**: Read, Write, Create, Delete di **semua** model `x_incentive_*`
   - **Salesperson**: **Read saja** di `x_incentive_branch`, `x_incentive_branch_target`, `x_incentive_designation`, `x_incentive_period`, `x_incentive_rule`, `x_incentive_rule_tier`, `x_incentive_target`, `x_incentive_target_movement`, `x_incentive_refund_policy`, `x_incentive_transaction`, `x_incentive_payout`
   - Cek tab **Access Rights** di setiap model baru. Jika Odoo menambahkan baris akses otomatis, baris untuk *Administration / Settings* boleh dibiarkan. Hapus baris yang memberi akses ke semua *Internal User* atau yang tanpa grup, supaya record rule VIF berlaku.
3. **Record Rules**: Settings → Technical → Security → **Record Rules** → New. Berlaku untuk model `x_incentive_payout`, `x_incentive_target`, dan `x_incentive_transaction`:

   | Group | Domain |
   |---|---|
   | Salesperson (data sendiri) | `[('x_employee_id.user_id', '=', user.id)]` |
   | Manager (sendiri + bawahan) | `['\|', ('x_employee_id.user_id', '=', user.id), ('x_employee_id', 'child_of', user.employee_id.id)]` |
   | Administrator (semua) | `[(1, '=', 1)]` |

4. Tambahkan user ke grupnya: Finance/Admin → Administrator, Sales Manager → Manager, Sales → Salesperson.

---

## 11. Data Awal

Import CSV dari folder `data/` lewat: buka list view → ⚙ → **Import records** → upload → cek mapping kolom → **Import**.

| Urutan | File | Ke menu |
|---|---|---|
| 1 | `1_designations.csv` | Configuration → FTE Designations |
| 2 | `2_branches.csv` | Configuration → Sales Branches |
| 3 | `3_rules.csv` | Configuration → Rules & Tiers |
| 4 | `4_tiers.csv` | Settings → Technical → Models → `x_incentive_rule_tier` (kolom `x_rule_id` diisi nama rule) |
| 5 | Data karyawan | Employees → export ID karyawan dulu, isi kolom `x_incentive_*`, lalu import ulang (contoh: `5_employees_example.csv`) |

Setelah itu:
1. Buat **Incentive Period** untuk bulan berjalan, pilih Rule, lalu klik **Open**.
2. Isi **Branch Targets**, lalu jalankan **Cascade Branch Target** (Preview → Apply).
3. Jalankan **VIF: Backfill Invoice Salesperson** sekali pada periode yang akan dihitung (⚙ Actions di list Period), supaya invoice yang dibuat sebelum automation rule aktif punya Incentive Salesperson.
4. Klik **Calculate**.

Isi CSV sudah disamakan dengan konfigurasi di database klien sekarang (designation Lead/Team/Support/Head, 5 branch, 2 rule). Cek ulang sebelum import.

---

## 12. Operasional Bulanan

Sama seperti panduan user (`PANDUAN_USER_VIF_SALES_INCENTIVE.md`). Menu, tombol, dan label kolomnya sama. Penjelasan rumus setiap angka juga berlaku di Online: contoh perhitungan lengkap ada di **§32**, dan kamus rumus setiap kolom Target / Payout / Transaction ada di **§33**. Perbedaannya hanya:
- **Credit note** baru masuk transaksi insentif saat **Calculate** berikutnya. Di modul Python, credit note langsung masuk saat di-post. Hasil akhirnya sama.
- Kalau Calculate satu periode terasa lambat atau timeout, lihat bagian 14.

---

## 13. Hasil Uji yang Sudah Dilakukan

Diuji di `vaniaeut_online` (salinan database klien, Odoo 19). Semua model dan kode dibuat oleh `build_test_db.py` persis sesuai spesifikasi, lalu dijalankan berdampingan dengan modul Python:

| Uji | Hasil |
|---|---|
| Semua kode lolos validator `safe_eval` Odoo 19 | 36 file (12 compute, 16 action, 8 automation), 0 error |
| Semua view bisa dibuat dan dirender | 25 view OK |
| Sept 26 data asli: transaksi (split project, retur POS, credit note) | 41 = 41 transaksi, **0 selisih** |
| Sept 26 target diperkecil: payout Tier 4, bucket bonus, branch payout, global member (Kenny) | **0 selisih** di 16 kolom × 8 karyawan |
| Refund parsial 10 juta dari tombol Transaction | Credit note terbentuk, baris refund terhubung, payout turun, **0 selisih** dengan Python |
| Cascade preview Sept 26 B2B | 7 = 7 baris, **0 selisih** |
| Blokir: karyawan tanpa branch, branch/periode locked, refund dobel | Semua ditolak dengan pesan yang benar |
| Calculate / Approve / Lock per branch & per periode, Generate Next | OK. Shortfall terisi saat Lock |
| Automation: target dobel, periode tumpang tindih, tier tumpang tindih, nomor movement | Semua OK |

Untuk mengulang uji di database lain:
```
odoo-bin shell -c odoo.conf -d <db_salinan> --no-http < vif_sales_incentive/docs/odoo_online/build_test_db.py
```

---

## 14. Perbedaan dengan Modul Python & Hal yang Perlu Diperhatikan

1. **Order POS di hari terakhir periode**: modul Python memakai `date_order <= tanggal_akhir`, sehingga order tanggal 30 setelah jam 00:00 **tidak ikut** di periode mana pun. Versi Online memakai `< tanggal_akhir + 1 hari`, jadi order itu ikut. Modul Python sebaiknya ikut diperbaiki.
2. **Calculate per Branch** di versi Online juga memperbarui transaksi POS. Di modul Python, hanya Calculate periode yang memperbarui POS.
3. **Credit note** masuk saat Calculate, bukan saat di-post (hasil sama).
4. **Kolom "Incentive Eligible" di baris invoice** (tampilan saja) tidak dipindahkan. Status diskon > 35% tetap terlihat di menu Transactions.
5. **Batas waktu request Odoo Online.** Calculate berjalan dalam satu klik (satu request). Untuk volume sekarang (41 transaksi/bulan) sangat cepat. Jika nanti ribuan baris per bulan dan muncul timeout, pecah perhitungan menjadi per branch, atau jalankan lewat **Scheduled Action** (limit waktunya lebih panjang).
6. **Tidak ada chatter/tracking.** Aktifkan lewat Studio (*Chatter*) jika perlu riwayat perubahan target.
7. **Refund Policy** tetap hanya tabel referensi, sama seperti di modul Python.

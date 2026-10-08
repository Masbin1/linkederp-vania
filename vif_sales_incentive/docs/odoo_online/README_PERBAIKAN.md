# README Perbaikan -- VIF Sales Incentive (Odoo Online / Studio)

Dokumen ini **khusus untuk membetulkan konfigurasi yang salah** pada database
yang sudah dibangun mengikuti `README.md` + `FIELDS.md`. Dokumen ini bukan
panduan pemasangan dari nol -- itu ada di [README.md](README.md).

Hasil audit database `vania-odoo` (Odoo 19) vs `spec.py` ditemukan beberapa
kelas kesalahan. Yang **menyebabkan langsung** error *"Population Changed -- No
target yet for ..."* saat menekan **Calculate** hanya Bagian A. Sisanya
menyebabkan data basi, fitur tidak jalan, atau risiko timeout.

> Urutan pengerjaan yang disarankan: **A -> B -> C -> D -> E -> F -> G -> H -> I**.

---

## Konteks: kenapa sampai error?

`sa_engine_calculate.py` punya guard (baris 401) yang menolak Calculate kalau
ada branch target dengan `x_needs_recascade = True`:

```
These teams changed since their targets were cascaded:
- Jan 2026 B2C Jakarta: No target yet for: Rizki Nugraha
...
Calculating now would pay against a team that no longer exists.
Re-run the target cascade first.
```

Masalahnya: `x_recascade_reason` & `x_needs_recascade` di DB di-set **Stored**,
padahal speknya **Not stored**. Field computed yang Stored hanya dihitung ulang
kalau salah satu **Depends** berubah. Depends-nya:

```
x_recascade_reason : x_state, x_period_id, x_branch_id, x_business_type
x_needs_recascade  : x_recascade_reason
```

**Tidak ada** yang menyentuh `x_incentive_target`. Jadi ketika target dibuat
oleh cascade, flag tidak pernah dihitung ulang -> tetap `True` -> Calculate
diblokir. Ini **false alarm yang beku**, bukan data yang salah.

---

## Cara mengerjakan

Sebagian besar lewat **Settings -> Technical -> Fields** (aktifkan Developer
Mode dulu: Settings -> Activate the developer mode). Buka field berdasarkan
**Model** + **Field Name**, ubah, lalu **Save**.

Setelah tiap perubahan besar, **Reload halaman** (Ctrl/Cmd+Shift+R).

Legenda prioritas:
- 🔴 WAJIB -- tanpa ini Calculate tetap gagal
- 🟠 PENTING -- data basi / risiko timeout
- 🟡 FITUR -- fitur tampilan tidak lengkap
- 🟢 RAPI -- validasi & kenyamanan

---

# 🔴 A. WAJIB -- penyebab error Calculate

Hilangkan centang **Stored** pada dua field ini (biarkan Compute & Depends
seperti sekarang):

| Model | Field Name | Label | Sekarang | Harusnya |
|---|---|---|---|---|
| `x_incentive_branch_target` | `x_recascade_reason` | Re-cascade Reason | Stored ✓ | **Not stored** |
| `x_incentive_branch_target` | `x_needs_recascade` | Population Changed | Stored ✓ | **Not stored** |

Langkah:
1. Settings -> Technical -> Fields.
2. Cari `x_recascade_reason`, Model `x_incentive_branch_target`.
3. Buka -> hilangkan centang **Stored** -> Save.
4. Ulangi untuk `x_needs_recascade`.

**Cek hasil:** buka Branch Target `Jan 2026 B2C Jakarta`. Banner kuning
"Population changed..." harus **hilang**. Lalu coba **Calculate**.

- [ ] `x_recascade_reason` -> Not stored
- [ ] `x_needs_recascade` -> Not stored

> Kalau setelah ini muncul pesan *"No target yet for ..."* dengan **nama lain**
> (bukan Rizki), berarti ada orang yang memang belum punya target -- jalankan
> **Cascade Branch Target -> Preview -> Apply** dulu, baru Calculate.

---

# 🟠 B. Unstore -- data basi & risiko timeout

Field-field ini di DB Stored, padahal spek Not stored. Hilangkan centang
**Stored** satu per satu:

| # | Model | Field Name | Label | Alasan |
|---|---|---|---|---|
| B1 | `x_incentive_branch_target` | `x_payout_total` | Branch Payout | Stored hanya depends `x_period_id,x_branch_id,x_business_type` -- **tidak** ikut berubah saat payout berubah, jadi kolom Payout cabang basi. |
| B2 | `x_incentive_period` | `x_total_target` | Total Target | Spek Not stored. |
| B3 | `x_incentive_period` | `x_total_payout` | Total Payout | Spek Not stored. |
| B4 | `x_incentive_refund` | `x_base_amount` | Invoice Line Amount | Spek Not stored. |
| B5 | `x_incentive_refund` | `x_refundable_amount` | Refundable | Spek Not stored. |
| B6 | `account.move.line` | `x_incentive_eligible` | Incentive Eligible | **Paling penting**: README aturan 8 melarang simpan compute di tabel besar (di sini 123.382 baris) karena bisa timeout. |

- [ ] B1 `x_incentive_branch_target.x_payout_total`
- [ ] B2 `x_incentive_period.x_total_target`
- [ ] B3 `x_incentive_period.x_total_payout`
- [ ] B4 `x_incentive_refund.x_base_amount`
- [ ] B5 `x_incentive_refund.x_refundable_amount`
- [ ] B6 `account.move.line.x_incentive_eligible`

---

# 🟡 C. Field yang HILANG -- perlu dibuat

Buat lewat Settings -> Technical -> Fields -> New (atau Studio). Kolom
"Compute" diisi dari file di folder `compute/`.

> **Penting:** buat field Compute dari atas ke bawah, dan pastikan model
> induknya sudah ada lebih dulu. Field Compute hanya menghitung data baru --
> data lama dihitung saat diakses (Not stored) atau saat dependennya berubah.

| # | Model | Field Name | Label | Type | Detail |
|---|---|---|---|---|---|
| C1 | `x_incentive_payout` | `x_user_id` | User | Many2one | Model `res.users`; Related `x_employee_id.user_id`; **Stored**; On Delete Set Null |
| C2 | `x_incentive_branch` | `x_employee_count` | Employee Count | Integer | Compute `compute/c_branch_employee_count.py`; Depends `x_employee_ids`; Not stored |
| C3 | `x_incentive_branch` | `x_effective_fte_b2b` | FTE B2B | Float | Compute `compute/c_branch_effective_fte_b2b.py`; Depends `x_employee_ids.x_incentive_business_type,x_employee_ids.x_incentive_designation_id`; Not stored |
| C4 | `x_incentive_branch` | `x_effective_fte_b2c` | FTE B2C | Float | Compute `compute/c_branch_effective_fte_b2c.py`; Depends sama seperti C3; Not stored |
| C5 | `x_incentive_branch` | `x_effective_fte` | Effective FTE | Float | Compute `compute/c_branch_effective_fte.py`; Depends sama seperti C3; Not stored |
| C6 | `x_incentive_target` | `x_movement_ids` | Movements | One2many | Model `x_incentive_target_movement`; Relation Field `x_target_id` |
| C7 | `x_incentive_transaction` | `x_display_ref` | Display Ref | Char | Compute `compute/c_transaction_display_ref.py`; Depends `x_move_id.name,x_pos_order_id.pos_reference,x_product_id.name`; Not stored |
| C8 | `x_incentive_refund` | `x_move_line_id` | Invoice Line | Many2one | Model `account.move.line`; Related `x_transaction_id.x_move_line_id` |

- [ ] C1 `x_incentive_payout.x_user_id`
- [ ] C2 `x_incentive_branch.x_employee_count`
- [ ] C3 `x_incentive_branch.x_effective_fte_b2b`
- [ ] C4 `x_incentive_branch.x_effective_fte_b2c`
- [ ] C5 `x_incentive_branch.x_effective_fte`
- [ ] C6 `x_incentive_target.x_movement_ids`
- [ ] C7 `x_incentive_transaction.x_display_ref`
- [ ] C8 `x_incentive_refund.x_move_line_id`

> Catatan: `hr.employee.x_is_global_branch_member` dan
> `pos.order.x_incentive_transaction_ids` **sudah ada** -- tidak perlu dibuat.

---

# 🟡 D. `x_name` belum Compute -- nama kosong

Tiga model ini `x_name`-nya adalah Char biasa (bukan computed), sehingga nama
record kosong (terlihat di list Targets). Pasang Compute:

| # | Model | Field Name | Compute | Depends | Stored |
|---|---|---|---|---|---|
| D1 | `x_incentive_branch_target` | `x_name` | `compute/c_branch_target_name.py` | `x_branch_id.x_name,x_business_type,x_period_id.x_name` | ✓ |
| D2 | `x_incentive_target` | `x_name` | `compute/c_target_name.py` | `x_employee_id.name,x_target_type,x_period_id.x_name` | ✓ |
| D3 | `x_incentive_cascade` | `x_name` | `compute/c_cascade_name.py` | `x_period_id.x_name,x_business_type` | ✓ |

Setelah dipasang, buka field `x_name` masing-masing (Settings -> Technical ->
Fields) lalu isi tab **Advanced Properties -> Compute** + **Dependencies**, dan
centang **Stored**.

- [ ] D1 `x_incentive_branch_target.x_name`
- [ ] D2 `x_incentive_target.x_name`
- [ ] D3 `x_incentive_cascade.x_name`

---

# 🟡 E. Related yang hilang

| # | Model | Field Name | Label | Set Related |
|---|---|---|---|---|
| E1 | `x_incentive_payout` | `x_company_id` | Company | `x_period_id.x_company_id` (Stored) |

Ini menentukan `x_currency_id` (`x_company_id.currency_id`) dan perilaku
multi-company pada payout.

- [ ] E1 `x_incentive_payout.x_company_id`

---

# 🟢 F. Required yang hilang

Centang **Required**:

| # | Model | Field Name | Label |
|---|---|---|---|
| F1 | `x_incentive_branch` | `x_code` | Code |
| F2 | `x_incentive_branch_target` | `x_business_type` | Business Type |
| F3 | `x_incentive_branch_target` | `x_amount` | Branch Net Sales Target |
| F4 | `x_incentive_target_movement` | `x_amount` | Amount |
| F5 | `x_incentive_transaction` | `x_source_period_id` | Source Period |
| F6 | `x_incentive_refund_policy` | `x_name` | Name |

- [ ] F1..F6

---

# 🟢 G. Readonly salah

| # | Model | Field Name | Sekarang | Harusnya |
|---|---|---|---|---|
| G1 | `x_incentive_branch_target` | `x_carry_forward_amount` | editable | **Readonly** |
| G2 | `x_incentive_target` | `x_shortfall_amount` | editable | **Readonly** |
| G3 | `x_incentive_target` | `x_carry_forward_amount` | editable | **Readonly** |
| G4 | `x_incentive_payout` | `x_name` | editable | **Readonly** |
| G5 | `hr.employee` | `x_branch_incentive_eligible` | Readonly | **Readonly OFF** (editable) |
| G6 | `hr.employee` | `x_individual_incentive_eligible` | Readonly | **Readonly OFF** (editable) |

G5/G6 adalah computed+stored tapi sengaja dibuat bisa di-override manual,
karena itu Readonly-nya harus dimatikan.

- [ ] G1..G6

---

# 🔵 H. Setting Model -- Mail Thread & Order

## H1. Chatter (Has Mail Thread / Has Mail Activity)
Settings -> Technical -> Database Structure -> **Models**: buka model, centang
sesuai tabel. Sekali dicentang tidak bisa dimatikan lagi.

| Model | Has Mail Thread | Has Mail Activity |
|---|---|---|
| `x_incentive_period` | ✓ | ✓ |
| `x_incentive_payout` | ✓ | |
| `x_incentive_target` | ✓ | |
| `x_incentive_target_movement` | ✓ | |

## H2. Default Order
Masih perlu diisi di form Model (field **Order**) **setelah semua field model
itu ada**:

| Model | Order |
|---|---|
| `x_incentive_designation` | `x_sequence, id` |
| `x_incentive_branch` | `x_sequence, x_code` |
| `x_incentive_rule` | `x_date_from desc` |
| `x_incentive_rule_tier` | `x_level` |
| `x_incentive_period` | `x_date_start desc` |
| `x_incentive_branch_target` | `x_period_id desc, x_branch_id, x_business_type` |
| `x_incentive_target` | `x_period_id desc, x_employee_id, x_target_type` |
| `x_incentive_target_movement` | `x_date_effective desc, id desc` |
| `x_incentive_transaction` | `x_source_period_id desc, x_employee_id, id` |
| `x_incentive_payout` | `x_period_id desc, x_employee_id` |
| `x_incentive_cascade` | `create_date desc` |
| `x_incentive_refund` | `create_date desc` |
| `x_incentive_refund_policy` | `x_sequence, id` |

- [ ] H1 Chatter 4 model
- [ ] H2 Order semua model

---

# 🔵 I. Default Value yang kurang

Saat ini hanya ada 2 default (`x_state='draft'` pada period & branch target).
Tambahkan lewat Settings -> Technical -> Actions -> **User-defined Defaults**
(field `json_value`), atau Studio (klik field -> Default value):

| Model | Field | Nilai |
|---|---|---|
| `x_incentive_designation` | `x_active` | `true` |
| `x_incentive_designation` | `x_branch_eligible` | `true` |
| `x_incentive_designation` | `x_individual_eligible` | `true` |
| `x_incentive_designation` | `x_fte_branch` | `1.0` |
| `x_incentive_designation` | `x_fte_individual` | `1.0` |
| `x_incentive_rule` | `x_active` | `true` |
| `x_incentive_rule` | `x_base_rate` | `0.0075` |
| `x_incentive_rule` | `x_bonus_rate` | `0.01` |
| `x_incentive_rule` | `x_max_discount` | `35.0` |
| `x_incentive_rule` | `x_cap_tier_in_mixed` | `true` |
| `x_incentive_rule` | `x_mixed_cap_tier_level` | `4` |
| `x_incentive_branch_target` | `x_business_type` | `"b2b"` |
| `x_incentive_target` | `x_target_type` | `"incentive"` |
| `x_incentive_target` | `x_source` | `"manual"` |
| `x_incentive_target` | `x_proration_ratio` | `1.0` |
| `x_incentive_target_movement` | `x_reason` | `"manual"` |
| `x_incentive_target_movement` | `x_target_type` | `"bonus"` |
| `x_incentive_cascade` | `x_business_type` | `"b2b"` |
| `x_incentive_cascade` | `x_scope` | `"individual"` |
| `x_incentive_cascade` | `x_redistribute_vacant` | `true` |
| `x_incentive_cascade` | `x_overwrite_existing` | `true` |
| `x_incentive_refund_policy` | `x_active` | `true` |

- [ ] I semua default di atas

---

# ✅ Verifikasi setelah perbaikan

## 1. Verifikasi lewat UI
1. Buka **Sales Incentive -> Operations -> Branch Targets**, filter Jan 2026.
   - Kolom *Re-cascade* harus kosong, tidak ada baris kuning.
2. Buka `Jan 2026 B2C Jakarta` -> tidak ada banner "Population changed".
3. Buka **Incentive Periods -> Jan 2026** -> **Calculate** berjalan tanpa error
   *Population Changed*.
4. Buka salah satu Payout -> tab **Calculation Log** harus berisi `[1]` s/d
   `[8]`, dan `x_total_payout` terisi.

## 2. Verifikasi lewat SQL (khusus salinan database, mis. `vania-odoo`)
Jalankan:

```sql
-- A: flag harus false
SELECT id, x_name, x_needs_recascade, x_recascade_reason
FROM x_incentive_branch_target WHERE x_period_id = 2
ORDER BY x_business_type, x_branch_id;

-- B: field-field ini harus store = false
SELECT m.model, f.name, f.store
FROM ir_model_fields f JOIN ir_model m ON m.id = f.model_id
WHERE (m.model, f.name) IN (
  ('x_incentive_branch_target','x_recascade_reason'),
  ('x_incentive_branch_target','x_needs_recascade'),
  ('x_incentive_branch_target','x_payout_total'),
  ('x_incentive_period','x_total_target'),
  ('x_incentive_period','x_total_payout'),
  ('x_incentive_refund','x_base_amount'),
  ('x_incentive_refund','x_refundable_amount'),
  ('account.move.line','x_incentive_eligible'))
ORDER BY m.model, f.name;
```

Semua baris di query B harus `store = f`.

## 3. Setelah target tim berubah di kemudian hari
Jalankan **Cascade Branch Target** lagi (Preview -> Apply) lalu **Calculate**.
Flag sekarang akan selalu segar karena sudah Not stored.

---

# ⚪ Yang sudah BENAR (jangan diubah)
- 21 Server Action `VIF: ...` lengkap, model tepat, state `code`.
- 8 Automation Rule `VIF: ...` lengkap & aktif.
- Kode **VIF: Engine Calculate** di DB identik dengan `actions/sa_engine_calculate.py`.
- Access Rights: Administrator full CRUD, Manager/Salesperson read.
- 9 Record Rule payout/target/transaction.

---

# Catatan & peringatan
1. **Ubah `Stored` pada field yang sudah punya data** akan menjatuhkan kolom di
   DB saat Save; field akan dihitung ulang saat diakses. Ini normal.
2. **Developer Mode** wajib aktif untuk melihat menu Technical.
3. Untuk **Odoo Online produksi**, kerjakan dulu di **database duplikat**
   (odoo.com/my/databases -> Duplicate), uji, baru ulangi di produksi.
4. Group di DB ini bernama `Salesperson` / `Manager` / `Administrator` (bukan
   `VIF Incentive / ...`). Access-nya sudah benar, tapi pastikan warisan group
   berurutan (Salesperson -> Manager -> Administrator) supaya record rule
   bekerja sesuai desain. Ini **opsional**.
5. Setelah semua beres, bandingkan angka hasil Calculate dengan perhitungan
   manual / modul Python untuk memastikan tidak ada selisih.

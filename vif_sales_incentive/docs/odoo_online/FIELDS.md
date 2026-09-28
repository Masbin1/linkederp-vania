# Daftar Field -- VIF Sales Incentive di Odoo Online

> File ini DIGENERATE dari `spec.py` (`python3 render_fields_md.py`). Jangan edit manual -- ubah `spec.py` lalu generate ulang.

Urutan di bawah = urutan pembuatan. Many2one hanya bisa menunjuk model yang sudah ada, jadi ikuti urutannya.

**`x_name` dibuat otomatis oleh Odoo** di setiap model baru. Jangan buat lagi. Jika tabel meminta `x_name` dengan Compute, EDIT field `x_name` yang sudah ada.

**Field Monetary** butuh `x_currency_id` sudah ada lebih dulu di model yang sama.

## 1. `x_incentive_designation` -- Incentive FTE Designation (model baru)

| # | Field Name | Label | Type | Detail |
|---|---|---|---|---|
| 1 | `x_name` | Name | Char (Text) | Required |
| 2 | `x_code` | Code | Char (Text) | Required |
| 3 | `x_sequence` | Sequence | Integer |  |
| 4 | `x_fte_branch` | Branch FTE | Float (Decimal) |  |
| 5 | `x_fte_individual` | Individual FTE | Float (Decimal) |  |
| 6 | `x_branch_eligible` | Branch Incentive Eligible | Boolean (Checkbox) |  |
| 7 | `x_individual_eligible` | Individual Incentive Eligible | Boolean (Checkbox) |  |
| 8 | `x_active` | Active | Boolean (Checkbox) |  |

## 2. `x_incentive_branch` -- Incentive Sales Branch (model baru)

| # | Field Name | Label | Type | Detail |
|---|---|---|---|---|
| 1 | `x_name` | Name | Char (Text) | Required |
| 2 | `x_code` | Code | Char (Text) | Required |
| 3 | `x_sequence` | Sequence | Integer |  |
| 4 | `x_company_id` | Company | Many2one | Model: `res.company`; On Delete: Set Null |
| 5 | `x_manager_id` | Branch Manager | Many2one | Model: `hr.employee`; On Delete: Set Null |
| 6 | `x_active` | Active | Boolean (Checkbox) |  |
| 7 | `x_ideal_team_size_b2b` | Ideal B2B Size | Integer |  |
| 8 | `x_ideal_team_size_b2c` | Ideal B2C Size | Integer |  |

## 3. `hr.employee` (model standar -- tambah field)

| # | Field Name | Label | Type | Detail |
|---|---|---|---|---|
| 1 | `x_incentive_branch_id` | Sales Branch | Many2one | Model: `x_incentive_branch`; On Delete: Set Null |
| 2 | `x_incentive_business_type` | Business Type | Selection | Nilai: `b2b`=B2B, `b2c`=B2C |
| 3 | `x_incentive_designation_id` | FTE Designation | Many2one | Model: `x_incentive_designation`; On Delete: Set Null |
| 4 | `x_incentive_date_start` | Effective Target Start | Date |  |
| 5 | `x_incentive_date_end` | Resignation Date | Date |  |
| 6 | `x_is_vacant_slot` | Vacant Position | Boolean (Checkbox) |  |
| 7 | `x_is_global_branch_member` | Global Branch Member | Boolean (Checkbox) |  |
| 8 | `x_branch_incentive_eligible` | Branch Incentive Eligible | Boolean (Checkbox) | **Compute** `compute/c_employee_branch_eligible.py`, Depends `x_incentive_designation_id`, Stored, editable (Readonly OFF) |
| 9 | `x_individual_incentive_eligible` | Individual Incentive Eligible | Boolean (Checkbox) | **Compute** `compute/c_employee_individual_eligible.py`, Depends `x_incentive_designation_id`, Stored, editable (Readonly OFF) |

## 4. `account.move` (model standar -- tambah field)

| # | Field Name | Label | Type | Detail |
|---|---|---|---|---|
| 1 | `x_incentive_employee_id` | Incentive Salesperson | Many2one | Model: `hr.employee`; On Delete: Set Null; Help: Filled by automation "VIF: Invoice Incentive Salesperson". Only used for invoices without a project. |

## 5. `x_incentive_rule` -- Incentive Rule Version (model baru)

| # | Field Name | Label | Type | Detail |
|---|---|---|---|---|
| 1 | `x_name` | Name | Char (Text) | Required |
| 2 | `x_date_from` | Valid From | Date | Required |
| 3 | `x_date_to` | Valid To | Date |  |
| 4 | `x_active` | Active | Boolean (Checkbox) |  |
| 5 | `x_company_id` | Company | Many2one | Model: `res.company`; On Delete: Set Null |
| 6 | `x_base_rate` | Base Rate | Float (Decimal) | Help: 0.0075 = 0.75% |
| 7 | `x_bonus_rate` | Bonus Rate | Float (Decimal) | Help: 0.01 = 1% |
| 8 | `x_max_discount` | Max Eligible Discount (%) | Float (Decimal) |  |
| 9 | `x_cap_tier_in_mixed` | Cap Tier in Mixed Scenario | Boolean (Checkbox) |  |
| 10 | `x_mixed_cap_tier_level` | Mixed Scenario Cap Level | Integer |  |

## 6. `x_incentive_rule_tier` -- Incentive Tier (model baru)

| # | Field Name | Label | Type | Detail |
|---|---|---|---|---|
| 1 | `x_rule_id` | Rule | Many2one | Model: `x_incentive_rule`; On Delete: Cascade; Required |
| 2 | `x_name` | Name | Char (Text) | Required |
| 3 | `x_level` | Level | Integer |  |
| 4 | `x_achievement_min` | Achievement From | Float (Decimal) | Help: 0.75 = 75% |
| 5 | `x_achievement_max` | Achievement To | Float (Decimal) |  |
| 6 | `x_is_top_tier` | Open-ended (Top Tier) | Boolean (Checkbox) |  |
| 7 | `x_allocation` | Allocation | Float (Decimal) | Help: 0.4 = 40% of base rate |
| 8 | `x_payout_rate` | Payout Rate | Float (Decimal) | **Compute** `compute/c_tier_payout_rate.py`, Depends `x_allocation,x_rule_id.x_base_rate`, Stored |

## 7. `x_incentive_period` -- Incentive Period (model baru)

| # | Field Name | Label | Type | Detail |
|---|---|---|---|---|
| 1 | `x_name` | Name | Char (Text) | Required |
| 2 | `x_date_start` | Start Date | Date | Required |
| 3 | `x_date_end` | End Date | Date | Required |
| 4 | `x_company_id` | Company | Many2one | Model: `res.company`; On Delete: Set Null |
| 5 | `x_rule_id` | Rule Version | Many2one | Model: `x_incentive_rule`; On Delete: Set Null |
| 6 | `x_state` | Status | Selection | Nilai: `draft`=Draft, `open`=Open, `calculated`=Calculated, `approved`=Approved, `locked`=Locked |

## 8. `x_incentive_branch_target` -- Incentive Branch Target (model baru)

| # | Field Name | Label | Type | Detail |
|---|---|---|---|---|
| 1 | `x_name` | Name | Char (Text) | **Compute** `compute/c_branch_target_name.py`, Depends `x_branch_id.x_name,x_business_type,x_period_id.x_name`, Stored |
| 2 | `x_period_id` | Period | Many2one | Model: `x_incentive_period`; On Delete: Restrict; Required |
| 3 | `x_branch_id` | Branch | Many2one | Model: `x_incentive_branch`; On Delete: Restrict; Required |
| 4 | `x_business_type` | Business Type | Selection | Nilai: `b2b`=B2B, `b2c`=B2C; Required |
| 5 | `x_company_id` | Company | Many2one | Model: `res.company`; On Delete: Set Null; Related: `x_period_id.x_company_id` (Stored) |
| 6 | `x_currency_id` | Currency | Many2one | Model: `res.currency`; On Delete: Set Null; Related: `x_company_id.currency_id` |
| 7 | `x_amount` | Branch Net Sales Target | Monetary | Required; Currency field: `x_currency_id` |
| 8 | `x_carry_forward_amount` | Carry-Forward | Monetary | Readonly; Currency field: `x_currency_id` |
| 9 | `x_amount_total` | Total Target | Monetary | **Compute** `compute/c_branch_target_amount_total.py`, Depends `x_amount,x_carry_forward_amount`, Stored; Currency field: `x_currency_id` |
| 10 | `x_state` | Status | Selection | Nilai: `draft`=Draft, `calculated`=Calculated, `approved`=Approved, `locked`=Locked |
| 11 | `x_recascade_reason` | Re-cascade Reason | Char (Text) | **Compute** `compute/c_branch_target_recascade.py`, Depends `x_state,x_period_id,x_branch_id,x_business_type`, Not stored |
| 12 | `x_needs_recascade` | Population Changed | Boolean (Checkbox) | **Compute** `compute/c_branch_target_needs_recascade.py`, Depends `x_recascade_reason`, Not stored |
| 13 | `x_payout_total` | Branch Payout | Monetary | **Compute** `compute/c_branch_target_payout_total.py`, Depends `x_period_id,x_branch_id,x_business_type`, Not stored; Currency field: `x_currency_id` |

## 9. `x_incentive_target` -- Incentive Target (model baru)

| # | Field Name | Label | Type | Detail |
|---|---|---|---|---|
| 1 | `x_name` | Name | Char (Text) | **Compute** `compute/c_target_name.py`, Depends `x_employee_id.name,x_target_type,x_period_id.x_name`, Stored |
| 2 | `x_period_id` | Period | Many2one | Model: `x_incentive_period`; On Delete: Restrict; Required |
| 3 | `x_employee_id` | Employee | Many2one | Model: `hr.employee`; On Delete: Restrict; Required |
| 4 | `x_branch_id` | Branch | Many2one | Model: `x_incentive_branch`; On Delete: Set Null; Related: `x_employee_id.x_incentive_branch_id` (Stored) |
| 5 | `x_business_type` | Business Type | Selection | Related: `x_employee_id.x_incentive_business_type` (Stored) |
| 6 | `x_designation_id` | Designation | Many2one | Model: `x_incentive_designation`; On Delete: Set Null; Related: `x_employee_id.x_incentive_designation_id` (Stored) |
| 7 | `x_company_id` | Company | Many2one | Model: `res.company`; On Delete: Set Null; Related: `x_period_id.x_company_id` (Stored) |
| 8 | `x_currency_id` | Currency | Many2one | Model: `res.currency`; On Delete: Set Null; Related: `x_company_id.currency_id` |
| 9 | `x_target_type` | Bucket | Selection | Nilai: `incentive`=Incentive-Based, `bonus`=Bonus-Based; Required |
| 10 | `x_amount` | Amount | Monetary | Required; Currency field: `x_currency_id` |
| 11 | `x_source` | Source | Selection | Nilai: `manual`=Manual Input, `rf_cascade`=Rolling Forecast Cascade, `redistribution`=Vacancy Redistribution, `proration`=New Hire Proration |
| 12 | `x_fte_used` | FTE Used | Float (Decimal) | Readonly |
| 13 | `x_date_effective_start` | Effective Start | Date |  |
| 14 | `x_date_effective_end` | Effective End | Date |  |
| 15 | `x_proration_ratio` | Proration | Float (Decimal) |  |
| 16 | `x_shortfall_amount` | Shortfall | Monetary | Readonly; Currency field: `x_currency_id` |
| 17 | `x_carry_forward_amount` | Carry-Forward / Month | Monetary | Readonly; Currency field: `x_currency_id` |
| 18 | `x_months_remaining` | Months Remaining | Integer | Readonly |
| 19 | `x_note` | Note | Char (Text) |  |

## 10. `x_incentive_target_movement` -- Incentive Target Movement (model baru)

| # | Field Name | Label | Type | Detail |
|---|---|---|---|---|
| 1 | `x_name` | Reference | Char (Text) |  |
| 2 | `x_period_id` | Period | Many2one | Model: `x_incentive_period`; On Delete: Restrict; Required |
| 3 | `x_target_id` | Resulting Target | Many2one | Model: `x_incentive_target`; On Delete: Set Null |
| 4 | `x_reason` | Reason | Selection | Nilai: `resignation`=Resignation / Vacant, `new_hire`=New Hire Proration, `rf_revision`=Rolling Forecast Revision, `replacement`=Replacement Joined, `manual`=Manual Adjustment; Required |
| 5 | `x_from_employee_id` | From | Many2one | Model: `hr.employee`; On Delete: Set Null |
| 6 | `x_to_employee_id` | To | Many2one | Model: `hr.employee`; On Delete: Set Null |
| 7 | `x_currency_id` | Currency | Many2one | Model: `res.currency`; On Delete: Set Null; Related: `x_period_id.x_company_id.currency_id` |
| 8 | `x_amount` | Amount | Monetary | Required; Currency field: `x_currency_id` |
| 9 | `x_target_type` | Bucket | Selection | Nilai: `incentive`=Incentive-Based, `bonus`=Bonus-Based; Required |
| 10 | `x_fte_share` | FTE Share | Float (Decimal) |  |
| 11 | `x_date_effective` | Effective Date | Date |  |
| 12 | `x_note` | Note | Char (Text) |  |

## 11. `x_incentive_transaction` -- Incentive Transaction (model baru)

| # | Field Name | Label | Type | Detail |
|---|---|---|---|---|
| 1 | `x_name` | Reference | Char (Text) | Readonly |
| 2 | `x_source_type` | Source | Selection | Nilai: `invoice`=Invoice, `pos`=POS Order; Indexed |
| 3 | `x_move_line_id` | Invoice Line | Many2one | Model: `account.move.line`; On Delete: Cascade; Indexed |
| 4 | `x_move_id` | Invoice | Many2one | Model: `account.move`; On Delete: Cascade; Indexed |
| 5 | `x_pos_order_line_id` | POS Order Line | Many2one | Model: `pos.order.line`; On Delete: Cascade; Indexed |
| 6 | `x_pos_order_id` | POS Order | Many2one | Model: `pos.order`; On Delete: Cascade; Indexed |
| 7 | `x_employee_id` | Employee | Many2one | Model: `hr.employee`; On Delete: Restrict; Required; Indexed |
| 8 | `x_project_id` | Project | Many2one | Model: `project.project`; On Delete: Set Null; Indexed |
| 9 | `x_split_role` | Credit Role | Selection | Nilai: `pm`=Project Manager, `sp2`=Salesperson 2, `sp3`=Salesperson 3, `salesperson`=Salesperson / Cashier |
| 10 | `x_split_share` | Share | Float (Decimal) |  |
| 11 | `x_branch_id` | Branch | Many2one | Model: `x_incentive_branch`; On Delete: Set Null; Related: `x_employee_id.x_incentive_branch_id` (Stored) |
| 12 | `x_business_type` | Business Type | Selection | Related: `x_employee_id.x_incentive_business_type` (Stored) |
| 13 | `x_partner_id` | Customer | Many2one | Model: `res.partner`; On Delete: Set Null |
| 14 | `x_product_id` | Product | Many2one | Model: `product.product`; On Delete: Set Null |
| 15 | `x_company_id` | Company | Many2one | Model: `res.company`; On Delete: Set Null |
| 16 | `x_currency_id` | Currency | Many2one | Model: `res.currency`; On Delete: Set Null; Related: `x_company_id.currency_id` |
| 17 | `x_source_period_id` | Source Period | Many2one | Model: `x_incentive_period`; On Delete: Restrict; Required; Indexed |
| 18 | `x_payment_period_id` | Payment Period | Many2one | Model: `x_incentive_period`; On Delete: Set Null; Indexed |
| 19 | `x_payout_period_id` | Payout Period | Many2one | Model: `x_incentive_period`; On Delete: Set Null |
| 20 | `x_invoice_date` | Invoice Date | Date |  |
| 21 | `x_payment_date` | Fully Paid On | Date |  |
| 22 | `x_is_prior_period` | Prior-Period Invoice | Boolean (Checkbox) |  |
| 23 | `x_transaction_type` | Type | Selection | Nilai: `invoice`=Invoice, `refund`=Credit Note / Refund |
| 24 | `x_base_amount` | Line Amount | Monetary | Currency field: `x_currency_id` |
| 25 | `x_discount` | Discount (%) | Float (Decimal) |  |
| 26 | `x_is_downpayment` | Down Payment Line | Boolean (Checkbox) |  |
| 27 | `x_is_discount_eligible` | Discount Eligible | Boolean (Checkbox) |  |
| 28 | `x_is_payment_eligible` | Fully Paid | Boolean (Checkbox) |  |
| 29 | `x_eligibility_note` | Eligibility Note | Char (Text) |  |
| 30 | `x_bucket` | Bucket | Selection | Nilai: `incentive`=Incentive-Based, `bonus`=Bonus-Based, `excluded`=Excluded |
| 31 | `x_incentive_alloc` | Incentive Allocation | Monetary | Currency field: `x_currency_id` |
| 32 | `x_bonus_alloc` | Bonus Allocation | Monetary | Currency field: `x_currency_id` |
| 33 | `x_tier_id` | Tier (snapshot) | Many2one | Model: `x_incentive_rule_tier`; On Delete: Set Null |
| 34 | `x_tier_payout_rate` | Payout Rate (snapshot) | Float (Decimal) |  |
| 35 | `x_payout_amount` | Payout Amount | Monetary | Currency field: `x_currency_id` |
| 36 | `x_reversal_of_id` | Reversal Of | Many2one | Model: `x_incentive_transaction`; On Delete: Set Null |
| 37 | `x_state` | Status | Selection | Nilai: `draft`=Draft, `confirmed`=Confirmed, `paid_out`=Paid Out, `reversed`=Reversed |

## 12. `x_incentive_payout` -- Incentive Payout (model baru)

| # | Field Name | Label | Type | Detail |
|---|---|---|---|---|
| 1 | `x_name` | Name | Char (Text) | Readonly |
| 2 | `x_period_id` | Period | Many2one | Model: `x_incentive_period`; On Delete: Cascade; Required |
| 3 | `x_employee_id` | Employee | Many2one | Model: `hr.employee`; On Delete: Restrict; Required |
| 4 | `x_user_id` | User | Many2one | Model: `res.users`; On Delete: Set Null; Related: `x_employee_id.user_id` (Stored) |
| 5 | `x_manager_id` | Manager | Many2one | Model: `hr.employee`; On Delete: Set Null; Related: `x_employee_id.parent_id` (Stored) |
| 6 | `x_branch_id` | Branch | Many2one | Model: `x_incentive_branch`; On Delete: Set Null; Related: `x_employee_id.x_incentive_branch_id` (Stored) |
| 7 | `x_business_type` | Business Type | Selection | Related: `x_employee_id.x_incentive_business_type` (Stored) |
| 8 | `x_company_id` | Company | Many2one | Model: `res.company`; On Delete: Set Null; Related: `x_period_id.x_company_id` (Stored) |
| 9 | `x_currency_id` | Currency | Many2one | Model: `res.currency`; On Delete: Set Null; Related: `x_company_id.currency_id` |
| 10 | `x_target_incentive` | Target Incentive | Monetary | Currency field: `x_currency_id` |
| 11 | `x_target_bonus` | Target Bonus | Monetary | Currency field: `x_currency_id` |
| 12 | `x_target_total` | Target Total | Monetary | Currency field: `x_currency_id` |
| 13 | `x_is_mixed` | Mixed Scenario | Boolean (Checkbox) |  |
| 14 | `x_gross_sales` | Gross Sales | Monetary | Currency field: `x_currency_id` |
| 15 | `x_sales_return` | Sales Return | Monetary | Currency field: `x_currency_id` |
| 16 | `x_net_sales` | Net Sales | Monetary | Currency field: `x_currency_id` |
| 17 | `x_achievement_pct` | Achievement | Float (Decimal) |  |
| 18 | `x_tier_id` | Tier | Many2one | Model: `x_incentive_rule_tier`; On Delete: Set Null |
| 19 | `x_tier_level` | Tier Level | Integer |  |
| 20 | `x_payout_rate` | Payout Rate | Float (Decimal) |  |
| 21 | `x_eligible_incentive` | Eligible Achievement Incentive | Monetary | Currency field: `x_currency_id` |
| 22 | `x_eligible_bonus` | Eligible Achievement Bonus | Monetary | Currency field: `x_currency_id` |
| 23 | `x_excluded_discount` | Excluded (Discount > cap) | Monetary | Currency field: `x_currency_id` |
| 24 | `x_paid_current_month` | Paid Current Month | Monetary | Currency field: `x_currency_id` |
| 25 | `x_paid_prior_month` | Paid Prior Month | Monetary | Currency field: `x_currency_id` |
| 26 | `x_paid_bonus` | Paid Bonus | Monetary | Currency field: `x_currency_id` |
| 27 | `x_payout_current` | Incentive Payout Current Month | Monetary | Currency field: `x_currency_id` |
| 28 | `x_payout_prior` | Incentive Payout Previous Month | Monetary | Currency field: `x_currency_id` |
| 29 | `x_incentive_payout` | Incentive Payout | Monetary | Currency field: `x_currency_id` |
| 30 | `x_payout_bonus` | Bonus Payout | Monetary | Currency field: `x_currency_id` |
| 31 | `x_branch_target` | Branch Target | Monetary | Currency field: `x_currency_id` |
| 32 | `x_branch_net_sales` | Branch Net Sales | Monetary | Currency field: `x_currency_id` |
| 33 | `x_branch_achievement_pct` | Branch Achievement | Float (Decimal) |  |
| 34 | `x_branch_tier_id` | Branch Tier | Many2one | Model: `x_incentive_rule_tier`; On Delete: Set Null |
| 35 | `x_branch_tier_level` | Branch Tier Level | Integer |  |
| 36 | `x_branch_payout_rate` | Branch Payout Rate | Float (Decimal) |  |
| 37 | `x_branch_eligible` | Branch Eligible Base | Monetary | Currency field: `x_currency_id` |
| 38 | `x_branch_paid` | Branch Paid Base | Monetary | Currency field: `x_currency_id` |
| 39 | `x_branch_pool` | Branch Pool | Monetary | Currency field: `x_currency_id` |
| 40 | `x_branch_fte` | Branch FTE Weight | Float (Decimal) |  |
| 41 | `x_branch_fte_share` | Branch FTE Share | Float (Decimal) |  |
| 42 | `x_branch_payout` | Branch Payout | Monetary | Currency field: `x_currency_id` |
| 43 | `x_total_payout` | Total Payout | Monetary | Currency field: `x_currency_id` |
| 44 | `x_is_eligible` | Eligible Month | Boolean (Checkbox) |  |
| 45 | `x_is_frozen` | Frozen | Boolean (Checkbox) | Readonly |
| 46 | `x_computation_log` | Computation Log | Text (Multiline) | Readonly |

## 13. `x_incentive_cascade` -- Cascade Branch Target (model baru)

| # | Field Name | Label | Type | Detail |
|---|---|---|---|---|
| 1 | `x_name` | Name | Char (Text) | **Compute** `compute/c_cascade_name.py`, Depends `x_period_id.x_name,x_business_type`, Stored |
| 2 | `x_period_id` | Period | Many2one | Model: `x_incentive_period`; On Delete: Cascade; Required |
| 3 | `x_branch_ids` | Branches | Many2many | Model: `x_incentive_branch` |
| 4 | `x_business_type` | Business Type | Selection | Nilai: `b2b`=B2B, `b2c`=B2C; Required |
| 5 | `x_scope` | Scope | Selection | Nilai: `individual`=Individual Target, `branch`=Branch Pool |
| 6 | `x_redistribute_vacant` | Redistribute Vacant Slots | Boolean (Checkbox) |  |
| 7 | `x_overwrite_existing` | Overwrite Existing Targets | Boolean (Checkbox) |  |
| 8 | `x_currency_id` | Currency | Many2one | Model: `res.currency`; On Delete: Set Null; Related: `x_period_id.x_company_id.currency_id` |
| 9 | `x_carry_forward_total` | Carry-Forward Total | Monetary | Readonly; Currency field: `x_currency_id` |

## 14. `x_incentive_cascade_line` -- Cascade Preview Line (model baru)

| # | Field Name | Label | Type | Detail |
|---|---|---|---|---|
| 1 | `x_cascade_id` | Cascade | Many2one | Model: `x_incentive_cascade`; On Delete: Cascade |
| 2 | `x_branch_target_id` | Branch Target | Many2one | Model: `x_incentive_branch_target`; On Delete: Cascade; Required |
| 3 | `x_branch_id` | Branch | Many2one | Model: `x_incentive_branch`; On Delete: Set Null; Related: `x_branch_target_id.x_branch_id` |
| 4 | `x_employee_id` | Employee | Many2one | Model: `hr.employee`; On Delete: Cascade; Required |
| 5 | `x_designation_id` | Designation | Many2one | Model: `x_incentive_designation`; On Delete: Set Null; Related: `x_employee_id.x_incentive_designation_id` |
| 6 | `x_currency_id` | Currency | Many2one | Model: `res.currency`; On Delete: Set Null; Related: `x_cascade_id.x_currency_id` |
| 7 | `x_fte` | FTE | Float (Decimal) |  |
| 8 | `x_proration` | Proration | Float (Decimal) |  |
| 9 | `x_base_amount` | Base Incentive | Monetary | Currency field: `x_currency_id` |
| 10 | `x_carry_forward_amount` | Carry-Forward | Monetary | Currency field: `x_currency_id` |
| 11 | `x_incentive_amount` | Total Incentive | Monetary | Currency field: `x_currency_id` |
| 12 | `x_bonus_amount` | Bonus | Monetary | Currency field: `x_currency_id` |

## 15. `x_incentive_refund` -- Refund Incentive Transaction (model baru)

| # | Field Name | Label | Type | Detail |
|---|---|---|---|---|
| 1 | `x_name` | Name | Char (Text) |  |
| 2 | `x_transaction_id` | Transaction | Many2one | Model: `x_incentive_transaction`; On Delete: Cascade; Required |
| 3 | `x_move_id` | Invoice | Many2one | Model: `account.move`; On Delete: Set Null; Related: `x_transaction_id.x_move_id` |
| 4 | `x_employee_id` | Employee | Many2one | Model: `hr.employee`; On Delete: Set Null; Related: `x_transaction_id.x_employee_id` |
| 5 | `x_currency_id` | Currency | Many2one | Model: `res.currency`; On Delete: Set Null; Related: `x_transaction_id.x_currency_id` |
| 6 | `x_base_amount` | Invoice Line Amount | Monetary | **Compute** `compute/c_refund_base_amount.py`, Depends `x_transaction_id`, Not stored; Currency field: `x_currency_id` |
| 7 | `x_refundable_amount` | Refundable | Monetary | **Compute** `compute/c_refund_refundable_amount.py`, Depends `x_transaction_id`, Not stored; Currency field: `x_currency_id` |
| 8 | `x_refund_amount` | Refund Amount | Monetary | Required; Currency field: `x_currency_id` |
| 9 | `x_refund_move_id` | Credit Note | Many2one | Model: `account.move`; On Delete: Set Null; Readonly |

## 16. `x_incentive_refund_policy` -- Incentive Refund Policy (model baru)

| # | Field Name | Label | Type | Detail |
|---|---|---|---|---|
| 1 | `x_name` | Name | Char (Text) | Required |
| 2 | `x_sequence` | Sequence | Integer |  |
| 3 | `x_stock_type` | Stock Type | Selection | Nilai: `available`=Available Stock, `indent`=Indent, `service`=Jasa / Service, `any`=All Types |
| 4 | `x_is_wip` | Work In Progress | Boolean (Checkbox) |  |
| 5 | `x_payment_status` | Payment Status | Selection | Nilai: `partial`=Partially Paid, `paid`=Fully Paid, `any`=Partial or Fully Paid |
| 6 | `x_initiator` | Initiator | Selection | Nilai: `customer`=Customer, `company`=Company (VIF) |
| 7 | `x_refund_pct` | Refund % | Float (Decimal) |  |
| 8 | `x_by_agreement` | By Agreement | Boolean (Checkbox) |  |
| 9 | `x_note` | Note | Char (Text) |  |
| 10 | `x_active` | Active | Boolean (Checkbox) |  |

## One2many (buat SETELAH semua model di atas ada)

| Model | Field Name | Label | Detail |
|---|---|---|---|
| `x_incentive_branch` | `x_employee_ids` | Sales Team | Model: `hr.employee`; Field relasi: `x_incentive_branch_id` |
| `x_incentive_rule` | `x_tier_ids` | Tiers | Model: `x_incentive_rule_tier`; Field relasi: `x_rule_id` |
| `x_incentive_period` | `x_branch_target_ids` | Branch Targets | Model: `x_incentive_branch_target`; Field relasi: `x_period_id` |
| `x_incentive_period` | `x_target_ids` | Targets | Model: `x_incentive_target`; Field relasi: `x_period_id` |
| `x_incentive_period` | `x_payout_ids` | Payouts | Model: `x_incentive_payout`; Field relasi: `x_period_id` |
| `x_incentive_period` | `x_transaction_ids` | Source Transactions | Model: `x_incentive_transaction`; Field relasi: `x_source_period_id` |
| `x_incentive_transaction` | `x_reversal_ids` | Reversals | Model: `x_incentive_transaction`; Field relasi: `x_reversal_of_id` |
| `x_incentive_cascade` | `x_line_ids` | Preview | Model: `x_incentive_cascade_line`; Field relasi: `x_cascade_id` |
| `account.move` | `x_incentive_transaction_ids` | Incentive Transactions | Model: `x_incentive_transaction`; Field relasi: `x_move_id` |
| `pos.order` | `x_incentive_transaction_ids` | Incentive Transactions | Model: `x_incentive_transaction`; Field relasi: `x_pos_order_id` |
| `hr.employee` | `x_incentive_payout_ids` | Incentive Payouts | Model: `x_incentive_payout`; Field relasi: `x_employee_id` |

## Default Value

Studio: klik field -> Properties -> Default Value. Atau Settings -> Technical -> User-defined Defaults.

| Model | Field | Default |
|---|---|---|
| `x_incentive_designation` | `x_active` | `True` |
| `x_incentive_designation` | `x_branch_eligible` | `True` |
| `x_incentive_designation` | `x_individual_eligible` | `True` |
| `x_incentive_designation` | `x_fte_branch` | `1.0` |
| `x_incentive_designation` | `x_fte_individual` | `1.0` |
| `x_incentive_branch` | `x_active` | `True` |
| `x_incentive_rule` | `x_active` | `True` |
| `x_incentive_rule` | `x_base_rate` | `0.0075` |
| `x_incentive_rule` | `x_bonus_rate` | `0.01` |
| `x_incentive_rule` | `x_max_discount` | `35.0` |
| `x_incentive_rule` | `x_cap_tier_in_mixed` | `True` |
| `x_incentive_rule` | `x_mixed_cap_tier_level` | `4` |
| `x_incentive_period` | `x_state` | `draft` |
| `x_incentive_branch_target` | `x_state` | `draft` |
| `x_incentive_branch_target` | `x_business_type` | `b2b` |
| `x_incentive_target` | `x_target_type` | `incentive` |
| `x_incentive_target` | `x_source` | `manual` |
| `x_incentive_target` | `x_proration_ratio` | `1.0` |
| `x_incentive_target_movement` | `x_reason` | `manual` |
| `x_incentive_target_movement` | `x_target_type` | `bonus` |
| `x_incentive_cascade` | `x_business_type` | `b2b` |
| `x_incentive_cascade` | `x_scope` | `individual` |
| `x_incentive_cascade` | `x_redistribute_vacant` | `True` |
| `x_incentive_cascade` | `x_overwrite_existing` | `True` |
| `x_incentive_refund_policy` | `x_active` | `True` |
| `x_incentive_branch`, `x_incentive_rule`, `x_incentive_period` | `x_company_id` | company Anda |

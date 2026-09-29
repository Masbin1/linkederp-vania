# -*- coding: utf-8 -*-
"""Model & field specification for running VIF Sales Incentive on Odoo Online
(Studio + server actions, no custom Python module).

This file is DATA, not an Odoo module file. It is the single source for:
  * the field tables in README.md (what to create in Studio / Technical), and
  * build_test_db.py, which creates exactly these models in a test database
    so the server-action code can be run before touching the client's Online.

Field tuple: (name, type, label, options)
  options keys: relation, relation_field, selection, required, related,
                store, readonly, compute (file under compute/), depends,
                ondelete, index, help, tracking (sequence; model must be
                in MAIL_MODELS)
"""

SEL_BTYPE = [('b2b', 'B2B'), ('b2c', 'B2C')]
SEL_TARGET_TYPE = [('incentive', 'Incentive-Based'), ('bonus', 'Bonus-Based')]

# Models are listed in creation order: a many2one can only point at a model
# that already exists, so masters come first. One2many fields that point at
# a later model are in EXTRA_FIELDS, created after every model exists.
MODELS = [
    ('x_incentive_designation', 'Incentive FTE Designation', [
        ('x_name', 'char', 'Name', {'required': True}),
        ('x_code', 'char', 'Code', {'required': True}),
        ('x_sequence', 'integer', 'Sequence', {}),
        ('x_fte_branch', 'float', 'Branch FTE', {}),
        ('x_fte_individual', 'float', 'Individual FTE', {}),
        ('x_branch_eligible', 'boolean', 'Branch Incentive Eligible', {}),
        ('x_individual_eligible', 'boolean', 'Individual Incentive Eligible', {}),
        ('x_active', 'boolean', 'Active', {}),
    ]),
    ('x_incentive_branch', 'Incentive Sales Branch', [
        ('x_name', 'char', 'Name', {'required': True}),
        ('x_code', 'char', 'Code', {'required': True}),
        ('x_sequence', 'integer', 'Sequence', {}),
        ('x_company_id', 'many2one', 'Company', {'relation': 'res.company'}),
        ('x_manager_id', 'many2one', 'Branch Manager', {'relation': 'hr.employee'}),
        ('x_active', 'boolean', 'Active', {}),
        ('x_ideal_team_size_b2b', 'integer', 'Ideal B2B Size', {}),
        ('x_ideal_team_size_b2c', 'integer', 'Ideal B2C Size', {}),
    ]),
    ('x_incentive_rule', 'Incentive Rule Version', [
        ('x_name', 'char', 'Name', {'required': True}),
        ('x_date_from', 'date', 'Valid From', {'required': True}),
        ('x_date_to', 'date', 'Valid To', {}),
        ('x_active', 'boolean', 'Active', {}),
        ('x_company_id', 'many2one', 'Company', {'relation': 'res.company'}),
        ('x_base_rate', 'float', 'Base Rate', {'help': '0.0075 = 0.75%'}),
        ('x_bonus_rate', 'float', 'Bonus Rate', {'help': '0.01 = 1%'}),
        ('x_max_discount', 'float', 'Max Eligible Discount (%)', {}),
        ('x_cap_tier_in_mixed', 'boolean', 'Cap Tier in Mixed Scenario', {}),
        ('x_mixed_cap_tier_level', 'integer', 'Mixed Scenario Cap Level', {}),
    ]),
    ('x_incentive_rule_tier', 'Incentive Tier', [
        ('x_rule_id', 'many2one', 'Rule', {'relation': 'x_incentive_rule',
                                           'required': True, 'ondelete': 'cascade'}),
        ('x_name', 'char', 'Name', {'required': True}),
        ('x_level', 'integer', 'Level', {}),
        ('x_achievement_min', 'float', 'Achievement From', {'help': '0.75 = 75%'}),
        ('x_achievement_max', 'float', 'Achievement To', {}),
        ('x_is_top_tier', 'boolean', 'Open-ended (Top Tier)', {}),
        ('x_allocation', 'float', 'Allocation', {'help': '0.4 = 40% of base rate'}),
        ('x_payout_rate', 'float', 'Payout Rate', {
            'compute': 'c_tier_payout_rate.py',
            'depends': 'x_allocation,x_rule_id.x_base_rate', 'store': True}),
    ]),
    ('x_incentive_period', 'Incentive Period', [
        ('x_name', 'char', 'Name', {'required': True, 'tracking': 10}),
        ('x_date_start', 'date', 'Start Date', {'required': True, 'tracking': 20}),
        ('x_date_end', 'date', 'End Date', {'required': True, 'tracking': 30}),
        ('x_company_id', 'many2one', 'Company', {'relation': 'res.company'}),
        ('x_currency_id', 'many2one', 'Currency', {
            'relation': 'res.currency', 'related': 'x_company_id.currency_id'}),
        ('x_rule_id', 'many2one', 'Rule Version', {'relation': 'x_incentive_rule',
                                                    'tracking': 40}),
        ('x_state', 'selection', 'Status', {'tracking': 50, 'selection': [
            ('draft', 'Draft'), ('open', 'Open'), ('calculated', 'Calculated'),
            ('approved', 'Approved'), ('locked', 'Locked')]}),
    ]),
    ('x_incentive_branch_target', 'Incentive Branch Target', [
        ('x_name', 'char', 'Name', {
            'compute': 'c_branch_target_name.py', 'store': True,
            'depends': 'x_branch_id.x_name,x_business_type,x_period_id.x_name'}),
        ('x_period_id', 'many2one', 'Period', {'relation': 'x_incentive_period',
                                                'required': True, 'ondelete': 'restrict'}),
        ('x_branch_id', 'many2one', 'Branch', {'relation': 'x_incentive_branch',
                                                'required': True}),
        ('x_business_type', 'selection', 'Business Type',
         {'selection': SEL_BTYPE, 'required': True}),
        ('x_company_id', 'many2one', 'Company', {
            'relation': 'res.company', 'related': 'x_period_id.x_company_id',
            'store': True}),
        ('x_currency_id', 'many2one', 'Currency', {
            'relation': 'res.currency', 'related': 'x_company_id.currency_id'}),
        ('x_amount', 'monetary', 'Branch Net Sales Target', {'required': True}),
        ('x_carry_forward_amount', 'monetary', 'Carry-Forward', {'readonly': True}),
        ('x_amount_total', 'monetary', 'Total Target', {
            'compute': 'c_branch_target_amount_total.py', 'store': True,
            'depends': 'x_amount,x_carry_forward_amount'}),
        ('x_state', 'selection', 'Status', {'selection': [
            ('draft', 'Draft'), ('calculated', 'Calculated'),
            ('approved', 'Approved'), ('locked', 'Locked')]}),
        ('x_recascade_reason', 'char', 'Re-cascade Reason', {
            'compute': 'c_branch_target_recascade.py', 'store': False,
            'depends': 'x_state,x_period_id,x_branch_id,x_business_type'}),
        ('x_needs_recascade', 'boolean', 'Population Changed', {
            'compute': 'c_branch_target_needs_recascade.py', 'store': False,
            'depends': 'x_recascade_reason'}),
        ('x_payout_total', 'monetary', 'Branch Payout', {
            'compute': 'c_branch_target_payout_total.py', 'store': False,
            'depends': 'x_period_id,x_branch_id,x_business_type'}),
    ]),
    ('x_incentive_target', 'Incentive Target', [
        ('x_name', 'char', 'Name', {
            'compute': 'c_target_name.py', 'store': True,
            'depends': 'x_employee_id.name,x_target_type,x_period_id.x_name'}),
        ('x_period_id', 'many2one', 'Period', {'relation': 'x_incentive_period',
                                                'required': True, 'ondelete': 'restrict'}),
        ('x_employee_id', 'many2one', 'Employee', {'relation': 'hr.employee',
                                                    'required': True, 'ondelete': 'restrict'}),
        ('x_branch_id', 'many2one', 'Branch', {
            'relation': 'x_incentive_branch',
            'related': 'x_employee_id.x_incentive_branch_id', 'store': True}),
        ('x_business_type', 'selection', 'Business Type', {
            'selection': SEL_BTYPE,
            'related': 'x_employee_id.x_incentive_business_type', 'store': True}),
        ('x_designation_id', 'many2one', 'Designation', {
            'relation': 'x_incentive_designation',
            'related': 'x_employee_id.x_incentive_designation_id', 'store': True}),
        ('x_company_id', 'many2one', 'Company', {
            'relation': 'res.company', 'related': 'x_period_id.x_company_id',
            'store': True}),
        ('x_currency_id', 'many2one', 'Currency', {
            'relation': 'res.currency', 'related': 'x_company_id.currency_id'}),
        ('x_target_type', 'selection', 'Bucket',
         {'selection': SEL_TARGET_TYPE, 'required': True}),
        ('x_amount', 'monetary', 'Amount', {'required': True}),
        ('x_source', 'selection', 'Source', {'selection': [
            ('manual', 'Manual Input'), ('rf_cascade', 'Rolling Forecast Cascade'),
            ('redistribution', 'Vacancy Redistribution'),
            ('proration', 'New Hire Proration')]}),
        ('x_fte_used', 'float', 'FTE Used', {'readonly': True}),
        ('x_date_effective_start', 'date', 'Effective Start', {}),
        ('x_date_effective_end', 'date', 'Effective End', {}),
        ('x_proration_ratio', 'float', 'Proration', {}),
        ('x_shortfall_amount', 'monetary', 'Shortfall', {'readonly': True}),
        ('x_carry_forward_amount', 'monetary', 'Carry-Forward / Month', {'readonly': True}),
        ('x_months_remaining', 'integer', 'Months Remaining', {'readonly': True}),
        ('x_note', 'char', 'Note', {}),
    ]),
    ('x_incentive_target_movement', 'Incentive Target Movement', [
        ('x_name', 'char', 'Reference', {}),
        ('x_period_id', 'many2one', 'Period', {'relation': 'x_incentive_period',
                                                'required': True, 'ondelete': 'restrict'}),
        ('x_target_id', 'many2one', 'Resulting Target', {
            'relation': 'x_incentive_target', 'ondelete': 'set null'}),
        ('x_reason', 'selection', 'Reason', {'required': True, 'selection': [
            ('resignation', 'Resignation / Vacant'), ('new_hire', 'New Hire Proration'),
            ('rf_revision', 'Rolling Forecast Revision'),
            ('replacement', 'Replacement Joined'), ('manual', 'Manual Adjustment')]}),
        ('x_from_employee_id', 'many2one', 'From', {'relation': 'hr.employee'}),
        ('x_to_employee_id', 'many2one', 'To', {'relation': 'hr.employee'}),
        ('x_currency_id', 'many2one', 'Currency', {
            'relation': 'res.currency', 'related': 'x_period_id.x_company_id.currency_id'}),
        ('x_amount', 'monetary', 'Amount', {'required': True}),
        ('x_target_type', 'selection', 'Bucket',
         {'selection': SEL_TARGET_TYPE, 'required': True}),
        ('x_fte_share', 'float', 'FTE Share', {}),
        ('x_date_effective', 'date', 'Effective Date', {}),
        ('x_note', 'char', 'Note', {}),
    ]),
    ('x_incentive_transaction', 'Incentive Transaction', [
        ('x_name', 'char', 'Reference', {'readonly': True}),
        ('x_source_type', 'selection', 'Source', {'selection': [
            ('invoice', 'Invoice'), ('pos', 'POS Order')], 'index': True}),
        ('x_move_line_id', 'many2one', 'Invoice Line', {
            'relation': 'account.move.line', 'ondelete': 'cascade', 'index': True}),
        ('x_move_id', 'many2one', 'Invoice', {
            'relation': 'account.move', 'ondelete': 'cascade', 'index': True}),
        ('x_pos_order_line_id', 'many2one', 'POS Order Line', {
            'relation': 'pos.order.line', 'ondelete': 'cascade', 'index': True}),
        ('x_pos_order_id', 'many2one', 'POS Order', {
            'relation': 'pos.order', 'ondelete': 'cascade', 'index': True}),
        ('x_employee_id', 'many2one', 'Employee', {'relation': 'hr.employee',
                                                    'required': True, 'index': True}),
        ('x_project_id', 'many2one', 'Project', {'relation': 'project.project',
                                                  'index': True}),
        ('x_split_role', 'selection', 'Credit Role', {'selection': [
            ('pm', 'Project Manager'), ('sp2', 'Salesperson 2'),
            ('sp3', 'Salesperson 3'), ('salesperson', 'Salesperson / Cashier')]}),
        ('x_split_share', 'float', 'Share', {}),
        ('x_branch_id', 'many2one', 'Branch', {
            'relation': 'x_incentive_branch',
            'related': 'x_employee_id.x_incentive_branch_id', 'store': True}),
        ('x_business_type', 'selection', 'Business Type', {
            'selection': SEL_BTYPE,
            'related': 'x_employee_id.x_incentive_business_type', 'store': True}),
        ('x_partner_id', 'many2one', 'Customer', {'relation': 'res.partner'}),
        ('x_product_id', 'many2one', 'Product', {'relation': 'product.product'}),
        ('x_company_id', 'many2one', 'Company', {'relation': 'res.company'}),
        ('x_currency_id', 'many2one', 'Currency', {
            'relation': 'res.currency', 'related': 'x_company_id.currency_id'}),
        ('x_source_period_id', 'many2one', 'Source Period', {
            'relation': 'x_incentive_period', 'required': True, 'index': True}),
        ('x_payment_period_id', 'many2one', 'Payment Period', {
            'relation': 'x_incentive_period', 'index': True}),
        ('x_payout_period_id', 'many2one', 'Payout Period', {
            'relation': 'x_incentive_period'}),
        ('x_invoice_date', 'date', 'Invoice Date', {}),
        ('x_payment_date', 'date', 'Fully Paid On', {}),
        ('x_is_prior_period', 'boolean', 'Prior-Period Invoice', {}),
        ('x_transaction_type', 'selection', 'Type', {'selection': [
            ('invoice', 'Invoice'), ('refund', 'Credit Note / Refund')]}),
        ('x_base_amount', 'monetary', 'Line Amount', {}),
        ('x_discount', 'float', 'Discount (%)', {}),
        ('x_is_downpayment', 'boolean', 'Down Payment Line', {}),
        ('x_is_discount_eligible', 'boolean', 'Discount Eligible', {}),
        ('x_is_payment_eligible', 'boolean', 'Fully Paid', {}),
        ('x_eligibility_note', 'char', 'Eligibility Note', {}),
        ('x_bucket', 'selection', 'Bucket', {'selection': [
            ('incentive', 'Incentive-Based'), ('bonus', 'Bonus-Based'),
            ('excluded', 'Excluded')]}),
        ('x_incentive_alloc', 'monetary', 'Incentive Allocation', {}),
        ('x_bonus_alloc', 'monetary', 'Bonus Allocation', {}),
        ('x_tier_id', 'many2one', 'Tier (snapshot)', {'relation': 'x_incentive_rule_tier'}),
        ('x_tier_payout_rate', 'float', 'Payout Rate (snapshot)', {}),
        ('x_payout_amount', 'monetary', 'Payout Amount', {}),
        ('x_reversal_of_id', 'many2one', 'Reversal Of', {
            'relation': 'x_incentive_transaction', 'ondelete': 'set null'}),
        ('x_state', 'selection', 'Status', {'selection': [
            ('draft', 'Draft'), ('confirmed', 'Confirmed'),
            ('paid_out', 'Paid Out'), ('reversed', 'Reversed')]}),
    ]),
    ('x_incentive_payout', 'Incentive Payout', [
        ('x_name', 'char', 'Name', {'readonly': True}),
        ('x_period_id', 'many2one', 'Period', {'relation': 'x_incentive_period',
                                                'required': True, 'ondelete': 'cascade'}),
        ('x_employee_id', 'many2one', 'Employee', {'relation': 'hr.employee',
                                                    'required': True}),
        ('x_user_id', 'many2one', 'User', {
            'relation': 'res.users', 'related': 'x_employee_id.user_id', 'store': True}),
        ('x_manager_id', 'many2one', 'Manager', {
            'relation': 'hr.employee', 'related': 'x_employee_id.parent_id', 'store': True}),
        ('x_branch_id', 'many2one', 'Branch', {
            'relation': 'x_incentive_branch',
            'related': 'x_employee_id.x_incentive_branch_id', 'store': True}),
        ('x_business_type', 'selection', 'Business Type', {
            'selection': SEL_BTYPE,
            'related': 'x_employee_id.x_incentive_business_type', 'store': True}),
        ('x_company_id', 'many2one', 'Company', {
            'relation': 'res.company', 'related': 'x_period_id.x_company_id',
            'store': True}),
        ('x_currency_id', 'many2one', 'Currency', {
            'relation': 'res.currency', 'related': 'x_company_id.currency_id'}),
        ('x_target_incentive', 'monetary', 'Target Incentive', {}),
        ('x_target_bonus', 'monetary', 'Target Bonus', {}),
        ('x_target_total', 'monetary', 'Target Total', {}),
        ('x_is_mixed', 'boolean', 'Mixed Scenario', {}),
        ('x_gross_sales', 'monetary', 'Gross Sales', {}),
        ('x_sales_return', 'monetary', 'Sales Return', {}),
        ('x_net_sales', 'monetary', 'Net Sales', {}),
        ('x_achievement_pct', 'float', 'Achievement', {}),
        ('x_tier_id', 'many2one', 'Tier', {'relation': 'x_incentive_rule_tier'}),
        ('x_tier_level', 'integer', 'Tier Level', {}),
        ('x_payout_rate', 'float', 'Payout Rate', {}),
        ('x_eligible_incentive', 'monetary', 'Eligible Achievement Incentive', {}),
        ('x_eligible_bonus', 'monetary', 'Eligible Achievement Bonus', {}),
        ('x_excluded_discount', 'monetary', 'Excluded (Discount > cap)', {}),
        ('x_paid_current_month', 'monetary', 'Paid Current Month', {}),
        ('x_paid_prior_month', 'monetary', 'Paid Prior Month', {}),
        ('x_paid_bonus', 'monetary', 'Paid Bonus', {}),
        ('x_payout_current', 'monetary', 'Incentive Payout Current Month', {}),
        ('x_payout_prior', 'monetary', 'Incentive Payout Previous Month', {}),
        ('x_incentive_payout', 'monetary', 'Incentive Payout', {}),
        ('x_payout_bonus', 'monetary', 'Bonus Payout', {}),
        ('x_branch_target', 'monetary', 'Branch Target', {}),
        ('x_branch_net_sales', 'monetary', 'Branch Net Sales', {}),
        ('x_branch_achievement_pct', 'float', 'Branch Achievement', {}),
        ('x_branch_tier_id', 'many2one', 'Branch Tier', {'relation': 'x_incentive_rule_tier'}),
        ('x_branch_tier_level', 'integer', 'Branch Tier Level', {}),
        ('x_branch_payout_rate', 'float', 'Branch Payout Rate', {}),
        ('x_branch_eligible', 'monetary', 'Branch Eligible Base', {}),
        ('x_branch_paid', 'monetary', 'Branch Paid Base', {}),
        ('x_branch_pool', 'monetary', 'Branch Pool', {}),
        ('x_branch_fte', 'float', 'Branch FTE Weight', {}),
        ('x_branch_fte_share', 'float', 'Branch FTE Share', {}),
        ('x_branch_payout', 'monetary', 'Branch Payout', {}),
        ('x_total_payout', 'monetary', 'Total Payout', {}),
        ('x_is_eligible', 'boolean', 'Eligible Month', {}),
        ('x_is_frozen', 'boolean', 'Frozen', {'readonly': True}),
        ('x_computation_log', 'text', 'Computation Log', {'readonly': True}),
    ]),
    ('x_incentive_cascade', 'Cascade Branch Target', [
        ('x_name', 'char', 'Name', {
            'compute': 'c_cascade_name.py', 'store': True,
            'depends': 'x_period_id.x_name,x_business_type'}),
        ('x_period_id', 'many2one', 'Period', {'relation': 'x_incentive_period',
                                                'required': True, 'ondelete': 'cascade'}),
        ('x_branch_ids', 'many2many', 'Branches', {'relation': 'x_incentive_branch'}),
        ('x_business_type', 'selection', 'Business Type',
         {'selection': SEL_BTYPE, 'required': True}),
        ('x_scope', 'selection', 'Scope', {'selection': [
            ('individual', 'Individual Target'), ('branch', 'Branch Pool')]}),
        ('x_redistribute_vacant', 'boolean', 'Redistribute Vacant Slots', {}),
        ('x_overwrite_existing', 'boolean', 'Overwrite Existing Targets', {}),
        ('x_currency_id', 'many2one', 'Currency', {
            'relation': 'res.currency', 'related': 'x_period_id.x_company_id.currency_id'}),
        ('x_carry_forward_total', 'monetary', 'Carry-Forward Total', {'readonly': True}),
    ]),
    ('x_incentive_cascade_line', 'Cascade Preview Line', [
        ('x_cascade_id', 'many2one', 'Cascade', {'relation': 'x_incentive_cascade',
                                                 'ondelete': 'cascade'}),
        ('x_branch_target_id', 'many2one', 'Branch Target', {
            'relation': 'x_incentive_branch_target', 'required': True,
            'ondelete': 'cascade'}),
        ('x_branch_id', 'many2one', 'Branch', {
            'relation': 'x_incentive_branch',
            'related': 'x_branch_target_id.x_branch_id'}),
        ('x_employee_id', 'many2one', 'Employee', {'relation': 'hr.employee',
                                                    'required': True, 'ondelete': 'cascade'}),
        ('x_designation_id', 'many2one', 'Designation', {
            'relation': 'x_incentive_designation',
            'related': 'x_employee_id.x_incentive_designation_id'}),
        ('x_currency_id', 'many2one', 'Currency', {
            'relation': 'res.currency', 'related': 'x_cascade_id.x_currency_id'}),
        ('x_fte', 'float', 'FTE', {}),
        ('x_proration', 'float', 'Proration', {}),
        ('x_base_amount', 'monetary', 'Base Incentive', {}),
        ('x_carry_forward_amount', 'monetary', 'Carry-Forward', {}),
        ('x_incentive_amount', 'monetary', 'Total Incentive', {}),
        ('x_bonus_amount', 'monetary', 'Bonus', {}),
    ]),
    ('x_incentive_refund', 'Refund Incentive Transaction', [
        ('x_name', 'char', 'Name', {}),
        ('x_transaction_id', 'many2one', 'Transaction', {
            'relation': 'x_incentive_transaction', 'required': True,
            'ondelete': 'cascade'}),
        ('x_move_id', 'many2one', 'Invoice', {
            'relation': 'account.move', 'related': 'x_transaction_id.x_move_id'}),
        ('x_employee_id', 'many2one', 'Employee', {
            'relation': 'hr.employee', 'related': 'x_transaction_id.x_employee_id'}),
        ('x_currency_id', 'many2one', 'Currency', {
            'relation': 'res.currency', 'related': 'x_transaction_id.x_currency_id'}),
        ('x_base_amount', 'monetary', 'Invoice Line Amount', {
            'compute': 'c_refund_base_amount.py', 'store': False,
            'depends': 'x_transaction_id'}),
        ('x_refundable_amount', 'monetary', 'Refundable', {
            'compute': 'c_refund_refundable_amount.py', 'store': False,
            'depends': 'x_transaction_id'}),
        ('x_refund_amount', 'monetary', 'Refund Amount', {'required': True}),
        ('x_refund_move_id', 'many2one', 'Credit Note', {
            'relation': 'account.move', 'readonly': True}),
    ]),
    ('x_incentive_refund_policy', 'Incentive Refund Policy', [
        ('x_name', 'char', 'Name', {'required': True}),
        ('x_sequence', 'integer', 'Sequence', {}),
        ('x_stock_type', 'selection', 'Stock Type', {'selection': [
            ('available', 'Available Stock'), ('indent', 'Indent'),
            ('service', 'Jasa / Service'), ('any', 'All Types')]}),
        ('x_is_wip', 'boolean', 'Work In Progress', {}),
        ('x_payment_status', 'selection', 'Payment Status', {'selection': [
            ('partial', 'Partially Paid'), ('paid', 'Fully Paid'),
            ('any', 'Partial or Fully Paid')]}),
        ('x_initiator', 'selection', 'Initiator', {'selection': [
            ('customer', 'Customer'), ('company', 'Company (VIF)')]}),
        ('x_refund_pct', 'float', 'Refund %', {}),
        ('x_by_agreement', 'boolean', 'By Agreement', {}),
        ('x_note', 'char', 'Note', {}),
        ('x_active', 'boolean', 'Active', {}),
    ]),
]

# Fields added to STANDARD models. hr.employee must come before the models
# that relate through it (target / transaction / payout use its fields), so
# the build creates these right after the masters -- see BUILD_ORDER.
STANDARD_FIELDS = [
    ('hr.employee', [
        ('x_incentive_branch_id', 'many2one', 'Sales Branch',
         {'relation': 'x_incentive_branch'}),
        ('x_incentive_business_type', 'selection', 'Business Type',
         {'selection': SEL_BTYPE}),
        ('x_incentive_designation_id', 'many2one', 'FTE Designation',
         {'relation': 'x_incentive_designation'}),
        ('x_incentive_date_start', 'date', 'Effective Target Start', {}),
        ('x_incentive_date_end', 'date', 'Resignation Date', {}),
        ('x_is_vacant_slot', 'boolean', 'Vacant Position', {}),
        ('x_is_global_branch_member', 'boolean', 'Global Branch Member', {}),
        ('x_branch_incentive_eligible', 'boolean', 'Branch Incentive Eligible', {
            'compute': 'c_employee_branch_eligible.py', 'store': True,
            'readonly': False, 'depends': 'x_incentive_designation_id'}),
        ('x_individual_incentive_eligible', 'boolean', 'Individual Incentive Eligible', {
            'compute': 'c_employee_individual_eligible.py', 'store': True,
            'readonly': False, 'depends': 'x_incentive_designation_id'}),
    ]),
    ('account.move', [
        ('x_incentive_employee_id', 'many2one', 'Incentive Salesperson', {
            'relation': 'hr.employee',
            'help': 'Filled by automation "VIF: Invoice Incentive Salesperson". '
                    'Only used for invoices without a project.'}),
    ]),
]

# One2many fields, created once both ends exist.
EXTRA_FIELDS = [
    ('x_incentive_branch', 'x_employee_ids', 'one2many', 'Sales Team',
     {'relation': 'hr.employee', 'relation_field': 'x_incentive_branch_id'}),
    ('x_incentive_rule', 'x_tier_ids', 'one2many', 'Tiers',
     {'relation': 'x_incentive_rule_tier', 'relation_field': 'x_rule_id'}),
    ('x_incentive_period', 'x_branch_target_ids', 'one2many', 'Branch Targets',
     {'relation': 'x_incentive_branch_target', 'relation_field': 'x_period_id'}),
    ('x_incentive_period', 'x_target_ids', 'one2many', 'Targets',
     {'relation': 'x_incentive_target', 'relation_field': 'x_period_id'}),
    ('x_incentive_period', 'x_payout_ids', 'one2many', 'Payouts',
     {'relation': 'x_incentive_payout', 'relation_field': 'x_period_id'}),
    ('x_incentive_period', 'x_transaction_ids', 'one2many', 'Source Transactions',
     {'relation': 'x_incentive_transaction', 'relation_field': 'x_source_period_id'}),
    ('x_incentive_transaction', 'x_reversal_ids', 'one2many', 'Reversals',
     {'relation': 'x_incentive_transaction', 'relation_field': 'x_reversal_of_id'}),
    ('x_incentive_cascade', 'x_line_ids', 'one2many', 'Preview',
     {'relation': 'x_incentive_cascade_line', 'relation_field': 'x_cascade_id'}),
    # Period totals read the one2many above, so they come after it.
    ('x_incentive_period', 'x_total_target', 'monetary', 'Total Target', {
        'compute': 'c_period_total_target.py', 'store': False,
        'depends': 'x_target_ids.x_amount'}),
    ('x_incentive_period', 'x_total_payout', 'monetary', 'Total Payout', {
        'compute': 'c_period_total_payout.py', 'store': False,
        'depends': 'x_payout_ids.x_total_payout'}),
    ('account.move', 'x_incentive_transaction_ids', 'one2many', 'Incentive Transactions',
     {'relation': 'x_incentive_transaction', 'relation_field': 'x_move_id'}),
    ('pos.order', 'x_incentive_transaction_ids', 'one2many', 'Incentive Transactions',
     {'relation': 'x_incentive_transaction', 'relation_field': 'x_pos_order_id'}),
    ('hr.employee', 'x_incentive_payout_ids', 'one2many', 'Incentive Payouts',
     {'relation': 'x_incentive_payout', 'relation_field': 'x_employee_id'}),
]

# Models with a chatter (Settings > Technical > Models > Has Mail Thread /
# Has Mail Activity). Tick them when creating the model: once on, Odoo does
# not let them be switched off again.
MAIL_MODELS = ['x_incentive_period']

# Creation order: masters, then the employee fields every later model relates
# through, then the rest.
BUILD_ORDER = [
    'x_incentive_designation', 'x_incentive_branch',
    'hr.employee', 'account.move',
    'x_incentive_rule', 'x_incentive_rule_tier', 'x_incentive_period',
    'x_incentive_branch_target', 'x_incentive_target',
    'x_incentive_target_movement', 'x_incentive_transaction',
    'x_incentive_payout', 'x_incentive_cascade', 'x_incentive_cascade_line',
    'x_incentive_refund', 'x_incentive_refund_policy',
]

# Default values (Studio: field -> Properties -> Default Value).
DEFAULTS = [
    ('x_incentive_designation', 'x_active', True),
    ('x_incentive_designation', 'x_branch_eligible', True),
    ('x_incentive_designation', 'x_individual_eligible', True),
    ('x_incentive_designation', 'x_fte_branch', 1.0),
    ('x_incentive_designation', 'x_fte_individual', 1.0),
    ('x_incentive_branch', 'x_active', True),
    ('x_incentive_rule', 'x_active', True),
    ('x_incentive_rule', 'x_base_rate', 0.0075),
    ('x_incentive_rule', 'x_bonus_rate', 0.01),
    ('x_incentive_rule', 'x_max_discount', 35.0),
    ('x_incentive_rule', 'x_cap_tier_in_mixed', True),
    ('x_incentive_rule', 'x_mixed_cap_tier_level', 4),
    ('x_incentive_period', 'x_state', 'draft'),
    ('x_incentive_branch_target', 'x_state', 'draft'),
    ('x_incentive_branch_target', 'x_business_type', 'b2b'),
    ('x_incentive_target', 'x_target_type', 'incentive'),
    ('x_incentive_target', 'x_source', 'manual'),
    ('x_incentive_target', 'x_proration_ratio', 1.0),
    ('x_incentive_target_movement', 'x_reason', 'manual'),
    ('x_incentive_target_movement', 'x_target_type', 'bonus'),
    ('x_incentive_cascade', 'x_business_type', 'b2b'),
    ('x_incentive_cascade', 'x_scope', 'individual'),
    ('x_incentive_cascade', 'x_redistribute_vacant', True),
    ('x_incentive_cascade', 'x_overwrite_existing', True),
    ('x_incentive_refund_policy', 'x_active', True),
]

# Server actions (Settings > Technical > Server Actions, Action To Do =
# Execute Code). (name, model, code file under actions/)
SERVER_ACTIONS = [
    ('VIF: Engine Calculate', 'x_incentive_period', 'sa_engine_calculate.py'),
    ('VIF: Period Open', 'x_incentive_period', 'sa_period_open.py'),
    ('VIF: Period Approve', 'x_incentive_period', 'sa_period_approve.py'),
    ('VIF: Period Lock', 'x_incentive_period', 'sa_period_lock.py'),
    ('VIF: Period Reset to Open', 'x_incentive_period', 'sa_period_reset.py'),
    ('VIF: Period Generate Next', 'x_incentive_period', 'sa_period_generate_next.py'),
    ('VIF: Branch Target Calculate', 'x_incentive_branch_target', 'sa_bt_calculate.py'),
    ('VIF: Branch Target Approve', 'x_incentive_branch_target', 'sa_bt_approve.py'),
    ('VIF: Branch Target Lock', 'x_incentive_branch_target', 'sa_bt_lock.py'),
    ('VIF: Branch Target Reset to Draft', 'x_incentive_branch_target', 'sa_bt_reset.py'),
    ('VIF: Cascade Preview', 'x_incentive_cascade', 'sa_cascade_preview.py'),
    ('VIF: Cascade Apply', 'x_incentive_cascade', 'sa_cascade_apply.py'),
    ('VIF: Target Movement Apply', 'x_incentive_target_movement', 'sa_movement_apply.py'),
    ('VIF: Transaction Refund', 'x_incentive_transaction', 'sa_tx_open_refund.py'),
    ('VIF: Refund Confirm', 'x_incentive_refund', 'sa_refund_confirm.py'),
    ('VIF: Backfill Invoice Salesperson', 'x_incentive_period',
     'sa_backfill_incentive_employee.py'),
]

# Automation rules (Settings > Technical > Automation Rules).
# (name, model, trigger, fields that trigger it, code file under automations/)
AUTOMATIONS = [
    ('VIF: Check Target', 'x_incentive_target', 'on_create_or_write',
     ['x_period_id', 'x_employee_id', 'x_target_type', 'x_amount'], 'au_check_target.py'),
    ('VIF: Check Branch Target', 'x_incentive_branch_target', 'on_create_or_write',
     ['x_period_id', 'x_branch_id', 'x_business_type'], 'au_check_branch_target.py'),
    ('VIF: Check Period', 'x_incentive_period', 'on_create_or_write',
     ['x_date_start', 'x_date_end', 'x_company_id'], 'au_check_period.py'),
    ('VIF: Check Tier Ranges', 'x_incentive_rule_tier', 'on_create_or_write',
     ['x_achievement_min', 'x_achievement_max', 'x_rule_id'], 'au_check_tier.py'),
    ('VIF: Check Same-Day Handover', 'hr.employee', 'on_create_or_write',
     ['x_incentive_branch_id', 'x_incentive_business_type',
      'x_incentive_date_start', 'x_incentive_date_end'], 'au_check_employee.py'),
    ('VIF: Target Movement Reference', 'x_incentive_target_movement', 'on_create',
     [], 'au_movement_name.py'),
    ('VIF: Invoice Incentive Salesperson', 'account.move', 'on_create_or_write',
     ['invoice_user_id'], 'au_move_incentive_employee.py'),
    ('VIF: POS Invoice Cashier', 'pos.order', 'on_create_or_write',
     ['account_move'], 'au_pos_invoice_cashier.py'),
]

# Views (Settings > Technical > User Interface > Views). Replace every
# "[ID <server action name>]" in the XML with that server action's ID.
# (view name, model, type, file under views/, inherited view xmlid or None)
VIEWS = [
    ('x_incentive_period.form', 'x_incentive_period', 'form', 'period_form.xml', None),
    ('x_incentive_period.list', 'x_incentive_period', 'list', 'period_list.xml', None),
    ('x_incentive_branch_target.form', 'x_incentive_branch_target', 'form', 'branch_target_form.xml', None),
    ('x_incentive_branch_target.list', 'x_incentive_branch_target', 'list', 'branch_target_list.xml', None),
    ('x_incentive_cascade.form', 'x_incentive_cascade', 'form', 'cascade_form.xml', None),
    ('x_incentive_cascade.list', 'x_incentive_cascade', 'list', 'cascade_list.xml', None),
    ('x_incentive_target.list', 'x_incentive_target', 'list', 'target_list.xml', None),
    ('x_incentive_target_movement.form', 'x_incentive_target_movement', 'form', 'movement_form.xml', None),
    ('x_incentive_target_movement.list', 'x_incentive_target_movement', 'list', 'movement_list.xml', None),
    ('x_incentive_transaction.form', 'x_incentive_transaction', 'form', 'transaction_form.xml', None),
    ('x_incentive_transaction.list', 'x_incentive_transaction', 'list', 'transaction_list.xml', None),
    ('x_incentive_transaction.search', 'x_incentive_transaction', 'search', 'transaction_search.xml', None),
    ('x_incentive_payout.form', 'x_incentive_payout', 'form', 'payout_form.xml', None),
    ('x_incentive_payout.list', 'x_incentive_payout', 'list', 'payout_list.xml', None),
    ('x_incentive_payout.search', 'x_incentive_payout', 'search', 'payout_search.xml', None),
    ('x_incentive_refund.form', 'x_incentive_refund', 'form', 'refund_form.xml', None),
    ('x_incentive_rule.form', 'x_incentive_rule', 'form', 'rule_form.xml', None),
    ('x_incentive_rule.list', 'x_incentive_rule', 'list', 'rule_list.xml', None),
    ('x_incentive_branch.form', 'x_incentive_branch', 'form', 'branch_form.xml', None),
    ('x_incentive_branch.list', 'x_incentive_branch', 'list', 'branch_list.xml', None),
    ('x_incentive_designation.list', 'x_incentive_designation', 'list', 'designation_list.xml', None),
    ('x_incentive_refund_policy.list', 'x_incentive_refund_policy', 'list', 'refund_policy_list.xml', None),
    ('hr.employee.form.x_incentive', 'hr.employee', 'form', 'employee_form_inherit.xml', 'hr.view_employee_form'),
    ('account.move.form.x_incentive', 'account.move', 'form', 'move_form_inherit.xml', 'account.view_move_form'),
    ('pos.order.form.x_incentive', 'pos.order', 'form', 'pos_order_form_inherit.xml', 'point_of_sale.view_pos_pos_form'),
]

# Window actions (Settings > Technical > Actions > Window Actions).
# (name, model, view_mode, domain, context)
WINDOW_ACTIONS = [
    ('Incentive Periods', 'x_incentive_period', 'list,form', '[]', '{}'),
    ('Branch Targets', 'x_incentive_branch_target', 'list,form', '[]', '{}'),
    ('Cascade Branch Target', 'x_incentive_cascade', 'list,form', '[]', '{}'),
    ('Targets', 'x_incentive_target', 'list', '[]', '{}'),
    ('Target Movements', 'x_incentive_target_movement', 'list,form', '[]', '{}'),
    ('Payouts', 'x_incentive_payout', 'list,form', '[]', "{'search_default_g_period': 1}"),
    ('My Incentive', 'x_incentive_payout', 'list,form', "[('x_employee_id.user_id', '=', uid)]", '{}'),
    ('Transactions', 'x_incentive_transaction', 'list,form', '[]', '{}'),
    ('Rules & Tiers', 'x_incentive_rule', 'list,form', '[]', '{}'),
    ('Sales Branches', 'x_incentive_branch', 'list,form', '[]', '{}'),
    ('FTE Designations', 'x_incentive_designation', 'list', '[]', '{}'),
    ('Refund Policies', 'x_incentive_refund_policy', 'list', '[]', '{}'),
]

# Menus (Settings > Technical > User Interface > Menu Items).
# (menu name, parent menu name or None, window action name or None, sequence)
MENUS = [
    ('Sales Incentive', None, None, 60),
    ('Operations', 'Sales Incentive', None, 10),
    ('Incentive Periods', 'Operations', 'Incentive Periods', 10),
    ('Branch Targets', 'Operations', 'Branch Targets', 20),
    ('Cascade Branch Target', 'Operations', 'Cascade Branch Target', 30),
    ('Targets', 'Operations', 'Targets', 40),
    ('Target Movements', 'Operations', 'Target Movements', 50),
    ('Reporting', 'Sales Incentive', None, 20),
    ('My Incentive', 'Reporting', 'My Incentive', 5),
    ('Payouts', 'Reporting', 'Payouts', 10),
    ('Transactions', 'Reporting', 'Transactions', 20),
    ('Configuration', 'Sales Incentive', None, 90),
    ('Rules & Tiers', 'Configuration', 'Rules & Tiers', 10),
    ('Sales Branches', 'Configuration', 'Sales Branches', 20),
    ('FTE Designations', 'Configuration', 'FTE Designations', 30),
    ('Refund Policies', 'Configuration', 'Refund Policies', 40),
]

# Security (Settings > Users & Companies > Groups; Technical > Access Rights /
# Record Rules). Each group implies the one before it.
GROUPS = [
    ('VIF Incentive / Salesperson', None),
    ('VIF Incentive / Manager', 'VIF Incentive / Salesperson'),
    ('VIF Incentive / Administrator', 'VIF Incentive / Manager'),
]
# Salesperson (and so Manager): READ ONLY on these. Administrator: full CRUD
# on every x_incentive_* model.
READ_MODELS = [
    'x_incentive_branch', 'x_incentive_branch_target', 'x_incentive_designation',
    'x_incentive_period', 'x_incentive_rule', 'x_incentive_rule_tier',
    'x_incentive_target', 'x_incentive_target_movement', 'x_incentive_refund_policy',
    'x_incentive_transaction', 'x_incentive_payout',
]
# (rule name, model, group, domain)
RECORD_RULES = [
    ('Payout: own', 'x_incentive_payout', 'VIF Incentive / Salesperson',
     "[('x_employee_id.user_id', '=', user.id)]"),
    ('Payout: subordinates', 'x_incentive_payout', 'VIF Incentive / Manager',
     "['|', ('x_employee_id.user_id', '=', user.id), ('x_employee_id', 'child_of', user.employee_id.id)]"),
    ('Payout: all', 'x_incentive_payout', 'VIF Incentive / Administrator', "[(1, '=', 1)]"),
    ('Target: own', 'x_incentive_target', 'VIF Incentive / Salesperson',
     "[('x_employee_id.user_id', '=', user.id)]"),
    ('Target: subordinates', 'x_incentive_target', 'VIF Incentive / Manager',
     "['|', ('x_employee_id.user_id', '=', user.id), ('x_employee_id', 'child_of', user.employee_id.id)]"),
    ('Target: all', 'x_incentive_target', 'VIF Incentive / Administrator', "[(1, '=', 1)]"),
    ('Transaction: own', 'x_incentive_transaction', 'VIF Incentive / Salesperson',
     "[('x_employee_id.user_id', '=', user.id)]"),
    ('Transaction: subordinates', 'x_incentive_transaction', 'VIF Incentive / Manager',
     "['|', ('x_employee_id.user_id', '=', user.id), ('x_employee_id', 'child_of', user.employee_id.id)]"),
    ('Transaction: all', 'x_incentive_transaction', 'VIF Incentive / Administrator', "[(1, '=', 1)]"),
]

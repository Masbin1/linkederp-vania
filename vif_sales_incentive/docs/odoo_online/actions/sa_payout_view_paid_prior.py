# Server Action : "VIF: Payout View Paid Prior"   Model: x_incentive_payout
# Button        : smart button Paid Prior Month (SQ3 -- prior invoices paid this period)
# Port of: incentive.payout.action_view_transactions filtered by payment period + prior source
# Same domain as the engine's prior_tx query: prior-period invoices, fully
# paid in THIS period, with an incentive allocation -- the x_paid_prior_month set.
action = {
    'type': 'ir.actions.act_window',
    'name': 'Paid Prior Month -- %s' % record.x_employee_id.name,
    'res_model': 'x_incentive_transaction',
    'view_mode': 'list,pivot,form',
    'domain': [
        ('x_employee_id', '=', record.x_employee_id.id),
        ('x_payment_period_id', '=', record.x_period_id.id),
        ('x_source_period_id', '!=', record.x_period_id.id),
        ('x_transaction_type', '=', 'invoice'),
        ('x_is_discount_eligible', '=', True),
        ('x_is_payment_eligible', '=', True),
        ('x_is_downpayment', '=', False),
        ('x_state', '!=', 'reversed'),
        ('x_incentive_alloc', '>', 0.0),
    ],
    'context': {
        'search_default_g_source': 1,
    },
}

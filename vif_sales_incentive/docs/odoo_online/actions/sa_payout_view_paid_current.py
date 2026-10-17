# Server Action : "VIF: Payout View Paid Current"   Model: x_incentive_payout
# Button        : smart button Paid Current Month (SQ3 -- fully paid this period)
# Port of: incentive.payout.action_view_transactions filtered by payment period
# Rows of THIS period, discount-eligible, not a down-payment, fully paid in
# this same period -- exactly the set summed into x_paid_current_month.
action = {
    'type': 'ir.actions.act_window',
    'name': 'Paid Current Month -- %s' % record.x_employee_id.name,
    'res_model': 'x_incentive_transaction',
    'view_mode': 'list,pivot,form',
    'domain': [
        ('x_employee_id', '=', record.x_employee_id.id),
        ('x_source_period_id', '=', record.x_period_id.id),
        ('x_payment_period_id', '=', record.x_period_id.id),
        ('x_transaction_type', '=', 'invoice'),
        ('x_is_discount_eligible', '=', True),
        ('x_is_payment_eligible', '=', True),
        ('x_is_downpayment', '=', False),
        ('x_state', '!=', 'reversed'),
    ],
    'context': {},
}

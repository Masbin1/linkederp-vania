# Server Action : "VIF: Payout View Gross Sales"   Model: x_incentive_payout
# Button        : smart button Gross Sales (SQ1 breakdown)
# Port of: incentive.payout.action_view_transactions filtered by source period
# Matches the engine: gross = invoice rows of the source period, not reversed.
action = {
    'type': 'ir.actions.act_window',
    'name': 'Gross Sales -- %s' % record.x_employee_id.name,
    'res_model': 'x_incentive_transaction',
    'view_mode': 'list,pivot,form',
    'domain': [
        ('x_employee_id', '=', record.x_employee_id.id),
        ('x_source_period_id', '=', record.x_period_id.id),
        ('x_transaction_type', '=', 'invoice'),
        ('x_state', '!=', 'reversed'),
    ],
    'context': {},
}

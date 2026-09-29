# Server Action : "VIF: Payout View Transactions"   Model: x_incentive_payout
# Button        : smart button "Transactions"
# Port of incentive.payout.action_view_transactions.
action = {
    'type': 'ir.actions.act_window',
    'name': 'Transactions -- %s' % record.x_employee_id.name,
    'res_model': 'x_incentive_transaction',
    'view_mode': 'list,form',
    'domain': [
        ('x_employee_id', '=', record.x_employee_id.id),
        '|',
        ('x_source_period_id', '=', record.x_period_id.id),
        ('x_payment_period_id', '=', record.x_period_id.id),
    ],
}

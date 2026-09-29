# Server Action : "VIF: Period View Transactions"   Model: x_incentive_period
# Button        : smart button "Transactions"
# Port of incentive.period.action_view_transactions.
action = {
    'type': 'ir.actions.act_window',
    'name': 'Transactions -- %s' % record.x_name,
    'res_model': 'x_incentive_transaction',
    'view_mode': 'list,form',
    'domain': [('x_source_period_id', '=', record.id)],
}

# Server Action : "VIF: Period View Payouts"   Model: x_incentive_period
# Button        : smart button "Payouts"
# Port of incentive.period.action_view_payouts.
action = {
    'type': 'ir.actions.act_window',
    'name': 'Payouts -- %s' % record.x_name,
    'res_model': 'x_incentive_payout',
    'view_mode': 'list,form',
    'domain': [('x_period_id', '=', record.id)],
    'context': {'default_x_period_id': record.id},
}

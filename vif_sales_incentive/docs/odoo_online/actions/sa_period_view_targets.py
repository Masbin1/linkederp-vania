# Server Action : "VIF: Period View Targets"   Model: x_incentive_period
# Button        : smart button "Targets"
# Port of incentive.period.action_view_targets.
action = {
    'type': 'ir.actions.act_window',
    'name': 'Targets -- %s' % record.x_name,
    'res_model': 'x_incentive_target',
    'view_mode': 'list,form',
    'domain': [('x_period_id', '=', record.id)],
    'context': {'default_x_period_id': record.id},
}

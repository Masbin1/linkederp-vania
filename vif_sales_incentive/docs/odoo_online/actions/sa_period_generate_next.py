# Server Action : "VIF: Period Generate Next"   Model: x_incentive_period
# Button        : Generate Next Period
rd = dateutil.relativedelta.relativedelta
new = env['x_incentive_period']
for rec in records:
    start = rec.x_date_start + rd(months=1)
    new |= env['x_incentive_period'].create({
        'x_name': start.strftime('%b %Y'),
        'x_date_start': start,
        'x_date_end': start + rd(months=1, days=-1),
        'x_rule_id': rec.x_rule_id.id,
        'x_company_id': rec.x_company_id.id,
        'x_state': 'draft',
    })
action = {
    'type': 'ir.actions.act_window',
    'res_model': 'x_incentive_period',
    'view_mode': 'form',
    'res_id': new[:1].id,
}

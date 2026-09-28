# Server Action : "VIF: Period Open"      Model: x_incentive_period
# Button        : Open (visible when state = draft)
for rec in records:
    if not rec.x_rule_id:
        raise UserError('Assign a Rule Version before opening period %s.' % rec.x_name)
    rec.write({'x_state': 'open'})

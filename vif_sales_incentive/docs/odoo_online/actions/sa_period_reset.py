# Server Action : "VIF: Period Reset to Open"   Model: x_incentive_period
# Button        : Reset to Open (visible when state in calculated, approved)
for rec in records:
    if rec.x_state == 'locked':
        raise UserError('Period %s is locked. Create an adjustment in a later '
                        'period instead.' % rec.x_name)
    rec.write({'x_state': 'open'})
    rec.x_branch_target_ids.filtered(
        lambda b: b.x_state == 'approved').write({'x_state': 'calculated'})

# Server Action : "VIF: Period Approve"   Model: x_incentive_period
# Button        : Approve (visible when state = calculated)
for rec in records:
    if rec.x_state != 'calculated':
        raise UserError('Calculate period %s before approving.' % rec.x_name)
    rec.write({'x_state': 'approved'})
    rec.x_branch_target_ids.filtered(
        lambda b: b.x_state == 'calculated').write({'x_state': 'approved'})

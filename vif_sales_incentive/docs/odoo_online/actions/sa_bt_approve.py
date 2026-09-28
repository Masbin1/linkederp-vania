# Server Action : "VIF: Branch Target Approve"   Model: x_incentive_branch_target
# Button        : Approve (visible when state = calculated)
for rec in records:
    if rec.x_state != 'calculated':
        raise UserError('Calculate branch target %s before approving.' % rec.x_name)
records.write({'x_state': 'approved'})

# Server Action : "VIF: Branch Target Reset to Draft"   Model: x_incentive_branch_target
# Button        : Reset to Draft (visible when state in calculated, approved)
for rec in records:
    if rec.x_state == 'locked' or rec.x_period_id.x_state == 'locked':
        raise UserError('Branch target %s is locked. Create an adjustment in a '
                        'later period instead.' % rec.x_name)
records.write({'x_state': 'draft'})

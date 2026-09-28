# Server Action : "VIF: Target Movement Apply"   Model: x_incentive_target_movement
# Button        : Apply
# Materialise the movement into the receiving employee's target row.
Target = env['x_incentive_target']
for mv in records:
    if mv.x_period_id.x_state in ('approved', 'locked'):
        raise UserError('Period %s is closed.' % mv.x_period_id.x_name)
    if not mv.x_to_employee_id:
        raise UserError('Set the receiving salesperson first.')
    target = Target.search([
        ('x_period_id', '=', mv.x_period_id.id),
        ('x_employee_id', '=', mv.x_to_employee_id.id),
        ('x_target_type', '=', mv.x_target_type)], limit=1)
    if target:
        target.write({'x_amount': target.x_amount + mv.x_amount})
    else:
        target = Target.create({
            'x_period_id': mv.x_period_id.id,
            'x_employee_id': mv.x_to_employee_id.id,
            'x_target_type': mv.x_target_type,
            'x_amount': mv.x_amount,
            'x_source': 'redistribution' if mv.x_reason == 'resignation' else 'manual',
            'x_fte_used': mv.x_fte_share,
            'x_proration_ratio': 1.0,
        })
    mv.write({'x_target_id': target.id})

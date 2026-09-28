# Automation Rule : "VIF: Check Target"
# Model           : Incentive Target (x_incentive_target)
# Trigger         : On create and edit
#                   (When updating: Period, Employee, Bucket, Amount)
# Action          : Execute Code
# Replaces: unique(period, employee, bucket) + "no change after approval".
for rec in records:
    if rec.x_period_id.x_state in ('approved', 'locked'):
        raise UserError('Period %s is %s -- targets can no longer be changed.'
                        % (rec.x_period_id.x_name, rec.x_period_id.x_state))
    dup = env['x_incentive_target'].search_count([
        ('id', '!=', rec.id),
        ('x_period_id', '=', rec.x_period_id.id),
        ('x_employee_id', '=', rec.x_employee_id.id),
        ('x_target_type', '=', rec.x_target_type)])
    if dup:
        raise UserError('%s already has a %s target in %s.'
                        % (rec.x_employee_id.name, rec.x_target_type, rec.x_period_id.x_name))

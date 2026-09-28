# Field  : x_incentive_target.x_name
# Depends: x_employee_id.name, x_target_type, x_period_id.x_name
for record in self:
    record['x_name'] = '%s - %s - %s' % (
        record.x_employee_id.name or '',
        record.x_target_type or '',
        record.x_period_id.x_name or '')

# Field  : x_incentive_branch_target.x_name
# Depends: x_branch_id.x_name, x_business_type, x_period_id.x_name
for record in self:
    record['x_name'] = '%s / %s -- %s' % (
        record.x_branch_id.x_name or '',
        (record.x_business_type or '').upper(),
        record.x_period_id.x_name or '')

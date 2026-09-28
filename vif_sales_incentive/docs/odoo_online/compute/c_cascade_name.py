# Field  : x_incentive_cascade.x_name
# Depends: x_period_id.x_name, x_business_type
for record in self:
    record['x_name'] = 'Cascade %s %s' % (
        record.x_period_id.x_name or '', (record.x_business_type or '').upper())

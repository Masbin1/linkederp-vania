# Field  : x_incentive_period.x_total_target   (not stored)
# Depends: x_target_ids.x_amount
for record in self:
    record['x_total_target'] = sum(record.x_target_ids.mapped('x_amount'))

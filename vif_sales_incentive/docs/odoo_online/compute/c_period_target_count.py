# Field  : x_incentive_period.x_target_count   (not stored)
# Depends: x_target_ids
for record in self:
    record['x_target_count'] = len(record.x_target_ids)

# Field  : x_incentive_branch_target.x_needs_recascade   (not stored)
# Depends: x_recascade_reason
for record in self:
    record['x_needs_recascade'] = bool(record.x_recascade_reason)

# Field  : x_incentive_period.x_payout_count   (not stored)
# Depends: x_payout_ids
for record in self:
    record['x_payout_count'] = len(record.x_payout_ids)

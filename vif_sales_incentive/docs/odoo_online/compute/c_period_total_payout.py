# Field  : x_incentive_period.x_total_payout   (not stored)
# Depends: x_payout_ids.x_total_payout
for record in self:
    record['x_total_payout'] = sum(record.x_payout_ids.mapped('x_total_payout'))

# Field  : x_incentive_rule_tier.x_payout_rate
# Depends: x_allocation, x_rule_id.x_base_rate
for record in self:
    record['x_payout_rate'] = record.x_allocation * record.x_rule_id.x_base_rate

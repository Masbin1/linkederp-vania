# Field  : x_incentive_branch_target.x_amount_total
# Depends: x_amount, x_carry_forward_amount
for record in self:
    record['x_amount_total'] = record.x_amount + record.x_carry_forward_amount

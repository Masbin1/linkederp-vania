# Field  : x_incentive_branch_target.x_payout_total   (not stored)
# Depends: x_period_id, x_branch_id, x_business_type
for record in self:
    payouts = self.env['x_incentive_payout'].search([
        ('x_period_id', '=', record.x_period_id.id),
        ('x_branch_id', '=', record.x_branch_id.id),
        ('x_business_type', '=', record.x_business_type),
    ])
    record['x_payout_total'] = sum(payouts.mapped('x_total_payout'))

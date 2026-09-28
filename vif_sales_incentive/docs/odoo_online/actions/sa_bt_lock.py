# Server Action : "VIF: Branch Target Lock"   Model: x_incentive_branch_target
# Button        : Lock (visible when state = approved)
Payout = env['x_incentive_payout']
Target = env['x_incentive_target']
for rec in records:
    if rec.x_state != 'approved':
        raise UserError('Only an approved branch target can be locked.')
    rec.write({'x_state': 'locked'})
    scope = [('x_period_id', '=', rec.x_period_id.id),
             ('x_branch_id', '=', rec.x_branch_id.id),
             ('x_business_type', '=', rec.x_business_type)]
    Payout.search(scope).write({'x_is_frozen': True})

    period = rec.x_period_id
    months = 0
    if period.x_rule_id.x_date_to:
        month = (period.x_date_end + dateutil.relativedelta.relativedelta(months=1)).replace(day=1)
        while month <= period.x_rule_id.x_date_to:
            months += 1
            month = month + dateutil.relativedelta.relativedelta(months=1)
    for target in Target.search(scope + [('x_target_type', '=', 'incentive')]):
        payout = Payout.search([
            ('x_period_id', '=', period.id),
            ('x_employee_id', '=', target.x_employee_id.id)], limit=1)
        shortfall = max(target.x_amount - (payout.x_net_sales if payout else 0.0), 0.0)
        target.write({
            'x_shortfall_amount': shortfall,
            'x_months_remaining': months,
            'x_carry_forward_amount': (shortfall / months) if months else 0.0,
        })

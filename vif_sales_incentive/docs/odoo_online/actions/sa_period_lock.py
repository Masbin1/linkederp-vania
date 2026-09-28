# Server Action : "VIF: Period Lock"      Model: x_incentive_period
# Button        : Lock (visible when state = approved)
#
# Freezes every payout and snapshots each incentive target's shortfall:
#   shortfall = target - net sales (if positive), spread evenly over the
#   rule's remaining months -> carry-forward added by the next cascade.
Payout = env['x_incentive_payout']
for rec in records:
    if rec.x_state != 'approved':
        raise UserError('Only an approved period can be locked.')
    rec.write({'x_state': 'locked'})
    rec.x_branch_target_ids.write({'x_state': 'locked'})
    rec.x_payout_ids.write({'x_is_frozen': True})

    months = 0
    if rec.x_rule_id.x_date_to:
        month = (rec.x_date_end + dateutil.relativedelta.relativedelta(months=1)).replace(day=1)
        while month <= rec.x_rule_id.x_date_to:
            months += 1
            month = month + dateutil.relativedelta.relativedelta(months=1)
    for target in rec.x_target_ids.filtered(lambda t: t.x_target_type == 'incentive'):
        payout = Payout.search([
            ('x_period_id', '=', rec.id),
            ('x_employee_id', '=', target.x_employee_id.id)], limit=1)
        shortfall = max(target.x_amount - (payout.x_net_sales if payout else 0.0), 0.0)
        target.write({
            'x_shortfall_amount': shortfall,
            'x_months_remaining': months,
            'x_carry_forward_amount': (shortfall / months) if months else 0.0,
        })

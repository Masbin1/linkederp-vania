# =====================================================================
# Server Action : "VIF: Cascade Apply"     Model: x_incentive_cascade
# Button        : Apply
#
# Writes the preview into x_incentive_target (incentive + bonus buckets),
# logs a movement for every bonus redistribution, and stamps each branch
# target's carry-forward (kept apart from the base so re-running the
# cascade never compounds it).
# =====================================================================
wiz = record
period = wiz.x_period_id
if period.x_state in ('approved', 'locked'):
    raise UserError('Period %s is closed.' % period.x_name)

if not wiz.x_line_ids:
    preview = env['ir.actions.server'].search(
        [('name', '=', 'VIF: Cascade Preview')], limit=1)
    if not preview:
        raise UserError('Server action "VIF: Cascade Preview" not found.')
    preview.with_context(active_model='x_incentive_cascade', active_id=wiz.id,
                         active_ids=[wiz.id]).run()

bts = wiz.x_line_ids.mapped('x_branch_target_id')
closed = bts.filtered(
    lambda b: b.x_state in ('approved', 'locked')
    or b.x_period_id.x_state in ('approved', 'locked'))
if closed:
    raise UserError('Branch target %s is closed -- reset it to draft to cascade '
                    'again.' % ', '.join(closed.mapped('x_name')))

Target = env['x_incentive_target']
Movement = env['x_incentive_target_movement']
for line in wiz.x_line_ids:
    for spec in (('incentive', line.x_incentive_amount, 'rf_cascade'),
                 ('bonus', line.x_bonus_amount, 'redistribution')):
        ttype = spec[0]
        amount = spec[1]
        if not amount:
            continue
        vals = {
            'x_amount': amount,
            'x_source': spec[2],
            'x_fte_used': line.x_fte,
            'x_proration_ratio': line.x_proration,
        }
        existing = Target.search([
            ('x_period_id', '=', period.id),
            ('x_employee_id', '=', line.x_employee_id.id),
            ('x_target_type', '=', ttype)], limit=1)
        if existing:
            if wiz.x_overwrite_existing:
                existing.write(vals)
        else:
            vals.update({
                'x_period_id': period.id,
                'x_employee_id': line.x_employee_id.id,
                'x_target_type': ttype,
            })
            Target.create(vals)
        if ttype == 'bonus':
            Movement.create({
                'x_period_id': period.id,
                'x_reason': 'resignation',
                'x_to_employee_id': line.x_employee_id.id,
                'x_amount': amount,
                'x_target_type': 'bonus',
                'x_fte_share': line.x_fte,
                'x_date_effective': period.x_date_start,
                'x_note': 'Vacancy redistribution from FTE cascade.',
            })

for bt in bts:
    bt.write({'x_carry_forward_amount': sum(wiz.x_line_ids.filtered(
        lambda l: l.x_branch_target_id == bt).mapped('x_carry_forward_amount'))})

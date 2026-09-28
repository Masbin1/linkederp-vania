# =====================================================================
# Server Action : "VIF: Cascade Preview"     (name must match exactly --
#                 Cascade Apply looks it up by name)
# Model         : Cascade Branch Target (x_incentive_cascade)
# Button        : Preview
#
# Port of incentive.target.cascade.action_preview. For every selected branch:
#   individual target = branch target x (own FTE / total FTE) x proration
#                       + own carry-forward
#   vacant seats / uncovered days / ideal-size gap -> bonus pool, spread by
#   FTE over the people who worked the full month (their BONUS bucket).
# =====================================================================
Employee = env['hr.employee']
BranchTarget = env['x_incentive_branch_target']
Target = env['x_incentive_target']
Line = env['x_incentive_cascade_line']

wiz = record
period = wiz.x_period_id
if not wiz.x_branch_ids:
    raise UserError('Select at least one branch.')


def proration(emp):
    start = max(emp.x_incentive_date_start or period.x_date_start, period.x_date_start)
    end = min(emp.x_incentive_date_end or period.x_date_end, period.x_date_end)
    if end < start:
        return 0.0
    total = (period.x_date_end - period.x_date_start).days + 1
    return ((end - start).days + 1) / total


def carry_forward(emp):
    """This employee's own carry-forward from prior LOCKED months of the rule."""
    if not period.x_rule_id:
        return 0.0
    locked_periods = BranchTarget.search([
        ('x_branch_id', '=', emp.x_incentive_branch_id.id),
        ('x_business_type', '=', emp.x_incentive_business_type),
        ('x_state', '=', 'locked'),
        ('x_period_id.x_date_end', '<', period.x_date_start),
        ('x_period_id.x_rule_id', '=', period.x_rule_id.id),
    ]).mapped('x_period_id')
    if not locked_periods:
        return 0.0
    prior = Target.search([
        ('x_employee_id', '=', emp.id),
        ('x_target_type', '=', 'incentive'),
        ('x_period_id', 'in', locked_periods.ids),
        ('x_carry_forward_amount', '>', 0.0)])
    return sum(prior.mapped('x_carry_forward_amount'))


# Branch target rows: one per selected branch, else error.
bts = BranchTarget
missing = []
for branch in wiz.x_branch_ids:
    bt = BranchTarget.search([
        ('x_period_id', '=', period.id),
        ('x_branch_id', '=', branch.id),
        ('x_business_type', '=', wiz.x_business_type)], limit=1)
    if bt:
        bts |= bt
    else:
        missing.append(branch.x_name)
if missing:
    raise UserError('No Branch Target for %s in %s. Enter the rolling forecast '
                    'under Branch Targets first.' % (', '.join(missing), period.x_name))

wiz.x_line_ids.unlink()
carry_total = 0.0

for bt in bts:
    branch = bt.x_branch_id
    # -- population ---------------------------------------------------
    active = []
    vacant = []
    for emp in Employee.search([
            ('x_incentive_branch_id', '=', branch.id),
            ('x_incentive_business_type', '=', wiz.x_business_type)]):
        if emp.x_incentive_date_end and emp.x_incentive_date_end < period.x_date_start:
            continue
        if emp.x_incentive_date_start and emp.x_incentive_date_start > period.x_date_end:
            continue
        desig = emp.x_incentive_designation_id
        if not desig:
            continue
        fte = desig.x_fte_individual if wiz.x_scope == 'individual' else desig.x_fte_branch
        if not fte:
            continue
        if emp.x_is_vacant_slot or not proration(emp):
            vacant.append((emp, fte))
        else:
            active.append((emp, fte))
    if not active:
        raise UserError('No eligible salesperson found for %s / %s.'
                        % (branch.x_name, (wiz.x_business_type or '').upper()))

    # -- seats: a resignation chained to the same-designation hire that
    #    fills it counts ONCE in the FTE denominator -------------------
    by_id = {}
    for a in active:
        by_id[a[0].id] = a
    leavers = sorted([a for a in active if a[0].x_incentive_date_end],
                     key=lambda a: a[0].x_incentive_date_end)
    joiners = sorted([a for a in active if a[0].x_incentive_date_start],
                     key=lambda a: a[0].x_incentive_date_start)
    succ = {}
    claimed = set()
    for lv in leavers:
        leaver = lv[0]
        for jn in joiners:
            joiner = jn[0]
            if (joiner.id in claimed or joiner.id == leaver.id
                    or joiner.x_incentive_date_start <= leaver.x_incentive_date_end
                    or joiner.x_incentive_designation_id != leaver.x_incentive_designation_id):
                continue
            succ[leaver.id] = joiner.id
            claimed.add(joiner.id)
            break
    seats = []
    for a in active:
        if a[0].id in claimed:
            continue
        chain = [a]
        cur = a[0].id
        while cur in succ:
            cur = succ[cur]
            chain.append(by_id[cur])
        seats.append(chain)

    # -- ideal team size gap (empty chair weighs 1.0) ------------------
    ideal = (branch.x_ideal_team_size_b2b if wiz.x_business_type == 'b2b'
             else branch.x_ideal_team_size_b2c)
    gap_fte = 0.0
    if ideal:
        seated = 0
        for emp in Employee.search([
                ('x_incentive_branch_id', '=', branch.id),
                ('x_incentive_business_type', '=', wiz.x_business_type)]):
            if emp.x_incentive_date_start and emp.x_incentive_date_start > period.x_date_start:
                continue
            if emp.x_incentive_date_end and emp.x_incentive_date_end < period.x_date_start:
                continue
            seated += 1
        gap_fte = float(max(0, ideal - seated))

    total_fte_all = (sum([s[0][1] for s in seats]) + sum([v[1] for v in vacant]) + gap_fte)
    if not total_fte_all:
        raise UserError('Total effective FTE is zero for %s.' % branch.x_name)

    base_target = bt.x_amount
    vacant_pool = 0.0
    rows = []
    for seat in seats:
        seat_base = base_target * (seat[0][1] / total_fte_all)
        coverage = 0.0
        for a in seat:
            emp = a[0]
            p = proration(emp)
            coverage += p
            cf = carry_forward(emp)
            carry_total += cf
            rows.append((emp, a[1], p, seat_base * p, cf))
        if wiz.x_redistribute_vacant:
            vacant_pool += seat_base * max(0.0, 1.0 - coverage)
    if wiz.x_redistribute_vacant:
        vacant_pool += sum([base_target * (v[1] / total_fte_all) for v in vacant])
        vacant_pool += base_target * (gap_fte / total_fte_all)

    # Pool goes to full-month people; if nobody worked the whole month,
    # to everyone weighted by proration.
    receivers = [(r[0], r[1]) for r in rows if r[2] >= 1.0]
    if not receivers:
        receivers = [(r[0], r[1] * r[2]) for r in rows]
    total_recv = sum([r[1] for r in receivers])
    share_by_emp = {}
    if total_recv:
        for r in receivers:
            share_by_emp[r[0].id] = r[1] / total_recv

    for r in rows:
        Line.create({
            'x_cascade_id': wiz.id,
            'x_branch_target_id': bt.id,
            'x_employee_id': r[0].id,
            'x_fte': r[1],
            'x_proration': r[2],
            'x_base_amount': r[3],
            'x_carry_forward_amount': r[4],
            'x_incentive_amount': r[3] + r[4],
            'x_bonus_amount': vacant_pool * share_by_emp.get(r[0].id, 0.0),
        })

wiz.write({'x_carry_forward_total': carry_total})

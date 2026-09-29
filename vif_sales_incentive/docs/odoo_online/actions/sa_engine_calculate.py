# =====================================================================
# VIF Sales Incentive -- ENGINE: Calculate
# ---------------------------------------------------------------------
# Server Action  : "VIF: Engine Calculate"      (name must match exactly --
#                  the Branch Target button looks it up by name)
# Model          : Incentive Period (x_incentive_period)
# Action To Do   : Execute Code
# Called by      : button Calculate on Incentive Period   -> whole period
#                  button Calculate on Branch Target      -> that branch only
#                  (context key vif_branch_target_id)
#                  button Recompute on Incentive Payout   -> that payout only
#                  (context key vif_recompute_payout_id)
#
# Port of: incentive.transaction._generate_for_period / _generate_pos_for_period,
#          incentive.period._check_credited_employees,
#          incentive.payout._compute_for_period / _run / _compute_branch_for_period
#
# SAFE_EVAL NOTE: Odoo refuses closures. Inside a `def`, never use a lambda /
# comprehension that reads a variable of that def. Top-level code is free to.
# =====================================================================

Period = env['x_incentive_period']
BranchTarget = env['x_incentive_branch_target']
Target = env['x_incentive_target']
Tx = env['x_incentive_transaction']
Payout = env['x_incentive_payout']
Tier = env['x_incentive_rule_tier']
Employee = env['hr.employee']

period = record
if not period:
    raise UserError('Run this action from an Incentive Period.')
only_bt = BranchTarget.browse(env.context.get('vif_branch_target_id') or [])
# Recompute button on one payout (context vif_recompute_payout_id): re-runs
# that employee's individual stream only -- no transaction refresh, no
# branch stream, no state change. Same as incentive.payout.action_recompute.
only_payout = Payout.browse(env.context.get('vif_recompute_payout_id') or [])

# Project split: (role, user field on project, commission share field).
# The Salesperson 2/3 and share fields are the client's Studio fields.
PROJECT_SLOTS = [
    ('pm', 'user_id', 'x_studio_komisi_pm'),
    ('sp2', 'x_studio_salesperson_2', 'x_studio_komisi_salesperson_2'),
    ('sp3', 'x_studio_salesperson_3', 'x_studio_komisi_salesperson_3'),
]
MAXDATE = datetime.date.max
ONE_DAY = datetime.timedelta(days=1)


# ---------------------------------------------------------------------
# Helpers (no closures -- see note above)
# ---------------------------------------------------------------------
def is_closed(bt):
    return (bt.x_state in ('approved', 'locked')
            or bt.x_period_id.x_state in ('approved', 'locked'))


period_cache = {}


def period_for_date(d):
    if not d:
        return Period
    if d not in period_cache:
        period_cache[d] = Period.search([
            ('x_date_start', '<=', d), ('x_date_end', '>=', d),
            ('x_company_id', '=', company.id)], limit=1)
    return period_cache[d]


emp_by_user = {}


def employee_of(user):
    if not user:
        return Employee
    if user.id not in emp_by_user:
        emp_by_user[user.id] = Employee.search([('user_id', '=', user.id)], limit=1)
    return emp_by_user[user.id]


target_emps = {}


def has_target(emp, p):
    if not p:
        return True
    if p.id not in target_emps:
        target_emps[p.id] = set(
            Target.search([('x_period_id', '=', p.id)]).mapped('x_employee_id').ids)
    return emp.id in target_emps[p.id]


def in_scheme(emp, p):
    """SP2 / SP3 only keep their share when they can earn from it."""
    if not (emp.x_incentive_branch_id and emp.x_incentive_business_type):
        return False
    return has_target(emp, p)


def project_split(project, p):
    """[(employee, share, role)] for a project, shares summing to 1.
    Empty list -> nobody on the project is an employee (fall back to the
    invoice salesperson)."""
    pm = employee_of(project.user_id)
    shares = {}
    order = []
    orphan = 0.0
    for slot in PROJECT_SLOTS:
        role = slot[0]
        user_field = slot[1]
        share_field = slot[2]
        share = project[share_field] if share_field in project._fields else 0.0
        if not share or share <= 0:
            continue
        user = project[user_field] if user_field in project._fields else False
        emp = employee_of(user)
        # No employee, or an SP2/SP3 outside the scheme -> the share goes to PM
        if not emp or (emp != pm and not in_scheme(emp, p)):
            orphan += share
            continue
        if emp.id not in shares:
            shares[emp.id] = [emp, 0.0, role]
            order.append(emp.id)
        shares[emp.id][1] += share
    if not shares and not orphan:
        if pm:
            return [(pm, 1.0, 'pm')]
        return []
    assigned = 0.0
    for k in order:
        assigned += shares[k][1]
    orphan += max(1.0 - assigned - orphan, 0.0)
    if orphan and pm:
        if pm.id not in shares:
            shares[pm.id] = [pm, 0.0, 'pm']
            order.append(pm.id)
        shares[pm.id][1] += orphan
    total = 0.0
    for k in order:
        total += shares[k][1]
    if total <= 0:
        return []
    res = []
    for k in order:
        res.append((shares[k][0], shares[k][1] / total, shares[k][2]))
    return res


def move_project(move):
    project = move.invoice_line_ids.sale_line_ids.order_id.project_id[:1]
    if not project and move.reversed_entry_id:
        project = move.reversed_entry_id.invoice_line_ids.sale_line_ids.order_id.project_id[:1]
    return project


split_cache = {}


def line_split(line):
    """[(employee, share, role, project)] for one invoice line."""
    move = line.move_id
    project = line.sale_line_ids.order_id.project_id[:1] or move_project(move)
    if project:
        # Eligibility is judged in the period of the invoice -- for a credit
        # note, of the invoice it reverses, so the refund splits like the sale.
        src = move
        if move.move_type == 'out_refund' and move.reversed_entry_id:
            src = move.reversed_entry_id
        p = period_for_date(src.invoice_date)
        key = (project.id, p.id)
        if key not in split_cache:
            split_cache[key] = project_split(project, p)
        split = split_cache[key]
        if split:
            res = []
            for item in split:
                res.append((item[0], item[1], item[2], project))
            return res
    emp = move.x_incentive_employee_id
    if move.move_type == 'out_refund' and move.reversed_entry_id:
        emp = move.reversed_entry_id.x_incentive_employee_id or emp
    if emp:
        return [(emp, 1.0, 'salesperson', project)]
    return []


def full_paid_date(move):
    """Date the invoice became FULLY paid (last reconciliation), else False."""
    if move.move_type not in ('out_invoice', 'out_refund'):
        return False
    if move.payment_state not in ('paid', 'in_payment'):
        return False
    dates = []
    for ml in move.line_ids:
        if ml.account_id.account_type != 'asset_receivable':
            continue
        for part in ml.matched_credit_ids:
            dates.append(part.max_date)
        for part in ml.matched_debit_ids:
            dates.append(part.max_date)
    return max(dates) if dates else move.invoice_date


def get_tier(rule, ach, is_mixed):
    """Tier for an achievement fraction. min <= ach < max; top tier open."""
    tiers = rule.x_tier_ids.sorted('x_achievement_min')
    matched = Tier
    for tier in tiers:
        if ach >= tier.x_achievement_min and (
                tier.x_is_top_tier or ach < tier.x_achievement_max):
            matched = tier
    if not matched and tiers:
        matched = tiers[0]
    if (matched and is_mixed and rule.x_cap_tier_in_mixed
            and matched.x_level > rule.x_mixed_cap_tier_level):
        for tier in tiers:
            if tier.x_level == rule.x_mixed_cap_tier_level:
                matched = tier
                break
    return matched


def tier_rate(tier):
    if not tier:
        return 0.0
    return tier.x_allocation * tier.x_rule_id.x_base_rate


def net_alloc(t):
    """(incentive, bonus) portions of the base, net of linked refunds."""
    refunded = 0.0
    for r in t.x_reversal_ids:
        if r.x_state != 'reversed':
            refunded += r.x_base_amount
    base = max(t.x_base_amount + refunded, 0.0)
    if base <= 0 or not t.x_base_amount:
        return (0.0, 0.0)
    return (base * t.x_incentive_alloc / t.x_base_amount,
            base * t.x_bonus_alloc / t.x_base_amount)


def target_amount(emp, ttype):
    row = Target.search([
        ('x_employee_id', '=', emp.id), ('x_period_id', '=', period.id),
        ('x_target_type', '=', ttype)], limit=1)
    return row.x_amount if row else 0.0


def is_active_on(emp, d):
    if emp.x_is_vacant_slot:
        return False
    if emp.x_incentive_date_start and d < emp.x_incentive_date_start:
        return False
    if emp.x_incentive_date_end and d > emp.x_incentive_date_end:
        return False
    return True


def bt_for_employee(emp):
    if not (emp.x_incentive_branch_id and emp.x_incentive_business_type):
        return BranchTarget
    return BranchTarget.search([
        ('x_period_id', '=', period.id),
        ('x_branch_id', '=', emp.x_incentive_branch_id.id),
        ('x_business_type', '=', emp.x_incentive_business_type)], limit=1)


def get_payout(emp):
    row = Payout.search([
        ('x_period_id', '=', period.id), ('x_employee_id', '=', emp.id)], limit=1)
    if not row:
        row = Payout.create({
            'x_period_id': period.id, 'x_employee_id': emp.id,
            'x_name': '%s - %s' % (emp.name, period.x_name)})
    return row


# ---------------------------------------------------------------------
# 0. Guards
# ---------------------------------------------------------------------
if period.x_state == 'locked':
    raise UserError('Period %s is locked. Approved payout figures must never '
                    'change. Create an adjustment in a later period instead.'
                    % period.x_name)
if period.x_state == 'draft':
    raise UserError('Open period %s before calculating.' % period.x_name)
rule = period.x_rule_id
if not rule:
    raise UserError('Period %s has no Rule Version.' % period.x_name)
company = period.x_company_id or env.company
max_discount = rule.x_max_discount

if only_payout:
    # Recompute button (module: incentive.payout.action_recompute)
    if only_payout.x_is_frozen:
        raise UserError('Payout for %s in %s is frozen -- the accounting period is '
                        'closed.' % (only_payout.x_employee_id.name, period.x_name))
    rbt = bt_for_employee(only_payout.x_employee_id)
    if rbt and is_closed(rbt):
        raise UserError('Branch target %s is %s -- reset it to draft before '
                        'recomputing.' % (rbt.x_name, rbt.x_state))
    check_bts = BranchTarget
elif only_bt:
    if only_bt.x_state == 'locked' or period.x_state in ('approved', 'locked'):
        raise UserError('Branch target %s is locked.' % only_bt.x_name)
    if only_bt.x_state == 'approved':
        raise UserError('Branch target %s is approved. Reset it to draft to '
                        'recalculate.' % only_bt.x_name)
    check_bts = only_bt
else:
    check_bts = period.x_branch_target_ids.filtered(lambda b: not is_closed(b))

stale_bts = check_bts.filtered(lambda b: b.x_needs_recascade)
if stale_bts:
    raise UserError(
        'These teams changed since their targets were cascaded:\n\n%s\n\n'
        'Calculating now would pay against a team that no longer exists. '
        'Re-run the target cascade first.' % '\n'.join(
            ['- %s: %s' % (b.x_name, b.x_recascade_reason or '') for b in stale_bts]))

# ---------------------------------------------------------------------
# 1. Invoice transactions (one row per invoice line x credited employee)
# ---------------------------------------------------------------------
if not only_payout:
    lines = env['account.move.line'].search([
        ('move_id.state', '=', 'posted'),
        ('move_id.move_type', 'in', ('out_invoice', 'out_refund')),
        ('move_id.invoice_date', '>=', period.x_date_start),
        ('move_id.invoice_date', '<=', period.x_date_end),
        ('display_type', '=', 'product'),
        ('company_id', '=', company.id),
    ])
    existing = {}
    for t in Tx.search([('x_move_line_id', 'in', lines.ids)]):
        existing[(t.x_move_line_id.id, t.x_employee_id.id)] = t

    kept_ids = []
    for line in lines:
        move = line.move_id
        is_refund = move.move_type == 'out_refund'
        sign = -1 if is_refund else 1
        for item in line_split(line):
            emp = item[0]
            share = item[1]
            vals = {
                'x_name': '%s / %s' % (move.name or '-', line.product_id.display_name or '-'),
                'x_source_type': 'invoice',
                'x_move_line_id': line.id,
                'x_move_id': move.id,
                'x_employee_id': emp.id,
                'x_company_id': company.id,
                'x_partner_id': move.partner_id.id,
                'x_product_id': line.product_id.id,
                'x_invoice_date': move.invoice_date,
                'x_source_period_id': period.id,
                'x_transaction_type': 'refund' if is_refund else 'invoice',
                # Credit note lines are stored positive -> negate. The DP negation
                # line on a final invoice is already negative and stays so.
                'x_base_amount': line.currency_id.round(sign * line.price_subtotal * share),
                'x_split_share': share,
                'x_split_role': item[2],
                'x_project_id': item[3].id or False,
                'x_discount': line.discount,
                'x_is_downpayment': line.is_downpayment,
                'x_is_discount_eligible': line.discount <= max_discount,
                'x_eligibility_note': (
                    'Line discount %.2f%% exceeds the %.2f%% cap.' % (line.discount, max_discount)
                    if line.discount > max_discount else False),
                'x_state': 'confirmed',
            }
            ex = existing.get((line.id, emp.id))
            if ex:
                if ex.x_state == 'paid_out':
                    continue
                ex.write(vals)
                kept_ids.append(ex.id)
            else:
                kept_ids.append(Tx.create(vals).id)

    # People no longer credited on these lines (project changed, old 100% row).
    Tx.search([
        ('x_source_type', '=', 'invoice'),
        ('x_move_line_id', 'in', lines.ids),
        ('x_state', 'not in', ('paid_out', 'reversed')),
        ('id', 'not in', kept_ids),
    ]).unlink()

    # Payment stamps: this period's rows + every older row still waiting.
    pending = Tx.search([
        ('x_source_type', '=', 'invoice'),
        ('x_company_id', '=', company.id),
        ('x_source_period_id.x_date_start', '<=', period.x_date_start),
        ('x_state', '!=', 'paid_out'),
    ])
    paid_cache = {}
    for t in pending:
        move = t.x_move_id
        if not move:
            continue
        if move.id not in paid_cache:
            paid_cache[move.id] = full_paid_date(move)
        paid_on = paid_cache[move.id]
        if not paid_on:
            t.write({'x_is_payment_eligible': False, 'x_payment_date': False,
                     'x_payment_period_id': False, 'x_is_prior_period': False})
            continue
        pay_period = period_for_date(paid_on)
        t.write({
            'x_is_payment_eligible': True,
            'x_payment_date': paid_on,
            'x_payment_period_id': pay_period.id or False,
            'x_payout_period_id': pay_period.id or False,
            'x_is_prior_period': bool(
                pay_period and t.x_source_period_id
                and pay_period.x_date_start > t.x_source_period_id.x_date_start),
        })

    # Link credit-note rows to the invoice row they reverse (partial refund net-off).
    for refund in Tx.search([
            ('x_source_type', '=', 'invoice'),
            ('x_transaction_type', '=', 'refund'),
            ('x_source_period_id', '=', period.id),
            ('x_reversal_of_id', '=', False)]):
        src = refund.x_move_id.reversed_entry_id
        if not src:
            continue
        inv = Tx.search([
            ('x_move_id', '=', src.id),
            ('x_employee_id', '=', refund.x_employee_id.id),
            ('x_transaction_type', '=', 'invoice'),
            ('x_is_downpayment', '=', False)], limit=1)
        if inv:
            refund.write({'x_reversal_of_id': inv.id})

    # ---------------------------------------------------------------------
    # 2. POS transactions (non-invoiced orders; paid at the till)
    # ---------------------------------------------------------------------
    orders = env['pos.order'].search([
        ('state', 'in', ('paid', 'done', 'invoiced')),
        ('date_order', '>=', period.x_date_start),
        ('date_order', '<', period.x_date_end + ONE_DAY),
        ('account_move', '=', False),
        ('company_id', '=', company.id),
    ])
    pos_existing = {}
    for t in Tx.search([('x_pos_order_id', 'in', orders.ids)]):
        pos_existing[(t.x_pos_order_line_id.id, t.x_employee_id.id)] = t
    pos_kept = []
    for order in orders:
        emp = order.employee_id
        if not emp or not emp.x_incentive_branch_id:
            continue
        order_date = order.date_order.date() if order.date_order else period.x_date_start
        for pl in order.lines:
            if not pl.product_id:
                continue
            # A return line has a negative qty but its subtotal is not reliably
            # negative (Odoo 19 stores +740,000 for qty -5): sign from the qty.
            is_return = pl.qty < 0
            vals = {
                'x_name': '%s / %s' % (order.pos_reference or order.name,
                                       pl.product_id.display_name),
                'x_source_type': 'pos',
                'x_pos_order_line_id': pl.id,
                'x_pos_order_id': order.id,
                'x_employee_id': emp.id,
                'x_company_id': company.id,
                'x_partner_id': order.partner_id.id,
                'x_product_id': pl.product_id.id,
                'x_invoice_date': order_date,
                'x_source_period_id': period.id,
                'x_transaction_type': 'refund' if is_return else 'invoice',
                'x_base_amount': -abs(pl.price_subtotal) if is_return else pl.price_subtotal,
                'x_split_share': 1.0,
                'x_split_role': 'salesperson',
                'x_discount': pl.discount,
                'x_is_downpayment': False,
                'x_is_discount_eligible': pl.discount <= max_discount,
                'x_eligibility_note': (
                    'Line discount %.2f%% exceeds the %.2f%% cap.' % (pl.discount, max_discount)
                    if pl.discount > max_discount else False),
                'x_is_payment_eligible': True,
                'x_payment_date': order_date,
                'x_payment_period_id': period.id,
                'x_payout_period_id': period.id,
                'x_is_prior_period': False,
                'x_state': 'confirmed',
            }
            ex = pos_existing.get((pl.id, emp.id))
            if ex:
                if ex.x_state == 'paid_out':
                    continue
                ex.write(vals)
                pos_kept.append(ex.id)
            else:
                pos_kept.append(Tx.create(vals).id)

    # Rows this run no longer produces (cashier changed, order invoiced since).
    Tx.search([
        ('x_source_type', '=', 'pos'),
        ('x_source_period_id', '=', period.id),
        ('x_state', '!=', 'paid_out'),
        ('id', 'not in', pos_kept),
    ]).unlink()

    # Link each POS return to the sale it takes back -> that sale pays out only
    # on what the customer kept. Done after the loop: orders come newest first,
    # so a return is usually generated before its sale.
    for refund in Tx.browse(pos_kept).filtered(
            lambda t: t.x_transaction_type == 'refund'
            and t.x_pos_order_line_id.refunded_orderline_id):
        originals = Tx.search([
            ('x_pos_order_line_id', '=', refund.x_pos_order_line_id.refunded_orderline_id.id),
            ('x_transaction_type', '=', 'invoice')])
        same_emp = originals.filtered(lambda t: t.x_employee_id == refund.x_employee_id)
        refund.write({'x_reversal_of_id': (same_emp or originals)[:1].id or False})

    # ---------------------------------------------------------------------
    # 3. Refuse when credited people would silently earn nothing
    # ---------------------------------------------------------------------
    chk_domain = [('x_source_period_id', '=', period.id), ('x_state', '!=', 'reversed')]
    if only_bt:
        chk_domain += ['|', '&',
                       ('x_branch_id', '=', only_bt.x_branch_id.id),
                       ('x_business_type', '=', only_bt.x_business_type),
                       ('x_branch_id', '=', False)]
    credited = Tx.search(chk_domain).mapped('x_employee_id')
    if not only_bt:
        # Only the teams with a Branch Target this period are calculated, so only
        # they (and the branchless) are reported.
        scopes = set()
        for bt in period.x_branch_target_ids:
            scopes.add((bt.x_branch_id.id, bt.x_business_type))
        credited = credited.filtered(
            lambda e: not (e.x_incentive_branch_id and e.x_incentive_business_type)
            or (e.x_incentive_branch_id.id, e.x_incentive_business_type) in scopes)
    # Nobody earns in a month they did not work: sales credited to someone who
    # joins after (or left before) this period are simply not paid -- no error.
    credited = credited.filtered(
        lambda e: not (e.x_incentive_date_start and e.x_incentive_date_start > period.x_date_end)
        and not (e.x_incentive_date_end and e.x_incentive_date_end < period.x_date_start))
    with_target = Target.search([
        ('x_period_id', '=', period.id),
        ('x_employee_id', 'in', credited.ids)]).mapped('x_employee_id')
    no_branch = credited.filtered(
        lambda e: not (e.x_incentive_branch_id and e.x_incentive_business_type))
    no_target = credited - with_target - no_branch
    if no_branch or no_target:
        msg = []
        if no_branch:
            msg.append('- No Sales Branch / Business Type: %s'
                       % ', '.join(no_branch.mapped('name')))
        if no_target:
            msg.append('- No target in %s: %s'
                       % (period.x_name, ', '.join(no_target.mapped('name'))))
        raise UserError(
            'These people have sales in %s but would get no payout:\n\n%s\n\n'
            'Fill in their employee incentive settings and run the target '
            'cascade, then calculate again.' % (period.x_name, '\n'.join(msg)))

# ---------------------------------------------------------------------
# 4. Individual payout (SQ1 tier -> SQ2 eligible -> SQ3 paid)
# ---------------------------------------------------------------------
tgt_domain = [('x_period_id', '=', period.id)]
if only_bt:
    tgt_domain += [('x_branch_id', '=', only_bt.x_branch_id.id),
                   ('x_business_type', '=', only_bt.x_business_type)]
touched = Payout
if only_payout:
    run_emps = only_payout.x_employee_id
else:
    run_emps = Target.search(tgt_domain).mapped('x_employee_id')
for emp in run_emps:
    bt = only_bt or bt_for_employee(emp)
    # A team is in the period only through its Branch Target: a B2C target
    # left in a B2B-only month is not paid.
    if not bt and not only_payout:
        continue
    if bt and is_closed(bt) and not only_bt:
        continue
    payout = get_payout(emp)
    touched |= payout
    if payout.x_is_frozen:
        continue

    t_inc = target_amount(emp, 'incentive')
    t_bon = target_amount(emp, 'bonus')
    is_mixed = bool(t_bon)
    log_lines = ['Target incentive=%s bonus=%s mixed=%s' % (t_inc, t_bon, is_mixed)]

    # SQ1 -- tier from ALL invoices of the month (unpaid, DP, >cap included)
    source_tx = Tx.search([
        ('x_employee_id', '=', emp.id),
        ('x_source_period_id', '=', period.id),
        ('x_state', '!=', 'reversed')])
    gross = sum(source_tx.filtered(
        lambda t: t.x_transaction_type == 'invoice').mapped('x_base_amount'))
    returns = abs(sum(Tx.search([
        ('x_employee_id', '=', emp.id),
        ('x_transaction_type', '=', 'refund'),
        ('x_source_period_id', '=', period.id)]).mapped('x_base_amount')))
    net = gross - returns
    achievement = (net / t_inc) if t_inc else 0.0
    tier = get_tier(rule, achievement, is_mixed)
    rate = tier_rate(tier)
    log_lines.append('SQ1 net=%s / target=%s => %.4f => %s (rate %.6f)' % (
        net, t_inc, achievement, tier.x_name if tier else 'none', rate))
    # Freeze the source tier onto this month's rows: a prior-period invoice
    # paid later is paid at THIS rate, never the later month's.
    source_tx.filtered(lambda t: t.x_state != 'paid_out').write({
        'x_tier_id': tier.id or False, 'x_tier_payout_rate': rate})

    # SQ2 -- discount-eligible, non-DP invoice lines; incentive bucket first
    eligible_tx = source_tx.filtered(
        lambda t: t.x_is_discount_eligible and t.x_transaction_type == 'invoice'
        and not t.x_is_downpayment)
    excluded = sum(source_tx.filtered(
        lambda t: not t.x_is_discount_eligible and t.x_transaction_type == 'invoice'
        and not t.x_is_downpayment).mapped('x_base_amount'))
    eligible_base = sum(eligible_tx.mapped('x_base_amount'))
    if is_mixed:
        elig_inc = min(eligible_base, t_inc)
        elig_bon = max(eligible_base - t_inc, 0.0)
    else:
        elig_inc = eligible_base
        elig_bon = 0.0
    log_lines.append('SQ2 eligible=%s excluded=%s -> incentive=%s bonus=%s' % (
        eligible_base, excluded, elig_inc, elig_bon))

    remaining_inc = elig_inc
    remaining_bon = elig_bon
    # Chronological; ties broken by the invoice / POS line (stable even when
    # a row is recreated), never by amount.
    for t in eligible_tx.sorted(
            key=lambda t: (t.x_invoice_date or t.x_payment_date or MAXDATE,
                           t.x_move_line_id.id or t.x_pos_order_line_id.id or 0, t.id)):
        inc = min(t.x_base_amount, remaining_inc)
        remaining_inc -= inc
        bon = min(t.x_base_amount - inc, remaining_bon)
        remaining_bon -= bon
        if inc >= bon and inc > 0:
            bucket = 'incentive'
        elif bon > 0:
            bucket = 'bonus'
        else:
            bucket = 'excluded'
        t.write({'x_incentive_alloc': inc, 'x_bonus_alloc': bon, 'x_bucket': bucket})
    (source_tx - eligible_tx).write({
        'x_incentive_alloc': 0.0, 'x_bonus_alloc': 0.0, 'x_bucket': 'excluded'})

    # SQ3 -- only what is FULLY PAID
    paid_current_tx = eligible_tx.filtered(
        lambda t: t.x_is_payment_eligible and t.x_payment_period_id == period)
    paid_current = 0.0
    paid_bonus = 0.0
    for t in paid_current_tx:
        a = net_alloc(t)
        paid_current += a[0]
        paid_bonus += a[1]
    prior_tx = Tx.search([
        ('x_employee_id', '=', emp.id),
        ('x_payment_period_id', '=', period.id),
        ('x_source_period_id', '!=', period.id),
        ('x_is_discount_eligible', '=', True),
        ('x_is_payment_eligible', '=', True),
        ('x_transaction_type', '=', 'invoice'),
        ('x_is_downpayment', '=', False),
        ('x_state', '!=', 'reversed'),
        ('x_incentive_alloc', '>', 0.0)])
    paid_prior = 0.0
    payout_prior = 0.0
    for t in prior_tx:
        a = net_alloc(t)
        paid_prior += a[0]
        payout_prior += a[0] * t.x_tier_payout_rate   # its OWN frozen rate
    payout_current = paid_current * rate
    payout_bonus = paid_bonus * rule.x_bonus_rate
    log_lines.append('SQ3 paid_current=%s x %.6f = %s' % (paid_current, rate, payout_current))
    log_lines.append('SQ3 paid_prior=%s (own frozen rates) = %s' % (paid_prior, payout_prior))
    log_lines.append('Bonus %s x %.6f = %s' % (paid_bonus, rule.x_bonus_rate, payout_bonus))

    for t in (paid_current_tx | prior_tx):
        if not t.x_is_discount_eligible or not t.x_is_payment_eligible or t.x_is_downpayment:
            t.write({'x_payout_amount': 0.0})
        else:
            a = net_alloc(t)
            t.write({'x_payout_amount': a[0] * t.x_tier_payout_rate + a[1] * rule.x_bonus_rate})

    payout.write({
        'x_target_incentive': t_inc,
        'x_target_bonus': t_bon,
        'x_gross_sales': gross,
        'x_sales_return': returns,
        'x_net_sales': net,
        'x_achievement_pct': achievement,
        'x_tier_id': tier.id or False,
        'x_tier_level': tier.x_level if tier else 0,
        'x_payout_rate': rate,
        'x_eligible_incentive': elig_inc,
        'x_eligible_bonus': elig_bon,
        'x_excluded_discount': excluded,
        'x_paid_current_month': paid_current,
        'x_paid_prior_month': paid_prior,
        'x_paid_bonus': paid_bonus,
        'x_payout_current': payout_current,
        'x_payout_prior': payout_prior,
        'x_payout_bonus': payout_bonus,
        'x_computation_log': '\n'.join(log_lines),
    })

# ---------------------------------------------------------------------
# 5. Branch payout: pool = team's payout_current, split by branch FTE,
#    x branch tier rate. Global members (e.g. Pak Kenny) join every branch.
if not only_payout:
    # ---------------------------------------------------------------------
    global_members = Employee.search([
        ('x_is_global_branch_member', '=', True),
        ('x_incentive_designation_id', '!=', False)])
    global_accum = {}
    for bt in (only_bt or period.x_branch_target_ids):
        if is_closed(bt) and not only_bt:
            continue
        branch = bt.x_branch_id
        team = Employee.search([
            ('x_incentive_branch_id', '=', branch.id),
            ('x_incentive_business_type', '=', bt.x_business_type)]).filtered(
            lambda e: e.x_branch_incentive_eligible and is_active_on(e, period.x_date_start))
        btx = Tx.search([
            ('x_branch_id', '=', branch.id),
            ('x_business_type', '=', bt.x_business_type),
            ('x_source_period_id', '=', period.id),
            ('x_state', '!=', 'reversed')])
        b_gross = sum(btx.filtered(
            lambda t: t.x_transaction_type == 'invoice').mapped('x_base_amount'))
        b_returns = abs(sum(btx.filtered(
            lambda t: t.x_transaction_type == 'refund').mapped('x_base_amount')))
        b_net = b_gross - b_returns
        b_ach = (b_net / bt.x_amount_total) if bt.x_amount_total else 0.0
        b_tier = get_tier(rule, b_ach, False)
        b_rate = tier_rate(b_tier)

        team_data = []
        for e in team:
            p = get_payout(e)
            touched |= p
            if p.x_is_frozen:
                continue
            team_data.append((p, e, e.x_incentive_designation_id.x_fte_branch, False))
        for e in global_members:
            if e in team or not e.x_incentive_designation_id.x_fte_branch:
                continue
            p = get_payout(e)
            touched |= p
            if p.x_is_frozen:
                continue
            team_data.append((p, e, e.x_incentive_designation_id.x_fte_branch, True))
            if e.id not in global_accum:
                global_accum[e.id] = [p, 0.0]
        if not team_data:
            continue

        pool = sum([d[0].x_payout_current for d in team_data])
        total_fte = sum([d[2] for d in team_data])
        for d in team_data:
            share = (d[2] / total_fte) if total_fte else 0.0
            bp = pool * share * b_rate
            if d[3]:
                global_accum[d[1].id][1] += bp
            else:
                d[0].write({
                    'x_branch_target': bt.x_amount_total,
                    'x_branch_net_sales': b_net,
                    'x_branch_achievement_pct': b_ach,
                    'x_branch_tier_id': b_tier.id or False,
                    'x_branch_tier_level': b_tier.x_level if b_tier else 0,
                    'x_branch_payout_rate': b_rate,
                    'x_branch_eligible': pool,
                    'x_branch_paid': pool * share,
                    'x_branch_pool': pool,
                    'x_branch_fte': d[2],
                    'x_branch_fte_share': share,
                    'x_branch_payout': bp,
                })
    for key in global_accum:
        global_accum[key][0].write({'x_branch_payout': global_accum[key][1]})

# ---------------------------------------------------------------------
# 6. Totals, then state
# ---------------------------------------------------------------------
for p in touched:
    if p.x_is_frozen:
        continue
    p.write({
        'x_target_total': p.x_target_incentive + p.x_target_bonus,
        'x_is_mixed': bool(p.x_target_bonus),
        'x_incentive_payout': p.x_payout_prior + p.x_payout_current,
        'x_total_payout': (p.x_payout_current + p.x_payout_prior
                           + p.x_payout_bonus + p.x_branch_payout),
        'x_is_eligible': bool(p.x_tier_level > 0 or p.x_branch_tier_level > 0),
    })

if only_payout:
    pass    # a recompute leaves the period / branch state alone
elif only_bt:
    only_bt.write({'x_state': 'calculated'})
else:
    period.write({'x_state': 'calculated'})

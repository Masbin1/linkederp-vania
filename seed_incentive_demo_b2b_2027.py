# -*- coding: utf-8 -*-
"""Seed a THREE-MONTH B2B worked example for VIF Sales Incentive
(June, July, August 2027) and CALCULATE it. The data is COMMITTED -- it stays
in the database as the worked example of PANDUAN_USER_VIF_SALES_INCENTIVE.md
section 34. June and July are Approved + Locked (so carry-forward rolls on),
August is left Calculated.

Run it through exec() so an error anywhere rolls the whole seed back
(set DRY_RUN = True in the dict to print the figures without committing):

    echo "try:
        exec(open('seed_incentive_demo_b2b_2027.py').read(), {'env': env, 'DRY_RUN': False})
    except BaseException:
        env.cr.rollback(); raise" | <venv>/python odoo-bin shell -c odoo.conf -d vaniaeut --no-http

Everything it creates is tagged "DEMO27":
  * branch    "Demo B2B 2027" (code DEMO27), business type B2B
  * rule      "Demo Scheme Jun-Agu 2027" (tiers of 2H 2025, valid Jun-Aug 2027)
  * periods   "Demo Jun 2027", "Demo Jul 2027", "Demo Agu 2027"
  * employees "[DEMO27] Rudi / Sari / Tono / Wati / Umar" + their users

Cases covered:
  June    Sari's invoice only PARTIALLY paid -> counts for tier, not paid;
          Sari below target -> shortfall, carried into July + August after Lock
  July    Tono resigns 15 Jul (prorated, seat's rest -> bonus targets);
          Rudi's DOWN PAYMENT lifts his tier but is not paid;
          Sari's June invoice fully paid -> paid at JUNE's rate (prior period);
          Tono below 75% -> Tier 0
  August  Wati replaces Tono from 1 Aug; Rudi's final invoice settles the DP;
          project invoice split Rudi 40% / Wati 60%; Sari below 75% -> Tier 0
Kenny (existing Global Branch Member) joins the branch payout every month.
"""
from datetime import date

from odoo import Command

S = env  # noqa: F821 -- provided by odoo-bin shell
COMPANY = S.company
M = 1_000_000

if S['incentive.branch'].search_count([('code', '=', 'DEMO27')]):
    raise SystemExit('Demo B2B 2027 already exists -- nothing done.')

ref = S.ref
lead = ref('vif_sales_incentive.designation_lead')
team = ref('vif_sales_incentive.designation_team')
support = ref('vif_sales_incentive.designation_support')

# ------------------------------------------------------------ master data
branch = S['incentive.branch'].create({
    'name': 'Demo B2B 2027', 'code': 'DEMO27', 'company_id': COMPANY.id})

src_rule = S['incentive.rule'].search([('name', '=', 'Incentive Scheme 2H 2025')], limit=1)
rule = S['incentive.rule'].create({
    'name': 'Demo Scheme Jun-Agu 2027',
    'date_from': date(2027, 6, 1), 'date_to': date(2027, 8, 31),
    'company_id': COMPANY.id,
    'base_rate': src_rule.base_rate, 'bonus_rate': src_rule.bonus_rate,
    'max_discount': src_rule.max_discount,
    'cap_tier_in_mixed': src_rule.cap_tier_in_mixed,
    'mixed_cap_tier_level': src_rule.mixed_cap_tier_level,
    'tier_ids': [Command.create({
        'name': t.name, 'level': t.level, 'achievement_min': t.achievement_min,
        'achievement_max': t.achievement_max, 'is_top_tier': t.is_top_tier,
        'allocation': t.allocation}) for t in src_rule.tier_ids.sorted('level')],
})

ROSTER = [
    # key, name, designation, start, end
    ('rudi', 'Rudi', lead, False, False),
    ('sari', 'Sari', team, False, False),
    ('tono', 'Tono', team, False, date(2027, 7, 15)),
    ('wati', 'Wati', team, date(2027, 8, 1), False),
    ('umar', 'Umar', support, False, False),
]
users, emps = {}, {}
for key, name, desig, start, end in ROSTER:
    users[key] = S['res.users'].create({
        'name': '[DEMO27] %s' % name, 'login': 'demo27.%s@vania.demo' % key,
        'email': 'demo27.%s@vania.demo' % key})
    emps[key] = S['hr.employee'].create({
        'name': '[DEMO27] %s' % name, 'user_id': users[key].id,
        'company_id': COMPANY.id,
        'incentive_branch_id': branch.id, 'incentive_business_type': 'b2b',
        'incentive_designation_id': desig.id,
        'incentive_date_start': start, 'incentive_date_end': end})

partner = S['res.partner'].create({'name': '[DEMO27] PT Pelanggan Contoh'})
product = S['product.product'].create({
    'name': '[DEMO27] Meja Kerja', 'type': 'consu', 'invoice_policy': 'order',
    'taxes_id': [Command.clear()]})


# --------------------------------------------------------------- helpers
def period(name, start, end, bt_amount):
    p = S['incentive.period'].create({
        'name': name, 'date_start': start, 'date_end': end,
        'rule_id': rule.id, 'company_id': COMPANY.id})
    p.action_open()
    S['incentive.branch.target'].create({
        'period_id': p.id, 'branch_id': branch.id, 'business_type': 'b2b',
        'amount': bt_amount})
    S['incentive.target.cascade'].create({
        'period_id': p.id, 'branch_ids': [Command.set(branch.ids)],
        'business_type': 'b2b', 'scope': 'individual',
        'redistribute_vacant': True, 'overwrite_existing': True,
    }).action_apply()
    return p


def invoice(key, d, lines, ref_text):
    """lines: [(amount, is_downpayment)]"""
    move = S['account.move'].create({
        'move_type': 'out_invoice', 'partner_id': partner.id,
        'invoice_date': d, 'invoice_user_id': users[key].id, 'ref': ref_text,
        'invoice_line_ids': [Command.create({
            'product_id': product.id, 'name': ref_text, 'quantity': 1,
            'price_unit': amt, 'is_downpayment': dp, 'tax_ids': [Command.clear()],
        }) for amt, dp in lines]})
    move.action_post()
    return move


def pay(move, d, amount=None):
    vals = {'payment_date': d}
    if amount:
        vals['amount'] = amount
    S['account.payment.register'].with_context(
        active_model='account.move', active_ids=move.ids).create(vals)._create_payments()


def close(p):
    p.action_approve()
    p.action_lock()


# ------------------------------------------------------------- June 2027
jun = period('Demo Jun 2027', date(2027, 6, 1), date(2027, 6, 30), 800 * M)

inv = invoice('rudi', date(2027, 6, 8), [(360 * M, False)], 'DEMO27 Rudi Juni')
pay(inv, date(2027, 6, 20))
inv_sari_jun = invoice('sari', date(2027, 6, 10), [(200 * M, False)], 'DEMO27 Sari Juni')
pay(inv_sari_jun, date(2027, 6, 25), 100 * M)          # partial in June
inv = invoice('tono', date(2027, 6, 12), [(240 * M, False)], 'DEMO27 Tono Juni')
pay(inv, date(2027, 6, 28))

jun.action_calculate()
close(jun)

# ------------------------------------------------------------- July 2027
jul = period('Demo Jul 2027', date(2027, 7, 1), date(2027, 7, 31), 800 * M)

pay(inv_sari_jun, date(2027, 7, 10))                   # rest of June invoice
inv = invoice('rudi', date(2027, 7, 6), [(300 * M, False)], 'DEMO27 Rudi Juli')
pay(inv, date(2027, 7, 16))
inv_rudi_dp = invoice('rudi', date(2027, 7, 20), [(100 * M, True)], 'DEMO27 Rudi DP')
pay(inv_rudi_dp, date(2027, 7, 22))
inv = invoice('sari', date(2027, 7, 9), [(260 * M, False)], 'DEMO27 Sari Juli')
pay(inv, date(2027, 7, 19))
inv = invoice('tono', date(2027, 7, 5), [(60 * M, False)], 'DEMO27 Tono Juli')
pay(inv, date(2027, 7, 12))

jul.action_calculate()
close(jul)

# ----------------------------------------------------------- August 2027
agu = period('Demo Agu 2027', date(2027, 8, 1), date(2027, 8, 31), 800 * M)

# Final invoice of Rudi's order: the product line + the DP deduction line.
inv = invoice('rudi', date(2027, 8, 5), [(250 * M, False), (-100 * M, True)],
              'DEMO27 Rudi Pelunasan')
pay(inv, date(2027, 8, 15))
inv = invoice('rudi', date(2027, 8, 10), [(200 * M, False)], 'DEMO27 Rudi Agustus')
pay(inv, date(2027, 8, 20))
inv = invoice('sari', date(2027, 8, 12), [(150 * M, False)], 'DEMO27 Sari Agustus')
pay(inv, date(2027, 8, 22))
inv = invoice('wati', date(2027, 8, 14), [(180 * M, False)], 'DEMO27 Wati Agustus')
pay(inv, date(2027, 8, 24))

# Project: PM Rudi 40% / Salesperson 2 Wati 60%.
project = S['project.project'].create({
    'name': '[DEMO27] Proyek Kantor Cabang', 'allow_billable': True,
    'partner_id': partner.id, 'user_id': users['rudi'].id,
    'x_studio_salesperson_2': users['wati'].id,
    'x_studio_komisi_pm': 0.4, 'x_studio_komisi_salesperson_2': 0.6})
so = S['sale.order'].create({
    'partner_id': partner.id, 'user_id': users['wati'].id,
    'project_id': project.id,
    'order_line': [Command.create({
        'product_id': product.id, 'product_uom_qty': 1,
        'price_unit': 100 * M, 'tax_ids': [Command.clear()]})]})
so.action_confirm()
inv = so._create_invoices()
inv.write({'invoice_date': date(2027, 8, 18), 'ref': 'DEMO27 Proyek Kantor Cabang'})
inv.action_post()
pay(inv, date(2027, 8, 28))

agu.action_calculate()


# --------------------------------------------------------------- report
def fmt(x):
    return '{:,.2f}'.format(x)


def show(p):
    print('\n=== %s (%s) ===' % (p.name, p.state))
    for t in S['incentive.target'].search([('period_id', '=', p.id)], order='employee_id, target_type'):
        print('  target %-15s %-9s %18s  prorata %.4f  shortfall %s  cf/mo %s  months %s  (%s)' % (
            t.employee_id.name, t.target_type, fmt(t.amount), t.proration_ratio,
            fmt(t.shortfall_amount), fmt(t.carry_forward_amount), t.months_remaining, t.source))
    for po in S['incentive.payout'].search([('period_id', '=', p.id)], order='employee_id'):
        print('  payout %-24s gross %s ret %s net %s ach %.4f %s %.6f | elig %s/%s excl %s | '
              'paidC %s paidP %s paidB %s | cur %s prior %s bonus %s | br %s (pool %s fte %.2f share %.4f %s %.6f) | TOTAL %s' % (
                  po.employee_id.name, fmt(po.gross_sales), fmt(po.sales_return), fmt(po.net_sales),
                  po.achievement_pct, po.tier_id.name, po.payout_rate,
                  fmt(po.eligible_incentive), fmt(po.eligible_bonus), fmt(po.excluded_discount),
                  fmt(po.paid_current_month), fmt(po.paid_prior_month), fmt(po.paid_bonus),
                  fmt(po.payout_current), fmt(po.payout_prior), fmt(po.payout_bonus),
                  fmt(po.branch_payout), fmt(po.branch_pool), po.branch_fte, po.branch_fte_share,
                  po.branch_tier_id.name, po.branch_payout_rate, fmt(po.total_payout)))
    bt = p.branch_target_ids
    print('  branch target %s carry %s total %s' % (fmt(bt.amount), fmt(bt.carry_forward_amount), fmt(bt.amount_total)))


for p in (jun, jul, agu):
    show(p)
if globals().get('DRY_RUN'):
    S.cr.rollback()
    print('\nDRY RUN -- rolled back')
else:
    S.cr.commit()
    print('\nDEMO B2B 2027 COMMITTED')

# -*- coding: utf-8 -*-
"""Seed a B2B worked example for VIF Sales Incentive (Oct + Nov 2026) and
CALCULATE it. The data is COMMITTED -- it stays in the database as the
worked example of PANDUAN_USER_VIF_SALES_INCENTIVE.md section 32.

Run it through exec() so an error anywhere rolls the whole seed back
(set DRY_RUN = True in the dict to print the figures without committing):

    echo "try:
        exec(open('seed_incentive_demo_b2b_2026.py').read(), {'env': env, 'DRY_RUN': False})
    except BaseException:
        env.cr.rollback(); raise" | <venv>/python odoo-bin shell -c odoo.conf -d vaniaeut --no-http

Everything it creates is tagged "DEMO" so it is easy to find:
  * branch      "Demo B2B" (code DEMO), business type B2B
  * rule        "Demo Scheme Q4 2026" (same tiers as 2H 2025)
  * periods     "Demo Okt 2026", "Demo Nov 2026"
  * employees   "[DEMO] Andi / Bella / Candra / Dewi / Eko" + their users
  * customer    "[DEMO] PT Contoh Pelanggan", product "[DEMO] Sofa Kantor"

Refuses to run twice: delete the demo records first to rebuild.

Cases covered (Oct 2026):
  Andi   Lead   invoice 380M paid  + 30% of a project invoice -> mixed, tier capped
  Bella  Team   150M paid + 50M UNPAID (paid 10 Nov -> prior-period payout in Nov)
  Candra Team   170M + 30M line at 40% discount (excluded) + 10M credit note
  Dewi   Team   joins 16 Oct (prorated target), 60M own invoice + 70% of project
  Eko    Support no target, branch payout only
  Kenny  (existing Global Branch Member) joins the branch payout
"""
from datetime import date

from odoo import Command

S = env  # noqa: F821 -- provided by odoo-bin shell
COMPANY = S.company
M = 1_000_000

if S['incentive.branch'].search_count([('code', '=', 'DEMO')]):
    raise SystemExit('Demo B2B already exists -- nothing done.')

ref = S.ref
lead = ref('vif_sales_incentive.designation_lead')
team = ref('vif_sales_incentive.designation_team')
support = ref('vif_sales_incentive.designation_support')

# ------------------------------------------------------------ master data
branch = S['incentive.branch'].create({
    'name': 'Demo B2B', 'code': 'DEMO', 'company_id': COMPANY.id})

src_rule = S['incentive.rule'].search([('name', '=', 'Incentive Scheme 2H 2025')], limit=1)
rule = S['incentive.rule'].create({
    'name': 'Demo Scheme Q4 2026',
    'date_from': date(2026, 10, 1), 'date_to': date(2026, 12, 31),
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
    ('andi', 'Andi', lead, False),
    ('bella', 'Bella', team, False),
    ('candra', 'Candra', team, False),
    ('dewi', 'Dewi', team, date(2026, 10, 16)),
    ('eko', 'Eko', support, False),
]
users, emps = {}, {}
for key, name, desig, start in ROSTER:
    users[key] = S['res.users'].create({
        'name': '[DEMO] %s' % name, 'login': 'demo.%s@vania.demo' % key,
        'email': 'demo.%s@vania.demo' % key})
    emps[key] = S['hr.employee'].create({
        'name': '[DEMO] %s' % name, 'user_id': users[key].id,
        'company_id': COMPANY.id,
        'incentive_branch_id': branch.id, 'incentive_business_type': 'b2b',
        'incentive_designation_id': desig.id,
        'incentive_date_start': start})

partner = S['res.partner'].create({'name': '[DEMO] PT Contoh Pelanggan'})
product = S['product.product'].create({
    'name': '[DEMO] Sofa Kantor', 'type': 'consu', 'invoice_policy': 'order',
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
    """lines: [(amount, discount%)]"""
    move = S['account.move'].create({
        'move_type': 'out_invoice', 'partner_id': partner.id,
        'invoice_date': d, 'invoice_user_id': users[key].id, 'ref': ref_text,
        'invoice_line_ids': [Command.create({
            'product_id': product.id, 'name': ref_text, 'quantity': 1,
            'price_unit': amt, 'discount': disc, 'tax_ids': [Command.clear()],
        }) for amt, disc in lines]})
    move.action_post()
    return move


def pay(move, d):
    S['account.payment.register'].with_context(
        active_model='account.move', active_ids=move.ids).create(
        {'payment_date': d})._create_payments()


# ------------------------------------------------------------- Oct 2026
okt = period('Demo Okt 2026', date(2026, 10, 1), date(2026, 10, 31), 1000 * M)

inv_andi = invoice('andi', date(2026, 10, 5), [(380 * M, 0)], 'DEMO Andi - Kantor A')
pay(inv_andi, date(2026, 10, 15))

inv_bella_a = invoice('bella', date(2026, 10, 8), [(150 * M, 0)], 'DEMO Bella - Kantor B')
pay(inv_bella_a, date(2026, 10, 20))
inv_bella_b = invoice('bella', date(2026, 10, 25), [(50 * M, 0)], 'DEMO Bella - Kantor C')
# inv_bella_b stays unpaid in October

inv_candra = invoice('candra', date(2026, 10, 12),
                     [(170 * M, 0), (50 * M, 40)], 'DEMO Candra - Kantor D')
pay(inv_candra, date(2026, 10, 22))
cn_candra = S['account.move'].create({
    'move_type': 'out_refund', 'partner_id': partner.id,
    'invoice_date': date(2026, 10, 28), 'invoice_user_id': users['candra'].id,
    'reversed_entry_id': inv_candra.id, 'ref': 'DEMO Retur Candra',
    'invoice_line_ids': [Command.create({
        'product_id': product.id, 'name': 'DEMO Retur Candra', 'quantity': 1,
        'price_unit': 10 * M, 'tax_ids': [Command.clear()]})]})
cn_candra.action_post()

inv_dewi = invoice('dewi', date(2026, 10, 20), [(60 * M, 0)], 'DEMO Dewi - Kantor E')
pay(inv_dewi, date(2026, 10, 27))

# Project: PM Andi 30% / Salesperson 2 Dewi 70%. The SO salesperson (Bella)
# is NOT on the project, so she gets nothing from it.
project = S['project.project'].create({
    'name': '[DEMO] Proyek Interior Kantor', 'allow_billable': True,
    'partner_id': partner.id, 'user_id': users['andi'].id,
    'x_studio_salesperson_2': users['dewi'].id,
    'x_studio_komisi_pm': 0.3, 'x_studio_komisi_salesperson_2': 0.7})
so = S['sale.order'].create({
    'partner_id': partner.id, 'user_id': users['bella'].id,
    'project_id': project.id,
    'order_line': [Command.create({
        'product_id': product.id, 'product_uom_qty': 1,
        'price_unit': 100 * M, 'tax_ids': [Command.clear()]})]})
so.action_confirm()
inv_project = so._create_invoices()
inv_project.write({'invoice_date': date(2026, 10, 18), 'ref': 'DEMO Proyek Interior'})
inv_project.action_post()
pay(inv_project, date(2026, 10, 30))

okt.action_calculate()

# ------------------------------------------------------------- Nov 2026
pay(inv_bella_b, date(2026, 11, 10))
nov = period('Demo Nov 2026', date(2026, 11, 1), date(2026, 11, 30), 1000 * M)
nov.action_calculate()


# --------------------------------------------------------------- report
def show(p):
    print('\n=== %s ===' % p.name)
    for t in S['incentive.target'].search([('period_id', '=', p.id)], order='employee_id'):
        print('  target %-16s %-9s %16s  FTE %.2f  prorata %.4f  (%s)' % (
            t.employee_id.name, t.target_type, '{:,.2f}'.format(t.amount),
            t.fte_used, t.proration_ratio, t.source))
    for po in S['incentive.payout'].search([('period_id', '=', p.id)], order='employee_id'):
        print('  payout %-16s net %s ach %.4f tier %s rate %.6f | inc %s bon %s | '
              'cur %s prior %s bonus %s branch %s TOTAL %s' % (
                  po.employee_id.name, '{:,.0f}'.format(po.net_sales),
                  po.achievement_pct, po.tier_id.name, po.payout_rate,
                  '{:,.0f}'.format(po.eligible_incentive), '{:,.0f}'.format(po.eligible_bonus),
                  '{:,.2f}'.format(po.payout_current), '{:,.2f}'.format(po.payout_prior),
                  '{:,.2f}'.format(po.payout_bonus), '{:,.2f}'.format(po.branch_payout),
                  '{:,.2f}'.format(po.total_payout)))


show(okt)
show(nov)
if globals().get('DRY_RUN'):
    S.cr.rollback()
    print('\nDRY RUN -- rolled back')
else:
    S.cr.commit()
    print('\nDEMO B2B COMMITTED')

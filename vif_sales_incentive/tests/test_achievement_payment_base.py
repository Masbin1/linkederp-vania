# -*- coding: utf-8 -*-
"""Achievement vs payout base, with down payments.

The rules, from the client's August -> November walk-through:

* Branch and individual ACHIEVEMENT (the tier) count everything invoiced in
  the month: paid or not, down-payment lines included.
* The PAYOUT base counts only what is FULLY PAID in the month, and never a
  down-payment line on its own. A settled order is released in full on the
  final invoice's real product line, in the month that invoice is paid.
* The branch payout = branch tier x the employee's own paid base. A month
  with no invoiced sales has tier 0, so money collected that month earns
  nothing (the client's October/November case).

The test runs in 2027 so it never collides with the periods seeded by
``data/incentive_period_data.xml`` (2H 2025).
"""
from odoo import fields
from odoo.tests import TransactionCase, tagged

M = 1_000_000
# payout_rate is stored with 4 decimals, so Tier 5's 1.05 x 0.75% lands on
# 0.0079 -- the exact number the engine multiplies with.
RATE_T4 = 0.0075
RATE_T5 = 0.0079


@tagged('post_install', '-at_install')
class TestAchievementPaymentBase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.user = cls.env['res.users'].create({
            'name': 'Achievement Sales User',
            'login': 'achievement_sales_user',
            'email': 'achievement.sales@example.com',
        })
        cls.employee = cls.env['hr.employee'].create({
            'name': 'Achievement Sales',
            'user_id': cls.user.id,
            'incentive_branch_id': cls.env.ref(
                'vif_sales_incentive.branch_jkt').id,
            'incentive_business_type': 'b2b',
            'incentive_designation_id': cls.env.ref(
                'vif_sales_incentive.designation_team').id,
        })

        rule = cls.env['incentive.rule'].create({
            'name': 'Achievement Rule 2027',
            'date_from': fields.Date.to_date('2027-01-01'),
            'date_to': fields.Date.to_date('2027-12-31'),
            'company_id': cls.company.id,
            'base_rate': 0.0075,
            'tier_ids': [(0, 0, {
                'name': 'Tier 0', 'level': 0, 'achievement_min': 0.0,
                'achievement_max': 0.75, 'allocation': 0.0,
            }), (0, 0, {
                'name': 'Tier 4', 'level': 4, 'achievement_min': 1.0,
                'achievement_max': 1.1, 'allocation': 1.0,
            }), (0, 0, {
                'name': 'Tier 5', 'level': 5, 'achievement_min': 1.1,
                'allocation': 1.05, 'is_top_tier': True,
            })],
        })
        cls.periods = {}
        for month in (1, 2, 3, 4):
            date_start = fields.Date.to_date('2027-%02d-01' % month)
            period = cls.env['incentive.period'].create({
                'name': 'Achievement %02d/2027' % month,
                'date_start': date_start,
                'date_end': fields.Date.end_of(date_start, 'month'),
                'rule_id': rule.id,
                'company_id': cls.company.id,
            })
            period.action_open()
            cls.periods[month] = period
            cls.env['incentive.branch.target'].create({
                'period_id': period.id,
                'branch_id': cls.employee.incentive_branch_id.id,
                'business_type': 'b2b',
                'amount': 100 * M,
            })
            cls.env['incentive.target'].create({
                'period_id': period.id,
                'employee_id': cls.employee.id,
                'target_type': 'incentive',
                'amount': 100 * M,
            })

        cls.partner = cls.env['res.partner'].create(
            {'name': 'Achievement Customer'})
        cls.product = cls.env['product.product'].create(
            {'name': 'Achievement Widget', 'type': 'consu'})

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _invoice(self, date, lines):
        """Create + post an invoice. ``lines`` is (amount, is_downpayment)."""
        move = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'invoice_date': date,
            'invoice_user_id': self.user.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'name': 'Achievement line',
                'quantity': 1.0,
                'price_unit': amount,
                'is_downpayment': is_dp,
                'tax_ids': [(5, 0, 0)],
            }) for amount, is_dp in lines],
        })
        move.action_post()
        return move

    def _pay(self, move, date):
        wizard = self.env['account.payment.register'].with_context(
            active_model='account.move', active_ids=move.ids).create({
                'payment_date': date,
            })
        wizard._create_payments()

    def _calculate(self, period):
        self.env['incentive.transaction']._generate_for_period(period)
        return self.env['incentive.payout']._compute_for_period(period)

    def _payout(self, period):
        return self.env['incentive.payout'].search([
            ('period_id', '=', period.id),
            ('employee_id', '=', self.employee.id),
        ], limit=1)

    # ------------------------------------------------------------------
    # The client's four-month walk-through
    # ------------------------------------------------------------------
    def test_january_dp_counts_for_tier_but_not_for_payout(self):
        jan = self.periods[1]
        inv1 = self._invoice(fields.Date.to_date('2027-01-05'),
                             [(100 * M, False)])
        self._pay(inv1, fields.Date.to_date('2027-01-06'))
        dp = self._invoice(fields.Date.to_date('2027-01-07'), [(50 * M, True)])
        self._pay(dp, fields.Date.to_date('2027-01-08'))
        self._calculate(jan)

        payout = self._payout(jan)
        # Eligibility: 100M invoice + 50M DP = 150M -> Tier 5.
        self.assertAlmostEqual(payout.net_sales, 150 * M, delta=1.0)
        self.assertEqual(payout.tier_id.level, 5)
        # Payout base: only the 100M that was actually collected.
        self.assertAlmostEqual(payout.paid_current_month, 100 * M, delta=1.0)
        self.assertAlmostEqual(
            payout.payout_current, 100 * M * RATE_T5, delta=1.0)
        # Branch stream: same two bases.
        self.assertAlmostEqual(payout.branch_net_sales, 150 * M, delta=1.0)
        self.assertEqual(payout.branch_tier_id.level, 5)
        self.assertAlmostEqual(payout.branch_paid, 100 * M, delta=1.0)
        self.assertAlmostEqual(
            payout.branch_payout, 100 * M * RATE_T5, delta=1.0)

    def test_february_settlement_releases_the_full_order(self):
        # Settle January's order: 100M goods - 50M DP = 50M due, plus a
        # separate 50M invoice. Both fully paid.
        feb = self.periods[2]
        final = self._invoice(fields.Date.to_date('2027-02-03'),
                              [(100 * M, False), (-50 * M, True)])
        self._pay(final, fields.Date.to_date('2027-02-04'))
        inv4 = self._invoice(fields.Date.to_date('2027-02-05'),
                             [(50 * M, False)])
        self._pay(inv4, fields.Date.to_date('2027-02-06'))
        self._calculate(feb)

        payout = self._payout(feb)
        # Eligibility: 100M - 50M (DP negation) + 50M = 100M -> Tier 4.
        self.assertAlmostEqual(payout.net_sales, 100 * M, delta=1.0)
        self.assertEqual(payout.tier_id.level, 4)
        # Payout base: the settled order in full (100M) + 50M = 150M.
        self.assertAlmostEqual(payout.paid_current_month, 150 * M, delta=1.0)
        self.assertAlmostEqual(
            payout.payout_current, 150 * M * RATE_T4, delta=1.0)
        self.assertAlmostEqual(payout.branch_net_sales, 100 * M, delta=1.0)
        self.assertAlmostEqual(payout.branch_paid, 150 * M, delta=1.0)
        self.assertAlmostEqual(
            payout.branch_payout, 150 * M * RATE_T4, delta=1.0)

    def test_march_unpaid_invoice_sets_the_tier_but_not_the_payout(self):
        mar = self.periods[3]
        self._invoice(fields.Date.to_date('2027-03-05'), [(100 * M, False)])
        self._calculate(mar)

        payout = self._payout(mar)
        self.assertAlmostEqual(payout.net_sales, 100 * M, delta=1.0)
        self.assertEqual(payout.tier_id.level, 4)
        self.assertAlmostEqual(payout.paid_current_month, 0.0, delta=1.0)
        self.assertAlmostEqual(payout.payout_current, 0.0, delta=1.0)
        self.assertAlmostEqual(payout.branch_net_sales, 100 * M, delta=1.0)
        self.assertAlmostEqual(payout.branch_paid, 0.0, delta=1.0)
        self.assertAlmostEqual(payout.branch_payout, 0.0, delta=1.0)

    def test_april_collection_has_no_branch_tier_so_no_branch_payout(self):
        # Pay the March invoice in April. April invoiced nothing, so its
        # branch tier is 0 even though 100M is collected -- the branch payout
        # is 0. The individual stream keeps its source-period rate.
        mar = self.periods[3]
        inv5 = self._invoice(fields.Date.to_date('2027-03-05'),
                             [(100 * M, False)])
        self._calculate(mar)
        self._pay(inv5, fields.Date.to_date('2027-04-05'))
        self._calculate(self.periods[4])

        payout = self._payout(self.periods[4])
        self.assertAlmostEqual(payout.net_sales, 0.0, delta=1.0)
        self.assertEqual(payout.tier_id.level, 0)
        self.assertAlmostEqual(payout.paid_prior_month, 100 * M, delta=1.0)
        self.assertAlmostEqual(payout.branch_net_sales, 0.0, delta=1.0)
        self.assertAlmostEqual(payout.branch_paid, 100 * M, delta=1.0)
        self.assertAlmostEqual(payout.branch_payout, 0.0, delta=1.0)
        # Individual prior-period rule: March's frozen Tier 4 rate.
        self.assertAlmostEqual(
            payout.payout_prior, 100 * M * RATE_T4, delta=1.0)

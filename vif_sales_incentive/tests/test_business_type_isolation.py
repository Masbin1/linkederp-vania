# -*- coding: utf-8 -*-
"""B2B / B2C isolation within the same branch.

One branch carries two separate teams. Their targets, FTE denominators,
achievements, and payouts must be completely independent -- cascading B2C
must never read B2B employees, and vice versa.

The numbers mirror the client's Jakarta B2C scenario:
  Branch target B2C = 701,394,331.91
  Total FTE B2C     = 3.5  (Lead 1.5 + Team 1.0 + Team 1.0)
  Nur Suci (Lead)   = 1.5 / 3.5 x 701,394,331.91 ~ 300,597,571
"""
from odoo import fields
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestBusinessTypeIsolation(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.lead = cls.env.ref('vif_sales_incentive.designation_lead')
        cls.team = cls.env.ref('vif_sales_incentive.designation_team')

        cls.branch = cls.env['incentive.branch'].create({
            'name': 'Jakarta', 'code': 'JKT',
            'company_id': cls.company.id,
        })

        # -- B2C team: Lead(1.5) + 2 x Team(1.0) = 3.5 FTE --
        cls.nur_suci, cls.b2c_m1, cls.b2c_m2 = cls.env['hr.employee'].create([
            {'name': 'Nur Suci', 'incentive_branch_id': cls.branch.id,
             'incentive_business_type': 'b2c',
             'incentive_designation_id': cls.lead.id},
            {'name': 'B2C Member 1', 'incentive_branch_id': cls.branch.id,
             'incentive_business_type': 'b2c',
             'incentive_designation_id': cls.team.id},
            {'name': 'B2C Member 2', 'incentive_branch_id': cls.branch.id,
             'incentive_business_type': 'b2c',
             'incentive_designation_id': cls.team.id},
        ])

        # -- B2B team: Lead(1.5) + 3 x Team(1.0) = 4.5 FTE --
        cls.b2b_lead, cls.b2b_m1, cls.b2b_m2, cls.b2b_m3 = (
            cls.env['hr.employee'].create([
                {'name': 'B2B Lead', 'incentive_branch_id': cls.branch.id,
                 'incentive_business_type': 'b2b',
                 'incentive_designation_id': cls.lead.id},
                {'name': 'B2B Member 1', 'incentive_branch_id': cls.branch.id,
                 'incentive_business_type': 'b2b',
                 'incentive_designation_id': cls.team.id},
                {'name': 'B2B Member 2', 'incentive_branch_id': cls.branch.id,
                 'incentive_business_type': 'b2b',
                 'incentive_designation_id': cls.team.id},
                {'name': 'B2B Member 3', 'incentive_branch_id': cls.branch.id,
                 'incentive_business_type': 'b2b',
                 'incentive_designation_id': cls.team.id},
            ]))

        rule = cls.env['incentive.rule'].create({
            'name': 'Isolation Rule',
            'date_from': fields.Date.to_date('2025-01-01'),
            'date_to': fields.Date.to_date('2025-12-31'),
            'company_id': cls.company.id,
            'tier_ids': [(0, 0, {
                'name': 'Tier 1', 'level': 1, 'achievement_min': 0.0,
                'achievement_max': 1.0, 'allocation': 0.4,
            }), (0, 0, {
                'name': 'Tier 4', 'level': 4, 'achievement_min': 1.0,
                'allocation': 1.0, 'is_top_tier': True,
            })],
        })
        cls.period = cls.env['incentive.period'].create({
            'name': 'Isolation Oct 2025',
            'date_start': fields.Date.to_date('2025-10-01'),
            'date_end': fields.Date.to_date('2025-10-31'),
            'rule_id': rule.id,
            'company_id': cls.company.id,
        })
        cls.period.action_open()

        cls.bt_b2c = cls.env['incentive.branch.target'].create({
            'period_id': cls.period.id, 'branch_id': cls.branch.id,
            'business_type': 'b2c', 'amount': 701_394_331.91,
        })
        cls.bt_b2b = cls.env['incentive.branch.target'].create({
            'period_id': cls.period.id, 'branch_id': cls.branch.id,
            'business_type': 'b2b', 'amount': 500_000_000.0,
        })

    def _target(self, employee, target_type='incentive'):
        return self.env['incentive.target'].search([
            ('period_id', '=', self.period.id),
            ('employee_id', '=', employee.id),
            ('target_type', '=', target_type),
        ], limit=1)

    # ------------------------------------------------------------------
    # Effective FTE display fields
    # ------------------------------------------------------------------
    def test_effective_fte_separated_by_business_type(self):
        """The branch form must show B2B and B2C FTE independently."""
        self.assertAlmostEqual(self.branch.effective_fte_b2b, 4.5, 2)
        self.assertAlmostEqual(self.branch.effective_fte_b2c, 3.5, 2)
        self.assertAlmostEqual(self.branch.effective_fte, 8.0, 2)

    # ------------------------------------------------------------------
    # Cascade isolation
    # ------------------------------------------------------------------
    def test_b2c_cascade_uses_only_b2c_fte(self):
        """B2C denominator must be 3.5, not 8.0 (the combined branch FTE)."""
        self.env['incentive.target.cascade'].create({
            'period_id': self.period.id,
            'branch_ids': [(6, 0, self.branch.ids)],
            'business_type': 'b2c',
        }).action_apply()

        # Nur Suci: Lead FTE 1.5 / 3.5 total B2C FTE x 701,394,331.91
        expected = 701_394_331.91 * (1.5 / 3.5)
        self.assertAlmostEqual(
            self._target(self.nur_suci).amount, expected, delta=1.0)

        # Team member: 1.0 / 3.5 x 701,394,331.91
        expected_team = 701_394_331.91 * (1.0 / 3.5)
        self.assertAlmostEqual(
            self._target(self.b2c_m1).amount, expected_team, delta=1.0)

    def test_b2b_cascade_uses_only_b2b_fte(self):
        """B2B denominator must be 4.5, not 8.0."""
        self.env['incentive.target.cascade'].create({
            'period_id': self.period.id,
            'branch_ids': [(6, 0, self.branch.ids)],
            'business_type': 'b2b',
        }).action_apply()

        # B2B Lead: 1.5 / 4.5 x 500,000,000
        expected = 500_000_000.0 * (1.5 / 4.5)
        self.assertAlmostEqual(
            self._target(self.b2b_lead).amount, expected, delta=1.0)

    def test_b2c_cascade_does_not_create_b2b_targets(self):
        """Cascading B2C must not touch any B2B employee."""
        self.env['incentive.target.cascade'].create({
            'period_id': self.period.id,
            'branch_ids': [(6, 0, self.branch.ids)],
            'business_type': 'b2c',
        }).action_apply()

        self.assertFalse(self._target(self.b2b_lead))
        self.assertFalse(self._target(self.b2b_m1))

    def test_b2b_cascade_does_not_create_b2c_targets(self):
        """Cascading B2B must not touch any B2C employee."""
        self.env['incentive.target.cascade'].create({
            'period_id': self.period.id,
            'branch_ids': [(6, 0, self.branch.ids)],
            'business_type': 'b2b',
        }).action_apply()

        self.assertFalse(self._target(self.nur_suci))
        self.assertFalse(self._target(self.b2c_m1))

    def test_cascading_both_types_independently(self):
        """Run both cascades; each must produce its own figures untouched."""
        self.env['incentive.target.cascade'].create({
            'period_id': self.period.id,
            'branch_ids': [(6, 0, self.branch.ids)],
            'business_type': 'b2c',
        }).action_apply()
        self.env['incentive.target.cascade'].create({
            'period_id': self.period.id,
            'branch_ids': [(6, 0, self.branch.ids)],
            'business_type': 'b2b',
        }).action_apply()

        # B2C targets unchanged after B2B cascade
        expected_b2c = 701_394_331.91 * (1.5 / 3.5)
        self.assertAlmostEqual(
            self._target(self.nur_suci).amount, expected_b2c, delta=1.0)

        # B2B targets unchanged after B2C cascade
        expected_b2b = 500_000_000.0 * (1.5 / 4.5)
        self.assertAlmostEqual(
            self._target(self.b2b_lead).amount, expected_b2b, delta=1.0)

    def test_b2c_targets_sum_to_branch_target(self):
        """The cascade must account for every rupiah of the branch target."""
        self.env['incentive.target.cascade'].create({
            'period_id': self.period.id,
            'branch_ids': [(6, 0, self.branch.ids)],
            'business_type': 'b2c',
        }).action_apply()

        total = sum(self.env['incentive.target'].search([
            ('period_id', '=', self.period.id),
            ('business_type', '=', 'b2c'),
        ]).mapped('amount'))
        self.assertAlmostEqual(total, 701_394_331.91, delta=1.0)

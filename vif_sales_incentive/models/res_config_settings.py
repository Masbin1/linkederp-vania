# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    incentive_rule_id = fields.Many2one(
        'incentive.rule', string='Active Incentive Rule',
        compute='_compute_incentive_rule_id',
        help="Rule in effect today for the current company. Resolved the "
             "same way as the S07 discount-eligibility check on invoice "
             "lines: date_from <= today <= date_to, scoped to the company.")
    incentive_base_rate = fields.Float(
        related='incentive_rule_id.base_rate', readonly=False,
        string='Base Rate')
    incentive_bonus_rate = fields.Float(
        related='incentive_rule_id.bonus_rate', readonly=False,
        string='Bonus Rate')
    incentive_max_discount = fields.Float(
        related='incentive_rule_id.max_discount', readonly=False,
        string='Max Eligible Discount (%)')
    incentive_cap_tier_in_mixed = fields.Boolean(
        related='incentive_rule_id.cap_tier_in_mixed', readonly=False,
        string='Cap Tier 5 in Mixed Scenario')
    incentive_mixed_cap_tier_level = fields.Integer(
        related='incentive_rule_id.mixed_cap_tier_level', readonly=False,
        string='Mixed Scenario Cap Level')

    @api.depends('company_id')
    def _compute_incentive_rule_id(self):
        Rule = self.env['incentive.rule']
        today = fields.Date.context_today(self)
        for wizard in self:
            company = wizard.company_id or self.env.company
            wizard.incentive_rule_id = Rule.search([
                ('date_from', '<=', today),
                '|', ('date_to', '=', False), ('date_to', '>=', today),
                ('company_id', '=', company.id),
            ], limit=1)

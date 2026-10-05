# -*- coding: utf-8 -*-
import logging

from odoo import api, models
from odoo.fields import Domain

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.model
    def _pos_branch_cashier_domain(self, config):
        """Cashiers visible in POS "Select Cashier" = employees whose branch
        is one of the *currently logged-in Odoo user's* allowed branches,
        AND who have a PIN set.

        IMPORTANT: this must be based on ``self.env.user`` (the Odoo user
        whose browser session is loading the POS data right now), NOT on
        ``config.current_user_id`` (= pos.session.user_id, the "Responsible"
        who opened the register). Those are frequently different people: one
        person opens the register for the day, then several different
        employees log into Odoo with their own accounts throughout the shift
        to use the same POS terminal. Filtering on the session opener would
        show every cashier the opener (often a supervisor/all-branch user)
        is allowed to see, to everyone using that terminal — which is the
        bug that made the previous filtering attempt ineffective.

        Fails closed (Domain.FALSE) in every degenerate case: missing
        fields, or the user has no allowed branches.
        """
        if "x_branch" not in self._fields:
            _logger.warning(
                "[POS Branch Cashier] hr.employee.x_branch is missing; "
                "failing closed (no cashiers visible)."
            )
            return Domain.FALSE

        user = self.env.user
        if "x_studio_many2many_field_51u_1je2hqiji" not in user._fields:
            _logger.warning(
                "[POS Branch Cashier] res.users.x_studio_many2many_field_51u_1je2hqiji "
                "is missing; failing closed (no cashiers visible)."
            )
            return Domain.FALSE

        branch_ids = user.sudo().x_studio_many2many_field_51u_1je2hqiji.ids

        if not branch_ids:
            _logger.info(
                "[POS Branch Cashier] current_user=%s (uid=%s) has no allowed "
                "branches; cashier list is empty.",
                user.login, user.id,
            )
            return Domain.FALSE

        _logger.info(
            "[POS Branch Cashier] current_user=%s (uid=%s) allowed_branch_ids=%s",
            user.login, user.id, branch_ids,
        )
        return Domain.AND([
            [("x_branch", "in", branch_ids)],
            [("pin", "!=", False)],
        ])

    @api.model
    def _load_pos_data_domain(self, data, config):
        domain = super()._load_pos_data_domain(data, config)
        if not config.module_pos_hr:
            return domain
        branch_domain = self._pos_branch_cashier_domain(config)
        if branch_domain is Domain.FALSE:
            return Domain.FALSE
        return Domain.AND([domain, branch_domain])

    def _unrelevant_records(self, config):
        """Purge cashiers cached in the browser's IndexedDB from a previous
        user/session too. Without this, switching the logged-in Odoo user on
        the same device (without a full data wipe) could still show
        previously cached employees that are no longer allowed (fail open)."""
        ids = super()._unrelevant_records(config)
        if not config.module_pos_hr:
            return ids
        branch_domain = self._pos_branch_cashier_domain(config)
        if branch_domain is Domain.FALSE:
            return list(set(ids) | set(self.ids))
        allowed = self.sudo().filtered_domain(branch_domain).ids
        return list(set(ids) | (set(self.ids) - set(allowed)))

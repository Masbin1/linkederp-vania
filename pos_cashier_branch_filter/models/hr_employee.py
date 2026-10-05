# -*- coding: utf-8 -*-
import logging

from odoo import api, models
from odoo.fields import Domain

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.model
    def _pos_branch_cashier_domain(self, config):
        """Cashiers visible = employee branch in the *logged-in user's* allowed
        branches AND a PIN is set. Fails closed (Domain.FALSE) in every
        degenerate case: no allowed branches, missing field."""
        if "x_branch" not in self._fields:
            _logger.warning(
                "[POS Branch Cashier] hr.employee.x_branch is missing; "
                "failing closed (no cashiers visible)."
            )
            return Domain.FALSE

        user = config.current_user_id
        if "x_studio_many2many_field_51u_1je2hqiji" not in user._fields:
            _logger.warning(
                "[POS Branch Cashier] res.users.x_studio_many2many_field_51u_1je2hqiji "
                "is missing; failing closed (no cashiers visible)."
            )
            return Domain.FALSE

        branch_ids = user.sudo().x_studio_many2many_field_51u_1je2hqiji.ids

        if not branch_ids:
            _logger.info(
                "[POS Branch Cashier] user=%s has no allowed branches; "
                "cashier list is empty.", user.display_name
            )
            return Domain.FALSE

        _logger.info(
            "[POS Branch Cashier] user=%s allowed_branch_ids=%s",
            user.display_name, branch_ids,
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
        """Also purge cashiers cached in the browser's IndexedDB from a previous
        user/session. Without this, a user with no allowed branches would still
        see the previously cached employee list (fail open)."""
        ids = super()._unrelevant_records(config)
        if not config.module_pos_hr:
            return ids
        branch_domain = self._pos_branch_cashier_domain(config)
        if branch_domain is Domain.FALSE:
            return list(set(ids) | set(self.ids))
        allowed = self.sudo().filtered_domain(branch_domain).ids
        return list(set(ids) | (set(self.ids) - set(allowed)))

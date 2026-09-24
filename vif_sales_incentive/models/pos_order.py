# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    incentive_transaction_ids = fields.One2many(
        'incentive.transaction', 'pos_order_id', string='Incentive Transactions')

    def _generate_pos_order_invoice(self):
        """Override to set incentive_employee_id from the POS cashier.

        Standard Odoo derives incentive_employee_id from invoice_user_id,
        but in POS the actual cashier is employee_id, which may differ from
        the session's responsible user.
        """
        moves = super()._generate_pos_order_invoice()
        for order in self:
            if order.employee_id and order.account_move:
                order.account_move.incentive_employee_id = order.employee_id
        return moves

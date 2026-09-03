# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_reference = fields.Char(string='Customer Reference')
    employee_id = fields.Char(string='Employee')
    percentage_deal = fields.Float(string='Percentage Deal')

    revision_number = fields.Integer(
        string='Revision', default=0, copy=False,
        help='Revision sequence number. 0 means original order.')
    revision_parent_id = fields.Many2one(
        'sale.order', string='Revision Of', copy=False, readonly=True,
        help='Original sale order this revision was created from.')
    revision_ids = fields.One2many(
        'sale.order', 'revision_parent_id', string='Revisions', copy=False)

    def action_create_revision(self):
        self.ensure_one()
        root = self.revision_parent_id or self
        existing_numbers = [root.revision_number] + root.revision_ids.mapped('revision_number')
        next_number = max(existing_numbers) + 1
        new_order = self.copy(default={
            'revision_parent_id': root.id,
            'revision_number': next_number,
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': new_order.id,
            'target': 'current',
        }

# Field  : x_incentive_refund.x_base_amount   (not stored)
# Depends: x_transaction_id
# The WHOLE invoice line (every share of a project split).
Tx = self.env['x_incentive_transaction']
for record in self:
    tx = record.x_transaction_id
    rows = tx
    if tx.x_move_line_id:
        rows = Tx.search([('x_move_line_id', '=', tx.x_move_line_id.id),
                          ('x_transaction_type', '=', 'invoice')])
    record['x_base_amount'] = sum(rows.mapped('x_base_amount'))

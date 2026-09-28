# Field  : x_incentive_refund.x_refundable_amount   (not stored)
# Depends: x_transaction_id
# What is left of the WHOLE invoice line after earlier refunds.
Tx = self.env['x_incentive_transaction']
for record in self:
    tx = record.x_transaction_id
    rows = tx
    if tx.x_move_line_id:
        rows = Tx.search([('x_move_line_id', '=', tx.x_move_line_id.id),
                          ('x_transaction_type', '=', 'invoice')])
    refundable = 0.0
    for row in rows:
        refunded = 0.0
        for rev in row.x_reversal_ids:
            if rev.x_state != 'reversed':
                refunded += rev.x_base_amount
        refundable += max(row.x_base_amount + refunded, 0.0)
    record['x_refundable_amount'] = refundable

# Server Action : "VIF: Refund Confirm"   Model: x_incentive_refund
# Button        : Create Credit Note (in the refund form)
#
# Creates + posts a partial credit note for the invoice line, scaled to the
# refund amount. The next Calculate picks the credit note up, splits it like
# the invoice and nets it off the original line's payout.
rec = record
if rec.x_refund_move_id:
    raise UserError('This refund was already processed as credit note %s.'
                    % rec.x_refund_move_id.display_name)
rounding = rec.x_currency_id.rounding or 0.01
if float_compare(rec.x_refund_amount, 0.0, precision_rounding=rounding) <= 0:
    raise UserError('Refund amount must be positive.')
if float_compare(rec.x_refund_amount, rec.x_refundable_amount,
                 precision_rounding=rounding) > 0:
    raise UserError('Refund amount %s exceeds the refundable amount %s.'
                    % (rec.x_refund_amount, rec.x_refundable_amount))

tx = rec.x_transaction_id
move = tx.x_move_id
line = tx.x_move_line_id
subtotal = line.price_subtotal or 1.0
qty = round(line.quantity * rec.x_refund_amount / subtotal, 6)
credit_note = env['account.move'].create({
    'move_type': 'out_refund',
    'partner_id': move.partner_id.id,
    'invoice_date': datetime.date.today(),
    'journal_id': move.journal_id.id,
    'reversed_entry_id': move.id,
    'ref': 'Incentive refund of %s' % (move.name or move.id),
    'invoice_user_id': move.invoice_user_id.id,
    'invoice_line_ids': [Command.create({
        'product_id': line.product_id.id,
        'product_uom_id': line.product_uom_id.id,
        'quantity': qty,
        'price_unit': line.price_unit,
        'discount': line.discount,
        'tax_ids': [Command.set(line.tax_ids.ids)],
        'account_id': line.account_id.id,
        'name': line.name or line.product_id.display_name,
        'analytic_distribution': line.analytic_distribution,
    })],
})
credit_note.action_post()
full = float_compare(rec.x_refund_amount, rec.x_refundable_amount,
                     precision_rounding=rounding) >= 0
rec.write({'x_refund_move_id': credit_note.id})
if full:
    # A full refund closes every share of the line (project split).
    env['x_incentive_transaction'].search([
        ('x_move_line_id', '=', line.id),
        ('x_transaction_type', '=', 'invoice'),
    ]).write({'x_state': 'reversed'})
action = {'type': 'ir.actions.act_window_close'}

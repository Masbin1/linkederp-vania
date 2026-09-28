# Server Action : "VIF: Transaction Refund"   Model: x_incentive_transaction
# Button        : Create Credit Note / Refund (visible when type = invoice
#                 and source = invoice and state = confirmed)
# Opens the refund form pre-filled with the line's remaining refundable amount.
if record.x_transaction_type != 'invoice' or record.x_source_type != 'invoice':
    raise UserError('Only invoice transactions can be refunded here.')
refund = env['x_incentive_refund'].create({
    'x_transaction_id': record.id,
    'x_name': 'Refund %s' % (record.x_name or ''),
    'x_refund_amount': 0.0,
})
refund.write({'x_refund_amount': refund.x_refundable_amount})
action = {
    'type': 'ir.actions.act_window',
    'name': 'Refund Invoice',
    'res_model': 'x_incentive_refund',
    'view_mode': 'form',
    'res_id': refund.id,
    'target': 'new',
}

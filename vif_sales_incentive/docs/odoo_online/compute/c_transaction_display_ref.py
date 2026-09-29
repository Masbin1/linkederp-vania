# Field  : x_incentive_transaction.x_display_ref   (not stored)
# Depends: x_move_id.name, x_pos_order_id.pos_reference, x_product_id.name
for record in self:
    if record.x_source_type == 'pos':
        ref = record.x_pos_order_id.pos_reference or '-'
    else:
        ref = record.x_move_id.name or '-'
    record['x_display_ref'] = '%s / %s' % (ref, record.x_product_id.display_name or '-')

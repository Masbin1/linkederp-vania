# Field  : account.move.x_incentive_full_payment_date   (not stored)
# Depends: payment_state
# Date the invoice became FULLY paid = the last reconciliation date.
# Partial / not paid / reversed -> empty.
for record in self:
    paid_on = False
    if (record.move_type in ('out_invoice', 'out_refund')
            and record.payment_state in ('paid', 'in_payment')):
        dates = []
        for line in record.line_ids:
            if line.account_id.account_type != 'asset_receivable':
                continue
            for part in line.matched_credit_ids:
                dates.append(part.max_date)
            for part in line.matched_debit_ids:
                dates.append(part.max_date)
        paid_on = max(dates) if dates else record.invoice_date
    record['x_incentive_full_payment_date'] = paid_on

# Field  : account.move.line.x_incentive_eligible   (not stored)
# Depends: discount, is_downpayment, move_id.invoice_date
# True when the line discount is within the rule's cap. Per line, so one bad
# line does not disqualify the whole invoice. Down payments never qualify.
Rule = self.env['x_incentive_rule']
for record in self:
    move = record.move_id
    if (record.display_type != 'product' or record.is_downpayment
            or move.move_type not in ('out_invoice', 'out_refund')):
        record['x_incentive_eligible'] = False
        continue
    date_ref = move.invoice_date or datetime.date.today()
    rule = Rule.search([
        ('x_date_from', '<=', date_ref),
        '|', ('x_date_to', '=', False), ('x_date_to', '>=', date_ref),
        ('x_company_id', '=', record.company_id.id),
    ], limit=1)
    cap = rule.x_max_discount if rule else 35.0
    record['x_incentive_eligible'] = record.discount <= cap

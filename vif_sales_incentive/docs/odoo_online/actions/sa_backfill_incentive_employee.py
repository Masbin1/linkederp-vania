# Server Action : "VIF: Backfill Invoice Salesperson"   Model: x_incentive_period
# Run ONCE per period after setup (Action menu on the period), so invoices that
# existed before the automation rule get their Incentive Salesperson.
Employee = env['hr.employee']
emp_by_user = {}
count = 0
for period in records:
    moves = env['account.move'].search([
        ('move_type', 'in', ('out_invoice', 'out_refund')),
        ('invoice_date', '>=', period.x_date_start),
        ('invoice_date', '<=', period.x_date_end),
        ('x_incentive_employee_id', '=', False)])
    for move in moves:
        employee = move.pos_order_ids.employee_id[:1]
        if not employee and move.invoice_user_id:
            uid = move.invoice_user_id.id
            if uid not in emp_by_user:
                emp_by_user[uid] = Employee.search([('user_id', '=', uid)], limit=1)
            employee = emp_by_user[uid]
        if employee:
            move.write({'x_incentive_employee_id': employee.id})
            count += 1
action = {
    'type': 'ir.actions.client', 'tag': 'display_notification',
    'params': {'title': 'Backfill done',
               'message': '%s invoices got an Incentive Salesperson.' % count,
               'type': 'success', 'sticky': False},
}

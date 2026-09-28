# Automation Rule : "VIF: Invoice Incentive Salesperson"
# Model           : Journal Entry (account.move)
# Trigger         : On create and edit
#                   (When updating: Salesperson (invoice_user_id))
# Apply on        : Type in (Customer Invoice, Customer Credit Note)
# Action          : Execute Code
#
# Fills "Incentive Salesperson" with the employee behind the invoice
# salesperson -- or, for an invoice made from a POS order, the POS cashier.
# A plain field filled by this rule (not a computed field): computing a
# stored field over every existing journal entry can time out on Online.
# Anyone can still change it by hand afterwards.
Employee = env['hr.employee']
for move in records:
    if move.move_type not in ('out_invoice', 'out_refund'):
        continue
    employee = move.pos_order_ids.employee_id[:1]
    if not employee and move.invoice_user_id:
        employee = Employee.search([('user_id', '=', move.invoice_user_id.id)], limit=1)
    if employee != move.x_incentive_employee_id:
        move.write({'x_incentive_employee_id': employee.id or False})

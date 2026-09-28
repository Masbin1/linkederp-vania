# Automation Rule : "VIF: POS Invoice Cashier"
# Model           : Point of Sale Orders (pos.order)
# Trigger         : On create and edit
#                   (When updating: Invoice (account_move))
# Action          : Execute Code
#
# An invoice made from a POS order is credited to the POS CASHIER, not to the
# session user Odoo puts in the invoice's Salesperson field.
for order in records:
    if order.account_move and order.employee_id:
        if order.account_move.x_incentive_employee_id != order.employee_id:
            order.account_move.write({'x_incentive_employee_id': order.employee_id.id})

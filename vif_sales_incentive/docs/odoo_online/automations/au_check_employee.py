# Automation Rule : "VIF: Check Same-Day Handover"
# Model           : Employee (hr.employee)
# Trigger         : On create and edit
#                   (When updating: Sales Branch, Business Type,
#                    Effective Target Start, Resignation Date)
# Action          : Execute Code
# Nobody may join a team on the day a colleague leaves it: both would count
# as active that day and the team would carry one FTE too many.
for emp in records:
    if not (emp.x_incentive_branch_id and emp.x_incentive_business_type):
        continue
    others = env['hr.employee'].search([
        ('id', '!=', emp.id),
        ('x_incentive_branch_id', '=', emp.x_incentive_branch_id.id),
        ('x_incentive_business_type', '=', emp.x_incentive_business_type)])
    clash = False
    if emp.x_incentive_date_start:
        leaving = others.filtered(lambda e: e.x_incentive_date_end == emp.x_incentive_date_start)
        if leaving:
            clash = (', '.join(leaving.mapped('name')), emp.name, emp.x_incentive_date_start)
    if not clash and emp.x_incentive_date_end:
        joining = others.filtered(lambda e: e.x_incentive_date_start == emp.x_incentive_date_end)
        if joining:
            clash = (emp.name, ', '.join(joining.mapped('name')), emp.x_incentive_date_end)
    if clash:
        raise UserError(
            '%s resigns from %s / %s on %s and %s joins the same team on the same '
            'date.\n\nOne seat cannot be held by two people on the same day -- the '
            'joining date must be at least the day AFTER the resignation.'
            % (clash[0], emp.x_incentive_branch_id.x_name,
               (emp.x_incentive_business_type or '').upper(), clash[2], clash[1]))

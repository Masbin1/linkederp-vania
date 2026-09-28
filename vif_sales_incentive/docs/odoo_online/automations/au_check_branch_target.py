# Automation Rule : "VIF: Check Branch Target"
# Model           : Incentive Branch Target (x_incentive_branch_target)
# Trigger         : On create and edit
#                   (When updating: Period, Branch, Business Type)
# Action          : Execute Code
for rec in records:
    dup = env['x_incentive_branch_target'].search_count([
        ('id', '!=', rec.id),
        ('x_period_id', '=', rec.x_period_id.id),
        ('x_branch_id', '=', rec.x_branch_id.id),
        ('x_business_type', '=', rec.x_business_type)])
    if dup:
        raise UserError('One branch target per period / branch / business type.')

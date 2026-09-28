# Automation Rule : "VIF: Check Period"
# Model           : Incentive Period (x_incentive_period)
# Trigger         : On create and edit
#                   (When updating: Start Date, End Date, Company)
# Action          : Execute Code
for rec in records:
    if rec.x_date_end < rec.x_date_start:
        raise UserError('End date must be after start date.')
    overlap = env['x_incentive_period'].search_count([
        ('id', '!=', rec.id),
        ('x_company_id', '=', rec.x_company_id.id),
        ('x_date_start', '<=', rec.x_date_end),
        ('x_date_end', '>=', rec.x_date_start)])
    if overlap:
        raise UserError('Period %s overlaps another incentive period.' % rec.x_name)

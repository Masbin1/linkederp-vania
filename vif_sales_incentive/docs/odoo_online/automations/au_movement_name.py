# Automation Rule : "VIF: Target Movement Reference"
# Model           : Incentive Target Movement (x_incentive_target_movement)
# Trigger         : On create
# Action          : Execute Code
# Needs a sequence with code x_incentive_target_movement (prefix TMV/%(year)s/).
for rec in records:
    if not rec.x_name or rec.x_name == 'New':
        rec.write({'x_name': env['ir.sequence'].next_by_code('x_incentive_target_movement') or 'New'})

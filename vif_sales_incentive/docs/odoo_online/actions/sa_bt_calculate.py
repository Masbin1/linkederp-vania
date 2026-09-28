# Server Action : "VIF: Branch Target Calculate"   Model: x_incentive_branch_target
# Button        : Calculate (visible when state = draft or calculated)
# Runs the engine for THIS branch x business type only.
engine = env['ir.actions.server'].search(
    [('name', '=', 'VIF: Engine Calculate')], limit=1)
if not engine:
    raise UserError('Server action "VIF: Engine Calculate" not found.')
for rec in records:
    if rec.x_period_id.x_state == 'draft':
        raise UserError('Open period %s before calculating a branch.'
                        % rec.x_period_id.x_name)
    engine.with_context(
        active_model='x_incentive_period',
        active_id=rec.x_period_id.id,
        active_ids=[rec.x_period_id.id],
        vif_branch_target_id=rec.id,
    ).run()

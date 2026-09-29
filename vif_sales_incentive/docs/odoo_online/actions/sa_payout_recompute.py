# Server Action : "VIF: Payout Recompute"   Model: x_incentive_payout
# Button        : Recompute (visible when not frozen)
# Port of incentive.payout.action_recompute: re-runs THIS employee's
# individual stream (tier, eligible base, paid base) on the current
# transactions. Does not regenerate transactions or touch the branch stream.
engine = env['ir.actions.server'].search(
    [('name', '=', 'VIF: Engine Calculate')], limit=1)
if not engine:
    raise UserError('Server action "VIF: Engine Calculate" not found.')
for rec in records:
    engine.with_context(
        active_model='x_incentive_period',
        active_id=rec.x_period_id.id,
        active_ids=[rec.x_period_id.id],
        vif_recompute_payout_id=rec.id,
    ).run()

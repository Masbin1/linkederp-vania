# Automation Rule : "VIF: Check Tier Ranges"
# Model           : Incentive Tier (x_incentive_rule_tier)
# Trigger         : On create and edit
#                   (When updating: Achievement From, Achievement To, Rule)
# Action          : Execute Code
for rule in records.mapped('x_rule_id'):
    tiers = rule.x_tier_ids.sorted('x_achievement_min')
    for i in range(1, len(tiers)):
        prev = tiers[i - 1]
        curr = tiers[i]
        if prev.x_achievement_max > curr.x_achievement_min:
            raise UserError('Tier ranges overlap: %s ends at %s but %s starts at %s.'
                            % (prev.x_name, prev.x_achievement_max,
                               curr.x_name, curr.x_achievement_min))

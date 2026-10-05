# Automation Rule : "VIF: POS Journal Analytic Tags"
# Model           : Point of Sale Orders (pos.order)
# Trigger         : On create and edit
#                   (When updating: Invoice (account_move))
# Action          : Execute Code
#
# Not part of the Sales Incentive engine -- this just fixes the gap shown in
# the client's screenshots: a Journal Entry created from a Sales Order gets
# its Analytic Distribution (Project / Branch / Business Type) filled in
# manually, but a Journal Entry created from a POS order never does. This
# rule copies the same 3 tags onto every journal item of the POS invoice:
#   - Project       = N/A          (fixed)
#   - Branch        = whatever the invoice's own "Branch" field already
#                      says (so it matches the PoS the order was rung up at)
#   - Business Type = B2C          (fixed -- POS sales are always retail)
# Only lines with NO analytic distribution yet are touched, so a line a
# human already tagged by hand is never overwritten.
#
# TESTED against vaniaeut_online (copy of the client DB, same one used for
# vif_sales_incentive -- see README.md section 13) via `odoo-bin shell`,
# 2026-10-02: ran this exact code against pos.order id 3 (account_move
# 59249, Branch "Center"), confirmed all 5 previously-untagged lines got
# analytic_distribution {'56,3,8': 100.0} (Project N/A=56, Branch Center=3,
# Business Type B2C=8), then rolled back. Fields below are the CONFIRMED
# values for that database -- re-check them if this runs anywhere else:
#   - x_studio_branch on account.move is a Selection field (values
#     "Bali"/"Bandung"/"Center"/"Medan"/"Surabaya"/"Jakarta"), NOT a
#     Many2one -- its value is already the plain branch name string.
#   - Analytic Plans "Project" (id 1), "Branch" (id 2), "Business Type"
#     (id 3) exist with accounts "N/A" (id 56), "Center" (id 3)/"Jakarta"
#     (id 6)/etc., "B2C" (id 8) respectively.
BRANCH_FIELD = 'x_studio_branch'
PROJECT_PLAN, PROJECT_ACCOUNT = 'Project', 'N/A'
BUSINESS_TYPE_PLAN, BUSINESS_TYPE_ACCOUNT = 'Business Type', 'B2C'
BRANCH_PLAN = 'Branch'

AnalyticAccount = env['account.analytic.account']
AnalyticPlan = env['account.analytic.plan']

def analytic_account_id(plan_name, account_name):
    plan = AnalyticPlan.search([('name', '=', plan_name)], limit=1)
    if not plan:
        raise UserError("Analytic Plan '%s' not found." % plan_name)
    acc = AnalyticAccount.search([
        ('plan_id', '=', plan.id), ('name', '=', account_name)], limit=1)
    if not acc:
        raise UserError("Analytic Account '%s' not found in plan '%s'."
                        % (account_name, plan_name))
    return acc.id

project_id = analytic_account_id(PROJECT_PLAN, PROJECT_ACCOUNT)
business_type_id = analytic_account_id(BUSINESS_TYPE_PLAN, BUSINESS_TYPE_ACCOUNT)
branch_cache = {}

for order in records:
    move = order.account_move
    if not move:
        continue
    branch_name = move[BRANCH_FIELD]
    if not branch_name:
        continue
    if branch_name not in branch_cache:
        branch_cache[branch_name] = analytic_account_id(BRANCH_PLAN, branch_name)
    branch_id = branch_cache[branch_name]
    key = '%s,%s,%s' % (project_id, branch_id, business_type_id)
    for line in move.line_ids:
        if not line.analytic_distribution:
            line.write({'analytic_distribution': {key: 100.0}})

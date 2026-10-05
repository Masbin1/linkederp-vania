/**
 * Project Profitability - "Expense by Journal Entry" cost row.
 *
 * Manual journal entries are never counted natively: the native query filters
 * analytic lines by project_id, which JE lines do not carry. This adds them as
 * their own row and ADDS the amount to the costs total.
 *
 * The rows that go MISSING for low-access users are not fixed here and cannot
 * be: every RPC runs as the logged-in user and the server enforces access, so
 * a browser query cannot recover a row the server withheld. That is what
 * security/profitability_access.xml is for - read its header before installing.
 */

import { patch } from "@web/core/utils/patch";
import { ProjectRightSidePanel } from "@project/components/project_right_side_panel/project_right_side_panel";

// ------------------------------------------------------------------ CONFIG --
const JE_ROW_ID = "je_manual_entries";
const JE_LABEL = "Expense by Journal Entry";
const JE_SEQUENCE_HINT = 16;                        // native uses 10, 11, 13, 14, 15
const DRILLDOWN_MODEL = "account.move";             // "account.move" or "account.move.line"
const EXPENSE_FLAG_FIELD = "x_studio_is_expense";   // Studio boolean on account.move.line
// ---------------------------------------------------------------------------

patch(ProjectRightSidePanel.prototype, {
    async loadData() {
        const result = await super.loadData(...arguments);
        try {
            await this._addJournalEntryRow();
        } catch (error) {
            console.warn("[project_profit_je_line] skipped:", error);
        }
        return result;
    },

    onProjectActionClick(params) {
        if (params && params.type === "ir.actions.act_window") {
            return this.actionService.doAction(params);
        }
        return super.onProjectActionClick(params);
    },

    async _addJournalEntryRow() {
        const data = this.state.data;
        if (!this.projectId || !data?.profitability_items?.costs) {
            return;
        }

        const [project] = await this.orm.read("project.project", [this.projectId], ["account_id"]);
        const analyticId = project?.account_id?.[0];
        if (!analyticId) {
            return; // no analytic account: nothing can be booked on this project
        }

        // Amount from analytic lines (signed, negative = cost) and the moves to
        // drill into. Throws for users without the grants -> caller logs, no row.
        const [aaLines, moveLines] = await Promise.all([
            this.orm.searchRead("account.analytic.line", [
                ["account_id", "in", [analyticId]],
                ["move_line_id.move_id.move_type", "=", "entry"],
                ["move_line_id.move_id.state", "=", "posted"],
                ["move_line_id." + EXPENSE_FLAG_FIELD, "=", true],
            ], ["amount"]),
            this.orm.searchRead("account.move.line", [
                ["analytic_distribution", "in", [analyticId]],
                ["move_id.move_type", "=", "entry"],
                ["move_id.state", "=", "posted"],
                [EXPENSE_FLAG_FIELD, "=", true],
            ], ["move_id"]).catch(() => []),   // drill-down is optional, the amount is not
        ]);

        const jeAmount = aaLines.reduce((sum, l) => sum + (l.amount || 0), 0);
        if (!jeAmount) {
            return;
        }

        const costs = data.profitability_items.costs;
        costs.total = costs.total || { billed: 0, to_bill: 0 };

        // Idempotent: loadData can run twice on the same state.
        let row = costs.data.find((r) => r.id === JE_ROW_ID);
        if (!row) {
            row = { id: JE_ROW_ID, sequence: JE_SEQUENCE_HINT, billed: 0, to_bill: 0 };
            costs.data.push(row);
        }
        costs.total.billed = (costs.total.billed || 0) + jeAmount - row.billed;
        row.billed = jeAmount;

        const action = this._jeAction(moveLines);
        if (action) {
            row.action = action;
        } else {
            delete row.action;
        }
        data.profitability_labels = { ...(data.profitability_labels || {}), [JE_ROW_ID]: JE_LABEL };
    },

    _jeAction(moveLines) {
        const ids = DRILLDOWN_MODEL === "account.move.line"
            ? moveLines.map((l) => l.id)
            : [...new Set(moveLines.map((l) => l.move_id?.[0]).filter(Boolean))];
        if (!ids.length) {
            return null;
        }
        return {
            type: "ir.actions.act_window",
            name: JE_LABEL,
            res_model: DRILLDOWN_MODEL,
            domain: [["id", "in", ids]],
            views: [[false, "list"], [false, "form"]],
            target: "current",
        };
    },
});

/**
 * Self-check for the JE row arithmetic. No framework, no Odoo:
 *   node static/tests/je_row_check.mjs
 * Loads the real patch file with the @web/@project imports stubbed, captures
 * the patch spec, and drives _addJournalEntryRow against a fake ORM.
 */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { SourceTextModule, SyntheticModule } from "node:vm";
import { fileURLToPath } from "node:url";

const SRC = fileURLToPath(new URL("../src/js/profitability_je_patch.js", import.meta.url));

let spec;
const stubs = {
    "@web/core/utils/patch": { patch: (_proto, s) => (spec = s) },
    "@project/components/project_right_side_panel/project_right_side_panel": {
        ProjectRightSidePanel: { prototype: {} },
    },
};
const mod = new SourceTextModule(readFileSync(SRC, "utf8"), { identifier: SRC });
await mod.link((specifier) => {
    const exports = stubs[specifier];
    assert.ok(exports, `unexpected import: ${specifier}`);
    return new SyntheticModule(Object.keys(exports), function () {
        for (const [k, v] of Object.entries(exports)) this.setExport(k, v);
    });
});
await mod.evaluate();
assert.ok(spec?._addJournalEntryRow, "patch spec not captured");

// --- fake component -------------------------------------------------------
const component = ({ analyticId = 7, aaLines = [], moveLines = [], costs }) =>
    Object.assign(Object.create(spec), {
        projectId: 1,
        state: { data: { profitability_items: { costs } } },
        orm: {
            read: async () => [{ account_id: analyticId ? [analyticId, "AA"] : false }],
            searchRead: async (model) =>
                model === "account.analytic.line" ? aaLines : moveLines,
        },
    });
const emptyCosts = () => ({ data: [], total: { billed: 0, to_bill: 0 } });
const jeRow = (costs) => costs.data.find((r) => r.id === "je_manual_entries");

// 1. amount lands on its own row AND is added to the total
{
    const costs = emptyCosts();
    costs.data.push({ id: "other", billed: -100 });
    costs.total.billed = -100;
    await component({ aaLines: [{ amount: -30 }, { amount: -20 }], costs })._addJournalEntryRow();
    assert.equal(jeRow(costs).billed, -50);
    assert.equal(costs.total.billed, -150, "JE amount must be ADDED, native never counts it");
}

// 2. idempotent: loadData can run twice on the same state
{
    const costs = emptyCosts();
    const c = component({ aaLines: [{ amount: -50 }], costs });
    await c._addJournalEntryRow();
    await c._addJournalEntryRow();
    assert.equal(costs.data.filter((r) => r.id === "je_manual_entries").length, 1);
    assert.equal(costs.total.billed, -50, "second run must not double-count");
}

// 3. amount changed between runs -> total follows the delta, not the sum
{
    const costs = emptyCosts();
    await component({ aaLines: [{ amount: -50 }], costs })._addJournalEntryRow();
    await component({ aaLines: [{ amount: -80 }], costs })._addJournalEntryRow();
    assert.equal(jeRow(costs).billed, -80);
    assert.equal(costs.total.billed, -80);
}

// 4. nothing to show -> no row at all
for (const args of [{ analyticId: 0 }, { aaLines: [] }, { aaLines: [{ amount: 0 }] }]) {
    const costs = emptyCosts();
    await component({ ...args, costs })._addJournalEntryRow();
    assert.equal(costs.data.length, 0, `row added for ${JSON.stringify(args)}`);
    assert.equal(costs.total.billed, 0);
}

// 5. no readable moves -> row stays, just not clickable
{
    const costs = emptyCosts();
    await component({ aaLines: [{ amount: -50 }], moveLines: [], costs })._addJournalEntryRow();
    assert.equal(jeRow(costs).billed, -50);
    assert.equal(jeRow(costs).action, undefined, "amount must survive without drill-down");
}

// 6. drill-down targets distinct moves
{
    const costs = emptyCosts();
    const moveLines = [{ id: 1, move_id: [9, "JE/1"] }, { id: 2, move_id: [9, "JE/1"] }, { id: 3, move_id: [11, "JE/2"] }];
    await component({ aaLines: [{ amount: -50 }], moveLines, costs })._addJournalEntryRow();
    assert.deepEqual(jeRow(costs).action.domain, [["id", "in", [9, 11]]]);
    assert.equal(jeRow(costs).action.res_model, "account.move");
}

console.log("je_row_check: all ok");

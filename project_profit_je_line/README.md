# Project Profitability — Journal Entries Line

Two things, independent of each other:

1. **Every row shows for every project user.** Odoo builds the panel with the
   current user's rights, so a row whose model the user cannot read is dropped
   silently — and the total shrinks with it. Fixed with XML security data.
2. **"Expense by Journal Entry"** cost row for manual journal entries
   (`move_type = "entry"`, posted) flagged `x_studio_is_expense` and booked on
   the project's analytic account. Native never counts these, so the amount is
   ADDED to the costs total.

XML and JS only. No Python business logic, no model overridden, no server
method patched. (`__manifest__.py` is a manifest, not code — Odoo has no other
format for it.)

## Why the missing rows need XML, not JS

Every RPC from the browser runs as the logged-in user and the server enforces
access. There is no sudo in the browser, so no JS can recover a row the server
withheld. The read has to actually be granted.

Scanning the `_get_*profitability*` methods across `odoo/addons` and
`enterprise`, exactly **one** model is read without `sudo()`: `hr.expense`
(in `project_hr_expense` and `project_sale_expense`). Everything else already
sudoes. That single gap is what hides the Expenses row.

It is **not** only about users without accounting. Measured on 19.0, same
project:

| user | costs rows |
|---|---|
| admin | `{'expenses': -304.35}` |
| `account.group_account_readonly` | `{}` |

The row needs `hr_expense.group_hr_expense_team_approver`, which an
accounting-readonly user does not have either.

## Read this before installing

`security/profitability_access.xml` grants `project.group_project_user`:

| model | why | delete it and… |
|---|---|---|
| `hr.expense` | the native Expenses row | that row goes missing again |
| `account.analytic.line` | the JE row's amount | JE row disappears |
| `account.move.line`, `account.move` | the JE row's drill-down | JE row shows, not clickable |

All **read only** — never write, create or unlink — and every grant is paired
with a record rule limiting rows to those carrying a project's analytic
account. Verified on a clean 19.0 DB:

```
admin rows : ({'expenses': -304.35}, -304.35)
plain rows : ({'expenses': -304.35}, -304.35)
plain JE amount : -300.0        plain can read that move : True
LEAK private lunch : False      LEAK non-project journal items : 0
```

**It is still a real widening.** A project user can open the expenses and
journal items booked against *any* project, not just their own — not only see
the totals. That is the price of showing them every row without server-side
code. If it is not acceptable, do not install.

The file is `noupdate="1"` and each grant is its own record, so deleting the
ones you do not want survives module upgrades.

## Install

1. Zip `project_profit_je_line/` (or upload the folder if your instance takes one).
2. Apps → (Developer Mode) → Update Apps List → search the module → Install.
3. Hard-refresh (Ctrl/Cmd + Shift + R) so the asset loads.

## Configure the JE row

**Studio → `account.move.line`** → add boolean `x_studio_is_expense`, tick it on
the JE lines you want counted. Without the field the JE row simply never
appears; the access fix above is unaffected.

Change `JE_LABEL`, `JE_SEQUENCE_HINT` (row order; native uses 10, 11, 13, 14, 15)
or `DRILLDOWN_MODEL` in the CONFIG block of
`static/src/js/profitability_je_patch.js`.

## Limits

- A journal entry counts **only if** it has an analytic distribution to the
  project's analytic account. Pure GL entries cannot be tied to a project.
- Posted entries only.
- Figures are live — no cron, no snapshot, no stale data.
- Re-test after an Odoo upgrade: this re-shapes server data in the client.
  `node static/tests/je_row_check.mjs` covers the row arithmetic (added to the
  total, idempotent, delta on re-run, no row when empty, amount survives
  without drill-down, distinct move ids).

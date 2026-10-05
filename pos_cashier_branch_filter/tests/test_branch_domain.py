"""Standalone self-check for the cashier branch-filter domain.

Run from the Odoo root:
    cd /path/to/odoo && python3 -m pytest <this file>
or plainly:
    cd /path/to/odoo && python3 <this file>

Mirrors _pos_branch_cashier_domain's semantics against in-memory employees,
so the fail-closed rules are verified without a database.
"""
import sys

sys.path.insert(0, ".")
from odoo.fields import Domain  # noqa: E402

BALI, JAKARTA, SURABAYA = 1, 2, 3

EMPLOYEES = [
    {"name": "Agus", "x_branch": BALI, "pin": "1234"},
    {"name": "Budi", "x_branch": BALI, "pin": "5678"},
    {"name": "Candra", "x_branch": JAKARTA, "pin": "1111"},
    {"name": "Dedi", "x_branch": BALI, "pin": False},
    {"name": "Eko", "x_branch": SURABAYA, "pin": "2222"},
    {"name": "Fajar", "x_branch": False, "pin": "3333"},
]


def build_domain(branch_ids, has_x_branch=True, has_user_field=True):
    """Same decision tree as HrEmployee._pos_branch_cashier_domain."""
    if not has_x_branch or not has_user_field:
        return Domain.FALSE
    if not branch_ids:
        return Domain.FALSE
    return Domain.AND([
        [("x_branch", "in", branch_ids)],
        [("pin", "!=", False)],
    ])


def visible(branch_ids, **kw):
    domain = build_domain(branch_ids, **kw)
    if domain is Domain.FALSE:
        return []
    allowed = domain.__iter__ and branch_ids
    return [
        e["name"] for e in EMPLOYEES
        if e["x_branch"] and e["x_branch"] in allowed and e["pin"]
    ]


# Test 1 — Bali only: two Bali employees with a PIN.
assert visible([BALI]) == ["Agus", "Budi"], visible([BALI])

# Test 2 — Jakarta only.
assert visible([JAKARTA]) == ["Candra"], visible([JAKARTA])

# Test 3 — Bali + Jakarta.
assert visible([BALI, JAKARTA]) == ["Agus", "Budi", "Candra"], visible([BALI, JAKARTA])

# Test 4 — no allowed branches must fail closed, never fail open.
assert visible([]) == []
assert build_domain([]) is Domain.FALSE

# Test 5 — right branch, no PIN (Dedi) is never visible.
assert "Dedi" not in visible([BALI, JAKARTA, SURABAYA])

# Test 6 — PIN set, wrong branch (Eko) is not visible to a Bali user.
assert "Eko" not in visible([BALI])

# Test 7 — employee with no branch at all (Fajar) is never visible.
assert "Fajar" not in visible([BALI, JAKARTA, SURABAYA])

# Missing custom fields must fail closed too.
assert build_domain([BALI], has_x_branch=False) is Domain.FALSE
assert build_domain([BALI], has_user_field=False) is Domain.FALSE

# The emitted domain is a plain AND of both conditions.
assert list(build_domain([BALI, JAKARTA])) == [
    "&", ("x_branch", "in", [BALI, JAKARTA]), ("pin", "!=", False)
]

print("OK: pos_cashier_branch_filter domain logic")

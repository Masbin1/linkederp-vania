{
    "name": "POS Branch Modification",
    "version": "19.0.1.0.0",
    "category": "Point of Sale",
    "summary": "Restrict the POS 'Select Cashier' list to employees of the CURRENTLY LOGGED-IN Odoo user's allowed branches, with a PIN set",
    "description": """
POS Cashier Filtering by Logged-in User Allowed Branch
========================================================

The "Select Cashier" screen in POS only shows employees who:

1. Belong to one of the branches allowed for the Odoo user who is
   *currently logged in and loading the POS* (res.users field
   x_studio_many2many_field_51u_1je2hqiji), not the user who opened
   the POS session.
2. Have a PIN configured on their Employee record.

If the logged-in user has no allowed branches, the cashier list is
empty (fails closed, never falls back to showing everyone).
""",
    "depends": ["pos_hr"],
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}

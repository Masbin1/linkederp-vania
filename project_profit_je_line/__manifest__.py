{
    "name": "Project Profitability - Journal Entries Line",
    "summary": "Show manual journal-entry costs as their own line in the Project "
               "Profitability panel, and grant project users the reads the panel "
               "needs so no row silently disappears.",
    "version": "19.0.1.1.0",
    "category": "Services/Project",
    "license": "LGPL-3",
    "depends": ["project_account", "project_hr_expense"],
    "data": [
        "security/profitability_access.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "project_profit_je_line/static/src/js/profitability_je_patch.js",
        ],
    },
    "installable": True,
    "application": False,
}

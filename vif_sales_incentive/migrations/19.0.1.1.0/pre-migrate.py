# -*- coding: utf-8 -*-
from odoo.tools.sql import column_exists, rename_column


def migrate(cr, version):
    if column_exists(cr, 'incentive_branch', 'ideal_team_size'):
        rename_column(cr, 'incentive_branch', 'ideal_team_size', 'ideal_team_size_b2b')
    if not column_exists(cr, 'incentive_branch', 'ideal_team_size_b2c'):
        cr.execute(
            "ALTER TABLE incentive_branch "
            "ADD COLUMN ideal_team_size_b2c INTEGER DEFAULT 0"
        )

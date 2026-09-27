# -*- coding: utf-8 -*-
from odoo import models

# (role, user field, share field). The Salesperson 2/3 slots and every share
# field are Odoo Studio fields living only in the client database, so each is
# read defensively: a database without them simply sees PM-only projects.
# Shares are fractions (0.5 == 50%), as the Studio percentage widget stores.
PROJECT_SPLIT_SLOTS = [
    ('pm', 'user_id', 'x_studio_komisi_pm'),
    ('sp2', 'x_studio_salesperson_2', 'x_studio_komisi_salesperson_2'),
    ('sp3', 'x_studio_salesperson_3', 'x_studio_komisi_salesperson_3'),
]


class ProjectProject(models.Model):
    _inherit = 'project.project'

    def _incentive_split(self):
        """Who gets the credit for a sale on this project, and how much.

        Returns ``[(employee, share, role), ...]`` with shares summing to 1,
        or an empty list when nobody on the project maps to an employee (the
        caller then falls back to the invoice salesperson).

        The SO salesperson is deliberately NOT part of this: a salesperson who
        is not on the project earns nothing from it.

          * all shares empty/0       -> PM takes 100%
          * a share with no person   -> that share goes to the PM
            (or a person without an employee record)
          * shares under 100%        -> the remainder goes to the PM
          * shares over 100%         -> scaled down proportionally
          * one person in two slots  -> their shares are added up
        """
        self.ensure_one()
        Employee = self.env['hr.employee']

        def employee_of(user):
            if not user:
                return Employee
            return Employee.search([('user_id', '=', user.id)], limit=1)

        pm = employee_of(self.user_id)
        shares = {}   # employee -> [share, role]
        orphan = 0.0
        for role, user_field, share_field in PROJECT_SPLIT_SLOTS:
            share = self[share_field] if share_field in self._fields else 0.0
            if not share or share <= 0:
                continue
            user = self[user_field] if user_field in self._fields else False
            employee = employee_of(user)
            if not employee:
                orphan += share
                continue
            shares.setdefault(employee, [0.0, role])[0] += share

        if not shares and not orphan:
            return [(pm, 1.0, 'pm')] if pm else []

        orphan += max(1.0 - sum(s for s, _r in shares.values()) - orphan, 0.0)
        if orphan and pm:
            shares.setdefault(pm, [0.0, 'pm'])[0] += orphan

        total = sum(s for s, _r in shares.values())
        if total <= 0:
            return []
        return [(employee, share / total, role)
                for employee, (share, role) in shares.items()]

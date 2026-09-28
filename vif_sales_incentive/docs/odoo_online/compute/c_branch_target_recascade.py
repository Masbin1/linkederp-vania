# Field  : x_incentive_branch_target.x_recascade_reason   (not stored)
# Depends: x_state, x_period_id, x_branch_id, x_business_type
#
# Has the team changed since the targets were cascaded? Somebody's working
# days moved (resignation / join date entered) or a new person has no target
# row yet. The Calculate buttons refuse to run while this is set.


def proration(emp, p):
    start = max(emp.x_incentive_date_start or p.x_date_start, p.x_date_start)
    end = min(emp.x_incentive_date_end or p.x_date_end, p.x_date_end)
    if end < start:
        return 0.0
    total = (p.x_date_end - p.x_date_start).days + 1
    return ((end - start).days + 1) / total


Target = self.env['x_incentive_target']
Employee = self.env['hr.employee']
for record in self:
    reason = False
    p = record.x_period_id
    if record.x_state != 'locked' and p and record.x_branch_id:
        targets = Target.search([
            ('x_period_id', '=', p.id),
            ('x_branch_id', '=', record.x_branch_id.id),
            ('x_business_type', '=', record.x_business_type),
            ('x_target_type', '=', 'incentive'),
        ])
        if targets:
            stale = []
            for t in targets:
                if abs(t.x_proration_ratio - proration(t.x_employee_id, p)) > 0.0001:
                    stale.append(t.x_employee_id.name)
            if stale:
                reason = 'Working days changed for: %s' % ', '.join(stale)
            else:
                covered = targets.mapped('x_employee_id')
                team = Employee.search([
                    ('x_incentive_branch_id', '=', record.x_branch_id.id),
                    ('x_incentive_business_type', '=', record.x_business_type),
                ])
                joined = []
                for e in team:
                    if (e not in covered and not e.x_is_vacant_slot
                            and e.x_incentive_designation_id.x_fte_individual
                            and proration(e, p)):
                        joined.append(e.name)
                if joined:
                    reason = 'No target yet for: %s' % ', '.join(joined)
    record['x_recascade_reason'] = reason

# Field  : x_incentive_branch.x_employee_count   (not stored)
# Depends: x_employee_ids
for record in self:
    record['x_employee_count'] = len(record.x_employee_ids)

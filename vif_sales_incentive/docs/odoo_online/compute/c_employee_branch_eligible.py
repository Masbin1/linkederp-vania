# Field  : hr.employee.x_branch_incentive_eligible   (stored, editable)
# Depends: x_incentive_designation_id
for record in self:
    desig = record.x_incentive_designation_id
    record['x_branch_incentive_eligible'] = bool(desig and desig.x_branch_eligible)

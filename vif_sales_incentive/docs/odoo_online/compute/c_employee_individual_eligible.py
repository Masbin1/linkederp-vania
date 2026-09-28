# Field  : hr.employee.x_individual_incentive_eligible   (stored, editable)
# Depends: x_incentive_designation_id
for record in self:
    desig = record.x_incentive_designation_id
    record['x_individual_incentive_eligible'] = bool(desig and desig.x_individual_eligible)

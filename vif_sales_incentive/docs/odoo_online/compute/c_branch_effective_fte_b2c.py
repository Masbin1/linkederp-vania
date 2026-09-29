# Field  : x_incentive_branch.x_effective_fte_b2c   (not stored)
# Depends: x_employee_ids.x_incentive_business_type, x_employee_ids.x_incentive_designation_id
# Today's weighted head-count (branch FTE) of the B2C team. Form display only --
# the cascade builds its own population per period.
today = datetime.date.today()
for record in self:
    total = 0.0
    for emp in record.x_employee_ids:
        if emp.x_incentive_business_type != 'b2c' or emp.x_is_vacant_slot:
            continue
        if emp.x_incentive_date_start and today < emp.x_incentive_date_start:
            continue
        if emp.x_incentive_date_end and today > emp.x_incentive_date_end:
            continue
        total += emp.x_incentive_designation_id.x_fte_branch
    record['x_effective_fte_b2c'] = total

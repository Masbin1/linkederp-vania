# Field  : x_incentive_period.x_transaction_count   (not stored)
# Depends: x_transaction_ids
for record in self:
    record['x_transaction_count'] = len(record.x_transaction_ids)

data_sorted = data_clean.sort_values(['user_id', 'timestamp'])
first_5 = data_sorted.groupby('user_id').head(5)
first_5['event_rank'] = first_5.groupby('user_id').cumcount() + 1


first_5_power   = first_5[first_5['user_id'].isin(power_users['user_id'])]
first_5_churned = first_5[~first_5['user_id'].isin(power_users['user_id'])]


print("Power users - most common event at each position")
print(first_5_power.groupby('event_rank')['event'].agg(lambda x: x.value_counts().index[0]))

print("Churned users - most common event at each position")
print(first_5_churned.groupby('event_rank')['event'].agg(lambda x: x.value_counts().index[0]))
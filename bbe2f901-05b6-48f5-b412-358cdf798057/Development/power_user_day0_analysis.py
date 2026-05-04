data_clean['is_power_user'] = data_clean['user_id'].isin(power_users['user_id'])

first_seen = data_clean.groupby('user_id')['timestamp'].min().rename('first_seen')
data_clean = data_clean.join(first_seen, on='user_id')
data_clean['days_since_signup'] = (data_clean['timestamp'] - data_clean['first_seen']).dt.days

day0_power = data_clean[(data_clean['is_power_user']) & (data_clean['days_since_signup'] == 0)]

print("What power users did on Day 0")
print(day0_power['event'].value_counts().head(15))
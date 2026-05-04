day0_bucket_map = user_stats.set_index('user_id')['day0_bucket']
data_clean['day0_bucket'] = data_clean['user_id'].map(day0_bucket_map)

low = data_clean[data_clean['day0_bucket'] == '1']
high = data_clean[data_clean['day0_bucket'] == '21-50']

print("Top events - Low engagement (1 event on Day 0)")
print(low['event'].value_counts().head(10))
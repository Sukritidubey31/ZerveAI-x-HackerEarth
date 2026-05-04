import pandas as pd

user_stats['is_power_user'] = user_stats['lifespan_days'] >= 30

day0_counts = data_clean[data_clean['days_since_signup'] == 0].groupby('user_id').size().rename('day0_events')
user_stats = user_stats.join(day0_counts, on='user_id')

bins = [0, 1, 3, 5, 10, 20, 50, 999]
labels = ['1', '2-3', '4-5', '6-10', '11-20', '21-50', '50+']

user_stats['day0_bucket'] = pd.cut(user_stats['day0_events'], bins=bins, labels=labels)

print("Retention rate by Day 0 event count")
retention = user_stats.groupby('day0_bucket', observed=True)['is_power_user'].agg(['mean', 'count'])
retention['mean'] = (retention['mean'] * 100).round(1)
retention.columns = ['retention_%', 'user_count']
print(retention)
event_counts = data_clean.groupby('user_id').size().rename('total_events_all')
user_stats_aha = user_stats.join(event_counts, on='user_id')

thresholds = [1, 3, 5, 10, 15, 20, 30, 50, 100]

print("If a user reaches N total events, % who become power users")
for n in thresholds:
    users_reached = user_stats_aha[user_stats_aha['total_events_all'] >= n]
    pct = users_reached['is_power_user'].mean() * 100
    count = len(users_reached)
    print(f"  {n:>4} events → {pct:>5.1f}% retained  ({count} users)")
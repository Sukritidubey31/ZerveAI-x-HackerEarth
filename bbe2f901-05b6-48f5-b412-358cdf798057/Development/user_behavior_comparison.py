import pandas as pd

everyone_else = user_stats[user_stats['lifespan_days'] < 30]

print("Behavior comparison between power users vs rest of the users")
comparison = pd.DataFrame({
    'power_users_%'  : (power_users[flag_cols].mean() * 100).round(1),
    'everyone_else_%': (everyone_else[flag_cols].mean() * 100).round(1)
})
comparison['difference'] = (comparison['power_users_%'] - comparison['everyone_else_%']).round(1)
print(comparison.sort_values('difference', ascending=False))
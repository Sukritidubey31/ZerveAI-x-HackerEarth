power_users = user_stats[user_stats['lifespan_days'] >= 30]

print("Power users i.e users for 30+ days")
print(len(power_users))
print("What they did")
flag_cols = [
    'completed_onboarding', 'skipped_onboarding', 'tour_finished',
    'ran_block', 'created_block', 'created_canvas', 'created_edge',
    'uploaded_files', 'used_agent', 'used_agent_start',
    'published_app', 'shared_canvas', 'scheduled_job', 'bought_addon_credits'
]
print((power_users[flag_cols].mean() * 100).round(1).sort_values(ascending=False))
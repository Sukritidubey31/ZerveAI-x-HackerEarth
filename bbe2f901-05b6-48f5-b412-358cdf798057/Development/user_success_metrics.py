user_stats['is_successful'] = (
    (user_stats['lifespan_days'] >= 7) &
    (
        user_stats['ran_block'] |
        user_stats['created_canvas'] |
        user_stats['used_agent_start'] |
        user_stats['published_app'] |
        user_stats['scheduled_job'] |
        user_stats['bought_addon_credits']
    )
).astype(int)

print(user_stats['is_successful'].value_counts())
print(f"Success rate: {user_stats['is_successful'].mean()*100:.1f}%")
agent_events = [
    'agent_tool_call_create_block_tool', 'agent_tool_call_run_block_tool',
    'agent_tool_call_get_block_tool', 'agent_tool_call_refactor_block_tool',
    'agent_tool_call_finish_ticket_tool', 'agent_worker_created'
]

manual_events = [
    'run_block', 'block_create', 'block_resize', 'block_delete',
    'canvas_create', 'edge_create', 'files_upload', 'fullscreen_open'
]

user_agent_counts  = data_clean[data_clean['event'].isin(agent_events)].groupby('user_id').size().rename('agent_actions')
user_manual_counts = data_clean[data_clean['event'].isin(manual_events)].groupby('user_id').size().rename('manual_actions')

user_stats = user_stats.join(user_agent_counts, on='user_id').join(user_manual_counts, on='user_id')
user_stats['agent_actions']  = user_stats['agent_actions'].fillna(0)
user_stats['manual_actions'] = user_stats['manual_actions'].fillna(0)
user_stats['manual_ratio']   = user_stats['manual_actions'] / (user_stats['agent_actions'] + user_stats['manual_actions'] + 1)

print("Average manual ratio")
print("Power users")
print(round(user_stats[user_stats['is_power_user']]['manual_ratio'].mean(), 3))
print("Churned users")
print(round(user_stats[~user_stats['is_power_user']]['manual_ratio'].mean(), 3))
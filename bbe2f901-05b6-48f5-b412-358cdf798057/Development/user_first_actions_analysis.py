system_events = [
    'credits_used', 'agent_worker_created', 'sign_in', 'sign_up',
    'new_user_created', 'credits_below_1', 'credits_below_2',
    'credits_below_3', 'credits_below_4', 'credits_exceeded',
    'addon_credits_used', 'agent_tool_call_create_block_tool',
    'agent_tool_call_run_block_tool', 'agent_tool_call_get_block_tool',
    'agent_tool_call_get_canvas_summary_tool',
    'agent_tool_call_get_variable_preview_tool',
    'agent_tool_call_finish_ticket_tool',
    'agent_tool_call_refactor_block_tool',
    'agent_tool_call_delete_block_tool',
    'agent_tool_call_create_edges_tool',
    'agent_block_created', 'agent_block_run'
]

meaningful = data_clean[~data_clean['event'].isin(system_events)]
meaningful_sorted = meaningful.sort_values(['user_id', 'timestamp'])

first_5_meaningful = meaningful_sorted.groupby('user_id').head(5)
first_5_meaningful['event_rank'] = first_5_meaningful.groupby('user_id').cumcount() + 1

first_5_power   = first_5_meaningful[first_5_meaningful['user_id'].isin(power_users['user_id'])]
first_5_churned = first_5_meaningful[~first_5_meaningful['user_id'].isin(power_users['user_id'])]

print("Power users - first 5 meaningful actions")
print(first_5_power.groupby('event_rank')['event'].agg(lambda x: x.value_counts().index[0]))

print("Churned users - first 5 meaningful actions")
print(first_5_churned.groupby('event_rank')['event'].agg(lambda x: x.value_counts().index[0]))
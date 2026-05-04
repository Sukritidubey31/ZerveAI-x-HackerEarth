import pandas as pd
user_stats = data_clean.groupby('user_id').agg(
    total_events        = ('event', 'count'),
    unique_event_types  = ('event', 'nunique'),
    first_seen          = ('timestamp', 'min'),
    last_seen           = ('timestamp', 'max'),
    total_credits_used  = ('prop_credits_used', 'sum'),
    total_sessions      = ('prop_session_id', 'nunique'),
).reset_index()

user_stats['lifespan_days'] = (user_stats['last_seen'] - user_stats['first_seen']).dt.days
user_stats['events_per_day'] = user_stats['total_events'] / (user_stats['lifespan_days'] + 1)

def user_did(event_name):
    return data_clean[data_clean['event'] == event_name].groupby('user_id').size().gt(0)

behavior_flags = pd.DataFrame(index=user_stats['user_id'])

behavior_flags['completed_onboarding'] = user_did('submit_onboarding_form')
behavior_flags['skipped_onboarding'] = user_did('skip_onboarding_form')
behavior_flags['tour_finished'] = user_did('canvas_onboarding_tour_finished')

behavior_flags['ran_block'] = user_did('run_block')
behavior_flags['created_block'] = user_did('block_create')
behavior_flags['created_canvas'] = user_did('canvas_create')
behavior_flags['created_edge'] = user_did('edge_create')
behavior_flags['uploaded_files'] = user_did('files_upload')

behavior_flags['used_agent'] = user_did('agent_new_chat')
behavior_flags['used_agent_start'] = user_did('agent_start_from_prompt')

behavior_flags['published_app'] = user_did('app_publish')
behavior_flags['shared_canvas'] = user_did('canvas_share')
behavior_flags['scheduled_job'] = user_did('scheduled_job_start')
behavior_flags['bought_addon_credits'] = user_did('addon_credits_used')

behavior_flags = behavior_flags.reset_index()

user_stats = user_stats.merge(behavior_flags, on='user_id', how='left').fillna(False)

print("User stats shape")
print(user_stats.shape)
print("Sample")
print(user_stats.head(3))
print("Behavior adoption rates")
flag_cols = behavior_flags.columns.drop('user_id')
print((user_stats[flag_cols].sum() / len(user_stats) * 100).round(1).sort_values(ascending=False))
onboarding_events = [
    'sign_up',
    'new_user_created', 
    'submit_onboarding_form',
    'skip_onboarding_form',
    'canvas_onboarding_tour_started',
    'canvas_onboarding_tour_finished'
]

print("Onboarding funnel - unique users at each step")
for event in onboarding_events:
    count = data_clean[data_clean['event'] == event]['user_id'].nunique()
    print(f"{event}: {count}")
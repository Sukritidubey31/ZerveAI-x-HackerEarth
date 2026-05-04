skip_counts = data_clean[data_clean['event'] == 'skip_onboarding_form'].groupby('user_id').size()

print("How many times does skip_onboarding_form fire per user?")
print(skip_counts.describe())
print("Value counts")
print(skip_counts.value_counts().head(10))
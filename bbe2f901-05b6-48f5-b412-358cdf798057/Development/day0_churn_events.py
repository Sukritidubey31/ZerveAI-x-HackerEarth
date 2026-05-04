day0_churned = data_clean[(~data_clean['is_power_user']) & (data_clean['days_since_signup'] == 0)]

print("What churned users did on Day 0")
print(day0_churned['event'].value_counts().head(15))
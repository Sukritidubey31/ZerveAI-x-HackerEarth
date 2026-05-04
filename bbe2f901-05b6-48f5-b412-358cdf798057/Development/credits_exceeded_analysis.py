print("Unique users who hit credits_exceeded on Day 0")

power_exceeded_users = day0_power[day0_power['event'] == 'credits_exceeded']['user_id'].nunique()
churned_exceeded_users = day0_churned[day0_churned['event'] == 'credits_exceeded']['user_id'].nunique()

print("Power users")
print(power_exceeded_users)
print("Churned users")
print(churned_exceeded_users)

total_power = power_users['user_id'].nunique()
total_churned = everyone_else['user_id'].nunique()

print("As % of each group")
print("Power users %")
print(round(power_exceeded_users / total_power * 100, 1))
print("Churned users %")
print(round(churned_exceeded_users / total_churned * 100, 1))
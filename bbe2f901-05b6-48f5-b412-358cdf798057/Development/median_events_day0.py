print("Median events on Day 0")
power_day0_counts = day0_power.groupby('user_id').size()
churned_day0_counts = day0_churned.groupby('user_id').size()

print("Power users")
print(power_day0_counts.median())
print("Churned users")
print(churned_day0_counts.median())
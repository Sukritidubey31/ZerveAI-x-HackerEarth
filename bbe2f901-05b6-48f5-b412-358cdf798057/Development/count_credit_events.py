print("credits_exceeded on Day 0")
power_exceeded = day0_power[day0_power['event'] == 'credits_exceeded'].shape[0]
churned_exceeded = day0_churned[day0_churned['event'] == 'credits_exceeded'].shape[0]
print("Power users")
print(power_exceeded)
print("Churned users")
print(churned_exceeded)

print("credits_below_1 on Day 0")
power_below1 = day0_power[day0_power['event'] == 'credits_below_1'].shape[0]
churned_below1 = day0_churned[day0_churned['event'] == 'credits_below_1'].shape[0]
print("Power users")
print(power_below1)
print("Churned users")
print(churned_below1)
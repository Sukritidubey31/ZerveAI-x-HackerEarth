print("addon_credits_used on Day 0")
power_addon = day0_power[day0_power['event'] == 'addon_credits_used'].shape[0]
churned_addon = day0_churned[day0_churned['event'] == 'addon_credits_used'].shape[0]
print("Power users")
print(power_addon)
print("Churned users")
print(churned_addon)
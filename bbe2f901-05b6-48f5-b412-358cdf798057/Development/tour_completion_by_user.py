print("Onboarding tour completion rate by user type")
power_tour = user_stats[user_stats['is_power_user']]['tour_finished'].mean() * 100
churned_tour = user_stats[~user_stats['is_power_user']]['tour_finished'].mean() * 100

print("Power users")
print(round(power_tour, 1), "%")
print("Churned users")
print(round(churned_tour, 1), "%")
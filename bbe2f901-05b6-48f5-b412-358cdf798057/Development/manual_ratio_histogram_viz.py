import matplotlib.pyplot as plt

power_ratios = user_stats[user_stats['is_power_user']]['manual_ratio']
churned_ratios = user_stats[~user_stats['is_power_user']]['manual_ratio']

plt.figure(figsize=(8, 4))
plt.hist(churned_ratios, bins=30, alpha=0.6, label='Churned', color='salmon')
plt.hist(power_ratios, bins=30, alpha=0.6, label='Power users', color='steelblue')
plt.xlabel('Manual action ratio')
plt.ylabel('Number of users')
plt.title('Manual vs Agent Action Ratio: Power vs Churned Users')
plt.legend()
plt.tight_layout()
plt.savefig('manual_ratio_distribution.png', dpi=150)
plt.show()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Zerve design system ────────────────────────────────────────────────────────
BG       = '#1D1D20'
TEXT     = '#fbfbff'
SUBTEXT  = '#909094'
BLUE     = '#A1C9F4'
ORANGE   = '#FFB482'
CORAL    = '#FF9F9B'
GOLD     = '#ffd400'
SUCCESS  = '#17b26a'

# ── Feature labels (clean display names) ──────────────────────────────────────
LABEL_MAP = {
    'total_events':        'Total Events',
    'day0_events':         'Day-0 Events',
    'unique_event_types':  'Unique Event Types',
    'agent_actions':       'Agent Actions ★',
    'manual_ratio':        'Manual Action Ratio',
    'total_sessions':      'Total Sessions',
    'manual_actions':      'Manual Actions',
    'used_agent':          'Used Agent (flag)',
    'used_agent_start':    'Used Agent Start (flag)',
    'total_credits_used':  'Credits Used',
    'ran_block':           'Ran a Block',
    'created_block':       'Created Block',
    'skipped_onboarding':  'Skipped Onboarding',
    'completed_onboarding':'Completed Onboarding',
    'created_canvas':      'Created Canvas',
    'created_edge':        'Created Edge',
    'tour_finished':       'Tour Finished',
    'uploaded_files':      'Uploaded Files',
    'published_app':       'Published App',
    'shared_canvas':       'Shared Canvas',
    'scheduled_job':       'Scheduled Job',
    'bought_addon_credits':'Bought Addon Credits',
}

# ── Reconstruct Series with proper string feature-name indexes ─────────────────
# feature_cols is the canonical list of feature names (22 items)
# lr_coefficients_sorted index = feature names sorted by |coef|
# rf_importances_sorted index  = feature names sorted by importance desc
lr_feat_names = list(feature_cols)   # original order

# Logistic regression: sorted by |coef| descending
lr_coefs_raw = pd.Series(lr_model.coef_[0], index=lr_feat_names)
lr_sorted = lr_coefs_raw.reindex(lr_coefs_raw.abs().sort_values(ascending=False).index)

# Random forest: sorted by importance descending
rf_imps_raw  = pd.Series(rf_model.feature_importances_, index=lr_feat_names)
rf_sorted    = rf_imps_raw.sort_values(ascending=False)

# ── Top-10 by |LR coef|, with aligned RF importances ──────────────────────────
top10_raw    = lr_sorted.index[:10].tolist()          # raw feature names
top10_labels = [LABEL_MAP.get(f, f) for f in top10_raw]

lr_top10 = lr_sorted[top10_raw]
rf_top10 = rf_imps_raw[top10_raw]          # align RF to same order as LR top-10

# Normalize to [0, 1] for visual comparability
rf_top10_norm = rf_top10 / rf_top10.max()
lr_top10_abs  = lr_top10.abs() / lr_top10.abs().max()

# ── CHART 1: Side-by-side horizontal bar ──────────────────────────────────────
fig1, ax = plt.subplots(figsize=(13, 7))
fig1.patch.set_facecolor(BG)
ax.set_facecolor(BG)

y_pos  = np.arange(len(top10_labels))
bar_h  = 0.35

lr_colors = [GOLD if abs(v) == lr_top10.abs().max() else BLUE for v in lr_top10.values]
rf_colors = [GOLD if v == rf_top10.max() else ORANGE for v in rf_top10.values]

ax.barh(y_pos + bar_h/2, lr_top10_abs.values, bar_h,
        color=lr_colors, alpha=0.9)
ax.barh(y_pos - bar_h/2, rf_top10_norm.values, bar_h,
        color=rf_colors, alpha=0.9)

for ii in range(len(top10_raw)):
    ax.text(lr_top10_abs.values[ii] + 0.01, y_pos[ii] + bar_h/2,
            f'{lr_top10.values[ii]:+.3f}', va='center', ha='left', fontsize=8, color=BLUE)
    ax.text(rf_top10_norm.values[ii] + 0.01, y_pos[ii] - bar_h/2,
            f'{rf_top10.values[ii]:.4f}', va='center', ha='left', fontsize=8, color=ORANGE)

ax.set_yticks(y_pos)
ax.set_yticklabels(top10_labels, color=TEXT, fontsize=10)
ax.invert_yaxis()
ax.set_xlabel('Normalized Score (0 → 1)', color=SUBTEXT, fontsize=10)
ax.set_title('Feature Importance Comparison — Logistic Regression vs Random Forest\n'
             'Top 10 features by |LR coefficient| magnitude  ★ = AI Agent Usage',
             color=TEXT, fontsize=13, fontweight='bold', pad=14)
ax.tick_params(colors=SUBTEXT)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color(SUBTEXT)
ax.spines['left'].set_color(SUBTEXT)
ax.set_xlim(0, 1.28)

for ii, feat in enumerate(top10_raw):
    if 'agent' in feat.lower():
        ax.axhspan(ii - 0.45, ii + 0.45, color=GOLD, alpha=0.06)

patch_lr = mpatches.Patch(color=BLUE,   label='Logistic Regression |coeff| (normalized)')
patch_rf = mpatches.Patch(color=ORANGE, label='Random Forest Importance (normalized)')
patch_hi = mpatches.Patch(color=GOLD,   label='★ Top predictor in each model')
ax.legend(handles=[patch_lr, patch_rf, patch_hi],
          loc='lower right', framealpha=0.15,
          facecolor=BG, edgecolor=SUBTEXT, labelcolor=TEXT, fontsize=9)
plt.tight_layout()
plt.savefig('feature_importance_comparison.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.show()

# ── CHART 2: Agent vs Manual — retained vs churned ─────────────────────────────
power_mask   = user_stats['is_power_user'] == True
churned_mask = user_stats['is_power_user'] == False

power_agent_mean    = user_stats[power_mask]['agent_actions'].mean()
churned_agent_mean  = user_stats[churned_mask]['agent_actions'].mean()
power_manual_mean   = user_stats[power_mask]['manual_actions'].mean()
churned_manual_mean = user_stats[churned_mask]['manual_actions'].mean()
agent_ratio         = power_agent_mean / max(churned_agent_mean, 1e-9)
manual_ratio_val    = power_manual_mean / max(churned_manual_mean, 1e-9)

print(f"\n── Agent vs Manual Action Breakdown ─────────────────────")
print(f"{'Metric':<35} {'Power Users':>14} {'Churned Users':>14} {'Ratio':>8}")
print("─" * 75)
print(f"{'Avg Agent Actions':<35} {power_agent_mean:>14.2f} {churned_agent_mean:>14.2f} {agent_ratio:>7.1f}x")
print(f"{'Avg Manual Actions':<35} {power_manual_mean:>14.2f} {churned_manual_mean:>14.2f} {manual_ratio_val:>7.1f}x")
manual_r_power   = user_stats[power_mask]['manual_ratio'].mean()
manual_r_churned = user_stats[churned_mask]['manual_ratio'].mean()
print(f"{'Avg Manual Ratio':<35} {manual_r_power:>14.3f} {manual_r_churned:>14.3f}")
used_agent_power   = user_stats[power_mask]['used_agent'].mean() * 100
used_agent_churned = user_stats[churned_mask]['used_agent'].mean() * 100
print(f"{'% Users Who Used Agent':<35} {used_agent_power:>13.1f}% {used_agent_churned:>13.1f}%")

fig2, ax2 = plt.subplots(figsize=(10, 5.5))
fig2.patch.set_facecolor(BG)
ax2.set_facecolor(BG)

categories   = ['Agent\nActions', 'Manual\nActions']
power_vals   = [power_agent_mean, power_manual_mean]
churned_vals = [churned_agent_mean, churned_manual_mean]
x2 = np.arange(len(categories))
w  = 0.35

b1 = ax2.bar(x2 - w/2, power_vals,   w, color=SUCCESS, alpha=0.9, label='Retained (Power Users)')
b2 = ax2.bar(x2 + w/2, churned_vals, w, color=CORAL,   alpha=0.9, label='Churned Users')

for bar in b1:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f'{bar.get_height():.1f}', ha='center', va='bottom', color=TEXT, fontsize=11, fontweight='bold')
for bar in b2:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f'{bar.get_height():.1f}', ha='center', va='bottom', color=TEXT, fontsize=11, fontweight='bold')

ax2.annotate(f'{agent_ratio:.1f}x more\nagent usage',
             xy=(x2[0], max(power_agent_mean, churned_agent_mean)),
             xytext=(x2[0] - 0.05, max(power_agent_mean, churned_agent_mean) * 1.2),
             fontsize=12, fontweight='bold', color=GOLD, ha='center',
             arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.5))

ax2.set_xticks(x2)
ax2.set_xticklabels(categories, color=TEXT, fontsize=12)
ax2.tick_params(colors=SUBTEXT)
ax2.set_ylabel('Avg Actions per User', color=SUBTEXT, fontsize=11)
ax2.set_title('AI Agent Usage vs Manual Actions\nRetained (Power) Users vs Churned Users',
              color=TEXT, fontsize=13, fontweight='bold', pad=12)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_color(SUBTEXT)
ax2.spines['left'].set_color(SUBTEXT)
ax2.legend(facecolor=BG, edgecolor=SUBTEXT, labelcolor=TEXT, fontsize=10)
plt.tight_layout()
plt.savefig('agent_vs_manual_comparison.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.show()

# ── CHART 3: Agent-related features deep-dive (LR + RF side-by-side) ──────────
agent_feats = ['agent_actions', 'used_agent', 'used_agent_start', 'manual_ratio', 'manual_actions']
agent_labels = [LABEL_MAP.get(f, f) for f in agent_feats]
agent_lr_coefs = [float(lr_coefs_raw[f]) for f in agent_feats]
agent_rf_imps  = [float(rf_imps_raw[f])  for f in agent_feats]

fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(13, 4.5))
fig3.patch.set_facecolor(BG)
for _ax in [ax3a, ax3b]:
    _ax.set_facecolor(BG)
    _ax.spines['top'].set_visible(False)
    _ax.spines['right'].set_visible(False)
    _ax.spines['bottom'].set_color(SUBTEXT)
    _ax.spines['left'].set_color(SUBTEXT)
    _ax.tick_params(colors=SUBTEXT)

colors_lr_agent = [SUCCESS if v > 0 else CORAL for v in agent_lr_coefs]
ax3a.barh(agent_labels, agent_lr_coefs, color=colors_lr_agent, alpha=0.9)
ax3a.axvline(0, color=SUBTEXT, linewidth=1, linestyle='--')
for jj, v in enumerate(agent_lr_coefs):
    offset = 0.02 if v >= 0 else -0.02
    align  = 'left' if v >= 0 else 'right'
    ax3a.text(v + offset, jj, f'{v:+.4f}', va='center', ha=align, fontsize=9, color=TEXT)
ax3a.set_title('Logistic Regression\nCoefficients (signed)', color=TEXT, fontsize=11, fontweight='bold')
ax3a.set_xlabel('Coefficient Value', color=SUBTEXT, fontsize=9)
ax3a.invert_yaxis()
ax3a.set_yticklabels(agent_labels, color=TEXT, fontsize=9)

ax3b.barh(agent_labels, agent_rf_imps, color=ORANGE, alpha=0.9)
for jj, v in enumerate(agent_rf_imps):
    ax3b.text(v + 0.001, jj, f'{v:.4f}', va='center', ha='left', fontsize=9, color=TEXT)
ax3b.set_title('Random Forest\nFeature Importances', color=TEXT, fontsize=11, fontweight='bold')
ax3b.set_xlabel('Gini Importance', color=SUBTEXT, fontsize=9)
ax3b.invert_yaxis()
ax3b.set_yticklabels(agent_labels, color=TEXT, fontsize=9)

pos_patch = mpatches.Patch(color=SUCCESS, label='→ Power user predictor')
neg_patch = mpatches.Patch(color=CORAL,   label='→ Churn risk predictor')
ax3a.legend(handles=[pos_patch, neg_patch],
            facecolor=BG, edgecolor=SUBTEXT, labelcolor=TEXT, fontsize=8, loc='lower right')

fig3.suptitle('Agent & Manual Feature Deep-Dive  ★ AI Agent Usage = Top Retention Signal',
              color=TEXT, fontsize=12, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('agent_feature_deepdive.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.show()

# ── Summary ────────────────────────────────────────────────────────────────────
lr_agent_rank = list(lr_sorted.index).index('agent_actions') + 1
rf_agent_rank = list(rf_sorted.index).index('agent_actions') + 1
print(f"\n── Model Summary ───────────────────────────────────────────")
print(f"LR  'agent_actions' coefficient : {lr_coefs_raw['agent_actions']:+.4f}  (rank #{lr_agent_rank} of 22 by |coef|)")
print(f"RF  'agent_actions' importance  : {rf_imps_raw['agent_actions']:.4f}   (rank #{rf_agent_rank} of 22)")
print(f"Agent usage differential (power vs churned): {agent_ratio:.1f}x")
print(f"Power users avg agent actions : {power_agent_mean:.1f}  |  Churned: {churned_agent_mean:.1f}")

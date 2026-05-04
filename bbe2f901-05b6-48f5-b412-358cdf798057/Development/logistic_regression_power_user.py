from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np

# Define features and target
feature_cols = [
    'day0_events', 'manual_ratio', 'total_events', 'unique_event_types',
    'total_sessions', 'total_credits_used', 'manual_actions', 'agent_actions',
    'completed_onboarding', 'skipped_onboarding', 'tour_finished', 'ran_block',
    'created_block', 'created_canvas', 'created_edge', 'uploaded_files',
    'used_agent', 'used_agent_start', 'published_app', 'shared_canvas',
    'scheduled_job', 'bought_addon_credits'
]

# Drop rows with NaNs in relevant columns
lr_df = user_stats[feature_cols + ['is_power_user']].dropna()

X = lr_df[feature_cols]
y = lr_df['is_power_user']

print(f"Dataset: {len(lr_df):,} users | Power users: {y.sum()} ({y.mean()*100:.1f}%) | Others: {(~y.astype(bool)).sum()}")

# Train/test split (stratified to preserve class balance)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Logistic regression with class_weight='balanced' to handle imbalance
lr_model = LogisticRegression(
    class_weight='balanced',
    max_iter=1000,
    random_state=42
)
lr_model.fit(X_train_scaled, y_train)

# Evaluation
y_pred = lr_model.predict(X_test_scaled)
print("\n── Classification Report ──────────────────────────────")
print(classification_report(y_test, y_pred, target_names=['Not Power User', 'Power User']))

# Feature importance via coefficients
lr_coefficients = pd.Series(lr_model.coef_[0], index=feature_cols)
lr_coefficients_sorted = lr_coefficients.reindex(
    lr_coefficients.abs().sort_values(ascending=False).index
)

print("── Feature Coefficients (sorted by |magnitude|) ──────")
print(f"{'Feature':<25} {'Coefficient':>12}  {'Direction':>12}")
print("─" * 55)
for feat, coef in lr_coefficients_sorted.items():
    direction = "▲ power user" if coef > 0 else "▼ churn risk"
    print(f"{feat:<25} {coef:>+12.4f}  {direction:>12}")
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pandas as pd

# Re-use the same prepared data from logistic regression block
# (feature_cols, X_train, X_test, y_train, y_test are all available upstream)

# Train Random Forest — no scaling needed for tree-based models
rf_model = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)

# Predictions on test set
rf_y_pred = rf_model.predict(X_test)

# Classification report
print("── Random Forest Classification Report ───────────────")
print(classification_report(y_test, rf_y_pred, target_names=['Not Power User', 'Power User']))

# Feature importances sorted highest to lowest
rf_importances = pd.Series(rf_model.feature_importances_, index=feature_cols)
rf_importances_sorted = rf_importances.sort_values(ascending=False)

print("── Feature Importances (sorted highest → lowest) ─────")
print(f"{'Feature':<25} {'Importance':>10}  {'Bar':}")
print("─" * 60)
for _feat, _imp in rf_importances_sorted.items():
    _bar = "█" * int(_imp * 200)
    print(f"{_feat:<25} {_imp:>10.4f}  {_bar}")
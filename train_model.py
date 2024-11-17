from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Initialize the model
model = RandomForestRegressor(random_state=42, n_estimators=100)

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Evaluate the model on training data
print("Training Performance:")
print(f"Mean Absolute Error (MAE): {mean_absolute_error(y_train, y_pred_train):.2f}")
print(f"Mean Squared Error (MSE): {mean_squared_error(y_train, y_pred_train):.2f}")
print(f"R² Score: {r2_score(y_train, y_pred_train):.2f}")

# Evaluate the model on testing data
print("\nTesting Performance:")
print(f"Mean Absolute Error (MAE): {mean_absolute_error(y_test, y_pred_test):.2f}")
print(f"Mean Squared Error (MSE): {mean_squared_error(y_test, y_pred_test):.2f}")
print(f"R² Score: {r2_score(y_test, y_pred_test):.2f}")

# Feature importance
feature_importances = model.feature_importances_
features = ['Hour', 'Day', 'Month', 'Minute',
            'Inj Gas Meter Volume Instantaneous',
            'Inj Gas Meter Volume Setpoint',
            'Inj Gas Valve Percent Open']
print("\nFeature Importances:")
for feature, importance in zip(features, feature_importances):
    print(f"{feature}: {importance:.4f}")

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

file_path = "combined_dataset.csv"
data = pd.read_csv(file_path)

data['Time'] = pd.to_datetime(data['Time'], errors='coerce')
data['Hour'] = data['Time'].dt.hour
data['Day'] = data['Time'].dt.day
data['Month'] = data['Time'].dt.month
data['Minute'] = data['Time'].dt.minute

X = data[['Hour', 'Day', 'Month', 'Minute',
          'Inj Gas Meter Volume Instantaneous',
          'Inj Gas Meter Volume Setpoint',
          'Inj Gas Valve Percent Open']]
y = data['Likelihood of Hydrate']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

joblib.dump(scaler, "scaler.pkl")

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"R² Score: {r2}")

feature_importances = model.feature_importances_
features = ['Hour', 'Day', 'Month', 'Minute',
            'Inj Gas Meter Volume Instantaneous',
            'Inj Gas Meter Volume Setpoint',
            'Inj Gas Valve Percent Open']

print("Feature Importances:")
for feature, importance in zip(features, feature_importances):
    print(f"{feature}: {importance:.4f}")

joblib.dump(model, "random_forest_hydrate_model.pkl")
print("Model saved as random_forest_hydrate_model.pkl")

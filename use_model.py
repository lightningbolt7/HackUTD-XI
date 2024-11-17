import joblib
import pandas as pd

model = joblib.load("random_forest_hydrate_model.pkl")
scaler = joblib.load("scaler.pkl")

input_data = {
    'Hour': [2],
    'Day': [29],
    'Month': [10],
    'Minute': [8],
    'Inj Gas Meter Volume Instantaneous': [0.0],
    'Inj Gas Meter Volume Setpoint': [375.0],
    'Inj Gas Valve Percent Open': [100.0]
}


input_df = pd.DataFrame(input_data)

input_scaled = scaler.transform(input_df)

predicted_likelihood = model.predict(input_scaled)

print(f"Predicted Likelihood of Hydrate: {predicted_likelihood[0]}")

import joblib
import pandas as pd

# Load the saved Random Forest model and scaler
model = joblib.load("random_forest_hydrate_model.pkl")
scaler = joblib.load("scaler.pkl")  # Load the saved scaler

# Example input data for prediction (same format as the training data)
input_data = {
    'Hour': [2],  # Example: 12 PM
    'Day': [29],  # Example: 29th day
    'Month': [10],  # Example: October
    'Minute': [8],  # Example: 8 minutes
    'Inj Gas Meter Volume Instantaneous': [0.0],  # Example value
    'Inj Gas Meter Volume Setpoint': [375.0],  # Example value
    'Inj Gas Valve Percent Open': [100.0]  # Example value
}

# Convert the input data into a pandas DataFrame
input_df = pd.DataFrame(input_data)

# Normalize the input data using the same scaler used for training
input_scaled = scaler.transform(input_df)  # Use the scaler that was fitted during training

# Predict the likelihood of hydrate using the trained model
predicted_likelihood = model.predict(input_scaled)

# Print the predicted likelihood (the output)
print(f"Predicted Likelihood of Hydrate: {predicted_likelihood[0]}")

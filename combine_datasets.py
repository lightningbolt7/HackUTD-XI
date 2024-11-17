import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import glob  # To load multiple files

# Define the folder where all pipe data is stored
data_folder = "data/final/"
pipe_files = glob.glob(data_folder + "*.csv")  # Get all CSV files in the folder

# Combine all pipe datasets into one DataFrame
combined_data = pd.DataFrame()

for file in pipe_files:
    data = pd.read_csv(file)
    combined_data = pd.concat([combined_data, data], ignore_index=True)

# Display combined data structure
print("Combined Data:")
print(combined_data.head())
print(f"Total records: {combined_data.shape[0]}")

# Save the combined dataset to a file
output_file = "combined_dataset.csv"
combined_data.to_csv(output_file, index=False)
print(f"Combined dataset saved to {output_file}")

# Ensure 'Time' column is in datetime format and extract features
combined_data['Time'] = pd.to_datetime(combined_data['Time'], errors='coerce')
combined_data['Hour'] = combined_data['Time'].dt.hour
combined_data['Day'] = combined_data['Time'].dt.day
combined_data['Month'] = combined_data['Time'].dt.month
combined_data['Minute'] = combined_data['Time'].dt.minute

# Define features and target
X = combined_data[['Hour', 'Day', 'Month', 'Minute',
                   'Inj Gas Meter Volume Instantaneous',
                   'Inj Gas Meter Volume Setpoint',
                   'Inj Gas Valve Percent Open']]
y = combined_data['Likelihood of Hydrate']

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split into train and test sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Display split sizes
print(f"Training set size: {X_train.shape[0]} samples")
print(f"Test set size: {X_test.shape[0]} samples")

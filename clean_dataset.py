import pandas as pd
import numpy as np

file_name = "Example"

# Define the path to the single CSV file
file_path = "data/initial/" + file_name + ".csv"  # Replace with your actual file path

# Load the data from the CSV file
data = pd.read_csv(file_path)

# Display the first few rows to understand the structure
print("Original Data:")
print(data.head())

# Ensure 'Time' column is in datetime format
if 'Time' in data.columns:
    data['Time'] = pd.to_datetime(data['Time'], errors='coerce')  # Handle invalid dates

# Fill missing values
# First, apply backward fill to handle the top rows with NaN values
data = data.bfill(axis=0)

# Then, apply forward fill to handle the rest of the missing data
data = data.fillna(method='ffill')  # Forward-fill remaining missing values

# Calculate the rolling standard deviation for the Gas Meter Volume Instantaneous
window_size = 20  # You can adjust the window size based on your data
data['Rolling Std'] = data['Inj Gas Meter Volume Instantaneous'].rolling(window=window_size).std()

# Normalize the rolling standard deviation to the range 0-100
min_std = data['Rolling Std'].min()
max_std = data['Rolling Std'].max()

# Apply normalization formula (Min-Max scaling to [0, 100])
data['Likelihood of Hydrate'] = 100 * (data['Rolling Std'] - min_std) / (max_std - min_std)

# Handle cases where max_std equals min_std (avoid division by zero)
data['Likelihood of Hydrate'] = data['Likelihood of Hydrate'].fillna(0)

# Save the cleaned data to a new CSV file
output_file = "data/final/" + file_name + ".csv"  # Save the cleaned DataFrame
data.to_csv(output_file, index=False)

# Display the cleaned data
print("Cleaned Data with 'Likelihood of Hydrate':")
print(data.head())
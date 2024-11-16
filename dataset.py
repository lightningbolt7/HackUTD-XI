import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
pipe_name = "Bold"
file_path = "data/initial/" + pipe_name + ".csv"  # Replace with your CSV file path
data = pd.read_csv(file_path)

# Display the first few rows to understand the structure
print("Original Data:")
print(data.head())

# Ensure 'Time' column is in datetime format
if 'Time' in data.columns:
    data['Time'] = pd.to_datetime(data['Time'], errors='coerce')  # Handle invalid dates

# Fill missing values
data = data.fillna(method='ffill')  # Forward-fill missing values

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

# Save the cleaned and final data to a CSV file
data.to_csv("data/final/" + pipe_name + ".csv", index=False)  # Save the final DataFrame to "final.csv"

# Check cleaned data with the new column
print("Cleaned Data with 'Likelihood of Hydrate':")
print(data.head())

# Example: Overlay plotting the cleaned dataset
plt.figure(figsize=(12, 6))

# Plotting the different columns
plt.plot(data['Time'], data['Inj Gas Meter Volume Instantaneous'], label='Gas Meter Volume Instantaneous', color='blue')
plt.plot(data['Time'], data['Inj Gas Meter Volume Setpoint'], label='Gas Meter Volume Setpoint', color='green')
plt.plot(data['Time'], data['Inj Gas Valve Percent Open'], label='Gas Valve Percent Open', color='orange')

# Plotting the Likelihood of Hydrate
plt.plot(data['Time'], data['Likelihood of Hydrate'], label='Likelihood of Hydrate', color='purple', linestyle='--')

# Adding a horizontal line at y = 100
plt.axhline(y=100, color='red', linestyle='--', label='y = 100')

# Adding Titles and Labels
plt.title("Overlay Plot - Gas Meter Volumes, Valve Percent, and Likelihood of Hydrate")
plt.xlabel("Time")
plt.ylabel("Value")
plt.legend()
plt.grid(True)

# Rotating x-axis labels for better readability
plt.xticks(rotation=45)

# Tight layout to avoid label cutoffs
plt.tight_layout()

# Show the plot
plt.show()

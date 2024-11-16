import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = "data/Valiant.csv"  # Replace with your CSV file path
data = pd.read_csv(file_path)

# Display the first few rows to understand the structure
print("Original Data:")
print(data.head())

# Ensure 'Time' column is in datetime format
if 'Time' in data.columns:
    data['Time'] = pd.to_datetime(data['Time'], errors='coerce')  # Handle invalid dates

# Fill missing values
data = data.fillna(method='ffill')  # Forward-fill missing values
data = data.fillna(0)  # Fill remaining NaN values with 0 or another value if needed

# Check cleaned data
print("Cleaned Data:")
print(data.head())

# Example: Overlay plotting the cleaned dataset
plt.figure(figsize=(12, 6))

# Plotting the different columns
plt.plot(data['Time'], data['Inj Gas Meter Volume Instantaneous'], label='Gas Meter Volume Instantaneous', color='blue')
plt.plot(data['Time'], data['Inj Gas Meter Volume Setpoint'], label='Gas Meter Volume Setpoint', color='green')
plt.plot(data['Time'], data['Inj Gas Valve Percent Open'], label='Gas Valve Percent Open', color='orange')

# Adding a horizontal line at y = 100
plt.axhline(y=100, color='red', linestyle='--', label='y = 100')

# Adding Titles and Labels
plt.title("Overlay Plot - Gas Meter Volumes and Valve Percent")
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

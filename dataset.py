import pandas as pd
import matplotlib.pyplot as plt
import os

# Folder paths
input_folder = "data/initial/"  # Folder containing the input CSV files
output_folder = "data/final/"  # Folder to save the processed files
graph_folder = "data/graphs/"  # Folder to save the graphs
output_file = output_folder + "final.csv"  # Merged final file

# Ensure the output and graph folders exist
os.makedirs(output_folder, exist_ok=True)
os.makedirs(graph_folder, exist_ok=True)

# List all CSV files in the input folder
files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# Initialize a list to hold processed DataFrames
processed_dfs = []

# Process each file
for file in files:
    file_path = os.path.join(input_folder, file)
    data = pd.read_csv(file_path)

    # Ensure 'Time' column is in datetime format
    if 'Time' in data.columns:
        data['Time'] = pd.to_datetime(data['Time'], errors='coerce')  # Handle invalid dates

    # Fill missing values
    data = data.fillna(method='ffill')  # Forward-fill missing values
    data = data.fillna(method='bfill')  # Backward-fill remaining missing values

    # Calculate the rolling standard deviation for the Gas Meter Volume Instantaneous
    window_size = 20  # You can adjust the window size based on your data
    data['Rolling Std'] = data['Inj Gas Meter Volume Instantaneous'].rolling(window=window_size).std()

    # Handle NaN values in the Rolling Std (e.g., at the start of the series)
    data['Rolling Std'] = data['Rolling Std'].fillna(0)  # Replace NaN with 0

    # Normalize the rolling standard deviation to the range 0-100
    min_std = data['Rolling Std'].min()
    max_std = data['Rolling Std'].max()

    # Apply normalization formula (Min-Max scaling to [0, 100])
    if max_std > min_std:  # Avoid division by zero
        data['Likelihood of Hydrate'] = 100 * (data['Rolling Std'] - min_std) / (max_std - min_std)
    else:
        data['Likelihood of Hydrate'] = 0

    # Save the processed file to the output folder
    processed_file_path = os.path.join(output_folder, file)
    data.to_csv(processed_file_path, index=False)

    # Append the processed DataFrame to the list
    processed_dfs.append(data)

    # Generate and save the graph for the current file
    plt.figure(figsize=(12, 6))

    # Plotting the different columns
    plt.plot(data['Time'], data['Inj Gas Meter Volume Instantaneous'], label='Gas Meter Volume Instantaneous', color='blue')
    plt.plot(data['Time'], data['Inj Gas Meter Volume Setpoint'], label='Gas Meter Volume Setpoint', color='green')
    plt.plot(data['Time'], data['Inj Gas Valve Percent Open'], label='Gas Valve Percent Open', color='orange')

    # Plotting the Likelihood of Hydrate
    plt.plot(data['Time'], data['Likelihood of Hydrate'], label='Likelihood of Hydrate', color='purple', linestyle='--')

    # Adding Titles and Labels
    plt.title(f"Overlay Plot - {file}")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)

    # Rotating x-axis labels for better readability
    plt.xticks(rotation=45)

    # Tight layout to avoid label cutoffs
    plt.tight_layout()

    # Save the graph as an image file
    graph_file_path = os.path.join(graph_folder, f"{file.split('.')[0]}.png")
    plt.savefig(graph_file_path)
    plt.close()  # Close the figure to avoid overlap in the loop

    print(f"Processed and graphed: {file}")

# Merge all processed DataFrames into one
final_df = pd.concat(processed_dfs, ignore_index=True)

# Save the merged DataFrame to the final output file
final_df.to_csv(output_file, index=False)

print(f"Processed {len(files)} files. Merged file saved as '{output_file}'. Graphs saved in '{graph_folder}'.")

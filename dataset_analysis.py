import pandas as pd
import matplotlib.pyplot as plt
import os


input_folder = "data/initial/"
output_folder = "data/final/"
graph_folder = "data/graphs/"
output_file = output_folder + "final.csv"


os.makedirs(output_folder, exist_ok=True)
os.makedirs(graph_folder, exist_ok=True)


files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]


processed_dfs = []


for file in files:
    file_path = os.path.join(input_folder, file)
    data = pd.read_csv(file_path)


    if 'Time' in data.columns:
        data['Time'] = pd.to_datetime(data['Time'], errors='coerce')


    data = data.fillna(method='ffill')
    data = data.fillna(method='bfill')


    window_size = 20
    data['Rolling Std'] = data['Inj Gas Meter Volume Instantaneous'].rolling(window=window_size).std()


    data['Rolling Std'] = data['Rolling Std'].fillna(0)

    min_std = data['Rolling Std'].min()
    max_std = data['Rolling Std'].max()

    if max_std > min_std:
        data['Likelihood of Hydrate'] = 100 * (data['Rolling Std'] - min_std) / (max_std - min_std)
    else:
        data['Likelihood of Hydrate'] = 0


    processed_file_path = os.path.join(output_folder, file)
    data.to_csv(processed_file_path, index=False)


    processed_dfs.append(data)


    plt.figure(figsize=(12, 6))


    plt.plot(data['Time'], data['Inj Gas Meter Volume Instantaneous'], label='Gas Meter Volume Instantaneous', color='blue')
    plt.plot(data['Time'], data['Inj Gas Meter Volume Setpoint'], label='Gas Meter Volume Setpoint', color='green')
    plt.plot(data['Time'], data['Inj Gas Valve Percent Open'], label='Gas Valve Percent Open', color='orange')


    plt.plot(data['Time'], data['Likelihood of Hydrate'], label='Likelihood of Hydrate', color='purple', linestyle='--')


    plt.title(f"Overlay Plot - {file}")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)


    plt.xticks(rotation=45)


    plt.tight_layout()


    graph_file_path = os.path.join(graph_folder, f"{file.split('.')[0]}.png")
    plt.savefig(graph_file_path)
    plt.close()

    print(f"Processed and graphed: {file}")


final_df = pd.concat(processed_dfs, ignore_index=True)
final_df.to_csv(output_file, index=False)

print(f"Processed {len(files)} files. Merged file saved as '{output_file}'. Graphs saved in '{graph_folder}'.")

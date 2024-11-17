import pandas as pd
import numpy as np

file_name = "Example"

file_path = "data/initial/" + file_name + ".csv"


data = pd.read_csv(file_path)


print("Original Data:")
print(data.head())


if 'Time' in data.columns:
    data['Time'] = pd.to_datetime(data['Time'], errors='coerce')


data = data.bfill(axis=0)


data = data.fillna(method='ffill')


window_size = 20
data['Rolling Std'] = data['Inj Gas Meter Volume Instantaneous'].rolling(window=window_size).std()


min_std = data['Rolling Std'].min()
max_std = data['Rolling Std'].max()


data['Likelihood of Hydrate'] = 100 * (data['Rolling Std'] - min_std) / (max_std - min_std)


data['Likelihood of Hydrate'] = data['Likelihood of Hydrate'].fillna(0)


output_file = "data/final/" + file_name + ".csv"
data.to_csv(output_file, index=False)


print("Cleaned Data with 'Likelihood of Hydrate':")
print(data.head())
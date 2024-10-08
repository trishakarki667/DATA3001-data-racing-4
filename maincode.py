import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_2022 = pd.read_csv('/Users/zhaoxuanliu/desktop/data3001/f1sim-data-2022.csv')
file_2023 = pd.read_csv('/Users/zhaoxuanliu/desktop/data3001/f1sim-data-2023.csv')

total_data = pd.concat([file_2022, file_2023])

columns_to_keep = ['SESSION_IDENTIFIER', 'LAP_NUM', 'LAP_DISTANCE', 'CURRENT_LAP_TIME_MS', 
                   'THROTTLE', 'BRAKE', 'STEERING', 'WORLDPOSX', 'WORLDPOSY']

total_data_filtered = total_data[columns_to_keep]

# Processing data initially
# Convert all columns to numeric, coercing errors, and remove rows with non-numeric values
total_data_filtered = total_data_filtered.apply(pd.to_numeric, errors='coerce')

# Drop rows where any of the columns have NaN values (resulting from non-numeric data)
total_data_filtered = total_data_filtered.dropna()

# Step 2: Filter throttle and brake values between 0 and 1
total_data_filtered = total_data_filtered[(total_data_filtered['THROTTLE'] >= 0) & (total_data_filtered['THROTTLE'] <= 1)]
total_data_filtered = total_data_filtered[(total_data_filtered['BRAKE'] >= 0) & (total_data_filtered['BRAKE'] <= 1)]
total_data_filtered['LAP_ID'] = total_data_filtered['SESSION_IDENTIFIER'].astype(str) + '_' + total_data_filtered['LAP_NUM'].astype(str)

file_left = '/Users/zhaoxuanliu/desktop/data3001/f1sim-ref-left.csv'
file_right = '/Users/zhaoxuanliu/desktop/data3001/f1sim-ref-right.csv'

data_left = pd.read_csv(file_left)
data_right = pd.read_csv(file_right)

filtered_left = data_left[(data_left['WORLDPOSX'] >= 0) & (data_left['WORLDPOSX'] <= 700) & 
                          (data_left['WORLDPOSY'] >= -300) & (data_left['WORLDPOSY'] <= 620)]

filtered_right = data_right[(data_right['WORLDPOSX'] >= 0) & (data_right['WORLDPOSX'] <= 700) & 
                            (data_right['WORLDPOSY'] >= -300) & (data_right['WORLDPOSY'] <= 620)]
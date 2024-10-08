import pandas as pd
import numpy as np

# Load the 2022 and 2023 data, and select only needed cols
file_2022 = pd.read_csv('/Users/chris/Downloads/data-2/f1sim-data-2022.csv')
file_2023 = pd.read_csv('/Users/chris/Downloads/data-2/f1sim-data-2023.csv')
columns_to_keep = ['SESSION_IDENTIFIER', 'LAP_NUM', 'LAP_DISTANCE', 'CURRENT_LAP_TIME_MS', 
                   'THROTTLE', 'BRAKE', 'STEERING', 'WORLDPOSX', 'WORLDPOSY']
total_data_filtered = pd.concat([file_2022[columns_to_keep], file_2023[columns_to_keep]])

# Load the 2024 data file, rename the cols to match 22/23 cols names
file_2024 = pd.read_csv('/Users/chris/Downloads/data-2/F124 Data Export UNSW.csv', low_memory = False)
file_2024_renamed = file_2024.rename(columns = {
    'SESSION_GUID': 'SESSION_IDENTIFIER',
    'M_CURRENTLAPNUM': 'LAP_NUM',
    'M_LAPDISTANCE_1': 'LAP_DISTANCE',
    'M_CURRENTLAPTIMEINMS_1': 'CURRENT_LAP_TIME_MS',
    'M_THROTTLE_1': 'THROTTLE',
    'M_BRAKE_1': 'BRAKE',
    'M_STEER_1': 'STEERING',
    'M_WORLDPOSITIONX_1': 'WORLDPOSX',
    'M_WORLDPOSITIONY_1': 'WORLDPOSY'
})

# Select required cols from the 2024 data and concat to the existing 22/23
file_2024_filtered = file_2024_renamed[columns_to_keep]
total_data_filtered = pd.concat([total_data_filtered, file_2024_filtered], ignore_index = True)

# Processing data initially
# Check numeric values for selected cols and drop NaN values
numeric_columns = ['LAP_NUM', 'LAP_DISTANCE', 'CURRENT_LAP_TIME_MS', 'THROTTLE', 'BRAKE', 'STEERING', 'WORLDPOSX', 'WORLDPOSY']
total_data_filtered[numeric_columns] = total_data_filtered[numeric_columns].apply(pd.to_numeric, errors = 'coerce')
total_data_filtered = total_data_filtered.dropna(subset = numeric_columns)

# Check for throttle and brake between 0 and 1
total_data_filtered = total_data_filtered[(total_data_filtered['THROTTLE'] >= 0) & (total_data_filtered['THROTTLE'] <= 1)]
total_data_filtered = total_data_filtered[(total_data_filtered['BRAKE'] >= 0) & (total_data_filtered['BRAKE'] <= 1)]

# Create LAP_ID for group and subset data
total_data_filtered['LAP_ID'] = total_data_filtered['SESSION_IDENTIFIER'].astype(str) + '_' + total_data_filtered['LAP_NUM'].astype(str)

# Process left and rigth data
file_left = '/Users/chris/Downloads/data-2/f1sim-ref-left.csv'
file_right = '/Users/chris/Downloads/data-2/f1sim-ref-right.csv'
data_left = pd.read_csv(file_left)
data_right = pd.read_csv(file_right)
filtered_left = data_left[(data_left['WORLDPOSX'] >= 0) & (data_left['WORLDPOSX'] <= 600) & 
                          (data_left['WORLDPOSY'] >= -300) & (data_left['WORLDPOSY'] <= 620)]
filtered_right = data_right[(data_right['WORLDPOSX'] >= 0) & (data_right['WORLDPOSX'] <= 600) & 
                            (data_right['WORLDPOSY'] >= -300) & (data_right['WORLDPOSY'] <= 620)]

# Function to filter out subset of each lap data
def filtered_sorted_data_subset(data):
    filtered_data = data[(data['WORLDPOSX'] >= 100) & (data['WORLDPOSX'] <= 475) &
                         (data['WORLDPOSY'] >= -50) & (data['WORLDPOSY'] <= 460) &
                         (data['LAP_DISTANCE'] >= 0) & (data['LAP_DISTANCE'] <= 1000)] 
    filtered_sorted_data = filtered_data.sort_values(by = 'LAP_DISTANCE', ascending = True)
    return filtered_sorted_data

# Function to get data for car position using interpolation method
def interpolate_data_info(filtered_sorted_data, lap_distance_target):
    # Check exact match for the target lap distance, return value if exist
    exact_match = filtered_sorted_data[filtered_sorted_data['LAP_DISTANCE'] == lap_distance_target]
    if not exact_match.empty:
        exact_point = exact_match.iloc[0]
        return (exact_point['CURRENT_LAP_TIME_MS'], 
                exact_point['BRAKE'], 
                exact_point['THROTTLE'], 
                exact_point['STEERING'], 
                exact_point['WORLDPOSX'], 
                exact_point['WORLDPOSY'])
    
    # Find the two rows that are closest to the target lap distance (P_t and P_t+1)
    filtered_before = filtered_sorted_data[filtered_sorted_data['LAP_DISTANCE'] <= lap_distance_target]
    filtered_after = filtered_sorted_data[filtered_sorted_data['LAP_DISTANCE'] > lap_distance_target]
    if filtered_before.empty or filtered_after.empty:
        return np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
    
    Pt = filtered_before.iloc[-1]
    Pt1 = filtered_after.iloc[0]

    # Extract the pos for the P_t and P_t+1
    Pt_pos = np.array([Pt['WORLDPOSX'], Pt['WORLDPOSY']])
    Pt1_pos = np.array([Pt1['WORLDPOSX'], Pt1['WORLDPOSY']])
    distance_Pt_Pt1 = np.linalg.norm(Pt1_pos - Pt_pos)

    # Calculate c as per the interpolation algorithm
    Lt = Pt['LAP_DISTANCE']
    Lt1 = Pt1['LAP_DISTANCE']
    c = (lap_distance_target - Lt) / distance_Pt_Pt1
    
    # Calculate the interpolated values
    Te = (1 - c) * Pt['CURRENT_LAP_TIME_MS'] + c * Pt1['CURRENT_LAP_TIME_MS']
    Be = (1 - c) * Pt['BRAKE'] + c * Pt1['BRAKE']
    The = (1 - c) * Pt['THROTTLE'] + c * Pt1['THROTTLE']
    Se = (1 - c) * Pt['STEERING'] + c * Pt1['STEERING']
    Xe = (1 - c) * Pt['WORLDPOSX'] + c * Pt1['WORLDPOSX']
    Ye = (1 - c) * Pt['WORLDPOSY'] + c * Pt1['WORLDPOSY']
    
    return Te, Be, The, Se, Xe, Ye

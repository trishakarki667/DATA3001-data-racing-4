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


# Function to calculate the distance between two points
def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Function to find two closest point to a threshold point
def find_closest_points(x_threshold, y_threshold, filtered_left, filtered_right):
    filtered_left_copy = filtered_left.copy()
    filtered_right_copy = filtered_right.copy()

    # Calculate the distance from each point in filtered_left to the threshold point
    filtered_left_copy['distance_to_threshold'] = filtered_left_copy.apply(
        lambda row: distance(row['WORLDPOSX'], row['WORLDPOSY'], x_threshold, y_threshold), axis=1
    )

    # Sort by distance to get the two closest points L1 and L2
    filtered_left_copy = filtered_left_copy.sort_values(by = 'distance_to_threshold')
    L1 = filtered_left_copy.iloc[0]  
    L2 = filtered_left_copy.iloc[1]  

    # Calculate the distance from each point in filtered_right to the threshold point
    filtered_right_copy['distance_to_threshold'] = filtered_right_copy.apply(
        lambda row: distance(row['WORLDPOSX'], row['WORLDPOSY'], x_threshold, y_threshold), axis=1
    )

    # Sort by distance to get the two closest points R1 and R2
    filtered_right_copy = filtered_right_copy.sort_values(by='distance_to_threshold')
    R1 = filtered_right_copy.iloc[0]  
    R2 = filtered_right_copy.iloc[1]  

    return L1, L2, R1, R2

# Function to find whether a car pos is on-track or not
def check_track_position(x_P, y_P, filtered_left, filtered_right):
    # Recalculate L1, L2, R1, R2 for the current threshold point
    L1, L2, R1, R2 = find_closest_points(x_P, y_P, filtered_left, filtered_right)

    # Avoid division by zero in c_L and c_R
    denom_L = (L2['WORLDPOSX'] - L1['WORLDPOSX'])**2 + (L2['WORLDPOSY'] - L1['WORLDPOSY'])**2
    denom_R = (R2['WORLDPOSX'] - R1['WORLDPOSX'])**2 + (R2['WORLDPOSY'] - R1['WORLDPOSY'])**2
    if denom_L != 0:
        c_L = ((x_P - L1['WORLDPOSX']) * (L2['WORLDPOSX'] - L1['WORLDPOSX']) + (y_P - L1['WORLDPOSY']) * (L2['WORLDPOSY'] - L1['WORLDPOSY'])) / denom_L
    else:
        c_L = 0  
    if denom_R != 0:
        c_R = ((x_P - R1['WORLDPOSX']) * (R2['WORLDPOSX'] - R1['WORLDPOSX']) + (y_P - R1['WORLDPOSY']) * (R2['WORLDPOSY'] - R1['WORLDPOSY'])) / denom_R
    else:
        c_R = 0  

    # Calculate the projected points L_p and R_p
    L_p_x = L1['WORLDPOSX'] + c_L * (L2['WORLDPOSX'] - L1['WORLDPOSX'])
    L_p_y = L1['WORLDPOSY'] + c_L * (L2['WORLDPOSY'] - L1['WORLDPOSY'])
    R_p_x = R1['WORLDPOSX'] + c_R * (R2['WORLDPOSX'] - R1['WORLDPOSX'])
    R_p_y = R1['WORLDPOSY'] + c_R * (R2['WORLDPOSY'] - R1['WORLDPOSY'])

    # Calculate the distances from car pos to L_p and R_p
    distance_L = np.sqrt((x_P - L_p_x)**2 + (y_P - L_p_y)**2)
    distance_R = np.sqrt((x_P - R_p_x)**2 + (y_P - R_p_y)**2)
    
    # Calculate the track width plus buffer = 1
    track_width = np.sqrt((L_p_x - R_p_x)**2 + (L_p_y - R_p_y)**2) + 1 

    # Check if the car is on-track, left-off, or right-off
    if max(distance_L, distance_R) <= track_width:
        pos_valid = "on-track"
    elif distance_R > track_width:
        pos_valid = "right-off"
    elif distance_L > track_width:
        pos_valid = "left-off"
    
    return distance_L, distance_R, pos_valid

def process_lap_data(lap_data, lap_distance, filtered_left, filtered_right):
    # Interpolate data for the given lap distance
    Te, Be, The, Se, Xe, Ye = interpolate_data_info(lap_data, lap_distance)
    
    # Check track position using the interpolated X and Y
    if not np.isnan(Xe) and not np.isnan(Ye):
        left_distance, right_distance, _ = check_track_position(Xe, Ye, filtered_left, filtered_right)
    else:
        left_distance, right_distance = np.nan, np.nan

    return Te, Be, The, Se, left_distance, right_distance

def validate_track_positions(filtered_sorted_data, filtered_left, filtered_right):
    for _, row in filtered_sorted_data.iterrows():
        x_P, y_P = row['WORLDPOSX'], row['WORLDPOSY']
        _, _, pos_valid = check_track_position(x_P, y_P, filtered_left, filtered_right)
        
        # If any position is off-track, mark as invalid
        if pos_valid != "on-track":
            return "invalid"  
    return "valid" 

lap_results = []
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_2022 = pd.read_csv('/Users/chris/Downloads/data-2/f1sim-data-2022.csv')
file_2023 = pd.read_csv('/Users/chris/Downloads/data-2/f1sim-data-2023.csv')

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

file_left = '/Users/chris/Downloads/data-2/f1sim-ref-left.csv'
file_right = '/Users/chris/Downloads/data-2/f1sim-ref-right.csv'

data_left = pd.read_csv(file_left)
data_right = pd.read_csv(file_right)

filtered_left = data_left[(data_left['WORLDPOSX'] >= 0) & (data_left['WORLDPOSX'] <= 700) & 
                          (data_left['WORLDPOSY'] >= -300) & (data_left['WORLDPOSY'] <= 620)]

filtered_right = data_right[(data_right['WORLDPOSX'] >= 0) & (data_right['WORLDPOSX'] <= 700) & 
                            (data_right['WORLDPOSY'] >= -300) & (data_right['WORLDPOSY'] <= 620)]

def filtered_sorted_data_subset(data):
    filtered_data = data[(data['WORLDPOSX'] >= 100) & (data['WORLDPOSX'] <= 475) &
                               (data['WORLDPOSY'] >= -50) & (data['WORLDPOSY'] <= 450)]
    filtered_sorted_data = filtered_data.sort_values(by = 'WORLDPOSY', ascending = False) 
    return filtered_sorted_data

def interpolate_data_info(filtered_sorted_data, lap_distance_target):
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

def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def find_closest_points(x_threshold, y_threshold, filtered_left, filtered_right):
    filtered_left_copy = filtered_left.copy()
    filtered_right_copy = filtered_right.copy()
    
    # Calculate the distance from each point in filtered_left to the threshold point
    filtered_left_copy['distance_to_threshold'] = filtered_left_copy.apply(
        lambda row: distance(row['WORLDPOSX'], row['WORLDPOSY'], x_threshold, y_threshold), axis=1
    )

    # Find the closest point L1 and L2
    L1 = filtered_left_copy.loc[filtered_left_copy['distance_to_threshold'].idxmin()]
    filtered_left_without_L1 = filtered_left_copy.drop(L1.name)
    L2 = filtered_left_without_L1.loc[filtered_left_without_L1['distance_to_threshold'].idxmin()]

    # Calculate the distance from each point in filtered_right to the threshold point
    filtered_right_copy['distance_to_threshold'] = filtered_right_copy.apply(
        lambda row: distance(row['WORLDPOSX'], row['WORLDPOSY'], x_threshold, y_threshold), axis=1
    )

    # Find the closest point R1 and R2
    R1 = filtered_right_copy.loc[filtered_right_copy['distance_to_threshold'].idxmin()]
    filtered_right_without_R1 = filtered_right_copy.drop(R1.name)
    R2 = filtered_right_without_R1.loc[filtered_right_without_R1['distance_to_threshold'].idxmin()]

    return L1, L2, R1, R2

def check_track_position(x_P, y_P, filtered_left, filtered_right):

    # Recalculate L1, L2, R1, R2 for the current threshold point
    L1, L2, R1, R2 = find_closest_points(x_P, y_P, filtered_left, filtered_right)

    # Calculate c_L and c_R
    c_L = ((x_P - L1['WORLDPOSX']) * (L2['WORLDPOSX'] - L1['WORLDPOSX']) + (y_P - L1['WORLDPOSY']) * (L2['WORLDPOSY'] - L1['WORLDPOSY'])) / ((L2['WORLDPOSX'] - L1['WORLDPOSX'])**2 + (L2['WORLDPOSY'] - L1['WORLDPOSY'])**2)
    c_R = ((x_P - R1['WORLDPOSX']) * (R2['WORLDPOSX'] - R1['WORLDPOSX']) + (y_P - R1['WORLDPOSY']) * (R2['WORLDPOSY'] - R1['WORLDPOSY'])) / ((R2['WORLDPOSX'] - R1['WORLDPOSX'])**2 + (R2['WORLDPOSY'] - R1['WORLDPOSY'])**2)

    # Calculate the projected points L_p and R_p
    L_p_x = L1['WORLDPOSX'] + c_L * (L2['WORLDPOSX'] - L1['WORLDPOSX'])
    L_p_y = L1['WORLDPOSY'] + c_L * (L2['WORLDPOSY'] - L1['WORLDPOSY'])
    R_p_x = R1['WORLDPOSX'] + c_R * (R2['WORLDPOSX'] - R1['WORLDPOSX'])
    R_p_y = R1['WORLDPOSY'] + c_R * (R2['WORLDPOSY'] - R1['WORLDPOSY'])

    # Calculate the distances from car position to left and right projected points
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

for lap_id, lap_data in total_data_filtered.groupby('LAP_ID'):
    # Apply filtering and sorting to each subset
    filtered_sorted_data = filtered_sorted_data_subset(lap_data)
    
    # Process lap data for lap distances 295, 435, and 575
    Te_295, Be_295, The_295, Se_295, left_distance_295, right_distance_295 = process_lap_data(filtered_sorted_data, 295, filtered_left, filtered_right)
    Te_435, Be_435, The_435, Se_435, left_distance_435, right_distance_435 = process_lap_data(filtered_sorted_data, 435, filtered_left, filtered_right)
    Te_575, Be_575, The_575, Se_575, left_distance_575, right_distance_575 = process_lap_data(filtered_sorted_data, 575, filtered_left, filtered_right)
    
    # Process finishing time at lap distance 600
    Te_600, _, _, _, _, _ = process_lap_data(filtered_sorted_data, 600, filtered_left, filtered_right)
    
    # Validate if all car positions are on-track or not
    track_valid = validate_track_positions(filtered_sorted_data, filtered_left, filtered_right)
    
    # Store the results 
    lap_result = {
        'LAP_ID': lap_id,
        'FINISHING_TIME_AT_600': Te_600,
        'TRACK_VALID': track_valid,
        'BRAKE_AT_295': Be_295,
        'THROTTLE_AT_295': The_295,
        'STEERING_AT_295': Se_295,
        'LEFT_DISTANCE_AT_295': left_distance_295,
        'RIGHT_DISTANCE_AT_295': right_distance_295,
        'BRAKE_AT_435': Be_435,
        'THROTTLE_AT_435': The_435,
        'STEERING_AT_435': Se_435,
        'LEFT_DISTANCE_AT_435': left_distance_435,
        'RIGHT_DISTANCE_AT_435': right_distance_435,
        'BRAKE_AT_575': Be_575,
        'THROTTLE_AT_575': The_575,
        'STEERING_AT_575': Se_575,
        'LEFT_DISTANCE_AT_575': left_distance_575,
        'RIGHT_DISTANCE_AT_575': right_distance_575,
    }
    
    # Append the result to the lap_results list
    lap_results.append(lap_result)

data_product_final = pd.DataFrame(lap_results)
data_product_final_file_path = '/Users/chris/Downloads/data-2/data_product_final.csv'
data_product_final.to_csv(data_product_final_file_path, index = False)

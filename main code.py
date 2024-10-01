#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


file_2022 = pd.read_csv('/Users/chris/Downloads/data-2/f1sim-data-2022.csv')
file_2023 = pd.read_csv('/Users/chris/Downloads/data-2/f1sim-data-2023.csv')

total_data = pd.concat([file_2022, file_2023])

# Select only the required columns
columns_to_keep = ['SESSION_IDENTIFIER', 'LAP_NUM', 'LAP_DISTANCE', 'CURRENT_LAP_TIME_MS', 
                   'THROTTLE', 'BRAKE', 'WORLDPOSX', 'WORLDPOSY']

total_data_filtered = total_data[columns_to_keep]


# In[3]:


# Processing data initially
# Convert all columns to numeric, coercing errors, and remove rows with non-numeric values
total_data_filtered = total_data_filtered.apply(pd.to_numeric, errors='coerce')

# Drop rows where any of the columns have NaN values (resulting from non-numeric data)
total_data_filtered = total_data_filtered.dropna()

# Step 2: Filter throttle and brake values between 0 and 1
total_data_filtered = total_data_filtered[(total_data_filtered['THROTTLE'] >= 0) & (total_data_filtered['THROTTLE'] <= 1)]
total_data_filtered = total_data_filtered[(total_data_filtered['BRAKE'] >= 0) & (total_data_filtered['BRAKE'] <= 1)]
total_data_filtered['LAP_ID'] = total_data_filtered['SESSION_IDENTIFIER'].astype(str) + '_' + total_data_filtered['LAP_NUM'].astype(str)


# In[4]:


file_left = '/Users/chris/Downloads/data-2/f1sim-ref-left.csv'
file_right = '/Users/chris/Downloads/data-2/f1sim-ref-right.csv'

data_left = pd.read_csv(file_left)
data_right = pd.read_csv(file_right)

filtered_left = data_left[(data_left['WORLDPOSX'] >= 0) & (data_left['WORLDPOSX'] <= 600) & 
                          (data_left['WORLDPOSY'] >= -180) & (data_left['WORLDPOSY'] <= 600)]

filtered_right = data_right[(data_right['WORLDPOSX'] >= 0) & (data_right['WORLDPOSX'] <= 600) & 
                            (data_right['WORLDPOSY'] >= -180) & (data_right['WORLDPOSY'] <= 600)]


# In[5]:


def filtered_sorted_data_subset(data):
    filtered_data = data[(data['WORLDPOSX'] >= 100) & (data['WORLDPOSX'] <= 475) &
                               (data['WORLDPOSY'] >= -50) & (data['WORLDPOSY'] <= 450)]
    filtered_sorted_data = filtered_data.sort_values(by = 'WORLDPOSY', ascending = False) 
    return filtered_sorted_data


# In[6]:


def count_finishing_time(filtered_sorted_data):
    # Set finishing line at lap distance equal to 600
    # Looking for the two points where LAP_DISTANCE is just before and after 600
    lap_distance_target = 600

    # Find the two rows that are closest to the target lap distance (P_t and P_t+1)
    filtered_before = filtered_sorted_data[filtered_sorted_data['LAP_DISTANCE'] <= lap_distance_target]
    filtered_after = filtered_sorted_data[filtered_sorted_data['LAP_DISTANCE'] > lap_distance_target]

    if filtered_before.empty or filtered_after.empty:
        return np.nan
    
    # Find the two rows closest to the target lap distance
    Pt = filtered_before.iloc[-1]
    Pt1 = filtered_after.iloc[0]

    
    # Extract the pos for the P_t and P_t+1
    Pt_pos = np.array([Pt['WORLDPOSX'], Pt['WORLDPOSY']])
    Pt1_pos = np.array([Pt1['WORLDPOSX'], Pt1['WORLDPOSY']])

    # Compute distance between P_t and P_t+1
    distance_Pt_Pt1 = np.linalg.norm(Pt1_pos - Pt_pos)

    # Calculate c as per the interpolation algorithm
    Lt = Pt['LAP_DISTANCE']
    Lt1 = Pt1['LAP_DISTANCE']
    c = (lap_distance_target - Lt) / distance_Pt_Pt1

    # Calculate the finishing time at lap distance 600
    Tt = Pt['CURRENT_LAP_TIME_MS']
    Tt1 = Pt1['CURRENT_LAP_TIME_MS']
    Te = (1 - c) * Tt + c * Tt1
    
    return Te


# In[7]:


def extract_crictal_point(filtered_sorted_data, filtered_left, filtered_right):
    # Initialize the critical points with NaN in case the condition isn't met
    result = {
        'THROTTLE_CRITICAL_POINT_1': np.nan,
        'BRAKE_CRITICAL_POINT_1': np.nan,
        'LAP_DISTANCE_POINT_1': np.nan,
        'RIGHT_DISTANCE_POINT_1': np.nan,
        'LEFT_DISTANCE_POINT_1': np.nan,
        'THROTTLE_CRITICAL_POINT_2': np.nan,
        'BRAKE_CRITICAL_POINT_2': np.nan,
        'LAP_DISTANCE_POINT_2': np.nan,
        'RIGHT_DISTANCE_POINT_2': np.nan,
        'LEFT_DISTANCE_POINT_2': np.nan,
        'THROTTLE_CRITICAL_POINT_3': np.nan,
        'BRAKE_CRITICAL_POINT_3': np.nan,
        'LAP_DISTANCE_POINT_3': np.nan,
        'RIGHT_DISTANCE_POINT_3': np.nan,
        'LEFT_DISTANCE_POINT_3': np.nan,
    }

    # Find the car position point closest to y = 260 
    car_pos_y_above_260 = filtered_sorted_data[filtered_sorted_data['WORLDPOSY'] >= 260]
    if not car_pos_y_above_260.empty:
        closest_to_y_260 = car_pos_y_above_260.iloc[(car_pos_y_above_260['WORLDPOSY'] - 260).abs().argmin()]
        result['THROTTLE_CRITICAL_POINT_1'] = closest_to_y_260['THROTTLE']
        result['BRAKE_CRITICAL_POINT_1'] = closest_to_y_260['BRAKE']
        result['LAP_DISTANCE_POINT_1'] = closest_to_y_260['LAP_DISTANCE']
        distance_L_1, distance_R_1, _ = check_track_position(closest_to_y_260, filtered_left, filtered_right)
        result['LEFT_DISTANCE_POINT_1'] = distance_L_1
        result['RIGHT_DISTANCE_POINT_1'] = distance_R_1

    # Find the car position point closest to y = 145
    car_pos_y_above_145 = filtered_sorted_data[filtered_sorted_data['WORLDPOSY'] >= 145]
    if not car_pos_y_above_145.empty:
        closest_to_y_145 = car_pos_y_above_145.iloc[(car_pos_y_above_145['WORLDPOSY'] - 145).abs().argmin()]
        result['THROTTLE_CRITICAL_POINT_2'] = closest_to_y_145['THROTTLE']
        result['BRAKE_CRITICAL_POINT_2'] = closest_to_y_145['BRAKE']
        result['LAP_DISTANCE_POINT_2'] = closest_to_y_145['LAP_DISTANCE']
        distance_L_2, distance_R_2, _ = check_track_position(closest_to_y_145, filtered_left, filtered_right)
        result['LEFT_DISTANCE_POINT_2'] = distance_L_2
        result['RIGHT_DISTANCE_POINT_2'] = distance_R_2

    # Find the car position point closest to x = 405
    car_pos_x_below_405 = filtered_sorted_data[filtered_sorted_data['WORLDPOSX'] <= 405]
    if not car_pos_x_below_405.empty:
        closest_to_x_405 = car_pos_x_below_405.iloc[(car_pos_x_below_405['WORLDPOSX'] - 405).abs().argmin()]
        result['THROTTLE_CRITICAL_POINT_3'] = closest_to_x_405['THROTTLE']
        result['BRAKE_CRITICAL_POINT_3'] = closest_to_x_405['BRAKE']
        result['LAP_DISTANCE_POINT_3'] = closest_to_x_405['LAP_DISTANCE']
        distance_L_3, distance_R_3, _ = check_track_position(closest_to_x_405, filtered_left, filtered_right)
        result['LEFT_DISTANCE_POINT_3'] = distance_L_3
        result['RIGHT_DISTANCE_POINT_3'] = distance_R_3

    return result


# In[8]:


def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)


# In[9]:


# Function to find the two closest points L1, L2, R1, R2 given a threshold point
# Using Algo 1
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


# In[10]:


def check_track_position(row, filtered_left, filtered_right):
    x_P = row['WORLDPOSX']
    y_P = row['WORLDPOSY']

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
    
    # Calculate the track width plus buffer
    track_width = np.sqrt((L_p_x - R_p_x)**2 + (L_p_y - R_p_y)**2) + 2 # buffer = 2

    # Check if the car is on-track, left-off, or right-off
    if max(distance_L, distance_R) <= track_width:
        pos_valid = "on-track"
    elif distance_R > track_width:
        pos_valid = "right-off"
    elif distance_L > track_width:
        pos_valid = "left-off"
    
    return distance_L, distance_R, pos_valid


# In[11]:


lap_results = []

for lap_id, lap_data in total_data_filtered.groupby('LAP_ID'):
    # Apply filtering and sorting to each subset
    filtered_sorted_data = filtered_sorted_data_subset(lap_data)
    
    # Calculate the finishing time for each subset
    finishing_time = count_finishing_time(filtered_sorted_data)
    
    # Extract critical points
    critical_points = extract_crictal_point(filtered_sorted_data, filtered_left, filtered_right)
    
    # Initialize track_valid as "valid"
    track_valid = "valid"

    # Check if any point is off-track (right-off or left-off)
    for _, row in filtered_sorted_data.iterrows():
        _, _, pos_valid = check_track_position(row, filtered_left, filtered_right)
        if pos_valid != "on-track":
            track_valid = "invalid"
            break
    
    # Store the results (LAP_ID, FINISHING_TIME, 'TRACK_VALID', and critical points)
    lap_result = {
        'LAP_ID': lap_id,
        'FINISHING_TIME': finishing_time,
        'TRACK_VALID': track_valid
    }
    
    # Add critical points to the result
    lap_result.update(critical_points)
    
    # Append the result to the lap_results list
    lap_results.append(lap_result)

# Create a final DataFrame with the results
data_product_final = pd.DataFrame(lap_results)

data_product_final


# In[12]:


data_product_final_file_path = '/Users/chris/Downloads/data-2/data_product_final.csv'
data_product_final.to_csv(data_product_final_file_path, index = False)


# In[ ]:





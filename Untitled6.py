#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


file_path = '/Users/chris/Downloads/data-2/f1sim-data-2023.csv'
data = pd.read_csv(file_path)

first_session_id = data['SESSION_IDENTIFIER'].iloc[0]

# Filter the data for car position with X between 325 and 475, Y between -50 and 260, and for lap 1
filtered_data_corrected = data[(data['WORLDPOSX'] >= 325) & (data['WORLDPOSX'] <= 475) &
                               (data['WORLDPOSY'] >= -50) & (data['WORLDPOSY'] <= 260) &
                               (data['LAP_NUM'] == 1)]  # Correct lap number column
# Filter for the first session
filtered_data_corrected_session = filtered_data_corrected[filtered_data_corrected['SESSION_IDENTIFIER'] == first_session_id]

# Save the filtered data to a new CSV file named 'f1-sample.csv'
output_file_path_final = '/Users/chris/Downloads/data-2/f1-sample.csv'
filtered_data_corrected_session.to_csv(output_file_path_final, index = False)


# In[3]:


file_left = '/Users/chris/Downloads/data-2/f1sim-ref-left.csv'
file_right = '/Users/chris/Downloads/data-2/f1sim-ref-right.csv'
turns_file = '/Users/chris/Downloads/data-2/f1sim-ref-turns.csv'
car_pos = '/Users/chris/Downloads/data-2/f1-sample.csv'

data_left = pd.read_csv(file_left)
data_right = pd.read_csv(file_right)
turns_data = pd.read_csv(turns_file)
car_pos_data = pd.read_csv(car_pos)

turns_filtered = turns_data.head(2)
filtered_left = data_left[(data_left['WORLDPOSX'] >= 200) & (data_left['WORLDPOSX'] <= 600) & 
                          (data_left['WORLDPOSY'] >= -180) & (data_left['WORLDPOSY'] <= 300)]

filtered_right = data_right[(data_right['WORLDPOSX'] >= 200) & (data_right['WORLDPOSX'] <= 600) & 
                            (data_right['WORLDPOSY'] >= -180) & (data_right['WORLDPOSY'] <= 300)]

# Extract X and Y coordinates for both datasets
x_left = filtered_left['WORLDPOSX']
y_left = filtered_left['WORLDPOSY']

x_right = filtered_right['WORLDPOSX']
y_right = filtered_right['WORLDPOSY']

x_car = car_pos_data['WORLDPOSX']
y_car = car_pos_data['WORLDPOSY']

# Plotting the filtered turns along with the left, right, car positions, turn points
plt.figure(figsize=(10, 10))

plt.scatter(x_left, y_left, color = 'blue', s = 10, label = 'Left Path (X: 200-600, Y: -180-300)')

plt.scatter(x_right, y_right, color = 'red', s=10, label = 'Right Path (X: 200-600, Y: -180-300)')

plt.scatter(x_car, y_car, color = 'black', s = 10, label = 'Car position')

for idx, row in turns_filtered.iterrows():
    plt.scatter(row['APEX_X1'], row['APEX_Y1'], color = 'green', marker = '*', s = 200, label = f'Turn {row["TURN"]} Apex')  

# Customize the plot
plt.title('Car Position with X: 300-500 and Y: -180 to 300 and Turns 1, 2, 3')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.grid(True)
plt.legend(loc = 'best')  
plt.show()


# In[4]:


car_pos_sorted = car_pos_data.sort_values(by = 'WORLDPOSY', ascending = False)
filtered_left_sorted = filtered_left.sort_values(by = 'WORLDPOSY', ascending = False)
filtered_right_sorted = filtered_right.sort_values(by = 'WORLDPOSY', ascending = False)


# In[5]:


def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)


# In[6]:


# Example for the first car position of the list

y_threshold = car_pos_sorted['WORLDPOSY'].iloc[0]
x_threshold = car_pos_sorted['WORLDPOSX'].iloc[0]

# Filter points in sorted filtered_left with Y coordinate greater than the threshold
greater_than_threshold_left = filtered_left_sorted[filtered_left_sorted['WORLDPOSY'] > y_threshold].head(50)

# Filter points in sorted filtered_left with Y coordinate smaller than the threshold
smaller_than_threshold_left = filtered_left_sorted[filtered_left_sorted['WORLDPOSY'] < y_threshold].head(50)

# Calculate the distance from each point in the set to the threshold point, for the left hand
filtered_left_sorted['distance_to_threshold'] = filtered_left_sorted.apply(
    lambda row: distance(row['WORLDPOSX'], row['WORLDPOSY'], x_threshold, y_threshold), axis = 1
)

# Find the closest point L1
L1 = filtered_left_sorted.loc[filtered_left_sorted['distance_to_threshold'].idxmin()]

# Remove L1 from the set
filtered_left_sorted_without_L1 = filtered_left_sorted.drop(L1.name)

# Find the next closest point L2
L2 = filtered_left_sorted_without_L1.loc[filtered_left_sorted_without_L1['distance_to_threshold'].idxmin()]

# Filter points in sorted filtered_right with Y coordinate greater than the threshold
greater_than_threshold_right = filtered_right_sorted[filtered_right_sorted['WORLDPOSY'] > y_threshold].head(50)

# Filter points in sorted filtered_right with Y coordinate smaller than the threshold
smaller_than_threshold_right = filtered_right_sorted[filtered_right_sorted['WORLDPOSY'] < y_threshold].head(50)

# Calculate the distance from each point in the set to the threshold point, for the right hand
filtered_right_sorted['distance_to_threshold'] = filtered_right_sorted.apply(
    lambda row: distance(row['WORLDPOSX'], row['WORLDPOSY'], x_threshold, y_threshold), axis = 1
)

# Find the closest point R1
R1 = filtered_right_sorted.loc[filtered_right_sorted['distance_to_threshold'].idxmin()]

# Remove B1 from the set
filtered_right_sorted_without_R1 = filtered_right_sorted.drop(R1.name)

# Find the next closest point R2
R2 = filtered_right_sorted_without_R1.loc[filtered_right_sorted_without_R1['distance_to_threshold'].idxmin()]

x_P = x_threshold  # X coordinate of the threshold point
y_P = y_threshold  # Y coordinate of the threshold point

# Coordinates of the two closest points L1 and L2
x_1_L, y_1_L = L1['WORLDPOSX'], L1['WORLDPOSY']  # Closest point L1
x_2_L, y_2_L = L2['WORLDPOSX'], L2['WORLDPOSY']  # Second closest point L2

# Calculate c_L
c_L = ((x_P - x_1_L) * (x_2_L - x_1_L) + (y_P - y_1_L) * (y_2_L - y_1_L)) / ((x_2_L - x_1_L)**2 + (y_2_L - y_1_L)**2)

# Calculate the projected point L_p
L_p_x = x_1_L + c_L * (x_2_L - x_1_L)
L_p_y = y_1_L + c_L * (y_2_L - y_1_L)

# Calculate the distance d from A to L_p
distance_L = np.sqrt((x_P - L_p_x)**2 + (y_P - L_p_y)**2)

# Coordinates of the two closest points R1 and R2
x_1_R, y_1_R = R1['WORLDPOSX'], R1['WORLDPOSY']  # Closest point R1
x_2_R, y_2_R = R2['WORLDPOSX'], R2['WORLDPOSY']  # Second closest point R2

# Calculate c_R
c_R = ((x_P - x_1_R) * (x_2_R - x_1_R) + (y_P - y_1_R) * (y_2_R - y_1_R)) / ((x_2_R - x_1_R)**2 + (y_2_R - y_1_R)**2)

# Calculate the projected point R_p
R_p_x = x_1_R + c_R * (x_2_R - x_1_R)
R_p_y = y_1_R + c_R * (y_2_R - y_1_R)

# Calculate the distance d from A to R_p
distance_R = np.sqrt((x_P - R_p_x)**2 + (y_P - R_p_y)**2)

track_width = np.sqrt((L_p_x - R_p_x)**2 + (L_p_y - R_p_y)**2)

if max(distance_L, distance_R) <= track_width:
    track_valid = "on-track"
elif distance_R > track_width:
    track_valid = "right-off"
elif distancec_L > track_width:
    track_valid = "left-off"
    
# Output the track_valid value
print(f"Track validation: {track_valid}")


# In[7]:


# Function to find the two closest points L1, L2, R1, R2 given a threshold point
# Using Algo 1
def find_closest_points(x_threshold, y_threshold, filtered_left, filtered_right):
    
    # Calculate the distance from each point in filtered_left to the threshold point
    filtered_left['distance_to_threshold'] = filtered_left.apply(
        lambda row: distance(row['WORLDPOSX'], row['WORLDPOSY'], x_threshold, y_threshold), axis=1
    )

    # Find the closest point L1 and L2
    L1 = filtered_left.loc[filtered_left['distance_to_threshold'].idxmin()]
    filtered_left_without_L1 = filtered_left.drop(L1.name)
    L2 = filtered_left_without_L1.loc[filtered_left_without_L1['distance_to_threshold'].idxmin()]

    # Calculate the distance from each point in filtered_right to the threshold point
    filtered_right['distance_to_threshold'] = filtered_right.apply(
        lambda row: distance(row['WORLDPOSX'], row['WORLDPOSY'], x_threshold, y_threshold), axis=1
    )

    # Find the closest point R1 and R2
    R1 = filtered_right.loc[filtered_right['distance_to_threshold'].idxmin()]
    filtered_right_without_R1 = filtered_right.drop(R1.name)
    R2 = filtered_right_without_R1.loc[filtered_right_without_R1['distance_to_threshold'].idxmin()]

    return L1, L2, R1, R2


# In[8]:


# Function to calculate the track position for each point
# Using Algo 2 and 4
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
        return "on-track"
    elif distance_R > track_width:
        return "right-off"
    elif distance_L > track_width:
        return "left-off"


# In[9]:


# Apply the logic to each row in car_pos_sorted and create the 'TRACK_VALID' column
car_pos_sorted['TRACK_VALID'] = car_pos_sorted.apply(lambda row: check_track_position(row, filtered_left_sorted, filtered_right_sorted), axis=1)


# In[10]:


car_pos_sorted_file_path = '/Users/chris/Downloads/data-2/car-pos-sorted.csv'
car_pos_sorted.to_csv(car_pos_sorted_file_path, index = False)


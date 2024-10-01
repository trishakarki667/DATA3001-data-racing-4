import pandas as pd 

# Load left-hand side and right-hand side data
left_data = pd.read_csv("f1sim-ref-left.csv")
right_data = pd.read_csv("f1sim-ref-right.csv")

# Load corner data from the CSV file
corner_data = pd.read_csv("f1sim-ref-turns.csv")

# Load the lap data from the CSV file
lap_data = pd.read_csv("f1sim-ref-line.csv")  # Assuming you have a lap_data.csv file

# Create the scatter plot
plt.figure(figsize=(10, 6))

# Scatter plot for left-hand side route (Longitude vs Latitude)
plt.scatter(left_data['WORLDPOSX'], left_data['WORLDPOSY'], color='blue', label='Left Side', s=10)

# Scatter plot for right-hand side route (Longitude vs Latitude)
plt.scatter(right_data['WORLDPOSX'], right_data['WORLDPOSY'], color='red', label='Right Side', s=10)

# Plot the lap data (Longitude vs Latitude)
plt.scatter(lap_data['WORLDPOSX'], lap_data['WORLDPOSY'], color='orange', label='Lap Line', s=0.5)

# Plot the apex points
plt.scatter(corner_data['APEX_X1'], corner_data['APEX_Y1'], color='green', label='Apex Points', s=40)

# Label each apex with the turn number
for i, row in corner_data.iterrows():
    plt.text(row['APEX_X1'], row['APEX_Y1'], f'Turn {row["TURN"]}', fontsize=9, color='black')

# Set labels and title
plt.xlabel('Longitude (WORLDPOSX)')
plt.ylabel('Latitude (WORLDPOSY)')
plt.title('F1 Racing Route with Apexes and Lap Line')

# Show legend and plot
plt.legend()
plt.grid(True)
plt.show()



# Create a new column 'lap_id' by combining 'SESSION_IDENTIFIER' and 'LAP_NUM'
data['lap_id'] = data['SESSION_IDENTIFIER'].astype(str) + '_' + data['LAP_NUM'].astype(str)

# Display the updated DataFrame
print(data[['SESSION_IDENTIFIER', 'LAP_NUM', 'lap_id']])
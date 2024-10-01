import pandas as pd 

# Load datasets 
left_data = pd.read_csv("f1sim-ref-left.csv")
right_data = pd.read_csv("f1sim-ref-right.csv")
corner_data = pd.read_csv("f1sim-ref-turns.csv")
lap_data = pd.read_csv("f1sim-ref-line.csv") 

# Create a new column 'lap_id' by combining 'SESSION_IDENTIFIER' and 'LAP_NUM'
data['lap_id'] = data['SESSION_IDENTIFIER'].astype(str) + '_' + data['LAP_NUM'].astype(str)
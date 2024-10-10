## Project Title: F1 Data Product

# Project Description:

# Main Objective 

&nbsp;&nbsp;&nbsp;&nbsp;To develop a comprehensive dataset using data collected in 2022, 2023 and 2024 from an F1 simulation by Oracle. This product will identify key variables that should be optimised to achieve an ideal lap time, specifically focusing on turns 1 and 2 on the race track.

# Significance  

&nbsp;&nbsp;&nbsp;&nbsp;F1 racing is becoming increasingly data-centric, with teams relying on extensive data to make strategic decisions and improve their performance. This data product will serve as a foundation for further modelling by identifying crucial factors such as braking point, turning points, and car positioning to maximise exit speed from turn 2. By leveraging these insights, teams can make informed decisions, giving their drivers a competitive edge on the track.

# Relation to  previous work 

&nbsp;&nbsp;&nbsp;&nbsp;In recent years, data analysis has become central to F1 racing, with teams leveraging Monte Carlo simulations and real-time data to improve their strategies for optimal performance. Previous efforts, particularly by teams like Oracle Red Bull Racing, have focused on collecting data related to variables such as speed, throttle, and steering inputs. Drivers like Max Verstappen use these advanced simulations to identify key factors that influence lap times and make adjustments accordingly. 
 
&nbsp;&nbsp;&nbsp;&nbsp;This project builds on Oracle’s existing data by introducing new variables and manipulating data to ultimately create a data framework. By expanding the dataset in this way, we aim to provide drivers with more detailed insights to make better-informed decisions and ultimately improve lap times. 

# Sources:

&nbsp;&nbsp;&nbsp;&nbsp;The data sources used to construct the data product are datasets provided by Oracle which contain records of variables recorded in an F1 simulation during the years 2022 - 2024. The data itself was produced via the EA F1 simulator in which various drivers raced around the track while information on relevant variables was recorded. 

&nbsp;&nbsp;&nbsp;&nbsp;The variables included in the 2022 and 2023 datasets will be used to construct data product are shown below.

| Variable       | Description | 
|:-----------|:----|
| SESSION_IDENTIFIER   |  Unique identifier for the session | 
| LAP_NUM |  Current lap number |
| LAP_DISTANCE  |  Distance vehicle is around current lap in metre | 
| CURRENT_LAP_TIME_MS  |  Current time around the lap in milliseconds |
| THROTTLE  |  Amount of throttle applied (0.0 to 1.0) |
| BRAKE  |  Amount of brake applied (0.0 to 1.0) |
| STEERING  |  Steering (-1.0 (full lock left) to 1.0 (full lock right)) |
| WORLDPOS X/Y  |  World space X/Y position |

&nbsp;&nbsp;&nbsp;&nbsp;Additional variables that were included in the 2024 are shown below along with their corresponding variable names:

| Variable       | Corresponding Variable | 
|:-----------|:----|
| SESSION_GUID   |  SESSION_IDENTIFIER | 
| M_CURRENTLAPNUM |  LAP_NUM |
| M_LAPDISTANCE_1  |  LAP_DISTANCE | 
| M_CURRENTLAPTIMEINMS_1  |  CURRENT_LAP_TIME_MS |
| M_THROTTLE_1  |  THROTTLE |
| M_BRAKE_1  |  BRAKE |
| M_STEER_1  |  STEERING |
| M_WORLDPOSITIONX_1/Y_1  |  WORLDPOS X/Y |
| STEERING  |  WORLDPOS X/Y |


# Workflow:
&nbsp;&nbsp;&nbsp;&nbsp;__1. Setting up our track of interest__ 

&nbsp;&nbsp;&nbsp;&nbsp;The first step is to identify critical points within the lap, from the start of Turn 1, through Turn 2, to the finishing line. By plotting the first lap of the 2023 data, using the left and right side distances and corner coordinates, we identified five key points at 295m, 386m, 435m, 494m, 575m, and 600m (the new finishing line). These points are just before the boundary and apex of Turns 1 and 2, with 600m (a point between Turns 2 and 3). These points are crucial for modelling, as they capture significant insights like brake, throttle, steering and distances to the track edges. 

&nbsp;&nbsp;&nbsp;&nbsp;__2. Combining 3 datasets__

&nbsp;&nbsp;&nbsp;&nbsp;To ensure consistency and make the data easier to process, we first merged the 2022 and 2023 data files, as they shared the same variables and format. After merging, we kept only the variables necessary for modelling, which is described in the data description. Next, we integrated the 2024 data file, which had a different format and variable names. This required renaming and aligning the variables with those from the combined 2022 and 2023 dataset.

&nbsp;&nbsp;&nbsp;&nbsp;__3. Initial data cleaning__

&nbsp;&nbsp;&nbsp;&nbsp;Once the data was merged, we performed initial data cleaning after taking all the columns, and dropped NaN values. The criteria for identifying if it is NaN is if the value is missing for columns where that value must be shown in numerical type, or the value for variable not is numerical type, such as string value. We also checked for any inconsistencies in the throttle and brake values as it needs to be between 0.00 to 1.00

&nbsp;&nbsp;&nbsp;&nbsp;__4. New lap ID variable__

&nbsp;&nbsp;&nbsp;&nbsp;We created a new variable LAP_ID, by combining SESSION_ID and the LAP_NUMBER. Each unique LAP_ID represents an independent subset, ensuring that all data within each lap is treated as a separate observation in our data product.

&nbsp;&nbsp;&nbsp;&nbsp;__5. Data interpolation__

&nbsp;&nbsp;&nbsp;&nbsp;To determine the throttle, brake and steering values for the chosen five critical points, linear interpolation was used. Due to the format of data files in 2022 and 2023, we do not have exact data information for those critical points, which is the reason behind our decision to use linear interpolation, as we need the two closest points to find the values for those critical points.

&nbsp;&nbsp;&nbsp;&nbsp;__6. Further Data cleaning__

&nbsp;&nbsp;&nbsp;&nbsp;Since the lap distance at 600m is treated as a new finishing line, the finishing time at this point becomes a potential response variable. After producing the data, we’ll filter out any rows with NaN values for finishing time at 600m, though some NaN values for other variables will remain for modellers to handle later as these laps could still provide valuable information. The missing data for finishing time at 600m is due to insufficient data for interpolation, which requires two points (before and after the target point). For example, if the lap distance data goes up to 1000m but the critical point is at 600m, and there is no point close enough after 600m, interpolation becomes unreliable. This issue also affects other critical points with large gaps in lap distance. 

&nbsp;&nbsp;&nbsp;&nbsp;__7. Is the lap valid?__

&nbsp;&nbsp;&nbsp;&nbsp;We created a new variable, ‘TRACK_VALID’, which determines whether a lap is valid or invalid. A lap is considered valid if the car stays on track throughout. To check this, we first find the two nearest points on both the left and right edges of the track for each car position. Then, we calculate the distance from the car to both edges. If the car’s distance from either side is within the width of the track (plus a 1 metre buffer for the car’s width), the lap is marked as valid. However, if all four wheels of the car are off the track—meaning it crosses the boundary on either side—the lap is considered invalid.

# Data description:

&nbsp;&nbsp;&nbsp;&nbsp;This dataset contains 1272 rows, each representing a lap in the F1 racing simulator for the Albert Park race track, covering data from 2022,2023 and 2024. A unique identifier for each lap, lap_id was created by combining the session ID and lap number.

&nbsp;&nbsp;&nbsp;&nbsp;The key variables of interest are: 

| Variable       | Description | 
|:-----------|:----|
| LAP_ID   |  Unique identifier for each lap, formed by combining the session ID and lap number | 
| LBRAKE_AT_[distance] |  The amount of braking (0.0 to 1.0) applied at that specific distance (i.e 295m, 386m, 435m, 494m, 575m) |
| THROTTLE_AT_[distance]  |  The amount of throttle (0.0 to 1.0) applied at that specific distance (i.e 295m, 386m, 435m, 494m, 575m) | 
| STEERING_AT_[distance]  |  Steering angle (-1.0 for full lock left to 1.0 for full lock right) recorded at specific distances (i.e 295m, 386m, 435m, 494m, 575m) |
| LEFT_DISTANCE_AT_[distance]  |  Distance from the car to the left side of the track, calculated using interpolation, recorded at specific distances (i.e 295m, 386m, 435m, 494m, 575m) |
| RIGHT_DISTANCE_AT_[distance]  |  Distance from the car to the right side of the track, calculated using interpolation, recorded at specific distances (i.e 295m, 386m, 435m, 494m, 575m) |
| FINISHING_TIME_AT_600  |  The total time (in milliseconds) taken to complete 600 meters of the lap |
| TRACK_VALID  |  Indicates whether the lap was classified as 'valid' or 'invalid' |
# Usage:

The data product is intended to be used for future data modelling to provide a racer numerous scenarios to account for different situations including finding the optimal position, throttle, and brake to minimise the lap time, specifically for the completion of the first 2 turns. A simple analysis model that can be used to analyse data is the linear regression. Other than that, there are several useful models that can be used to analyse the data, which include Ridge and Lasso regression, GAM, K-nearest neighbour. 

_Support Info:_

Contact Mamun Khan via email - z5361508@ad.unsw.edu.au

# Contributors: 

Hoang Hung Le, Trishanti Karki, Mamun Khan, Zhaoxuan Liu and Honoka Kobayashi
Dataset provided by Oracle

_How can others get involved?_ 

Others can get involved by joining the github repository, sharing feedback and contributing through pull requests. All forms of collaboration are welcome, including others reporting issues, suggesting improvements or contributing code. 





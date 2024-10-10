## Project Title: F1 Data Product

# Project Description:

# Main Objective 

To develop a comprehensive dataset using data collected in 2022, 2023 and 2024 from an F1 simulation by Oracle. This product will identify key variables that should be optimised to achieve an ideal lap time, specifically focusing on turns 1 and 2 on the race track.

# Significance  

F1 racing is becoming increasingly data-centric, with teams relying on extensive data to make strategic decisions and improve their performance. This data product will serve as a foundation for further modelling by identifying crucial factors such as braking point, turning points, and car positioning to maximise exit speed from turn 2. By leveraging these insights, teams can make informed decisions, giving their drivers a competitive edge on the track.

# Relation to  previous work 

In recent years, data analysis has become central to F1 racing, with teams leveraging Monte Carlo simulations and real-time data to improve their strategies for optimal performance. Previous efforts, particularly by teams like Oracle Red Bull Racing, have focused on collecting data related to variables such as speed, throttle, and steering inputs. Drivers like Max Verstappen use these advanced simulations to identify key factors that influence lap times and make adjustments accordingly. 
 
This project builds on Oracle’s existing data by introducing new variables and manipulating data to ultimately create a data framework. By expanding the dataset in this way, we aim to provide drivers with more detailed insights to make better-informed decisions and ultimately improve lap times. 

# Sources:

The data sources used to construct the data product are datasets provided by Oracle which contain records of variables recorded in an F1 simulation during the years 2022 - 2024. The data itself was produced via the EA F1 simulator in which various drivers raced around the track while information on relevant variables was recorded. 

The variables included in the 2022 and 2023 datasets will be used to construct data product are shown below.

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

Additional variables that were included in the 2024 are shown below along with their corresponding variable names:

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

_Brake and Throttle_ 

  -_Idea 1:_ We will take observations for any car position around turns 1 and 2, and find the average level of brake and throttle being used around Turn 1 and turn 2 by taking the average value of 5 points to the before and after (nearest the turning point).

  -_Idea 2:_ Study the trigger points for the braking point for turn 1 and the throttle point after turn 2. Before entering turn 1 the driver will apply brakes. There is no throttle being used between turns 1 and 2 since its a small distance, the driver only uses brakes and steering to control the car. He only uses throttle at any point after turn 2. We will identify these observations in the dataset. Plotting a graph of brake versus distance graph around turns 1 and 2 can help identify those trigger points. We believe that these trigger points will occur inside of the box at each turn mapped by 4 points. 

_Finish time_ 

To determine the time at which a car crossed the ‘finish line,” we will use linear interpolation using algorithm 3. The finishing line is at x = 450m. This process will be repeated for each lap.

_On-track_

The on-track value will be determined by using the algorithms 1, 2, and 4. All the car positions in the selected data set will be determined whether to be on-track or not, in order of that, the lap will be identified as valid or invalid. The selected data set here has been selected from the range of car position before the car approaches the turn 1 until it crosses the so-called finishing line, which is determined in algorithm 3. 


# Data description:

The data product will be panel data structured as a comprehensive set of observations, each representing different variables impacting the car’s performance on the track sorted by the lap in which they were recorded. 
The number of rows is dependent on the number of laps and represents the series of observations regarding key variables arranged by the session id and further sorted by the lap number. The session id represents the driver in the simulation, while the lap number represents the number of times the driver raced the track. The lap variable is classified as one that begins at the starting line, passes through turns 1 and 2 of the track and ends at a point between turns 2 and 3. Additionally, the lap number serves as a unique identifier for the recorded variables and enables a systematic analysis of how these variables impact lap time. 
Moreover, the data frame will record observations regarding key features separated into columns. These features were selected on their ability to strongly influence lap time as well as be optimised to improve these times. These features include: 
On-track: A new variable that determines whether the lap raced was valid 
Braking Point: The optimal point at which a car brakes to improves lap times
Turning Point: The optimal point at which a car turns to improve lap times
Car Position: The coordinates of the car on the track which enables the driver to determine where they should be in order to improve lap times.

# Project Status:

With a draft of the ReadMe in place, the focus shifts to creating a data frame that satisfies the design stated. This involves a multistep process required for the creation of new variables such as track validity and structuring the data frame.

_Progress:_ 

We have conducted an in-depth review of the datasets, exploring the available variables and their relevance to the final data product 
Key variables to include in the final data product have been identified, and we’ve agreed on the creation of a new variable ‘on-track?’
Discussions on algorithms and methods to apply in the development of the data product have been conducted, with ideas such as using local averaging, projection of a point onto a line, and linear interpolation considered 

_Next steps:_ 

We need to ensure that the variables in the 2024 dataset are consistent with those in the 2022 and 2023 datasets for consistency and integration all three years will be used to create the data product 
A decision needs to be made on whether to proceed with idea 1 or idea 2 regarding handling the variables for braking, turning point and throttle 


# Usage:

The data product is intended to be used for future data modelling to provide a racer numerous scenarios to account for different situations including finding the optimal position, throttle, and brake to minimise the lap time, specifically for the completion of the first 2 turns. A simple analysis model that can be used to analyse data is the linear regression. Other than that, there are several useful models that can be used to analyse the data, which include Ridge and Lasso regression, GAM, K-nearest neighbour. 

_Support Info:_

Contact Mamun Khan via email - z5361508@ad.unsw.edu.au

# Contributors: 

Hoang Hung Le, Trishanti Karki, Mamun Khan, Zhaoxuan Liu and Honoka Kobayashi
Dataset provided by Oracle

_How can others get involved?_ 

Others can get involved by joining the github repository, sharing feedback and contributing through pull requests. All forms of collaboration are welcome, including others reporting issues, suggesting improvements or contributing code. 





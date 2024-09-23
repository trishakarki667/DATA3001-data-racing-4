## Project Title: Data Frame Proposal

# Project Description:

# Main Objective 

The objective of this project is to create a comprehensive, data-driven framework using historical data obtained by Oracle via an F1 sim which encompasses the relevant variables that should be optimised in order to achieve an ideal lap. Specifically, the data frame produced will contain key variables that influence lap time during turns 1 and 2 on the race track. Through a process of leveraging algorithms to find optimal points for the variables including braking point, turning point and car position, the aim is to determine a course for the driver that maximises the exit speed from turn 2. Ultimately, by optimising the variables influencing this section of the race track, drivers can produce an ideal lap on the race track.

# Significance  

F1 is becoming increasingly data-driven. Drivers and their teams use a vast array of data to understand relevant variables, predict outcomes and make informed decisions. This project holds importance in its ability to inform driver and team decisions on the lap and hence, maximise their ability to produce the fastest time possible. Data gathered on an assortment of variables that influence the time taken between the start and the first 2 turns of the track will enable drivers to reduce their times on the track by improving their approach to these vital factors which impact lap times such as throttle, brake, turning point and braking point. An understanding of these variables will enable strategic decision-making to fine tune driver performance.  Primarily, with this data frame, drivers can pinpoint and improve the variables that will allow them to generate an optimal lap.

# Relation to  previous work 

In F1, teams rely on collecting and analysing large volumes of data to develop an optimal race strategy. Over the past few years, Oracle Red Bull Racing has captured data using F1 simulations which contain relevant variables that need to be optimised to maximise performance. With this data, they have performed countless Monte Carlo simulations to inform strategic decisions that tackle the problem of producing an ideal lap. Moreover, drivers have used these F1 sims to translate data into improvements on the race track. For instance, Max Verstappen assesses his throttle, brake and steering inputs and evaluates strategy choices. 
This project expands on the data collated by Oracle to produce a data framework with new, relevant variables including the optimal braking point, turning point and car position which will enable drivers to make more informed decisions on the track and hence, achieve improved lap times.

# Sources:

The data sources used in the construction of this product are datasets provided by Oracle which contain data on variables recorded in an F1 simulation during the years 2022 to 2024. The data itself was produced using the EA F1 simulator, in which various drivers raced around the track and as they did, information on relevant variables was collected. These variables were included as factors that influenced lap time and included amongst others:
A session identifier: A unique ID for each driver that raced in the simulation 
Lap_Num: The current lap number
Lap_Distance: The distance the vehicle has covered on the lap in metres
Throttle: The amount of throttle applied
Brake: The mount of brake applied
World Position: Various metrics on the vehicle position in relation to the track

# Workflow:

_Brake and Throttle_ 

_Idea 1:_ We will take observations for any car position around turns 1 and 2, and find the average level of brake and throttle being used around Turn 1 and turn 2 by taking the average value of 5 points to the before and after (nearest the turning point).

_Idea 2:_ Study the trigger points for the braking point for turn 1 and the throttle point after turn 2. Before entering turn 1 the driver will apply brakes. There is no throttle being used between turns 1 and 2 since its a small distance, the driver only uses brakes and steering to control the car. He only uses throttle at any point after turn 2. We will identify these observations in the dataset. Plotting a graph of brake versus distance graph around turns 1 and 2 can help identify those trigger points. We believe that these trigger points will occur inside of the box at each turn mapped by 4 points. 

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





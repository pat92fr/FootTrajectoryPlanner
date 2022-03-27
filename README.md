# FootTrajectoryPlanner
 Legged robot foot's trajectory planner based on Bezier curves
 
## Usage
Run foot_trajectory_planner.py, select the type of trajectory, and adjust parameters: velocity, stride duration, overlay and stance/swing heights.
![Foot trajectory](https://github.com/pat92fr/FootTrajectoryPlanner/blob/main/02-Result/2022-03-27%20X%20and%20Y%20Bezier%20Curves%20proposed%20by%20Pat92fr.png?raw=true)

The control points of Beziers curves maybe adapted. See line 200+ in the Python script.

The inverse kinematic function maybe adapted. It is designed for my 5-bar legged robot called Felin. See IK Python script.

## Purpose
I was looking for a foot trajectory for the swing phase of my legged robot, that suits a large range of robot velocity (from 0 to 1 m/s and more). This trajectory shall be computed in real time, and should minimize foot velocity and acceleration, and joint velocity and acceleration, in order to get a good tracking and minimal ground impact force at the begining of the stance phase. 



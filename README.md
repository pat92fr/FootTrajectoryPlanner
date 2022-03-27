# FootTrajectoryPlanner
 Legged robot foot's trajectory planner based on Bezier curves
 
## Usage
Run foot_trajectory_planner.py, select the type of trajectory, and adjust parameters: velocity, stride duration, overlay and stance/swing heights.
![Foot trajectory](https://github.com/pat92fr/FootTrajectoryPlanner/blob/main/02-Result/2022-03-27%20X%20and%20Y%20Bezier%20Curves%20proposed%20by%20Pat92fr.png?raw=true)

The control points of Beziers curves maybe adapted. See line 200+ in the Python script.

The inverse kinematic function maybe adapted. It is designed for my 5-bar legged robot called Felin. See IK Python script.

## Purpose
I was looking for a foot trajectory for the swing phase of my legged robot, that suits a large range of robot velocity (from 0 to 1 m/s and more). This trajectory shall be computed in real time, and should minimize foot velocity and acceleration, and joint velocity and acceleration, in order to get a good tracking and minimal ground impact force at the begining of the stance phase. 

### Swing curve using cos()
My very first implementation used a cosinus(t) for the swing phase. Such a trajectory causes velocity and acceleration discontinuities. I got a poor tracking and a high ground impact force at the touch down.

### Swing XZ Bezier curve 
My second implementation was based on the paper [Leg Trajectory Planning for Quadruped Robots with High-Speed Trot Gait](https://github.com/pat92fr/FootTrajectoryPlanner/blob/main/00-Papers/Leg_Trajectory_Planning_for_Quadruped_Robots_with_.pdf) comparing Bezier and Spline curves. 

So, I have defined a Bezier curve with 12 control points. 2D coordinates of control points depends on robot actual velocities, swing and stance durations (with overlay), and swing and stance heights. I got quite good tracking and the raisonable ground impact force at the touch down. 

In the §3.1, author compares Spline and Bezier curve trajectories : Comparing the swing phase trajectory acceleration of spline curve with that of the Bézier curve as shown in Figure 13, a curve with continuous acceleration cannot be obtained. Moreover, the acceleration of the Bézier curve at a contact point with the stance phase cannot reach 0, which means that there will be an impact force on the ground, and the maximum value of its acceleration curve is also larger than that in the spline curve. As to the spline curve trajectory, it will be more difficult to obtain the trajectory.

### Swing X+Z Bezier curve 
The spline method was too complex for me at the moment. So, I am trying the Bezier curve, and I think it is possible to obtain the same features of spline curve using Bezier curves : zero acceleration at the begining and the end of swing trajectory, low and continuous acceleration. I have tried several parameters with one XY Bezier curve without success. By using separates Bezier curves, one per axis, I think I have got a result very close of spline.
So, I have defined two Bezier curves (6 control points for X/Y axis, 13 points for Z vertical axis) . Coordinates of control points depends on robot actual velocities, swing and stance durations (with overlay), and swing and stance heights.


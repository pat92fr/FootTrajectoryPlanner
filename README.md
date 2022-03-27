# FootTrajectoryPlanner
 Legged robot foot's trajectory planner based on **Bezier curves**.
 
 Features :
 - Compute XZ position velocity and acceleration of foot end according desired robot velocity and gait parameters.
 - Compute position, velocity, and acceleration of joints based on IK and robot geometry.
 - Four different PRESETs including MIT-like Bezier curve.
 
## Usage
Run the Python3 script **foot_trajectory_planner.py**, select the type of trajectory, and adjust parameters:
- Desired robot velocity (mm/s)
- Stride duration (ms)
- Overlay (%)
- Stance heights (mm)
- Swing heights (mm)
- Robot standing height Z0 (mm)

![Foot trajectory](https://github.com/pat92fr/FootTrajectoryPlanner/blob/main/02-Result/2022-03-27%20XY%20Bezier%20Curve%20inspired%20from%20paper%20(MIT).png?raw=true)

- Note 1 : The control points of Beziers curves maybe adapted. See line 200+ in the Python script.
- Note 2 : The *inverse kinematic* function maybe adapted. It is designed for my 5-bar legged robot called Felin. See IK Python script.

## Purpose
I was looking for a **smooth swing phase trajectory** for my DIY legged robot, that suits a large range of robot velocity (from 0 to 1 m/s and more). This trajectory shall be computed in real time, and should minimize foot velocity and acceleration, and joint velocity and acceleration, in order to get a good tracking and minimal ground impact force at the begining of the stance phase. 

### Basic curve using math
My very first implementation was based on a **cos(t)** for both the stance and the swing phases. Such a trajectory causes velocity and acceleration discontinuities at the begining and the end of the stance/swing phases. I got a poor tracking in real experiments, and a high ground impact force at the touch down.

<p align="center"><img src="https://github.com/pat92fr/FootTrajectoryPlanner/blob/main/02-Result/XZ%20Cosinus.png"></p>
<p align="center">Figure. XZ Foot end trajectory at 1m/s.</p>

### XZ Bezier curve 
My second implementation was based on the paper [Leg Trajectory Planning for Quadruped Robots with High-Speed Trot Gait](https://github.com/pat92fr/FootTrajectoryPlanner/blob/main/00-Papers/Leg_Trajectory_Planning_for_Quadruped_Robots_with_.pdf) comparing Bezier and Spline curves. This implementation was also inspired from the Miguel Ayuso Parrilla's project log for DIY hobby servos quadruped robot [Step Trajectory and Gait Planner (from MIT cheetah)](https://hackaday.io/project/171456-diy-hobby-servos-quadruped-robot/log/178481-step-trajectory-and-gait-planner-from-mit-cheetah). 

<p align="center"><img src="https://github.com/pat92fr/FootTrajectoryPlanner/blob/main/00-Papers/Figure%2012.%20The%20Bezier%20curve%20trajectory.png"></p>

So, I have defined a **2D Bezier curve** with 12 control points. 2D coordinates of control points depends on robot actual velocities, swing and stance durations (with overlay), and swing and stance heights. I got quite good tracking and the raisonable ground impact force at the touch down. 

|Pn|X|Z|
|---|---|---|
|P0|-Vx\*Tstance/2|0|
|P1|-Vx\*(Tstance/2-Tswing/(n-1))|0|
|P2|-Vx\*(Tstance/2-2\*Tswing/(n-1))|Hswing|
|P3|-Vx\*(Tstance/2-2\*Tswing/(n-1))|Hswing|
|P4|-Vx\*(Tstance/2-2\*Tswing/(n-1))|Hswing|
|P5|0|Hswing|
|P6|0|Hswing|
|P7|0|Hswing\*1.2|
|P8|Vx\*(Tstance/2+2\*Tswing/(n-1))|Hswing\*1.2|
|P9|Vx\*(Tstance/2+2\*Tswing/(n-1))|Hswing\*1.2|
|P10|Vx\*(Tstance/2+Tswing/(n-1))|0|
|P11|Vx\*Tstance/2|0|

where :

- Tstance : Stance phase duration (s)
- Tswing : Swing phase duration (s)
- Hswing : Swing phase height (m)
- Vx : Desired robot velocity along X axis (longitudinal) (m/s)
- n = 12 : number of control points
    
<p align="center"><img src="https://github.com/pat92fr/FootTrajectoryPlanner/blob/main/02-Result/XZ%20Bezier.png"></p>
<p align="center">Figure. XZ Foot end trajectory at 1m/s.</p>

In the §3.1, author compares Spline and Bezier curve trajectories : *Comparing the swing phase trajectory acceleration of spline curve with that of the Bézier curve as shown in Figure 13, a curve with continuous acceleration cannot be obtained. Moreover, the acceleration of the Bézier curve at a contact point with the stance phase cannot reach 0, which means that there will be an impact force on the ground, and the maximum value of its acceleration curve is also larger than that in the spline curve. As to the spline curve trajectory, it will be more difficult to obtain the trajectory.*

The swing phase trajectory based on Bezier curve features a continuous acceleration along X direction, but there are **velocity and acceleration discontinuities at both ends along Z direction**.

<p align="center"><img src="https://github.com/pat92fr/FootTrajectoryPlanner/blob/main/02-Result/XZ%20Bezier%20Acceleration.png"></p>
<p align="center">Figure. XZ Foot end acceleration plot at 1m/s.</p>

### X+Z Bezier curves 
The spline method was too complex for me at the moment. So, I am trying the Bezier curve, and I thought it was possible to obtain the same features than spline curve using Bezier curves: zero acceleration at the begining and the end of swing phase, lower and continuous acceleration in both X and Z directions. I have tried several parameters with one 2D Bezier curve without success. By using separates 1D Bezier curves, one per axis, I think I have got an interesting result, very close of spline.

So, I have defined **two 1D Bezier curves (8 control points for X/Y axis, 17 points for Z vertical axis)**. Coordinates of control points depends on robot actual velocities, swing and stance durations (with overlay), and swing and stance heights.

<p align="center"><img src="https://github.com/pat92fr/FootTrajectoryPlanner/blob/main/02-Result/XZ%20Dual%20Bezier.png"></p>
<p align="center">Figure. XZ Foot end trajectory at 1m/s.</p>

|Pn|X|
|---|---|
|P0|-Vx\*Tstance/2|
|P1|-Vx\*(Tstance/2-Tswing/(n-1))|
|P2|-Vx\*(Tstance/2-2\*Tswing/(n-1))|
|P3|0|
|P4|0|
|P5|Vx\*(Tstance/2+2\*Tswing/(n-1))|
|P6|Vx\*(Tstance/2+Tswing/(n-1))|
|P7|Vx\*Tstance/2|

|Pn|Z|
|---|---|
|P0|0|
|P1|1/(n-1)\*dVz/dt\*Tswing|
|P2|2/(n-1)\*dVz/dt\*Tswing|
|P3|Hswing|
|P4|Hswing|
|P5|Hswing|
|P6|Hswing|
|P7|Hswing|
|P8|Hswing|
|P9|Hswing|
|P10|Hswing\*1.2|
|P11|Hswing\*1.2|
|P12|Hswing|
|P13|Hswing|
|P14|2/(n-1)\*dVz/dt\*Tswing|
|P15|1/(n-1)\*dVz/dt\*Tswing|
|P16|0|

where :

- dVz/dt : derivative of Z velocity of stance phase trajectory = Hstance\*PI/Tstance

The swing phase trajectory based on these two Bezier curves features a continuous acceleration along both X and Z directions. *Houra!*

<p align="center"><img src="https://github.com/pat92fr/FootTrajectoryPlanner/blob/main/02-Result/XZ%20Dual%20Bezier%20Acceleration.png"></p>
<p align="center">Figure. XZ Foot end acceleration at 1m/s.</p>

The result is very close of the spline curve acceleration along X and Z direction.

<p align="center"><img src="https://github.com/pat92fr/FootTrajectoryPlanner/blob/main/00-Papers/Figure%2013.%20The%20spline%20curve%20acceleration%20X%20and%20Z%20axis.png"></p>
<p align="center">XZ Foot end acceleration at 1..4m/s;  (a) The acceleration in the X diretion for the spline curve trajectory;  (b) The acceleration in the Z direction for the spline curve trajectory.</p>


![Foot trajectory](https://github.com/pat92fr/FootTrajectoryPlanner/blob/main/02-Result/2022-03-27%20X%20and%20Y%20Bezier%20Curves%20proposed%20by%20Pat92fr.png?raw=true)
<p align="center">Screenshot. Two Bezier curves analysis.</p>

### Circle trajectory (test)

![Foot trajectory](https://github.com/pat92fr/FootTrajectoryPlanner/blob/main/02-Result/2022-03-27%20Circle%20trajectory%20test.png?raw=true)
<p align="center">Screenshot. Circle analysis.</p>





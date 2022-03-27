#ik.py

import numpy as np 
import math

from felin_geometry import *

##DEBUG #######################################################################

# TRACE macro
DEBUG = False

def log(s):
    if DEBUG:
        print(s)

##DEBUG #######################################################################

# S1 : 0 = X aligned, to the front
# S2 : 0 = X aligned, to the front
# S3 : 0 = Z aligned, to the floor

# S1 : default position, front tibia is HOR, to the front, angle = 0
# S2 : default position, rear tibia is HOR, to the rear, angle = 180
# S3 : default position, legs are VER, angle = 0

# S1 is positive, CW
# S2 is positive, CW
# S3 is positive, CW

def normalize_positive(a_rad):
	if a_rad < 0:
		return a_rad + 2.0*math.pi
	else:
		return a_rad

def cos_law_c(a,b,angle):
	return math.sqrt(a**2+b**2-2*a*b*math.cos(angle))

def cos_law_A(a,b,c):
	return math.acos( (a**2+b**2-c**2) / (2*a*b) )

# return 3x1 vector (S1 (front hip servo), S2 (rear hip  servo), S3 (coxa servo)) in RADIANS
def ik2(foot_position): # input 3x1 vector  (x,y,z,1) in METERS, where x axis pointing forward, y axis pointing int or exterior, and z axis pointing upward
	log("foot_position:\n"+str(foot_position))
	# coxa to foot distance
	CF = math.sqrt((foot_position[1,0]+Lc)**2+foot_position[2,0]**2)
	log("CF: "+str(CF))
	# bound CF
	CFmin = math.sqrt(Lc**2+Lmin**2)
	CFmax = math.sqrt(Lc**2+Lmax**2)
	CF = min(CFmax,max(CF,CFmin))
	log("CFbounded: "+str(CF))
	# hips to foot distance
	HFsq = CF**2-Lc**2
	HF = math.sqrt(HFsq)
	log("HF: "+str(HF))
	# foot - coxa - hips angle
	FCH = math.acos((CF**2+Lc**2-HFsq)/(2*CF*Lc))
	log("FCH: "+str(round(math.degrees(FCH),0))+"deg")
	# coxa angle
	A3 = math.pi/2 - math.atan2(Lc-foot_position[1,0],-foot_position[2,0]) - FCH
	log("A3: "+str(round(math.degrees(A3),0))+"deg")

	# compute angle and elongation of the leg, in the xz' (coxa plane)
	L = math.sqrt(foot_position[0,0]**2 + HFsq)
	Alpha = math.atan2(HF,foot_position[0,0]);
	log("L: "+str(round(L,3)))
	log("Alpha: "+str(round(math.degrees(Alpha),0)))

	# bound max elongation
	if(L>Lmax):
		L = Lmax
	if(L<Lmin):
		L = Lmin
	log("Lbounded: "+str(round(L,3)))		
	# take in account Lbounded
	x = L * math.cos(Alpha)
	z = -L * math.sin(Alpha)
	log("x: "+str(round(x,3)))		
	log("z: "+str(round(z,3)))		

	# compute distance from front HIP to foot in coxa plane
	FH_to_FOOT_distance = cos_law_c(H2H_distance/2.0,L,Alpha)
	log("FH_to_FOOT_distance: "+str(round(FH_to_FOOT_distance,3)))			
	# compute angle from front HIP to foot in coxa plane
	FH_to_FOOT_angle=math.atan2(-z,x-H2H_distance/2.0);
	log("FH_to_FOOT_angle: "+str(round(math.degrees(FH_to_FOOT_angle),0))+"deg")
	# compute angle from front HIP to femur in coxa plane
	A1 = FH_to_FOOT_angle-cos_law_A(FH_to_FOOT_distance,Lf,Lt)
	log("A1: "+str(round(math.degrees(A1),0))+"deg")

	# compute distance from rear HIP to foot in coxa plane
	RH_to_FOOT_distance = cos_law_c(H2H_distance/2.0,L,math.pi-Alpha)
	log("RH_to_FOOT_distance: "+str(round(RH_to_FOOT_distance,3)))			
	# compute angle from rear HIP to foot in coxa plane
	RH_to_FOOT_angle=math.atan2(-z,x+H2H_distance/2.0);
	log("RH_to_FOOT_angle: "+str(round(math.degrees(RH_to_FOOT_angle),0))+"deg")
	# compute angle from front HIP to femur in coxa plane
	A2 = RH_to_FOOT_angle+cos_law_A(RH_to_FOOT_distance,Lf,Lt)
	log("A2: "+str(round(math.degrees(A2),0))+"deg")

	return np.array((A1,A2,A3)).reshape((3,1))


if __name__ == "__main__":
	print("Test Unitaire ik.py")
	foot_position = np.zeros((3,1)) # x,y,z
	foot_position[0,0] =  0.000
	foot_position[1,0] = -0.000
	foot_position[2,0] = -0.1152
	print(foot_position)
	leg_joint_angles = ik2(foot_position) # A,B
	print(np.round(np.degrees(leg_joint_angles),1))
	# return 0.0 180.0 0.0
	print('*****************************************************')

	foot_position[0,0] =  0.000
	foot_position[1,0] = -0.000
	foot_position[2,0] = -0.160
	print(foot_position)
	leg_joint_angles = ik2(foot_position) # A,B
	print(np.round(np.degrees(leg_joint_angles),1))
	# return 27.4 152.6 0.0
	print('*****************************************************')


# Copyright © 2022, Pat92fr

# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the “Software”), to 
# deal in the Software without restriction, including without limitation the 
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.

# The Software is provided “as is”, without warranty of any kind, express or
# implied, including but not limited to the warranties of merchantability, 
# fitness for a particular purpose and noninfringement. In no event shall the
# authors or copyright holders X be liable for any claim, damages or other 
# liability, whether in an action of contract, tort or otherwise, arising from,
# out of or in connection with the software or the use or other dealings in the
# Software.

# Except as contained in this notice, the name of the <copyright holders> shall
# not be used in advertising or otherwise to promote the sale, use or other 
# dealings in this Software without prior written authorization from Pat92fr.

from tkinter import *
import numpy as np
import math
import bezier
import matplotlib.pyplot as plt
import ik

class gui:

	def __init__(self,window):
		self.window = window

		self.lf_inputs = LabelFrame(window, text="Parameters", width=1000)
		self.lf_graphs = Frame(window)

		self.lf_inputs.grid(column = 0, row = 0, sticky='nsew')		
		self.lf_graphs.grid(column = 1, row = 0, sticky='nsew')		
		
		self.window.columnconfigure(1, weight=1)
		#self.window.rowconfigure(1, weight=1)

		self.radio = {}
		self.labels = {}
		self.scales = {}
		self.viewports = {}
		self.variables = {}

		# plot button
		button_update = Button(window,text="Plot All",command = self.plotter)
		button_update.grid(column = 0, row =1, sticky='nsew')

		self.row = 0

		# radio button
		curve_name = ["Circle(test)","Cosinus","XZ Bezier curve","X+Z Bezier curves"]
		curve_value = ["Circle","Cosinus","MIT","Pat92fr"]
		self.variables["Curve"] = StringVar()
		self.variables["Curve"].set(curve_value[0])
		for i in range(4):
			self.radio["Curve"+str(i)] = Radiobutton(self.lf_inputs,variable=self.variables["Curve"],text=curve_name[i],value=curve_value[i],command=self.update)
			self.radio["Curve"+str(i)].grid(column = 0, row = self.row, sticky='w')
			self.row += 1

		self.labels["vx"] = Label(self.lf_inputs, text="Vx (mm/s)", anchor="w", justify=LEFT)
		self.labels["vx"].grid(column = 0, row = self.row, sticky='w')
		self.scales["vx"] = Scale(self.lf_inputs, from_=0, to=3000, tickinterval=2000, orient=HORIZONTAL)
		self.scales["vx"].grid(column = 1, row = self.row, sticky='w')
		self.scales["vx"].bind("<ButtonRelease>", self.scale_handler)
		self.scales["vx"].set(1000)
		self.row += 1

		self.labels["Tstride"] = Label(self.lf_inputs, text="Tstride (ms)", anchor="w", justify=LEFT)
		self.labels["Tstride"].grid(column = 0, row = self.row, sticky='w')
		self.scales["Tstride"] = Scale(self.lf_inputs, from_=350, to=800, tickinterval=500, orient=HORIZONTAL)
		self.scales["Tstride"].grid(column = 1, row = self.row, sticky='w')
		self.scales["Tstride"].bind("<ButtonRelease>", self.scale_handler)
		self.scales["Tstride"].set(400)
		self.row += 1

		self.labels["Overlay"] = Label(self.lf_inputs, text="Overlay (%)", anchor="w", justify=LEFT)
		self.labels["Overlay"].grid(column = 0, row = self.row, sticky='w')
		self.scales["Overlay"] = Scale(self.lf_inputs, from_=0, to=15, tickinterval=10, orient=HORIZONTAL)
		self.scales["Overlay"].grid(column = 1, row = self.row, sticky='w')
		self.scales["Overlay"].bind("<ButtonRelease>", self.scale_handler)
		self.scales["Overlay"].set(0)
		self.row += 1

		self.labels["Hswing"] = Label(self.lf_inputs, text="Swing Height (mm)", anchor="w", justify=LEFT)
		self.labels["Hswing"].grid(column = 0, row = self.row, sticky='w')
		self.scales["Hswing"] = Scale(self.lf_inputs, from_=0, to=100, tickinterval=50, orient=HORIZONTAL)
		self.scales["Hswing"].grid(column = 1, row = self.row, sticky='w')
		self.scales["Hswing"].bind("<ButtonRelease>", self.scale_handler)
		self.scales["Hswing"].set(30)
		self.row += 1

		self.labels["Hstance"] = Label(self.lf_inputs, text="Stance Height (mm)", anchor="w", justify=LEFT)
		self.labels["Hstance"].grid(column = 0, row = self.row, sticky='w')
		self.scales["Hstance"] = Scale(self.lf_inputs, from_=0, to=25, tickinterval=10, orient=HORIZONTAL)
		self.scales["Hstance"].grid(column = 1, row = self.row, sticky='w')
		self.scales["Hstance"].bind("<ButtonRelease>", self.scale_handler)
		self.scales["Hstance"].set(5)
		self.row += 1

		self.labels["Z0"] = Label(self.lf_inputs, text="Standing Height (mm)", anchor="w", justify=LEFT)
		self.labels["Z0"].grid(column = 0, row = self.row, sticky='w')
		self.scales["Z0"] = Scale(self.lf_inputs, from_=100, to=300, tickinterval=100, orient=HORIZONTAL)
		self.scales["Z0"].grid(column = 1, row = self.row, sticky='w')
		self.scales["Z0"].bind("<ButtonRelease>", self.scale_handler)
		self.scales["Z0"].set(130)
		self.row += 1

		self.row = 0
	
		self.lf_graphs.columnconfigure(0, weight=1)
		self.lf_graphs.columnconfigure(1, weight=1)

		self.labels["XZ_position"] = Label(self.lf_graphs, text="XZ position (m)", anchor="w", justify=LEFT)
		self.labels["XZ_position"].grid(column = 0, row = self.row, sticky='w')
		self.row += 1

		self.viewports['XZ_position'] = Canvas(self.lf_graphs, bg="#FFFFFF") #, width=viewport_max_x, height=viewport_size_y_pos, bg="#FFFFFF")
		self.viewports["XZ_position"].grid(column = 0, row = self.row, sticky='we')
		self.row += 1

		self.labels["XZ_velocity"] = Label(self.lf_graphs, text="XZ velocity (m/s)", anchor="w", justify=LEFT)
		self.labels["XZ_velocity"].grid(column = 0, row = self.row, sticky='w')
		self.row += 1

		self.viewports['XZ_velocity'] = Canvas(self.lf_graphs, bg="#FFFFFF") #, width=viewport_max_x, height=viewport_size_y_pos, bg="#FFFFFF")
		self.viewports["XZ_velocity"].grid(column = 0, row = self.row, sticky='we')
		self.row += 1

		self.labels["XZ_acceleration"] = Label(self.lf_graphs, text="XZ acceleration (m/s²)", anchor="w", justify=LEFT)
		self.labels["XZ_acceleration"].grid(column = 0, row = self.row, sticky='w')
		self.row += 1

		self.viewports['XZ_acceleration'] = Canvas(self.lf_graphs, bg="#FFFFFF") #, width=viewport_max_x, height=viewport_size_y_pos, bg="#FFFFFF")
		self.viewports["XZ_acceleration"].grid(column = 0, row = self.row, sticky='we')
		self.row += 1

		self.row = 0
	
		self.labels["Joint_Position"] = Label(self.lf_graphs, text="Joint position (°)", anchor="w", justify=LEFT)
		self.labels["Joint_Position"].grid(column = 1, row = self.row, sticky='w')
		self.row += 1

		self.viewports['Joint_Position'] = Canvas(self.lf_graphs, bg="#FFFFFF") #, width=viewport_max_x, height=viewport_size_y_pos, bg="#FFFFFF")
		self.viewports["Joint_Position"].grid(column = 1, row = self.row, sticky='we')
		self.row += 1

		self.labels["Joint_Velocity"] = Label(self.lf_graphs, text="Joint velocity (°/s)", anchor="w", justify=LEFT)
		self.labels["Joint_Velocity"].grid(column = 1, row = self.row, sticky='w')
		self.row += 1

		self.viewports['Joint_Velocity'] = Canvas(self.lf_graphs, bg="#FFFFFF") #, width=viewport_max_x, height=viewport_size_y_pos, bg="#FFFFFF")
		self.viewports["Joint_Velocity"].grid(column = 1, row = self.row, sticky='we')
		self.row += 1

		self.labels["Joint_Acceleration"] = Label(self.lf_graphs, text="Joint acceleration (°/s²)", anchor="w", justify=LEFT)
		self.labels["Joint_Acceleration"].grid(column = 1, row = self.row, sticky='w')
		self.row += 1

		self.viewports['Joint_Acceleration'] = Canvas(self.lf_graphs, bg="#FFFFFF") #, width=viewport_max_x, height=viewport_size_y_pos, bg="#FFFFFF")
		self.viewports["Joint_Acceleration"].grid(column = 1, row = self.row, sticky='we')
		self.row += 1


	def scale_handler(self, event):
		self.update()

	def update(self):
		for n,c in self.viewports.items():
			c.delete("all")

		# parameters
		T_stride_s = self.scales["Tstride"].get()/1000.0
		overlay = self.scales["Overlay"].get()/100.0

		self.T_stance_s = T_stride_s * (0.5+overlay) # 0.200
		self.T_swing_s = T_stride_s * (0.5-overlay) # 0.200
		H_stance_m = self.scales["Hstance"].get()/1000.0 # 0.005
		H_swing_m = self.scales["Hswing"].get()/1000.0  # 0.040
		Z0 = -self.scales["Z0"].get()/1000.0
		Vx_mps = self.scales["vx"].get()/1000.0+0.001

		x_begin = -Vx_mps * (0.5) * self.T_stance_s
		x_end   =  Vx_mps * (0.5) * self.T_stance_s

		x_points = None
		z_points = None

		if self.variables["Curve"].get() == "MIT":

			n = 12 # point count in x_points
			A = Vx_mps*self.T_swing_s/(n-1)
			B = 2.00*A

			# XZ Bezier curve
			xz_points = np.array( 
				[ 
					[ x_begin,  	0.0,  0.0 ],  		# P0
					[ x_begin-A,  	0.0,  0.0 ],  		# P1
					[ x_begin-B,  	0.0,  H_swing_m ],  # P2
					[ x_begin-B,  	0.0,  H_swing_m ],  # P3
					[ x_begin-B,  	0.0,  H_swing_m ],  # P4
					[ 0.0,  		0.0,  H_swing_m ],  # P5
					[ 0.0,  		0.0,  H_swing_m ],  # P6
					[ 0.0,  		0.0,  H_swing_m*1.2 ],  # P7
					[ x_end+B,  	0.0,  H_swing_m*1.2 ],  # P8
					[ x_end+B,  	0.0,  H_swing_m*1.2 ],  # P9
					[ x_end+A,  	0.0,  0.0 ],  		# P10
					[ x_end,  		0.0,  0.0 ]  		# P11
				]
			).transpose()

		if self.variables["Curve"].get() == "Pat92fr":

			xn = 8 # point count in x_points
			A = Vx_mps*self.T_swing_s/(xn-1)
			B = 2.00*A

			# X Bezier curve
			x_points = [ 
				x_begin,  	# C0 begin
				x_begin-A,  # C1 zero speed
				x_begin-B,  # C2 zero speed
				0,
				0,
				x_end+B,  	# C3 zero speed
				x_end+A,  	# C4 zero speed
				x_end,     	# C5
			]

			zn = 17 # point count in x_points
			A = 1.00/(zn-1)*H_stance_m*math.pi*self.T_swing_s/self.T_stance_s
			B = 2.00*A
			
			# Z Bezier curve
			z_points = [ 
					0.0,  	# C0
					A,  	# C1
					B,  	# C2
					H_swing_m*1.0,  # C3
					H_swing_m*1.0,  # C3
					H_swing_m*1.0,  # C3
					H_swing_m*1.0,  # C3
					H_swing_m*1.0,  # C3
					H_swing_m*1.0,  # C4
					H_swing_m*1.0,  # C5
					H_swing_m*1.2,  # C6
					H_swing_m*1.2,  # C7
					H_swing_m*1.0,  # C8
					H_swing_m*1.0,  # C9
					B,  	# C10
					A,  	# C11
					0.0  	# C12
			]

		# build data
		self.step_s = 0.0005 # s 

		# .. for stride XZ position
		self.x_dataset = []
		self.z_dataset = []
		x_min = 1.000
		x_max = -1.000
		z_min = 1.000
		z_max = -1.000

		for t in np.arange(self.step_s,self.T_stance_s,self.step_s):
			multiplier = t/self.T_stance_s
			x = -Vx_mps * (multiplier-0.5) * self.T_stance_s
			z = Z0-H_stance_m * math.cos(math.pi*(multiplier-0.5))
			
			# circle test
			if self.variables["Curve"].get() == "Circle":
				r = 0.04
				x = r*math.cos(math.pi*2*t/(self.T_stance_s+self.T_swing_s))
				z = Z0+r*math.sin(math.pi*2*t/(self.T_stance_s+self.T_swing_s))

			self.x_dataset.append(x)
			self.z_dataset.append(z)
			x_max = max(x,x_max)
			x_min = min(x,x_min)
			z_max = max(z,z_max)
			z_min = min(z,z_min)

		for t in np.arange(0,self.T_swing_s+self.step_s,self.step_s):
			multiplier = t/self.T_swing_s
			x = 0
			z = 0

			if self.variables["Curve"].get() == "Circle":
				r = 0.04
				x = r*math.cos(math.pi*2*(t+self.T_stance_s)/(self.T_stance_s+self.T_swing_s))
				z = r*math.sin(math.pi*2*(t+self.T_stance_s)/(self.T_stance_s+self.T_swing_s))

			if self.variables["Curve"].get() == "MIT":
				p = bezier.bezier(multiplier,xz_points)
				x = p[0,0]
				z = p[2,0]
			
			if self.variables["Curve"].get() == "Pat92fr":
				x = bezier.bezier1D(multiplier,x_points)
				z = bezier.bezier1D(multiplier,z_points)

			if self.variables["Curve"].get() == "Cosinus":
				x = Vx_mps * (multiplier-0.5) * self.T_stance_s
				z = H_swing_m * math.cos(math.pi*(multiplier-0.5))
			
			z = z + Z0

			self.x_dataset.append(x)
			self.z_dataset.append(z)
			x_max = max(x,x_max)
			x_min = min(x,x_min)
			z_max = max(z,z_max)
			z_min = min(z,z_min)
			
		self.x_dataset.append(self.x_dataset[0])
		self.z_dataset.append(self.z_dataset[0])

		# .. for stride XZ velocity
		self.vx_dataset = []
		self.vz_dataset = []
		vx_min = 1.000
		vx_max = -1.000
		vz_min = 1.000
		vz_max = -1.000

		vx_index_start = int(0.5*self.T_stance_s/self.step_s)
		
		for i in range(len(self.x_dataset)-1): 
			current = (vx_index_start+i)%(len(self.x_dataset)-1)
			past = current-1
			if past < 0:
				past = len(self.x_dataset)-1-1
			vx =(self.x_dataset[current]-self.x_dataset[past])/self.step_s
			vz =(self.z_dataset[current]-self.z_dataset[past])/self.step_s
			self.vx_dataset.append(vx)
			self.vz_dataset.append(vz)
			vx_max = max(vx,vx_max)
			vx_min = min(vx,vx_min)
			vz_max = max(vz,vz_max)
			vz_min = min(vz,vz_min)
		
		# .. for stride XZ acceleration
		self.ax_dataset = []
		self.az_dataset = []
		ax_min = 1.000
		ax_max = -1.000
		az_min = 1.000
		az_max = -1.000
		
		for i in range(len(self.vx_dataset)-1): 
			ax =(self.vx_dataset[i+1]-self.vx_dataset[i])/self.step_s
			az =(self.vz_dataset[i+1]-self.vz_dataset[i])/self.step_s
			self.ax_dataset.append(ax)
			self.az_dataset.append(az)
			ax_max = max(ax,ax_max)
			ax_min = min(ax,ax_min)
			az_max = max(az,az_max)
			az_min = min(az,az_min)

		# .. for joint position
		self.coxa_dataset = []
		self.front_hips_dataset = []
		self.rear_hips_dataset = []
		coxa_min = 180.0
		coxa_max = -180.0
		front_hips_min = 180.0
		front_hips_max = -180.0
		rear_hips_min = 180.0
		rear_hips_max = -180.0

		x_index_start = int(0.5*self.T_stance_s/self.step_s)

		for i in range(len(self.x_dataset)-1): 
			current = (x_index_start+i)%(len(self.x_dataset)-1)		
			foot_position = np.zeros((3,1)) # x,y,z
			foot_position[0,0] =  self.x_dataset[current]
			foot_position[1,0] =  0.0
			foot_position[2,0] =  self.z_dataset[current]
			#print(foot_position)
			leg_joint_angles = ik.ik2(foot_position) # A,B
			final_joint_angles = np.degrees(leg_joint_angles)
			self.coxa_dataset.append(final_joint_angles[2,0])
			self.front_hips_dataset.append(final_joint_angles[0,0])
			self.rear_hips_dataset.append(final_joint_angles[1,0])
			coxa_max = max(final_joint_angles[2,0],coxa_max)
			coxa_min = min(final_joint_angles[2,0],coxa_min)
			front_hips_max = max(final_joint_angles[0,0],front_hips_max)
			front_hips_min = min(final_joint_angles[0,0],front_hips_min)
			rear_hips_max = max(final_joint_angles[1,0],rear_hips_max)
			rear_hips_min = min(final_joint_angles[1,0],rear_hips_min)

		# .. for joint velocity
		self.v_coxa_dataset = []
		self.v_front_hips_dataset = []
		self.v_rear_hips_dataset = []
		v_coxa_min = 36000.0
		v_coxa_max = -36000.0
		v_front_hips_min = 36000.0
		v_front_hips_max = -36000.0
		v_rear_hips_min = 36000.0
		v_rear_hips_max = -36000.0

		for i in range(len(self.coxa_dataset)-1): 
			v_coxa =(self.coxa_dataset[i+1]-self.coxa_dataset[i])/self.step_s
			v_front_hips =(self.front_hips_dataset[i+1]-self.front_hips_dataset[i])/self.step_s
			v_rear_hips =(self.rear_hips_dataset[i+1]-self.rear_hips_dataset[i])/self.step_s
			self.v_coxa_dataset.append(v_coxa)
			self.v_front_hips_dataset.append(v_front_hips)
			self.v_rear_hips_dataset.append(v_rear_hips)
			v_coxa_max = max(v_coxa_max,v_coxa)
			v_coxa_min = min(v_coxa_min,v_coxa)
			v_front_hips_max = max(v_front_hips_max,v_front_hips)
			v_front_hips_min = min(v_front_hips_min,v_front_hips)
			v_rear_hips_max = max(v_rear_hips_max,v_rear_hips)
			v_rear_hips_min = min(v_rear_hips_min,v_rear_hips)

		# .. for joint acceleration
		self.a_coxa_dataset = []
		self.a_front_hips_dataset = []
		self.a_rear_hips_dataset = []
		a_coxa_min = 36000.0
		a_coxa_max = -36000.0
		a_front_hips_min = 36000.0
		a_front_hips_max = -36000.0
		a_rear_hips_min = 36000.0
		a_rear_hips_max = -36000.0

		for i in range(len(self.v_coxa_dataset)-1): 
			a_coxa =(self.v_coxa_dataset[i+1]-self.v_coxa_dataset[i])/self.step_s
			a_front_hips =(self.v_front_hips_dataset[i+1]-self.v_front_hips_dataset[i])/self.step_s
			a_rear_hips =(self.v_rear_hips_dataset[i+1]-self.v_rear_hips_dataset[i])/self.step_s
			self.a_coxa_dataset.append(a_coxa)
			self.a_front_hips_dataset.append(a_front_hips)
			self.a_rear_hips_dataset.append(a_rear_hips)
			a_coxa_max = max(a_coxa_max,a_coxa)
			a_coxa_min = min(a_coxa_min,a_coxa)
			a_front_hips_max = max(a_front_hips_max,a_front_hips)
			a_front_hips_min = min(a_front_hips_min,a_front_hips)
			a_rear_hips_max = max(a_rear_hips_max,a_rear_hips)
			a_rear_hips_min = min(a_rear_hips_min,a_rear_hips)

		# trace data

		# .. for stride XZ position
		x_view_size = self.viewports['XZ_position'].winfo_width()
		y_view_size = self.viewports['XZ_position'].winfo_height()

		# compute scale
		x_scale_m_per_pixel = x_view_size/(x_max-x_min)
		y_scale_m_per_pixel = y_view_size/(z_max-z_min)
		scale_m_per_pixel = min(x_scale_m_per_pixel,y_scale_m_per_pixel)*0.9

		# compute mediam postion
		x_middle_m = (x_max+x_min)/2.0
		z_middle_m = (z_max+z_min)/2.0

		for z in np.arange(Z0-0.050,Z0+0.100,0.010):
			self.viewports['XZ_position'].create_line(
				0,
				-(z-z_middle_m)*scale_m_per_pixel+y_view_size/2.0,
				x_view_size,
				-(z-z_middle_m)*scale_m_per_pixel+y_view_size/2.0,
				width=1,
				fill="#DDDDDD"
			)

		for x in np.arange(-1.00,1.00,0.010):
			_color = "#DDDDDD"
			_width = 1
			if (abs(int(round(x,3)*100.0)) % 10) == 0 :
				_width = 1		
				_color = "#BBBBBB"		
			if round(x,3) == 0.0 :
				_width = 2		
				_color = "#999999"

			self.viewports['XZ_position'].create_line(
				(x-x_middle_m)*scale_m_per_pixel+x_view_size/2.0,
				0,
				(x-x_middle_m)*scale_m_per_pixel+x_view_size/2.0,
				y_view_size,
				width=_width,
				fill=_color
			)

		for i in range(len(self.x_dataset)-1): 
			self.viewports['XZ_position'].create_line(
				(self.x_dataset[i]-x_middle_m)*scale_m_per_pixel+x_view_size/2.0,
				-(self.z_dataset[i]-z_middle_m)*scale_m_per_pixel+y_view_size/2.0,
				(self.x_dataset[i+1]-x_middle_m)*scale_m_per_pixel+x_view_size/2.0,
				-(self.z_dataset[i+1]-z_middle_m)*scale_m_per_pixel+y_view_size/2.0,
				width=2,
				fill="#0000FF"
			)

		#self.viewports['XZ_position'].create_rectangle(6,10,120,90,fill="white",outline="white")
		self.viewports['XZ_position'].create_text(10,10,anchor="nw",justify='left',text="Stride length   "+str((round(Vx_mps * self.T_stance_s,3)))+" m", fill="#0000FF", font=('Consolas 11 bold'))
		self.viewports['XZ_position'].create_text(10,30,anchor="nw",justify='left',text="Stance duration "+str((round(self.T_stance_s,3)))+" s", fill="#0000FF", font=('Consolas 11 bold'))
		self.viewports['XZ_position'].create_text(10,50,anchor="nw",justify='left',text="Swing duration  "+str((round(self.T_swing_s,3)))+" s", fill="#0000FF", font=('Consolas 11 bold'))
 
		# .. for stride XZ velocity
		vx_view_size = self.viewports['XZ_velocity'].winfo_width()
		vy_view_size = self.viewports['XZ_velocity'].winfo_height()

		for v in np.arange(-10.000,10.000,0.500):
			_color = "#DDDDDD"
			_width = 1
			if round(v,1) % 1.0 == 0.00 :
				_width = 1		
				_color = "#BBBBBB"		
			if round(v,1) == 0.0 :
				_width = 2		
				_color = "#999999"	
			self.viewports['XZ_velocity'].create_line(
				0,
				self.viewport_scale(v,min(vx_min,vz_min),max(vx_max,vz_max),vy_view_size,"y",0.05),
				vx_view_size,
				self.viewport_scale(v,min(vx_min,vz_min),max(vx_max,vz_max),vy_view_size,"y",0.05),
				width=_width,
				fill=_color
			)

		for i in range(len(self.vx_dataset)-1): 
			self.viewports['XZ_velocity'].create_line(
				self.viewport_scale(i,0,len(self.vx_dataset),vx_view_size,"x"),
				self.viewport_scale(self.vx_dataset[i],min(vx_min,vz_min),max(vx_max,vz_max),vy_view_size,"y",0.05),
				self.viewport_scale(i+1,0,len(self.vx_dataset),vx_view_size,"x"),
				self.viewport_scale(self.vx_dataset[i+1],min(vx_min,vz_min),max(vx_max,vz_max),vy_view_size,"y",0.05),
				width=2,
				fill="#FF0000"
			)
			self.viewports['XZ_velocity'].create_line(
				self.viewport_scale(i,0,len(self.vx_dataset),vx_view_size,"x"),
				self.viewport_scale(self.vz_dataset[i],min(vx_min,vz_min),max(vx_max,vz_max),vy_view_size,"y",0.05),
				self.viewport_scale(i+1,0,len(self.vx_dataset),vx_view_size,"x"),
				self.viewport_scale(self.vz_dataset[i+1],min(vx_min,vz_min),max(vx_max,vz_max),vy_view_size,"y",0.05),
				width=2,
				fill="#00FF00"
			)

		self.viewports['XZ_velocity'].create_rectangle(6,10,120,90,fill="white",outline="white")
		self.viewports['XZ_velocity'].create_text(10,10,anchor="nw",justify='left',text="X max "+str((round(vx_max,1)))+" m/s", fill="#FF0000", font=('Consolas 11 bold'))
		self.viewports['XZ_velocity'].create_text(10,30,anchor="nw",justify='left',text="  min "+str((round(vx_min,1)))+" m/s", fill="#FF0000", font=('Consolas 11 bold'))
		self.viewports['XZ_velocity'].create_text(10,50,anchor="nw",justify='left',text="Z max "+str((round(vz_max,1)))+" m/s", fill="#00AA00", font=('Consolas 11 bold'))
		self.viewports['XZ_velocity'].create_text(10,70,anchor="nw",justify='left',text="  min "+str((round(vz_min,1)))+" m/s", fill="#00AA00", font=('Consolas 11 bold'))
 
		# .. for stride XZ acceleration
		ax_view_size = self.viewports['XZ_acceleration'].winfo_width()
		ay_view_size = self.viewports['XZ_acceleration'].winfo_height()

		for a in np.arange(-200.000,200.000,10.00):
			_color = "#DDDDDD"
			_width = 1
			if round(a,1) % 50.0 == 0.00 :
				_width = 1		
				_color = "#BBBBBB"		
			if round(a,1) == 0.0 :
				_width = 2		
				_color = "#999999"	
			self.viewports['XZ_acceleration'].create_line(
				0,
				self.viewport_scale(a,min(ax_min,az_min),max(ax_max,az_max),ay_view_size,"y",0.05),
				vx_view_size,
				self.viewport_scale(a,min(ax_min,az_min),max(ax_max,az_max),ay_view_size,"y",0.05),
				width=_width,
				fill=_color
			)

		for i in range(len(self.ax_dataset)-1): 
			self.viewports['XZ_acceleration'].create_line(
				self.viewport_scale(i,0,len(self.ax_dataset),ax_view_size,"x"),
				self.viewport_scale(self.ax_dataset[i],min(ax_min,az_min),max(ax_max,az_max),ay_view_size,"y",0.05),
				self.viewport_scale(i+1,0,len(self.ax_dataset),ax_view_size,"x"),
				self.viewport_scale(self.ax_dataset[i+1],min(ax_min,az_min),max(ax_max,az_max),ay_view_size,"y",0.05),
				width=2,
				fill="#FF0000"
			)
			self.viewports['XZ_acceleration'].create_line(
				self.viewport_scale(i,0,len(self.ax_dataset),ax_view_size,"x"),
				self.viewport_scale(self.az_dataset[i],min(ax_min,az_min),max(ax_max,az_max),ay_view_size,"y",0.05),
				self.viewport_scale(i+1,0,len(self.ax_dataset),ax_view_size,"x"),
				self.viewport_scale(self.az_dataset[i+1],min(ax_min,az_min),max(ax_max,az_max),ay_view_size,"y",0.05),
				width=2,
				fill="#00FF00"
			)

		self.viewports['XZ_acceleration'].create_rectangle(6,10,120,90,fill="white",outline="white")
		self.viewports['XZ_acceleration'].create_text(10,10,anchor="nw",justify='left',text="X max "+str(int(round(ax_max,0)))+" m/s²", fill="#FF0000", font=('Consolas 11 bold'))
		self.viewports['XZ_acceleration'].create_text(10,30,anchor="nw",justify='left',text="  min "+str(int(round(ax_min,0)))+" m/s²", fill="#FF0000", font=('Consolas 11 bold'))
		self.viewports['XZ_acceleration'].create_text(10,50,anchor="nw",justify='left',text="Z max "+str(int(round(az_max,0)))+" m/s²", fill="#00AA00", font=('Consolas 11 bold'))
		self.viewports['XZ_acceleration'].create_text(10,70,anchor="nw",justify='left',text="  min "+str(int(round(az_min,0)))+" m/s²", fill="#00AA00", font=('Consolas 11 bold'))
 
		# .. for joint position
		jpx_view_size = self.viewports['Joint_Position'].winfo_width()
		jpy_view_size = self.viewports['Joint_Position'].winfo_height()

		mi = min(coxa_min,front_hips_min,rear_hips_min)
		ma = max(coxa_max,front_hips_max,rear_hips_max)

		for angle in np.arange(-90.0,270.0,90.0):
			_color = "#DDDDDD"
			_width = 1
			if round(angle,1) % 90.0 == 0.00 :
				_width = 1		
				_color = "#BBBBBB"		
			if round(angle,1) == 0.0 :
				_width = 2		
				_color = "#999999"	
			self.viewports['Joint_Position'].create_line(
				0,
				self.viewport_scale(angle,mi,ma,jpy_view_size,"y",0.05),
				jpx_view_size,
				self.viewport_scale(angle,mi,ma,jpy_view_size,"y",0.05),
				width=_width,
				fill=_color
			)

		for i in range(len(self.front_hips_dataset)-1): 
			self.viewports['Joint_Position'].create_line(
				self.viewport_scale(i,0,len(self.front_hips_dataset),jpx_view_size,"x"),
				self.viewport_scale(self.front_hips_dataset[i],mi,ma,jpy_view_size,"y",0.05),
				self.viewport_scale(i+1,0,len(self.front_hips_dataset),jpx_view_size,"x"),
				self.viewport_scale(self.front_hips_dataset[i+1],mi,ma,jpy_view_size,"y",0.05),
				width=2,
				fill="#FF0000"
			)
			self.viewports['Joint_Position'].create_line(
				self.viewport_scale(i,0,len(self.front_hips_dataset),jpx_view_size,"x"),
				self.viewport_scale(self.rear_hips_dataset[i],mi,ma,jpy_view_size,"y",0.05),
				self.viewport_scale(i+1,0,len(self.front_hips_dataset),jpx_view_size,"x"),
				self.viewport_scale(self.rear_hips_dataset[i+1],mi,ma,jpy_view_size,"y",0.05),
				width=2,
				fill="#00FF00"
			)

		self.viewports['Joint_Position'].create_rectangle(6,10,180,90,fill="white",outline="white")
		self.viewports['Joint_Position'].create_text(10,10,anchor="nw",justify='left',text="Front HIPS max "+str(int(round(front_hips_max,0)))+"°", fill="#FF0000", font=('Consolas 11 bold'))
		self.viewports['Joint_Position'].create_text(10,30,anchor="nw",justify='left',text="           min "+str(int(round(front_hips_min,0)))+"°", fill="#FF0000", font=('Consolas 11 bold'))
		self.viewports['Joint_Position'].create_text(10,50,anchor="nw",justify='left',text="Rear HIPS  max "+str(int(round(rear_hips_max,0)))+"°", fill="#00AA00", font=('Consolas 11 bold'))
		self.viewports['Joint_Position'].create_text(10,70,anchor="nw",justify='left',text="           min "+str(int(round(rear_hips_min,0)))+"°", fill="#00AA00", font=('Consolas 11 bold'))

		# .. for joint velocity
		jvx_view_size = self.viewports['Joint_Velocity'].winfo_width()
		jvy_view_size = self.viewports['Joint_Velocity'].winfo_height()

		mi = min(v_coxa_min,v_front_hips_min,v_rear_hips_min)
		ma = max(v_coxa_max,v_front_hips_max,v_rear_hips_max)

		for dps in np.arange(-5000.0,5000.0,500.0):
			_color = "#DDDDDD"
			_width = 1
			if round(dps,1) % 1000.0 == 0.00 :
				_width = 1		
				_color = "#BBBBBB"		
			if round(dps,1) == 0.0 :
				_width = 2		
				_color = "#999999"	
			self.viewports['Joint_Velocity'].create_line(
				0,
				self.viewport_scale(dps,mi,ma,jvy_view_size,"y",0.05),
				jvx_view_size,
				self.viewport_scale(dps,mi,ma,jvy_view_size,"y",0.05),
				width=_width,
				fill=_color
			)

		for i in range(0,len(self.v_front_hips_dataset)-1): 
			self.viewports['Joint_Velocity'].create_line(
				self.viewport_scale(i,0,len(self.v_front_hips_dataset),jvx_view_size,"x"),
				self.viewport_scale(self.v_front_hips_dataset[i],mi,ma,jvy_view_size,"y",0.05),
				self.viewport_scale(i+1,0,len(self.v_front_hips_dataset),jvx_view_size,"x"),
				self.viewport_scale(self.v_front_hips_dataset[i+1],mi,ma,jvy_view_size,"y",0.05),
				width=2,
				fill="#FF0000"
			)
			self.viewports['Joint_Velocity'].create_line(
				self.viewport_scale(i,0,len(self.v_rear_hips_dataset),jvx_view_size,"x"),
				self.viewport_scale(self.v_rear_hips_dataset[i],mi,ma,jvy_view_size,"y",0.05),
				self.viewport_scale(i+1,0,len(self.v_rear_hips_dataset),jvx_view_size,"x"),
				self.viewport_scale(self.v_rear_hips_dataset[i+1],mi,ma,jvy_view_size,"y",0.05),
				width=2,
				fill="#00FF00"
			)

		self.viewports['Joint_Velocity'].create_rectangle(6,10,200,90,fill="white",outline="white")
		self.viewports['Joint_Velocity'].create_text(10,10,anchor="nw",justify='left',text="Front HIPS max "+str(int(round(v_front_hips_max,0)))+" °/s", fill="#FF0000", font=('Consolas 11 bold'))
		self.viewports['Joint_Velocity'].create_text(10,30,anchor="nw",justify='left',text="           min "+str(int(round(v_front_hips_min,0)))+" °/s", fill="#FF0000", font=('Consolas 11 bold'))
		self.viewports['Joint_Velocity'].create_text(10,50,anchor="nw",justify='left',text="Rear HIPS  max "+str(int(round(v_rear_hips_max,0)))+" °/s", fill="#00AA00", font=('Consolas 11 bold'))
		self.viewports['Joint_Velocity'].create_text(10,70,anchor="nw",justify='left',text="           min "+str(int(round(v_rear_hips_min,0)))+" °/s", fill="#00AA00", font=('Consolas 11 bold'))

		# .. for joint acceleration
		jax_view_size = self.viewports['Joint_Acceleration'].winfo_width()
		jay_view_size = self.viewports['Joint_Acceleration'].winfo_height()

		mi = min(a_coxa_min,a_front_hips_min,a_rear_hips_min)
		ma = max(a_coxa_max,a_front_hips_max,a_rear_hips_max)

		for dpss in np.arange(-200000.0,200000.0,50000.0):
			_color = "#DDDDDD"
			_width = 1
			if round(dpss,1) % 100000.0 == 0.00 :
				_width = 1		
				_color = "#BBBBBB"		
			if round(dpss,1) == 0.0 :
				_width = 2		
				_color = "#999999"	
			self.viewports['Joint_Acceleration'].create_line(
				0,
				self.viewport_scale(dpss,mi,ma,jay_view_size,"y",0.05),
				jax_view_size,
				self.viewport_scale(dpss,mi,ma,jay_view_size,"y",0.05),
				width=_width,
				fill=_color
			)

		for i in range(0,len(self.a_front_hips_dataset)-1): 
			self.viewports['Joint_Acceleration'].create_line(
				self.viewport_scale(i,0,len(self.a_front_hips_dataset),jax_view_size,"x"),
				self.viewport_scale(self.a_front_hips_dataset[i],mi,ma,jay_view_size,"y",0.05),
				self.viewport_scale(i+1,0,len(self.a_front_hips_dataset),jax_view_size,"x"),
				self.viewport_scale(self.a_front_hips_dataset[i+1],mi,ma,jay_view_size,"y",0.05),
				width=2,
				fill="#FF0000"
			)
			self.viewports['Joint_Acceleration'].create_line(
				self.viewport_scale(i,0,len(self.a_rear_hips_dataset),jax_view_size,"x"),
				self.viewport_scale(self.a_rear_hips_dataset[i],mi,ma,jay_view_size,"y",0.05),
				self.viewport_scale(i+1,0,len(self.a_rear_hips_dataset),jax_view_size,"x"),
				self.viewport_scale(self.a_rear_hips_dataset[i+1],mi,ma,jay_view_size,"y",0.05),
				width=2,
				fill="#00FF00"
			)

		self.viewports['Joint_Acceleration'].create_rectangle(6,10,230,90,fill="white",outline="white")
		self.viewports['Joint_Acceleration'].create_text(10,10,anchor="nw",justify='left',text="Front HIPS max "+str(int(round(a_front_hips_max,0)))+" °/s²", fill="#FF0000", font=('Consolas 11 bold'))
		self.viewports['Joint_Acceleration'].create_text(10,30,anchor="nw",justify='left',text="           min "+str(int(round(a_front_hips_min,0)))+" °/s²", fill="#FF0000", font=('Consolas 11 bold'))
		self.viewports['Joint_Acceleration'].create_text(10,50,anchor="nw",justify='left',text="Rear HIPS  max "+str(int(round(a_rear_hips_max,0)))+" °/s²", fill="#00AA00", font=('Consolas 11 bold'))
		self.viewports['Joint_Acceleration'].create_text(10,70,anchor="nw",justify='left',text="           min "+str(int(round(a_rear_hips_min,0)))+" °/s²", fill="#00AA00", font=('Consolas 11 bold'))

	def viewport_scale(self,a,a_min,a_max,view_size,axis,margin = 0.00):
		
		if axis=="x":
			return view_size*margin/2 + view_size*(1.0-margin)*(a-a_min)/(a_max-a_min)
		else:
			return view_size*margin/2 + view_size*(1.0-margin)*(1.0-(a-a_min)/(a_max-a_min))

	def plotter(self):

		plt.plot(np.arange(self.step_s,self.T_swing_s+self.T_stance_s,self.step_s),self.ax_dataset)
		plt.xlabel('Time (s)')
		plt.ylabel('X - Acceleration (m/s²)')
		plt.show()

		plt.plot(np.arange(self.step_s,self.T_swing_s+self.T_stance_s,self.step_s),self.az_dataset)
		plt.xlabel('Time (s)')
		plt.ylabel('Z - Acceleration (m/s²)')
		plt.show()

		plt.plot(np.arange(0,self.T_swing_s+self.T_stance_s,self.step_s),self.vx_dataset)
		plt.xlabel('Time (s)')
		plt.ylabel('X - Velocity (m/s)')
		plt.show()

		plt.plot(np.arange(0,self.T_swing_s+self.T_stance_s,self.step_s),self.vz_dataset)
		plt.xlabel('Time (s)')
		plt.ylabel('Z - Velocity (m/s)')
		plt.show()

		plt.plot(np.arange(0,self.T_swing_s+self.T_stance_s+self.step_s,self.step_s),self.x_dataset)
		plt.xlabel('Time (s)')
		plt.ylabel('X - Position (m)')
		plt.show()

		plt.plot(np.arange(0,self.T_swing_s+self.T_stance_s+self.step_s,self.step_s),self.z_dataset)
		plt.xlabel('Time (s)')
		plt.ylabel('Z - Position (m)')
		plt.show()

		plt.plot(self.x_dataset,self.z_dataset)
		plt.axis('equal')
		plt.xlabel('X - Position (m)')
		plt.ylabel('Z - Position (m)')
		plt.show()


def main():
	window = Tk()
	window.title("Foot trajectory planner")
	window.geometry("1600x800")
	window.minsize(1600,1000)

	g = gui(window)	
	window.update_idletasks( ) # doesn't work as expected
	g.update()
	window.mainloop()

if __name__ == "__main__":

	##cProfile.run("main()")
	main()


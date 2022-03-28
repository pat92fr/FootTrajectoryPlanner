#felin_geometry.py

# Felin 2022
# 12-DOF with 5-bar legs

# Front Hip to Rear Hip distance = 62mm
H2H_distance = 0.062 #m

# Coxa Length = 60mm
Lc = 0.060 #m

# Femur Length = 80mm
Lf = 0.120 #m

# Tibia Length = 160mm
Lt = 0.150 #m

# Min Tibia+Femur elongation
Lmin = 0.08 #m

# Max Tibia+Femur elongation
Lmax = Lf + Lt -0.02 #m

# Stand-by position
X0 =  0.000 #m
Y0 =  0.000 #m
Z0 = -0.130 #m

# Gait bounds
max_stride_length = 0.160 #m
max_swing_height = 0.050 #m
max_stance_height = -0.010 #m

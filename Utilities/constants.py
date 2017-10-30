# Made by Christian Oliveros on 06/10/2017 for MMKF15

# Imports Used
import decimal as d

try:
	from .decimalMath import deg2rad, cos, sin
except SystemError as e:
	from decimalMath import deg2rad, cos, sin

# Minimun possible movement and tolerance of math calculations
EPSILON = d.Decimal(1e-01)
# I.e. if(abs(p0-p1) < EPSILON) then p0==p1

# Length of arms rod to center cart
L = d.Decimal(290) # 290

# Step maximun distance
STEP_MAX = d.Decimal(10) # mm

# Squared L
LSQR = L**2

# Height of the roof of the 3d printer in mm
VL = d.Decimal(440) # 440

# Radius of the base of the 3d printer in mm
HL = d.Decimal(160) # 160

# Angle of first leg in radians
THETA1 = deg2rad(d.Decimal(90))

# Angle of second leg in radians
THETA2 = deg2rad(d.Decimal(90) + (d.Decimal(360) / d.Decimal(3)))

# Angle of third leg in radians
THETA3 = deg2rad(d.Decimal(90) - (d.Decimal(360) / d.Decimal(3)))

# Cos of theta1
COS_THETA1 = cos(THETA1)

# Cos of theta2
COS_THETA2 = cos(THETA2)

# Cos of theta3
COS_THETA3 = cos(THETA3)

# Sin of theta1
SIN_THETA1 = sin(THETA1)

# Sin of theta2
SIN_THETA2 = sin(THETA2)

# Sin of theta3
SIN_THETA3 = sin(THETA3)

# Positions of leg 1
POS_X_1 = HL * COS_THETA1
POS_Y_1 = HL * SIN_THETA1

# Positions of leg 2
POS_X_2 = HL * COS_THETA2
POS_Y_2 = HL * SIN_THETA2

# Positions of leg 2
POS_X_3 = HL * COS_THETA2
POS_Y_3 = HL * SIN_THETA2


# Start Height Offset against the roof of the robot
START_POSITION_HEIGHT_OFFSET = (L**2-HL**2).sqrt() # mm

# Start Position of the robot
# It is defined in vector.py
START_POSITION = None

# The Velocity that the robot is going to use if no one is supplied at start in mm/s
START_VELOCITY = d.Decimal(1)

# Start Joint Position of the robot
# It is defined in trajectoryGeneration.py
START_JOINT_POSITION = None

# Made by Christian Oliveros on 06/10/2017 for MMKF15

# Imports Used
import decimal as d

# Minimun possible movement and tolerance of math calculations
EPSILON = d.Decimal(1e-04)
# I.e. if(abs(p0-p1) < EPSILON) then p0==p1

# Height of the roof of the 3d printer
VL = d.Decimal(150)

# Start Position of the robot
# It is defined in vector.py
START_POSITION = None

# The Velocity that the robot is going to use if no one is supplied at start
START_VELOCITY = d.Decimal(1)
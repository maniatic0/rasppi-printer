#Code for control the stepper motors

#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
from math import pi
import time
import atexit
import threading
import random

# gear motor radius in centimeters
R = 0.6

# const motor steps in grades in SINGLE mode
stepDeg = 1.8

# const motor steps in centimeters in SINGLE mode
stepDist = stepDeg*pi/180*R

# define motors at home position
q1 = q2 = q3 = 0
q1_v = q2_v = q3_v = 0

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

# create empty threads (these will hold the stepper 1 and 2 threads)
st1 = threading.Thread()
st2 = threading.Thread()


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

# cerate the tolerance rate
def makeTolerance(step):
    if (step == Adafruit_MotorHAT.SINGLE or step == Adafruit_MotorHAT.DOUBLE):
        tolerance = 0.9*stepDist
    elif (step == Adafruit_MotorHAT.INTERLEAVE):
        tolerance = (0.9*stepDist)/2
    elif (step == Adafruit_MotorHAT.MICROSTEP):
        tolerance = (0.9*stepDist)/16
    else:
        tolerance = 0.9*stepDist
    return tolerance

# gives the angular velocity in REV/min when qi_vel is in cm/s
def angVel(qi_vel):
    return 30/pi*qi_vel/R

atexit.register(turnOffMotors)

myStepper1 = mh.getStepper(200, 1)      # 200 steps/rev, motor port #1
myStepper2 = mh.getStepper(200, 2)      # 200 steps/rev, motor port #2
#myStepper3 = mh.getStepper(200, 3)      # 200 steps/rev, motor port #3

stepstyle = Adafruit_MotorHAT.MICROSTEP

def stepper_worker(stepper, numsteps, direction, style):
    #print("Steppin!")
    stepper.step(numsteps, direction, style)
    #print("Done")

while (True):
    TOLERANCE = makeTolerance(stepstyle)    # movement precision
    if not st1.isAlive():
        print("Stepper 1")
        if (q1_req > q1 + TOLERANCE):
            dir = Adafruit_MotorHAT.FORWARD
        elif (q1_req < q1 - TOLERANCE):
            dir = Adafruit_MotorHAT.BACKWARD
        else:
            dir = Adafruit_MotorHAT.FORWARD
        # define angular velocity in rev/min
        w = angVel(q1_vel_req)
        myStepper1.setSpeed(w)

        # create thread with 16 steps
        if (q1_req > q1 + TOLERANCE or q1_req < q1 - TOLERANCE):
            st1 = threading.Thread(target=stepper_worker, args=(myStepper1, 16, dir, stepstyle,))
            st1.start()

    if not st2.isAlive():
        print("Stepper 2")
        if (q2_req > q2 + TOLERANCE):
            dir = Adafruit_MotorHAT.FORWARD
        elif (q2_req < q2 - TOLERANCE):
            dir = Adafruit_MotorHAT.BACKWARD
        else:
            dir = Adafruit_MotorHAT.FORWARD
        # define angular velocity in rev/min
        w = angVel(q2_vel_req)
        myStepper2.setSpeed(w)

        # create thread with 16 steps        
        if (q2_req > q2 + TOLERANCE or q2_req < q2 - TOLERANCE):
            st2 = threading.Thread(target=stepper_worker, args=(myStepper2, 16, dir, stepstyle,))
            st2.start()
    
    time.sleep(0.1)  # Small delay to stop from constantly polling threads (see: https://forums.adafruit.com/viewtopic.php?f=50&t=104354&p=562733#p562733)


#-------------------------------------------------------------------------------
# Name:        moveMotors
# Purpose:     move steppers motors with the position and velocity of the blue joints
#
# Author:      Luis Felipe Leiva H.
#
# Created:     09-10-2017
# Copyright:   (c) felipe 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Imports used
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
from math import pi
import time
import atexit
import threading
import constantsMotor as cMot

try:
	from .constantsMotor import stepDist, numSteps, R
except SystemError as e:
	from constantsMotor import stepDist, numSteps, R

# Imports Used

try:
	from ..Utilities.instruction import Instruction, InterpretedInstruction
except SystemError as e:
	from instruction import Instruction, InterpretedInstruction

try:
	from ..Utilities.vector import Vector3, interpolatePoints
except SystemError as e:
	from vector import Vector3, interpolatePoints      

"""Code for control the stepper motors"""

# global variables
q1 = q2 = q3 = 0                                            # define motors at home position for test purposes
q = [q1, q2, q3]                                            # vector of position
q_req = [q1_req, q2_req, q3_req]                            # vector of  required position
q_vel_req = [q1_vel_req, q2_vel_req, q3_vel_req]            # vector of required velocity

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    tophat.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    tophat.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    tophat.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    tophat.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
    bottomhat.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    bottomhat.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    bottomhat.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    bottomhat.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

# create the tolerance rate
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

# gives the angular velocity in REV/min when qi_vel is in mm/s
def angVel(qi_vel):
    return 30/pi*qi_vel/R

def stepper_worker(stepper, numsteps, direction, style):
    #print("Steppin!")
    stepper.step(numsteps, direction, style)
    #print("Done")

def moveSteppers(qPos, qRec, qVelReq, stepperThreads, numSteps, TOLERANCE):
    q_req = [qRec.x, qRec.y, qRec.z]
    q_vel_req = [qVelReq.x, qVelReq.y, qVelReq.z]
    q = [qPos.x, qPos.y, qPos.z]
    # Aqui esta preguntando para un i que fue definido mas abajo ----- hay que cambiarlo por un arreglo de bool
    movBool = [True, True, True]
    # Preguntar si los 3 objetos del arreglo son false por si es que hay que mover el motor
    while (movBool[0] or movBool[1] or movBool[2]):
        for i in range(3):
            case1 = q_req[i] > q[i] + TOLERANCE
            case2 = q_req[i] < q[i] - TOLERANCE
            movBool[i] = case1 or case2
            if movBool[i] and not stepperThreads[i].isAlive():
                print("Stepper %s" % i)
                if (case2):
                    dir = Adafruit_MotorHAT.BACKWARD                    
                else:
                    dir = Adafruit_MotorHAT.FORWARD
                    
                # define angular velocity in rev/min
                w = angVel(q_vel_req[i])
                
                # set velocity
                steppers[i].setSpeed(w)

                # create thread with numStep steps
                stepperThreads[i] = threading.Thread(target=stepper_worker, args=(steppers[i], numSteps, dir, stepstyle,))
                stepperThreads[i].start()

        time.sleep(0.1)  # Small delay to stop from constantly polling threads (see: https://forums.adafruit.com/viewtopic.php?f=50&t=104354&p=562733#p562733)
      
# bottom hat is default address 0x60
bottomhat = Adafruit_MotorHAT(addr=0x60)

# top hat has A0 jumper closed, so its address 0x61
tophat = Adafruit_MotorHAT(addr=0x61)

# create empty threads (these will hold the stepper 1, 2 & 3 threads)
stepperThreads = [threading.Thread(), threading.Thread(), threading.Thread()]

# ni idea lo que hace, pero sirve
atexit.register(turnOffMotors)

# motor configurations
myStepper1 = bottomhat.getStepper(200, 1)      # 200 steps/rev, motor port #1
myStepper2 = bottomhat.getStepper(200, 2)      # 200 steps/rev, motor port #2
myStepper3 = tophat.getStepper(200, 1)         # 200 steps/rev, motor port #1

# step type
stepstyle = Adafruit_MotorHAT.MICROSTEP
steppers = [myStepper1, myStepper2, myStepper3]

# movement precision
TOLERANCE = makeTolerance(stepstyle)        

def movMotor(qPos, inst):
    # move motors   
    moveSteppers(qPos, inst.pos, inst.vel, stepperThreads, numSteps, TOLERANCE)
        
if __name__ == '__main__':
    
    # move motors
    moveSteppers(q_req, q_vel_req, stepperThreads, numSteps, TOLERANCE)

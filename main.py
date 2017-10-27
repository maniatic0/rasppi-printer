#!/usr/bin/env python3
# Made by Christian Oliveros on 09/10/2017 for MMKF15

# Imports Used
import sys
import os

import Utilities.fileReader as reader
import Utilities.trajectoryGeneration as trajectoryGeneration
import Utilities.constants as consts
import Motors.motorDrivers_final as motor


def main():
	if len(sys.argv) < 2:
		print("Usage: put the file to read as the argument")
		exit(-1)

	if not os.path.exists(sys.argv[1]):
		print("File missing")
		exit(-1)

	if not os.path.isfile(sys.argv[1]):
		print("Path not leading to file")
		exit(-1)

	print("Welcome to the MMKF15 project of:\n * Christian Oliveros\n * Luis Felipe Leiva\n * Pablo Correa")
	print("Initializing File Reader")
	f = reader.FileReader(sys.argv[1])
	print("Initializing at Cartesian Position = %s" % consts.START_POSITION)
	print("Initializing at Joint Position = %s" % consts.START_JOINT_POSITION)
	print("Initializing Movement")
	q_prev_pos = consts.START_JOINT_POSITION
	for joints in trajectoryGeneration.generateJointPathTrajectory(f):
		print("==============================================================")
		print("Following Instruction: %s" % joints)
		print("From Position: %s" % q_prev_pos)
		motor.movMotor(q_prev_pos, joints)
		print("Instruction Done")
		print("==============================================================")
		q_prev_pos = joints.pos
	print("Movement Done")
	print("Releasing Motors")
	motor.turnOffMotors()
	print("Motors Off")
	exit(0)


if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print("Releasing Motors")
		motor.turnOffMotors()
		print("Motors Off")
		print(e)
		exit(-1)
		

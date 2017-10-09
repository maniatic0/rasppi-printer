# Made by Christian Oliveros on 09/10/2017 for MMKF15

# Imports Used
import sys
import os

import Utilities.fileReader as reader
import Utilities.trajectoryGeneration as trajectoryGeneration




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

	print("Initializing Movement")
	for joints in trajectoryGeneration.generateJointPathTrajectory(f):
		print("Following Instruction")
		# TODO: REAL MOTORS GO HERE
		print("TODO: REAL MOTORS GO HERE")
		print(joints)
		import time
		time.sleep(0.5)
		# TODO: REAL MOTORS GO HERE
		print("Instruction Done")
	print("Movement Done")
	exit(0)


if __name__ == '__main__':
	main()

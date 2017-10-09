# Made by Christian Oliveros on 09/10/2017 for MMKF15

# Imports Used

try:
	from .instruction import Instruction, InterpretedInstruction
except SystemError as e:
	from instruction import Instruction, InterpretedInstruction

try:
	from .vector import Vector3, interpolatePoints
except SystemError as e:
	from vector import Vector3, interpolatePoints

try:
	from .constants import START_VELOCITY, START_POSITION, LSQR, VL, POS_X_1, POS_X_2, POS_X_3, POS_Y_1, POS_Y_2, POS_Y_3
except SystemError as e:
	from constants import START_VELOCITY, START_POSITION, LSQR, VL, POS_X_1, POS_X_2, POS_X_3, POS_Y_1, POS_Y_2, POS_Y_3


"""Generates the cartesian trajectory from a file reader, a start velocity and a start position"""
def generateCartesianPathTrajectory(fileReader, start_vel=START_VELOCITY, start_pos=START_POSITION):
	traj = []
	current_vel = start_vel
	current_pos = start_pos
	pre_pos = None
	started = False
	for instruction in fileReader:
		if instruction.V is not None:
			current_vel = instruction.V

		traj.clear()
		# Amount of points in interpolation, used to know if we moved
		count = 0

		for pos in interpolatePoints(current_pos, instruction.pos):
			# Lets not put the original starting position of the arm
			traj.append(InterpretedInstruction(pos, (pos - current_pos).normalized() * current_vel))
			pre_pos = current_pos
			current_pos = pos
			count += 1

		if not started:
			started = True
			del traj[0]
			# If we did not move from the origin
			if len(traj) == 0:
				started = False
				continue

		# We actually moved
		if count > 1 :
			traj[len(traj) - 1].vel = Vector3()
		# We didn't move
		else:
			size = len(traj)
			if size > 0:
				del traj[size - 1]
				current_pos = pre_pos
				if size - 1 == 0:
					continue

		for ans in traj:
			yield ans

"""Calculate one joint position"""
def _iKinePos(X, Y, Z):
	return -(LSQR - (X)**2 - (Y)**2).sqrt() - Z + VL

"""Calculate one joint velocity"""
def _iKineVel(X, Y, Z, vel, q):
	return - ((X * vel.x + Y * vel.y) / (Z - VL + q)) - vel.z

"""Receives a cartesian instruction and converts it to an joint one"""
def iKine(cartesian_instruction):
	sub_x_1 = cartesian_instruction.pos.x - POS_X_1
	sub_y_1 = cartesian_instruction.pos.y - POS_Y_1

	sub_x_2 = cartesian_instruction.pos.x - POS_X_2
	sub_y_2 = cartesian_instruction.pos.y - POS_Y_2

	sub_x_3 = cartesian_instruction.pos.x - POS_X_3
	sub_y_3 = cartesian_instruction.pos.y - POS_Y_3

	q = Vector3()

	q.x = _iKinePos(sub_x_1, sub_y_1, cartesian_instruction.pos.z)
	q.y = _iKinePos(sub_x_2, sub_y_2, cartesian_instruction.pos.z)
	q.z = _iKinePos(sub_x_3, sub_y_3, cartesian_instruction.pos.z)

	q_vel = Vector3()

	q_vel.x = _iKineVel(sub_x_1, sub_y_1, cartesian_instruction.pos.z, cartesian_instruction.vel, q.x)
	q_vel.y = _iKineVel(sub_x_2, sub_y_2, cartesian_instruction.pos.z, cartesian_instruction.vel, q.y)
	q_vel.z = _iKineVel(sub_x_3, sub_y_3, cartesian_instruction.pos.z, cartesian_instruction.vel, q.z)

	return InterpretedInstruction(q, q_vel)


"""Generates the joint trajectory from a file reader, a start velocity and a start position"""
def generateJointPathTrajectory(fileReader, start_vel=START_VELOCITY, start_pos=START_POSITION):
	for instruction in generateCartesianPathTrajectory(fileReader, start_vel, start_pos):
		yield iKine(instruction)

if __name__ == '__main__':
	import os
	print("Test of Path Trajectory")
	print("Generation Start")
	import fileReader as reader
	f = reader.FileReader(os.path.relpath(os.path.join("Test", "correct_test.txt"), start=os.curdir))
	traj = [x for x in generateCartesianPathTrajectory(f)]
	print("Generation Done")
	print("len=%s" % len(traj))
	print("pos0=%s" % traj[0])
	print("pos%s=%s" % (len(traj) - 1,traj[len(traj) - 1]))
	print("pos%s=%s" % (len(traj) - 2,traj[len(traj) - 2]))
	print("pos%s=%s" % (len(traj) - 3,traj[len(traj) - 3]))
	print("iKine Test")
	print(iKine(InterpretedInstruction(Vector3(10, 20, 30), Vector3(10, 20, 30).normalized())))
	print("Joint Trajectory")
	f = reader.FileReader(os.path.relpath(os.path.join("Test", "correct_test.txt"), start=os.curdir))
	print("Generation Start")
	jtraj = [x for x in generateJointPathTrajectory(f)]
	print("Generation Done")
	print("len=%s" % len(jtraj))
	print("pos0=%s" % jtraj[0])
	print("pos%s=%s" % (len(jtraj) - 1,jtraj[len(jtraj) - 1]))
	print("pos%s=%s" % (len(jtraj) - 2,jtraj[len(jtraj) - 2]))
	print("pos%s=%s" % (len(jtraj) - 3,jtraj[len(jtraj) - 3]))



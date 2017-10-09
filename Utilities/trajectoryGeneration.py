# Made by Christian Oliveros on 09/10/2017 for MMKF15

# Imports Used
import fileReader as reader
import instruction as ins
import vector as vec
import constants as c

"""Generates the cartesian trajectory from a file reader, a start velocity and a start position"""
def generateCartesianPathTrajectory(fileReader, start_vel=c.START_VELOCITY, start_pos=c.START_POSITION):
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

		for pos in vec.interpolatePoints(current_pos, instruction.pos):
			# Lets not put the original starting position of the arm
			traj.append(ins.InterpretedInstruction(pos, (pos - current_pos).normalized() * current_vel))
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
			traj[len(traj) - 1].vel = vec.Vector3()
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
	return -(c.LSQR - (X)**2 - (Y)**2).sqrt() - Z + c.VL

"""Calculate one joint velocity"""
def _iKineVel(X, Y, Z, vel, q):
	return - ((X * vel.x + Y * vel.y) / (Z - c.VL + q)) - vel.z

"""Receives a cartesian instruction and converts it to an joint one"""
def iKine(cartesian_instruction):
	sub_x_1 = cartesian_instruction.pos.x - c.POS_X_1
	sub_y_1 = cartesian_instruction.pos.y - c.POS_Y_1

	sub_x_2 = cartesian_instruction.pos.x - c.POS_X_2
	sub_y_2 = cartesian_instruction.pos.y - c.POS_Y_2

	sub_x_3 = cartesian_instruction.pos.x - c.POS_X_3
	sub_y_3 = cartesian_instruction.pos.y - c.POS_Y_3

	q = vec.Vector3()

	q.x = _iKinePos(sub_x_1, sub_y_1, cartesian_instruction.pos.z)
	q.y = _iKinePos(sub_x_2, sub_y_2, cartesian_instruction.pos.z)
	q.z = _iKinePos(sub_x_3, sub_y_3, cartesian_instruction.pos.z)

	q_vel = vec.Vector3()

	q_vel.x = _iKineVel(sub_x_1, sub_y_1, cartesian_instruction.pos.z, cartesian_instruction.vel, q.x)
	q_vel.y = _iKineVel(sub_x_2, sub_y_2, cartesian_instruction.pos.z, cartesian_instruction.vel, q.y)
	q_vel.z = _iKineVel(sub_x_3, sub_y_3, cartesian_instruction.pos.z, cartesian_instruction.vel, q.z)

	return ins.InterpretedInstruction(q, q_vel)



if __name__ == '__main__':
	import os
	print("Test of Path Trajectory")
	print("Generation Start")
	f = reader.FileReader(os.path.relpath(os.path.join("Test", "correct_test.txt"), start=os.curdir))
	traj = [x for x in generateCartesianPathTrajectory(f)]
	print("Generation Done")
	print("len=%s" % len(traj))
	print("pos0=%s" % traj[0])
	print("pos%s=%s" % (len(traj) - 1,traj[len(traj) - 1]))
	print("pos%s=%s" % (len(traj) - 2,traj[len(traj) - 2]))
	print("pos%s=%s" % (len(traj) - 3,traj[len(traj) - 3]))
	print("iKine Test")
	print(iKine(ins.InterpretedInstruction(vec.Vector3(10, 20, 30), vec.Vector3(10, 20, 30).normalized())))
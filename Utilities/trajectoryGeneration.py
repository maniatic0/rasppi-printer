# Made by Christian Oliveros on 09/10/2017 for MMKF15

# Imports Used
import fileReader as reader
import instruction as ins
import vector as vec
import constants as c


def generatePathTrajectory(fileReader, start_vel=c.START_VELOCITY, start_pos=c.START_POSITION):
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

	# TODO : volver esto un iterador y devolver cada posicion creada
	# Aceptar posicion inicial, velocidad inicial y lector generico
	# mover esto de lugar
	# Hacer jtraj basado en esto


if __name__ == '__main__':
	import os
	print("Test of Path Trajectory")
	print("Generation Start")
	f = reader.FileReader(os.path.relpath(os.path.join("Test", "correct_test.txt"), start=os.curdir))
	traj = [x for x in generatePathTrajectory(f)]
	print("Generation Done")
	print("len=%s" % len(traj))
	print("pos0=%s" % traj[0])
	print("pos%s=%s" % (len(traj) - 1,traj[len(traj) - 1]))
	print("pos%s=%s" % (len(traj) - 2,traj[len(traj) - 2]))
	print("pos%s=%s" % (len(traj) - 3,traj[len(traj) - 3]))

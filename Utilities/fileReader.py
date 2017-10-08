# Made by Christian Oliveros on 06/10/2017 for MMKF15

# Imports Used
import instruction as ins
import vector as vec
import constants as c

class FileReader(object):
	"""File Reader for Instructions on a file"""
	def __init__(self, path):
		self.path = path
		self.file = open(self.path, 'r')
		self.line = 0

	"""Iterator"""
	def __iter__(self):
		return self

	"""Iterator next method"""
	def __next__(self):
		if self.file.closed:
			raise StopIteration

		line = self.file.readline()

		self.line += 1

		if line == "":
			self.file.close()
			raise StopIteration

		try:
			line = line.lstrip()
			if len(line) == 0:
				return self.__next__()
			ans = ins.Instruction(line)
			return ans
		except Exception as e:
			self.file.close()
			import sys
			raise type(e)(str(e) 
				+ ' in file %s on the line %s' 
				% (self.path, self.line)).with_traceback(sys.exc_info()[2])

	"""Destructor that ensures the file is closed"""
	def __del__(self):
		if not self.file.closed:
			self.file.close()


def generatePathTrajectory(path):
	f = FileReader(path)
	traj = []
	current_vel = c.START_VELOCITY
	current_pos = c.START_POSITION
	started = False
	for instruction in f:
		if instruction.V is not None:
			current_vel = instruction.V

		# Amount of points in interpolation, used to know if we moved
		count = 0

		for pos in vec.interpolatePoints(current_pos, instruction.pos):
			# Lets not put the original starting position of the arm
			traj.append(ins.InterpretedInstruction(pos, (pos - current_pos).normalized() * current_vel))
			current_pos = pos
			count += 1

		if not started:
			started = True
			del traj[0]
			# We moved to the origin from the origin
			if len(traj) == 0 :
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
				current_pos = traj[size - 2].pos

	return traj



if __name__ == '__main__':
	import os

	print("File without error")
	f = FileReader(os.path.relpath(os.path.join("Test", "correct_test.txt"), start=os.curdir))

	for i in f:
		print(i)

	del f

	print("File with error")
	f = FileReader(os.path.relpath(os.path.join("Test", "bad_test.txt"), start=os.curdir))

	try:
		for i in f:
			print(i)
	except Exception as e:
		print(e)
		
	del f

	print("Test of Path Trajectory")
	print("Generation Start")
	traj = generatePathTrajectory(os.path.relpath(os.path.join("Test", "correct_test.txt"), start=os.curdir))
	print("Generation Done")
	print("len=%s" % len(traj))
	print("pos0=%s" % traj[0])
	print("pos%s=%s" % (len(traj) - 1,traj[len(traj) - 1]))

# Made by Christian Oliveros on 06/10/2017 for MMKF15

# Imports Used
try:
	from .instruction import Instruction
except SystemError as e:
	from instruction import Instruction


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
			ans = Instruction(line)
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
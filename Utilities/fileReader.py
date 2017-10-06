# Made by Christian Oliveros on 06/10/2017 for MMKF15

# Imports Used
import instruction as ins

class FileReader(object):
	"""File Reader for Instructions on a file"""
	def __init__(self, path):
		self.path = path
		self.file = open(self.path, 'r')

	"""Iterator"""
	def __iter__(self):
		return self

	"""Iterator next method"""
	def __next__(self):
		if self.file.closed:
			raise StopIteration

		line = self.file.readline()

		if line == "":
			self.file.close()
			raise StopIteration

		try:
			return ins.Instruction(line)
		except Exception as e:
			error_line = self.file.tell()
			self.file.close()
			import sys
			raise type(e)(str(e) 
				+ ' in file %s at position %s and on the line: %s' % (self.path, error_line, line)).with_traceback(sys.exc_info()[2])

		

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
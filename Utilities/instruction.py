# Made by Christian Oliveros on 05/10/2017 for MMKF15

# Imports Used
import decimal as d
import re
import vector as v

class Instruction(object):
	"""Regex pattern"""
	_pattern = r"^(\s)*(?P<X>([^\s])+) (?P<Y>([^\s])+) (?P<Z>([^\s])+)( (?P<V>([^\s])+))?(\s)*$"
	"""Regex state machine"""
	_prog = re.compile(_pattern)
	"""Instruction for the Arm
	Requires a lines following the format X Y Z <V>"""
	def __init__(self, line):
		super(Instruction, self).__init__()
		line = line.rstrip()
		result = Instruction._prog.match(line)
		if result is None:
			raise ValueError(("The instruction format should be numbers in the form \"X Y Z <V>\" but found \"%s\"" % (line)))

		try:
			self.pos = v.Vector3(d.Decimal(result.group('X')), d.Decimal(result.group('Y')), d.Decimal(result.group('Z')))
		except Exception as e:
			raise ValueError(("The instruction format should be numbers in the form \"X Y Z <V>\" but found \"%s\"" % (line)))

		
		if result.group('V') is not None:
			try:
				self.V = d.Decimal(result.group('V'))
			except Exception as e:
				raise ValueError(("The instruction format should be numbers in the form \"X Y Z <V>\" but found \"%s\"" % (line)))
		else:
			self.V = None

	"""Converts from the values X, Y, Z, <V> to a valid Instruction line"""
	def fromValuesToLine(X, Y, Z, V=None):
		if V is None:
			return "%s %s %s" % (d.Decimal(X), d.Decimal(Y), d.Decimal(Z))
		else:
			return "%s %s %s %s" % (d.Decimal(X), d.Decimal(Y), d.Decimal(Z), d.Decimal(V))

	"""Instruction representation"""
	def __repr__(self):
		return "Instruction(line=\"%s\")" % Instruction.fromValuesToLine(self.pos.x, self.pos.y, self.pos.z, self.V)

	"""Instruction string representation"""
	def __str__(self):
		return Instruction.fromValuesToLine(self.pos.x, self.pos.y, self.pos.z, self.V)


class InterpretedInstruction(object):
	"""Intruction with vector position and velocity"""
	def __init__(self, pos, vel):
		super(InterpretedInstruction, self).__init__()
		self.pos = pos
		self.vel = vel

	"""Interpreted Instruction representation"""
	def __repr__(self):
		return "InterpretedInstruction(pos=%r,vel=%r)" % (self.pos, self.vel)

	"""Interpreted Instruction string representation"""
	def __str__(self):
		return "(pos=%s,vel=%s)" % (self.pos, self.vel)
		

if __name__ == '__main__':
	Instruction("1 2 3")
	Instruction("1.2 3.4 5.8 4")
	Instruction("3 4 5 6                          ")
	Instruction("4 10.3 99                           ")
	try:
		Instruction("X Z                           \n")
	except Exception as e:
		print(e.args)

	i = Instruction("4 10.3 99.00000000000000000000000001                           ")
	print(i)
	print(Instruction(Instruction.fromValuesToLine(i.pos.x, i.pos.y, i.pos.z, i.V)))
	print(Instruction(str(i)))




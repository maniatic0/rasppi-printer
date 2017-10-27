# Made by Christian Oliveros on 04/10/2017 for MMKF15

# Imports Used
import decimal as d

try:
	from .constants import VL, EPSILON, STEP_MAX
except SystemError as e:
	from constants import VL, EPSILON, STEP_MAX



class Vector3(object):
	"""Class that represents a Vector with 3 coordinates"""
	def __init__(self, x=0.0, y=0.0, z=0.0):
		super(Vector3, self).__init__()
		self.x = d.Decimal(x)
		self.y = d.Decimal(y)
		self.z = d.Decimal(z)

	"""Class Representation"""
	def __repr__(self):
		return "Vector3(x=%r,y=%r,z=%r)" % (self.x, self.y, self.z)

	"""Class String Representation"""
	def __str__(self):
		return "(%s, %s, %s)" % (str(self.x), str(self.y), str(self.z))

	"""Copy this vector in new instance"""
	def copy(self):
		return Vector3(self.x, self.y, self.z)

	"""Get Square Magnitude of vector"""
	def sqrMagnitude(self):
		dec2 = d.Decimal(2.0)
		return self.x**dec2 + self.y**dec2 + self.z**dec2

	"""Get Magnitude of vector"""
	def magnitude(self):
	 	return self.sqrMagnitude().sqrt() 

	"""Unary minus"""
	def __neg__(self):
		return self * -1

	"""Unary addition"""
	def __pos__(self):
		return self

	"""Absolute Value, Equivalent to Magnitude"""
	def __abs__(self):
		return self.magnitude()

	"""In place addition"""
	def __iadd__(self, other):
		if not isinstance(other, Vector3):
			raise TypeError("Expected Vector3 but got '%s'" % str(type(other).__name__))
		self.x += other.x
		self.y += other.y
		self.z += other.z
		return self

	"""Addition"""
	def __add__(self, other):
		v = Vector3()
		v += other
		v += self
		return v

	"""Reverse Addition"""
	def __radd__(self, other):
		return self + other

	"""In place Scalar Multiplication"""
	def __imul__(self, other):
		rhs = d.Decimal(other)
		self.x *= rhs
		self.y *= rhs
		self.z *= rhs
		return self

	"""Scalar Multiplication"""
	def __mul__(self, other):
		v = self.copy()
		v *= other
		return v

	"""Reverse Addition"""
	def __rmul__(self, other):
		return self * other

	"""In place Substraction"""
	def __isub__(self, other):
		if not isinstance(other, Vector3):
			msg = "Expected Vector3 but got '%s'" % str(type(other).__name__)
			raise TypeError(msg)
		self += (other * -1)
		return self

	"""Substraction"""
	def __sub__(self, other):
		v = self.copy()
		v -= other
		return v

	"""Normalize this vector"""
	def normalize(self):
		length = self.magnitude()
		if length < EPSILON:
			self *= 0
			return
		self *= d.Decimal(1) / length

	"""Return this vector normalized"""
	def normalized(self):
		v = self.copy()
		v.normalize()
		return v

# Set constant start position
def _setConstants():
	try:
		from .constants import __name__ as constants_module_name
		from .constants import START_POSITION_HEIGHT_OFFSET
	except SystemError as e:
		from constants import __name__ as constants_module_name
		from constants import START_POSITION_HEIGHT_OFFSET
	import sys
	module = sys.modules[constants_module_name]
	setattr(module, 'START_POSITION', Vector3(0, 0, VL - START_POSITION_HEIGHT_OFFSET))

_setConstants()

"""
Generates Lineary Interpolated points from p0 to p1 with steps of size maxStep or less.
If step lesser than EPSILON then no step is done
"""
def interpolatePoints(p0, p1, maxStep=STEP_MAX):
	direction = p1 - p0
	length_sqr = direction.sqrMagnitude()
	if length_sqr < EPSILON**2:
		yield p0
		return

	dist = d.Decimal(0)
	one = d.Decimal(1)

	segments = int(length_sqr.sqrt() / maxStep)
	if segments <= 1:
		yield p0
		yield p1
		return

	step = one / d.Decimal(segments)

	while True:
		yield p0 + (direction * dist)
		dist += step
		if dist > one:
			break


if __name__ == '__main__':

	print("Init test")
	v = Vector3()
	print(v)
	v2 = Vector3(1,2,3.3)
	print(v2)

	print("Square Magnitude test")
	print(v.sqrMagnitude())
	print(v2.sqrMagnitude())

	print("Magnitude test")
	print(v.magnitude())
	print(v2.magnitude())

	print("In place Addition Tests")
	try:
		v += 1
	except Exception as e:
		print(e.args)

	try:
		v3 = Vector3(1,1,1)
		v3 += v2
		print(v3)
	except Exception as e:
		print(e.args)

	print("Addition Tests")
	try:
		a = v + 1
	except Exception as e:
		print(e.args)

	try:
		v3 = Vector3(1,1,1)
		a = v3 + v2
		print(a)
	except Exception as e:
		print(e.args)

	print("In place Scalar Multiplication Tests")
	try:
		v *= Vector3()
	except Exception as e:
		print(e.args)

	try:
		v3 = Vector3(1,1,1)
		v3 *= 2
		print(v3)
	except Exception as e:
		print(e.args)

	print("Scalar Multiplication Tests")
	try:
		a = v * Vector3()
	except Exception as e:
		print(e.args)

	try:
		v3 = Vector3(1,1,1)
		a = v3 * 4
		print(a)
		print("v3=%s" % str(v3))
	except Exception as e:
		print(e.args)

	print("Unary minus test")
	v3 = Vector3(1,2,3)
	print("v=%s" % str(v3))
	print("-v=%s" % str(-v3))

	print("Substraction test")
	v2 = Vector3(1,0,1)
	v3 = Vector3(1,1,0)
	print("v2=%s" % str(v2))
	print("v3=%s" % str(v3))
	print("v3-v2=%s" % str(v3 - v2))
	print("v3=%s" % str(v3))
	v3 -= v2
	print("(v3-=v2)=%s" % str(v3))

	print("Normalization Tests")
	v3 = Vector3(1,1,1)
	print(v3.normalized())
	print(v3)
	v3.normalize()
	print(v3)

	v3 = Vector3(0,0,0)
	v3.normalize()
	print(v3)

	print("Interpolation Tests")
	p0 = Vector3(0, 0, 0)
	p1 = Vector3(1, 1, 1)
	a = [v for v in interpolatePoints(p0, p1)]
	print("Too long to print but it is here, uncomment if want you to see")
	#print(a)
	print("Interpolation test for points too close")
	print([v for v in interpolatePoints(p0, Vector3(0, EPSILON / d.Decimal(2), 0))])
	print("Interpolation test for points really close")
	print([v for v in interpolatePoints(p0, Vector3(0, EPSILON, 0))])
	print("Interpolation test for points almost really close")
	print([v for v in interpolatePoints(p0, Vector3(0, EPSILON * d.Decimal(2), 0))])
		

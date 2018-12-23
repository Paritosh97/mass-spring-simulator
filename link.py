from math import sqrt

class Link:

	def __init__(self, p1, p2, restingDist):
		self.point1 = p1
		self.point2 = p2
		self.restingDistance = restingDist
		self.stiffness = 1

	def applyConstraints(self):
		dx = self.point1.position[1] - self.point2.position[1]
		dy = self.point1.position[0] - self.point2.position[0]
		hypotenuse = sqrt(dx * dx + dy * dy)
		hypotenuse = 1 if hypotenuse == 0 else hypotenuse
		
		diff = (self.restingDistance - hypotenuse) / hypotenuse		

		translateX = dx * 0.5 * diff
		translateY = dy * 0.5 * diff		

		if (not self.point1.pinned):
			self.point1.position[1] = self.point1.position[1] + translateX
			self.point1.position[0] = self.point1.position[0] + translateY

		if (not self.point2.pinned):
			self.point2.position[1] = self.point2.position[1] - translateX
			self.point2.position[0] = self.point2.position[0] - translateY

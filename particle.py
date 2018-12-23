import pyglet
from math import fabs
from copy import deepcopy

class Particle:

	def __init__(self, pos):
		self.position = pos
		self.lastPosition = pos
		self.mass = 1.0
		self.gravity = 1500
		self.pinned = False
		self.dragged = False
		self.accY = 0.0
		self.accX = 0.0
		self.links = []

	def update(self, timeElapsed):
		
		if (not self.pinned):

			x = round(self.position[1], 5)
			y = round(self.position[0], 5)

			lastX = round(self.lastPosition[1], 5)
			lastY = round(self.lastPosition[0], 5)

			self.applyForce(0, self.gravity)

			velY = lastY - y
			velY = round(velY * 0.99, 5)

			velX = lastX - x
			velX = round(velX * 0.99, 5)

			timeSq = timeElapsed * timeElapsed

			nextY = y - velY - 0.5 * self.accY * timeSq
			nextX = x - velX - 0.5 * self.accX * timeSq

			self.lastPosition = list(self.position)

			self.position[1] = round(nextX, 5)
			self.position[0] = round(nextY, 5)

			self.accX = 0
			self.accY = 0

	def applyConstraints(self):
		if (not self.pinned):
			if (self.position[0] < 10):
				self.position[0] = 10
			if (self.position[0] > 600):
				self.position[0] = 600

			if (self.position[1] < 10):
				self.position[1] = 10
			if (self.position[1] > 600):
				self.position[1] = 600

		for link in self.links:
			link.applyConstraints()

	def applyForce(self, x, y):
		self.accX = self.accX + x
		self.accY = self.accY + y

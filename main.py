import pyglet
from pyglet.gl import *
from math import pi, sin, cos
from particle import Particle
from link import Link
from time import time
from copy import deepcopy

class HelloWorldWindow(pyglet.window.Window):

	def __init__(self):
		super(HelloWorldWindow, self).__init__()
		self.counter = 1
		self.squareSize = 10
		self.width = 10
		self.height = 10
		self.x = 150
		self.y = 150
		self.pointBeingDragged = False
		self.pointDragged = [0, 0]
		self.pointBeingDraggedPosition = [0, 0]
		self.points = self.createNet(self.squareSize, self.width,
									self.height, self.x, self.y)
		self.currentTime = time()
		self.lastTime = time()
		self.timeElapsed = 0.0
		self.startTime = time()
		self.leftOverDeltaTime = 0.0
		self.fixedDeltaTime = 16
		self.constraintAccuracy = 3
		self.set_size(400, 400)

	def on_key_press(self, symbol, modifiers):
		if symbol == pyglet.window.key.SPACE:
			if (self.pointBeingDragged):
				point = self.points[self.pointDragged]

				if (not point.pinned):
					point.pinned = True
					point.position = self.pointBeingDraggedPosition
				else:
					point.pinned = False

	def on_mouse_release(self, x, y, button, modifiers):
		self.pointBeingDragged = False

	def on_mouse_press(self, x, y, button, modifiers):
		pointIndex = 0
		pointsList = []

		for point in self.points:
			pointsList.append([round(point.position[0]), round(point.position[1])])

		for extraX in range(-5, 5):
				for extraY in range(-5, 5):
					try:
						pointIndex = pointsList.index([y + extraY, x + extraX])
					except ValueError:
						pass
					else:
						if (not self.points[pointIndex].pinned):
							self.pointBeingDragged = True
							self.pointDragged = pointIndex
						else:
							self.points[pointIndex].pinned = False

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if (self.pointBeingDragged):
			self.points[self.pointDragged].position = [y, x]
			self.pointBeingDraggedPosition = [y, x]

	def on_mouse_motion(self, x, y, dx, dy):
		pointIndex = 0
		pointsList = []

		for point in self.points:
			pointsList.append([round(point.position[0]), round(point.position[1])])

		for extraX in range(-5, 5):
			for extraY in range(-5, 5):
				try:
					pointIndex = pointsList.index([y + extraY, x + extraX])
				except ValueError:
					pass
				else:
					if (not self.points[pointIndex].pinned):
						self.points[pointIndex].position[0] = self.points[pointIndex].position[0] + dy
						self.points[pointIndex].position[1] = self.points[pointIndex].position[1] + dx



	def drawPoint(self, x, y, color):
		pyglet.graphics.draw(1, GL_POINTS,
							('v2i', (x, y)),
							('c3B', (color[0], color[1], color[2])))

	def circle(self, x, y, radius, color):
		smoothness = int(2*radius*pi)
		glBegin(GL_TRIANGLE_FAN)
		glColor3f(color[0], color[1], color[2])
		for i in range(0, smoothness):
			angle = i * pi * 2.0 / smoothness
			glVertex2f(x + radius * cos(angle), y + radius * sin(angle))
		glEnd()

	def createNet(self, squareSize, width, height, posX, posY):
		points = [Particle([0.0, 0.0]) for x in range(width*height)]

		for point in range(0, len(points)):
			# Link to point to the right (rows)
			if ((point+1) <= len(points) and (point+1) % width != 0):
				points[point].links.append(Link(points[point], points[(point+1)], squareSize))

			# Link to point above (columns)
			if ((point+width) <= len(points)-1):
				points[point].links.append(Link(points[point], points[point+width], squareSize))

		# Pin the top two points
		points[0].pinned = True
		points[0].position = [250, 150]
		points[width-1].pinned = True
		points[width-1].position = [250, 250]

		return points

	def drawNet(self, net):
		for point in net:
			self.circle(point.position[1], point.position[0], 2, [1, 0, 0])

			for link in point.links:
				point1 = link.point1
				point2 = link.point2

				glColor3f(1, 1, 1)
				pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i',
					(int(round(point1.position[1])), int(round(point1.position[0])),
					int(round(point2.position[1])),	int(round(point2.position[0])))))

	def on_draw(self):
		pass

	def update(self, dt):
		self.clear()
		self.drawNet(self.points)

		for accuracy in range(0, self.constraintAccuracy):
			for point in self.points:
				point.applyConstraints()

		for point in self.points:
			point.update(0.016)

if __name__ == '__main__':
    window = HelloWorldWindow()
    pyglet.clock.schedule_interval(window.update, 1.0/60.0)
    pyglet.app.run()

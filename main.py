import pyglet
from pyglet.gl import *
import numpy as np
import scipy.sparse
import scipy.sparse.linalg
from math import pi, sin, cos


class Spring:

    def __init__(self, p1, p2, spring_constant, resting_dist):
        self.point1 = p1
        self.point2 = p2
        self.n = np.zeros(2, dtype=int)
        self.k = spring_constant
        self.r = resting_dist


class Particle:

    def __init__(self, pos):
        self.position = pos
        self.lastPosition = pos
        self.mass = 1.0
        self.pinned = False


class Cloth:

    def __init__(self, width, height, squareSize, spring_constant, time_step):
        self.width = width
        self.height = height
        self.no_of_particles = width * height
        self.springs = []
        self.particles = [Particle(np.zeros(self.no_of_particles, float)) for x in range(self.no_of_particles)]

        for particle in range(0, self.no_of_particles):
            # Link to point to the right (rows)
            if (particle + 1) <= self.no_of_particles and (particle + 1) % width != 0:
                self.springs.append(Spring(self.particles[particle], self.particles[(particle + 1)], spring_constant, squareSize))

            # Link to point above (columns)
            if (particle + width) <= self.no_of_particles - 1:
                self.springs.append(Spring(self.particles[particle], self.particles[particle + width], spring_constant, squareSize))

        # Pin the top two points
        self.particles[0].pinned = True
        self.particles[0].position = [250, 150]
        self.particles[width - 1].pinned = True
        self.particles[width - 1].position = [250, 250]

        self.springs = np.asarray(self.springs)

        self.no_of_springs = self.springs.shape[0]

        self.time_step = time_step
        self.ndim = 2

        self.M, self.Mi = self.compute_M()
        self.L = self.compute_L()
        self.J = self.compute_J()

        self.d = np.empty((self.ndim * self.no_of_springs, 1))
        self.b = np.zeros((self.no_of_particles * self.ndim, 1))

        self.solveAxb = scipy.sparse.linalg.factorized(self.M + self.L * self.time_step ** 2)

    def compute_M(self):
        # Computes the diagonal mass matrix and its inverse. M and M inverse are m*ndims x m*ndims

        mass = []
        massi = []

        for particle in range(0, self.no_of_particles):
            mass.append(self.particles[particle].mass)
            massi.append(1.0 / self.particles[particle].mass)

        return (scipy.sparse.kron(scipy.sparse.diags(mass), np.eye(self.ndim, self.ndim), format='csc'),
                scipy.sparse.kron(scipy.sparse.diags(massi), np.eye(self.ndim, self.ndim), format='csc'))

    def compute_A(self, i):
        # Returns the incidence vector for the i-th spring of size m x 1
        i1 = self.springs[i].n[0]
        i2 = self.springs[i].n[1]
        return scipy.sparse.csc_matrix(([1., -1.], ([i1, i2], [0, 0])), shape=(self.no_of_particles, 1))

    def compute_S(self, i):
        # Returns the i-th spring indicator of size s x 1
        return scipy.sparse.csc_matrix(([1], ([i], [0])), shape=(self.no_of_springs, 1))

    def compute_L(self):
        # Computes the stiffness-weighted Laplacian of the mass-spring graph. L is m*ndims x m*ndims
        l = scipy.sparse.csc_matrix((self.no_of_particles, self.no_of_particles))

        for i in range(self.no_of_springs):
            s = self.springs[i]
            A = self.compute_A(i)
            l += s.k * A * A.transpose()

        return scipy.sparse.kron(l, np.eye(self.ndim, self.ndim), format='csc')

    def compute_J(self):
        # Computes J. J is m*ndims x s*ndims
        j = scipy.sparse.csc_matrix((self.no_of_particles, self.no_of_springs))

        for i in range(self.no_of_springs):
            s = self.springs[i]
            A = self.compute_A(i)
            j += s.k * A * self.compute_S(i).transpose()

        return scipy.sparse.kron(j, np.eye(self.ndim, self.ndim), format='csc')

    def global_step(self):
        # Updates the spring lengths to optimal rest length values while keeping their directions

        def normalized(a):
            # Normalizes each row of a
            n = np.apply_along_axis(np.linalg.norm, 1, a)
            n[n == 0.] = 1  # Leave as is for zero vectors
            return a / n.reshape(-1, 1)

        r = []

        for i in range(self.no_of_springs):
            r.append(self.springs[i].r)

        r = np.asarray(r)

        pi1 = np.empty((self.no_of_springs, self.ndim), float)
        pi2 = np.empty((self.no_of_springs, self.ndim), float)

        for spring in range(0, self.no_of_springs):
            for axis in range(0, self.ndim):
                pi1[spring][axis] = self.particles[self.springs[spring].n[0]].position[axis]
                pi2[spring][axis] = self.particles[self.springs[spring].n[1]].position[axis]

        p = normalized(pi2 - pi1)

        # Compute the directions of springs using the current position of the particles
        self.d[:] = (r[0] * p).reshape(-1, 1)

    def local_step(self):
        # Computes new particles positions by solving Ax=b

        # Update the right hand side.
        self.b.fill(0.)

        pos = np.zeros((self.no_of_particles, self.ndim), float)
        last_pos = np.zeros((self.no_of_particles, self.ndim), float)

        for particle in range(0, self.no_of_particles):
            for axis in range(0, self.ndim):
                pos[particle][axis] = self.particles[particle].position[axis]
                last_pos[particle][axis] = self.particles[particle].lastPosition[axis]

        self.b += self.time_step ** 2 * self.J * self.d
        self.b += self.M * (2 * pos - last_pos).reshape(-1, 1)

        last_pos[:] = pos
        pos[:] = self.solveAxb(self.b).reshape(self.no_of_particles, -1)

        # Copy back
        for particle in range(0, self.no_of_particles):
            if not self.particles[particle].pinned:
                self.particles[particle].position = pos[particle]
                self.particles[particle].lastPosition = last_pos[particle]

    def update(self):
        self.global_step()
        self.local_step()


class HelloWorldWindow(pyglet.window.Window):

    def __init__(self):
        super(HelloWorldWindow, self).__init__()
        self.cloth = Cloth(10, 10, 1, 10, 0.016)
        self.points = self.cloth.particles
        self.links = self.cloth.springs
        self.x = 150
        self.y = 150
        self.set_size(400, 400)

    def drawPoint(self, x, y, color):
        pyglet.graphics.draw(1, GL_POINTS,
                             ('v2i', (x, y)),
                             ('c3B', (color[0], color[1], color[2])))

    def circle(self, x, y, radius, color):
        smoothness = int(2 * radius * pi)
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(color[0], color[1], color[2])
        for i in range(0, smoothness):
            angle = i * pi * 2.0 / smoothness
            glVertex2f(x + radius * cos(angle), y + radius * sin(angle))
        glEnd()

    def drawNet(self, net):
        for point in net:
            self.circle(point.position[1], point.position[0], 2, [1, 0, 0])

            for link in self.links:
                point1 = link.point1
                point2 = link.point2

                glColor3f(1, 1, 1)
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i',
                                                             (int(round(point1.position[1])),
                                                              int(round(point1.position[0])),
                                                              int(round(point2.position[1])),
                                                              int(round(point2.position[0])))))

    def on_draw(self):
        pass

    def update(self, dt):
        self.clear()
        self.drawNet(self.points)

        self.cloth.update()


if __name__ == '__main__':
    window = HelloWorldWindow()
    pyglet.clock.schedule_interval(window.update, 1.0 / 60.0)
    pyglet.app.run()
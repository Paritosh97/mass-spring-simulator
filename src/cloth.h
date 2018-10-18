#ifndef CLOTH_H
#define CLOTH_H

#define CONSTRAINT_ITERATIONS 15

#include <vector>
#include <GL/gl.h>
#include <GL/glut.h>

#include "particle.h"
#include "constraint.h"
#include "vec3.h"

class Cloth
{
private:

	int num_particles_width;
	int num_particles_height;

	std::vector<Particle> particles;
	std::vector<Constraint> constraints;

	Particle* getParticle(int x, int y);
	void makeConstraint(Particle *p1, Particle *p2);

	Vec3 calcTriangleNormal(Particle *p1,Particle *p2,Particle *p3);

	void addWindForcesForTriangle(Particle *p1,Particle *p2,Particle *p3, const Vec3 direction);

	void drawTriangle(Particle *p1, Particle *p2, Particle *p3, const Vec3 color);

public:
    Cloth(float width, float height, int num_particles_width, int num_particles_height);

	void drawShaded();

	void timeStep();

	void addForce(const Vec3 direction);

	void windForce(const Vec3 direction);

	void ballCollision(const Vec3 center,const float radius );

	void doFrame();
};


#endif
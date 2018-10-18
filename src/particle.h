#ifndef PARTICLE_H
#define PARTICLE_H

#define DAMPING 0.01 // how much to damp the cloth simulation each frame
#define TIME_STEPSIZE2 0.5*0.5 // how large time step each particle takes each frame

#include "vec3.h"

class Particle
{
private:
	bool movable;

	float mass;

	Vec3 pos;
	Vec3 old_pos;
	Vec3 acceleration;
	Vec3 accumulated_normal;

public:

    Particle(Vec3 pos);

    Particle();
	
	void addForce(Vec3 f);

	void timeStep();

	Vec3& getPos();

	void resetAcceleration();

	void offsetPos(const Vec3 v);

	void makeUnmovable();

	void addToNormal(Vec3 normal);

	Vec3& getNormal();

	void resetNormal();
};

#endif
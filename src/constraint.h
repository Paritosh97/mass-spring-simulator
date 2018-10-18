#ifndef CONSTRAINT_H
#define CONSTRAINT_H

#include "particle.h"

class Constraint
{
private:
	float rest_distance; // the length between particle p1 and p2 in rest configuration

public:
	Particle *p1, *p2; // the two particles that are connected through this constraint

	Constraint(Particle *p1, Particle *p2);

	void satisfyConstraint();
};

#endif
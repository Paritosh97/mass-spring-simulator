#ifndef VEC3_H
#define VEC3_H

#include <math.h>

class Vec3
{
public:
	float f[3];

    Vec3(float x, float y, float z);

    Vec3();

    float length();

	Vec3 normalized();

	void operator+= (const Vec3 &v);

	Vec3 operator/ (const float &a);

	Vec3 operator- (const Vec3 &v);

	Vec3 operator+ (const Vec3 &v);

	Vec3 operator* (const float &a);

	Vec3 operator-();

	Vec3 cross(const Vec3 &v);

	float dot(const Vec3 &v);
};

#endif
# Simulator for Mass Spring Systems


## Explicit Euler

### Description
The most basic first-order procedure for solving ordinary differential equations. In this integration scheme, we predict the next position of the particle using the previous velocity. This results in inaccuracies with larger timesteps since the solution for the timestep is a tangent to the original curve imposing the problem of energy conservation. 

[Demo](./explicit-euler/explicit-euler.html){:target="_blank" rel="noopener"}


## Semi Implicit Euler

### Description
The semi-implicit Euler integration solves the problem of energy conservation. Here, we use the current velocity instead of the previous velocity.

[Demo](./semi-implicit-euler/semi-implicit-euler.html){:target="_blank" rel="noopener"}


## Implicit Euler

### Description
Also, known as the Backward Euler method. Here, we predict the next position of the particle using the next velocity(hence implicit). Thus, achieving higher accuracy but at higher computation costs.

<!--[Demo](./implicit-euler/implicit-euler.html){:target="_blank" rel="noopener"}-->


## Verlet Integration

### Description
A popular technique used in ragdoll physics and inverse kinematics. We store the previous positions of the particles instead of the velocity and predict the next position using the current position, previous position, and the acceleration.

<!--[Demo](./verlet/verlet.html){:target="_blank" rel="noopener"}-->


## Runge-Kutta, Position Based Dynamics, Corotated linear, Block Coordinate Descent
[WIP]


<!--
## Runge-Kutta

### Description
[TODO Small Description]

[Demo](./runge-kutta/runge-kutta.html){:target="_blank" rel="noopener"}


## Position Based Dynamics

### Description
[TODO Small Description]

[Demo](./position-based-dynamics/position-based-dynamics.html){:target="_blank" rel="noopener"}


## Corotated Linear

### Description
[TODO Small Description]

[Demo](./corotated-linear/corotated-linear.html){:target="_blank" rel="noopener"}


## Block Coordinate Descent

### Description
[TODO Small Description]

[Demo](./block-coordinate-descent/block-coordinate-descent.html){:target="_blank" rel="noopener"}
-->

# About
Particle sim using simple physics and Euler's method. Newtonian mechanics are used for $F=ma$, and the position and velocity updates follow for the force acting on the particle, 

$a_{i+1} = F/m,$

$v_{i+1}=v_i+a_idt,$

$x_{i+1}=x_i+v_idt.$

Forces can be gravitational, electric, or spring-like:

$F = \frac{GmM}{x^2}$

$F = \frac{kqQ}{x^2}$

$F = \frac{1}{2}kx^2$

All forces and positions are 3D vectors, and the simulation configuration rules are stored in `toybox.py`.

# References
- https://nssdc.gsfc.nasa.gov/planetary/factsheet/

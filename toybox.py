import particle
import numpy as np

p1 = particle.Particle(q=0,
  m=1e5,
  s=0,
  name='Sun',
  color='yellow')
p2 = particle.Particle(q=0,
  m=1e1,
  s=0,
  rvec=np.array([5.,5.,0]),
  vvec=np.array([-10.,10.,0]),
  name='Earth',
  color='blue')
p3 = particle.Particle(q=0,
  m=1e-3,
  s=0,
  rvec=np.array([5.1,5.,0]),
  vvec=np.array([-10.,10.,0]), 
  name='Moon',
  color='gray')
p4 = particle.Particle(q=0,
  m=1e4,
  s=0,
  rvec=np.array([30.1,0,0]),
  vvec=np.array([-5,10.,0]), 
  name='Jupiter',
  color='red')
particles = [p1,p2,p3,p4]
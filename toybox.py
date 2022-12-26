import particle
import numpy as np
import pandas as pd

planet_info = pd.read_csv('planets.txt', sep='\t', index_col=0)
mass_sun = 1.9891e30 #kg
inds = [str(ind).strip() for ind in planet_info.loc['OrbitalInclination(degrees)'].index]
planet_info.columns = inds
#print(planet_info.loc['OrbitalInclination(degrees)'].index)
print(planet_info.index)


sun = particle.Particle(q=0,
  m=mass_sun,
  s=0,
  name='Sun',
  color='yellow')
theta_earth = planet_info.loc['OrbitalInclination(degrees)','EARTH']*np.pi/180
vy_init = planet_info.loc['OrbitalVelocity(km/s)','EARTH']*1e3*np.cos(theta_earth)
vz_init = planet_info.loc['OrbitalVelocity(km/s)','EARTH']*1e3*np.sin(theta_earth)
earth = particle.Particle(q=0,
  m=planet_info.loc['Mass(10^24kg)','EARTH']*1e24,
  s=0,
  rvec=np.array([planet_info.loc['Perihelion(10^6km)','EARTH']*1e9,0,0]),
  vvec=np.array([0,vy_init,vz_init]),
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
#particles = [p1,p2,p3,p4]
solar_system = [sun,earth]
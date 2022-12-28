import particle
import numpy as np
import pandas as pd

planet_info = pd.read_csv('planets.txt', sep='\t', index_col=0)
mass_sun = 1.9891e30 #kg
inds = [str(ind).strip() for ind in planet_info.loc['OrbitalInclination(degrees)'].index]
planet_info.columns = inds

def make_moon(planet_name,moon_name,color,theta_planet=None,theta_moon=None,v_planet=None,
  v_moon=None,perihelion_planet=None,perihilion_moon=None,m=None):
  if theta_planet is None:
    theta_planet = float(planet_info.loc['OrbitalInclination(degrees)',planet_name])*np.pi/180
  if theta_moon is None:
    theta_moon = float(planet_info.loc['OrbitalInclination(degrees)',moon_name])*np.pi/180
  if v_planet is None:
    v_planet = float(planet_info.loc['OrbitalVelocity(km/s)',planet_name])*1e3
  if v_moon is None:
    v_moon = float(planet_info.loc['OrbitalVelocity(km/s)',moon_name])*1e3
  if perihelion_planet is None:
    perihelion_planet = planet_info.loc['Perihelion(10^6km)',planet_name]*1e9
  if perihilion_moon is None:
    perihilion_moon = planet_info.loc['Perihelion(10^6km)',moon_name]*1e9
  if m is None:
    m = planet_info.loc['Mass(10^24kg)',moon_name]*1e24

  vy_init = v_planet*np.cos(theta_planet)+v_moon*np.cos(theta_moon)
  vz_init = v_planet*np.sin(theta_planet)+v_moon*np.sin(theta_moon)
  return particle.Particle(q=0,
    m=m,
    s=0,
    rvec=np.array([perihelion_planet+perihilion_moon,0,0]),
    vvec=np.array([0,vy_init,vz_init]),
    name=moon_name,
    color=color)

def make_planet(name,color,theta=None,v=None,perihelion=None,m=None):
  if theta is None:
    theta = float(planet_info.loc['OrbitalInclination(degrees)',name])*np.pi/180
  if v is None:
    v = float(planet_info.loc['OrbitalVelocity(km/s)',name])*1e3
  if perihelion is None:
    perihelion = planet_info.loc['Perihelion(10^6km)',name]*1e9
  if m is None:
    m = planet_info.loc['Mass(10^24kg)',name]*1e24

  vy_init = v*np.cos(theta)
  vz_init = v*np.sin(theta)
  return particle.Particle(q=0,
    m=m,
    s=0,
    rvec=np.array([perihelion,0,0]),
    vvec=np.array([0,vy_init,vz_init]),
    name=name,
    color=color)

sun = particle.Particle(q=0,
  m=mass_sun,
  s=0,
  name='Sun',
  color='yellow')
earth = make_planet('EARTH','blue')
moon = make_moon('EARTH','MOON','grey')
mars = make_planet('MARS','red')
pluto = make_planet('PLUTO','cyan')
mercury = make_planet('MERCURY','brown')
venus = make_planet('VENUS','pink')
saturn = make_planet('SATURN','green')
jupiter = make_planet('JUPITER','orange')
uranus = make_planet('URANUS','aqua')
neptune = make_planet('NEPTUNE','purple')
#particles = [p1,p2,p3,p4]
close_planets = [sun,mercury,venus,earth,moon,mars]
solar_system = [sun,mercury,venus,earth,mars,saturn,jupiter,uranus,pluto]

spring1 = particle.Particle(q=0,
  m=1e9,
  s=1,
  name='Big spring 1',
  rvec=[0,-1,0],
  size=100,
  color='orange',
  moveable=False)
spring2 = particle.Particle(q=0,
  m=1e9,
  s=1,
  name='Big spring 2',
  rvec=[0,1,0],
  size=100,
  color='orange',
  moveable=False)

big_charge = 5
positive1 = particle.Particle(s=0,
  m=1e9,
  q=big_charge,
  name='Big positive 1',
  rvec=[0,1,0],
  size=100,
  color='red',
  moveable=False)
negative1 = particle.Particle(s=0,
  m=1e9,
  q=-big_charge,
  name='Big negative 1',
  rvec=[0,-1,0],
  size=100,
  color='blue',
  moveable=False)

def make_up(quark_rmax = 1):
  up = particle.Particle(s=1/2,
    m=1,
    q=2/3,
    name='Up',
    rvec=np.random.uniform(-1*quark_rmax,quark_rmax,3),
    color='pink',
    marker='o'
    )
  return up

def make_down(quark_rmax = 1):
  down = particle.Particle(s=1/2,
    m=1,
    q=-1/3,
    name='Down',
    rvec=np.random.uniform(-1*quark_rmax,quark_rmax,3),
    color='cyan',
    marker='o'
    )
  return down


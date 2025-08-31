import toybox
import dynamics
import particle

#Constants
dt = 0.0001
day = 86400 #seconds in a day
n = 6
m = 1
q = 1
s = 1
g = 0
boundary = None
update_rate = int(2e3)
part_name = 'Charge'
memory = 100000 #remember most recent points
planet_framerate = 5

particles = particle.make_particles(n,m=m,rmax=1,vmax=0,charge=q,s=s,g=g,
  name=part_name,a0=1e-1)
#particles.extend([toybox.spring1,toybox.spring2])
#particles.extend([toybox.positive1,toybox.negative1])
#particles = particle.make_particles(n,m,rmax=2,rtype='gaussian',charge=q)
solar_system = toybox.solar_system
close_planets = toybox.close_planets
planets = solar_system

frames=100
dir = f'Gifs/solar_system/close_planets'
fname = f'close_planets_day_100_frames{frames}'
dynamics.sim_particle_motions(planets,boundary,memory,day*5e-1,timeit=True,
  xlim=1.1*planets[-1].rvec[0],ylim=1.1*planets[-1].rvec[0],
  save=False,dir=dir,fname=fname,frames=frames,update_rate=update_rate,set_legend=True)

dir = f'Gifs/frames{frames}'
fname = f'n{n}_m{m}_q{q}_s{s}_g{g}_memory{memory}_boundary{boundary}_dt{dt}'
# dynamics.sim_particle_motions(particles,
#   boundary,
#   memory,
#   dt,
#   save=False,
#   timeit=True,
#   dir=dir,
#   fname=fname,
#   frames=frames,
#   update_rate=100,
#   display_rate=1,
#   closest_N=n)

n_neutrons = 4
n_protons = 0
n_ups = 1*n_neutrons + 2*n_protons
n_downs = 2*n_neutrons + 1*n_protons
quarks = []
for i in range(n_ups):
  quarks.append(toybox.make_up())
for i in range(n_downs):
  quarks.append(toybox.make_down())

fname = f'quarks_memory{memory}_boundary{boundary}_dt{dt}' 
# dynamics.sim_particle_motions(quarks,
#   boundary,
#   memory,
#   dt,
#   save=False,
#   timeit=True,
#   dir=dir,
#   fname=fname,
#   frames=frames,
#   update_rate=update_rate,
#   display_rate=1,
#   closest_N=n,
#   set_legend=False)


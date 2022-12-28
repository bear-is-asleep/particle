import toybox
import dynamics
import particle

#Constants
dt = 0.001
day = 86400 #seconds in a day
n = 20
m = 1
q = 1
s = 0
g = 0.1
boundary = None
memory = 5000 #remember most recent points
planet_framerate = 5

particles = particle.make_particles(n,m=m,rmax=5,vmax=1,charge=q,s=s,g=g)
#particles = particle.make_particles(n,m,rmax=2,rtype='gaussian',charge=q)
solar_system = toybox.solar_system
close_planets = toybox.close_planets

frames=50
# dir = f'Gifs/solar_system/close_planets'
# fname = f'close_planets_day_100_frames{frames}'
# dynamics.sim_particle_motions(close_planets,boundary,memory,day,timeit=False,display_rate=5,
#   xlim=1.1*close_planets[-1].rvec[0],ylim=1.1*close_planets[-1].rvec[0],
#   save=False,dir=dir,fname=fname,save_after=frames,update_rate=5)

dir = f'Gifs/frames{frames}'
fname = f'n{n}_m{m}_q{q}_s{s}_g{g}_memory{memory}_boundary{boundary}_dt{dt}'
dynamics.sim_particle_motions(particles,
  boundary,
  memory,
  dt,
  save=True,
  timeit=True,
  dir=dir,
  fname=fname,
  frames=frames,
  update_rate=100,
  display_rate=1,
  closest_N=n)

        


import toybox
import dynamics
import particle

#Constants
dt = 0.1
day = 86400 #seconds in a day
n = 3
m = 1
q = 0
s = 1
boundary = None
memory = 50 #remember most recent points
planet_framerate = 5

particles = particle.make_particles(n,m=m,rmax=1,charge=q,s=s)
#particles = particle.make_particles(n,m,rmax=2,rtype='gaussian',charge=q)
solar_system = toybox.solar_system
close_planets = toybox.close_planets

# dynamics.sim_particle_motions(close_planets,boundary,memory,day/100,timeit=False,display_rate=5,
#   xlim=1.1*close_planets[-1].rvec[0],ylim=1.1*close_planets[-1].rvec[0])
dynamics.sim_particle_motions(particles,boundary,memory,dt)

        


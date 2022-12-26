import toybox
import dynamics
import particle

#Constants
dt = 86400 
day = 86400 #seconds in a day
n = 10
m = 1
q = 1
s = 0
boundary = None
memory = 500 #remember most recent points

#particles = particle.make_particles(n,m=m,rmax=1,charge=q,s=s)
#particles = particle.make_particles(n,m,rmax=2,rtype='gaussian',charge=q)
solar_system = toybox.solar_system

dynamics.sim_particle_motions(solar_system,boundary,memory,day,timeit=False,display_rate=5)

        


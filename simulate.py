import toybox
import dynamics
import particle

#Constants
dt = 0.01
n = 10
m = 1
q = 1
s = 0
boundary = None
memory = 50 #remember most recent points

#particles = particle.make_particles(n,m=m,rmax=1,charge=q,s=s)
particles = particle.make_particles(n,m,rmax=2,rtype='gaussian',charge=q)

dynamics.sim_particle_motions(particles,boundary,memory,dt,framerate=600,display_rate=5)

        


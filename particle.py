import numpy as np

G = 0.1 #Gravitational constant
GN = 6.6743e-11 # Newtons's Gm3 kg-1 s-2
class Particle:

  k = 10 #EM Coupling constant - all have the same constant

  def __init__(self,q=0,m=1,s=0,a0=1e-1,name=None,rvec=np.zeros(3),vvec=np.zeros(3),avec=np.zeros(3),color=None,
    g=0): #
    self.rvec = rvec #location
    self.vvec = vvec #velocity
    self.avec = avec #acceleration
    self.q = q #charge
    self.m = m #mass
    self.name = name #
    self.s = s #s is spring constant used, 0 for no springiness
    self.a0 = a0 #minimum distance (Bound state formation)?
    self.color = color #Set color for particle point
    self.g = g #Set downward acceleration

  def get_r(self,rvec): #Distance between particle and other point
    tot = 0
    assert (len(rvec) == 3)
    for i in range(3):
      tot+= (self.rvec[i]-rvec[i])**2
    return max(np.sqrt(tot),self.a0) #returns max between distance and smallest possible distance

  def v_t(self,avec,dt): #Find velocity given acceleration
    vvec = np.zeros(3) #Initialize return velocity
    for i in range(3):
      vvec[i] = avec[i]*dt+self.vvec[i]
    return vvec

  def get_rhat(self,rvec):
    assert (len(rvec) == 3)
    r = self.get_r(rvec)
    return (self.rvec-rvec)/r #rvec/rmag = rhat

  def a_g(self,m,r,G=G): #Graviational acceleration
    return -G*m/r**2
  def a_s(self,r,s): #Spring acceleration
    if self.m == 0:
      return 0
    return -np.sqrt(self.s*s)*r**2/(2*self.m)
  def a_C(self,r,q): #Coloumb acceleration
    if self.m == 0:
      return 0
    return self.k*self.q*q/(self.m*r**2) #Coloumb acceleration
  def a_fall(self): #Downward graviation
    if self.m == 0:
      return 0
    return self.g

class EMParticle(Particle): #Make em particle to simulate coloumb force
  k = 10 #Coupling constant - all have the same constant

  def __init__(self): 
    Particle.__init__(self)

  def a_C(self,r,q): #Coloumb acceleration
    return self.k*self.q*q/(self.m*r**2) #Coloumb acceleration


class SpringParticle(Particle): #Make spring particle to simulate spring force
  def __init__(self): 
    Particle.__init__(self)
  def a_s(self,r,s): #Spring acceleration
    return np.sqrt(self.s*s)*r**2/(2*self.m)


def make_particles(n,m=50,rmax=10,vmax=0,amax=0,rtype='uniform',dim=2,charge=1,
  s=0,g=0): 
  """
  Make n random particles and turn them into a list
  """
  particles = []
  for _ in range(n):
    q = np.random.choice([-charge,charge])
    if rtype == 'uniform':
      #Acceleration, velocity, acceleration initialize
      rvec = np.random.uniform(-1*rmax,rmax,3)
      vvec = np.random.uniform(-1*vmax,vmax,3)
      avec = np.random.uniform(-1*amax,amax,3)
    elif rtype == 'gaussian':
      #Acceleration, velocity, acceleration initialize
      rvec = np.random.normal(0,rmax,3)
      vvec = np.random.uniform(0,vmax,3)
      avec = np.random.uniform(0,amax,3)
    if dim == 2:
      rvec[2] = 0.0
      vvec[2] = 0.0
      avec[2] = 0.0
    # if isinstance(part_type,EMParticle):
    #   part = EMParticle(q=q,m=m,s=s,rvec=rvec,vvec=vvec,avec=avec)
    # elif isinstance(part_type,Particle):
    #   part = Particle(q=q,m=m,s=s,rvec=rvec,vvec=vvec,avec=avec)
    # elif isinstance(part_type,SpringParticle):
    #   part = SpringParticle(q=q,m=m,s=s,rvec=rvec,vvec=vvec,avec=avec)
    part = Particle(q=q,m=m,s=s,rvec=rvec,vvec=vvec,avec=avec,g=g)
    particles.append(part)
  return particles

  
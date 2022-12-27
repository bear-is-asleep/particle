#import particle
import pylab as plt
import numpy as np
import time
import particle


def sim_particle_motions(particles,boundary,memory,dt,timeit=False,display_rate=10,
  xlim=None,ylim=None):

  fig = plt.figure(figsize=(9,7))
  fig.set_facecolor('black')
  ax = fig.add_subplot()
  if boundary is not None:
    ax.set_xlim([-1.01*boundary,1.01*boundary])
    ax.set_ylim([-1.01*boundary,1.01*boundary])
    ax.axhline(-boundary,color='white')
    ax.axhline(boundary,color='white')
    ax.axvline(-boundary,color='white')
    ax.axvline(boundary,color='white')
  if xlim is not None:
    ax.set_xlim([-xlim,xlim])
  if ylim is not None:
    ax.set_ylim([-ylim,ylim])
  ax.axis('off')
  ax.xaxis.label.set_color('white')        #setting up X-axis label color to yellow
  ax.yaxis.label.set_color('white')          #setting up Y-axis label color to blue

  ax.tick_params(axis='x', colors='white')    #setting up X-axis tick color to red
  ax.tick_params(axis='y', colors='white')  #setting up Y-axis tick color to black

  ax.spines['left'].set_color('white')        # setting up Y-axis tick color to red
  ax.spines['top'].set_color('white')         #setting up above X-axis tick color to red
  ax.set_facecolor('black')
  plt.ion()

  nparts = len(particles)
  rvecs = np.zeros((nparts,memory,3)) #Positions
  vvecs = np.zeros((nparts,memory,3)) #Velocities
  avecs = np.zeros((nparts,memory,3)) #Accelerations

  points = []
  graphs = []
  legend = []

  for i,part in enumerate(particles):
    rvecs[i] = part.rvec #r init
    vvecs[i] = part.vvec #v init
    avecs[i] = part.avec #a init
    points.append(plt.scatter(0,0))
    graphs.append(plt.plot(part.rvec[0],part.rvec[1])[0])
    if part.name is not None:
      legend.append([points[i],f'{part.name} ({np.linalg.norm(part.vvec):<.1f} SPEED)'])

  leg = ax.legend([i[0] for i in legend],[i[1] for i in legend])
  background = fig.canvas.copy_from_bbox(ax.bbox)

  cnt = -1
  while True:
    #ax.clear()
    #fig.canvas.restore_region(background)
    leg.remove()
    legend.clear()
    update = False
    cnt+=1
    tot_sim_start = time.time()
    for j,part in enumerate(particles):
      #Current coordinates
      rvec = rvecs[j,-1]
      vvec = vvecs[j,-1]
      avec = avecs[j,-1]
      part.rvec = rvec
      part.vvec = vvec
      part.avec = avec

      other_parts = particles[:j]+particles[j+1:] 
      avec_next = np.zeros(3)
      for k,other_part in enumerate(other_parts):
        #Compare to other em particle positons, get forces based on 
        r = part.get_r(other_part.rvec) #Seperation between two 
        rhat = part.get_rhat(other_part.rvec) #Direction of seperation
        m,q,s = other_part.m,other_part.q,other_part.s #mass, charge, spin
        a = part.a_g(m,r,G=particle.GN) #acceleration due to gravity
        a+=part.a_C(r,q) #acceleration due to em
        a+=part.a_s(r,s) #acceleration due to spring
        avec_next += a*rhat #Get vector acceleration
      avecs[j,-2] = avec_next
      avec = avecs[j,-2]
      #Destroy first points to preserve memory
      #print(avec.shape,np.reshape(rvec+dt**2*avec/2+vvec*dt,(1,3)),np.reshape(part.v_t(avec,dt),(1,3)))
      rvecs[j] = np.append(rvecs[j,1:],np.reshape(rvec+dt**2*avec/2+vvec*dt,(1,3)),axis=0) #Get vector position #update values
      vvecs[j] = np.append(vvecs[j,1:], np.reshape(part.v_t(avec,dt),(1,3)),axis=0) #Get vector velocity
      avecs[j] = np.append(avecs[j,1:],np.reshape(avec,(1,3)),axis=0) #add dumby value
      
      if boundary is not None:
        for k in range(3):
          if abs(rvecs[j,-1][k]) > boundary:
            vvecs[j,-1][k] = -vvecs[j,-1][k]
    tot_sim_end = time.time()
    tot_plot_start = time.time()
    #if cnt*dt/86400%1 == 0:
    if 10*cnt*dt%1 == 0:
      update = True
    #update=True
    if update:
      for i,part in enumerate(particles):

        if part.color is None:
          if part.q < 0:
            color = 'blue'
          elif part.q > 0:
            color = 'red'
          elif part.q == 0:
            color = 'yellow'
        else:
          color = part.color
        if part.s > 0:
          marker = 'x'
        else:
          marker = 'o'
        part.rvec = rvecs[i,-1]
        part.vvec = vvecs[i,-1]
        part.avec = avecs[i,-1]
        points[i].remove()
        graphs[i].remove()
        points[i] = plt.scatter(part.rvec[0],part.rvec[1],color=color,label=part.name,marker=marker)
        graphs[i] = plt.plot(rvecs[i,:,0],rvecs[i,:,1],color=color,label=part.name,alpha=0.5)[0]
        if part.name is not None:
          legend.append([points[i],f'{part.name} (v = {np.linalg.norm(part.vvec)/1e3:<.2f} km/s d = {np.linalg.norm(part.rvec)/1.496e+11:<.2f} AU)'])
        #print(f'{part.name} ({np.linalg.norm(part.vvec):<.1f} SPEED)')
      #print([i[1] for i in legend])
      make_graphs_end = time.time()
      #plt.title(f't = {dt*cnt/86400:<.2f} days',color='white')
      plt.title(f't = {dt*cnt:<.2f}',color='white')
      leg = ax.legend([i[0] for i in legend],[i[1] for i in legend]) #Get items from columns of legend list
      leg.get_frame().set_alpha(0.3)
      #leg.get_frame().set_facecolor((0, 0, 1, 0.1))
      plt.draw()
      plt.pause(1/6e5)
    tot_plot_end = time.time()
    if timeit and cnt%display_rate == 0:
      print(f'Sim time (s): {tot_sim_end-tot_sim_start:<.3f}')
      print(f'Plot time (s): {tot_plot_end-tot_plot_start:<.3f}')
      print(f'-Make graph time (s): {make_graphs_end-tot_plot_start:<.3f}')
      

    




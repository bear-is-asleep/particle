#import particle
import pylab as plt
import numpy as np
import time
import particle
import os
import plotters
import helpers



def sim_particle_motions(particles,boundary,memory,dt,timeit=False,display_rate=10,
  xlim=None,ylim=None,save=False,dir='Gifs',fname='sim',frames=100,update_rate=1,
  closest_N=1e9):
  """
  Sim particle motions with option to save as gif
  frames: amount of pngs to make before saving, then deleting pngs
  """
  if save:
    os.system(f'mkdir -p {dir}')

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
  save_cnt = 0 #Cnt saved images
  update = True
  while True:
    if update: #Only stop sim time if we've updated the plot
      tot_sim_start = time.time()
    #ax.clear()
    #fig.canvas.restore_region(background)
    leg.remove()
    legend.clear()
    update = False
    cnt+=1
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
      check_other_size = len(other_parts)>closest_N
      if check_other_size:
        #use only closest N particles to do physics
        distance_other = dict.fromkeys(list(range(len(other_parts))))
        for k,other_part in enumerate(other_parts):
          distance_other[k] = part.get_r(other_part.rvec) #Seperation between two 
        distance_other = dict(sorted(distance_other.items(), key=lambda item: item[1]))
        closest_parts = dict(list(distance_other.items())[:closest_N]) 
        furthest_parts = dict(list(distance_other.items())[:closest_N]) 
        #print(closest_parts,furthest_parts)

      
      for k,other_part in enumerate(other_parts):
        calc_inverse = True #calc all inverse power law acceleration
        calc_polynomial = True #calc all positive polynomial power law acceleration
        if check_other_size:
          if k not in closest_parts.keys(): #Check to see which forces we need to calc
            calc_inverse = False
          if k not in furthest_parts.keys(): #Check to see which forces we need to calc
            calc_polynomial = False
        if not (calc_inverse and calc_polynomial): #Skip if we're not calculating forces
          continue
        a = 0
        #Compare to other em particle positons, get forces based on 
        r = part.get_r(other_part.rvec) #Seperation between two 
        rhat = part.get_rhat(other_part.rvec) #Direction of seperation
        m,q,s = other_part.m,other_part.q,other_part.s #mass, charge, spin
        if calc_inverse:
          a+= part.a_g(m,r,G=particle.GN) #acceleration due to gravity
          if q != 0:
            a+=part.a_C(r,q) #acceleration due to em
        if calc_polynomial and s!=0:
          a+=part.a_s(r,s) #acceleration due to spring
        avec_next += a*rhat-part.g*np.array([0,1,0]) #Get vector acceleration
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
    #if cnt*dt/86400%10 == 0:
    #if 10*cnt*dt%1 == 0:
    if cnt%update_rate == 0:
      update = True
    #update=True
    if update:
      tot_sim_end = time.time()
      tot_plot_start = time.time()
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
      if save:
        plt.savefig(fname=f'{dir}/{fname}_{save_cnt}.jpg')
        if save_cnt > frames:
          plotters.make_image_gif(dir+'/',fname)
          break
        save_cnt += 1
      else:
        plt.draw()
        plt.pause(1/6e5)
      tot_plot_end = time.time()
      if timeit and cnt%display_rate == 0:
        helpers.print_stars()
        print(f'Frames made: {cnt}')
        print(f'Sim time (s): {tot_sim_end-tot_sim_start:<.3f}')
        print(f'Plot time (s): {tot_plot_end-tot_plot_start:<.3f}')
        print(f'--Make graph time (s): {make_graphs_end-tot_plot_start:<.3f}')
  


    




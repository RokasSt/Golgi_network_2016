
import sys
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import seaborn as sns
import pyspike
import methods
import string
import subprocess
import os

def Synchronization_analysis(sim_duration,specify_targets,no_of_groups,exp_specify,trial_ids_for_raster_plot):

    #get target ids

    target_cell_array=methods.get_cell_ids_for_sync_analysis(specify_targets,no_of_groups,exp_specify)

    
    n_trials=exp_specify[2]
    # make different spike subplots for different populations later
    fig, ax = plt.subplots(figsize=(4,2),ncols=1,nrows=2, sharex=True)
    lines = []
    labels = []

    distances = []
    color = sns.color_palette()[0]

    if string.lower(specify_targets[0])=="all":
       for trial in range(0,n_trials):
           sim_dir = 'simulations/' + exp_specify[0]+'/sim%d'%trial+'/txt'
           spike_trains = []
           for pop in range(0,len(target_cell_array)):
               for cell in range(0,len(target_cell_array[pop])):
                   #create target txt file containing spike times
                   methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,cell),exp_specify[0],trial)
                   spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop, cell))
                   spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                   spike_trains.append(spike_train)
                   if trial in trial_ids_for_raster_plot:
                      ax[trial].scatter(spikes,np.zeros_like(spikes)+cell,marker='|',s=2,c=color)
           distances.append(pyspike.spike_profile_multi(spike_trains))
           
    if (specify_targets[0]=="3D region specific") and (not("subtype specific" in specify_targets )):
       for trial in range(0,n_trials):
           sim_dir = 'simulations/' + exp_specify[0]+'/sim%d'%trial+'/txt'
           spike_trains = []
           if exp_specify[1][1]==True:
              for pop in range(0,len(target_cell_array)):
                  for cell in range(0,len(target_cell_array[pop])):
                      #create target txt file containing spike times
                      methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[pop][cell]),exp_specify[0],trial)
                      spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[pop][cell]))
                      spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                      spike_trains.append(spike_train)
                   
                      if trial in trial_ids_for_raster_plot:
                         ax[trial].scatter(spikes,np.zeros_like(spikes)+target_cell_array[pop][cell],marker='|',s=2,c=color)
           else:
              for pop in range(0,len(target_cell_array)):
                  for cell in range(0,len(target_cell_array[pop])):
                      methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[trial][pop][cell]),exp_specify[0],trial)
                      spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[trial][pop][cell]))
                      spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                      spike_trains.append(spike_train)
                   
                      if trial in trial_ids_for_raster_plot:
                         ax[trial].scatter(spikes,np.zeros_like(spikes)+target_cell_array[trial][pop][cell],marker='|',s=2,c=color)
                            
           distances.append(pyspike.spike_profile_multi(spike_trains))
          
    if (specify_targets[0]=="3D region specific") and ("subtype specific" in specify_targets):
       for trial in range(0,n_trials):
           sim_dir = 'simulations/' + exp_specify[0]+'/sim%d'%trial+'/txt'
           spike_trains = []
           if exp_specify[1][1]==True:
              if ("randomly set target ids only once" in specify_targets ) or ("explicit list" in specify_targets):
                 for pop in range(0,len(target_cell_array)):
                     for cell in range(0,len(target_cell_array[pop])):
                         #create target txt file containing spike times
                         methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[pop][cell]),exp_specify[0],trial)
                         spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[pop][cell]))
                         spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                         spike_trains.append(spike_train)
                   
                         if trial in trial_ids_for_raster_plot:
                            ax[trial].scatter(spikes,np.zeros_like(spikes)+target_cell_array[pop][cell],marker='|',s=2,c=color)
              else:
                 for pop in range(0,len(target_cell_array)):
                     for cell in range(0,len(target_cell_array[pop])):
                         methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[trial][pop][cell]),exp_specify[0],trial)
                         spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[trial][pop][cell]))
                         spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                         spike_trains.append(spike_train)
                   
                         if trial in trial_ids_for_raster_plot:
                            ax[trial].scatter(spikes,np.zeros_like(spikes)+target_cell_array[trial][pop][cell],marker='|',s=2,c=color)
           else:
              for pop in range(0,len(target_cell_array)):
                  for cell in range(0,len(target_cell_array[pop])):
                      methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[trial][pop][cell]),exp_specify[0],trial)
                      spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[trial][pop][cell]))
                      spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                      spike_trains.append(spike_train)
                   
                      if trial in trial_ids_for_raster_plot:
                         ax[trial].scatter(spikes,np.zeros_like(spikes)+target_cell_array[trial][pop][cell],marker='|',s=2,c=color)
                         
           distances.append(pyspike.spike_profile_multi(spike_trains))
          
    if string.lower(specify_targets[0])=="subtype specific":
       for trial in range(0,n_trials):
           sim_dir = 'simulations/' + exp_specify[0]+'/sim%d'%trial+'/txt'
           spike_trains = []
           if specify_targets[0][2]=="randomly set target ids only once":
              for pop in range(0,len(target_cell_array)):
                  for cell in range(0,len(target_cell_array[pop])):
                       #create target txt file containing spike times
                       methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[pop][cell]),exp_specify[0],trial)
                       spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[pop][cell]))
                       spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                       spike_trains.append(spike_train)
                   
                       if trial in trial_ids_for_raster_plot:
                          ax[trial].scatter(spikes,np.zeros_like(spikes)+target_cell_array[pop][cell],marker='|',s=2,c=color)
           else:
              for pop in range(0,len(target_cell_array)):
                  for cell in range(0,len(target_cell_array[pop])):
                      #create target txt file containing spike times
                      if n_trials==1:
                         methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[pop][cell]),exp_specify[0],trial)
                         spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[pop][cell]))
                      else:
                         methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[trial][pop][cell]),exp_specify[0],trial)
                         spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[trial][pop][cell]))
                      spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                      spike_trains.append(spike_train)
                   
                      if trial in trial_ids_for_raster_plot:
                         if n_trials==1:
                            ax[trial].scatter(spikes,np.zeros_like(spikes)+target_cell_array[pop][cell],marker='|',s=2,c=color)
                         else:
                            ax[trial].scatter(spikes,np.zeros_like(spikes)+target_cell_array[trial][pop][cell],marker='|',s=2,c=color)

           distances.append(pyspike.spike_profile_multi(spike_trains))

    # average synchrony index across trials
    average_distance = distances[0]
    for distance in distances[1:]:
        average_distance.add(distance)
    average_distance.mul_scalar(1./exp_specify[2])


    mark_step=sim_duration/50
    marks=[]
    for mark in range(0,mark_step+1):
        Mark=50*mark
        marks.append(Mark)



    xmin = 20
    xmax = 400
    x, y = average_distance.get_plottable_data()
    ximin = np.searchsorted(x, xmin)
    ximax = np.searchsorted(x, xmax)
    lines.append(ax[1].plot(x[ximin:ximax+1], 1-y[ximin:ximax+1], lw=2, c=color)[0])

    ax[1].plot(x[:ximin+1], 1-y[:ximin+1], lw=2, c=color, alpha=0.4)
    ax[1].plot(x[ximax:], 1-y[ximax:], lw=2, c=color, alpha=0.4)

    ax[0].locator_params(tight=True, nbins=mark_step+1)
    ax[1].locator_params(axis='y', tight=True, nbins=mark_step+1)
    ax[1].set_xticks(marks)
    ax[0].set_ylabel('Cell number',size=5)
    
    for subplot in range(0,2):
        for tick in ax[subplot].yaxis.get_major_ticks():
            tick.label.set_fontsize(4) 
     
    #for subplot in range(0,2):
        #for tick in ax[subplot].yaxis.get_major_ticks():
            #tick.label.set_fontsize(8) 
       
                
    ax[1].set_xlabel('Time (ms)')
    ax[1].set_ylabel('Synchrony index',size=5)
    plt.tight_layout()
    plt.savefig('simulations/desynchronisation_random_graph_test2.pdf')
    

if __name__=="__main__":
   #Test1
   #Synchronization_analysis(450,["all"],1,["V2012multi1_2c_1input",["seed specifier",True],1],[0])
   #Test2
   Synchronization_analysis(450,["subtype specific","random fraction","randomly set target ids only once",[0.5,0.5]],2,["V2010multi1_2c_1input",["seed specifier",True],1],[0])
   #the former in general would have the following format : ["subtype specific","random fraction","randomize only once" or "randomize on every trial","[fraction of Golgi_pop0 to target, fraction of Golgi_pop1 to target, ...,fraction of Golgi_pop n to target]]
   #Test3
   #Synchronization_analysis(450,["subtype specific","explicit list",[[0,1]]],1,["V2012multi1_2c_1input",["seed specifier",True],1])
   #Synchronization_analysis(450,["3D region specific",[[40,80],[40,80],[40,80]]],1,["V2012multi1_2c_1input",["seed specifier",True],1])
   #Synchronization_analysis(450,["3D region specific",[[40,80],[40,80],[40,80]]],1,["V2012multi1_2c_1input",["seed specifier",True],1])
   
   #if present, "3D region specific" string has to be at 0 index position in a parameter array; more flexible search through input arrays  might be coded in the future 
   #Synchronization_analysis(450,["3D region specific",[[40,80],[40,80],[40,80]],/
   #"subtype specific","random fraction","randomly set target ids only once",[0.5,0.5]],1,["V2012multi1_2c_1input",["seed specifier",True],1])
   #if seeded, 3D region specificity and explicit list can be combined because ids within a given region do not change across simulation trials
   #Synchronization_analysis(450,["3D region specific",[[40,80],[40,80],[40,80]],/
   #"subtype specific","random fraction",[0.5,0.5]],1,["V2012multi1_2c_1input",["seed specifier",False],1])
   print("Testing Synchronization_analysis.py")
   


        
                    

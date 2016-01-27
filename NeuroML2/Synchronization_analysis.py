
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

def Synchronization_analysis(sim_duration,specify_targets,no_of_groups,exp_specify):

    #get target ids

    target_cell_array=methods.get_cell_ids_for_sync_analysis(specify_targets,no_of_groups,exp_specify)

  
    n_trial=exp_specify[2]
    fig, ax = plt.subplots(figsize=(4,2),ncols=1,nrows=2, sharex=True)
    lines = []
    labels = []

    distances = []
    color = sns.color_palette()[0]

    if string.lower(specify_targets[0])=="all":
       for trial in range(0,exp_specify[2]):
           sim_dir = 'simulations/' + exp_specify[0]+'/sim%d'%trial+'/txt'
           spike_trains = []
           for pop in range(0,len(target_cell_array)):
               for cell in range(0,len(target_cell_array[pop])):
                   #create target txt file containing spike times
                   methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,cell),exp_specify[0],trial)
                   spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop, cell))
                   spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                   spike_trains.append(spike_train)
               if trial==0:
                  ax[0].scatter(spikes,
                          np.zeros_like(spikes)+cell,
                          marker='|',
                          s=2,
                          c=color)
           distances.append(pyspike.spike_profile_multi(spike_trains))

    # average synchrony index across trials
    average_distance = distances[0]
    for distance in distances[1:]:
        average_distance.add(distance)
    average_distance.mul_scalar(1./exp_specify[2])


    mark_step=sim_duration/50
    marks=[]
    for mark in range(0,mark_step+1):
        Mark=mark*mark_step
        marks.append(Mark)



    xmin = 0
    xmax = sim_duration
    x, y = average_distance.get_plottable_data()
    ax[1].plot(x,y)
    #ximin = np.searchsorted(x, xmin)
    #ximax = np.searchsorted(x, xmax)
    #lines.append(ax[1].plot(x[ximin:ximax+1], 1-y[ximin:ximax+1], lw=2, c=color)[0])

    #ax[1].plot(x[:ximin+1], 1-y[:ximin+1], lw=2, c=color, alpha=0.4)
    #ax[1].plot(x[ximax:], 1-y[ximax:], lw=2, c=color, alpha=0.4)

    #ax[0].locator_params(tight=True, nbins=mark_step+1)
    #ax[1].locator_params(axis='y', tight=True, nbins=mark_step+1)
    #ax[1].set_xticks(marks,('0','50','100','150','200','250','300','350','400','450'))
    #ax[0].set_ylabel('Cell number')
    #ax[1].set_xlabel('Time (ms)')
    #ax[1].set_ylabel('Synchrony index',size=0.02)
    #plt.tight_layout()
    #fig.savefig('simulations/desynchronisation_random_graph.pdf')
    fig.canvas.draw() 

if __name__=="__main__":
   Synchronization_analysis(450,["all"],1,["V2012multi1_2c_1input",["seed specifier",False],1])
   print("Testing Synchronization_analysis.py")
   


        
                    

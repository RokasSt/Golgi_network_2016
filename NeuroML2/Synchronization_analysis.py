
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

def Synchronization_analysis(sim_duration,specify_targets,no_of_groups,exp_specify,spike_plot_parameters):

    cell_no_array=[]
    if ex_specify[1][1]==True:
       for cell_group in range(0,no_of_cell_groups):
           cell_group_positions=np.loadtxt('simulations/%s/Golgi_pop%d.txt'%(exp_specify[0][exp_id],cell_group))
           dim_array=np.shape(cell_group_positions)
           cell_no_array.append(dim_array[0])
           
    else:
       for cell_group in range(0,no_of_cell_groups):
           cell_group_positions=np.loadtxt('simulations/%s/sim0/Golgi_pop%d.txt'%(exp_specify[0][exp_id],cell_group))
           dim_array=np.shape(cell_group_positions)
           cell_no_array.append(dim_array[0])



    n_trials=exp_specify[2]

    if spike_plot_parameters[0]=="2D raster plots":

        ncols=1
        nrows=1+no_of_groups

       fig_stack, ax_stack = plt.subplots(figsize=(4,nrows),ncols,nrows, sharex=True)

       if spike_plot_parameters[2]=="save all rasters to separate files":

          raster_fig_array=[]
          raster_ax_array=[]

          for trial in range(0,n_trials):
              ncols=1
              nrows=1+no_of_groups
              fig, ax = plt.subplots(figsize=(4,nrows),ncols,nrows, sharex=True)
              raster_fig_array.append(fig)
              raster_ax_array.append(ax)
    
    if spike_plot_parameters[0]=="3D scatter plot":

       nrows = max(1,math.ceil((1+no_of_groups)/3))
       ncols = min(3,1+no_of_groups)

       fig_stack, ax_stack = plt.subplots(figsize=(4*ncols,4*rows),ncols,nrows,sharex=False,projection='3d')

       if spike_plot_parameters[2]=="save all rasters to separate files":


           fig_3D_separate, ax_3D_separate = plt.subplots(figsize=(4*ncols,2*rows),ncols,nrows, sharex=False,projection='3d')



       

    lines = []
    labels = []

    

    for exp_id in range(0,len(exp_specify[0])):
        #get target ids
        experiment_parameters=[]
        experiment_parameters[0]=exp_specify[0][exp_id]
        experiment_parameters[1]=exp_specify[1]
        experiment_parameters[2]=exp_specify[2]
       
        target_cell_array=methods.get_cell_ids_for_sync_analysis(specify_targets,no_of_groups,experiment_parameters)


        #plot_params=["2D raster plot",[0],"save all simulations to separate files","pdf",#"jpeg"or"png",....]         

        #plot_params=["3D raster plot",[0], # the same options !!!!!

        #plot_params=["3D scatter plot", # one plot for each population include all sims; then the same options !!!!!
       
        distances = []
        
        color = sns.color_palette()
        if spike_plot_parameters[0]=="3D scatter plot":
           3D_spikes=[]
           3D_spike_times=[]
           sim_axis_array=[]
           population_wise_3D_spikes=[]
           population_wise_3D_spike_times=[]
           population_wise_sim_axis_array=[]
        
        
        for trial in range(0,n_trials):
            sim_dir = 'simulations/' + exp_specify[0][exp_id]+'/sim%d'%trial+'/txt'
            spike_trains = []
            if spike_plot_parameters[0]=="3D scatter plot":
               3D_spikes_array_per_trial=[]   
               3D_spike_times_array_per_trial=[]
               sim_axis_array_per_trial=[]
            ######   
            if (specify_targets[0]=="3D region specific") and (not("subtype specific" in specify_targets )):
               if exp_specify[1][1]==True:
                  for pop in range(0,len(target_cell_array)):
                      if spike_plot_parameters[0]=="3D scatter plot":
                         3D_spikes_per_pop=[]   
                         3D_spike_times_per_pop=[]
                         sim_axis_per_pop=[]
                      for cell in range(0,len(target_cell_array[pop])):
                          #create target txt file containing spike times
                          methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[pop][cell]),exp_specify[0],trial)
                          spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[pop][cell]))
                          spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                          spike_trains.append(spike_train)
                          if spike_plot_parameters[0]=="2D raster plot":
                             if trial in spike_plot_parameters[1]:
                                ax_stack[pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                             if spike_plot_parameters[2]=="save all rasters to separate files":
                                raster_ax_array[trial][pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                          if spike_plot_parameters[0]=="3D scatter plot":
                             if cell==0:
                                3D_spikes_per_pop=np.zeros_like(spikes)+(target_cell_array[pop][cell]+ exp_id*cell_no_array[pop])
                                3D_spike_times_per_pop=spikes
                                sim_axis_per_pop=np.zeros_like(spikes)+trial+1  # for display start numbering trials from the index of 1
                             else:
                                3D_spikes_per_pop=3D_spikes_per_pop+np.zeros_like(spikes)+(target_cell_array[pop][cell]+exp_id*cell_no_array[pop])
                                3D_spike_times_per_pop=3D_spike_times_per_pop+spikes
                                sim_axis_per_pop=sim_axis_per_pop+np.zeros_like(spikes)+trial+1
                      if spike_plot_parameters[0]=="3D scatter plot":
                         3D_spikes_array_per_trial.append(3D_spikes_per_pop)
                         3D_spike_times_array_per_trial.append(3D_spike_times_per_pop)
                         sim_axis_array_per_trial.append(sim_axis_per_pop)
                         
               else:
                  for pop in range(0,len(target_cell_array[trial])):
                      if spike_plot_parameters[0]=="3D scatter plot":
                         3D_spikes_per_pop=[]   
                         3D_spike_times_per_pop=[]
                         sim_axis_per_pop=[]
                      for cell in range(0,len(target_cell_array[trial][pop])):
                          methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[trial][pop][cell]),exp_specify[0],trial)
                          spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[trial][pop][cell]))
                          spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                          spike_trains.append(spike_train)
                          if spike_plot_parameters[0]=="2D raster plot":
                             if trial in spike_plot_parameters[1]:
                                ax_stack[pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                             if spike_plot_parameters[2]=="save all rasters to separate files":
                                raster_ax_array[trial][pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                          if spike_plot_parameters[0]=="3D scatter plot":
                             if cell==0:
                                3D_spikes_per_pop=np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+ exp_id*cell_no_array[pop])
                                3D_spike_times_per_pop=spikes
                                sim_axis_per_pop=np.zeros_like(spikes)+trial+1  # for display start numbering trials from the index of 1
                             else:
                                3D_spikes_per_pop=3D_spikes_per_pop+np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*cell_no_array[pop])
                                3D_spike_times_per_pop=3D_spike_times_per_pop+spikes
                                sim_axis_per_pop=sim_axis_per_pop+np.zeros_like(spikes)+trial+1
                      if spike_plot_parameters[0]=="3D scatter plot":
                         3D_spikes_array_per_trial.append(3D_spikes_per_pop)
                         3D_spike_times_array_per_trial.append(3D_spike_times_per_pop)
                         sim_axis_array_per_trial.append(sim_axis_per_pop)
            ######   
            if string.lower(specify_targets[0])=="all":
               for pop in range(0,len(target_cell_array)):
                   if spike_plot_parameters[0]=="3D scatter plot":
                      3D_spikes_per_pop=[]   
                      3D_spike_times_per_pop=[]
                      sim_axis_per_pop=[]
                   for cell in range(0,len(target_cell_array[pop])):
                       #create target txt file containing spike times
                       methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,cell),exp_specify[0][exp_id],trial)
                       spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop, cell))
                       spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                       spike_trains.append(spike_train)
                       if spike_plot_parameters[0]=="2D raster plot":
                          if trial in spike_plot_parameters[1]:
                             ax_stack[pop].scatter(spikes,np.zeros_like(spikes)+(cell+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                          if spike_plot_parameters[2]=="save all rasters to separate files":
                             raster_ax_array[trial][pop].scatter(spikes,np.zeros_like(spikes)+(cell+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                       if spike_plot_parameters[0]=="3D scatter plot":
                           if cell==0:
                              3D_spikes_per_pop=np.zeros_like(spikes)+(cell+exp_id*cell_no_array[pop])
                              3D_spike_times_per_pop=spikes
                              sim_axis_per_pop=np.zeros_like(spikes)+trial+1  # for display start numbering trials from the index of 1
                           else:
                               3D_spikes_per_pop=3D_spikes_per_pop+np.zeros_like(spikes)+(cell+exp_id*cell_no_array[pop])
                               3D_spike_times_per_pop=3D_spike_times_per_pop+spikes
                               sim_axis_per_pop=sim_axis_per_pop+np.zeros_like(spikes)+trial+1
                               
                   if spike_plot_parameters[0]=="3D scatter plot":
                      3D_spikes_array_per_trial.append(3D_spikes_per_pop)
                      3D_spike_times_array_per_trial.append(3D_spike_times_per_pop)
                      sim_axis_array_per_trial.append(sim_axis_per_pop)
            ########
            if (specify_targets[0]=="3D region specific") and ("subtype specific" in specify_targets):
               if exp_specify[1][1]==True:
                  if ("randomly set target ids only once" in specify_targets ) or ("explicit list" in specify_targets):
                     for pop in range(0,len(target_cell_array)):
                         for cell in range(0,len(target_cell_array[pop])):
                             #create target txt file containing spike times
                             methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[pop][cell]),exp_specify[0],trial)
                             spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[pop][cell]))
                             spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                             spike_trains.append(spike_train)
                             if spike_plot_parameters[0]=="2D raster plot":
                                if trial in spike_plot_parameters[1]:
                                   ax_stack[pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                                if spike_plot_parameters[2]=="save all rasters to separate files":
                                   raster_ax_array[trial][pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                             if spike_plot_parameters[0]=="3D scatter plot":
                                if cell==0:
                                   3D_spikes_per_pop=np.zeros_like(spikes)+(target_cell_array[pop][cell]+ exp_id*cell_no_array[pop])
                                   3D_spike_times_per_pop=spikes
                                   sim_axis_per_pop=np.zeros_like(spikes)+trial+1  # for display start numbering trials from the index of 1
                                else:
                                   3D_spikes_per_pop=3D_spikes_per_pop+np.zeros_like(spikes)+(target_cell_array[pop][cell]+exp_id*cell_no_array[pop])
                                   3D_spike_times_per_pop=3D_spike_times_per_pop+spikes
                                   sim_axis_per_pop=sim_axis_per_pop+np.zeros_like(spikes)+trial+1
                         if spike_plot_parameters[0]=="3D scatter plot":
                            3D_spikes_array_per_trial.append(3D_spikes_per_pop)
                            3D_spike_times_array_per_trial.append(3D_spike_times_per_pop)
                            sim_axis_array_per_trial.append(sim_axis_per_pop)
                  else:
                     for pop in range(0,len(target_cell_array[trial])):
                         for cell in range(0,len(target_cell_array[trial][pop])):
                             methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[trial][pop][cell]),exp_specify[0],trial)
                             spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[trial][pop][cell]))
                             spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                             spike_trains.append(spike_train)
                             if spike_plot_parameters[0]=="2D raster plot":
                                if trial in spike_plot_parameters[1]:
                                   ax_stack[pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                                if spike_plot_parameters[2]=="save all rasters to separate files":
                                raster_ax_array[trial][pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                             if spike_plot_parameters[0]=="3D scatter plot":
                                if cell==0:
                                   3D_spikes_per_pop=np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+ exp_id*cell_no_array[pop])
                                   3D_spike_times_per_pop=spikes
                                   sim_axis_per_pop=np.zeros_like(spikes)+trial+1  # for display start numbering trials from the index of 1
                                else:
                                   3D_spikes_per_pop=3D_spikes_per_pop+np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*cell_no_array[pop])
                                   3D_spike_times_per_pop=3D_spike_times_per_pop+spikes
                                   sim_axis_per_pop=sim_axis_per_pop+np.zeros_like(spikes)+trial+1
                         if spike_plot_parameters[0]=="3D scatter plot":
                            3D_spikes_array_per_trial.append(3D_spikes_per_pop)
                            3D_spike_times_array_per_trial.append(3D_spike_times_per_pop)
                            sim_axis_array_per_trial.append(sim_axis_per_pop)
               else:
                  for pop in range(0,len(target_cell_array[trial])):
                      for cell in range(0,len(target_cell_array[trial][pop])):
                          methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[trial][pop][cell]),exp_specify[0],trial)
                          spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[trial][pop][cell]))
                          spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                          spike_trains.append(spike_train)
                          if spike_plot_parameters[0]=="2D raster plot":
                             if trial in spike_plot_parameters[1]:
                                ax_stack[pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                             if spike_plot_parameters[2]=="save all rasters to separate files":
                                raster_ax_array[trial][pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                          if spike_plot_parameters[0]=="3D scatter plot":
                             if cell==0:
                                3D_spikes_per_pop=np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+ exp_id*cell_no_array[pop])
                                3D_spike_times_per_pop=spikes
                                sim_axis_per_pop=np.zeros_like(spikes)+trial+1  # for display start numbering trials from the index of 1
                             else:
                                3D_spikes_per_pop=3D_spikes_per_pop+np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*cell_no_array[pop])
                                3D_spike_times_per_pop=3D_spike_times_per_pop+spikes
                                sim_axis_per_pop=sim_axis_per_pop+np.zeros_like(spikes)+trial+1
                      if spike_plot_parameters[0]=="3D scatter plot":
                         3D_spikes_array_per_trial.append(3D_spikes_per_pop)
                         3D_spike_times_array_per_trial.append(3D_spike_times_per_pop)
                         sim_axis_array_per_trial.append(sim_axis_per_pop)
            ########
            if string.lower(specify_targets[0])=="subtype specific":
               if specify_targets[0][2]=="randomly set target ids only once":
                  for pop in range(0,len(target_cell_array)):
                      for cell in range(0,len(target_cell_array[pop])):
                          #create target txt file containing spike times
                          methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[pop][cell]),exp_specify[0],trial)
                          spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[pop][cell]))
                          spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                          spike_trains.append(spike_train)
                          if spike_plot_parameters[0]=="2D raster plot":
                             if trial in spike_plot_parameters[1]:
                                ax_stack[pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                              if spike_plot_parameters[2]=="save all rasters to separate files":
                                 raster_ax_array[trial][pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                          if spike_plot_parameters[0]=="3D scatter plot":
                             if cell==0:
                                3D_spikes_per_pop=np.zeros_like(spikes)+(target_cell_array[pop][cell]+ exp_id*cell_no_array[pop])
                                3D_spike_times_per_pop=spikes
                                sim_axis_per_pop=np.zeros_like(spikes)+trial+1  # for display start numbering trials from the index of 1
                             else:
                                3D_spikes_per_pop=3D_spikes_per_pop+np.zeros_like(spikes)+(target_cell_array[pop][cell]+exp_id*cell_no_array[pop])
                                3D_spike_times_per_pop=3D_spike_times_per_pop+spikes
                                sim_axis_per_pop=sim_axis_per_pop+np.zeros_like(spikes)+trial+1
                      if spike_plot_parameters[0]=="3D scatter plot":
                         3D_spikes_array_per_trial.append(3D_spikes_per_pop)
                         3D_spike_times_array_per_trial.append(3D_spike_times_per_pop)
                         sim_axis_array_per_trial.append(sim_axis_per_pop)
                       
               else:
                  for pop in range(0,len(target_cell_array[trial])):
                      for cell in range(0,len(target_cell_array[trial][pop])):
                          #create target txt file containing spike times
                          methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[trial][pop][cell]),exp_specify[0],trial)
                          spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[trial][pop][cell]))
                          spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                          spike_trains.append(spike_train)
                          if spike_plot_parameters[0]=="2D raster plot":
                             if trial in spike_plot_parameters[1]:
                                ax_stack[pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                             if spike_plot_parameters[2]=="save all rasters to separate files":
                                raster_ax_array[trial][pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                          if spike_plot_parameters[0]=="3D scatter plot":
                             if cell==0:
                                3D_spikes_per_pop=np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+ exp_id*cell_no_array[pop])
                                3D_spike_times_per_pop=spikes
                                sim_axis_per_pop=np.zeros_like(spikes)+trial+1  # for display start numbering trials from the index of 1
                             else:
                                3D_spikes_per_pop=3D_spikes_per_pop+np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*cell_no_array[pop])
                                3D_spike_times_per_pop=3D_spike_times_per_pop+spikes
                                sim_axis_per_pop=sim_axis_per_pop+np.zeros_like(spikes)+trial+1
                      if spike_plot_parameters[0]=="3D scatter plot":
                         3D_spikes_array_per_trial.append(3D_spikes_per_pop)
                         3D_spike_times_array_per_trial.append(3D_spike_times_per_pop)
                         sim_axis_array_per_trial.append(sim_axis_per_pop)
                      
            ########           
            if spike_plot_parameters[0]=="3D scatter plot":
               3D_spikes.append(3D_spikes_array_per_trial)
               3D_spike_times.append(3D_spike_times_array_per_trial)
               sim_axis_array.append(sim_axis_array_per_trial)
                  
            distances.append(pyspike.spike_profile_multi(spike_trains))

            for pop in range(0,no_of_groups):
                population_wise_3D_spikes.append(3D_spikes[0][pop])
                population_wise_3D_spike_times.append(3D_spike_times[0][pop])
                population_wise_sim_axis_array.append(sim_axis_array[0][pop])
               
            for pop in range(0,no_of_groups):
                for trial in range(1,n_trials):
                    population_wise_3D_spikes[pop]=population_wise_3D_spikes[pop]+3D_spikes[trial][pop]
                    population_wise_3D_spike_times[pop]=population_wise_3D_spike_times[pop]+3D_spike_times[trial][pop]
                    population_wise_sim_axis_array[pop]=population_wise_sim_axis_array[pop]+sim_axis_array[trial][pop]

            for pop in range(0,no_of_groups):
                ax_stack[pop].scatter(population_wise_3D_spike_times[pop],population_wise_sim_axis_array[pop],population_wise_3D_spikes[pop],marker='|',s=2,c=color)

            if spike_plot_parameters[0]=="3D scatter plot":
               if spike_plot_parameters[2]=="save all rasters to separate files":
                  for pop in range(0,no_of_groups):
                      ax_3D_separate[pop].scatter(population_wise_3D_spike_times[pop],population_wise_sim_axis_array[pop],population_wise_3D_spikes[pop],marker='|',s=2,c=color)
            ######         
            
            
    
          
   

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

   Synchronization_analysis(450,["subtype specific","random fraction","randomly set target ids only once",[0.5,0.5]],2,[["V2010multi1_2c_1input"],["seed specifier",True],1],plot_params)
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
   


        
                    

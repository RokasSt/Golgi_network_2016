
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
import math
from mpl_toolkits.mplot3d import Axes3D


def Synchronization_analysis(sim_duration,specify_targets,no_of_groups,exp_specify,spike_plot_parameters,general_plot_parameters,testing=False):


    cell_no_array=[]
    for exp_id in range(0,len(exp_specify[0]) ):
        if exp_specify[1][1]==True:
           for cell_group in range(0,no_of_groups):
               cell_group_positions=np.loadtxt('simulations/%s/Golgi_pop%d.txt'%(exp_specify[0][exp_id],cell_group))
               dim_array=np.shape(cell_group_positions)
               cell_no_array.append(dim_array[0])
           
        else:
           for cell_group in range(0,no_of_groups):
               cell_group_positions=np.loadtxt('simulations/%s/sim0/Golgi_pop%d.txt'%(exp_specify[0][exp_id],cell_group))
               dim_array=np.shape(cell_group_positions)
               cell_no_array.append(dim_array[0])



    n_trials=exp_specify[2]

    if spike_plot_parameters[0]=="2D raster plots":

       columns=1
       rows=1+no_of_groups

       fig_stack, ax_stack = plt.subplots(figsize=(4,rows),ncols=columns,nrows=rows, sharex=True)
       ax_stack=ax_stack.ravel()
       
       if spike_plot_parameters[2]=="save all simulations to separate files":

          raster_fig_array=[]
          raster_ax_array=[]

          fig_sync, ax_sync=plt.subplots(figsize=(2,1.5),ncols=1,nrows=1)

          for trial in range(0,n_trials):
              columns=1
              rows=no_of_groups
              fig, ax = plt.subplots(figsize=(4,rows),ncols=columns,nrows=rows, sharex=True)
              if no_of_groups >1:
                 ax=ax.ravel()
              raster_fig_array.append(fig)
              raster_ax_array.append(ax)
   

    lines = []
    lines_sep=[]
    
    for exp_id in range(0,len(exp_specify[0])):
        #get target ids
        experiment_parameters=[]
        experiment_parameters.append(exp_specify[0][exp_id])
        experiment_parameters.append(exp_specify[1])
        experiment_parameters.append(exp_specify[2])
       
        target_cell_array=methods.get_cell_ids_for_sync_analysis(specify_targets,no_of_groups,experiment_parameters)

        

        #plot_params=["2D raster plot",[0],"save all simulations to separate files","pdf",#"jpeg"or"png",....]         

        #plot_params=["3D raster plot",[0], # the same options !!!!!

        #plot_params=["3D scatter plot", # one plot for each population include all sims; then the same options !!!!!
       
        distances = []
        
        color = sns.color_palette()[exp_id+1]
        
        
        for trial in range(0,n_trials):
            sim_dir = 'simulations/' + exp_specify[0][exp_id]+'/sim%d'%trial+'/txt'
            spike_trains = []
            ######   
            if (specify_targets[0]=="3D region specific") and (not("subtype specific" in specify_targets )):
               if exp_specify[1][1]==True:
                  for pop in range(0,len(target_cell_array)):
                      for cell in range(0,len(target_cell_array[pop])):
                          #create target txt file containing spike times
                          if not os.path.isfile('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[pop][cell])):
                             methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[pop][cell]),exp_specify[0][exp_id],trial)
                          spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[pop][cell]))
                          spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                          spike_trains.append(spike_train)
                          if spike_plot_parameters[0]=="2D raster plots":
                             if trial in spike_plot_parameters[1]:
                                ax_stack[pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[pop][cell]+exp_id*(cell_no_array[pop]+1)),marker='|',s=2,c=color)
                             if spike_plot_parameters[2]=="save all simulations to separate files":
                                raster_ax_array[trial][pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[pop][cell]+exp_id*(cell_no_array[pop]+1)),marker='|',s=2,c=color)
                             
                         
               else:
                  for pop in range(0,len(target_cell_array[trial])):
                      if len(target_cell_array[trial][pop]) >0 :
                         for cell in range(0,len(target_cell_array[trial][pop])):
                             if not os.path.isfile('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[trial][pop][cell])):
                                methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[trial][pop][cell]),exp_specify[0][exp_id],trial)
                             spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[trial][pop][cell]))
                             print('Printing spikes of %s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[trial][pop][cell]))
                             print spikes 
                             spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                             spike_trains.append(spike_train)
                             if spike_plot_parameters[0]=="2D raster plots":
                                if trial in spike_plot_parameters[1]:
                                   ax_stack[pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*(cell_no_array[pop]+1)),marker='|',s=2,c=color)
                                if spike_plot_parameters[2]=="save all simulations to separate files":
                                   raster_ax_array[trial][pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*(cell_no_array[pop]+1)),marker='|',s=2,c=color)
                      
                              
                          
            ######   
            if string.lower(specify_targets[0])=="all":
               for pop in range(0,len(target_cell_array)):
                   for cell in range(0,len(target_cell_array[pop])):
                       #create target txt file containing spike times
                       if not os.path.isfile('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,cell)):
                          methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,cell),exp_specify[0][exp_id],trial)
                       spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop, cell))
                       spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                       spike_trains.append(spike_train)
                       if spike_plot_parameters[0]=="2D raster plots":
                          if trial in spike_plot_parameters[1]:
                             ax_stack[pop].scatter(spikes,np.zeros_like(spikes)+(cell+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                          if spike_plot_parameters[2]=="save all simulations to separate files":
                             raster_ax_array[trial][pop].scatter(spikes,np.zeros_like(spikes)+(cell+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                       
                               
                  
            ########
            if (specify_targets[0]=="3D region specific") and ("subtype specific" in specify_targets):
               if exp_specify[1][1]==True:
                  if ("randomly set target ids only once" in specify_targets ) or ("explicit list" in specify_targets):
                     for pop in range(0,len(target_cell_array)):
                         for cell in range(0,len(target_cell_array[pop])):
                             #create target txt file containing spike times
                             if not os.path.isfile('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[pop][cell])):
                                methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[pop][cell]),exp_specify[0][exp_id],trial)
                             spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[pop][cell]))
                             spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                             spike_trains.append(spike_train)
                             if spike_plot_parameters[0]=="2D raster plots":
                                if trial in spike_plot_parameters[1]:
                                   ax_stack[pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                                if spike_plot_parameters[2]=="save all simulations to separate files":
                                   raster_ax_array[trial][pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                             
                         
                  else:
                     for pop in range(0,len(target_cell_array[trial])):
                         for cell in range(0,len(target_cell_array[trial][pop])): 
                             if not os.path.isfile('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[trial][pop][cell])):
                                methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[trial][pop][cell]),exp_specify[0][exp_id],trial)
                             spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[trial][pop][cell]))
                             spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                             spike_trains.append(spike_train)
                             if spike_plot_parameters[0]=="2D raster plots":
                                if trial in spike_plot_parameters[1]:
                                   ax_stack[pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                                if spike_plot_parameters[2]=="save all simulations to separate files":
                                   raster_ax_array[trial][pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                             
                         
               else:
                  for pop in range(0,len(target_cell_array[trial])):
                      for cell in range(0,len(target_cell_array[trial][pop])):
                          if not os.path.isfile('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[trial][pop][cell])):
                             methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[trial][pop][cell]),exp_specify[0][exp_id],trial)
                          spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[trial][pop][cell]))
                          spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                          spike_trains.append(spike_train)
                          if spike_plot_parameters[0]=="2D raster plots":
                             if trial in spike_plot_parameters[1]:
                                ax_stack[pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                             if spike_plot_parameters[2]=="save all simulations to separate files":
                                raster_ax_array[trial][pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*cell_no_array[pop]),marker='|',s=2,c=color)
                          
                      
            ########
            if string.lower(specify_targets[0])=="subtype specific":
               if specify_targets[2]=="randomly set target ids only once" or specify_targets[1]=="explicit list":
                  for pop in range(0,len(target_cell_array)):
                      if len(target_cell_array[pop]) > 0:
                         for cell in range(0,len(target_cell_array[pop])):
                             #create target txt file containing spike times
                             if not os.path.isfile('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[pop][cell])):
                                methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[pop][cell]),exp_specify[0][exp_id],trial)
                             spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[pop][cell]))
                             print('Printing spikes of %s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[pop][cell]))
                             print spikes 
                             spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                             spike_trains.append(spike_train)
                             if spike_plot_parameters[0]=="2D raster plots":
                                if trial in spike_plot_parameters[1]:
                                   ax_stack[pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[pop][cell]+exp_id*(cell_no_array[pop]+1)),marker='|',s=2,c=color)
                                if spike_plot_parameters[2]=="save all simulations to separate files":
                                   raster_ax_array[trial][pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[pop][cell]+exp_id*(cell_no_array[pop]+1)),marker='|',s=2,c=color)
                          

                      
                       
               else:
                  for pop in range(0,len(target_cell_array[trial])):
                      for cell in range(0,len(target_cell_array[trial][pop]) ):
                          #create target txt file containing spike times
                          if not os.path.isfile('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[trial][pop][cell])):
                             methods.get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cell_array[trial][pop][cell]),exp_specify[0][exp_id],trial)
                          spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cell_array[trial][pop][cell]))
                          spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                          spike_trains.append(spike_train)
                          if spike_plot_parameters[0]=="2D raster plots":
                             if trial in spike_plot_parameters[1]:
                                ax_stack[pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*(cell_no_array[pop]+1)),marker='|',s=2,c=color)
                             if spike_plot_parameters[2]=="save all simulations to separate files":
                                raster_ax_array[trial][pop].scatter(spikes,np.zeros_like(spikes)+(target_cell_array[trial][pop][cell]+exp_id*(cell_no_array[pop]+1)),marker='|',s=2,c=color)
                          

                      
                      
            ########           
            if len(spike_trains) !=0:
               distances.append(pyspike.spike_profile_multi(spike_trains))
            ######## 
        ######    
        
        ######         
            
            
        # average synchrony index across trials
        average_distance = distances[0]
        for distance in distances[1:]:
            average_distance.add(distance)
        average_distance.mul_scalar(1./exp_specify[2])

        # below blocks for saving synchrony and spike raster plots
        
        mark_steps=sim_duration/50
        marks=[]
        for mark in range(0,mark_steps+1):
            Mark=50*mark
            marks.append(Mark)

        xmin = 50
        right_shaded_region=50
        if sim_duration >=1000:
            right_shaded_region=100
        xmax = sim_duration-right_shaded_region
        x, y = average_distance.get_plottable_data()
        ximin = np.searchsorted(x, xmin)
        ximax = np.searchsorted(x, xmax)
        if spike_plot_parameters[0]=="2D raster plots":
           lines.append(ax_stack[no_of_groups].plot(x[ximin:ximax+1], 1-y[ximin:ximax+1], lw=2, c=color)[0])
           ax_stack[no_of_groups].plot(x[:ximin+1], 1-y[:ximin+1], lw=2, c=color, alpha=0.4)
           ax_stack[no_of_groups].plot(x[ximax:], 1-y[ximax:], lw=2, c=color, alpha=0.4)
           if spike_plot_parameters[2]=="save all simulations to separate files":
              lines_sep.append(ax_sync.plot(x[ximin:ximax+1], 1-y[ximin:ximax+1], lw=2, c=color)[0])
              ax_sync.plot(x[:ximin+1], 1-y[:ximin+1], lw=2, c=color, alpha=0.4)
              ax_sync.plot(x[ximax:], 1-y[ximax:], lw=2, c=color, alpha=0.4)
        
             
              
    
       
    if spike_plot_parameters[0]=="2D raster plots":    
       #create label array

       for pop in range(0,no_of_groups):
           label_array=[]
           ytick_array=[]
           for exp in range(0,len(general_plot_parameters[3])):
               label_array.append("%d"%0)
               label_array.append("%d"%(cell_no_array[pop]-1))

               if exp==0:
                  ytick_array.append(exp)
                  ytick_array.append(cell_no_array[pop]-1)
                  left_value=cell_no_array[pop]-1
               else:
                  ytick_array.append(left_value+2)
                  ytick_array.append(left_value+2+cell_no_array[pop])
                  left_value=left_value+2+cell_no_array[pop]
           print label_array
           print ytick_array
            
           ax_stack[pop].set_yticks(ytick_array)
           fig_stack.canvas.draw()
           ax_stack[pop].set_ylim(0,(cell_no_array[pop]+1)*len(general_plot_parameters[3]) )
           ax_stack[pop].set_ylabel('Cell id, population %d'%pop,size=4)
           ax_stack[pop].set_yticks([cell_no_array[pop]+(cell_no_array[pop]+2)*k for k in range(0,len(general_plot_parameters[3]))],minor=True)
           ax_stack[pop].yaxis.grid(False, which='major')
           ax_stack[pop].yaxis.grid(True, which='minor')
           
           labels = [x.get_text() for x in ax_stack[pop].get_yticklabels()]
           
           for label in range(0,len(labels)):
               labels[label] =label_array[label]

           ax_stack[pop].set_yticklabels(labels)
           if pop==0:
              ax_stack[pop].set_title('Raster plots for Golgi cell populations (trial id=%d)'%spike_plot_parameters[1][0],size=6)
       for pop in range(0,no_of_groups+1):
           for tick in ax_stack[pop].xaxis.get_major_ticks():
               tick.label.set_fontsize(general_plot_parameters[4]) 
           for tick in ax_stack[pop].yaxis.get_major_ticks():
               tick.label.set_fontsize(general_plot_parameters[5])
       ax_stack[no_of_groups].locator_params(axis='y', tight=True, nbins=10)
       ax_stack[no_of_groups].set_xlabel('Time (ms)',fontsize=6)
       ax_stack[no_of_groups].set_ylabel('Synchrony index',size=4)
       ax_stack[no_of_groups].set_xticks(marks)
       ax_stack[no_of_groups].set_title('Synchronization between %s'%general_plot_parameters[1],size=6)
       fig_stack.tight_layout()
       
       fig_stack.subplots_adjust(top=0.80)
       fig_stack.subplots_adjust(bottom=0.15)
       fig_stack.subplots_adjust(hspace=.4)
       l=fig_stack.legend(lines,general_plot_parameters[3],title=general_plot_parameters[2], loc='upper center',ncol=len(general_plot_parameters[3]),bbox_to_anchor=(0.55, 1.0))
       plt.setp(l.get_title(),fontsize=6)
       plt.setp(l.get_texts(), fontsize=6)
       fig_stack.savefig('simulations/%s.%s'%(general_plot_parameters[0],spike_plot_parameters[3]))
       
       if spike_plot_parameters[2]=="save all simulations to separate files":
          for tick in ax_sync.xaxis.get_major_ticks():
              tick.label.set_fontsize(general_plot_parameters[4]) 
          for tick in ax_sync.yaxis.get_major_ticks():
              tick.label.set_fontsize(general_plot_parameters[5])
          ax_sync.locator_params(axis='y', tight=True, nbins=10)
          ax_sync.set_xlabel('Time (ms)',fontsize=4)
          ax_sync.set_ylabel('Synchrony index',size=4)
          ax_sync.set_xticks(marks)
          ax_sync.set_title('Synchronization between %s'%general_plot_parameters[1],size=4)
          fig_sync.tight_layout()

          fig_sync.subplots_adjust(top=0.90)
          fig_sync.subplots_adjust(bottom=0.55)
          l=fig_sync.legend(lines_sep,general_plot_parameters[3],title=general_plot_parameters[2],loc='center',ncol=len(general_plot_parameters[3]),bbox_to_anchor=(0.52, 0.25),prop={'size':4})
          plt.setp(l.get_title(),fontsize=4)
          #plt.setp(l.get_texts(), fontsize=general_plot_parameters[4])
          
          
          
          fig_sync.savefig('simulations/sync_only_%s.%s'%(general_plot_parameters[0],spike_plot_parameters[3]))
          
          for trial in range(0,n_trials):
              if no_of_groups >1:
                 for pop in range(0,no_of_groups):
                     label_array=[]
                     ytick_array=[]
                     for exp in range(0,len(general_plot_parameters[3])):
                         label_array.append("%d"%0)
                         label_array.append("%d"%(cell_no_array[pop]-1))

                         if exp==0:
                            ytick_array.append(exp)
                            ytick_array.append(cell_no_array[pop]-1)
                            left_value=cell_no_array[pop]-1
                         else:
                            ytick_array.append(left_value+2)
                            ytick_array.append(left_value+2+cell_no_array[pop])
                            left_value=left_value+2+cell_no_array[pop]
           
            
                     raster_ax_array[trial][pop].set_yticks(ytick_array)
                     raster_fig_array[trial].canvas.draw()
                     raster_ax_array[trial][pop].set_ylim(0,(cell_no_array[pop]+1)*len(general_plot_parameters[3]) )
                     raster_ax_array[trial][pop].set_ylabel('Cell id, population %d'%pop,size=4)
                     raster_ax_array[trial][pop].set_yticks([cell_no_array[pop]+(cell_no_array[pop]+2)*k for k in range(0,len(general_plot_parameters[3]))],minor=True)
                     raster_ax_array[trial][pop].yaxis.grid(False, which='major')
                     raster_ax_array[trial][pop].yaxis.grid(True, which='minor')
           
                     labels = [x.get_text() for x in raster_ax_array[trial][pop].get_yticklabels()]
           
                     for label in range(0,len(labels)):
                         labels[label] =label_array[label]

                     raster_ax_array[trial][pop].set_yticklabels(labels)
                     if pop==0:
                        raster_ax_array[trial][pop].set_title('Raster plot for Golgi cell populations (trial id=%d)'%trial,size=6)
                     if pop==no_of_groups-1:
                        raster_ax_array[trial][pop].set_xlabel('Time (ms)',fontsize=6)
                 for pop in range(0,no_of_groups):
                     for tick in raster_ax_array[trial][pop].xaxis.get_major_ticks():
                         tick.label.set_fontsize(general_plot_parameters[4]) 
                     for tick in raster_ax_array[trial][pop].yaxis.get_major_ticks():
                         tick.label.set_fontsize(general_plot_parameters[5])
                  
              else:
                 label_array=[]
                 ytick_array=[]
                 for exp in range(0,len(general_plot_parameters[3])):
                     label_array.append("%d"%0)
                     label_array.append("%d"%(cell_no_array[pop]-1))

                     if exp==0:
                        ytick_array.append(exp)
                        ytick_array.append(cell_no_array[0]-1)
                        left_value=cell_no_array[0]-1
                     else:
                        ytick_array.append(left_value+2)
                        ytick_array.append(left_value+2+cell_no_array[0])
                        left_value=left_value+2+cell_no_array[0]
           
            
                 raster_ax_array[trial].set_yticks(ytick_array)
                 fig_stack.canvas.draw()
                 raster_ax_array[trial][pop].set_ylim(0,(cell_no_array[pop]+1)*len(general_plot_parameters[3]) )
                 raster_ax_array[trial][pop].set_ylabel('Cell id, population %d'%pop,size=4)
                 raster_ax_array[trial][pop].set_yticks([cell_no_array[pop]+(cell_no_array[pop]+2)*k for k in range(0,len(general_plot_parameters[3]))],minor=True)
                 raster_ax_array[trial][pop].yaxis.grid(False, which='major')
                 raster_ax_array[trial][pop].yaxis.grid(True, which='minor')
           
                 labels = [x.get_text() for x in raster_ax_array[trial][pop].get_yticklabels()]
           
                 for label in range(0,len(labels)):
                     labels[label] =label_array[label]

                 raster_ax_array[trial].set_yticklabels(labels)
                 raster_ax_array[trial].set_title('Raster plot for Golgi cell populations (trial id=%d)'%trial,size=6)
                 raster_ax_array[trial].set_xlabel('Time (ms)',fontsize=6)
                 for tick in raster_ax_array[trial].xaxis.get_major_ticks():
                     tick.label.set_fontsize(general_plot_parameters[4]) 
                 for tick in raster_ax_array[trial].yaxis.get_major_ticks():
                     tick.label.set_fontsize(general_plot_parameters[5])

              raster_fig_array[trial].subplots_adjust(top=0.90)
              raster_fig_array[trial].subplots_adjust(bottom=0.3)
              l=raster_fig_array[trial].legend(lines_sep,general_plot_parameters[3],title=general_plot_parameters[2],loc='center',ncol=len(general_plot_parameters[3]),bbox_to_anchor=(0.52, 0.1),prop={'size':4})
              plt.setp(l.get_title(),fontsize=4)

              raster_fig_array[trial].savefig('simulations/sim%d_rasters_%s.%s'%(trial,general_plot_parameters[0],spike_plot_parameters[3]))
              plt.clf()

              if testing:
                 print target_cell_array

if __name__=="__main__":
   #Test1
   #Synchronization_analysis(450,["all"],1,["V2012multi1_2c_1input",["seed specifier",True],1],[0])
   #Test2
   #forget 3D plots for spike rasters; not the best way to visualize, spike dispersion is more obvious from 2D plots
   #spike_plot_params=["3D scatter plot",[2],"save 3D scatter plots separately","pdf"]         
   
   #plot_params=["test_lists_5trials3D","Golgi pop 0 and pop1","Spatial scale",["1","20"],4,4] 
  
   spike_plot_params=["2D raster plots",[1],"save all simulations to separate files","pdf"]  
   plot_params=["test_lists_5trials","Golgi pop 0 and pop1","Spatial scale",["1","20"],3,3]   

   #Synchronization_analysis(sim_duration,specify_targets,no_of_groups,exp_specify,spike_plot_parameters,general_plot_parameters)

   
   
   Synchronization_analysis(450,["subtype specific","random fraction","randomly set target ids only once",[0,1]],2,[["test_Lists_and_sync","test_Lists2_and_sync"],["seed specifier",False],5],spike_plot_params,plot_params,True)

   #Test options other than subtype specific, random fraction
  
   #Synchronization_analysis(450,["subtype specific","explicit list",[ [0,1,2,3,4],[5,6,7,8,9] ] ],2,[["test_Lists_and_sync","test_Lists2_and_sync"],["seed specifier",False],5],spike_plot_params,plot_params)

   #Synchronization_analysis(450,["3D region specific",[[40,80],[40,80],[40,80]],[[40,80],[40,80],[40,80]] ],2,[["test_Lists_and_sync","test_Lists2_and_sync"],["seed specifier",False],5],spike_plot_params,plot_params)


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
   
   

        
                    

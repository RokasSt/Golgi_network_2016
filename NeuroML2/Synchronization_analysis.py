
import sys
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import seaborn as sns
import pyspike
from methods import *
import string
import subprocess
import os
import math
from mpl_toolkits.mplot3d import Axes3D


def Synchronization_analysis(sim_duration,specify_targets,no_of_groups,exp_specify,spike_plot_parameters,general_plot_parameters):
    
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

   

    lines = []
    lines_sep=[]
    experiment_seed=random.sample(range(0,15000),1)[0]
    for exp_id in range(0,len(exp_specify[0])):
        #get target ids
        experiment_parameters=[]
        experiment_parameters.append(exp_specify[0][exp_id])
        experiment_parameters.append(exp_specify[1])
        experiment_parameters.append(exp_specify[2])
       
        target_cell_array=get_cell_ids_for_sync_analysis(specify_targets,no_of_groups,experiment_parameters,experiment_seed)
        test_array=target_cell_array
        
        if exp_id==0:
           
           if "save sync plot to a separate file" in spike_plot_parameters:
              fig_sync, ax_sync=plt.subplots(figsize=(2,1.5),ncols=1,nrows=1)
              
           if spike_plot_parameters[0]=="2D raster plots":
              trial_indicator_target=False
              if n_trials >1:
                 target_cell_array_target_trial=target_cell_array[spike_plot_parameters[1]]
                 no_of_rasters=0
                 if target_cell_array_target_trial != []:
                    test_non_empty_target_array=True
                    trial_indicator_target=True
                    no_of_rasters=len(target_cell_array_target_trial)
                    rows=1+no_of_rasters
                    columns=1
                    fig_stack, ax_stack = plt.subplots(figsize=(4,rows+1),ncols=columns,nrows=rows, sharex=True)
                    ax_stack=ax_stack.ravel()
                 
                    
              else:
                 no_of_rasters=0
                 if target_cell_array != []:
                    trial_indicator=True
                    no_of_rasters=len(target_cell_array)
                    rows=1+no_of_rasters
                    columns=1
                    fig_stack, ax_stack = plt.subplots(figsize=(4,rows),ncols=columns,nrows=rows, sharex=True)
                    ax_stack=ax_stack.ravel()
              
              if "save all trials to separate files" in spike_plot_parameters:
                 raster_fig_array=[]
                 raster_ax_array=[]
                 pop_no_array=[]
                 trial_indicator=False
                 if n_trials >1:
                    non_empty_trial_indices=[]
                    for trial in range(0,n_trials):
                        if target_cell_array[trial] !=[]:
                           non_empty_trial_indices.append(trial)
                    test_indices=non_empty_trial_indices
                    for trial in range(0,len(non_empty_trial_indices)):
                        target_trial=target_cell_array[non_empty_trial_indices[trial]]
                        columns=1
                        rows=len(target_trial)
                        pop_no_array.append(rows)
                        plot_rows=rows+1
                        fig, ax = plt.subplots(figsize=(4,plot_rows),ncols=columns,nrows=rows, sharex=True)
                        if len(target_trial) >1 :
                           ax=ax.ravel()
                        raster_fig_array.append(fig)
                        raster_ax_array.append(ax)
                 else:
                    no_of_rasters=0
                    if target_cell_array != []:
                       trial_indicator=True
                       no_of_rasters=len(target_cell_array)
                       rows=no_of_rasters
                       pop_no_array.append(rows)
                       columns=1
                       plot_rows=rows+1
                       fig_stack_one_trial, ax_stack_one_trial= plt.subplots(figsize=(4,plot_rows),ncols=columns,nrows=rows, sharex=True)
                       if no_of_rasters  >  1:
                          ax_stack_one_trial=ax_stack.ravel()
              if "save all trials to one separate file" in spike_plot_parameters:
                 pop_no_array=[]
                 if n_trials >1:
                    non_empty_trial_indices=[]
                    for trial in range(0,n_trials):
                        if target_cell_array[trial] !=[]:
                           non_empty_trial_indices.append(trial)
                    total_no_of_rows=0
                    for trial in range(0,len(non_empty_trial_indices)):
                        target_trial=target_cell_array[non_empty_trial_indices[trial]]
                        
                        rows=len(target_trial)
                        pop_no_array.append(rows)
                        total_no_of_rows=total_no_of_rows + rows
                    
                    fig_all_trials, ax_all_trials = plt.subplots(figsize=(4,total_no_of_rows),ncols=1,nrows=total_no_of_rows, sharex=True)
                    if total_no_of_rows >1 :
                        ax_all_trials=ax_all_trials.ravel()
                    
                        
                 

                 

                    
        non_empty_non_unitary_trial_counter=0
        distances = []
        
        color = sns.color_palette()[exp_id+1]
        
        row_counter=0
        target_pop_index_array=[]
        if spike_plot_parameters[0]=="2D raster plots":
           if "save all trials to one separate file" in spike_plot_parameters:
              row_array=range(0,total_no_of_rows)
        if spike_plot_parameters[0]=="2D raster plots":
           if "save all trials to separate files" in spike_plot_parameters:
              raster_ax_row_counter=0
            
        for trial in range(0,n_trials):
            sim_dir = 'simulations/' + exp_specify[0][exp_id]+'/sim%d'%trial+'/txt'
            ######   
            if n_trials > 1:
               target_cell_array_per_trial=target_cell_array[trial]
            else:
               target_cell_array_per_trial=target_cell_array
            
            if target_cell_array_per_trial !=[]:
               spike_trains = []
               target_pop_index_array_per_trial=[]
               print(" Trial %d is not empty"%(trial))
               for target_pop in range(0,len(target_cell_array_per_trial)):
                   for pop in range(0,no_of_groups):
                       if ('pop%d'%(pop)) in target_cell_array_per_trial[target_pop]:
                          target_pop_index_array_per_trial.append(pop)
                          target_cells = [x for x in target_cell_array_per_trial[target_pop] if isinstance(x,int)]
                          print target_cells
                          for cell in range(0,len(target_cells)):
                              #create target txt file containing spike times
                              if not os.path.isfile('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cells[cell])):
                                 get_spike_times('Golgi_pop%d_cell%d'%(pop,target_cells[cell]),exp_specify[0][exp_id],trial)
                              spikes = np.loadtxt('%s/Golgi_pop%d_cell%d.txt'%(sim_dir,pop,target_cells[cell]))
                              spike_train=pyspike.SpikeTrain(spikes,[0,sim_duration])
                              spike_trains.append(spike_train)
                              print spike_trains
                              if spike_plot_parameters[0]=="2D raster plots":
                                 if spike_plot_parameters[1]==trial:
                                    ax_stack[target_pop].scatter(spikes,np.zeros_like(spikes)+target_cells[cell]+exp_id*(cell_no_array[pop]+1) ,marker='|',s=2,c=color)
                                 if "save all trials to separate files" in spike_plot_parameters:
                                    if n_trials >1:
                                       if len(target_cell_array_per_trial) > 1:
                                          raster_ax_array[raster_ax_row_counter][target_pop].scatter(spikes,np.zeros_like(spikes)+target_cells[cell]+exp_id*(cell_no_array[pop]+1) ,marker='|',s=2,c=color)
                                          
                                       else:
                                          raster_ax_array[raster_ax_row_counter].scatter(spikes,np.zeros_like(spikes)+target_cells[cell]+exp_id*(cell_no_array[pop]+1) ,marker='|',s=2,c=color)
                                          
                                    else:
                                       if len(target_cell_array_per_trial) >1:
                                          ax_stack_one_trial[target_pop].scatter(spikes,np.zeros_like(spikes)+target_cells[cell]+exp_id*(cell_no_array[pop]+1) ,marker='|',s=2,c=color)
                                       else:
                                          ax_stack_one_trial.scatter(spikes,np.zeros_like(spikes)+target_cells[cell]+exp_id*(cell_no_array[pop]+1) ,marker='|',s=2,c=color)
                                 if "save all trials to one separate file" in spike_plot_parameters:
                                    if n_trials >1:
                                       if total_no_of_rows >1 :
                                          ax_all_trials[row_array[row_counter]].scatter(spikes,np.zeros_like(spikes)+target_cells[cell]+exp_id*(cell_no_array[pop]+1) ,marker='|',s=2,c=color)
                                          
                                       else:
                                          ax_all_trials.scatter(spikes,np.zeros_like(spikes)+target_cells[cell]+exp_id*(cell_no_array[pop]+1) ,marker='|',s=2,c=color)
                          if spike_plot_parameters[0]=="2D raster plots":
                             if "save all trials to one separate file" in spike_plot_parameters:
                                row_counter=row_counter+1
               if spike_plot_parameters[0]=="2D raster plots":
                  if "save all trials to separate files" in spike_plot_parameters:

                     raster_ax_row_counter+=1
                  

               

               if spike_plot_parameters[1]==trial:
                  target_trial_index=target_pop_index_array.index(target_pop_index_array_per_trial) 
               

               


               target_pop_index_array.append(target_pop_index_array_per_trial)
               ########   
               print("Length of spike_trains is %d"%len(spike_trains))
               if len(spike_trains) >1:
                  print("Trial %d contains more than one cell; Synchrony metric will be computed for this trial"%(trial))
                  non_empty_non_unitary_trial_counter+=1
                  print non_empty_non_unitary_trial_counter
                  distances.append(pyspike.spike_profile_multi(spike_trains))
               else:
                  print("Trial %d contains one cell; Synchrony metric will not be computed for this trial"%(trial))
               ######## 
               
        # average synchrony index across "non empty" trials
        average_distance = distances[0]
        for distance in distances[1:]:
            average_distance.add(distance)
        average_distance.mul_scalar(1./non_empty_non_unitary_trial_counter)

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
           if target_cell_array_target_trial != []:
              target_cell_array_target_trial_indicator=True
              lines.append(ax_stack[no_of_rasters].plot(x[ximin:ximax+1], 1-y[ximin:ximax+1], lw=2, c=color)[0])
              ax_stack[no_of_rasters].plot(x[:ximin+1], 1-y[:ximin+1], lw=2, c=color, alpha=0.4)
              ax_stack[no_of_rasters].plot(x[ximax:], 1-y[ximax:], lw=2, c=color, alpha=0.4)
        if "save sync plot to a separate file" in spike_plot_parameters:
           lines_sep.append(ax_sync.plot(x[ximin:ximax+1], 1-y[ximin:ximax+1], lw=2, c=color)[0])
           ax_sync.plot(x[:ximin+1], 1-y[:ximin+1], lw=2, c=color, alpha=0.4)
           ax_sync.plot(x[ximax:], 1-y[ximax:], lw=2, c=color, alpha=0.4)
        
             
              
    
    if "save sync plot to a separate file" in spike_plot_parameters:
       print("save sync plot to a separate file is specified")
       for tick in ax_sync.xaxis.get_major_ticks():
           tick.label.set_fontsize(general_plot_parameters[4]) 
       for tick in ax_sync.yaxis.get_major_ticks():
           tick.label.set_fontsize(general_plot_parameters[5])
       ax_sync.locator_params(axis='y', tight=True, nbins=10)
       ax_sync.set_xlabel('Time (ms)',fontsize=4)
       ax_sync.set_ylabel('Synchrony index',size=4)
       ax_sync.set_ylim(0,1)
       ax_sync.set_xticks(marks)
       ax_sync.set_title('Synchronization between %s'%general_plot_parameters[1],size=4)
       fig_sync.tight_layout()

       fig_sync.subplots_adjust(top=0.90)
       fig_sync.subplots_adjust(bottom=0.55)
       l=fig_sync.legend(lines_sep,general_plot_parameters[3],title=general_plot_parameters[2],loc='center',ncol=len(general_plot_parameters[3]),bbox_to_anchor=(0.52, 0.25),prop={'size':4})
       plt.setp(l.get_title(),fontsize=4)
          
       fig_sync.savefig('simulations/sync_only_%s.%s'%(general_plot_parameters[0],spike_plot_parameters[-1]))
       print("saved %s in simulations"%'sync_only_%s.%s'%(general_plot_parameters[0],spike_plot_parameters[-1]))
       
    if spike_plot_parameters[0]=="2D raster plots":    
       print("Intend to plot a main figure with representative 2D raster plots")
       #create label array
       if trial_indicator_target:
          print("2D raster plot procedures started")
          for pop in range(0,no_of_rasters):
              label_array=[]
              ytick_array=[]
              for exp in range(0,len(general_plot_parameters[3])):
                  label_array.append("%d"%0)
                  label_array.append("%d"%(cell_no_array[target_pop_index_array[target_trial_index][pop]]-1))

                  if exp==0:
                     ytick_array.append(exp)
                     ytick_array.append(cell_no_array[target_pop_index_array[target_trial_index][pop]]-1)
                     left_value=cell_no_array[target_pop_index_array[target_trial_index][pop]]-1
                  else:
                     ytick_array.append(left_value+2)
                     ytick_array.append(left_value+1+cell_no_array[target_pop_index_array[target_trial_index][pop]])
                     left_value=left_value+2+cell_no_array[target_pop_index_array[target_trial_index][pop]]

              print label_array
              print ytick_array
            
              ax_stack[pop].set_yticks(ytick_array)
              fig_stack.canvas.draw()
              ax_stack[pop].set_ylim(0,(cell_no_array[target_pop_index_array[target_trial_index][pop]]+1)*len(general_plot_parameters[3]) )
              ax_stack[pop].set_ylabel('Cell ids, population %d'%pop,size=4)
              ax_stack[pop].set_yticks([cell_no_array[target_pop_index_array[target_trial_index][pop]]+(cell_no_array[target_pop_index_array[target_trial_index][pop]]+2)*k for k in range(0,len(general_plot_parameters[3]))],minor=True)
              ax_stack[pop].yaxis.grid(False, which='major')
              ax_stack[pop].yaxis.grid(True, which='minor')
           
              labels = [x.get_text() for x in ax_stack[pop].get_yticklabels()]
           
              for label in range(0,len(labels)):
                   labels[label] =label_array[label]

              ax_stack[pop].set_yticklabels(labels)
              if pop==0:
                 ax_stack[pop].set_title('Raster plots for target Golgi cell populations (trial id=%d)'%spike_plot_parameters[1],size=6)
              for pop in range(0,no_of_rasters+1):
                  for tick in ax_stack[pop].xaxis.get_major_ticks():
                      tick.label.set_fontsize(general_plot_parameters[4]) 
                  for tick in ax_stack[pop].yaxis.get_major_ticks():
                      tick.label.set_fontsize(general_plot_parameters[5])
              ax_stack[no_of_rasters].locator_params(axis='y', tight=True, nbins=10)
              ax_stack[no_of_rasters].set_xlabel('Time (ms)',fontsize=6)
              ax_stack[no_of_rasters].set_ylabel('Synchrony index',size=4)
              ax_stack[no_of_rasters].set_ylim(0,1)
              ax_stack[no_of_rasters].set_xticks(marks)
              ax_stack[no_of_rasters].set_title('Synchronization between %s'%general_plot_parameters[1],size=6)
              fig_stack.tight_layout()
       
              fig_stack.subplots_adjust(top=0.80)
              fig_stack.subplots_adjust(bottom=0.15)
              fig_stack.subplots_adjust(hspace=.4)
              l=fig_stack.legend(lines,general_plot_parameters[3],title=general_plot_parameters[2], loc='upper center',ncol=len(general_plot_parameters[3]),bbox_to_anchor=(0.55, 1.0))
              plt.setp(l.get_title(),fontsize=6)
              plt.setp(l.get_texts(), fontsize=6)
              fig_stack.savefig('simulations/%s.%s'%(general_plot_parameters[0],spike_plot_parameters[-1]))
       else:
          print("Intended to plot raster plots for trial %d, but specified region-specific selection of cells produces an empty target array.\nThus a main figure with a representative raster will not be produced.\nHowever, synchrony plot can be saved in a separate file.\nAlternatively, plot a non-empty trial"%(spike_plot_parameters[1]))
       if "save all trials to one separate file" in spike_plot_parameters:
          print target_pop_index_array
          if total_no_of_rows >1:
             row_counter=0
             for trial in range(0,len(non_empty_trial_indices)):
                 if len(target_pop_index_array[trial]) >1:
                    for pop in range(0,len(target_pop_index_array[trial])):
                        label_array=[]
                        ytick_array=[]
                        for exp in range(0,len(general_plot_parameters[3])):
                            label_array.append("%d"%0)
                            label_array.append("%d"%(cell_no_array[target_pop_index_array[trial][pop] ]-1))
                            if exp==0:
                               ytick_array.append(exp)
                               ytick_array.append(cell_no_array[target_pop_index_array[trial][pop]]-1)
                               left_value=cell_no_array[target_pop_index_array[trial][pop]]-1
                            else:
                               ytick_array.append(left_value+2)
                               ytick_array.append(left_value+1+cell_no_array[target_pop_index_array[trial][pop]]   )
                               left_value=left_value+2+cell_no_array[target_pop_index_array[trial][pop]]
                        ax_all_trials[row_counter].set_yticks(ytick_array)
                        #ax_all_trials[row_counter].canvas.draw()
                        ax_all_trials[row_counter].set_ylim(0,(cell_no_array[target_pop_index_array[trial][pop]]+1)*len(general_plot_parameters[3]) )
                        ax_all_trials[row_counter].set_ylabel('Cell ids for pop %d\ntrial %d'%(target_pop_index_array[trial][pop],non_empty_trial_indices[trial]),size=4)
                        ax_all_trials[row_counter].set_yticks([cell_no_array[target_pop_index_array[trial][pop]]+( cell_no_array[target_pop_index_array[trial][pop]]+2)*k for k in range(0,len(general_plot_parameters[3]))],minor=True)
                        ax_all_trials[row_counter].yaxis.grid(False, which='major')
                        ax_all_trials[row_counter].yaxis.grid(True, which='minor')
                        if row_counter==total_no_of_rows-1:
                           ax_all_trials[row_counter].set_xlabel('Time (ms)',fontsize=4)
           
                        labels = [x.get_text() for x in  ax_all_trials[row_counter].get_yticklabels()]
           
                        for label in range(0,len(labels)):
                             labels[label] =label_array[label]

                        ax_all_trials[row_counter].set_yticklabels(labels)
                         
                        for tick in ax_all_trials[row_counter].xaxis.get_major_ticks():
                            tick.label.set_fontsize(general_plot_parameters[4]) 
                        for tick in ax_all_trials[row_counter].yaxis.get_major_ticks():
                            tick.label.set_fontsize(general_plot_parameters[5])
                        row_counter+=1
                 else:
                    label_array=[]
                    ytick_array=[]
                    for exp in range(0,len(general_plot_parameters[3])):
                        label_array.append("%d"%0)
                        label_array.append("%d"%(cell_no_array[target_pop_index_array[trial][0]]-1))
                        if exp==0:
                           ytick_array.append(exp)
                           ytick_array.append(cell_no_array[target_pop_index_array[trial][0]]-1)
                           left_value=cell_no_array[target_pop_index_array[trial][0]]-1
                        else:
                           ytick_array.append(left_value+2)
                           ytick_array.append(left_value+1+cell_no_array[target_pop_index_array[trial][0]]   )
                           left_value=left_value+2+cell_no_array[target_pop_index_array[trial][0]]
                    ax_all_trials[row_counter].set_yticks(ytick_array)
                    ax_all_trials[row_counter].set_ylim(0,(cell_no_array[target_pop_index_array[trial][0]]+1)*len(general_plot_parameters[3]) )
                    ax_all_trials[row_counter].set_ylabel('Cell ids for pop %d\ntrial %d'%(target_pop_index_array[trial][0],non_empty_trial_indices[trial]),size=4)
                    ax_all_trials[row_counter].set_yticks([cell_no_array[target_pop_index_array[trial][0]]+( cell_no_array[target_pop_index_array[trial][0]]+2)*k for k in range(0,len(general_plot_parameters[3]))],minor=True)
                    ax_all_trials[row_counter].yaxis.grid(False, which='major')
                    ax_all_trials[row_counter].yaxis.grid(True, which='minor')
                    if row_counter==total_no_of_rows-1:
                       ax_all_trials[row_counter].set_xlabel('Time (ms)',fontsize=4)
           
                    labels = [x.get_text() for x in  ax_all_trials[row_counter].get_yticklabels()]
           
                    for label in range(0,len(labels)):
                        labels[label] =label_array[label]

                    ax_all_trials[row_counter].set_yticklabels(labels)
                         
                    for tick in ax_all_trials[row_counter].xaxis.get_major_ticks():
                        tick.label.set_fontsize(general_plot_parameters[4]) 
                    for tick in ax_all_trials[row_counter].yaxis.get_major_ticks():
                        tick.label.set_fontsize(general_plot_parameters[5])
                    row_counter+=1

          else:
             label_array=[]
             ytick_array=[]
             for exp in range(0,len(general_plot_parameters[3])):
                 label_array.append("%d"%0)
                 label_array.append("%d"%(cell_no_array[target_pop_index_array[0][0]]-1))
                 if exp==0:
                    ytick_array.append(exp)
                    ytick_array.append(cell_no_array[target_pop_index_array[0][pop]]-1)
                    left_value=cell_no_array[target_pop_index_array[0][0]]-1
                 else:
                    ytick_array.append(left_value+2)
                    ytick_array.append(left_value+1+cell_no_array[target_pop_index_array[0][0]]   )
                    left_value=left_value+2+cell_no_array[target_pop_index_array[0][0]]
             ax_all_trials.set_yticks(ytick_array)
             ax_all_trials.canvas.draw()
             ax_all_trials.set_ylim(0,(cell_no_array[target_pop_index_array[0][0]]+1)*len(general_plot_parameters[3]) )
             ax_all_trials.set_ylabel('Cell ids for pop %d\ntrial %d'%(target_pop_index_array[trial][pop],non_empty_trial_indices[trial]),size=4)
             ax_all_trials.set_yticks([cell_no_array[target_pop_index_array[0][0]]+( cell_no_array[target_pop_index_array[0][0]]+2)*k for k in range(0,len(general_plot_parameters[3]))],minor=True)
             ax_all_trials.yaxis.grid(False, which='major')
             ax_all_trials.yaxis.grid(True, which='minor')
             ax_all_trials.set_xlabel('Time (ms)',fontsize=4)
           
             labels = [x.get_text() for x in  ax_all_trials.get_yticklabels()]
           
             for label in range(0,len(labels)):
                 labels[label] =label_array[label]

             ax_all_trials.set_yticklabels(labels)
                         
             for tick in ax_all_trials.xaxis.get_major_ticks():
                 tick.label.set_fontsize(general_plot_parameters[4]) 
             for tick in ax_all_trials.yaxis.get_major_ticks():
                 tick.label.set_fontsize(general_plot_parameters[5])
          
          fig_all_trials.subplots_adjust(hspace=0.1)
          fig_all_trials.subplots_adjust(top=0.95)
          fig_all_trials.subplots_adjust(bottom=0.1)
          l=fig_all_trials.legend(lines,general_plot_parameters[3],title=general_plot_parameters[2],loc='center',ncol=len(general_plot_parameters[3]),bbox_to_anchor=(0.52, 0.98),prop={'size':4})
          plt.setp(l.get_title(),fontsize=4)

          fig_all_trials.savefig('simulations/all_trials_%s.%s'%(general_plot_parameters[0],spike_plot_parameters[-1]))
          plt.clf() 
             
       if "save all trials to separate files" in spike_plot_parameters:
          if n_trials >1:
             for trial in range(0,len(non_empty_trial_indices)):
                 print("started ploting non-empty trials")
                 if pop_no_array[trial] >1:
                    for pop in range(0,pop_no_array[trial]):
                        label_array=[]
                        ytick_array=[]
                        for exp in range(0,len(general_plot_parameters[3])):
                            label_array.append("%d"%0)
                            label_array.append("%d"%(cell_no_array[target_pop_index_array[trial][pop]]-1))
                            if exp==0:
                               ytick_array.append(exp)
                               ytick_array.append(cell_no_array[target_pop_index_array[trial][pop]]-1)
                               left_value=cell_no_array[target_pop_index_array[trial][pop]]-1
                            else:
                               ytick_array.append(left_value+2)
                               ytick_array.append(left_value+1+cell_no_array[target_pop_index_array[trial][pop]]   )
                               left_value=left_value+2+cell_no_array[target_pop_index_array[trial][pop]]
                        raster_ax_array[trial][pop].set_yticks(ytick_array)
                        raster_fig_array[trial].canvas.draw()
                        raster_ax_array[trial][pop].set_ylim(0,(cell_no_array[target_pop_index_array[trial][pop]]+1)*len(general_plot_parameters[3]) )
                        raster_ax_array[trial][pop].set_ylabel('Cell ids, population %d'%target_pop_index_array[trial][pop],size=4)
                        raster_ax_array[trial][pop].set_yticks([cell_no_array[target_pop_index_array[trial][pop]]+( cell_no_array[target_pop_index_array[trial][pop]]+2)*k for k in range(0,len(general_plot_parameters[3]))],minor=True)
                        raster_ax_array[trial][pop].yaxis.grid(False, which='major')
                        raster_ax_array[trial][pop].yaxis.grid(True, which='minor')
           
                        labels = [x.get_text() for x in raster_ax_array[trial][pop].get_yticklabels()]
           
                        for label in range(0,len(labels)):
                            labels[label] =label_array[label]

                        raster_ax_array[trial][pop].set_yticklabels(labels)
                        if pop==0:
                           raster_ax_array[trial][pop].set_title('Raster plot for Golgi cell populations (trial id=%d)'%non_empty_trial_indices[trial],size=6)
                        if pop==pop_no_array[trial]-1:
                           raster_ax_array[trial][pop].set_xlabel('Time (ms)',fontsize=6)
                        for tick in raster_ax_array[trial][pop].xaxis.get_major_ticks():
                            tick.label.set_fontsize(general_plot_parameters[4]) 
                        for tick in raster_ax_array[trial][pop].yaxis.get_major_ticks():
                            tick.label.set_fontsize(general_plot_parameters[5])
                 else:
                    label_array=[]
                    ytick_array=[]
                    for exp in range(0,len(general_plot_parameters[3])):
                        label_array.append("%d"%0)
                        label_array.append("%d"%(cell_no_array[target_pop_index_array[trial][0]]-1))
                        if exp==0:
                           ytick_array.append(exp)
                           ytick_array.append(cell_no_array[target_pop_index_array[trial][0]]-1)
                           left_value=cell_no_array[target_pop_index_array[trial][0]]-1
                        else:
                           ytick_array.append(left_value+2)
                           ytick_array.append(left_value+1+cell_no_array[target_pop_index_array[trial][0]]   )
                           left_value=left_value+2+cell_no_array[target_pop_index_array[trial][0]]
                        raster_ax_array[trial].set_yticks(ytick_array)
                        raster_fig_array[trial].canvas.draw()
                        raster_ax_array[trial].set_ylim(0,(cell_no_array[target_pop_index_array[trial][0]]+1)*len(general_plot_parameters[3]) )
                        raster_ax_array[trial].set_ylabel('Cell ids, population %d'% target_pop_index_array[trial][0],size=4)
                        raster_ax_array[trial].set_yticks([cell_no_array[target_pop_index_array[trial][0]]+( cell_no_array[target_pop_index_array[trial][0]]+2)*k for k in range(0,len(general_plot_parameters[3]))],minor=True)
                        raster_ax_array[trial].yaxis.grid(False, which='major')
                        raster_ax_array[trial].yaxis.grid(True, which='minor')
           
                        labels = [x.get_text() for x in raster_ax_array[trial].get_yticklabels()]
           
                        for label in range(0,len(labels)):
                            labels[label] =label_array[label]

                        raster_ax_array[trial].set_yticklabels(labels)
                        raster_ax_array[trial].set_title('Raster plot for Golgi cell populations (trial id=%d)'%non_empty_trial_indices[trial],size=6)
                        raster_ax_array[trial].set_xlabel('Time (ms)',fontsize=6)
                        for tick in raster_ax_array[trial].xaxis.get_major_ticks():
                            tick.label.set_fontsize(general_plot_parameters[4]) 
                        for tick in raster_ax_array[trial].yaxis.get_major_ticks():
                            tick.label.set_fontsize(general_plot_parameters[5])
                            
                 raster_fig_array[trial].subplots_adjust(top=0.90)
                 raster_fig_array[trial].subplots_adjust(bottom=0.3)
                 l=raster_fig_array[trial].legend(lines,general_plot_parameters[3],title=general_plot_parameters[2],loc='center',ncol=len(general_plot_parameters[3]),bbox_to_anchor=(0.52, 0.1),prop={'size':4})
                 plt.setp(l.get_title(),fontsize=4)

                 raster_fig_array[trial].savefig('simulations/sim%d_rasters_%s.%s'%(non_empty_trial_indices[trial],general_plot_parameters[0],spike_plot_parameters[-1]))
                   
          else:
             if trial_indicator:
                if pop_no_array[0] >1:
                   for pop in range(0,pop_no_array[0]):
                       label_array=[]
                       ytick_array=[]
                       for exp in range(0,len(general_plot_parameters[3])):
                           label_array.append("%d"%0)
                           label_array.append("%d"%(cell_no_array[target_pop_index_array[0][pop]]-1))
                           if exp==0:
                              ytick_array.append(exp)
                              ytick_array.append(cell_no_array[target_pop_index_array[0][pop]]-1)
                              left_value=cell_no_array[target_pop_index_array[0][pop]]-1
                           else:
                              ytick_array.append(left_value+2)
                              ytick_array.append(left_value+1+cell_no_array[target_pop_index_array[0][pop]]   )
                              left_value=left_value+2+cell_no_array[target_pop_index_array[0][pop]]
                       ax_stack_one_trial[pop].set_yticks(ytick_array)
                       fig_stack_one_trial.canvas.draw()
                       ax_stack_one_trial[pop].set_ylim(0,(cell_no_array[target_pop_index_array[0][pop]]+1)*len(general_plot_parameters[3]) )
                       ax_stack_one_trial[pop].set_ylabel('Cell ids, population %d'%target_pop_index_array[0][pop],size=4)
                       ax_stack_one_trial[pop].set_yticks([cell_no_array[target_pop_index_array[0][pop]]+( cell_no_array[target_pop_index_array[0][pop]]+2)*k for k in range(0,len(general_plot_parameters[3]))],minor=True)
                       ax_stack_one_trial[pop].yaxis.grid(False, which='major')
                       ax_stack_one_trial[pop].yaxis.grid(True, which='minor')
           
                       labels = [x.get_text() for x in ax_stack_one_trial[pop].get_yticklabels()]
           
                       for label in range(0,len(labels)):
                           labels[label] =label_array[label]

                       ax_stack_one_trial[pop].set_yticklabels(labels)
                       if pop==0:
                          ax_stack_one_trial[pop].set_title('Raster plot for Golgi cell populations (trial id=%d)'%spike_plot_parameters[1],size=6)
                       if pop==pop_no_array[0]-1:
                          ax_stack_one_trial[pop].set_xlabel('Time (ms)',fontsize=6)
                       for tick in ax_stack_one_trial[pop].xaxis.get_major_ticks():
                           tick.label.set_fontsize(general_plot_parameters[4]) 
                       for tick in ax_stack_one_trial[pop].yaxis.get_major_ticks():
                           tick.label.set_fontsize(general_plot_parameters[5])
                else:
                   label_array=[]
                   ytick_array=[]
                   for exp in range(0,len(general_plot_parameters[3])):
                       label_array.append("%d"%0)
                       label_array.append("%d"%(cell_no_array[target_pop_index_array[0][0]]-1))
                       if exp==0:
                          ytick_array.append(exp)
                          ytick_array.append(cell_no_array[target_pop_index_array[0][0]]-1)
                          left_value=cell_no_array[target_pop_index_array[0][0]]-1
                       else:
                          ytick_array.append(left_value+2)
                          ytick_array.append(left_value+1+cell_no_array[target_pop_index_array[0][0]]   )
                          left_value=left_value+2+cell_no_array[target_pop_index_array[0][0]]
                   ax_stack_one_trial.set_yticks(ytick_array)
                   fig_stack_one_trial.canvas.draw()
                   ax_stack_one_trial.set_ylim(0,(cell_no_array[target_pop_index_array[0][0]]+1)*len(general_plot_parameters[3]) )
                   ax_stack_one_trial.set_ylabel('Cell ids, population %d'%target_pop_index_array[0][0],size=4)
                   ax_stack_one_trial.set_yticks([cell_no_array[target_pop_index_array[0][0]]+( cell_no_array[target_pop_index_array[0][0]]+2)*k for k in range(0,len(general_plot_parameters[3]))],minor=True)
                   ax_stack_one_trial.yaxis.grid(False, which='major')
                   ax_stack_one_trial.yaxis.grid(True, which='minor')
           
                   labels = [x.get_text() for x in ax_stack_one_trial.get_yticklabels()]
           
                   for label in range(0,len(labels)):
                       labels[label] =label_array[label]

                   ax_stack_one_trial.set_yticklabels(labels)
                   ax_stack_one_trial.set_title('Raster plot for Golgi cell populations (trial id=%d)'%spike_plot_parameters[1],size=6)
                   ax_stack_one_trial.set_xlabel('Time (ms)',fontsize=6)
                   for tick in ax_stack_one_trial.xaxis.get_major_ticks():
                       tick.label.set_fontsize(general_plot_parameters[4]) 
                   for tick in ax_stack_one_trial.yaxis.get_major_ticks():
                       tick.label.set_fontsize(general_plot_parameters[5])
                fig_stack_one_trial.subplots_adjust(top=0.90)
                fig_stack_one_trial.subplots_adjust(bottom=0.3)
                l=fig_stack_one_trial.legend(lines,general_plot_parameters[3],title=general_plot_parameters[2],loc='center',ncol=len(general_plot_parameters[3]),bbox_to_anchor=(0.52, 0.1),prop={'size':4})
                plt.setp(l.get_title(),fontsize=4)

                fig_stack_one_trial.savefig('simulations/sim%d_rasters_%s.%s'%(spike_plot_parameters[1],general_plot_parameters[0],spike_plot_parameters[-1]))
                plt.clf() 
    
    #print non_empty_trial_indices
    #print target_pop_index_array
    #print("Finished running Synchronization_analysis.py")
if __name__=="__main__":
   
          
   print("Testing Synchronization_analysis.py")
   
   # 3 is the id of the representative trial that is ploted on the same figure as synchrony plot; any trial can be passed in this way starting (id=0,id=1, ....)
   
   #spike_plot_params=["2D raster plots",3,"save all trials to separate files","save sync plot to a separate file","pdf"]  

   spike_plot_params=["2D raster plots",1,"save all trials to one separate file","save sync plot to a separate file","pdf"]  



   plot_params=["2012based_test","Golgi pop 0 and pop1","Spatial scale",["1","20"],3,3]   

   # template: Synchronization_analysis(sim_duration,specify_targets,no_of_groups,exp_specify,spike_plot_parameters,general_plot_parameters)

   
   
   #Synchronization_analysis(450,["subtype specific","random fraction","randomly set target ids only once",[1,1]],2,[["test_Lists_and_sync","test_Lists2_and_sync"],["seed specifier",False],5],spike_plot_params,plot_params)

   #Test options other than subtype specific, random fraction
  
   #Synchronization_analysis(450,["subtype specific","explicit list",[ [],[5,6,7,8,9] ] ],2,[["test_Lists_and_sync","test_Lists2_and_sync"],["seed specifier",False],5],spike_plot_params,plot_params)
  
   

   ####
   
   # Test the configurations below based on targeting specifications:
   #Synchronization_analysis(450,["all"],2,[["test_Lists_and_sync","test_Lists2_and_sync"],["seed specifier",False],5],spike_plot_params,plot_params)
   
   
   #target_cell_array=get_cell_ids_for_sync_analysis(["3D region specific",[[0,100],[0,100],[0,100]],[[0,100],[0,100],[0,100]] ],2, ["test_Lists_and_sync",["seed specifier",False],5])

   #Synchronization_analysis(450,["3D region specific",[[0,100],[0,100],[0,100]],[[0,100],[0,100],[0,100]] ],2,[["test_Lists_and_sync","test_Lists2_and_sync"],["seed specifier",False],5],spike_plot_params,plot_params)

   ##### the below command will plot correctly rasters only if a given pair of target trials from different experiments contain the same target populations; this might be extended in the future to account for differences in cell no or density if experiments are testing these parameters.
   #Synchronization_analysis(450,["3D region specific",[[0,50],[0,50],[0,50]],[[80,100],[80,100],[80,100]] ],2,[["test_Lists_and_sync","test_Lists2_and_sync"],["seed specifier",False],5],spike_plot_params,plot_params)
   
   


   #target_cell_array=get_cell_ids_for_sync_analysis(["3D region specific",[[0,50],[0,50],[0,50]],"subtype specific","random fraction",[ 0,1 ] ],2, ["test_Lists_and_sync",["seed specifier",False],5])

   #Synchronization_analysis(450,["3D region specific",[[0,50],[0,50],[0,50]],"subtype specific","random fraction",[ 0,1 ] ],2,[["test_Lists_and_sync","test_Lists2_and_sync"],["seed specifier",False],5],spike_plot_params,plot_params)


   #Synchronization_analysis(450,["3D region specific",[[0,100],[0,100],[0,100]],"subtype specific","random fraction",[ 1,1 ] ],2,[["test_iteration_1","test_iteration_2"],["seed specifier",False],5],spike_plot_params,plot_params)

   Synchronization_analysis(450,["3D region specific",[[0,100],[0,100],[0,100]],"subtype specific","random fraction",[ 1,1 ] ],2,[["2012based_test_1","2012based_test_2"],["seed specifier",False],2],spike_plot_params,plot_params)
 
 
   #Synchronization_analysis(450,["3D region specific",[[0,50],[0,50],[0,50]],"subtype specific","random fraction","randomly set target ids only once",[ 0,1 ] ],2,[["test_Lists_and_sync","test_Lists2_and_sync"],["seed specifier",True],5],spike_plot_params,plot_params)


  #target_cell_array=get_cell_ids_for_sync_analysis(["subtype specific","explicit list",[ [],[5,6,7,8,9] ] ],2, ["test_Lists_and_sync",["seed specifier",False],5])

  #target_cell_array=get_cell_ids_for_sync_analysis(["subtype specific","random fraction","randomly set target ids only once",[ 1,1 ] ],2, ["test_Lists_and_sync",["seed specifier",False],5])

  #target_cell_array=get_cell_ids_for_sync_analysis(["subtype specific","random fraction","randomize each trial individually",[ 0,1 ] ],2, ["test_Lists_and_sync",["seed specifier",False],5])





  
   
   
   

        
                    

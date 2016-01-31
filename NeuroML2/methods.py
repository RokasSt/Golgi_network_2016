
import neuroml
from pyneuroml import pynml
from pyneuroml.lems.LEMSSimulation import LEMSSimulation
import math
import neuroml.writers as writers
from neuroml.utils import validate_neuroml2
import random
import numpy as np
import string
import os.path
from pyelectro import analysis
from pyelectro import io
import numpy as np

#### the distance-dependent functions based on experimental results of Vervaeke et al. (2010); from https://github.com/epiasini/GJGolgi_ReducedMorph/blob/master/neuroConstruct/scripts/utils.py
def distance(p, q):
    return math.sqrt(sum([(a - b)**2 for a,b in zip(p,q)]))

def connection_probability_vervaeke_2010(r):
    return - 17.45 + 18.36 / (math.exp((r-267.)/39.) + 1)

def coupling_coefficient_vervaeke_2010(r):
    return - 2.3 + 29.7 * math.exp(-r/70.4)

def synaptic_weight_vervaeke_2010(r):
    cc = coupling_coefficient_vervaeke_2010(r)
    return 1000. * (0.576 * math.exp(cc / 12.4) + 0.000590 * math.exp(cc / 2.79) - 0.564)

###################

def get_spike_times(dat_file_name,exp_id,sim_id):

    delimiter = '\t'
    if os.path.isfile('simulations/%s/sim'%exp_id+'%d/'%sim_id+dat_file_name+ '.dat'):
       times, data = analysis.load_csv_data('simulations/%s/sim'%exp_id +'%d/'%sim_id+dat_file_name+'.dat', delimiter=delimiter)
       print("Loaded data with %i times & %i datapoints from %s"%(len(times),len(data),dat_file_name+'.dat'))

   
    results = analysis.max_min(data, times)

    Spike_time_array=np.asarray(results['maxima_times'])

    Spike_time_aray=np.transpose(Spike_time_array)
  
    print results['maxima_times']

    newpath = r'simulations/%s/sim%d/txt'%(exp_id,sim_id)
    if not os.path.exists(newpath):
               os.makedirs(newpath)

    np.savetxt('simulations/%s/sim%d/txt/%s.txt'%(exp_id,sim_id,dat_file_name),Spike_time_array,fmt='%f',newline=" ")
        
    return results['maxima_times']


def save_soma_positions(population_params,save_to_path):
    population_type=population_params[0]
    cell_array=population_params[1]
    Golgi_pop_index_array=population_params[2]
    soma_position_array=population_params[3]
    for cell_group in range(0,cell_array[0]):
        soma_positions=soma_position_array[cell_group]
        np.savetxt('%s/%s.txt'%(save_to_path,Golgi_pop_index_array[cell_group]),soma_positions,fmt='%f')


def get_cell_ids_for_sync_analysis(target_specifications,no_of_cell_groups,experiment_specifiers):
    target_cells=[]
    #########
    if target_specifications[0]=="all":
       if experiment_specifiers[1][1]==True:
          for cell_group in range(0,no_of_cell_groups):
              cell_group_positions=np.loadtxt('simulations/%s/Golgi_pop%d.txt'%(experiment_specifiers[0],cell_group))
              dim_array=np.shape(cell_group_positions)
              target_cell_ids=range(0,dim_array[0])
              target_cells.append(target_cell_ids)
       else: 
          for cell_group in range(0,no_of_cell_groups):
              cell_group_positions=np.loadtxt('simulations/%s/sim0/Golgi_pop%d.txt'%(experiment_specifiers[0],cell_group))
              dim_array=np.shape(cell_group_positions)
              target_cell_ids=range(0,dim_array[0])
              target_cells.append(target_cell_ids)
    #########
    if target_specifications[0]=="subtype specific":
        
       if target_specifications[1]=="explicit list":
          for cell_group in range(0,no_of_cell_groups):
              target_cells.append(target_specifications[2][cell_group])
              
       if target_specifications[1]=="random fraction":
          if target_specifications[2]=="randomly set target ids only once":
             if experiment_specifiers[1][1]==True:
                for cell_group in range(0,no_of_cell_groups):
                    cell_group_positions=np.loadtxt('simulations/%s/Golgi_pop%d.txt'%(experiment_specifiers[0],cell_group))
                    dim_array=np.shape(cell_group_positions)
                    target_cell_ids=range(0,dim_array[0])
                    random_targets_per_cell_group=random.sample(target_cell_ids,int(round(target_specifications[3][cell_group]*dim_array[0])))
                    target_cells.append(random_targets_per_cell_group)
             else:
                for cell_group in range(0,no_of_cell_groups):
                    #no need to scan through a list of simulations because this type of selection is not based on the position of cell soma;
                    #just get id listing via no of cells per population from sim0 dir
                    cell_group_positions=np.loadtxt('simulations/%s/sim0/Golgi_pop%d.txt'%(experiment_specifiers[0],cell_group))
                    dim_array=np.shape(cell_group_positions)
                    target_cell_ids=range(0,dim_array[0])
                    random_targets_per_cell_group=random.sample(target_cell_ids,int(round(target_specifications[3][cell_group]*dim_array[0])))
                    target_cells.append(random_targets_per_cell_group)
          else:
             for trial in range(0,experiment_specifiers[2]):
                 random_targets_per_trial=[]
                 if experiment_specifiers[1][1]==True:
                    for cell_group in range(0,no_of_cell_groups):
                        cell_group_positions=np.loadtxt('simulations/%s/Golgi_pop%d.txt'%(experiment_specifiers[0],cell_group))
                        dim_array=np.shape(cell_group_positions)
                        target_cell_ids=range(0,dim_array[0])
                        random_targets_per_cell_group=random.sample(target_cell_ids,int(round(target_specifications[3][cell_group]*dim_array[0])))
                        random_targets_per_trial.append(random_targets_per_cell_group)
                 else: 
                    for cell_group in range(0,no_of_cell_groups):
                        #no need to scan through a list of simulations because this type of selection is not based on the position of cell soma;
                        #just get id listing via no of cells per population from sim0 dir
                        cell_group_positions=np.loadtxt('simulations/%s/sim0/Golgi_pop%d.txt'%(experiment_specifiers[0],cell_group))
                        dim_array=np.shape(cell_group_positions)
                        target_cell_ids=range(0,dim_array[0])
                        random_targets_per_cell_group=random.sample(target_cell_ids,int(round(target_specifications[3][cell_group]*dim_array[0])))
                        random_targets_per_trial.append(random_targets_per_cell_group)
                 target_cells.append(random_targets_per_trial)
       
    
    #########
    if (target_specifcations[0]=="3D region specific") and (not("subtype specific" in target_specifcations)):
       if experiment_specifiers[1][1]==True:
          for cell_group in range(0,no_of_cell_groups):
              cell_group_positions=np.loadtxt('simulations/%s/Golgi_pop%d.txt'%(experiment_specifiers[0],cell_group))
              dim_array=np.shape(cell_group_positions)
              region_specific_targets_per_cell_group=[]
              for 3D_region in range(1,len(target_specifcations)):
                  for cell in range(0,dim_array[0]):
                      if target_specifications[3D_region][0][0] <  cell_group_positions[cell,0] and cell_group_positions[cell,0] < target_specifications[3D_region][0][1]:
                         if target_specifications[3D_region][1][0] <  cell_group_positions[cell,1] and cell_group_positions[cell,1] < target_specifications[3D_region][1][1]:
                            if target_specifications[3D_region][2][0] <  cell_group_positions[cell,2] and cell_group_positions[cell,2] < target_specifications[3D_region][2][1]:
                               region_specific_targets_per_cell_group.append(cell)
              target_cells.append(region_specific_targets_per_cell_group)
       else:
          for trial in range(0,experiment_specifiers[2]):
              region_specific_targets_per_trial=[]
              for cell_group in range(0,no_of_cell_groups):
                  cell_group_positions=np.loadtxt('simulations/%s/sim%d/Golgi_pop%d.txt'%(experiment_specifiers[0],trial,cell_group))
                  dim_array=np.shape(cell_group_positions)
                  region_specific_targets_per_cell_group=[]
                  for 3D_region in range(1,len(target_specifcations)):
                      for cell in range(0,dim_array[0]):
                          if target_specifications[3D_region][0][0] <  cell_group_positions[cell,0] and cell_group_positions[cell,0] < target_specifications[3D_region][0][1]:
                             if target_specifications[3D_region][1][0] <  cell_group_positions[cell,1] and cell_group_positions[cell,1] < target_specifications[3D_region][1][1]:
                                if target_specifications[3D_region][2][0] <  cell_group_positions[cell,2] and cell_group_positions[cell,2] < target_specifications[3D_region][2][1]:
                                   region_specific_targets_per_cell_group.append(cell)
                  region_specific_targets_per_trial.append(region_specific_targets_per_cell_group)
              target_cells.append(region_specific_targets_per_trial)
       
    if (target_specifcations[0]=="3D region specific") and ("subtype specific" in target_specifcations):
       region_specific_target_cells=[]
       subtype_specifier_position=target_specifcations.index("subtype specific")
       if experiment_specifiers[1][1]==True:
          for cell_group in range(0,no_of_cell_groups):
              cell_group_positions=np.loadtxt('simulations/%s/Golgi_pop%d.txt'%(experiment_specifiers[0],cell_group))
              dim_array=np.shape(cell_group_positions)
              region_specific_targets_per_cell_group=[]
              for 3D_region in range(1,subtype_specifier_position):
                  for cell in range(0,dim_array[0]):
                      if target_specifications[3D_region][0][0] <  cell_group_positions[cell,0] and cell_group_positions[cell,0] < target_specifications[3D_region][0][1]:
                         if target_specifications[3D_region][1][0] <  cell_group_positions[cell,1] and cell_group_positions[cell,1] < target_specifications[3D_region][1][1]:
                            if target_specifications[3D_region][2][0] <  cell_group_positions[cell,2] and cell_group_positions[cell,2] < target_specifications[3D_region][2][1]:
                               region_specific_targets_per_cell_group.append(cell)     
              region_specific_target_cells.append(region_specific_targets_per_cell_group)
          if "random fraction" in target_specifcations:
             if "randomly set target ids only once" in target_specifcations:
                for cell_group in range(0,no_of_cell_groups):
                    no_of_cells_per_region=len(region_specific_target_cells[cell_group])
                    random_targets_per_cell_group=random.sample(region_specific_target_cells[cell_group],int(round(target_specifications[subtype_specifier_position+3][cell_group]*no_of_cells_per_region)))
                    target_cells.append(random_targets_per_cell_group)
             else:
                for trial in range(0,experiment_specifiers[2]):
                    random_targets_per_trial=[]
                    for cell_group in range(0,no_of_cell_groups):
                        no_of_cells_per_region=len(region_specific_target_cells[cell_group])
                        random_targets_per_cell_group=random.sample(region_specific_target_cells[cell_group],int(round(target_specifications[subtype_specifier_position+3][cell_group]*no_of_cells_per_region)))
                        random_targets_per_trial.append(random_targets_per_cell_group)
                    target_cells.append(random_targets_per_trial)
          if "explicit list" in target_specifcations:
             for cell_group in range(0,no_of_cell_groups):
                 targets_per_cell_group=[]
                 for target_id in target_specifications[subtype_specifier_position+2][cell_group]:
                     if target_id in region_specific_target_cells[cell_group]:
                        targets_per_cell_group.append(target_id)
                target_cells.append(targets_per_cell_group)
       else:
          for trial in range(0,experiment_specifiers[2]):
              region_specific_targets_per_trial=[]
              for cell_group in range(0,no_of_cell_groups):
                  # if different seed is used everytime, randomly generated cell positions will be simulation-specific; therefore look inside sim%d
                  cell_group_positions=np.loadtxt('simulations/%s/sim%d/Golgi_pop%d.txt'%(experiment_specifiers[0],trial,cell_group))
                  dim_array=np.shape(cell_group_positions)
                  region_specific_targets_per_cell_group=[]
                  for 3D_region in range(1,subtype_specifier_position):
                      for cell in range(0,dim_array[0]):
                          if target_specifcations[3D_region][0][0] <  cell_group_positions[cell,0] and cell_group_positions[cell,0] < target_specifcations[3D_region][0][1]:
                             if target_specifcations[3D_region][1][0] <  cell_group_positions[cell,1] and cell_group_positions[cell,1] < target_specifcations[3D_region][1][1]:
                                if target_specifcations[3D_region][2][0] <  cell_group_positions[cell,2] and cell_group_positions[cell,2] < target_specifcations[3D_region][2][1]:
                                   region_specific_targets_per_cell_group.append(cell)
                  region_specific_targets_per_trial.append(region_specific_targets_per_cell_group)
              region_specific_target_cells.append(region_specific_targets_per_trial)
         if "random fraction" in target_specifcations:
            for trial in range(0,experiment_specifiers[2]):
                random_targets_per_trial=[]
                for cell_group in range(0,no_of_cell_groups):
                     no_of_cells_per_region=len(region_specific_target_cells[trial][cell_group])
                     random_targets_per_cell_group=random.sample(region_specific_target_cells[trial][cell_group],int(round(target_specifications[subtype_specifier_position+2][cell_group]*no_of_cells_per_region)))
                     random_targets_per_trial.append(random_targets_per_cell_group)
                target_cells.append(random_targets_per_trial)
              
          

    print target_cells
    

    return target_cells

def plot_voltage_traces(no_of_cell_groups,experiment_id,trial_id,plot_specifying_array,seed_specifying_array,legend=False):
    cell_no_array=[]
    if seed_specifying_array[1]==True:
       for cell_group in range(0,no_of_cell_groups):
           cell_group_positions=np.loadtxt('simulations/%s/Golgi_pop%d.txt'%(experiment_id,cell_group))
           dim_array=np.shape(cell_group_positions)
           cell_no_array.append(dim_array[0])
    else:
       for cell_group in range(0,no_of_cell_groups):
           cell_group_positions=np.loadtxt('simulations/%s/sim%d/Golgi_pop%d.txt'%(experiment_id,trial_id,cell_group))
           dim_array=np.shape(cell_group_positions)
           cell_no_array.append(dim_array[0])
    if plot_specifying_array[0]=="one population one subplot":
        
       if plot_specifying_array[1]=="explicit lists":
          which_pops_to_plot=[]
          no_of_pops_to_plot=0
          
          for cell_group in range(0,no_of_cell_groups):
              if plot_specifying_array[2][cell_group] !=[]:
                 which_pops_to_plot.append(cell_group)
                 no_of_pops_to_plot=no_of_pops_to_plot+1

          rows = max(1,math.ceil(no_of_pops_to_plot/3))
          columns = min(3,no_of_pops_to_plot)
          fig,ax = plt.subplots(rows,columns,sharex=True,
                              figsize=(4*columns,4*rows))
          ax = ax.ravel()
          
          for pop in range(0,no_of_pops_to_plot):
              ax[pop].set_xlabel('Time (ms)')
              ax[pop].set_ylabel('Membrane potential (V)')
              ax[pop].xaxis.grid(True)
              ax[pop].yaxis.grid(True)
              fig.canvas.set_window_title("Golgi_pop%d cells"%which_pops_to_plot[pop])
              for cell in plot_specifying_array[2][which_pops_to_plot[pop]]:
                  data=[]
                  cell_path='simulations/%s/sim'%experiment_id+'%d/'%trial_id+'Golgi_pop%d_cell%d'%(which_pops_to_plot[pop],cell)+'.dat'
                  for line in open(cell_path):
                      values=line.split() # for each line there is a time point and voltage value at that time point
                      for x in range(0,2):
                          data[x].append(float(values[x]))
                  time_array=data[0]
                  ax[pop].plot(data[0],data[1],label='Golgi_pop%d_cell%d'%(which_pops_to_plot[pop],cell))
                  print_comment("Adding trace for: Golgi_pop%d_cell%d, from: %s"%(which_pops_to_plot[pop],cell,cell_path), verbose)
              ax[pop].used = True
              if legend:
                 ax[pop].legend(loc='upper right', fancybox=True, shadow=True,ncol=4)
              
       # random fraction includes the case of ploting all cells of a given population       
       if plot_specifying_array[1]=="random fractions":
          which_pops_to_plot=[]
          no_of_pops_to_plot=0
          for cell_group in range(0,no_of_cell_groups):
              if plot_specifying_array[2][cell_group] !=[]:
                 which_pops_to_plot.append(cell_group)
                 no_of_pops_to_plot=no_of_pops_to_plot+1

          rows = max(1,math.ceil(no_of_pops_to_plot/3))
          columns = min(3,no_of_pops_to_plot)
          fig,ax = plt.subplots(rows,columns,sharex=True,
                              figsize=(4*columns,4*rows))
          ax = ax.ravel()

          for pop in range(0,no_of_pops_to_plot):
              ax[pop].set_xlabel('Time (ms)')
              ax[pop].set_ylabel('Membrane potential (V)')
              ax[pop].xaxis.grid(True)
              ax[pop].yaxis.grid(True)
              fig.canvas.set_window_title("Golgi_pop%d cells"%which_pops_to_plot[pop])
              
              which_cells_to_plot=random.sample(range(0,cell_no_array[which_pops_to_plot[pop]]),int(round(cell_no_array[which_pops_to_plot[pop]]*plot_specifying_array[2][which_pops_to_plot[pop]])))
              
              for cell in which_cells_to_plot:
                  data=[]
                  cell_path='simulations/%s/sim'%experiment_id+'%d/'%trial_id+'Golgi_pop%d_cell%d'%(which_pops_to_plot[pop],cell)+'.dat'
                  for line in open(cell_path):
                      values=line.split() # for each line there is a time point and voltage value at that time point
                      for x in range(0,2):
                          data[x].append(float(values[x]))
                  time_array=data[0]
                  ax[pop].plot(data[0],data[1],label='Golgi_pop%d_cell%d'%(which_pops_to_plot[pop],cell))
                  print_comment("Adding trace for: Golgi_pop%d_cell%d, from: %s"%(which_pops_to_plot[pop],cell,cell_path), verbose)
              ax[pop].used = True
              if legend:
                 ax[pop].legend(loc='upper right', fancybox=True, shadow=True,ncol=4)
                  
    #identify Golgi cell populations with pop id (0,1,2,3....) in the input array (here internal variable is plot_specifying_array)
    if plot_specifying_array[0]=="pairs":
       rows = max(1,math.ceil(len(plot_specifying_array[1])/3))
       columns = min(3,len(plot_specifying_array[1]))
       fig,ax = plt.subplots(rows,columns,sharex=True,
                              figsize=(4*columns,4*rows))
       ax = ax.ravel()
       for pair in range(0,len(plot_specifying_array[1])):
           pop1=plot_specifying_array[1][0]
           pop2=plot_specifying_array[1][1]
           ax[pair].set_xlabel('Time (ms)')
           ax[pair].set_ylabel('Membrane potential (V)')
           ax[pair].xaxis.grid(True)
           ax[pair].yaxis.grid(True)
           fig.canvas.set_window_title("Golgi_pop%d and Golgi_pop%d cells"%(pop1,pop2))
           
           if plot_specifying_array[2]=="explicit lists":
               
              for cell in plot_specifying_array[3][pair][0]:
                  data=[]
                  cell_path='simulations/%s/sim'%experiment_id+'%d/'%trial_id+'Golgi_pop%d_cell%d'%(pop1,cell)+'.dat'
                  for line in open(cell_path):
                      values=line.split() # for each line there is a time point and voltage value at that time point
                      for x in range(0,2):
                          data[x].append(float(values[x]))
                  time_array=data[0]
                  ax[pair].plot(data[0],data[1],label='Golgi_pop%d_cell%d'%(pop1,cell))
                  print_comment("Adding trace for: Golgi_pop%d_cell%d, from: %s"%(pop1,cell,cell_path), verbose)
                  
              for cell in plot_specifying_array[3][pair][1]:
                  data=[]
                  cell_path='simulations/%s/sim'%experiment_id+'%d/'%trial_id+'Golgi_pop%d_cell%d'%(pop2,cell)+'.dat'
                  for line in open(cell_path):
                      values=line.split() # for each line there is a time point and voltage value at that time point
                      for x in range(0,2):
                          data[x].append(float(values[x]))
                  time_array=data[0]
                  ax[pair].plot(data[0],data[1],label='Golgi_pop%d_cell%d'%(pop2,cell))
                  print_comment("Adding trace for: Golgi_pop%d_cell%d, from: %s"%(pop2,cell,cell_path), verbose)
                  
           if plot_specifying_array[2]=="random fractions":

              which_cells_to_plot_pop1=random.sample(range(0,cell_no_array[pop1]),\
                                                int(round(cell_no_array[pop1]*plot_specifying_array[3][pop1])))
              
              which_cells_to_plot_pop2=random.sample(range(0,cell_no_array[pop2]),\
                                                int(round(cell_no_array[pop2]*plot_specifying_array[3][pop2])))

              for cell in which_cells_to_plot_pop1:
                  data=[]
                  cell_path='simulations/%s/sim'%experiment_id+'%d/'%trial_id+'Golgi_pop%d_cell%d'%(pop1,cell)+'.dat'
                  for line in open(cell_path):
                      values=line.split() # for each line there is a time point and voltage value at that time point
                      for x in range(0,2):
                          data[x].append(float(values[x]))
                  time_array=data[0]
                  ax[pair].plot(data[0],data[1],label='Golgi_pop%d_cell%d'%(pop1,cell))
                  print_comment("Adding trace for: Golgi_pop%d_cell%d, from: %s"%(pop1,cell,cell_path), verbose)

              for cell in which_cells_to_plot_pop2:
                  data=[]
                  cell_path='simulations/%s/sim'%experiment_id+'%d/'%trial_id+'Golgi_pop%d_cell%d'%(pop2,cell)+'.dat'
                  for line in open(cell_path):
                      values=line.split() # for each line there is a time point and voltage value at that time point
                      for x in range(0,2):
                          data[x].append(float(values[x]))
                  time_array=data[0]
                  ax[pair].plot(data[0],data[1],label='Golgi_pop%d_cell%d'%(pop2,cell))
                  print_comment("Adding trace for: Golgi_pop%d_cell%d, from: %s"%(pop2,cell,cell_path), verbose)

           ax[pair].used = True
           if legend:
              ax[pair].legend(loc='upper right', fancybox=True, shadow=True,ncol=4)

def get_unique_target_points(targeting_specifications,

def get_3D_connection_length(cell_array,pre_pop,post_pop,pre_cell_ID,post_cell_ID,pre_segment_ID,post_segment_ID,pre_fraction_Along,post_fraction_Along):
    #cell_array variable has to contain cell component names
    loaded_cell_array={}
    for cell_pop in range(0,len(cell_array)):
        if cell_pop==pre_pop:
           Pre_cell_name=cell_array[pre_pop]
           pre_cell_nml_file = '%s.cell.nml'%cell_array[pre_pop]
           document_cell = neuroml.loaders.NeuroMLLoader.load(pre_cell_nml_file)
           loaded_cell_array[cell_array[pre_pop]]=document_cell.cells[0]
           pre_cell_position=cell_position_array[pre_pop][pre_cell_ID]
        if cell_pop==post_pop:
           Post_cell_name=cell_array[post_pop]
           post_cell_nml_file = '%s.cell.nml'%cell_array[post_pop]
           document_cell = neuroml.loaders.NeuroMLLoader.load(post_cell_nml_file)
           loaded_cell_array[cell_array[post_pop]]=document_cell.cells[0]
           post_cell_position=cell_position_array[post_pop][post_cell_ID]
        for pre_segment in loaded_cell_array[Pre_cell_name].morphology.segments:
            if pre_segment.id==pre_segment_ID:
               xd=pre_segment.distal.x
               yd=pre_segment.distal.y
               zd=pre_segment.distal.z
               if pre_segment_ID !=0:
                  xp=pre_segment.parent.distal.x
                  yp=pre_segment.parent.distal.y
                  zp=pre_segment.parent.distal.z
               else:
                  xp=pre_segment.proximal.x
                  yp=pre_segment.proximal.y
                  zp=pre_segment.proximal.z
               # translate the points by soma location vector
               xd=xd+pre_cell_position[0]
               yd=yd+pre_cell_position[1]
               zd=zd+pre_cell_position[2]
               xp=xp+pre_cell_position[0]
               yp=yp+pre_cell_position[1]
               zp=zp+pre_cell_position[2]
               pre_target_point=[]
               pre_target_point.append(pre_fraction_Along*(xd-xp)+xp)
               pre_target_point.append(pre_fraction_Along*(yd-yp)+yp)
               pre_target_point.append(pre_fraction_Along*(zd-zp)+zp)
        for post_segment in loaded_cell_array[Post_cell_name].morphology.segments:
            if post_segment.id==post_segment_ID:
               xd=post_segment.distal.x
               yd=post_segment.distal.y
               zd=post_segment.distal.z
               if pre_segment_ID !=0:
                  xp=post_segment.parent.distal.x
                  yp=post_segment.parent.distal.y
                  zp=post_segment.parent.distal.z
               else:
                  xp=post_segment.proximal.x
                  yp=post_segment.proximal.y
                  zp=post_segment.proximal.z
               # translate the points by soma location vector
               xd=xd+post_cell_position[0]
               yd=yd+post_cell_position[1]
               zd=zd+post_cell_position[2]
               xp=xp+post_cell_position[0]
               yp=yp+post_cell_position[1]
               zp=zp+post_cell_position[2]
               post_target_point=[]
               post_target_point.append(post_fraction_Along*(xd-xp)+xp)
               post_target_point.append(post_fraction_Along*(yd-yp)+yp)
               post_target_point.append(post_fraction_Along*(zd-zp)+zp)
        connection_length=distance(pre_target_point,post_target_point)
        
    return connection_length      
        
def extract_morphology_information(cell_array,target_array):
    loaded_cell_array={}
    cell_segment_group_array=[]
    for cell in cell_array:
        cell_nml_file = '%s.cell.nml'%cell
        document_cell = neuroml.loaders.NeuroMLLoader.load(cell_nml_file)
        loaded_cell_array[cell]=document_cell.cells[0]
        print("Loaded morphology file from: %s, with id: %s"%(cell_nml_file, loaded_cell_array[cell].id))
        segment_id_array=[]
        segment_group_array={}
        #print("Now printing segment ids")
        for segment in loaded_cell_array[cell].morphology.segments:
            segment_id_array.append(segment.id)   
            print segment.id
        print("Now printing segment group ids their segments and groups")
        for segment_group in loaded_cell_array[cell].morphology.segment_groups:
            pooled_segment_group_data={}
            segment_list=[]
            segment_group_list=[]
            print segment_group.id
            for member in segment_group.members:
                segment_list.append(member.segments)
                print member.segments
            for included_segment_group in segment_group.includes:
                segment_group_list.append(included_segment_group.segment_groups)
                   
               #for target_group_index in range(0,len(target_array)):
                   #if target_array[target_group_index+1][0]==segment_group.id:
            pooled_segment_group_data["segments"]=segment_list
            pooled_segment_group_data["groups"]=segment_group_list
            segment_group_array[segment_group.id]=pooled_segment_group_data  
               
            print segment_group_array[segment_group.id]["segments"]
               
            print segment_group_array[segment_group.id]["groups"]
        cell_segment_group=[] 
        cell_segment_group.append(cell)
        cell_segment_group.append(segment_group_array)
        cell_segment_group_array.append(cell_segment_group)
    

    if target_array[0]=="segment groups":
       target_segment_array=[]
       for cell_index in range(0, len(cell_array)):
           cell_specific_segment_array=[]
           cell_type=cell_segment_group_array[cell_index][0]
           cell_specific_segment_array.append(cell_type)
           for segment_group in cell_segment_group_array[cell_index][1].keys():
               #print("Start testing extraction of target segment ids for each cell:")
               #print segment_group
               for target_group in range(0,len(target_array[cell_index+1])):
                   if target_array[cell_index+1][target_group]==segment_group:
                      segment_target_array=[]
                      segment_target_array.append(target_array[cell_index+1][target_group])
                      if cell_segment_group_array[cell_index][1][segment_group]["segments"] !=[]:
                         for segment in cell_segment_group_array[cell_index][1][segment_group]["segments"]:
                             segment_target_array.append(segment)
                      if cell_segment_group_array[cell_index][1][segment_group]["groups"] !=[]:
                         for included_segment_group in cell_segment_group_array[cell_index][1][segment_group]["groups"]:
                             for included_segment_group_segment in cell_segment_group_array[cell_index][1][included_segment_group]["segments"]:
                                 segment_target_array.append(included_segment_group_segment)
                      cell_specific_segment_array.append(segment_target_array)
           target_segment_array.append(cell_specific_segment_array)
           print target_segment_array

    return target_segment_array        







if __name__ == "__main__":
    extract_morphology_information(["Very_Simple_Golgi_test_morph","Very_Simple_Golgi_test_morph"],["segment groups",["dendrite_group","Section_3"],["dendrite_group"]])
      





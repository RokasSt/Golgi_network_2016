
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
                        #just get id listing via no of cells per population
                        cell_group_positions=np.loadtxt('simulations/%s/sim0/Golgi_pop%d.txt'%(experiment_specifiers[0],cell_group))
                        dim_array=np.shape(cell_group_positions)
                        target_cell_ids=range(0,dim_array[0])
                        random_targets_per_cell_group=random.sample(target_cell_ids,int(round(target_specifications[3][cell_group]*dim_array[0])))
                        random_targets_per_trial.append(random_targets_per_cell_group)
                 target_cells.append(random_targets_per_trial)
       
    
    #########
    if (target_specifcations[0]=="3D region specific" and target_specifcations[1] != "subtype specific"):
       if experiment_specifiers[1][1]==True:
          for cell_group in range(0,no_of_cell_groups):
              cell_group_positions=np.loadtxt('simulations/%s/Golgi_pop%d.txt'%(experiment_specifiers[0],cell_group))
              dim_array=np.shape(cell_group_positions)
              random_targets_per_cell_group=[]
              for 3D_region in range(1,len(target_specifcations)):
                  for cell in range(0,dim_array[0]):
                      if target_specifcations[3D_region][0][0] <  cell_group_positions[cell,0] and cell_group_positions[cell,0] < target_specifcations[3D_region][0][1]:
                         if target_specifcations[3D_region][1][0] <  cell_group_positions[cell,1] and cell_group_positions[cell,1] < target_specifcations[3D_region][1][1]:
                            if target_specifcations[3D_region][2][0] <  cell_group_positions[cell,2] and cell_group_positions[cell,2] < target_specifcations[3D_region][2][1]:
                               random_targets_per_cell_group.append(cell)
              target_cells.append(random_targets_per_cell_group)
       else:
          for trial in range(0,experiment_specifiers[2]):
              random_targets_per_trial=[]
              for cell_group in range(0,no_of_cell_groups):
                  cell_group_positions=np.loadtxt('simulations/%s/sim%d/Golgi_pop%d.txt'%(experiment_specifiers[0],trial,cell_group))
                  dim_array=np.shape(cell_group_positions)
                  random_targets_per_cell_group=[]
                  for 3D_region in range(1,len(target_specifcations)):
                      for cell in range(0,dim_array[0]):
                          if target_specifcations[3D_region][0][0] <  cell_group_positions[cell,0] and cell_group_positions[cell,0] < target_specifcations[3D_region][0][1]:
                             if target_specifcations[3D_region][1][0] <  cell_group_positions[cell,1] and cell_group_positions[cell,1] < target_specifcations[3D_region][1][1]:
                                if target_specifcations[3D_region][2][0] <  cell_group_positions[cell,2] and cell_group_positions[cell,2] < target_specifcations[3D_region][2][1]:
                                   random_targets_per_cell_group.append(cell)
                  random_targets_per_trial.append(random_targets_per_cell_group)
              target_cells.append(random_targets_per_trial)
       
    #if (target_specifications[0]=="subtype specific" and target_specifcations[1]=="3D region specific") or (target_specifications[1]=="subtype specific" and target_specifcations[0]=="3D region specific"):

    print target_cells
    

    return target_cells

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
      





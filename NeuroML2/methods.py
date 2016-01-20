
import neuroml
from pyneuroml import pynml
from pyneuroml.lems.LEMSSimulation import LEMSSimulation
import math
import neuroml.writers as writers
from neuroml.utils import validate_neuroml2
import random
import numpy as np
import string

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
      





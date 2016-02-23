import neuroml
from pyneuroml import pynml
from pyneuroml.lems.LEMSSimulation import LEMSSimulation
import math
import neuroml.writers as writers
from neuroml.utils import validate_neuroml2
import random
import numpy as np
import string
import collections

from methods_v2 import *





def XF_input_models_uniform(popID,input_group_parameters,cell_position_array):

    fraction_to_target_per_pop=input_group_parameters['fractionToTarget']
                                                                        
    target_cells=random.sample(range(popSize),int(round(fraction_to_target_per_pop*popSize)   )   )
                                                                        
               
    inp_group_specifier=input_group_parameters['inputLabel']
    synapse_list=input_grooup_parameters['synapseList']
    synapse_name_array=[]
    poisson_synapse_array=[]
    for synapse_index in range(0,len(synapse_list)):
        synapse_name=synapse_list[synapse_index]['synapseType']
        synapse_name_array.append(synapse_name)                                            
        if synapse_list[synapse_index]['targetingModel']=="segments and subsegments":
           segment_target_array=extract_morphology_information([cell_array[pop_listIndex]['cellType']],\
                ["segments",synapse_list[synapse_index]['segmentList']])
                                                        
        if synapse_list[synapse_index]['targetingModel']=="segment groups and segments":
           segment_target_array =extract_morphology_information([cell_array[pop_listIndex]['cellType']],\
        ["segment groups",synapse_list[synapse_index]['segmentGroupList']])
                                                        
        if  synapse_list[synapse_index]['synapseMode']=="persistent":
            poisson_syn=neuroml.PoissonFiringSynapse(id="%s_pop%dsyn%d"%(inp_group_specifier,popID,synapse_index),\
                           average_rate="%f per_s"%synapse_list[synapse_index]['averageRate'],\
                           synapse=synapse_list[synapse_index]['synapseType'],\
                           spike_target="./%s"%synapse_list[synapse_index]['synapseType'])
                                     
        if synapse_list[synapse_index]['synapseMode']=="transient":
           poisson_syn=neuroml.TransientPoissonFiringSynapse(id="%s_%s_syn%d"%(inp_group_specifier,popID,synapse_index),\
           average_rate="%f per_s"%synapse_list[synapse_index]['averageRate'],\
           synapse=synapse_list[synapse_index]['synapseType'] ,\
           spike_target="./%s"%synapse_list[synapse_index]['synapseType'],\
           delay="%f%s"%(synapse_list[synapse_index]['delay'],synapse_list[synapse_index]['units']),\
           duration="%f%s"%(synapse_list[synapse_index]['duration'],synapse_list[synapse_index]['units'] )  )
                                  
        poisson_synapse_array(poisson_syn)

        input_list =neuroml.InputList(id="Input%s_%s_syn%d"%(inp_group_specifier,popID,synapse_index),omponent=poisson_syn.id,populations="%s"%popID)

                       
                                                                        
        count=0                               
        for target_cell in target_cells:
            if synapse_list[synapse_index]['numberModel']=="constant number of inputs per cell":
               no_of_inputs=synapse_list[synapse_index]['noInputs']
            if synapse_list[synapse_index]['numberModel']=="variable number of inputs per cell":
               if synapse_list[synapse_index]['distribution']=="binomial":
                  no_of_inputs=np.random.binomial(synapse_list[synapse_index]['maxNoInputs'],\
                  synapse_list[synapse_index]['averageNoInputs']/synapse_list[synapse_index]['maxNoInputs'])
               ### other options can be added
            if synapse_list[synapse_index]['targetingModel']=="segment groups and segments":
               target_points=get_unique_target_points(segment_target_array,"segment groups and segments",\
               [synapse_list[synapse_index]['segmentGroupList'],synapse_list[synapse_index]['segmentGroupProbabilities']],no_of_inputs)
            if synapse_list[synapse_index]['targetingModel']=="segments and subsegments":
               target_points=get_unique_target_points(segment_target_array,"segments and subsegments",\
               [synapse_list[synapse_index]['segmentList'],synapse_list[synapse_index]['segmentProbabilities'],\
               synapse_list[synapse_index]['fractionAlongANDsubsegProbabilities']],no_of_inputs)
            for target_point in range(0,len(target_points)):                     
                syn_input = neuroml.Input(id="%d"%(count),target="../%s/%i/%s"%(popID,target_cell,cell_array[pop_listIndex['cellType']),\
                destination="synapses",segment_id="%d"%target_points[target_point,0],fraction_along="%f"%target_points[target_point,1]) 
                                             
                input_list.input.append(syn_input)
                count=count+1


    return input_list, poisson_synapse_array,synapse_name_array


def XF_input_models_3D_region_specific(popID,input_group_parameters,cell_position_array):

    fraction_to_target_per_pop=input_group_parameters['fractionToTarget']
                                                                        
   
    cell_positions=cell_position_array[popID]
    dim_array=np.shape(cell_positions)
    region_specific_targets_per_cell_group=[]
    for region in range(1,len(which_cells_to_target_array[1])):
        for cell in range(0,dim_array[0]):
            if (which_cells_to_target_array[1][region][0][0] <  cell_positions[cell,0]) and (cell_positions[cell,0] < which_cells_to_target_array[1][region][0][1]):
               if (which_cells_to_target_array[1][region][1][0] <  cell_positions[cell,1]) and (cell_positions[cell,1] <which_cells_to_target_array[1][region][1][1]) :
                  if (which_cells_to_target_array[1][region][2][0] <  cell_positions[cell,2]) and (cell_positions[cell,2] < which_cells_to_target_array[1][region][2][1]):
                     region_specific_targets_per_cell_group.append(cell)
                                                                        
    target_cells=random.sample(region_specific_targets_per_cell_group,int(round(fraction_to_target_per_pop*len(region_specific_targets_per_cell_group))))
                                                                        
    inp_group_specifier=input_group_parameters['inputLabel']
    synapse_list=input_grooup_parameters['synapseList']
    synapse_name_array=[]
    poisson_synapse_array=[]
    for synapse_index in range(0,len(synapse_list)):
        synapse_name=synapse_list[synapse_index]['synapseType']
        synapse_name_array.append(synapse_name)                                            
        if synapse_list[synapse_index]['targetingModel']=="segments and subsegments":
           segment_target_array=extract_morphology_information([cell_array[pop_listIndex]['cellType']],\
                ["segments",synapse_list[synapse_index]['segmentList']])
                                                        
        if synapse_list[synapse_index]['targetingModel']=="segment groups and segments":
           segment_target_array =extract_morphology_information([cell_array[pop_listIndex]['cellType']],\
        ["segment groups",synapse_list[synapse_index]['segmentGroupList']])
                                                        
        if  synapse_list[synapse_index]['synapseMode']=="persistent":
            poisson_syn=neuroml.PoissonFiringSynapse(id="%s_pop%dsyn%d"%(inp_group_specifier,popID,synapse_index),\
                           average_rate="%f per_s"%synapse_list[synapse_index]['averageRate'],\
                           synapse=synapse_list[synapse_index]['synapseType'],\
                           spike_target="./%s"%synapse_list[synapse_index]['synapseType'])
                                     
        if synapse_list[synapse_index]['synapseMode']=="transient":
           poisson_syn=neuroml.TransientPoissonFiringSynapse(id="%s_%s_syn%d"%(inp_group_specifier,popID,synapse_index),\
           average_rate="%f per_s"%synapse_list[synapse_index]['averageRate'],\
           synapse=synapse_list[synapse_index]['synapseType'] ,\
           spike_target="./%s"%synapse_list[synapse_index]['synapseType'],\
           delay="%f%s"%(synapse_list[synapse_index]['delay'],synapse_list[synapse_index]['units']),\
           duration="%f%s"%(synapse_list[synapse_index]['duration'],synapse_list[synapse_index]['units'] )  )
                                  
        poisson_synapse_array(poisson_syn)

        input_list =neuroml.InputList(id="Input%s_%s_syn%d"%(inp_group_specifier,popID,synapse_index),omponent=poisson_syn.id,populations="%s"%popID)

                       
                                                                        
        count=0                               
        for target_cell in target_cells:
            if synapse_list[synapse_index]['numberModel']=="constant number of inputs per cell":
               no_of_inputs=synapse_list[synapse_index]['noInputs']
            if synapse_list[synapse_index]['numberModel']=="variable number of inputs per cell":
               if synapse_list[synapse_index]['distribution']=="binomial":
                  no_of_inputs=np.random.binomial(synapse_list[synapse_index]['maxNoInputs'],\
                  synapse_list[synapse_index]['averageNoInputs']/synapse_list[synapse_index]['maxNoInputs'])
               ### other options can be added
            if synapse_list[synapse_index]['targetingModel']=="segment groups and segments":
               target_points=get_unique_target_points(segment_target_array,"segment groups and segments",\
               [synapse_list[synapse_index]['segmentGroupList'],synapse_list[synapse_index]['segmentGroupProbabilities']],no_of_inputs)
            if synapse_list[synapse_index]['targetingModel']=="segments and subsegments":
               target_points=get_unique_target_points(segment_target_array,"segments and subsegments",\
               [synapse_list[synapse_index]['segmentList'],synapse_list[synapse_index]['segmentProbabilities'],\
               synapse_list[synapse_index]['fractionAlongANDsubsegProbabilities']],no_of_inputs)
            for target_point in range(0,len(target_points)):                     
                syn_input = neuroml.Input(id="%d"%(count),target="../%s/%i/%s"%(popID,target_cell,cell_array[pop_listIndex['cellType']),\
                destination="synapses",segment_id="%d"%target_points[target_point,0],fraction_along="%f"%target_points[target_point,1]) 
                                             
                input_list.input.append(syn_input)
                count=count+1


    return input_list, poisson_synapse_array,synapse_name_array              




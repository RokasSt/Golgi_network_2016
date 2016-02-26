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





def XF_input_models_uniform(popID,popSize,cellType,input_group_parameters,seed_number,parentDir=None):


    random.seed(seed_number)

    if parentDir !=None:
       cellTypeFile=parentDir+"/NeuroML2"+"/"+cellType
    else:
       cellTypeFile=cellType

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
           segment_target_array=extract_morphology_information([cellTypeFile],\
                ["segments",synapse_list[synapse_index]['segmentList']])
                                                        
        if synapse_list[synapse_index]['targetingModel']=="segment groups and segments":
           segment_target_array =extract_morphology_information([cellTypeFile],\
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

        input_list =neuroml.InputList(id="Input%s_%s_syn%d"%(inp_group_specifier,popID,synapse_index),component=poisson_syn.id,populations="%s"%popID)

                       
                                                                        
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
                syn_input = neuroml.Input(id="%d"%(count),target="../%s/%i/%s"%(popID,target_cell,cellType),\
                destination="synapses",segment_id="%d"%target_points[target_point,0],fraction_along="%f"%target_points[target_point,1]) 
                                             
                input_list.input.append(syn_input)
                count=count+1


    return input_list, poisson_synapse_array,synapse_name_array


def XF_input_models_3D_region_specific(popID,cellType,input_group_parameters,cell_positions,seed_number,parentDir=None):

    random.seed(seed_number)

    if parentDir !=None:
       cellTypeFile=parentDir+"/NeuroML2"+"/"+cellType
    else:
       cellTypeFile=cellType

    fraction_to_target_per_pop=input_group_parameters['fractionToTarget']
                                                                       
    dim_array=np.shape(cell_positions)
    region_specific_targets_per_cell_group=[]
    for region in range(1,len(input_group_parameters['regionList'])):
        for cell in range(0,dim_array[0]):
            if (input_group_parameters['regionList'][region]['xVector'][0] <  cell_positions[cell,0]) and (cell_positions[cell,0] < input_group_parameters['regionList'][region]['xVector'][1]):
               if (input_group_parameters['regionList'][region]['yVector'][0] <  cell_positions[cell,1]) and (cell_positions[cell,1] <input_group_parameters['regionList'][region]['yVector'][1]) :
                  if (input_group_parameters['regionList'][region]['zVector'][0] <  cell_positions[cell,2]) and (cell_positions[cell,2] < input_group_parameters['regionList'][region]['zVector'][1]):
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
           segment_target_array=extract_morphology_information([cellTypeFile],\
                ["segments",synapse_list[synapse_index]['segmentList']])
                                                        
        if synapse_list[synapse_index]['targetingModel']=="segment groups and segments":
           segment_target_array =extract_morphology_information([cellTypeFile],\
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

        input_list =neuroml.InputList(id="Input%s_%s_syn%d"%(inp_group_specifier,popID,synapse_index),component=poisson_syn.id,populations="%s"%popID)

                       
                                                                        
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
                syn_input = neuroml.Input(id="%d"%(count),target="../%s/%i/%s"%(popID,target_cell,cellType),\
                destination="synapses",segment_id="%d"%target_points[target_point,0],fraction_along="%f"%target_points[target_point,1]) 
                                             
                input_list.input.append(syn_input)
                count=count+1


    return input_list, poisson_synapse_array,synapse_name_array             





def variable_basal_firing_rate(popID,popSize,cellType,input_group_parameters,simulation_duration,seed_number):

   random.seed(seed_number)

   offset_units=input_group_parameters['offsetUnits']
   units=input_group_parameters['ampUnits']
   label=input_group_parameters['inputLabel']
   input_list_array=[]
   pulse_generator_array=[]
   for cell in range(0,popSize):

       if "gaussian"==input_group_parameters["amplitudeDistribution"]:
          amp=random.gauss(input_group_parameters['averageAmp'],input_group_parameters['stDevAmp'])

       if "uniform"==input_group_parameters["amplitudeDistribution"]:
          amp=random.uniform(input_group_parameters['leftAmpBound'],input_group_parameters['rightAmpBound'])

       if "constant"==input_group_parameters["amplitudeDistribution"]:
          amp=input_group_parameters['valueAmp']

       if "gaussian"==input_group_parameters["offsetDistribution"]:
          offset=random.gauss(input_group_parameters['averageOffset'],input_group_parameters['stDevOffset'])

       if "uniform"==input_group_parameters["offsetDistribution"]:
          offset=random.uniform(input_group_parameters['leftOffBound'],input_group_parameters['rightOffBound'])

       if "constant"==input_group_array[input_group]["offsetDistribution"]:
          offset=input_group_array[input_group]["valueOffset"]

       Pulse_generator_variable=neuroml.PulseGenerator(id="%s_%d"%(label,cell),delay="%f%s"%(offset,offset_units),\
       duration="%f%s"%((simulation_duration-offset),offset_units),amplitude="%f%s"%(amp,units))
       pulse_generator_array.append(Pulse_generator_variable)
       Input_list=neuroml.InputList(id="Input_%s%d"%(label,cell),component="%s_%d"%(label,cell),populations="%s"%popID)
       Inp = neuroml.Input(target="../%s/%d/%s"%(popID,cell,cellType),id="%d"%cell,destination="synapses")
       Input_list.input.append(Inp)
       input_list_array.append(Input_list)


   return input_list_array,pulse_generator_array

def testing(popID,popSize,cellType,input_group_parameters,seed_number):

     random.seed(seed_number)
     
     amp_units=input_group_parameters['ampUnits']
     time_units=input_group_parameters['timeUnits']
     randomly_select_target_cells=random.sample(range(popSize),int(round(popSize*input_group_parameters['cellFractionToTarget'])))
     pulseGenerator_array=[]
     input_list_array=[]
     for pulse_x in range(0,len(input_group_parameters['pulseParameters'])):
         Pulse_generator_x=neuroml.PulseGenerator(id="Input_%s_%d"%(popID,pulse_x),\
         delay="%f%s"%(input_group_parameters['pulseParameters'][pulse_x]['delay'],time_units),\
         duration="%f%s"%(input_group_parameters['pulseParameters'][pulse_x]['duration'],time_units),\
         amplitude="%f%s"%(input_group_parameters['pulseParameters'][pulse_x]['amplitude'],amp_units))
	 pulseGenerator_array.append(Pulse_generator_x)
                                                         
         Input_list=neuroml.InputList(id="Input_list_%s_%d"%(popID,pulse_x), component="Input_%s_%d"%(popID,pulse_x),populations="%s"%popID)
         
         for i in randomly_select_target_cells:
             Inp = neuroml.Input(target="../%s/%d/%s"%(popID,i,cellType),id="%d"%i,destination="synapses")
             Input_list.input.append(Inp)

         input_list_array.append(Input_list)


     return input_list_array,pulseGenerator_array
                      



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
from PythonUtils.Generate_Golgi_Network_v2 import generate_PoissonInputNet, generate_input_library

def generatePoissonTrainLibraries(network_parameters,simulation_parameters,library_params):
    
    if simulation_parameters['globalSeed']:
       for simulation_trial in range(0,simulation_parameters['numTrials']):
           for exp_id in range(1,len(network_parameters)+1):
               Cell_array=network_parameters['experiment%d'%(exp_id)]['popParams']
               Position_array=network_parameters['experiment%d'%(exp_id)]['distributionParams']
               Conn_array=network_parameters['experiment%d'%(exp_id)]['connParams']
               Input_array=network_parameters['experiment%d'%(exp_id)]['inputParams']
               Sim_array=simulation_parameters
               Sim_array['experimentID']=network_parameters['experiment%d'%(exp_id)]['experimentID']
               Sim_array['simID']=simulation_trial
               newpath = r'simulations/%s/sim%d'%(network_parameters['experiment%d'%(exp_id)]['experimentID'],simulation_trial)
               if not os.path.exists(newpath):
                  os.makedirs(newpath)
               sim_params,pop_params=generate_PoissonInputNet("InputNet_%s"%(network_parameters['experiment%d'%(exp_id)]['experimentID']),\
                                                    Cell_array,Position_array,Conn_array,Input_array,Sim_array,library_params)
               
               generate_input_library(sim_params,pop_params)
    else:
       if simulation_parameters['trialSeed']:
          for simulation_trial in range(0,simulation_parameters['numTrials']):
              seed_number=random.sample(range(0,15000),1)[0]
              for exp_id in range(1,len(network_parameters)+1):
                  Cell_array=network_parameters['experiment%d'%(exp_id)]['popParams']
                  Position_array=network_parameters['experiment%d'%(exp_id)]['distributionParams']
                  Conn_array=network_parameters['experiment%d'%(exp_id)]['connParams']
                  Input_array=network_parameters['experiment%d'%(exp_id)]['inputParams']
                  Sim_array=simulation_parameters
                  Sim_array['experimentID']=network_parameters['experiment%d'%(exp_id)]['experimentID']
                  Sim_array['simID']=simulation_trial
                  Sim_array['trialSeedNumber']=seed_number
                  newpath = r'simulations/%s/sim%d'%(network_parameters['experiment%d'%(exp_id)]['experimentID'],simulation_trial)
                  if not os.path.exists(newpath):
                     os.makedirs(newpath)
                  sim_params,pop_params=generate_PoissonInputNet("InputNet_%s_trial%d"%(network_parameters['experiment%d'%(exp_id)]['experimentID'],simulation_trial),\
                                            Cell_array,Position_array,Conn_array,Input_array,Sim_array,library_params)
                  
                  generate_input_library(sim_params,pop_params)


def XF_input_models_uniform_import(popID,popSize,cellType,cellNML2Type,input_group_parameters,seed_number,sim_params):

    random.seed(seed_number)
    parentDir=None
    simID=sim_params['simID']
    expID=sim_params['experimentID']
    lbID=sim_params['libraryID']
    saveCellID=sim_params['saveCellID']
    input_receiving_cells=[]
    if 'currentDir' in sim_params:
        currDir=sim_params_dict['currentDir']
    if 'parentDirRequired' in sim_params:
        parentDir=sim_params_dict['parentDir']
    if parentDir !=None:
       cellTypeFile=parentDir+"/NeuroML2"+"/"+cellType
    else:
       cellTypeFile=cellType

    fraction_to_target_per_pop=input_group_parameters['fractionToTarget']
                                                                        
    target_cells=random.sample(range(popSize),int(round(fraction_to_target_per_pop*popSize)   )   )
                                                                        
               
    synapse_list=input_group_parameters['synapseList']
    label=input_group_parameters['inputLabel']
    input_pop_array=[]
    spike_arrays=[]
    proj_arrays=[]
    if input_group_parameters['colocalizeSynapses']:
       print("will add block for localizing synapses")
       if input_group_parameters['targetingModel']=="segments and subsegments":
          segment_target_array=extract_morphology_information([cellTypeFile],{cellTypeFile:cellNML2Type},["segments",input_group_parameters['segmentList']])
                                                        
       if input_group_parameters['targetingModel']=="segment groups and segments":
          segment_target_array =extract_morphology_information([cellTypeFile],{cellTypeFile:cellNML2Type},["segment groups",input_group_parameters['segmentGroupList']])
                                                                                                                               
       count=0                               
       for target_cell in target_cells:
           if saveCellID:
              input_receiving_cells.append(target_cell)
           if input_group_parameters['numberModel']=="constant number of inputs per cell":
              no_of_inputs=input_group_parameters['noInputs']
           if synapse_array['numberModel']=="variable number of inputs per cell":
              if input_group_parameters['distribution']=="binomial":
                  no_of_inputs=np.random.binomial(input_group_parameters['maxNoInputs'],\
                  input_group_parameters['averageNoInputs']/input_group_parameters['maxNoInputs'])
               ### other options can be added
           if input_group_parameters['targetingModel']=="segment groups and segments":
              target_points=get_unique_target_points(segment_target_array,"segment groups and segments",\
              [input_group_parameters['segmentGroupList'],input_group_parameters['segmentGroupProbabilities']],no_of_inputs)
           if input_group_parameters['targetingModel']=="segments and subsegments":
              target_points=get_unique_target_points(segment_target_array,"segments and subsegments",\
              [input_group_parameters['segmentList'],input_group_parameters['segmentProbabilities'],\
              input_group_parameters['fractionAlongANDsubsegProbabilities']],no_of_inputs)
              for target_point in range(0,len(target_points)):
                  if libID=='newlyGenerated':
                     spike_times=np.loadtxt(currDir+"/simulations/%s/sim%d/%s_%s_syn%d_PoissonTrain_%d.dat"%(expID,simID,label,popID,synapse_index,target_point))
                  else:
                     spike_times=np.loadtxt(currDir+"/simulations/%s/sim%d/%s_PoissonTrain_%d.dat"%(libID,simID,synapse_array['inputIdLibrary'],target_point))
                  spike_times=np.transpose(spike_times)
                  spike_times=np.transpose(spike_times)
                  spike_times=spike_times[1]
                  spike_array=neuroml.SpikeArray(id="%s_%s_syn%d_%d"%(label,popID,synapse_index,target_point)
                                                  
                  for spike in range(0,len(spike_times)):
                      spike_object=neuroml.Spike(id="%d"%spike,time="%fs"%spike_times[spike])
	              spike_array.spikes.append(spike_object)
                  spike_arrays.append(spike_array)
                                                  
                  Input_pop=neuroml.Population(id="InputPop_%s_%s_syn%d_%d"%(label,popID,synapse_index,target_point), size=1,component=spike_array.id)
                  input_pop_array.append(Input_pop)
                  for synapse_index in range(0,len(synapse_list)):
                      synapse_array=synapse_list[synapse_index]
                      synapse_name=synapse_array['synapseType']
                      synapse_name_array.append(synapse_name)
                      proj = neuroml.Projection(id="InputProj_%s_%s_syn%d_%d"%(label,popID,synapse_index,target_point),presynaptic_population=Input_pop.id,\
                          postsynaptic_population=popID,synapse=synapse_name)
                                                  
                      conn = Connection(id=id, \
                            pre_cell_id="../%s[0]"%(Input_pop.id), \
                            pre_segment_id=0, \
                            pre_fraction_along=0.5
                            post_cell_id="../%s/%i/%s"%(popID,target_cell,cellType), \
                            post_segment_id="%d"%target_points[target_point,0],
                            post_fraction_along="%f"%target_points[target_point,1])
                   
                      proj.connections.append(conn)
                      proj_arrays.append(proj)
                                                 
    else:
       for synapse_index in range(0,len(synapse_list)):
           synapse_array=synapse_list[synapse_index]
           synapse_name=synapse_array['synapseType']
           synapse_name_array.append(synapse_name)                                          
           if synapse_array['targetingModel']=="segments and subsegments":
              segment_target_array=extract_morphology_information([cellTypeFile],{cellTypeFile:cellNML2Type},["segments",synapse_array['segmentList']])
                                                        
           if synapse_array['targetingModel']=="segment groups and segments":
              segment_target_array =extract_morphology_information([cellTypeFile],{cellTypeFile:cellNML2Type},["segment groups",synapse_array['segmentGroupList']])
                                                                                                                               
           count=0                               
           for target_cell in target_cells:
               if saveCellID:
                  input_receiving_cells.append(target_cell)                              
               if synapse_array['numberModel']=="constant number of inputs per cell":
                  no_of_inputs=synapse_array['noInputs']
               if synapse_array['numberModel']=="variable number of inputs per cell":
                  if synapse_array['distribution']=="binomial":
                     no_of_inputs=np.random.binomial(synapse_array['maxNoInputs'],\
                     synapse_array['averageNoInputs']/synapse_array['maxNoInputs'])
                  ### other options can be added
               if synapse_array['targetingModel']=="segment groups and segments":
                  target_points=get_unique_target_points(segment_target_array,"segment groups and segments",\
                  [synapse_array['segmentGroupList'],synapse_array['segmentGroupProbabilities']],no_of_inputs)
               if synapse_array['targetingModel']=="segments and subsegments":
                  target_points=get_unique_target_points(segment_target_array,"segments and subsegments",\
                  [synapse_array['segmentList'],synapse_array['segmentProbabilities'],\
                  synapse_array['fractionAlongANDsubsegProbabilities']],no_of_inputs)
               for target_point in range(0,len(target_points)):
                   if libID=='newlyGenerated':
                      spike_times=np.loadtxt(currDir+"/simulations/%s/sim%d/%s_%s_syn%d_PoissonTrain_%d.dat"%(expID,simID,label,popID,synapse_index,target_point))
                   else:
                      spike_times=np.loadtxt(currDir+"/simulations/%s/sim%d/%s_PoissonTrain_%d.dat"%(libID,simID,synapse_array['inputIdLibrary'],target_point))
                   spike_times=np.transpose(spike_times)
                   spike_times=spike_times[1]
                   spike_array=neuroml.SpikeArray(id="%s_%s_syn%d_%d"%(label,popID,synapse_index,target_point)
                                                  
                   for spike in range(0,len(spike_times)):
                       spike_object=neuroml.Spike(id="%d"%spike,time="%fs"%spike_times[spike])
	               spike_array.spikes.append(spike_object)
                   spike_arrays.append(spike_array)
                                                  
                   Input_pop=neuroml.Population(id="InputPop_%s_%s_syn%d_%d"%(label,popID,synapse_index,target_point), size=1,component=spike_array.id)
                   input_pop_array.append(Input_pop)
                                                  
                   proj = neuroml.Projection(id="InputProj_%s_%s_syn%d_%d"%(label,popID,synapse_index,target_point),presynaptic_population=Input_pop.id,\
                          postsynaptic_population=popID,synapse=synapse_name)
                                                  
                   conn = Connection(id=id, \
                            pre_cell_id="../%s[0]"%(Input_pop.id), \
                            pre_segment_id=0, \
                            pre_fraction_along=0.5
                            post_cell_id="../%s/%i/%s"%(popID,target_cell,cellType), \
                            post_segment_id="%d"%target_points[target_point,0],
                            post_fraction_along="%f"%target_points[target_point,1])
                   
                   proj.connections.append(conn)
                   proj_arrays.append(proj)

    return input_pop_array, spike_arrays,proj_arrays,synapse_name_array,input_receiving_cells



def XF_input_models_3D_region_specific_import(popID,popSize,cellType,cellNML2Type,input_group_parameters,cell_positions,seed_number,sim_params):

    random.seed(seed_number)
    parentDir=None
    simID=sim_params['simID']
    expID=sim_params['experimentID']
    lbID=sim_params['libraryID']
    saveCellID=sim_params['saveCellID']
    input_receiving_cells=[]                                         
    if 'currentDir' in sim_params:
        currDir=sim_params_dict['currentDir']
    if 'parentDirRequired' in sim_params:
        parentDir=sim_params_dict['parentDir']
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
                                                                        
               
    synapse_list=input_group_parameters['synapseList']
    label=input_group_parameters['inputLabel']
    input_pop_array=[]
    spike_arrays=[]
    proj_arrays=[]
    if input_group_parameters['colocalizeSynapses']:
       print("will add block for localizing synapses")
       if input_group_parameters['targetingModel']=="segments and subsegments":
          segment_target_array=extract_morphology_information([cellTypeFile],{cellTypeFile:cellNML2Type},["segments",input_group_parameters['segmentList']])
                                                        
       if input_group_parameters['targetingModel']=="segment groups and segments":
          segment_target_array =extract_morphology_information([cellTypeFile],{cellTypeFile:cellNML2Type},["segment groups",input_group_parameters['segmentGroupList']])
                                                                                                                               
       count=0                               
       for target_cell in target_cells:
           if saveCellID:
              input_receiving_cells.append(target_cell)
           if input_group_parameters['numberModel']=="constant number of inputs per cell":
              no_of_inputs=input_group_parameters['noInputs']
           if synapse_array['numberModel']=="variable number of inputs per cell":
              if input_group_parameters['distribution']=="binomial":
                  no_of_inputs=np.random.binomial(input_group_parameters['maxNoInputs'],\
                  input_group_parameters['averageNoInputs']/input_group_parameters['maxNoInputs'])
               ### other options can be added
           if input_group_parameters['targetingModel']=="segment groups and segments":
              target_points=get_unique_target_points(segment_target_array,"segment groups and segments",\
              [input_group_parameters['segmentGroupList'],input_group_parameters['segmentGroupProbabilities']],no_of_inputs)
           if input_group_parameters['targetingModel']=="segments and subsegments":
              target_points=get_unique_target_points(segment_target_array,"segments and subsegments",\
              [input_group_parameters['segmentList'],input_group_parameters['segmentProbabilities'],\
              input_group_parameters['fractionAlongANDsubsegProbabilities']],no_of_inputs)
              for target_point in range(0,len(target_points)):
                  if libID=='newlyGenerated':
                     spike_times=np.loadtxt(currDir+"/simulations/%s/sim%d/%s_%s_syn%d_PoissonTrain_%d.dat"%(expID,simID,label,popID,synapse_index,target_point))
                  else:
                     spike_times=np.loadtxt(currDir+"/simulations/%s/sim%d/%s_PoissonTrain_%d.dat"%(libID,simID,synapse_array['inputIdLibrary'],target_point))
                  spike_times=np.transpose(spike_times)
                  spike_times=np.transpose(spike_times)
                  spike_times=spike_times[1]
                  spike_array=neuroml.SpikeArray(id="%s_%s_syn%d_%d"%(label,popID,synapse_index,target_point)
                                                  
                  for spike in range(0,len(spike_times)):
                      spike_object=neuroml.Spike(id="%d"%spike,time="%fs"%spike_times[spike])
	              spike_array.spikes.append(spike_object)
                  spike_arrays.append(spike_array)
                                                  
                  Input_pop=neuroml.Population(id="InputPop_%s_%s_syn%d_%d"%(label,popID,synapse_index,target_point), size=1,component=spike_array.id)
                  input_pop_array.append(Input_pop)
                  for synapse_index in range(0,len(synapse_list)):
                      synapse_array=synapse_list[synapse_index]
                      synapse_name=synapse_array['synapseType']
                      synapse_name_array.append(synapse_name)
                      proj = neuroml.Projection(id="InputProj_%s_%s_syn%d_%d"%(label,popID,synapse_index,target_point),presynaptic_population=Input_pop.id,\
                          postsynaptic_population=popID,synapse=synapse_name)
                                                  
                      conn = Connection(id=id, \
                            pre_cell_id="../%s[0]"%(Input_pop.id), \
                            pre_segment_id=0, \
                            pre_fraction_along=0.5
                            post_cell_id="../%s/%i/%s"%(popID,target_cell,cellType), \
                            post_segment_id="%d"%target_points[target_point,0],
                            post_fraction_along="%f"%target_points[target_point,1])
                   
                      proj.connections.append(conn)
                      proj_arrays.append(proj)
                                                 
    else:
       for synapse_index in range(0,len(synapse_list)):
           synapse_array=synapse_list[synapse_index]
           synapse_name=synapse_array['synapseType']
           synapse_name_array.append(synapse_name)                                          
           if synapse_array['targetingModel']=="segments and subsegments":
              segment_target_array=extract_morphology_information([cellTypeFile],{cellTypeFile:cellNML2Type},["segments",synapse_array['segmentList']])
                                                        
           if synapse_array['targetingModel']=="segment groups and segments":
              segment_target_array =extract_morphology_information([cellTypeFile],{cellTypeFile:cellNML2Type},["segment groups",synapse_array['segmentGroupList']])
                                                                                                                               
           count=0                               
           for target_cell in target_cells:
               if saveCellID:
                  input_receiving_cells.append(target_cell)
               if synapse_array['numberModel']=="constant number of inputs per cell":
                  no_of_inputs=synapse_array['noInputs']
               if synapse_array['numberModel']=="variable number of inputs per cell":
                  if synapse_array['distribution']=="binomial":
                     no_of_inputs=np.random.binomial(synapse_array['maxNoInputs'],\
                     synapse_array['averageNoInputs']/synapse_array['maxNoInputs'])
                  ### other options can be added
               if synapse_array['targetingModel']=="segment groups and segments":
                  target_points=get_unique_target_points(segment_target_array,"segment groups and segments",\
                  [synapse_array['segmentGroupList'],synapse_array['segmentGroupProbabilities']],no_of_inputs)
               if synapse_array['targetingModel']=="segments and subsegments":
                  target_points=get_unique_target_points(segment_target_array,"segments and subsegments",\
                  [synapse_array['segmentList'],synapse_array['segmentProbabilities'],\
                  synapse_array['fractionAlongANDsubsegProbabilities']],no_of_inputs)
               for target_point in range(0,len(target_points)):
                   if libID=='newlyGenerated':
                      spike_times=np.loadtxt(currDir+"/simulations/%s/sim%d/%s_%s_syn%d_PoissonTrain_%d.dat"%(expID,simID,label,popID,synapse_index,target_point))
                   else:
                      spike_times=np.loadtxt(currDir+"/simulations/%s/sim%d/%s_PoissonTrain_%d.dat"%(libID,simID,synapse_array['inputIdLibrary'],target_point))
                   spike_times=np.transpose(spike_times)
                   spike_times=spike_times[1]
                   spike_array=neuroml.SpikeArray(id="%s_%s_syn%d_%d"%(label,popID,synapse_index,target_point)
                                                  
                   for spike in range(0,len(spike_times)):
                       spike_object=neuroml.Spike(id="%d"%spike,time="%fs"%spike_times[spike])
	               spike_array.spikes.append(spike_object)
                   spike_arrays.append(spike_array)
                                                  
                   Input_pop=neuroml.Population(id="InputPop_%s_%s_syn%d_%d"%(label,popID,synapse_index,target_point), size=1,component=spike_array.id)
                   input_pop_array.append(Input_pop)
                                                  
                   proj = neuroml.Projection(id="InputProj_%s_%s_syn%d_%d"%(label,popID,synapse_index,target_point),presynaptic_population=Input_pop.id,\
                          postsynaptic_population=popID,synapse=synapse_name)
                                                  
                   conn = Connection(id=id, \
                            pre_cell_id="../%s[0]"%(Input_pop.id), \
                            pre_segment_id=0, \
                            pre_fraction_along=0.5
                            post_cell_id="../%s/%i/%s"%(popID,target_cell,cellType), \
                            post_segment_id="%d"%target_points[target_point,0],
                            post_fraction_along="%f"%target_points[target_point,1])
                   
                   proj.connections.append(conn)
                   proj_arrays.append(proj)

    return input_pop_array, spike_arrays,proj_arrays,synapse_name_array,input_receiving_cells


                                                  

def XF_input_models_uniform(popID,popSize,cellType,cellNML2Type,input_group_parameters,seed_number,saveCellID,parentDir=None):


    random.seed(seed_number)
    input_receiving_cells=[]
    if parentDir !=None:
       cellTypeFile=parentDir+"/NeuroML2"+"/"+cellType
    else:
       cellTypeFile=cellType

    fraction_to_target_per_pop=input_group_parameters['fractionToTarget']
                                                                        
    target_cells=random.sample(range(popSize),int(round(fraction_to_target_per_pop*popSize)   )   )
                                                                        
               
    label=input_group_parameters['inputLabel']
    synapse_list=input_group_parameters['synapseList']
    synapse_name_array=[]
    poisson_synapse_array=[]
    input_list_array=[]
    for synapse_index in range(0,len(synapse_list)):
        synapse_array=synapse_list[synapse_index]
        synapse_name=synapse_array['synapseType']
        synapse_name_array.append(synapse_name)  
        synapse_dict={}                                         
        if synapse_array['targetingModel']=="segments and subsegments":
            segment_target_array=extract_morphology_information([cellTypeFile],{cellTypeFile:cellNML2Type},["segments",synapse_array['segmentList']])
                                                        
        if synapse_array['targetingModel']=="segment groups and segments":
           segment_target_array =extract_morphology_information([cellTypeFile],{cellTypeFile:cellNML2Type},["segment groups",synapse_array['segmentGroupList']])
                                                        
        if synapse_array['synapseMode']=="persistent":
           poisson_syn=neuroml.PoissonFiringSynapse(id="%s_%s_%s_syn%d"%(label,synapse_name,popID,synapse_index),\
                           average_rate="%f per_s"%synapse_array['averageRate'],\
                           synapse=synapse_array['synapseType'],\
                           spike_target="./%s"%synapse_array['synapseType'])
           synapse_dict['synapseMode']="persistent"      
           
   
        if synapse_array['synapseMode']=="transient":
           poisson_syn=neuroml.TransientPoissonFiringSynapse(id="%s_%s_%s_syn%d"%(label,synapse_name,popID,synapse_index),\
           average_rate="%f per_s"%synapse_array['averageRate'],\
           synapse=synapse_array['synapseType'] ,\
           spike_target="./%s"%synapse_array['synapseType'],\
           delay="%f%s"%(synapse_array['delay'],synapse_array['units']),\
           duration="%f%s"%(synapse_array['duration'],synapse_array['units'] )  )
              
           synapse_dict['synapseMode']="transient"

        synapse_dict['synapse_object']=poisson_syn
                            
        poisson_synapse_array.append(synapse_dict)

        input_list =neuroml.InputList(id="List_%s_%s_%s_syn%d"%(label,synapse_name,popID,synapse_index),component=poisson_syn.id,populations="%s"%popID)

                       
                                                                        
        count=0                               
        for target_cell in target_cells:
            if saveCellID:
               input_receiving_cells.append(target_cell)
            if synapse_array['numberModel']=="constant number of inputs per cell":
               no_of_inputs=synapse_array['noInputs']
            if synapse_array['numberModel']=="variable number of inputs per cell":
               if synapse_array['distribution']=="binomial":
                  no_of_inputs=np.random.binomial(synapse_array['maxNoInputs'],\
                  synapse_array['averageNoInputs']/synapse_array['maxNoInputs'])
               ### other options can be added
            if synapse_array['targetingModel']=="segment groups and segments":
               target_points=get_unique_target_points(segment_target_array,"segment groups and segments",\
               [synapse_array['segmentGroupList'],synapse_array['segmentGroupProbabilities']],no_of_inputs)
            if synapse_array['targetingModel']=="segments and subsegments":
               target_points=get_unique_target_points(segment_target_array,"segments and subsegments",\
               [synapse_array['segmentList'],synapse_array['segmentProbabilities'],\
               synapse_array['fractionAlongANDsubsegProbabilities']],no_of_inputs)
            for target_point in range(0,len(target_points)):                     
                syn_input = neuroml.Input(id="%d"%(count),target="../%s/%i/%s"%(popID,target_cell,cellType),\
                destination="synapses",segment_id="%d"%target_points[target_point,0],fraction_along="%f"%target_points[target_point,1]) 
                                             
                input_list.input.append(syn_input)
                count=count+1

        input_list_array.append(input_list)

    return input_list_array, poisson_synapse_array,synapse_name_array,input_receiving_cells


def XF_input_models_3D_region_specific(popID,cellType,cellNML2Type,input_group_parameters,cell_positions,seed_number,saveCellID,parentDir=None):

    random.seed(seed_number)
    input_receiving_cells=[]
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
                                                                        
    label=input_group_parameters['inputLabel']
    synapse_list=input_group_parameters['synapseList']
    synapse_name_array=[]
    poisson_synapse_array=[]
    input_list_array=[]
    for synapse_index in range(0,len(synapse_list)):
        synapse_name=synapse_list[synapse_index]['synapseType']
        synapse_name_array.append(synapse_name) 
        synapse_dict={}                                      
        if synapse_list[synapse_index]['targetingModel']=="segments and subsegments":
           segment_target_array=extract_morphology_information([cellTypeFile],{cellTypeFile:cellNML2Type},\
                ["segments",synapse_list[synapse_index]['segmentList']])
                                                        
        if synapse_list[synapse_index]['targetingModel']=="segment groups and segments":
           segment_target_array =extract_morphology_information([cellTypeFile],{cellTypeFile:cellNML2Type},\
        ["segment groups",synapse_list[synapse_index]['segmentGroupList']])
                                                        
        if  synapse_list[synapse_index]['synapseMode']=="persistent":
            poisson_syn=neuroml.PoissonFiringSynapse(id="%s_%s_%s_syn%d"%(label,synapse_name,popID,synapse_index),\
                           average_rate="%f per_s"%synapse_list[synapse_index]['averageRate'],\
                           synapse=synapse_list[synapse_index]['synapseType'],\
                           spike_target="./%s"%synapse_list[synapse_index]['synapseType'])
            synapse_dict['synapseMode']="persistent" 
                          
        if synapse_list[synapse_index]['synapseMode']=="transient":
           poisson_syn=neuroml.TransientPoissonFiringSynapse(id="%s_%s_%s_syn%d"%(label,synapse_name,popID,synapse_index),\
           average_rate="%f per_s"%synapse_list[synapse_index]['averageRate'],\
           synapse=synapse_list[synapse_index]['synapseType'] ,\
           spike_target="./%s"%synapse_list[synapse_index]['synapseType'],\
           delay="%f%s"%(synapse_list[synapse_index]['delay'],synapse_list[synapse_index]['units']),\
           duration="%f%s"%(synapse_list[synapse_index]['duration'],synapse_list[synapse_index]['units'] )  )
           synapse_dict['synapseMode']="transient"

        synapse_dict['synapse_object']=poisson_syn
                    
        poisson_synapse_array.append(synapse_dict)

        input_list =neuroml.InputList(id="List_%s_%s_%s_syn%d"%(label,synapse_name,popID,synapse_index),component=poisson_syn.id,populations="%s"%popID)

                       
                                                                        
        count=0                               
        for target_cell in target_cells:
            if saveCellID:
               input_receiving_cells.append(target_cell)
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

        input_list_array.append(input_list)
    return input_list_array, poisson_synapse_array,synapse_name_array,input_receiving_cells    





def variable_basal_firing_rate(popID,popSize,cellType,input_group_parameters,simulation_duration,seed_number):

   random.seed(seed_number)
   label=input_group_parameters['inputLabel']
   offset_units=input_group_parameters['offsetUnits']
   units=input_group_parameters['ampUnits']
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

       if "constant"==input_group_parameters["offsetDistribution"]:
          offset=input_group_parameters["valueOffset"]

       Pulse_generator_variable=neuroml.PulseGenerator(id="Pulse_%s_%s_%d"%(label,popID,cell),delay="%f%s"%(offset,offset_units),\
       duration="%f%s"%((simulation_duration-offset),offset_units),amplitude="%f%s"%(amp,units))
       pulse_generator_array.append(Pulse_generator_variable)
       Input_list=neuroml.InputList(id="%s_%s_%d"%(label,popID,cell),component="Pulse_%s_%s_%d"%(label,popID,cell),populations="%s"%popID)
       Inp = neuroml.Input(target="../%s/%d/%s"%(popID,cell,cellType),id="%d"%cell,destination="synapses")
       Input_list.input.append(Inp)
       input_list_array.append(Input_list)


   return input_list_array,pulse_generator_array

def testing(popID,popSize,cellType,input_group_parameters,seed_number,saveCellID):

     random.seed(seed_number)
     input_receiving_cells=[]
     amp_units=input_group_parameters['ampUnits']
     time_units=input_group_parameters['timeUnits']
     label=input_group_parameters['inputLabel']                                        
     randomly_select_target_cells=random.sample(range(popSize),int(round(popSize*input_group_parameters['cellFractionToTarget'])))
     pulseGenerator_array=[]
     input_list_array=[]
     for pulse_x in range(0,len(input_group_parameters['pulseParameters'])):
         Pulse_generator_x=neuroml.PulseGenerator(id="Pulse_%s_%s_%d"%(label,popID,pulse_x),\
         delay="%f%s"%(input_group_parameters['pulseParameters'][pulse_x]['delay'],time_units),\
         duration="%f%s"%(input_group_parameters['pulseParameters'][pulse_x]['duration'],time_units),\
         amplitude="%f%s"%(input_group_parameters['pulseParameters'][pulse_x]['amplitude'],amp_units))
	 pulseGenerator_array.append(Pulse_generator_x)
                                                         
         Input_list=neuroml.InputList(id="%s_%s_%d"%(label,popID,pulse_x), component="Pulse_%s_%s_%d"%(label,popID,pulse_x),populations="%s"%popID)
         
         for i in randomly_select_target_cells:
             if saveCellID:
                input_receiving_cells.append(i)
                                                  
             Inp = neuroml.Input(target="../%s/%d/%s"%(popID,i,cellType),id="%d"%i,destination="synapses")
             Input_list.input.append(Inp)

         input_list_array.append(Input_list)


     return input_list_array,pulseGenerator_array,input_receiving_cells
                      



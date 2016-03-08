
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
import os.path
from methods_v2 import *
from cell_distribution_models import *
from connectivity_models import *
from input_models import *


### a main script for generating and running golgi cell network by Rokas Stanislovas (2016)
def generate_golgi_cell_net(ref,cell_array,location_array,connectivity_information,input_information,simulation_parameters):
        
        
        if simulation_parameters['globalSeed']:
           random.seed(12345)
           seed=12345
        else:
           if simulation_parameters["trialSeed"]:
              random.seed(simulation_parameters["trialSeedNumber"])
              seed=simulation_parameters["trialSeedNumber"]

        nml_doc = neuroml.NeuroMLDocument(id=ref)
        #cell_array will have to include cell_types and no_of_cells
        #connectivity_information is a list of lists that will have to include connectivity parameters; now code only for a random configuration with parameters connection_probability and conductance_strength

        
        cell_type_list=[]
        for x in range(0,len(cell_array)):
            cell_type_list.append(cell_array[x]['cellType'])
            
        unique_cell_names=np.unique(cell_type_list)

        for unique_cell in unique_cell_names:
            if 'networkDir' in simulation_parameters and 'parentDirRequired' in simulation_parameters:
               if simulation_parameters['parentDirRequired'] and (simulation_parameters['networkDir']=="example" or simulation_parameters['networkDir']=="experiment"):
                  include_cell=neuroml.IncludeType(href="/../../../"+"%s.cell.nml"%unique_cell)
            else:
               include_cell=neuroml.IncludeType(href="%s.cell.nml"%unique_cell)

            nml_doc.includes.append(include_cell)

	
	# Create network
	net = neuroml.Network(id=ref+"_network",type="networkWithTemperature",temperature="23 degC")
	nml_doc.networks.append(net)

        Note_string="Parameter arrays for building this network are listed below:\n"

        
        Golgi_pop_index_array=[]
        neuroml_Golgi_pop_array={}

        for x in range(0,len(cell_array)):
	    Golgi_pop = neuroml.Population(id=cell_array[x]['popID'], size =cell_array[x]['size'], type="populationList",
		                  component=cell_array[x]['cellType'])
	    Golgi_pop_index_array.append(cell_array[x]['popID'])
            neuroml_Golgi_pop_array[cell_array[x]['popID']]=Golgi_pop
	    

        cell_diameter_array={}
        for cell_pop in range(0,len(cell_array)):
            if simulation_parameters['parentDirRequired']:

               if "NeuroML2CellType" in cell_array[cell_pop]:
                   cell_diameter=get_soma_diameter(simulation_parameters['parentDir']+"/NeuroML2"+"/"+cell_array[cell_pop]['cellType'],cell_array[cell_pop]["NeuroML2CellType"])
               else:
                   cell_diameter=get_soma_diameter(simulation_parameters['parentDir']+"/NeuroML2"+"/"+cell_array[cell_pop]['cellType'])
            else:

               if "NeuroML2CellType" in cell_array[cell_pop]:
                  cell_diameter=get_soma_diameter(cell_array[cell_pop]['cellType'],cell_array[cell_pop]["NeuroML2CellType"])
               else:
                  cell_diameter=get_soma_diameter(cell_array[cell_pop]['cellType'])

            cell_diameter_array[cell_array[cell_pop]['popID']]=cell_diameter

        
        
	cell_position_array={}

	for cell_population in range(0,len(cell_array)):
            cell_position_array[ cell_array[cell_population]['popID']]=np.zeros([0,3])
	
	Note_string=Note_string+"Cell distribution parameters:\n"
	
        
        ################# 
        for pop in range(0,len(location_array['populationList'])):
            Note_string=Note_string+"%s\n"%location_array['populationList'][pop]
            if location_array['populationList'][pop]['distanceModel']=="random_no_overlap":
               
               if location_array['populationList'][pop]['distributionModel']=="density_profile":
                  location_parameters=location_array['populationList'][pop]
                  golgi_pop_object=neuroml_Golgi_pop_array[location_parameters['popID']]
                  
                  pop_position_array, total_no_of_cells,Golgi_pop=density_model(location_parameters,golgi_pop_object,seed,pop,cell_position_array,cell_array,\
                  cell_diameter_array)

                  cell_array[pop]['size']=total_no_of_cells

                  cell_position_array[cell_array[pop]['popID']]=np.vstack((cell_position_array[cell_array[pop]['popID']],pop_position_array))
          
                  net.populations.append(Golgi_pop)
                  
               if location_array['populationList'][pop]['distributionModel']=="explicit_cell_numbers":
                       
                  golgi_pop_object=neuroml_Golgi_pop_array[cell_array[pop]['popID']]
                  dim_dict_max_values={}
                  dim_dict_max_values['x_dim']=location_array['populationList'][pop]['xDim']
                  dim_dict_max_values['y_dim']=location_array['populationList'][pop]['yDim']
                  dim_dict_max_values['z_dim']=location_array['populationList'][pop]['zDim']
                  
                  pop_position_array,Golgi_pop=random_no_overlap(cell_position_array,cell_array,cell_diameter_array,\
                  pop,seed,golgi_pop_object,dim_dict_max_values)

                  cell_position_array[cell_array[pop]['popID']]=np.vstack((cell_position_array[cell_array[pop]['popID']],pop_position_array))
                  

                  net.populations.append(Golgi_pop)
                  
            if location_array['populationList'][pop]['distanceModel']=="random_minimal_distance":
               
               if location_array['populationList'][pop]['distributionModel']=="density_profile":

                  location_parameters=location_array['populationList'][pop]
                  golgi_pop_object=neuroml_Golgi_pop_array[location_parameters['popID']]
                  pop_position_array, total_no_of_cells,Golgi_pop=density_model(location_parameters,golgi_pop_object,seed,pop,cell_position_array,cell_array)

                  cell_array[pop]['size']=total_no_of_cells

                  cell_position_array[cell_array[pop]['popID']]=np.vstack((cell_position_array[cell_array[pop]['popID']],pop_position_array))
          
                  net.populations.append(Golgi_pop)
                  
               if location_array['populationList'][pop]['distributionModel']=="explicit_cell_numbers":
                  minimal_distance=location_array['populationList'][pop]['minimal_distance']
                  golgi_pop_object=neuroml_Golgi_pop_array[cell_array[pop]['popID']]
                  dim_dict_max_values={}
                  dim_dict_max_values['x_dim']=location_array['populationList'][pop]['xDim']
                  dim_dict_max_values['y_dim']=location_array['populationList'][pop]['yDim']
                  dim_dict_max_values['z_dim']=location_array['populationList'][pop]['zDim']
                         
                  pop_position_array,Golgi_pop=random_minimal_distance(cell_position_array,cell_array,\
minimal_distance,pop,seed,golgi_pop_object,dim_dict_max_values)

                  cell_position_array[cell_array[pop]['popID']]=np.vstack((cell_position_array[cell_array[pop]['popID']],pop_position_array))
                  

                  net.populations.append(Golgi_pop)
                    
            if location_array['populationList'][pop]['distanceModel']=="random":

               if location_array['populationList'][pop]['distributionModel']=="density_profile":

                  location_parameters=location_array['populationList'][pop]
                  golgi_pop_object=neuroml_Golgi_pop_array[location_parameters['popID']]

                  pop_position_array, total_no_of_cells,Golgi_pop=density_model(location_parameters,golgi_pop_object,seed)

                  cell_array[pop]['size']=total_no_of_cells

                  cell_position_array[cell_array[pop]['popID']]=np.vstack((cell_position_array[cell_array[pop]['popID']],pop_position_array))
          
                  net.populations.append(Golgi_pop)



               if location_array['populationList'][pop]['distributionModel']=="explicit_cell_numbers":
                  Golgi_pop=neuroml_Golgi_pop_array[cell_array[pop]['popID']]  
                  for cell in range(0,cell_array[cell_pop]['size']):
	              Golgi_cell=neuroml.Instance(id="%d"%cell)
	              Golgi_pop.instances.append(Golgi_cell)
	              X=random.random()
	              Y=random.random()
	              Z=random.random()
                      x_dim=location_array['populationList'][pop]['xDim']
                      y_dim=location_array['populationList'][pop]['yDim']
                      z_dim=location_array['populationList'][pop]['zDim']
                      Golgi_cell.location=neuroml.Location(x=x_dim*X, y=y_dim*Y, z=z_dim*Z)
                      cell_position_array[cell_array[pop]['popID']]=np.vstack((cell_position_array[cell_array[pop]['popID']],[x_dim*X,y_dim*Y,z_dim*Z]))
                      print cell_position_array[cell_array[cell_pop]['popID']][cell,0], cell_position_array[cell_array[cell_pop]['popID']][cell,1], cell_position_array[cell_array[cell_pop]['popID']][cell,2]
                  net.populations.append(Golgi_pop)

        Note_string=Note_string+"Cell population parameters:\n"
        for population in range(0,len(cell_array)):
            Note_string=Note_string+"Cell population parameters for %s:\n"%cell_array[population]['popID']
            Note_string=Note_string+"%s\n"%cell_array[population]
        ############################################ connectivity block
        synapse_name_array=[]        
        connMatrix_array=[]
        initial_projection_counter=0
        synapse_counter=0
        Note_string=Note_string+"Cell connectivity parameters:\n"
        for pair in range(0,len(connectivity_information['populationPairs']) ):
            prePop=connectivity_information['populationPairs'][pair]['prePopID']  
            postPop=connectivity_information['populationPairs'][pair]['postPopID']
            preCell_NML2type=None
            postCell_NML2type=None
            for pop in range(0,len(cell_array)):
                if cell_array[pop]['popID']==prePop:
                   prePop_listIndex=pop
                   prePopSize=cell_array[pop]['size']
                if cell_array[pop]['popID']==postPop:
                   postPop_listIndex=pop
                   postPopSize=cell_array[pop]['size']

            if "NeuroML2CellType" in cell_array[prePop_listIndex]:
               preCell_NML2type=cell_array[prePop_listIndex]["NeuroML2CellType"]

            if "NeuroML2CellType" in cell_array[postPop_listIndex]:
               postCell_NML2type=cell_array[postPop_listIndex]["NeuroML2CellType"]
            
            if 'electricalConnModel' in connectivity_information['populationPairs'][pair]:
               ########## 2012 publication-based generation of model connectivity 
               if connectivity_information['populationPairs'][pair]['electricalConnModel']=="Vervaeke_2012_based" or connectivity_information['populationPairs'][pair]['electricalConnModel']=="explicit_connection_probabilities":
                  pair_connectivity_parameters=connectivity_information['populationPairs'][pair]
                  pre_pop_cell_component=cell_array[prePop_listIndex]['cellType']
                  post_pop_cell_component=cell_array[postPop_listIndex]['cellType']
                  pre_pop_cell_positions=cell_position_array[prePop]
                  print pre_pop_cell_positions
                  post_pop_cell_positions=cell_position_array[postPop]
                  print post_pop_cell_positions
                  if simulation_parameters['parentDirRequired']:
                     proj, nonempty_projection,gap_junction_array=Vervaeke_2012_AND_explicit_conn_prob_model(pair,initial_projection_counter,prePop,prePop_listIndex,prePopSize,pre_pop_cell_component,preCell_NML2type,pre_pop_cell_positions,\
                             postPop,postPop_listIndex,postPopSize,post_pop_cell_component,postCell_NML2type,post_pop_cell_positions,pair_connectivity_parameters,seed,simulation_parameters['parentDir'])
                  else:
                     proj, nonempty_projection,gap_junction_array=Vervaeke_2012_AND_explicit_conn_prob_model(pair,initial_projection_counter,prePop,prePop_listIndex,prePopSize,pre_pop_cell_component,preCell_NML2type,pre_pop_cell_positions,\
         postPop,postPop_listIndex,postPopSize,post_pop_cell_component,postCell_NML2type,post_pop_cell_positions,pair_connectivity_parameters,seed)
                  
                  if nonempty_projection:
                     initial_projection_counter+=1
                     net.electrical_projections.append(proj)
                     for gapJ in range(0,len(gap_junction_array)):
                         nml_doc.gap_junctions.append(gap_junction_array[gapJ])
               

               ############# 2010, both connection probabilities and synaptic weights are distance-dependent              
               if connectivity_information['populationPairs'][pair]['electricalConnModel']=="Vervaeke_2010_based":
                  pair_connectivity_parameters=connectivity_information['populationPairs'][pair]
                  pre_pop_cell_component=cell_array[prePop_listIndex]['cellType']
                  post_pop_cell_component=cell_array[postPop_listIndex]['cellType']
                  pre_pop_cell_positions=cell_position_array[prePop]
                  post_pop_cell_positions=cell_position_array[postPop]
                  
                  if simulation_parameters['parentDirRequired']:
                     proj, nonempty_projection,gap_junction_array=Vervaeke_2010_model(pair,initial_projection_counter,prePop,prePop_listIndex,prePopSize,pre_pop_cell_component,preCell_NML2type,pre_pop_cell_positions,\
postPop,postPop_listIndex,postPopSize,post_pop_cell_component,postCell_NML2type,post_pop_cell_positions,pair_connectivity_parameters,seed,simulation_parameters['parentDir'])
                  else:
                     proj, nonempty_projection,gap_junction_array=Vervaeke_2010_model(pair,initial_projection_counter,prePop,prePop_listIndex,prePopSize,pre_pop_cell_component,preCell_NML2type,pre_pop_cell_positions,\
 postPop,postPop_listIndex,postPopSize,post_pop_cell_component,postCell_NML2type,post_pop_cell_positions,pair_connectivity_parameters,seed)
  
                  if nonempty_projection:
                     initial_projection_counter+=1
                     net.electrical_projections.append(proj)
                     for gapJ in range(0,len(gap_junction_array)):
                         nml_doc.gap_junctions.append(gap_junction_array[gapJ])

            #######  introduce chemical connections into network building    
            if 'chemicalConnModel' in connectivity_information['populationPairs'][pair]:    
               pair_connectivity_parameters=connectivity_information['populationPairs'][pair]
               pre_pop_cell_component=cell_array[prePop_listIndex]['cellType']
               post_pop_cell_component=cell_array[postPop_listIndex]['cellType']
               pre_pop_cell_positions=cell_position_array[prePop]
               post_pop_cell_positions=cell_position_array[postPop]
               
               if simulation_parameters['parentDirRequired']:
                  proj, nonempty_projection,gap_junction_array,synapse_name=chemical_connection_model(pair,initial_projection_counter,prePop,prePop_listIndex,prePopSize,pre_pop_cell_component,preCell_NML2type,pre_pop_cell_positions,\
postPop,postPop_listIndex,postPopSize,post_pop_cell_component,postCell_NML2type,post_pop_cell_positions,pair_connectivity_parameters,seed,simulation_parameters['parentDir'])
               else:
                  proj, nonempty_projection,gap_junction_array,synapse_name=chemical_connection_model(pair,initial_projection_counter,prePop,prePop_listIndex,prePopSize,pre_pop_cell_component,preCell_NML2type,pre_pop_cell_positions,\
postPop,postPop_listIndex,postPopSize,post_pop_cell_component,postCell_NML2type,post_pop_cell_positions,pair_connectivity_parameters,seed)

               synapse_name_array.append(synapse_name)
               if nonempty_projection:
                  initial_projection_counter+=1
                  net.electrical_projections.append(proj)
                  for gapJ in range(0,len(gap_junction_array)):
                      nml_doc.gap_junctions.append(gap_junction_array[gapJ])
            
            Note_string=Note_string+"%s"%connectivity_information['populationPairs'][pair]+"\n"                                      
        ####################        input block                                                           
        Note_string=Note_string+"Input parameters for a list of populations:"+"\n" 
        for pop in range(0,len(input_information)):
            popID=input_information[pop]['popName']
            Note_string=Note_string+"Input group parameters for %s:"%popID+"\n" 
            for pop_in in range(0,len(cell_array)):
                if cell_array[pop_in]['popID']==popID:
                   pop_listIndex=pop_in
                   popSize=cell_array[pop_in]['size']
            input_group_array=input_information[pop]['inputGroups']
            cellType=cell_array[pop_listIndex]['cellType']
            cellNML2Type=None

            if "NeuroML2CellType" in cell_array[pop_listIndex]:
               cellNML2Type=cell_array[pop_listIndex]["NeuroML2CellType"]


            for input_group in range(0,len(input_group_array)):
                if input_group_array[input_group]['inputModel']=='XF' and input_group_array[input_group]['targetingRegime']=="uniform":
                            
                   if 'importPoissonTrainLibraries' in simulation_parameters:
                      if simulation_parameters['importPoissonTrainLibraries']:
                         print("will test generation and import of spike trains")
                         sim_params_dict={}
                         sim_params_dict['simID']=simulation_parameters['simID']
                         sim_params_dict['experimentID']=simulation_parameters['experimentID']
                         sim_params_dict['libraryID']=simulation_parameters['PoissonTrainLibraryID']
                         sim_params_dict['saveCellID']=simulation_parameters['saveInputReceivingCellID']
                         sim_params_dict['libraryParams']=simulation_parameters['libraryParams']
                         if simulation_parameters['currentDirRequired']:
                            sim_params_dict['currentDir']=simulation_parameters['currentDir']
                         if simulation_parameters['parentDirRequired']:
                            sim_params_dict['parentDir']=simulation_parameters['parentDir']

                         input_pops,spike_array_list,proj_arrays,synapse_name_list,cells_with_inputs=XF_input_models_uniform_import(popID,popSize,cellType,cellNML2Type,\
input_group_array[input_group],seed,sim_params_dict)
                         a=synapse_name_list
                         synapse_name_array.extend(synapse_name_list)

                         for input_pop in range(0,len(input_pops)):
                             net.populations.append(input_pops[input_pop])
                         for spike_array in range(0,len(spike_array_list)):
                             nml_doc.spike_arrays.append(spike_array_list[spike_array])
                         for projection in range(0,len(proj_arrays)):
                             net.projections.append(proj_arrays[projection])
                         
                   else:
                      if simulation_parameters['parentDirRequired']:
                         input_list_array,poisson_synapse_array,synapse_name_list,cells_with_inputs=XF_input_models_uniform(popID,popSize,cellType,cellNML2Type,input_group_array[input_group],seed,simulation_parameters['saveInputReceivingCellID'],simulation_parameters['parentDir'])
                      else:
                         input_list_array,poisson_synapse_array,synapse_name_list,cells_with_inputs=XF_input_models_uniform(popID,popSize,cellType,cellNML2Type,input_group_array[input_group],seed,\
                         simulation_parameters['saveInputReceivingCellID'])                                          
                   

                      synapse_name_array.extend(synapse_name_list)

                   
                      for poisson_syn in range(0,len(poisson_synapse_array)):
                          if poisson_synapse_array[poisson_syn]['synapseMode']=="persistent":
                             nml_doc.poisson_firing_synapses.append(poisson_synapse_array[poisson_syn]['synapse_object'])
                          if poisson_synapse_array[poisson_syn]['synapseMode']=="transient":
                             nml_doc.transient_poisson_firing_synapses.append(poisson_synapse_array[poisson_syn]['synapse_object'])
                          net.input_lists.append(input_list_array[poisson_syn])

                   if simulation_parameters['saveInputReceivingCellID']:
                   
                      if simulation_parameters['currentDirRequired']:
                         save_to_path=simulation_parameters['currentDir']+"/simulations/%s/sim%d"%(simulation_parameters['experimentID'],simulation_parameters['simID'])
                      else:
                         save_to_path="simulations/%s/sim%d"%(simulation_parameters['experimentID'],simulation_parameters['simID'])

                      np.savetxt('%s/%s_%s.txt'%(save_to_path,cell_array[pop_listIndex]['popID'],input_group_array[input_group]['inputLabel']),cells_with_inputs,\
                      fmt="%d" ) 
      
                if input_group_array[input_group]['inputModel']=='XF' and input_group_array[input_group]['targetingRegime']=="3D_region_specific":
                                   
                   if 'importPoissonTrainLibraries' in simulation_parameters:
                      if simulation_parameters['importPoissonTrainLibraries']:
                         print("will test generation and import of spike trains")
                         sim_params_dict={}
                         sim_params_dict['simID']=simulation_parameters['simID']
                         sim_params_dict['experimentID']=simulation_parameters['experimentID']
                         sim_params_dict['libraryID']=simulation_parameters['PoissonTrainLibraryID']
                         sim_params_dict['saveCellID']=simulation_parameters['saveInputReceivingCellID']
                         sim_params_dict['libraryParams']=simulation_parameters['libraryParams']
                         if simulation_parameters['currentDirRequired']:
                            sim_params_dict['currentDir']=simulation_parameters['currentDir']
                         if simulation_parameters['parentDirRequired']:
                            sim_params_dict['parentDir']=simulation_parameters['parentDir']
                         input_pops,spike_array_list,proj_arrays,synapse_name_list,cells_with_inputs=XF_input_model_3D_region_specific_import(popID,cellType,cellNML2Type,input_group_array[input_group],\
                         cell_position_array[popID],seed,sim_params_dict)                                       
                   
                         synapse_name_array.extend(synapse_name_list)
                         
                         for input_pop in range(0,len(input_pops)):
                             net.populations.append(input_pops[input_pop])
                         for spike_array in range(0,len(spike_array_list)):
                             nml_doc.spike_arrays.append(spike_array_list[spike_array])
                         for projection in range(0,len(proj_arrays)):
                             net.projections.append(proj_arrays[projection])

                
                   else:
                      if simulation_parameters['parentDirRequired']:
                           
                         input_list_array,poisson_synapse_array,synapse_name_list,cells_with_inputs=XF_input_model_3D_region_specific(popID,cellType,cellNML2Type,input_group_array[input_group],\
                         cell_position_array[popID],seed,simulation_parameters['saveInputReceivingCellID'],simulation_parameters['parentDir'])   

                      else:
                         input_list_array,poisson_synapse_array,synapse_name_list,cells_with_inputs=XF_input_model_3D_region_specific(popID,cellType,cellNML2Type,input_group_array[input_group],\
                         cell_position_array[popID],seed,simulation_parameters['saveInputReceivingCellID'])                                          
                   

                      synapse_name_array.extend(synapse_name_list)

                   

                      for poisson_syn in range(0,len(poisson_synapse_array)):
                          if poisson_synapse_array[poisson_syn]['synapseMode']=="persistent":
                             nml_doc.poisson_firing_synapses.append(poisson_synapse_array[poisson_syn]['synapse_object'])
                          if poisson_synapse_array[poisson_syn]['synapseMode']=="transient":
                             nml_doc.transient_poisson_firing_synapses.append(poisson_synapse_array[poisson_syn]['synapse_object'])           
                          net.input_lists.append(input_list_array[poisson_syn])

                   if simulation_parameters['saveInputReceivingCellID']:
                   
                      if simulation_parameters['currentDirRequired']:
                         save_to_path=simulation_parameters['currentDir']+"/simulations/%s/sim%d"%(simulation_parameters['experimentID'],simulation_parameters['simID'])
                      else:
                         save_to_path="simulations/%s/sim%d"%(simulation_parameters['experimentID'],simulation_parameters['simID'])

                      np.savetxt('%s/%s_%s.txt'%(save_to_path,cell_array[pop_listIndex]['popID'],input_group_array[input_group]['inputLabel']),cells_with_inputs,\
                      fmt="%d" ) 
	        ###### implementing physiological heterogeneity between cells with variations in a basal firing rate

                if input_group_array[input_group]['inputModel']=="variable_basal_firing_rate":

                   input_list_array,pulseGenerator_array=variable_basal_firing_rate(popID,popSize,cellType,input_group_array[input_group],\
                   simulation_parameters['duration'],seed)                                          

                   for input_list in range(0,len(input_list_array)):
          
                       net.input_lists.append(input_list_array[input_list])
                       nml_doc.pulse_generators.append(pulseGenerator_array[input_list])
                   
	               
	        ##############
                if input_group_array[input_group]['inputModel']=="testing":

                   input_list_array,pulseGenerator_array,cells_with_inputs=testing(popID,popSize,cellType,input_group_array[input_group],seed,simulation_parameters['saveInputReceivingCellID'])                                          

                   for input_list in range(0,len(input_list_array)):
          
                       net.input_lists.append(input_list_array[input_list])
                       nml_doc.pulse_generators.append(pulseGenerator_array[input_list])

                
                Note_string=Note_string+"%s"%input_group_array[input_group]+"\n"  
                
                
                   
        ##############       
	unique_synapse_names=np.unique(synapse_name_array)
        for unique_synapse in unique_synapse_names:
            if 'networkDir' in simulation_parameters and 'parentDirRequired' in simulation_parameters:
               if simulation_parameters['parentDirRequired'] and ( simulation_parameters['networkDir']=="example" or simulation_parameters['networkDir']=="experiment"):
                  include_synapse=neuroml.IncludeType(href="/../../../"+"%s.synapse.nml"%unique_synapse)
            else:
               include_synapse=neuroml.IncludeType(href="%s.synapse.nml"%unique_synapse)
            nml_doc.includes.append(include_synapse)
                                                 
        net.notes=Note_string
        
        if simulation_parameters['parentDirRequired']:

           if 'networkDir' in simulation_parameters:
               if  simulation_parameters['networkDir']=="example":
                   nml_file_dir =simulation_parameters['parentDir']+"/NeuroML2/NML2_LEMS_Net_Examples/"+simulation_parameters['experimentID']+"/"+"sim%d"%simulation_parameters['simID']+"/"+'%s.net.nml'%ref
                   path=simulation_parameters['parentDir']+"/NeuroML2/NML2_LEMS_Net_Examples/"+simulation_parameters['experimentID']+"/"+"sim%d"%simulation_parameters['simID']
               if simulation_parameters['networkDir']=="experiment":
                  nml_file_dir =simulation_parameters['parentDir']+"/NeuroML2/NML2_LEMS_Experiments/"+simulation_parameters['experimentID']+"/"+"sim%d"%simulation_parameters['simID']+"/"+'%s.net.nml'%ref
                  path=simulation_parameters['parentDir']+"/NeuroML2/NML2_LEMS_Experiments/"+simulation_parameters['experimentID']+"/"+"sim%d"%simulation_parameters['simID']

        

               if not os.path.exists(path):
                  os.makedirs(path)
        else:
           nml_file_dir ='%s.net.nml'%ref
        
        writers.NeuroMLWriter.write(nml_doc,nml_file_dir)


        nml_file='%s.net.nml'%ref

        print("Written network file to: "+nml_file_dir)
    
        ###### Validate the NeuroML2 ######   

        validate_neuroml2(nml_file_dir)
        
        sim_info_array={}
        sim_info_array['ref']=ref
        sim_info_array['netID']=net.id
        sim_info_array['simParams']=simulation_parameters
        sim_info_array['nmlFile']=nml_file
        sim_info_array['nmlPath']=path
       
        cell_info_array={}
        cell_info_array['popParams']=cell_array
        cell_info_array['cellPositionArray']=cell_position_array
        
        return sim_info_array, cell_info_array

def generate_LEMS_and_run(sim_array,pop_array):
        ref= sim_array['ref']
        net_id=sim_array['netID']
        simulation_parameters=sim_array['simParams']
        nml_file=sim_array['nmlFile']
        path=sim_array['nmlPath']

        cell_array=pop_array['popParams']
        
       
        # Create a LEMSSimulation to manage creation of LEMS file

        ls = LEMSSimulation(ref, simulation_parameters['duration'], simulation_parameters['timeStep'])
        
        # Point to network as target of simulation
    
        ls.assign_simulation_target(net_id)
        print simulation_parameters['parentDir']
        ls.include_neuroml2_file(nml_file,True,path)
        
        

        # Specify Displays and Output Files
	for x in range(0,len(cell_array)):
	    disp = "display_voltages%s"%(cell_array[x]['popID'])
	    ls.create_display(disp, "Voltages %s"%(cell_array[x]['popID']), "-75", "50")
	       
	    max_traces = 20
	    if cell_array[x]['size']<=max_traces:
	       for i in range(cell_array[x]['size']):
		   quantity = "%s/%i/%s/v"%(cell_array[x]['popID'], i,cell_array[x]['cellType'])
	           ls.add_line_to_display(disp, "../%s/%i: Vm"%(cell_array[x]['popID'],i), quantity, "1mV", pynml.get_next_hex_color())
                   of0 = 'Volts%d_file0_%d'%(x,i)
                   if simulation_parameters['currentDirRequired']:
                      ls.create_output_file(of0,simulation_parameters['currentDir']+"/simulations/%s/sim%d/%s_cell%d.dat"%(simulation_parameters['experimentID'],simulation_parameters['simID'],\
                                                                                    cell_array[x]['popID'],i))
                   else:
                      ls.create_output_file(of0,"simulations/%s/sim%d/%s_cell%d.dat"%(simulation_parameters['experimentID'],simulation_parameters['simID'],\
                                                                                    cell_array[x]['popID'],i))
		   ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
					   
	    else:
	       randomly_select_displayed_cells=random.sample(range(cell_array[x]['size']),max_traces)
	       for y in randomly_select_displayed_cells:
                   quantity = "%s/%i/%s/v"%(cell_array[x]['popID'], y, cell_array[x]['cellType'])
		   ls.add_line_to_display(disp, "../%s/%i: Vm"%(cell_array[x]['popID'],y), quantity, "1mV", pynml.get_next_hex_color())
					      
	       for i in range(cell_array[x]['size']):
		   quantity = "%s/%i/%s/v"%(cell_array[x]['popID'], i,cell_array[x]['cellType'])
                   of0 = 'Volts%d_file0_%d'%(x,i)
                   if simulation_parameters['currentDirRequired']:
                      ls.create_output_file(of0,simulation_parameters['currentDir']+"/simulations/%s/sim%d/%s_cell%d.dat"%(simulation_parameters['experimentID'],simulation_parameters['simID'],x,i))
                   else:
                      ls.create_output_file(of0,"simulations/%s/sim%d/%s_cell%d.dat"%(simulation_parameters['experimentID'],simulation_parameters['simID'],x,i))
		   ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
       
	# save LEMS file
        if simulation_parameters['parentDirRequired']:
           if simulation_parameters['networkDir']=="example":
              lems_file_name_dir=simulation_parameters['parentDir']+"/NeuroML2/NML2_LEMS_Net_Examples/"+simulation_parameters['experimentID']+"/"+"sim%d"%simulation_parameters['simID']+"/"+"LEMS_%s.xml"%ref
              lems_file_name = ls.save_to_file(lems_file_name_dir)
              

           if simulation_parameters['networkDir']=="experiment":
              lems_file_name_dir=simulation_parameters['parentDir']+"/NeuroML2/NML2_LEMS_Experiments/"+simulation_parameters['experimentID']+"/"+"sim%d"%simulation_parameters['simID']+"/"+"LEMS_%s.xml"%ref
              lems_file_name = ls.save_to_file(lems_file_name_dir)
        else:
           lems_file_name = ls.save_to_file()
           lems_file_name_dir="LEMS_%s.xml"%ref

        if simulation_parameters['plotSpecifier']:
           if simulation_parameters['simulator']=="jNeuroML":
              print("Finished building a network. Starts running a simulation with jNeuroML for %s"%lems_file_name_dir)
	      results1 = pynml.run_lems_with_jneuroml(lems_file_name, nogui=True, load_saved_data=True, plot=True)
              print("Finished running simulation with jNeuroML")
           elif simulation_parameters['simulator']=="jNeuroML_NEURON":
              print("Finished building a network. Starts running a simulation with NEURON for %s"%lems_file_name_dir)
              results1 = pynml.run_lems_with_jneuroml_neuron(lems_file_name, nogui=True, load_saved_data=True, plot=True)
              print("Finished running simulation with jNeuroML_NEURON")
           else:
              print("Finished building a network")
        else:
           if simulation_parameters['simulator']=="jNeuroML":
              print("Finished building a network. Starts running a simulation with jNeuroML for %s"%lems_file_name_dir)
	      results1 = pynml.run_lems_with_jneuroml(lems_file_name, nogui=True, load_saved_data=False, plot=False)
              print("Finished running simulation with jNeuroML")
           elif simulation_parameters['simulator']=="jNeuroML_NEURON":
              print("Finished building a network. Starts running a simulation with NEURON for %s"%lems_file_name_dir)
              results1 = pynml.run_lems_with_jneuroml_neuron(lems_file_name, nogui=True, load_saved_data=False, plot=False)
              print("Finished running simulation with jNeuroML_NEURON")
           else:
              print("Finished building a network")
         
### a main script for generating and running golgi cell network by Rokas Stanislovas (2016)
def generate_PoissonInputNet(ref,cell_array,location_array,connectivity_information,input_information,simulation_parameters,library_params):
        
        
        if simulation_parameters['globalSeed']:
           random.seed(12345)
           seed=12345
        else:
           if simulation_parameters["trialSeed"]:
              random.seed(simulation_parameters["trialSeedNumber"])
              seed=simulation_parameters["trialSeedNumber"]

        nml_doc = neuroml.NeuroMLDocument(id=ref)
        
	# Create network
	net = neuroml.Network(id=ref+"_network")
	nml_doc.networks.append(net)
        
        Note_string="A simple network that generates Poisson input trains for Golgi_%s"%ref[9:]
        net.notes=Note_string
        
        Golgi_pop_index_array=[]
        neuroml_Golgi_pop_array={}

	    
        dummy_syn=neuroml.ExpOneSynapse(erev="0mV",gbase="5nS", tau_decay="2.5ms",id="syn0")
        nml_doc.exp_one_synapses.append(dummy_syn)
        dummy_cell=neuroml.IafCell(id='iaf0',leak_reversal="-60mV",thresh="-40mV",reset="-70mV" ,C="1e-5uF", leak_conductance="5.2e-7mS")
        nml_doc.iaf_cells.append(dummy_cell)
        PopID_array=[]
        target_no_array=[]
        Poisson_syn_id_array=[]
        for pop in range(0,len(input_information)):
            popID=input_information[pop]['popName']
            Note_string=Note_string+"Input group parameters for %s:"%popID+"\n" 
            for pop_in in range(0,len(cell_array)):
                if cell_array[pop_in]['popID']==popID:
                   pop_listIndex=pop_in
                   popSize=cell_array[pop_in]['size']
            input_group_array=input_information[pop]['inputGroups']
            for input_group in range(0,len(input_group_array)):
                if input_group_array[input_group]['inputModel']=='XF':
                   label=input_group_array[input_group]['inputLabel']
                   synapse_list=input_group_array[input_group]['synapseList']
                   if input_group_array[input_group]['colocalizeSynapses']:
                      if input_group_array[input_group]['numberModel']=="constant number of inputs per cell":
                          no_of_inputs=input_group_array[input_group]['noInputs']
                      if input_group_array[input_group]['numberModel']=="variable number of inputs per cell":
                         if input_group_array[input_group]['distribution']=="binomial":
                            no_of_inputs=input_group_array[input_group]['maxNoInputs']
                         ### other options can be added
                      LibrarySize=int(round(popSize*library_params['libraryScale']*no_of_inputs))
                      Input_Golgi_pop=neuroml.Population(id="%s_%s_syn0"%(label,popID), size=LibrarySize,component='iaf0')
                      PopID_array.append("%s_%s_syn0"%(label,popID))
                      net.populations.append(Input_Golgi_pop)
                      if input_group_array[input_group]['synapseMode']=="persistent":
                         poisson_syn=neuroml.PoissonFiringSynapse(id="%s_%s_syn0one"%(label,popID),\
                         average_rate="%f per_s"%input_group_array[input_group]['averageRate'],\
                         synapse="syn0",spike_target="./syn0")
                         nml_doc.poisson_firing_synapses.append(poisson_syn)
           
   
                      if input_group_array[input_group]['synapseMode']=="transient":
                         poisson_syn=neuroml.TransientPoissonFiringSynapse(id="%s_%s_syn0one"%(label,popID),\
                         average_rate="%f per_s"%input_group_array[input_group]['averageRate'],\
                         synapse="syn0" ,\
                         spike_target="./syn0",\
                         delay="%f%s"%(input_group_array[input_group]['delay'],input_group_array[input_group]['units']),\
                         duration="%f%s"%(input_group_array[input_group]['duration'],input_group_array[input_group]['units'] )  )
                         nml_doc.transient_poisson_firing_synapses.append(poisson_syn) 
                                                            
                      Poisson_syn_id_array.append("%s_%s_syn0one"%(label,popID))
                      input_list =neuroml.InputList(id="List%s_%s_syn0one"%(label,popID),component=poisson_syn.id,populations=Input_Golgi_pop.id)
                      count=0
                      target_no_array.append(LibrarySize)
                      for target_point in range(0,no_of_inputs*popSize):                     
                          syn_input = neuroml.Input(id="%d"%(count),target="../%s_%s_syn0[%i]"%(label,popID,target_point),destination="synapses") 
                          input_list.input.append(syn_input)
                          count=count+1
                      net.input_lists.append(input_list)

                   else:
                     for synapse_index in range(0,len(synapse_list)):                
                         synapse_array=synapse_list[synapse_index]
                         synapse_name=synapse_array['synapseType']
                         if synapse_array['numberModel']=="constant number of inputs per cell":
                            no_of_inputs=synapse_array['noInputs']
                         if synapse_array['numberModel']=="variable number of inputs per cell":
                            if synapse_array['distribution']=="binomial":
                               no_of_inputs=synapse_array['maxNoInputs']
                            ### other options can be added
                         LibrarySize=int(round(popSize*library_params['libraryScale']*no_of_inputs))
                         Input_Golgi_pop=neuroml.Population(id="%s_%s_syn%d"%(label,popID,synapse_index), size=LibrarySize,
		                  component='iaf0')
                         PopID_array.append("%s_%s_syn%d"%(label,popID,synapse_index))
                         net.populations.append(Input_Golgi_pop)
                         if synapse_array['synapseMode']=="persistent":
                            poisson_syn=neuroml.PoissonFiringSynapse(id="%s_%s_%s_syn%d"%(label,synapse_name,popID,synapse_index),\
                            average_rate="%f per_s"%synapse_array['averageRate'],\
                            synapse="syn0",spike_target="./syn0")
                            nml_doc.poisson_firing_synapses.append(poisson_syn)
           
   
                         if synapse_array['synapseMode']=="transient":
                            poisson_syn=neuroml.TransientPoissonFiringSynapse(id="%s_%s_%s_syn%d"%(label,synapse_name,popID,synapse_index),\
                            average_rate="%f per_s"%synapse_array['averageRate'],\
                            synapse="syn0" ,\
                            spike_target="./syn0",\
                            delay="%f%s"%(synapse_array['delay'],synapse_array['units']),\
                            duration="%f%s"%(synapse_array['duration'],synapse_array['units'] )  )
                            nml_doc.transient_poisson_firing_synapses.append(poisson_syn) 
                                                            
                         Poisson_syn_id_array.append("%s_%s_%s_syn%d"%(label,synapse_name,popID,synapse_index))
                         input_list =neuroml.InputList(id="List_%s_%s_%s_syn%d"%(label,synapse_name,popID,synapse_index),component=poisson_syn.id,populations=Input_Golgi_pop.id)
                         count=0
                         target_no_array.append(LibrarySize)
                         for target_point in range(0,no_of_inputs*popSize):                     
                             syn_input = neuroml.Input(id="%d"%(count),target="../%s_%s_syn%d[%i]"%(label,popID,synapse_index,target_point),destination="synapses") 
                             input_list.input.append(syn_input)
                             count=count+1
                         net.input_lists.append(input_list)

        

        
        if simulation_parameters['parentDirRequired']:

           if 'networkDir' in simulation_parameters:
               if  simulation_parameters['networkDir']=="example":
                   nml_file_dir =simulation_parameters['parentDir']+"/NeuroML2/NML2_LEMS_Net_Examples/"+simulation_parameters['experimentID']+"/"+"sim%d"%simulation_parameters['simID']+"/"+'%s.net.nml'%ref
                   path=simulation_parameters['parentDir']+"/NeuroML2/NML2_LEMS_Net_Examples/"+simulation_parameters['experimentID']+"/"+"sim%d"%simulation_parameters['simID']
               if simulation_parameters['networkDir']=="experiment":
                  nml_file_dir =simulation_parameters['parentDir']+"/NeuroML2/NML2_LEMS_Experiments/"+simulation_parameters['experimentID']+"/"+"sim%d"%simulation_parameters['simID']+"/"+'%s.net.nml'%ref
                  path=simulation_parameters['parentDir']+"/NeuroML2/NML2_LEMS_Experiments/"+simulation_parameters['experimentID']+"/"+"sim%d"%simulation_parameters['simID']

        

               if not os.path.exists(path):
                  os.makedirs(path)
        else:
           nml_file_dir ='%s.net.nml'%ref
        
        writers.NeuroMLWriter.write(nml_doc,nml_file_dir)


        nml_file='%s.net.nml'%ref

        print("Written network file to: "+nml_file_dir)
    
        ###### Validate the NeuroML2 ######   

        validate_neuroml2(nml_file_dir)
        
        sim_info_array={}
        sim_info_array['ref']=ref
        sim_info_array['netID']=net.id
        sim_info_array['simParams']=simulation_parameters
        sim_info_array['nmlFile']=nml_file
        sim_info_array['nmlPath']=path
        sim_info_array['libraryParams']=library_params
       
        cell_info_array={}
        cell_info_array['popParams']=cell_array
        cell_info_array['popIDarray']=PopID_array
        cell_info_array['targetNoarray']=target_no_array
        cell_info_array['PoissonSynIdarray']=Poisson_syn_id_array
        
        
        return sim_info_array, cell_info_array



def generate_input_library(sim_array,pop_array):
        ref= sim_array['ref']
        net_id=sim_array['netID']
        simulation_parameters=sim_array['simParams']
        nml_file=sim_array['nmlFile']
        path=sim_array['nmlPath']
        library_params=sim_array['libraryParams']
        cell_array=pop_array['popParams']
        popIDarray=pop_array['popIDarray']
        targetNoarray=pop_array['targetNoarray']
        PoissonSynIDarray=pop_array['PoissonSynIdarray']
       
        # Create a LEMSSimulation to manage creation of LEMS file

        ls = LEMSSimulation(ref, simulation_parameters['duration'], simulation_parameters['timeStep'])
        
        # Point to network as target of simulation
    
        ls.assign_simulation_target(net_id)
        
        ls.include_neuroml2_file(nml_file,True,path)
        
        

        # Specify Displays and Output Files
	for x in range(0,len(popIDarray)):
	    for i in range(targetNoarray[x]):
		quantity = "%s[%i]/%s"%(popIDarray[x], i,PoissonSynIDarray[x])
                of0 = "eventFile%d%d"%(x,i)
                of1="0"
                if simulation_parameters['currentDirRequired']:
                   ls.create_event_output_file(of0,simulation_parameters['currentDir']+"/simulations/%s/sim%d/%s_PoissonTrain_%d.dat"%(simulation_parameters['experimentID'],simulation_parameters['simID'],\
                                                                               popIDarray[x],i))
                else:
                   ls.create_event_output_file(of0,"simulations/%s/sim%d/%s_PoissonTrain_%d.dat"%(simulation_parameters['experimentID'],simulation_parameters['simID'],\
                                                                                popIDarray[x],i))
		ls.add_selection_to_event_output_file(of0,of1,quantity,"spike")
       
	# save LEMS file
        if simulation_parameters['parentDirRequired']:
           if simulation_parameters['networkDir']=="example":
              lems_file_name_dir=simulation_parameters['parentDir']+"/NeuroML2/NML2_LEMS_Net_Examples/"+simulation_parameters['experimentID']+"/"+"sim%d"%simulation_parameters['simID']+"/"+"LEMS_%s.xml"%ref
              lems_file_name = ls.save_to_file(lems_file_name_dir)
              

           if simulation_parameters['networkDir']=="experiment":
              lems_file_name_dir=simulation_parameters['parentDir']+"/NeuroML2/NML2_LEMS_Experiments/"+simulation_parameters['experimentID']+"/"+"sim%d"%simulation_parameters['simID']+"/"+"LEMS_%s.xml"%ref
              lems_file_name = ls.save_to_file(lems_file_name_dir)
        else:
           lems_file_name = ls.save_to_file()
           lems_file_name_dir="LEMS_%s.xml"%ref

        
        if library_params['simulator']=="jNeuroML":
            print("Finished building a network which generates input trains. Starts running a simulation with jNeuroML for %s"%lems_file_name_dir)
	    results1 = pynml.run_lems_with_jneuroml(lems_file_name, nogui=True, load_saved_data=False, plot=False)
            print("Finished running simulations with jNeuroML")
        elif library_params['simulator']=="jNeuroML_NEURON":
             print("Finished building a network which generates input trains. Starts running a simulation with NEURON for %s"%lems_file_name_dir)
             results1 = pynml.run_lems_with_jneuroml_neuron(lems_file_name, nogui=True, load_saved_data=False, plot=False)
             print("Finished running simulations with NEURON.")
        else:
              print("Finished building a network which generates input trains.")

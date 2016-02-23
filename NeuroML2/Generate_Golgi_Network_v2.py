
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

from methods import *



### a main script for generating and running golgi cell network by Rokas Stanislovas (2016)
def generate_golgi_cell_net(ref,cell_array,location_array,connectivity_information,input_information,simulation_parameters):
        
       
        if simulation_parameters['globalSeed']:
           random.seed(12345)
        else:
           if simulation_parameters["trialSeed"]:
              random.seed(simulation_parameters["trialSeedNumber"])
        nml_doc = neuroml.NeuroMLDocument(id=ref)
        #cell_array will have to include cell_types and no_of_cells
        #connectivity_information is a list of lists that will have to include connectivity parameters; now code only for a random configuration with parameters connection_probability and conductance_strength

        
        cell_type_list=[]
        for x in range(0,len(cell_array)):
            cell_type_list.append(cell_array[x]['cellType'])
            
        unique_cell_names=np.unique(cell_type_list)
        for unique_cell in unique_cell_names:
            include_cell=neuroml.IncludeType(href="%s.cell.nml"%unique_cell)
            nml_doc.includes.append(include_cell)

	
	# Create network
	net = neuroml.Network(id=ref+"_network",type="networkWithTemperature",temperature="23 degC")
	nml_doc.networks.append(net)


        Golgi_pop_index_array=[]
        neuroml_Golgi_pop_array=[]

        for x in range(0,len(cell_array)):
	    Golgi_pop = neuroml.Population(id=cell_array[x]['popID'], size =cell_array[x]['size'], type="populationList",
		                  component=cell_array[x]['cellType'])
	    Golgi_pop_index_array.append(cell_array[x]['popID'])
            neuroml_Golgi_pop_array.append(Golgi_pop)
	    net.populations.append(Golgi_pop)

        
        
	cell_position_array={}
	   
        no_density_model=True
        #################    
	if string.lower(location_array['distributionModel'])=="density based":
           ### will override cell numbers in cell_array if specified
           no_density_model=False
           for cell_group in range(0,len(location_array['densityFiles'])):
               ### assuming that Y_values returned by load_density_data represent the depth with zero indicating Purkinje cell level
               cellpopName=location_array['densityFiles'][cell_group]['popID']
               X_array,Y_array,density_values=load_density_data(location_array['densityFiles'][cell_group]['fileName'],location_array['relativePath'])
               dim_X_array=np.shape(X_array)
               dim_Y_array=np.shape(Y_array)
               ## assume meshgrid
               if dim_X_array==dim_Y_array:
                  ## assume that data is not normalized and distribute cells on a density sheet
                  X_max=np.nanmax(X_array)
                  Y_max=np.nanmax(Y_array)
                  X_array=np.divide(X_array,X_max,dtype=float)
                  Y_array=np.divide(Y_array,Y_max,dtype=float)
                  cell_diameter=get_soma_diameter(cell_names[cell_group])
                  if string.lower(localization_type[4])=="minimal distance":
                     if string.lower(localization_type[5])=="uniform":
                        minimal_distance=localization_type[6]
                              
                     if string.lower(localization_type[4])=="random no overlap":
                        cell_diameter=get_soma_diameter(cell_names[cell_group])


  
        if no_density_model:
           ###### if no_density model assumes that dimensions of a cubic environment are specified
           x_dim=location_array['xDim']
           y_dim=location_array['yDim']
           z_dim=location_array['zDim']
           for cell_population in range(0,len(cell_array)):
               cell_position_array[ cell_array[cell_population]['popID'] ]=np.zeros([cell_array[cell_population]['size'],3])
              
        ##############
        if string.lower(location_array['distributionModel'])=="random minimal distance":
           for cell_pop in range(0,len(cell_array)):
               golgi_pop=neuroml_Golgi_pop_array[cell_pop]
               for cell in range(0,cell_array[cell_pop]['size']):
	           Golgi_cell=neuroml.Instance(id="%d"%cell)
	           golgi_pop.instances.append(Golgi_cell)
	           if cell_pop==0 and cell==0:
                      X=random.random()
	              Y=random.random()
	              Z=random.random()
                      cell_position_array[cell_array[cell_pop]['popID']][cell,0]=x_dim*X
                      cell_position_array[cell_array[cell_pop]['popID']][cell,1]=y_dim*Y
                      cell_position_array[cell_array[cell_pop]['popID']][cell,2]=z_dim*Z
                      Golgi_cell.location=neuroml.Location(x=x_dim*X, y=y_dim*Y, z=z_dim*Z)
                      print cell_position_array[cell_array[cell_pop]['popID']][cell,0], cell_position_array[cell_array[cell_pop]['popID']][cell,1],\
 cell_position_array[cell_array[cell_pop]['popID']][cell,2]
                   else:
                      x=0
                      while x==0:
                          overlap_counter=0
                          X=(random.random())*x_dim
	                  Y=(random.random())*y_dim
	                  Z=(random.random())*z_dim
                          for cell_pop_x in range(0,len(cell_array)):
                              pop_cell_positions=cell_position_array[cell_array[cell_pop_x]['popID']]
                              for cell_x in range(0,cell_array[cell_pop_x]['size']):
                                  if cell_position_array[cell_array[cell_pop_x]['popID']][cell_x,0]+cell_position_array[cell_array[cell_pop_x]['popID']][cell_x,1]+cell_position_array[cell_array[cell_pop_x]['popID']][cell_x,2] >0:
                                     if string.lower(location_array['metricMode'])=="uniform":
                                        if distance([X,Y,Z],cell_position_array[cell_array[cell_pop_x]['popID']][cell_x]) < location_array['globalMetric']:
                                           overlap_counter+=1
                                        #if string.lower(location_array['metricMode'])=="cell group specific": might be added in the future
                                              
                          if overlap_counter==0:
                             cell_position_array[cell_array[cell_pop]['popID']][cell,0]=X
                             cell_position_array[cell_array[cell_pop]['popID']][cell,1]=Y
                             cell_position_array[cell_array[cell_pop]['popID']][cell,2]=Z
                             Golgi_cell.location=neuroml.Location(x=X, y=Y, z=Z)
                               
                             print cell_position_array[cell_array[cell_pop]['popID']][cell,0], cell_position_array[cell_array[cell_pop]['popID']][cell,1], cell_position_array[cell_array[cell_pop]['popID']][cell,2]
                             x=1
        ############  random positioning but approximately no overlap between somata                  
        if string.lower(location_array['distributionModel'])=="random no overlap":
           cell_diameter_array={}
           for cell_pop in range(0,len(cell_array)):
               cell_diameter=get_soma_diameter(cell_array[cell_pop]['cellType'])
               cell_diameter_array[cell_array[cell_pop]['popID']]=cell_diameter
           for cell_pop in range(0,len(cell_array)):
               golgi_pop=neuroml_Golgi_pop_array[cell_pop]
               cell_diameter=get_soma_diameter(cell_array[cell_pop]['cellType'])
               for cell in range(0,cell_array[cell_pop]['size']):
	           Golgi_cell=neuroml.Instance(id="%d"%cell)
	           golgi_pop.instances.append(Golgi_cell)
	           if cell_pop==0 and cell==0:
                      X=random.random()
	              Y=random.random()
	              Z=random.random()
                      cell_position_array[cell_array[cell_pop]['popID']][cell,0]=x_dim*X
                      cell_position_array[cell_array[cell_pop]['popID']][cell,1]=y_dim*Y
                      cell_position_array[cell_array[cell_pop]['popID']][cell,2]=z_dim*Z
                      Golgi_cell.location=neuroml.Location(x=x_dim*X, y=y_dim*Y, z=z_dim*Z)
                      print cell_position_array[cell_array[cell_pop]['popID']][cell,0], cell_position_array[cell_array[cell_pop]['popID']][cell,1],\
 cell_position_array[cell_array[cell_pop]['popID']][cell,2]
                   else:
                      x=0
                      while x==0:
                         overlap_counter=0
                         X=(random.random())*x_dim
	                 Y=(random.random())*y_dim
	                 Z=(random.random())*z_dim
                         for cell_pop_x in range(0,len(cell_array)):
                             pop_cell_positions=cell_position_array[cell_array[cell_pop_x]['popID']]
                             for cell_x in range(0,cell_array[cell_pop_x]['size']):
                                 if cell_position_array[cell_array[cell_pop_x]['popID']][cell_x,0]+cell_position_array[cell_array[cell_pop_x]['popID']][cell_x,1]+cell_position_array[cell_array[cell_pop_x]['popID']][cell_x,2] >0:
                                    if distance([X,Y,Z],cell_position_array[cell_array[cell_pop_x]['popID']][cell_x]) < (cell_diameter+cell_diameter_array[cell_array[cell_pop_x]['popID']])/2:
                                       overlap_counter+=1
                         if overlap_counter==0:
                            cell_position_array[cell_array[cell_pop]['popID']][cell,0]=X
                            cell_position_array[cell_array[cell_pop]['popID']][cell,1]=Y
                            cell_position_array[cell_array[cell_pop]['popID']][cell,2]=Z
                            Golgi_cell.location=neuroml.Location(x=X, y=Y, z=Z)
                               
                            print cell_position_array[cell_array[cell_pop]['popID']][cell,0], cell_position_array[cell_array[cell_pop]['popID']][cell,1], cell_position_array[cell_array[cell_pop]['popID']][cell,2]
                            x=1

        ###### simply random positioning in a cubic environment               
        if string.lower(location_array['distributionModel'])=="random":
           for cell_pop in range(0,len(cell_array)):
               golgi_pop=neuroml_Golgi_pop_array[cell_pop]
               for cell in range(0,cell_array[cell_pop]['size']):
	           Golgi_cell=neuroml.Instance(id="%d"%cell)
	           golgi_pop.instances.append(Golgi_cell)
	           X=random.random()
	           Y=random.random()
	           Z=random.random()
                   cell_position_array[cell_array[cell_pop]['popID']][cell,0]=x_dim*X
                   cell_position_array[cell_array[cell_pop]['popID']][cell,1]=y_dim*Y
                   cell_position_array[cell_array[cell_pop]['popID']][cell,2]=z_dim*Z
                   Golgi_cell.location=neuroml.Location(x=x_dim*X, y=y_dim*Y, z=z_dim*Z)
                   print cell_position_array[cell_array[cell_pop]['popID']][cell,0], cell_position_array[cell_array[cell_pop]['popID']][cell,1], cell_position_array[cell_array[cell_pop]['popID']][cell,2]
                 
        connMatrix_array=[]
        gap_counter=0
        initial_projection_counter=0
        synapse_counter=0
        for pair in range(0,len(connectivity_information['populationPairs']) ):
            prePop=connectivity_information['populationPairs'][pair]['prePopID'])  
            postPop=connectivity_information['populationPairs'][pair]['postPopID'])
            for pop in range(0,len(cell_array)):
                if cell_array[pop]['popID']==prePop
                   prePop_listIndex=pop
                   prePopSize=cell_array[pop]['size']
                if cell_array[pop]['popID']==postPop:
                   postPop_listIndex=pop
                   postPopSize=cell_array[pop]['size']
            ########## 2012 publication-based generation of model connectivity 
            if connectivity_information['populationPairs'][pair]['connModel']=="Vervaeke_2012_based" or connectivity_information['populationPairs'][pair]['connModel']=="explicit_connection_probabilities":

               proj, nonempty_projection, gap_counter,gap_junction_array=Vervaeke_2012_AND_explicit_conn_prob_model(pair,initial_projection_counter,gap_counter,prePop,prePop_listIndex,prePopSize,\
                                                postPop,postPop_listIndex,postPopSize,cell_array,connectivity_information,cell_position_array)
                
               if nonempty_projection:
                  initial_projection_counter+=1
                  net.electrical_projections.append(proj)
                  for gapJ in range(0,len(gap_junction_array)):
                      nml_doc.gap_junctions.append(gap_junction_array[gapJ])
               

            #############                     
            if connectivity_information['populationPairs'][pair]['connModel']=="Vervaeke_2010_based":

               proj, nonempty_projection, gap_counter,gap_junction_array=Vervaeke_2010_model(pair,initial_projection_counter,gap_counter,prePop,prePop_listIndex,prePopSize,\
                                                postPop,postPop_listIndex,postPopSize,cell_array,connectivity_information,cell_position_array)


               if nonempty_projection:
                  initial_projection_counter+=1
                  net.electrical_projections.append(proj)
                  for gapJ in range(0,len(gap_junction_array)):
                      nml_doc.gap_junctions.append(gap_junction_array[gapJ])

                      
           if 
            
                                                     
        ####################                                                                   
        # use below as a template : 
        # input_information=[["MF",[pop0_array,pop1_array,pop2_array]],["PF",[pop0_array,pop1_array,pop2_array]]]
        # all pop_arrays have to be of the following form:
        # first_array=["uniform" or "3D region specific", if "uniform" fraction to target, if "3D region specific",[[40,80],[40,80],[40,80]]],all or random frac
        # pop0_array=[pop_index,first_array,synapse_array_per_pop,[[synapse average_rate_list]]["constant number of inputs per cell" or "variable number of inputs per cell"
        # if variable then "binomial",average_no_of_inputs,max_no_of_inputs    ]   then
        # for each different synapse     "segment groups and segments",[["Section_1","dend_1"],[0.7,0.3]]
        # "segments and subsegments"
        # [["Section_1"],[1],[ [   [0.25,0.2],[0.25,0.4],[0.25,0.4],[0.25,0]  ]         ]             ]          (note nesting  - four brackets at the end)
        #make InputList for MF and PF synapses
        synapse_name_array=[]
        for pop in range(0,len(input_information)):
            popID=input_information[pop]['popName']
            for pop in range(0,len(cell_array)):
                if cell_array[pop]['popID']==popID:
                   pop_listIndex=pop
                   popSize=cell_array[pop]['size']
            input_group_array=input_information[pop]['inputGroups']
            for input_group in range(0,len(input_group_array)):
                if input_group_array[input_group]['inputModel']=='XF':
                                                                        
                   fraction_to_target_per_pop=input_group_array[input_group]['fractionToTarget']
                                                                        
                   if input_group_array[input_group]['targetingRegime']=="uniform":
                      
                      target_cells=random.sample(range(popSize),int(round(fraction_to_target_per_pop*popSize)   )   )
                                                                        
                   if input_group_array[input_group]['targetingRegime']=="3D region specific":
                      cell_positions=cell_position_array[popID]
                      dim_array=np.shape(cell_positions)
                      region_specific_targets_per_cell_group=[]
                      for region in range(1,len(which_cells_to_target_array[1])):
                          for cell in range(0,dim_array[0]):
                              if (which_cells_to_target_array[1][region][0][0] <  cell_positions[cell,0]) and (cell_positions[cell,0] < which_cells_to_target_array[1][region][0][1]):
                                  if (which_cells_to_target_array[1][region][1][0] <  cell_positions[cell,1]) and (cell_positions[cell,1] <which_cells_to_target_array[1][region][1][1]) :
                                     if (which_cells_to_target_array[1][region][2][0] <  cell_positions[cell,2]) and (cell_positions[cell,2] < which_cells_to_target_array[1][region][2][1]):
                                        region_specific_targets_per_cell_group.append(cell)
                                                                        
                      target_cells=random.sample(region_specific_targets_per_cell_group,\
                                                int(round(fraction_to_target_per_pop*len(region_specific_targets_per_cell_group))))
                                                                        
                   inp_group_specifier=input_group_array[input_group]['inputLabel']
                   synapse_list=input_group_array[input_group]['synapseList']
                   for synapse_index in range(0,len(synapse_list)):
                       synapse_name_array.append(synapse_list[synapse_index]['synapseType'])
                                                        
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
                                  
                       nml_doc.poisson_firing_synapses.append(poisson_syn)

                       input_list =neuroml.InputList(id="Input%s_%s_syn%d"%(inp_group_specifier,popID,synapse_index),\
                       component=poisson_syn.id,populations="%s"%popID)

                       net.input_lists.append(input_list)
                                                                        
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

                                  
        
	        ###### implementing physiological heterogeneity between cells with variations in a basal firing rate
                if input_group_array[input_group]['inputModel']=="variable_basal_firing_rate":
                   offset_units=input_group_array[input_group]['offsetUnits']
                   units=input_group_array[input_group]['ampUnits']
                   label=input_group_array[input_group]['inputLabel']
                   for cell in range(0,popSize):
                       if "gaussian"==input_group_array[input_group]["amplitudeDistribution"]:
                          amp=random.gauss(input_group_array[input_group]['averageAmp'],input_group_array[input_group]['stDevAmp'])
                       if "uniform"==input_group_array[input_group]["amplitudeDistribution"]:
                          amp=random.uniform(input_group_array[input_group]['leftAmpBound'],input_group_array[input_group]['rightAmpBound'])
                       if "constant"==input_group_array[input_group]["amplitudeDistribution"]:
                          amp=input_group_array[input_group]['valueAmp']
                       if "gaussian"==input_group_array[input_group]["offsetDistribution"]:
                          offset=random.gauss(input_group_array[input_group]['averageOffset'],input_group_array[input_group]['stDevOffset'])
                       if offset_uniform_model:
                          offset=random.uniform(pop_offset_left_bound[pop],pop_offset_right_bound[pop])
                       if "constant"==input_group_array[input_group]["offsetDistribution"]:
                          offset=input_group_array[input_group]["valueOffset"]
                       Pulse_generator_variable=neuroml.PulseGenerator(id="%s_%d"%(label,cell),delay="%f%s"%(offset,offset_units),\
                                duration="%f%s"%((simulation_parameters[0]-offset),offset_units),amplitude="%f%s"%(amp,units))
	               nml_doc.pulse_generators.append(Pulse_generator_variable)
	               Input_list=neuroml.InputList(id="Input_%s%d"%(label,cell),component="%s_%d"%(label,cell),populations="%s"%popID)
	               net.input_lists.append(Input_list)
	               Inp = neuroml.Input(target="../%s/%d/%s"%(popID,cell,cell_array[pop_listIndex]['cellType']),id="%d"%cell,destination="synapses")
	               Input_list.input.append(Inp)
	                  
	        ##############
                if input_group_array[input_group]['inputModel']=="testing":
                   label=input_group_array[input_group]['inputLabel']
                   amp_units=input_group_array[input_group]['ampUnits']
                   time_units=input_group_array[input_group]['timeUnit']
                   randomly_select_target_cells=random.sample(range(popSize),int(round(input_group_array[input_group]['cellFractionToTarget'])))
                   for pulse_x in range(0,len(input_group_array[input_group]['pulseParameters'])):
                       Pulse_generator_x=neuroml.PulseGenerator(id="Input_%s_%d"%(label,pulse_x),\
                       delay="%f%s"%(input_group_array[input_group]['pulseParameters'][pulse_x]['delay'],time_units),\
                       duration="%f%s"%(input_group_array[input_group]['pulseParameters'][pulse_x]['duration'],time_units),\
                       amplitude="%f%s"%(input_group_array[input_group]['pulseParameters'][pulse_x]['amplitude'],amp_units))
	               nml_doc.pulse_generators.append(Pulse_generator_x)
                                                         
                       Input_list=neuroml.InputList(id="Input_list%d"%pulse_x, component="Input_%s_%d"%(label,pulse_x),populations="%s"%popID)
                       neuroml_input_array.append(Input_list)
                       net.input_lists.append(Input_list)
                       for i in randomly_select_target_cells:
                           Inp = neuroml.Input(target="../%s/%d/%s"%(popID,i,cell_array[pop_listIndex]['cellType']),id="%d"%i,destination="synapses")
                           input_list.input.append(Inp)
                      

        ##############       
	unique_synapse_names=np.unique(synapse_name_array)
        for unique_synapse in unique_synapse_names:
            include_synapse=neuroml.IncludeType(href="%s.synapse.nml"%unique_synapse)
            nml_doc.includes.append(include_synapse)
                                                 
  
        nml_file = '%s.net.nml'%ref

       

        writers.NeuroMLWriter.write(nml_doc,nml_file)

        print("Written network file to: "+nml_file)
    
        ###### Validate the NeuroML2 ######   

        validate_neuroml2(nml_file)

        sim_info_array=[]
        sim_info_array.append(ref)
        sim_info_array.append(net.id)
        sim_info_array.append(simulation_parameters)
        sim_info_array.append(nml_file)

        cell_info_array=[]
        cell_info_array.append(population_type)
        cell_info_array.append(cell_array)
        cell_info_array.append(Golgi_pop_index_array)
        cell_info_array.append(cell_position_array)
        
        return sim_info_array, cell_info_array

def generate_LEMS_and_run(sim_array,pop_array):
        ref=sim_array[0]
        net_id=sim_array[1]
        simulation_parameters=sim_array[2]
        nml_file=sim_array[3]

        population_type=pop_array[0]
        cell_array=pop_array[1]
        Golgi_pop_index_array=pop_array[2]
        
        # Create a LEMSSimulation to manage creation of LEMS file

        ls = LEMSSimulation(ref, simulation_parameters[0], simulation_parameters[1])

        # Point to network as target of simulation
    
        ls.assign_simulation_target(net_id)

        ls.include_neuroml2_file(nml_file)
        
        

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
                   ls.create_output_file(of0, "simulations/%s/sim%d/%s_cell%d.dat"%(simulation_parameters['experimentID'],simulation_parameters['simID'],\
                                                                                    cell_array[x]['popID'],i))
		   ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
					   
	    else:
	       randomly_select_displayed_cells=random.sample(range(cell_array[x]['size']),max_traces)
	       for y in randomly_select_displayed_cells:
                   quantity = "%s/%i/%s/v"%(cell_array[x]['popID'], y, cell_array[x]['cellType'])
		   ls.add_line_to_display(disp, "../%s/%i: Vm"%(cell_array[x]['popID'],y), quantity, "1mV", pynml.get_next_hex_color())
					      
		  for i in range(cell_array[x+1][1]):
		      quantity = "%s/%i/%s/v"%(cell_array[x]['popID'], i,cell_array[x]['cellType'])
                      of0 = 'Volts%d_file0_%d'%(x,i)
                      ls.create_output_file(of0, "simulations/%s/sim%d/%s_cell%d.dat"%(simulation_parameters['experimentID'],\
                      simulation_parameters['simID'],x,i))
		      ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
       
	# save LEMS file
        lems_file_name = ls.save_to_file()
        if simulation_parameters['plotSpecifier']:
           if simulation_parameters['simulator']=="jNeuroML":
	      results1 = pynml.run_lems_with_jneuroml(lems_file_name, nogui=True, load_saved_data=True, plot=True)
              print("Finished building network and running simulation with jNeuroML")
           elif simulation_parameters['simulator']=="jNeuroML_NEURON":
              results1 = pynml.run_lems_with_jneuroml_neuron(lems_file_name, nogui=True, load_saved_data=True, plot=True)
              print("Finished building a network and running simulation with jNeuroML_NEURON")
           else:
              print("Finished building a network")
        else:
           if simulation_parameters['simulator']=="jNeuroML":
	      results1 = pynml.run_lems_with_jneuroml(lems_file_name, nogui=True, load_saved_data=False, plot=False)
              print("Finished building a network and running simulation with jNeuroML")
           elif simulation_parameters['simulator']=="jNeuroML_NEURON":
              results1 = pynml.run_lems_with_jneuroml_neuron(lems_file_name, nogui=True, load_saved_data=False, plot=False)
              print("Finished building a network and running simulation with jNeuroML_NEURON")
           else:
              print("Finished building a network")
         

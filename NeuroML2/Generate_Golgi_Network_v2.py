
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
         ##### below lines to make a reference template for the density based model:
    #   net_params_test_2010_multiple['experiment1']['distributionParams']={}
    #   net_params_test_2010_multiple['experiment1']['distributionParams']['distributionModel']="density based"
    #   net_params_test_2010_multiple['experiment1']['distributionParams']['populationList']=[]
    #   net_params_test_2010_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Golgi_pop0','densityFilePath':'/home/rokas/Golgi_data/GlyT2 density matrix of shape 35 152.txt',\
    #   'planeDimensions':{'dim1':'x','dim2':'z'},'dim1CoordinateVector':[1300,1500],'dim2CoordinateVector':[0,50],'distanceModel':'minimal_distance',\
    #   'minimalDistance':25})
    #   net_params_test_2010_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Golgi_pop1','densityFilePath':'/home/rokas/Golgi_data/GlyT2 density matrix of shape 35 152.txt',\
    #   'planeDimensions':{'dim1':'x','dim2':'z'},'dim1CoordinateVector':[1300,1500],'dim2CoordinateVector':[0,50],'dim3':'y','dim3Boundary':200,\
    #   'distanceModel':'minimal_distance/random/random_no_overlap','minimalDistance':25,'canonicalVolumeBaseArea':54})  
	if string.lower(location_array['distributionModel'])=="density based":
           ### will override cell numbers in cell_array if specified
           no_density_model=False
           for cell_group in range(0,len(location_array['populationList'])):
               total_no_of_cells=0
               cellPopName=location_array['populationList'][cell_group]['popID']
               for pop in range(0,len(cell_array)):
                   if cellPopName==cell_array[pop]['popID']:
                      cell_type_name=cell_array[pop]['cellType']
                      pop_index_popParams=pop
               ### assuming that Y_values returned by load_density_data represent the depth with zero indicating Purkinje cell level
               X_array,Y_array,density_values=load_density_data(location_array['populationList'][cell_group]['densityFilePath'])
               dim_X_array=np.shape(X_array)
               dim_Y_array=np.shape(Y_array)
               ## assume meshgrid
               if dim_X_array==dim_Y_array:
                  ## assume that data is not normalized and distribute cells on a specific region on a density sheet
                  X_max=np.nanmax(X_array)
                  Y_max=np.nanmax(Y_array)
                  X_vector=X_array[0]
                  Y_vector=Y_array[0]
                  left_x_index=None
                  right_x_index=None
                  low_y_index=None
                  high_y_index=None

                  left_x_found=False
                  right_x_found=False
                  low_y_found=False
                  high_y_found=False
                  for X_value in range(0,len(X_vector)):
                      if left_x_found==False:
                         if X_vector[X_value] > location_array['populationList'][cell_group]['dim1CoordinateVector'][0]:
                            left_x_index=X_value
                            left_x_found=True
                      if right_x_found==False:
                         if X_vector[X_value] > location_array['populationList'][cell_group]['dim1CoordinateVector'][1]:
                            right_x_index=X_value-1
                  for Y_value in range(0,len(Y_vector)):
                      if low_y_found==False: 
                         if Y_vector[Y_value] > location_array['populationList'][cell_group]['dim2CoordinateVector'][0]:
                            low_y_index=Y_value
                            low_y_found=True
                      if high_y_found==False:
                         if Y_vector[Y_value] > location_array['populationList'][cell_group]['dim2CoordinateVector'][1]:
                            high_y_index=Y_value-1
                            high_y_found=True
                  if left_x_found and right_x_found and low_y_found and high_y_found:
                     X_index_array=range(left_x_index,right_x_index+1)
                     Y_index_array=range(low_y_index,high_y_index+1)
                     cell_diameter=get_soma_diameter(cell_type_name)
                     ##### assume that discrete density sheet is in mmm3. thus convert cell_diameter and dim3 to mm:
                     dim3Boundary=location_array['populationList'][cell_group]['dim3Boundary']/1000
                     ### find density points that fall within a region specified by 'dim1CoordinateVector' and 'dim2CoordinateVector'
                     
                     
                     base_area=location_array['populationList'][cell_group]['canonicalVolumeBaseArea']
                     canonical_volume=math.pi*((base_area/2)**2)*dim3Boundary
                        
                     for X_index in range(0,len(X_index_array)):
                         for Y_index in range(0,len(Y_index_array)):
                             density_value=density_values[X_index_array[X_index],Y_index_array[Y_index]]
                             no_of_cells_per_density_point=density_value*canonical_volume
                             total_no_of_cells=total_no_of_cells+no_of_cells_per_density_point
                             X_square_centre=X_array[X_index_array[X_index],Y_index_array[Y_index]]
                             Y_square_centre=Y_array[X_index_array[X_index],Y_index_array[Y_index]]
                             X_left_corner=X_square_centre-(math.sqrt(base_area)/2)
                             Y_left_corner=Y_square_centre-(math.sqrt(base_area)/2)
                             if location_array['populationList'][cell_group]['distanceModel']=="minimal_distance":
                     
                              
                             if location_array['populationList'][cell_group]['distanceModel']=="random_no_overlap":

                             if location_array['populationList'][cell_group]['distanceModel']=="random":
                                for cell in range(0,no_of_cells_per_density_point):
	                            Golgi_cell=neuroml.Instance(id="%d"%cell)
	                            golgi_pop.instances.append(Golgi_cell)
	                            X=random.random()
	                            Y=random.random()
	                            Z=random.random()
	                            
	                            if location_array['populationList'][cell_group]['planeDimensions']['dim1']=='x' and location_array['populationList'][cell_group]['planeDimensions']['dim2']!='x':
                                       cell_position_array[cell_array[pop_index_popParams]['popID']][cell,0]=X_left_corner*X
                                       
                                    if location_array['populationList'][cell_group]['planeDimensions']['dim1']=='y' and location_array['populationList'][cell_group]['planeDimensions']['dim2']!='y':
                                       cell_position_array[cell_array[pop_index_popParams]['popID']][cell,1]=X_left_corner*X
                                       
                                    if location_array['populationList'][cell_group]['planeDimensions']['dim1']=='z' and location_array['populationList'][cell_group]['planeDimensions']['dim2']!='z':

                                       cell_position_array[cell_array[pop_index_popParams]['popID']][cell,2]=X_left_corner*X
                                       
                                    if location_array['populationList'][cell_group]['planeDimensions']['dim2']=='x' and location_array['populationList'][cell_group]['planeDimensions']['dim1']!='x':
                                       cell_position_array[cell_array[pop_index_popParams]['popID']][cell,0]=Y_left_corner*Y
                                    if location_array['populationList'][cell_group]['planeDimensions']['dim2']=='y' and location_array['populationList'][cell_group]['planeDimensions']['dim1']!='y':
                                       cell_position_array[cell_array[pop_index_popParams]['popID']][cell,1]=Y_left_corner*Y
                                    if location_array['populationList'][cell_group]['planeDimensions']['dim2']=='z' and location_array['populationList'][cell_group]['planeDimensions']['dim1']!='z':
                                       cell_position_array[cell_array[pop_index_popParams]['popID']][cell,2]=Y_left_corner*Y
                                       
                                    if location_array['populationList'][cell_group]['dim3']=='z' and location_array['populationList'][cell_group]['planeDimensions']['dim2'] !='z'\
                                       and location_array['populationList'][cell_group]['planeDimensions']['dim1'] !='z':
                                       cell_position_array[cell_array[pop_index_popParams]['popID']][cell,2]=dim3Boundary*Z
                                    if location_array['populationList'][cell_group]['dim3']=='y' and location_array['populationList'][cell_group]['planeDimensions']['dim2'] !='y'\
                                       and location_array['populationList'][cell_group]['planeDimensions']['dim1'] !='y':
                                       cell_position_array[cell_array[pop_index_popParams]['popID']][cell,1]=dim3Boundary*Z
                                    if location_array['populationList'][cell_group]['dim3']=='x' and location_array['populationList'][cell_group]['planeDimensions']['dim2'] !='x'\
                                       and location_array['populationList'][cell_group]['planeDimensions']['dim1'] !='x':
                                       cell_position_array[cell_array[pop_index_popParams]['popID']][cell,0]=dim3Boundary*Z
                                    Golgi_cell.location=neuroml.Location(x=X_left_corner*X, y=Y_left_corner*Y, z=dim3Boundary*Z)
                                    print cell_position_array[cell_array[pop_index_popParams]['popID']][cell,0],\
                                          cell_position_array[cell_array[pop_index_popParams]['popID']][cell,1],\
                                          cell_position_array[cell_array[pop_index_popParams]['popID']][cell,2]
                                                                                                                          
                     ### override any specified value of population Size
                                                                                                                          
                     cell_array[pop_index_popParams]['size']=total_no_of_cells
                     


  
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

        synapse_name_array=[]        
        connMatrix_array=[]
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
            
            if 'electricalConnModel' in connectivity_information['populationPairs'][pair]:
               ########## 2012 publication-based generation of model connectivity 
               if connectivity_information['populationPairs'][pair]['electricalConnModel']=="Vervaeke_2012_based" or connectivity_information['populationPairs'][pair]['connModel']=="explicit_connection_probabilities":
                  pair_connectivity_parameters=connectivity_information['populationPairs'][pair]
                  pre_pop_cell_component=cell_array[prePop_listIndex]['cellType']
                  post_pop_cell_component=cell_array[postPop_listIndex]['cellType']
                  pre_pop_cell_positions=cell_position_array[prePop]
                  post_pop_cell_positions=cell_position_array[postPop]

                  proj, nonempty_projection,gap_junction_array=Vervaeke_2012_AND_explicit_conn_prob_model(pair,initial_projection_counter,prePop,prePop_listIndex,prePopSize,pre_pop_cell_component,pre_pop_cell_positions,\
                                postPop,postPop_listIndex,postPopSize,post_pop_cell_component,post_pop_cell_positions,pair_connectivity_parameters)
                
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

                  proj, nonempty_projection,gap_junction_array=Vervaeke_2010_model(pair,initial_projection_counter,prePop,prePop_listIndex,prePopSize,pre_pop_cell_component,pre_pop_cell_positions,\
                                postPop,postPop_listIndex,postPopSize,post_pop_cell_component,post_pop_cell_positions,pair_connectivity_parameters)

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

               proj, nonempty_projection,gap_junction_array,synapse_name=chemical_connection_model(pair,initial_projection_counter,prePop,prePop_listIndex,prePopSize,pre_pop_cell_component,pre_pop_cell_positions,\
                                postPop,postPop_listIndex,postPopSize,post_pop_cell_component,post_pop_cell_positions,pair_connectivity_parameters)

               synapse_name_array.append(synapse_name)
               if nonempty_projection:
                  initial_projection_counter+=1
                  net.electrical_projections.append(proj)
                  for gapJ in range(0,len(gap_junction_array)):
                      nml_doc.gap_junctions.append(gap_junction_array[gapJ])
            
                                                     
        ####################                                                                   
        
        for pop in range(0,len(input_information)):
            popID=input_information[pop]['popName']
            for pop in range(0,len(cell_array)):
                if cell_array[pop]['popID']==popID:
                   pop_listIndex=pop
                   popSize=cell_array[pop]['size']
            input_group_array=input_information[pop]['inputGroups']
            cellType=cell_array[pop_listIndex]['cellType']
            for input_group in range(0,len(input_group_array)):
                if input_group_array[input_group]['inputModel']=='XF' and input_group_array[input_group]['targetingRegime']=="uniform":

                   input_list,poisson_synapse_array,synapse_name_list=XF_input_model_uniform(popID,popSize,cellType,input_group_array[input_group])                                          
                   fraction_to_target_per_pop=input_group_array[input_group]['fractionToTarget']

                   synapse_name_array.extend(synapse_name_list)

                   net.input_lists.append(input_list)

                   for poisson_syn in range(0,len(poisson_synapse_array)):
          
                       nml_doc.poisson_firing_synapses.append(poisson_synapse_array[poisson_syn])

                if input_group_array[input_group]['inputModel']=='XF' and input_group_array[input_group]['targetingRegime']=="3D region specific":

                   input_list,poisson_synapse_array,synapse_name_list=XF_input_model_3D_region_specific(popID,cellType,input_group_array[input_group],\
                   cell_position_array[popID])                                          
                   fraction_to_target_per_pop=input_group_array[input_group]['fractionToTarget']

                   synapse_name_array.extend(synapse_name_list)

                   net.input_lists.append(input_list)

                   for poisson_syn in range(0,len(poisson_synapse_array)):
          
                       nml_doc.poisson_firing_synapses.append(poisson_synapse_array[poisson_syn])                
        
	        ###### implementing physiological heterogeneity between cells with variations in a basal firing rate
                if input_group_array[input_group]['inputModel']=="variable_basal_firing_rate":

                   input_list_array,pulseGenerator_array=variable_basal_firing_rate(popID,popSize,cellType,input_group_array[input_group],\
                   simulation_parameters['duration'])                                          

                   for input_list in range(0,len(input_list_array)):
          
                       net.input_lists.append(input_list_array[input_list])
                       nml_doc.pulse_generators.append(pulseGenerator_array[input_list])
                   
	               
	        ##############
                if input_group_array[input_group]['inputModel']=="testing":

                   input_list_array,pulseGenerator_array=testing(popID,popSize,cellType,input_group_array[input_group],\
                   simulation_parameters['duration'])                                          

                   for input_list in range(0,len(input_list_array)):
          
                       net.input_lists.append(input_list_array[input_list])
                       nml_doc.pulse_generators.append(pulseGenerator_array[input_list])

                
                      

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
         

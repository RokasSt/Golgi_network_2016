
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
def generate_golgi_cell_net(ref,cell_array,location_array, connectivity_information,input_information,simulation_parameters,population_type,output):
        
        if string.lower(simulation_parameters[5][0])=="seed":
           if simulation_parameters[5][1]==True:
              random.seed(12345)
              
        nml_doc = neuroml.NeuroMLDocument(id=ref)
        #cell_array will have to include cell_types and no_of_cells
        #connectivity_information is a list of lists that will have to include connectivity parameters; now code only for a random configuration with parameters connection_probability and conductance_strength

        cell_name_array=[]
        for x in range(cell_array[0]):
            cell_name_array.append(cell_array[x+1][0])
            
        unique_cell_names=np.unique(cell_name_array)
        for unique_cell in unique_cell_names:
            include_cell=neuroml.IncludeType(href="%s.cell.nml"%unique_cell)
            nml_doc.includes.append(include_cell)

        localization_type=location_array[0]
        x_dim=location_array[1]
        y_dim=location_array[2]
        z_dim=location_array[3]
        
        if input_information[0]=="testing":
           fraction_of_cells_to_target_in_pop=input_information[1]
           #tests only with PulseGenerators for the time being; can be coded for other eligible inputs too

           for pulse_x in range(0,len(input_information)-2):

           
	     Pulse_generator_x=neuroml.PulseGenerator(id="Input_%d"%pulse_x,delay=input_information[pulse_x+2][0],duration=input_information[pulse_x+2][1],amplitude=input_information[pulse_x+2][2])
	     nml_doc.pulse_generators.append(Pulse_generator_x)
             #Pulse_generator2=neuroml.PulseGenerator(id="Input_2",delay=testing_inputs[4], duration=testing_inputs[5], amplitude=testing_inputs[6])
	     #nml_doc.pulse_generators.append(Pulse_generator2)

	

	# Create network
	net = neuroml.Network(id=ref+"_network",type="networkWithTemperature",temperature="23 degC")
	nml_doc.networks.append(net)


	# Create populations
        Golgi_pop_index_array=[]
        neuroml_Golgi_pop_array=[]
        if string.lower(population_type) =="list":
	   

	   cell_position_array=[]
	   
           no_density_model=True
            
	   if type(localization_type) is list:
              if string.lower(localization_type[0])=="density based":
                 ### will override cell numbers in cell_array if specified
                 no_density_model=False
                 for cell_group in range(0,len(localization_type[2])):
                     ### assuming that Y_values returned by load_density_data represent the depth with zero indicating Purkinje cell level
                     X_array,Y_array,density_values=load_density_data(localization_type[2][cell_group],localization_type[1])
                     dim_X_array=np.shape(X_array)
                     dim_Y_array=np.shape(Y_array)
                     ## assume meshgrid
                     if dim_X_array==dim_Y_array:
                        ## assume that data is not normalized; double-check, though
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
              for cell_population in range(cell_array[0]):
                  cell_position_array.append(np.zeros([cell_array[cell_population+1][1],3]))


           for x in range(cell_array[0]):
	      Golgi_pop = neuroml.Population(id="Golgi_pop%d"%x, size =cell_array[x+1][1], type="populationList",
		                  component=cell_array[x+1][0])
	      Golgi_pop_index_array.append("Golgi_pop%d"%x)
              neuroml_Golgi_pop_array.append(Golgi_pop)
	      net.populations.append(Golgi_pop)
           
           
           if type(localization_type) is list:
              if string.lower(localization_type[0])=="minimal distance":
                 for cell_pop in range(cell_array[0]):
                     golgi_pop=neuroml_Golgi_pop_array[cell_pop]
                     for cell in range(cell_array[cell_pop+1][1]):
	                 Golgi_cell=neuroml.Instance(id="%d"%cell)
	                 golgi_pop.instances.append(Golgi_cell)
	                 if cell_pop==0 and cell==0:
                            X=random.random()
	                    Y=random.random()
	                    Z=random.random()
                            cell_position_array[cell_pop][cell,0]=x_dim*X
                            cell_position_array[cell_pop][cell,1]=y_dim*Y
                            cell_position_array[cell_pop][cell,2]=z_dim*Z
                            Golgi_cell.location=neuroml.Location(x=x_dim*X, y=y_dim*Y, z=z_dim*Z)
                            print cell_position_array[cell_pop][cell,0], cell_position_array[cell_pop][cell,1], cell_position_array[cell_pop][cell,2]
                         else:
                            x=0
                            while x==0:
                                overlap_counter=0
                                X=(random.random())*x_dim
	                        Y=(random.random())*y_dim
	                        Z=(random.random())*z_dim
                                for cell_pop_x in range(cell_array[0]):
                                    pop_cell_positions=cell_position_array[cell_pop_x]
                                    for cell_x in range(cell_array[cell_pop_x+1][1]):
                                        if cell_position_array[cell_pop_x][cell_x,0]+cell_position_array[cell_pop_x][cell_x,1]+cell_position_array[cell_pop_x][cell_x,2] >0:
                                           if string.lower(localization_type[1])=="uniform":
                                              if distance([X,Y,Z],cell_position_array[cell_pop_x][cell_x]) < localization_type[2]:
                                                 overlap_counter+=1
                                           #if string.lower(localization_type[1])=="cell group specific": might be added in the future
                                              
                                if overlap_counter==0:
                                   cell_position_array[cell_pop][cell,0]=X
                                   cell_position_array[cell_pop][cell,1]=Y
                                   cell_position_array[cell_pop][cell,2]=Z
                                   Golgi_cell.location=neuroml.Location(x=X, y=Y, z=Z)
                               
                                   print cell_position_array[cell_pop][cell,0], cell_position_array[cell_pop][cell,1], cell_position_array[cell_pop][cell,2]
                                   x=1
                               
           if localization_type=="random no overlap":
              cell_diameter_array=[]
              for cell_pop in range(cell_array[0]):
                  cell_diameter=get_soma_diameter(cell_names[cell_pop])
                  cell_diameter_array.append(cell_diameter)
              for cell_pop in range(cell_array[0]):
                  golgi_pop=neuroml_Golgi_pop_array[cell_pop]
                  cell_diameter=get_soma_diameter(cell_names[cell_pop])
                  for cell in range(cell_array[cell_pop+1][1]):
	              Golgi_cell=neuroml.Instance(id="%d"%cell)
	              golgi_pop.instances.append(Golgi_cell)
	              if cell_pop==0 and cell==0:
                         X=random.random()
	                 Y=random.random()
	                 Z=random.random()
                         cell_position_array[cell_pop][cell,0]=x_dim*X
                         cell_position_array[cell_pop][cell,1]=y_dim*Y
                         cell_position_array[cell_pop][cell,2]=z_dim*Z
                         Golgi_cell.location=neuroml.Location(x=x_dim*X, y=y_dim*Y, z=z_dim*Z)
                         print cell_position_array[cell_pop][cell,0], cell_position_array[cell_pop][cell,1], cell_position_array[cell_pop][cell,2]
                      else:
                         x=0
                         while x==0:
                            overlap_counter=0
                            X=(random.random())*x_dim
	                    Y=(random.random())*y_dim
	                    Z=(random.random())*z_dim
                            for cell_pop_x in range(cell_array[0]):
                                pop_cell_positions=cell_position_array[cell_pop_x]
                                for cell_x in range(cell_array[cell_pop_x+1][1]):
                                    if cell_position_array[cell_pop_x][cell_x,0]+cell_position_array[cell_pop_x][cell_x,1]+cell_position_array[cell_pop_x][cell_x,2] >0:
                                       if distance([X,Y,Z],cell_position_array[cell_pop_x][cell_x]) < (cell_diameter+cell_diameter_array[cell_pop_x])/2:
                                          overlap_counter+=1
                            if overlap_counter==0:
                               cell_position_array[cell_pop][cell,0]=X
                               cell_position_array[cell_pop][cell,1]=Y
                               cell_position_array[cell_pop][cell,2]=Z
                               Golgi_cell.location=neuroml.Location(x=X, y=Y, z=Z)
                               
                               print cell_position_array[cell_pop][cell,0], cell_position_array[cell_pop][cell,1], cell_position_array[cell_pop][cell,2]
                               x=1
                      
           if localization_type=="random":
              
              for cell_pop in range(cell_array[0]):
                  golgi_pop=neuroml_Golgi_pop_array[cell_pop]
                  for cell in range(cell_array[cell_pop+1][1]):
	              Golgi_cell=neuroml.Instance(id="%d"%cell)
	              golgi_pop.instances.append(Golgi_cell)
	              X=random.random()
	              Y=random.random()
	              Z=random.random()
                      cell_position_array[cell_pop][cell,0]=x_dim*X
                      cell_position_array[cell_pop][cell,1]=y_dim*Y
                      cell_position_array[cell_pop][cell,2]=z_dim*Z
                      Golgi_cell.location=neuroml.Location(x=x_dim*X, y=y_dim*Y, z=z_dim*Z)
                      print cell_position_array[cell_pop][cell,0], cell_position_array[cell_pop][cell,1], cell_position_array[cell_pop][cell,2]
                 
	   

        

           
           if connectivity_information[0]=="Vervaeke_2012_based":
               cell_names=[]
               for cell in range(cell_array[0]):
                   cell_names.append(cell_array[cell+1][0])
               
               gap_counter=0
               initial_projection_counter=0
               pairs=[]                                                    
               for pair in range(0,len(connectivity_information[5])):
                   members=[]
                   members.append(connectivity_information[5][pair][0])  
                   members.append(connectivity_information[5][pair][1])
                   pairs.append(members)
               pairs_gap_conductance=[]
               for pair in range(0,len(connectivity_information[2])):
                   members=[]
                   members.append(connectivity_information[5][pair][0])  
                   members.append(connectivity_information[5][pair][1])
                   pairs_gap_conductance.append(members)
               for pre_pop_index in range(0,len(Golgi_pop_index_array)):
                       
                   if connectivity_information[3][pre_pop_index]=="segment groups and segments":
                      pre_pop_target_segment_array=extract_morphology_information([cell_names[pre_pop_index]],\
                                                                                          ["segment groups",connectivity_information[4][pre_pop_index][0] ])
                   if connectivity_information[3][pre_pop_index]=="segments and subsegments":
                      pre_pop_target_segment_array=extract_morphology_information([cell_names[pre_pop_index]],\
                                                                                          ["segments",connectivity_information[4][pre_pop_index][0]])
                   for post_pop_index in range(0,len(Golgi_pop_index_array)):
                       if connectivity_information[3][post_pop_index]=="segment groups and segments":
                          post_pop_target_segment_array=extract_morphology_information([cell_names[post_pop_index]],\
                                                                                          ["segment groups",connectivity_information[4][post_pop_index][0]])
                       if connectivity_information[3][post_pop_index]=="segments and subsegments":
                          post_pop_target_segment_array=extract_morphology_information([cell_names[post_pop_index]],\
                                                                                          ["segments",connectivity_information[4][post_pop_index][0]])                                                
                       if pre_pop_index<=post_pop_index:
                          proj = neuroml.ElectricalProjection(id="proj%d"%initial_projection_counter,
		                presynaptic_population=Golgi_pop_index_array[pre_pop_index], 
		                postsynaptic_population=Golgi_pop_index_array[post_pop_index])
                          initial_projection_counter+=1
                          projection_counter=0
	                  conn_count = 0
                          pre_cell_positions=cell_position_array[pre_pop_index]
                          post_cell_positions=cell_position_array[post_pop_index]
                          pairs=[]                                                    
                          for pair in range(0,len(pairs)):
                              if collections.Counter(pairs[pair])==collections.Counter([cell_names[pre_pop_index],cell_names[post_pop_index]] ):
                                 if connectivity_information[5][pair][2]=="constant number of GJ contacts per pair":
                                    no_of_GJcon_per_pair=connectivity_information[5][pair][3]
                                 if connectivity_information[5][pair][2]=="variable number of GJ contacts per pair":
                                    if connectivity_information[5][pair][3]=="binomial":
                                       no_of_GJcon_per_pair=np.random.binomial(connectivity_information[5][pair][5],connectivity_information[5][pair][4]/connectivity_information[5][pair][5])

                          conductance_scaling=1
                          if connectivity_information[-2][0]=="testing":
                             conductance_scaling=connectivity_information[-2][1]

                          variable_conductance_parameters_of_cell_pairs=[]

                          for pair in range(0,len(pairs_gap_conductance)):
                              if collections.Counter(pairs_gap_conductance[pair])==collections.Counter([cell_names[pre_pop_index],cell_names[post_pop_index]] ):
                                 pair_index=pair
                                 if connectivity_information[2][pair][2]=="constant conductance":
                                    conductance_value=connectivity_information[2][pair][3]
                                    conductance_units=connectivity_information[2][pair][4]
                                    gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%f%s"%(conductance_value*conductance_scaling,conductance_units)) 
                                    gap_id_per_pair="gap_junction%d"%gap_counter        
                                    nml_doc.gap_junctions.append(gap_junction)
		                    gap_counter+=1
                                    
                          for Pre_cell in range(cell_array[pre_pop_index+1][1]):
                              for Post_cell in range(cell_array[post_pop_index+1][1]):
                                  if pre_pop_index==post_pop_index:
                                     compare_ids=Pre_cell < Post_cell
                                  if pre_pop_index < post_pop_index:
                                     compare_ids=Pre_cell<=Post_cell
                                  if compare_ids:
                                     distance_between_cells=distance(pre_cell_positions[Pre_cell],post_cell_positions[Post_cell])/connectivity_information[1]
                                     if random.random() <connection_probability_vervaeke_2010(distance_between_cells):
                                        if connectivity_information[3][pre_pop_index]=="segment groups and segments":
                                           pre_target_points=get_unique_target_points(pre_pop_target_segment_array,"segment groups and segments",\
                                                                                   connectivity_information[4][post_pop_index],no_of_GJcon_per_pair)
                                        if connectivity_information[3][pre_pop_index]=="segments and subsegments":
                                           pre_target_points=get_unique_target_points(pre_pop_target_segment_array,"segments and subsegments",\
                                                                                connectivity_information[4][post_pop_index],no_of_GJcon_per_pair) 
       
                                        if connectivity_information[3][post_pop_index]=="segment groups and segments":
                                           post_targeting_mode="segment groups and segments"
                                        if connectivity_information[3][post_pop_index]=="segments and subsegments":
                                           post_targeting_mode="segments and subsegments"
                                        for pre_target_point in range(0,len(pre_target_points)):
                                            if connectivity_information[-1][0]== "maximal connection length":
                                               if connectivity_information[-1][1] != None:
                                                  x=0
                                                  while x==0:
                                                      post_target_point=get_unique_target_points(post_pop_target_segment_array,post_targeting_mode,\
                                                                                connectivity_information[4][post_pop_index],1) 
                                                      if get_3D_connection_length(cell_names,cell_position_array,pre_pop_index,post_pop_index,Pre_cell,\
                                                         Post_cell,pre_target_points[pre_target_point,0],post_target_point[0,0],\
                                                         pre_target_points[pre_target_point,1],post_target_point[0,1]) <=connectivity_information[-1][1]:
                                                         x=1
                                                  Pre_segment_id=pre_target_points[pre_target_point,0]
                                                  Post_segment_id=post_target_point[0,0]
                                                  Pre_fraction=pre_target_points[pre_target_point,1]
                                                  Post_fraction=post_target_point[0,1] 

                                                  if connectivity_information[2][pair_index][2]=="variable conductance":
                                                     if string.lower(connectivity_information[2][pair][2])=="gaussian":
                                                        gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%f%s"%(connectivity_information[2][pair_index][3]*conductance_scaling,connectivity_information[2][pair_index][4]))
                                                        nml_doc.gap_junctions.append(gap_junction)
		                                        gap_counter+=1
                                                        #other options can be added such as gamma distribution
                                                     conn =neuroml.ElectricalConnectionInstance(id=conn_count,pre_cell="%d"%Pre_cell,post_cell="%d"%Post_cell,synapse=gap,\
                                                             pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                                                             pre_fraction_along="%f"%random.random(),post_fraction_along="%f"%random.random())
                                            
		                                     if projection_counter==0:
                                                        net.electrical_projections.append(proj)
                                                        projection_counter+=1
                                               
		                                     proj.electrical_connection_instances.append(conn)
		                                     conn_count+=1
                                                     x=1
                                                  if connectivity_information[2][pair_index][2]=="constant conductance":
                                                     conn =neuroml.ElectricalConnectionInstance(id=conn_count,pre_cell="%d"%Pre_cell,post_cell="%d"%Post_cell,synapse=gap_id_per_pair,\
                                                              pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                                                              pre_fraction_along="%f"%Pre_fraction,post_fraction_along="%f"%Post_fraction)
                                            
		                                     if projection_counter==0:
                                                        net.electrical_projections.append(proj)
                                                        projection_counter+=1
                                               
		                                     proj.electrical_connection_instances.append(conn)
		                                     conn_count+=1
                                                     x=1
                                                  else:
                                                     post_target_point=get_unique_target_points(post_pop_target_segment_array,post_targeting_mode,\
                                                                                connectivity_information[4][post_pop_index],1) 
                                                     Pre_segment_id=pre_target_points[pre_target_point,0]
                                                     Post_segment_id=post_target_point[0,0]
                                                     Pre_fraction=pre_target_points[pre_target_point,1]
                                                     Post_fraction=post_target_point[0,1] 

                                                     if connectivity_information[2][pair_index][2]=="variable conductance":
                                                        if string.lower(connectivity_information[2][pair][2])=="gaussian":
                                                           gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%f%s"%(connectivity_information[2][pair_index][3]*conductance_scaling,connectivity_information[2][pair_index][4]))
                                                           nml_doc.gap_junctions.append(gap_junction)
		                                           gap_counter+=1
                                                        #other options can be added such as gamma distribution
                                                        conn =neuroml.ElectricalConnectionInstance(id=conn_count,\
pre_cell="../%s/%d/%s"%(Golgi_pop_index_array[pre_pop_index],Pre_cell,cell_array[pre_pop_index+1][0]),\
post_cell="../%s/%d/%s"%(Golgi_pop_index_array[post_pop_index],Post_cell,cell_array[post_pop_index+1][0]),synapse=gap,\
                                                             pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                                                             pre_fraction_along="%f"%random.random(),post_fraction_along="%f"%random.random())
                                            
		                                        if projection_counter==0:
                                                           net.electrical_projections.append(proj)
                                                           projection_counter+=1
                                               
		                                        proj.electrical_connection_instances.append(conn)
		                                        conn_count+=1
                                                        x=1

                                                     if connectivity_information[2][pair_index][2]=="constant conductance":
                                                        conn =neuroml.ElectricalConnectionInstance(id=conn_count,pre_cell="%d"%Pre_cell,post_cell="%d"%Post_cell,synapse=gap_id_per_pair,\
                                                              pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                                                              pre_fraction_along="%f"%Pre_fraction,post_fraction_along="%f"%Post_fraction)
                                            
		                                        if projection_counter==0:
                                                           net.electrical_projections.append(proj)
                                                           projection_counter+=1
                                               
		                                        proj.electrical_connection_instances.append(conn)
		                                        conn_count+=1
                                                        x=1

           if connectivity_information[0]=="Vervaeke_2010_one_compartment":
               gap_counter=0
               initial_projection_counter=0
               for pre_pop_index in range(0,len(Golgi_pop_index_array)):
                   for post_pop_index in range(0,len(Golgi_pop_index_array)):
                       if pre_pop_index<=post_pop_index:
                          proj = neuroml.ElectricalProjection(id="proj%d"%initial_projection_counter,
		                presynaptic_population=Golgi_pop_index_array[pre_pop_index], 
		                postsynaptic_population=Golgi_pop_index_array[post_pop_index])
                          
                          initial_projection_counter+=1
                          projection_counter=0
	                  conn_count = 0
                          pre_cell_positions=cell_position_array[pre_pop_index]
                          post_cell_positions=cell_position_array[post_pop_index]
                          for Pre_cell in range(cell_array[pre_pop_index+1][1]):
                          #scripted so that to avoid inclusion of projection and gap_junction/synapse components if there are no connections; otherwise the mod files are not compiled.
                                  for Post_cell in range(cell_array[post_pop_index+1][1]):
                                      if pre_pop_index==post_pop_index:
                                         compare_ids=Pre_cell <Post_cell
                                      if pre_pop_index<post_pop_index:
                                         compare_ids=Pre_cell<=Post_cell
                                      if compare_ids:
                                         distance_between_cells=distance(pre_cell_positions[Pre_cell],post_cell_positions[Post_cell])/connectivity_information[1]
                                         if random.random() <connection_probability_vervaeke_2010(distance_between_cells):
                                            gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%fpS"%synaptic_weight_vervaeke_2010(distance_between_cells))
                                            conn =neuroml.ElectricalConnectionInstance(id=conn_count,\
                                                                               pre_cell="../%s/%d/%s"%(Golgi_pop_index_array[pre_pop_index],Pre_cell,cell_array[pre_pop_index+1][0]),\
                                                                               post_cell="../%s/%d/%s"%(Golgi_pop_index_array[post_pop_index],Post_cell,cell_array[post_pop_index+1][0]),\
                                                                               synapse=gap_junction.id)
                                            
		                            nml_doc.gap_junctions.append(gap_junction)
		                            gap_counter+=1
		                            if projection_counter==0:
                                               net.electrical_projections.append(proj)
                                               projection_counter+=1
                                               
		                            proj.electrical_connection_instances.append(conn)
		                            conn_count+=1
		                            
		                            
	   if connectivity_information[0]=="Vervaeke_2010_multi_compartment":
               cell_names=[]
               
               for cell in range(cell_array[0]):
                   cell_names.append(cell_array[cell+1][0])
               
               gap_counter=0
               initial_projection_counter=0
               segment_group_list=[]
               segment_group_list.append("segment groups")
               for cell_population in range(0,len(Golgi_pop_index_array)):
                   segment_group_list.append(connectivity_information[cell_population+2][0])
               target_segment_array=extract_morphology_information(cell_names,segment_group_list)
               for pre_pop_index in range(0,len(Golgi_pop_index_array)):
                   for post_pop_index in range(0,len(Golgi_pop_index_array)):
                       if pre_pop_index<=post_pop_index:
                          proj = neuroml.ElectricalProjection(id="proj%d"%initial_projection_counter,
		                presynaptic_population=Golgi_pop_index_array[pre_pop_index], 
		                postsynaptic_population=Golgi_pop_index_array[post_pop_index])
                          
                          initial_projection_counter+=1
                          projection_counter=0
	                  conn_count = 0
                          pre_cell_positions=cell_position_array[pre_pop_index]
                          post_cell_positions=cell_position_array[post_pop_index]
                          for Pre_cell in range(cell_array[pre_pop_index+1][1]):
                          #scripted so that to avoid inclusion of projection and gap_junction/synapse components if there are no connections; otherwise the mod files are not compiled.
                                  for Post_cell in range(cell_array[post_pop_index+1][1]):
                                      if pre_pop_index==post_pop_index:
                                         compare_ids=Pre_cell <Post_cell
                                      if pre_pop_index<post_pop_index:
                                         compare_ids=Pre_cell<=Post_cell                        
                                      if compare_ids:
                                         distance_between_cells=distance(pre_cell_positions[Pre_cell],post_cell_positions[Post_cell])/connectivity_information[1]
                                         if random.random() <connection_probability_vervaeke_2010(distance_between_cells):
                                            if connectivity_information[-1][0]== "maximal connection length":
                                               if connectivity_information[-1][1] != None:
                                                  z=0
                                                  while z==0:
                                                      x=0
                                                      while x==0:
                                                          pre_segment_group=random.sample(range(0,len(connectivity_information[pre_pop_index+2][0])),1)
                                                          pre_segment_group=pre_segment_group[0]
                                                          if random.random() < connectivity_information[pre_pop_index+2][1][pre_segment_group]:
                                                             pre_group=connectivity_information[pre_pop_index+2][0][pre_segment_group]
                                                             x=1
                                                      y=0
                                                      while y==0:
                                                          post_segment_group=random.sample(range(0,len(connectivity_information[post_pop_index+2][0])),1)
                                                          post_segment_group=post_segment_group[0]
                                                          if random.random() < connectivity_information[post_pop_index+2][1][post_segment_group]:
                                                             post_group=connectivity_information[post_pop_index+2][0][post_segment_group]
                                                             y=1
                                                      for segment_group in range(0,len(target_segment_array[pre_pop_index])):
                                                          if target_segment_array[pre_pop_index][segment_group+1][0]==pre_group:
                                                             pre_segment_ids=target_segment_array[pre_pop_index][segment_group+1][1:]
                                                             break
                                                      for segment_group in range(0,len(target_segment_array[post_pop_index])):
                                                          if target_segment_array[post_pop_index][segment_group+1][0]==post_group:
                                                             post_segment_ids=target_segment_array[post_pop_index][segment_group+1][1:]
                                                             break
                                            
                                                      Pre_segment_id=random.sample(pre_segment_ids,1)
                                                      Pre_segment_id=Pre_segment_id[0]
                                                      Post_segment_id=random.sample(post_segment_ids,1)
                                                      Post_segment_id=Post_segment_id[0]
                                                      pre_fraction=random.random()
                                                      post_fraction=random.random()
                                                      if get_3D_connection_length(cell_names,cell_position_array,pre_pop_index,post_pop_index,Pre_cell,\
                                                         Post_cell_ID,Pre_segment_id,Post_segment_id,pre_fraction,post_fraction) <=connectivity_information[-1][1]:
                                                         z=1
                                               else:
                                                  x=0
                                                  while x==0:
                                                      pre_segment_group=random.sample(range(0,len(connectivity_information[pre_pop_index+2][0])),1)
                                                      pre_segment_group=pre_segment_group[0]
                                                      if random.random() < connectivity_information[pre_pop_index+2][1][pre_segment_group]:
                                                         pre_group=connectivity_information[pre_pop_index+2][0][pre_segment_group]
                                                         x=1
                                                   
                                                  y=0
                                                  while y==0:
                                                      post_segment_group=random.sample(range(0,len(connectivity_information[post_pop_index+2][0])),1)
                                                      post_segment_group=post_segment_group[0]
                                                      if random.random() < connectivity_information[post_pop_index+2][1][post_segment_group]:
                                                         post_group=connectivity_information[post_pop_index+2][0][post_segment_group]
                                                         y=1
                                                                   
                                                  for segment_group in range(0,len(target_segment_array[pre_pop_index])):
                                                      if target_segment_array[pre_pop_index][segment_group+1][0]==pre_group:
                                                         pre_segment_ids=target_segment_array[pre_pop_index][segment_group+1][1:]
                                                         break
                                                  for segment_group in range(0,len(target_segment_array[post_pop_index])):
                                                      if target_segment_array[post_pop_index][segment_group+1][0]==post_group:
                                                         post_segment_ids=target_segment_array[post_pop_index][segment_group+1][1:]
                                                         break
                                            
                                                  Pre_segment_id=random.sample(pre_segment_ids,1)
                                                  Pre_segment_id=Pre_segment_id[0]
                                                  Post_segment_id=random.sample(post_segment_ids,1)
                                                  Post_segment_id=Post_segment_id[0]
                                                  Pre_fraction=random.random()
                                                  Post_fraction=random.random()
                                            
                                            if connectivity_information[-2][0]=="testing":
                                               gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%fpS"%(synaptic_weight_vervaeke_2010(distance_between_cells)*connectivity_information[-2][1]))
                                            else:
                                               gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%fpS"%synaptic_weight_vervaeke_2010(distance_between_cells))
                                               gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%fpS"%synaptic_weight_vervaeke_2010(distance_between_cells)*connectivity_information[-1][1])
                                            conn =neuroml.ElectricalConnectionInstance(id=conn_count,\
                                                                                pre_cell="../%s/%d/%s"%(Golgi_pop_index_array[pre_pop_index],Pre_cell,cell_array[pre_pop_index+1][0]),\
                                                                              post_cell="../%s/%d/%s"%(Golgi_pop_index_array[post_pop_index],Post_cell,cell_array[post_pop_index+1][0]),\
                                                                               synapse=gap_junction.id,pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                                                                               pre_fraction_along="%f"%Pre_fraction,post_fraction_along="%f"%Post_fraction)
		                            nml_doc.gap_junctions.append(gap_junction)
		                            gap_counter+=1
		                            if projection_counter==0:
                                               net.electrical_projections.append(proj)
                                               projection_counter+=1
                                               
		                            proj.electrical_connection_instances.append(conn)
		                            conn_count+=1
              
                                                                   
           if connectivity_information[0]=="uniform random":
               gap_junction0 = neuroml.GapJunction(id="gap_junction0", conductance=connectivity_information[1][1])
               gap_counter=0
               initial_projection_counter=0
               for pre_pop_index in range(0,len(Golgi_pop_index_array)):
                   for post_pop_index in range(0,len(Golgi_pop_index_array)):
                       if pre_pop_index<=post_pop_index:
                          proj = neuroml.ElectricalProjection(id="proj%d"%initial_projection_counter,
		                presynaptic_population=Golgi_pop_index_array[pre_pop_index], 
		                postsynaptic_population=Golgi_pop_index_array[post_pop_index])
                          
                          initial_projection_counter+=1
                          projection_counter=0
	                  conn_count = 0
                          for Pre_cell in range(cell_array[pre_pop_index+1][1]):
                          # randomly Connect cells with defined probability for now; scripted so that to avoid inclusion of projection and gap_junction/synapse components if there are no connections; otherwise the mod files are not compiled.
                                  for Post_cell in range(cell_array[post_pop_index+1][1]):
                                      if pre_pop_index==post_pop_index:
                                         compare_ids=Pre_cell <Post_cell
                                      if pre_pop_index<post_pop_index:
                                         compare_ids=Pre_cell<=Post_cell                   
                                      if compare_ids:
                                         if random.random() < connectivity_information[1][0]:
                                            conn =neuroml.ElectricalConnectionInstance(id=conn_count, \
				   pre_cell="../%s/%d/%s"%(Golgi_pop_index_array[pre_pop_index],Pre_cell,cell_array[pre_pop_index+1][0]),
				   post_cell="../%s/%d/%s"%(Golgi_pop_index_array[post_pop_index],Post_cell,cell_array[post_pop_index+1][0]),synapse=gap_junction0.id)
                                            if gap_counter==0:
		                               nml_doc.gap_junctions.append(gap_junction0)
		                               gap_counter+=1
		                            if projection_counter==0:
                                               net.electrical_projections.append(proj)
                                               projection_counter+=1
                                               
		                            proj.electrical_connection_instances.append(conn)
		                            conn_count+=1
           
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
           if "testing" not in input_information:
              for input_group in input_information:
                 if type(input_group) is list:
                    for var in range(0,len(input_group)):
                      #more options can be added in the future
                      if "MF"==input_group[var][0] or "PF"==input_group[var][0]:
                          inp_group_specifier=input_group[var][0]
                          synapse_name_array=[]
                          for pop in range(0,len(input_group[var][1])):
                              names_of_synapses=input_group[var][1][pop][2]
                              for name in names_of_synapses:
                                  synapse_name_array.append(name)
                              unique_synapse_names=np.unique(synapse_name_array)
                          for unique_synapse in unique_synapse_names:
                              include_synapse=neuroml.IncludeType(href="%s.synapse.nml"%unique_synapse)
                              nml_doc.includes.append(include_synapse)
                          for pop in range(0,len(input_group[var][1])):
                              genuine_pop_index=input_group[var][1][pop][0]
                              segment_group_list=[]
                              if input_group[var][1][pop][5]=="segment groups and segments":
                                 segment_group_list.append("segment groups")
                              if input_group[var][1][pop][5]=="segments and subsegments":
                                 segment_group_list.append("segments")
                              for poisson_synapse_list in range(0,len(input_group[var][1][pop][3])):
                                  segment_group_list.append(input_group[var][1][pop][6][poisson_synapse_list][0])
                                  segment_target_array=extract_morphology_information([cell_array[genuine_pop_index+1][0]],segment_group_list)
                                  targeting_parameters=input_group[var][1][pop][6][poisson_synapse_list]
                                  
                                  if input_group[var][1][pop][3][poisson_synapse_list][1]=="persistent":
                                     poisson_syn=neuroml.PoissonFiringSynapse(id="%s_pop%dsyn%d"%(inp_group_specifier,genuine_pop_index,poisson_synapse_list),\
                                                       average_rate="%f per_s"%input_group[var][1][pop][3][poisson_synapse_list][2],\
                                            synapse=input_group[var][1][pop][3][poisson_synapse_list][0] ,\
                                            spike_target="./%s"%input_group[var][1][pop][3][poisson_synapse_list][0])
                                     
                                  if input_group[var][1][pop][3][poisson_synapse_list][1]=="transient":
                                     poisson_syn=neuroml.TransientPoissonFiringSynapse(id="%s_pop%dsyn%d"%(inp_group_specifier,genuine_pop_index,poisson_synapse_list),\
                                            average_rate="%f per_s"%input_group[var][1][pop][3][poisson_synapse_list][2],\
                                            synapse=input_group[var][1][pop][3][poisson_synapse_list][0] ,\
                                            spike_target="./%s"%input_group[var][1][pop][3][poisson_synapse_list][0],\
                                            delay="%f%s"%(input_group[var][1][pop][3][poisson_synapse_list][3],input_group[var][1][pop][3][poisson_synapse_list][5]),\
                                            duration="%f%s"%(input_group[var][1][pop][3][poisson_synapse_list][4] ,input_group[var][1][pop][3][poisson_synapse_list][5])  )
                                  
                                  nml_doc.poisson_firing_synapses.append(poisson_syn)

                                  input_list =neuroml.InputList(id="%s_Input_pop%dsyn%d"%(inp_group_specifier,genuine_pop_index,poisson_synapse_list),\
                                             component=poisson_syn.id, populations=Golgi_pop_index_array[genuine_pop_index])
                                  net.input_lists.append(input_list)
                                  which_cells_to_target_array=input_group[var][1][pop][1]
                                  if which_cells_to_target_array[0]=="uniform":
                                     fraction_to_target_per_pop=which_cells_to_target_array[1]
                                     target_cells=random.sample(range(cell_array[genuine_pop_index+1][1]),int(round(fraction_to_target_per_pop*cell_array[genuine_pop_index+1][1])))
                                     count=0                           
                                     for target_cell in target_cells:
                                         if input_group[var][1][pop][4][0]=="constant number of inputs per cell":
                                             no_of_inputs=input_group[var][1][pop][4][1]
                                         if input_group[var][1][pop][4][0]=="variable number of inputs per cell":
                                            if input_group[var][1][pop][4][1]=="binomial":
                                               no_of_inputs=np.random.binomial(input_group[var][1][pop][4][3],\
                                                      input_group[var][1][pop][4][2]/input_group[var][1][pop][4][3])
                                            ### other options can be added

                                         if input_group[var][1][pop][5]=="segment groups and segments":
                                            target_points=get_unique_target_points(segment_target_array,"segment groups and segments",targeting_parameters,no_of_inputs)
                                         if input_group[var][1][pop][5]=="segments and subsegments":
                                            target_points=get_unique_target_points(segment_target_array,"segments and subsegments",targeting_parameters,no_of_inputs)
                                         #count_point=0
                                         for target_point in range(0,len(target_points)):                     
                                             syn_input = neuroml.Input(id="%d"%(count),target="../%s/%i/%s"%(Golgi_pop_index_array[genuine_pop_index],\
                                                                  target_cell,cell_array[genuine_pop_index+1][0] ),destination="synapses",\
                                                                  segment_id="%d"%target_points[target_point,0],fraction_along="%f"%target_points[target_point,1]) 
                                             
                                             input_list.input.append(syn_input)
                                             #count_point=count_point+1

                                             count=count+1

                                  if which_cells_to_target_array[0]=="3D region specific":
                                     cell_positions=cell_position_array[genuine_pop_index]
                                     dim_array=np.shape(cell_positions)
                                     region_specific_targets_per_cell_group=[]
                                     for region in range(1,len(which_cells_to_target_array[1])):
                                         for cell in range(0,dim_array[0]):
                                             if (which_cells_to_target_array[1][region][0][0] <  cell_positions[cell,0]) and (cell_positions[cell,0] < which_cells_to_target_array[1][region][0][1]):
                                                if (which_cells_to_target_array[1][region][1][0] <  cell_positions[cell,1]) and (cell_positions[cell,1] <which_cells_to_target_array[1][region][1][1]) :
                                                   if (which_cells_to_target_array[1][region][2][0] <  cell_positions[cell,2]) and (cell_positions[cell,2] < which_cells_to_target_array[1][region][2][1]):
                                                      region_specific_targets_per_cell_group.append(cell)  
   
                                     if which_cells_to_target_array[2]=="all":
                                        count=0
                                        for target_cell in region_specific_targets_per_cell_group:
                                            if input_group[var][1][pop][4][0]=="constant number of inputs per cell":
                                               no_of_inputs=input_group[var][1][pop][4][1]
                                            if input_group[var][1][pop][4][0]=="variable number of inputs per cell":
                                               if input_group[var][1][pop][4][1]=="binomial":
                                                  no_of_inputs=np.random.binomial(input_group[var][1][pop][4][3],input_group[var][1][pop][4][2]/input_group[var][1][pop][4][3])
                                            if input_group[var][1][pop][5]=="segment groups and segments":
                                               target_points=get_unique_target_points(segment_target_array,"segment groups and segments",targeting_parameters,no_of_inputs)
                                            if input_group[var][1][pop][5]=="segments and subsegments":
                                               target_points=get_unique_target_points(segment_target_array,"segments and subsegments",targeting_parameters,no_of_inputs)
                                            #count_point=0
                                            for target_point in range(0,len(target_points)):       
                                                syn_input = neuroml.Input(id="%d"%(count),target="../%s/%i/%s"%(Golgi_pop_index_array[genuine_pop_index],\
                                                                  target_cell,cell_array[genuine_pop_index+1][0] ),destination="synapses",\
                                                                  segmentId="%d"%target_points[target_point,0],fraction_along="%f"%target_points[target_point,1]) 
                                                input_list.input.append(syn_input)
                                                #count_point=count_point+1
                                                count=count+1
                                      #  now coded so that the same fraction applies to all 3D regions
                                     if which_cells_to_target_array[2]=="random fraction":
                                        random_targets_per_cell_group=random.sample(region_specific_targets_per_cell_group,\
                                                int(round(which_cells_to_target_array[3]*len(region_specific_targets_per_cell_group))))
                                        count=0
                                        for target_cell in random_targets_per_cell_group:
                                            if input_group[var][1][pop][4][0]=="constant number of inputs per cell":
                                               no_of_inputs=input_group[var][1][pop][4][1]
                                            if input_group[var][1][pop][4][0]=="variable number of inputs per cell":
                                               if input_group[var][1][pop][4][1]=="binomial":
                                                  no_of_inputs=np.random.binomial(input_group[var][1][pop][4][3],input_group[var][1][pop][4][2]/input_group[var][1][pop][4][3])
                                            if input_group[var][1][pop][5]=="segment groups and segments":
                                               target_points=get_unique_target_points(segment_target_array,"segment groups and segments",targeting_parameters,no_of_inputs)
                                            if input_group[var][1][pop][5]=="segments and subsegments":
                                               target_points=get_unique_target_points(segment_target_array,"segments and subsegments",targeting_parameters,no_of_inputs)
                                            #count_point=0
                                            for target_point in range(0,len(target_points)):       
                                                syn_input = neuroml.Input(id="%d"%(count),target="../%s/%i/%s"%(Golgi_pop_index_array[genuine_pop_index],\
                                                                  target_cell,cell_array[genuine_pop_index+1][0] ),destination="synapses",\
                                                                  segment_id="%d"%target_points[target_point,0],fraction_along="%f"%target_points[target_point,1]) 
                                                
                                                input_list.input.append(syn_input)
                                                #count_point=count_point+1
                                                count=count+1       
        
	   ###### implementing physiological heterogeneity between cells with variations in a basal firing rate
           if "testing" not in input_information:
             for input_group in input_information:
                if "variable basal firing rate"==input_group[0]:
                  for var in input_group:
                      if type(var) is list:
                         if var[0]=="amplitude distribution":
                            gaussian_model=False
                            uniform_model=False
                            constant_model=False
                            if "gaussian" in var:
                                pop_average_array=[]
                                pop_variance_array=[]
                                gaussian_model=True
                                for pop_var in range(0,len(var[2])):
                                    pop_average_array.append(var[2][pop_var])
                                    pop_variance_array.append(var[3][pop_var])
                                units=var[4]
                            if "constant" in var:
                               pop_amplitude=[]
                               constant_model=True
                               for pop_var in range(0,len(var[2])):
                                   pop_amplitude.append(var[2][pop_var])
                               units=var[3]  
                            if "uniform" in var:
                               pop_left_bound=[]
                               pop_right_bound=[]
                               uniform_model=True
                               for pop_var in range(0,len(var[2])):
                                   pop_left_bound.append(var[2][pop_var])
                                   pop_right_bound.append(var[3][pop_var])
                               units=var[4]
                         if var[0]=="offset distribution":
                            offset_gaussian_model=False
                            offset_uniform_model=False
                            offset_constant_model=False
                            if "gaussian" in var:
                                offset_gaussian_model=True
                                pop_offset_average=[]
                                pop_offset_variance=[]
                                for pop_var in range(0,len(var[2])):
                                    pop_offset_average.append(var[2][pop_var])
                                    pop_offset_variance.append(var[3][pop_var])
                                offset_units=var[4]
                            if "constant" in var:
                                pop_offset=[]
                                offset_constant_model=True
                                for pop_var in range(0,len(var[2])):
                                    pop_offset.append(var[2][pop_var])
                                offset_units=var[3]   
                            if "uniform" in var:
                                offset_uniform_model=True
                                pop_offset_left_bound=[]
                                pop_offset_right_bound=[]
                                for pop_var in range(0,len(var[2])):
                                    pop_offset_left_bound.append(var[2][pop_var])
                                    pop_offset_right_bound.append(var[3][pop_var])
                                offset_units=var[4]
                  for pop in range(0,len(Golgi_pop_index_array)):
                      for cell in range(cell_array[pop+1][1]):
                          if gaussian_model:
                             amp=random.gauss(pop_average_array[pop],pop_variance_array[pop])
                          if uniform_model:
                             amp=random.uniform(pop_left_bound[pop],pop_right_bound[pop])
                          if constant_model:
                             amp=pop_amplitude[pop] 
                          if offset_gaussian_model:
                             offset=random.gauss(pop_offset_average[pop],pop_offset_variance[pop])
                          if offset_uniform_model:
                             offset=random.uniform(pop_offset_left_bound[pop],pop_offset_right_bound[pop])
                          if offset_constant_model:
                             offset=pop_offset[pop]
                          Pulse_generator_variable=neuroml.PulseGenerator(id="Input_%d%d"%(pop,cell),delay="%f%s"%(offset,offset_units),duration="%f%s"%(simulation_parameters[1]-offset,offset_units),amplitude="%f%s"%(amp,units))
	                  nml_doc.pulse_generators.append(Pulse_generator_variable)
	                  Input_list=neuroml.InputList(id="Input_list%d%d"%(pop,cell),component="Input_%d%d"%(pop,cell))
	                  net.input_lists.append(Input_list)
	                  Inp = neuroml.Input(target="../%s/%d/%s"%(Golgi_pop_index_array[pop],cell,cell_array[pop+1][0]),id="%d"%cell,destination="synapses")
	                  Input_list.input.append(Inp)
	              
           if input_information[0]=="testing":
              neuroml_input_array=[]
              for pop in range(0,len(Golgi_pop_index_array)):
                  for pulse_x in range(0,len(input_information)-2):
                      Input_list=neuroml.InputList(id="Input_list%d"%pulse_x, component="Input_%d"%pulse_x,populations="%s"%Golgi_pop_index_array[pop])
                      neuroml_input_array.append(Input_list)
                      net.input_lists.append(Input_list)
                      randomly_select_target_cells=random.sample(range(cell_array[pop+1][1]),int(round(fraction_of_cells_to_target_in_pop*cell_array[pop+1][1])))
                      for input_list in neuroml_input_array:
                          for i in randomly_select_target_cells:
                              Inp = neuroml.Input(target="../%s/%d/%s"%(Golgi_pop_index_array[pop],i,cell_array[pop+1][0]),id="%d"%i,destination="synapses")
                              input_list.input.append(Inp)
                      

        else:
         
           
           for x in range(cell_array[0]):
	      Golgi_pop = neuroml.Population(id="Golgi_pop%d"%x, size =cell_array[x+1][1],
		                  component=cell_array[x+1][0])
	      Golgi_pop_index_array.append("Golgi_pop%d"%x)
              neuroml_Golgi_pop_array.append(Golgi_pop)
	      net.populations.append(Golgi_pop)


	   


           cell_position_array=[]
           
           for cell_population in range(cell_array[0]):
               
	       cell_position_array.append(np.zeros([cell_array[cell_population+1][1],3]))
               
           
           
           if localization_type=="random":
              for cell_pop in range(cell_array[0]):
                  for cell in range(cell_array[cell_pop+1][1]):
	             
	              X=random.random()
	              Y=random.random()
	              Z=random.random()
                      cell_position_array[cell_pop][cell,0]=x_dim*X
                      cell_position_array[cell_pop][cell,1]=y_dim*Y
                      cell_position_array[cell_pop][cell,2]=z_dim*Z
                      print cell_position_array[cell_pop][cell,0], cell_position_array[cell_pop][cell,1], cell_position_array[cell_pop][cell,2]
	   
             #Define GapJunction and ElectricalProjection elements; however inclusion of these elements in the nml file is conditional (see below)

             # for now only assume one Golgi population and code firstly for a uniform-random connectivity case; then extend the model with different connectivity rules
           

           #block(s) for explicit inputs
           if input_information[0]=="testing":
              for pop in range(0,len(Golgi_pop_index_array)):
                 randomly_select_target_cells=random.sample(range(cell_array[pop+1][1]),int(round(fraction_of_cells_to_target_in_pop*cell_array[pop+1][1])))
                 for i in randomly_select_target_cells:
                     for pulse_x in range(0,len(input_information)-2):
                         Inp = neuroml.ExplicitInput(target="%s[%d]"%(Golgi_pop_index_array[pop],i),input="Input_%d"%pulse_x,destination="synapses")
                         net.explicit_inputs.append(Inp)
           #block for explicit inputs end
           
           # as a template: if var in input_information is ["variable basal firing rate",["amplitude distribution","gaussian",[100],[50],"nA"],["offset distribution","uniform",[50],[100],"ms"]]  
           if "testing" not in input_information:      
             for input_group in input_information:
                if "variable basal firing rate"==input_group[0]:
                  for var in input_group:
                      if type(var) is list:
                         if var[0]=="amplitude distribution":
                            gaussian_model=False
                            uniform_model=False
                            constant_model=False
                            if "gaussian" in var:
                               pop_average_array=[]
                               pop_variance_array=[]
                               gaussian_model=True
                               for pop_var in range(0,len(var[2])):
                                   pop_average_array.append(var[2][pop_var])
                                   pop_variance_array.append(var[3][pop_var])
                               units=var[4]
                            if "uniform" in var:
                               pop_left_bound=[]
                               pop_right_bound=[]
                               uniform_model=True
                               for pop_var in range(0,len(var[2])):
                                   pop_left_bound.append(var[2][pop_var])
                                   pop_right_bound.append(var[3][pop_var])
                               units=var[4]
                            if "constant" in var:
                               pop_amplitude=[]
                               constant_model=True
                               for pop_var in range(0,len(var[2])):
                                   pop_amplitude.append(var[2][pop_var])
                               units=var[3]
                         if var[0]=="offset distribution":
                            offset_gaussian_model=False
                            offset_uniform_model=False
                            offset_constant_model=False
                            if "gaussian" in var:
                                offset_gaussian_model=True
                                pop_offset_average=[]
                                pop_offset_variance=[]
                                for pop_var in range(0,len(var[2])):
                                    pop_offset_average.append(var[2][pop_var])
                                    pop_offset_variance.append(var[3][pop_var])
                                offset_units=var[4]
                            if "constant" in var:
                                pop_offset=[]
                                offset_constant_model=True
                                for pop_var in range(0,len(var[2])):
                                    pop_offset.append(var[2][pop_var])
                                offset_units=var[3]
                            if "uniform" in var:
                                offset_uniform_model=True
                                pop_offset_left_bound=[]
                                pop_offset_right_bound=[]
                                for pop_var in range(0,len(var[2])):
                                    pop_offset_left_bound.append(var[2][pop_var])
                                    pop_offset_right_bound.append(var[3][pop_var])
                                offset_units=var[4]
                         
                  for pop in range(0,len(Golgi_pop_index_array)):
                      for cell in range(cell_array[pop+1][1]):
                          if gaussian_model:
                             amp=random.gauss(pop_average_array[pop],pop_variance_array[pop])
                          if uniform_model:
                             amp=random.uniform(pop_left_bound[pop],pop_right_bound[pop])
                          if constant_model:
                             amp=pop_amplitude[pop]
                          if offset_gaussian_model:
                             offset=random.gauss(pop_offset_average[pop],pop_offset_variance[pop])
                          if offset_uniform_model:
                             offset=random.uniform(pop_offset_left_bound[pop],pop_offset_right_bound[pop])
                          if offset_constant_model:
                             offset=pop_offset[pop]
                          Pulse_generator_variable=neuroml.PulseGenerator(id="Input_%d%d"%(pop,cell),delay="%f%s"%(offset,offset_units),duration="%f%s"%(simulation_parameters[1]-offset,offset_units),amplitude="%f%s"%(amp,units))
	                  nml_doc.pulse_generators.append(Pulse_generator_variable)
	                  Inp = neuroml.ExplicitInput(target="%s[%d]"%(Golgi_pop_index_array[pop],cell),input="Input_%d%d"%(pop,cell),destination="synapses")
                          net.explicit_inputs.append(Inp)
	              

           
           if connectivity_information[0]=="Vervaeke_2012_based":
               cell_names=[]
               for cell in range(cell_array[0]):
                   cell_names.append(cell_array[cell+1][0])
               
               gap_counter=0
               initial_projection_counter=0
               pairs=[]                                                    
               for pair in range(0,len(connectivity_information[5])):
                   members=[]
                   members.append(connectivity_information[5][pair][0])  
                   members.append(connectivity_information[5][pair][1])
                   pairs.append(members)
               pairs_gap_conductance=[]
               for pair in range(0,len(connectivity_information[2])):
                   members=[]
                   members.append(connectivity_information[5][pair][0])  
                   members.append(connectivity_information[5][pair][1])
                   pairs_gap_conductance.append(members)
               for pre_pop_index in range(0,len(Golgi_pop_index_array)):
                       
                   if connectivity_information[3][pre_pop_index]=="segment groups and segments":
                      pre_pop_target_segment_array=extract_morphology_information([cell_names[pre_pop_index]],\
                                                                                          ["segment groups",connectivity_information[4][pre_pop_index][0]])
                   if connectivity_information[3][pre_pop_index]=="segments and subsegments":
                      pre_pop_target_segment_array=extract_morphology_information([cell_names[pre_pop_index]],\
                                                                                          ["segments",connectivity_information[4][pre_pop_index][0]])
                   for post_pop_index in range(0,len(Golgi_pop_index_array)):
                       if connectivity_information[3][post_pop_index]=="segment groups and segments":
                          post_pop_target_segment_array=extract_morphology_information([cell_names[post_pop_index]],\
                                                                                          ["segment groups",connectivity_information[4][post_pop_index][0]])
                       if connectivity_information[3][post_pop_index]=="segments and subsegments":
                          post_pop_target_segment_array=extract_morphology_information([cell_names[post_pop_index]],\
                                                                                          ["segments",connectivity_information[4][post_pop_index][0]])                                                
                       if pre_pop_index<=post_pop_index:
                          proj = neuroml.ElectricalProjection(id="proj%d"%initial_projection_counter,
		                presynaptic_population=Golgi_pop_index_array[pre_pop_index], 
		                postsynaptic_population=Golgi_pop_index_array[post_pop_index])
                          initial_projection_counter+=1
                          projection_counter=0
	                  conn_count = 0
                          pre_cell_positions=cell_position_array[pre_pop_index]
                          post_cell_positions=cell_position_array[post_pop_index]
                          pairs=[]                                                    
                          for pair in range(0,len(pairs)):
                              if collections.Counter(pairs[pair])==collections.Counter([cell_names[pre_pop_index],cell_names[post_pop_index]] ):
                                 if connectivity_information[5][pair][2]=="constant number of GJ contacts per pair":
                                    no_of_GJcon_per_pair=connectivity_information[5][pair][3]
                                 if connectivity_information[5][pair][2]=="variable number of GJ contacts per pair":
                                    if connectivity_information[5][pair][3]=="binomial":
                                       no_of_GJcon_per_pair=np.random.binomial(connectivity_information[5][pair][5],connectivity_information[5][pair][4]/connectivity_information[5][pair][5])

                          conductance_scaling=1
                          if connectivity_information[-2][0]=="testing":
                             conductance_scaling=connectivity_information[-2][1]

                          variable_conductance_parameters_of_cell_pairs=[]

                          for pair in range(0,len(pairs_gap_conductance)):
                              if collections.Counter(pairs_gap_conductance[pair])==collections.Counter([ cell_names[pre_pop_index],cell_names[post_pop_index]] ):
                                 pair_index=pair
                                 if connectivity_information[2][pair][2]=="constant conductance":
                                    conductance_value=connectivity_information[2][pair][3]
                                    conductance_units=connectivity_information[2][pair][4]
                                    gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%f%s"%(conductance_value*conductance_scaling,conductance_units)) 
                                    gap_id_per_pair="gap_junction%d"%gap_counter        
                                    nml_doc.gap_junctions.append(gap_junction)
		                    gap_counter+=1
                                    
                          for Pre_cell in range(cell_array[pre_pop_index+1][1]):
                              for Post_cell in range(cell_array[post_pop_index+1][1]):
                                  if pre_pop_index==post_pop_index:
                                     compare_ids=Pre_cell < Post_cell
                                  if pre_pop_index < post_pop_index:
                                     compare_ids=Pre_cell<=Post_cell
                                  if compare_ids:
                                     distance_between_cells=distance(pre_cell_positions[Pre_cell],post_cell_positions[Post_cell])/connectivity_information[1]
                                     if random.random() <connection_probability_vervaeke_2010(distance_between_cells):
                                        if connectivity_information[3][pre_pop_index]=="segment groups and segments":
                                           pre_target_points=get_unique_target_points(pre_pop_target_segment_array,"segment groups and segments",\
                                                                                   connectivity_information[4][post_pop_index],no_of_GJcon_per_pair)
                                        if connectivity_information[3][pre_pop_index]=="segments and subsegments":
                                           pre_target_points=get_unique_target_points(pre_pop_target_segment_array,"segments and subsegments",\
                                                                                connectivity_information[4][post_pop_index],no_of_GJcon_per_pair) 
       
                                        if connectivity_information[3][post_pop_index]=="segment groups and segments":
                                           post_targeting_mode="segment groups and segments"
                                        if connectivity_information[3][post_pop_index]=="segments and subsegments":
                                           post_targeting_mode="segments and subsegments"
                                        for pre_target_point in range(0,len(pre_target_points)):
                                            if connectivity_information[-1][0]== "maximal connection length":
                                               if connectivity_information[-1][1] != None:
                                                  x=0
                                                  while x==0:
                                                      post_target_point=get_unique_target_points(post_pop_target_segment_array,post_targeting_mode,\
                                                                                connectivity_information[4][post_pop_index],1) 
                                                      if get_3D_connection_length(cell_names,cell_position_array,pre_pop_index,post_pop_index,Pre_cell,\
                                                         Post_cell,pre_target_points[pre_target_point,0],post_target_point[0,0],\
                                                         pre_target_points[pre_target_point,1],post_target_point[0,1]) <=connectivity_information[-1][1]:
                                                         x=1
                                                  Pre_segment_id=pre_target_points[pre_target_point,0]
                                                  Post_segment_id=post_target_point[0,0]
                                                  Pre_fraction=pre_target_points[pre_target_point,1]
                                                  Post_fraction=post_target_point[0,1] 

                                                  if connectivity_information[2][pair_index][2]=="variable conductance":
                                                     if string.lower(connectivity_information[2][pair][2])=="gaussian":
                                                        gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%f%s"%(connectivity_information[2][pair_index][3]*conductance_scaling,connectivity_information[2][pair_index][4]))
                                                        nml_doc.gap_junctions.append(gap_junction)
		                                        gap_counter+=1
                                                        #other options can be added such as gamma distribution
                                                     conn =neuroml.ElectricalConnection(id=conn_count,pre_cell="%d"%Pre_cell,post_cell="%d"%Post_cell,synapse=gap,\
                                                             pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                                                             pre_fraction_along="%f"%random.random(),post_fraction_along="%f"%random.random())
                                            
		                                     if projection_counter==0:
                                                        net.electrical_projections.append(proj)
                                                        projection_counter+=1
                                               
		                                     proj.electrical_connections.append(conn)
		                                     conn_count+=1
                                                     x=1
                                                  if connectivity_information[2][pair_index][2]=="constant conductance":
                                                     conn =neuroml.ElectricalConnection(id=conn_count,pre_cell="%d"%Pre_cell,post_cell="%d"%Post_cell,synapse=gap_id_per_pair,\
                                                              pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                                                              pre_fraction_along="%f"%Pre_fraction,post_fraction_along="%f"%Post_fraction)
                                            
		                                     if projection_counter==0:
                                                        net.electrical_projections.append(proj)
                                                        projection_counter+=1
                                               
		                                     proj.electrical_connections.append(conn)
		                                     conn_count+=1
                                                     x=1
                                                  else:
                                                     post_target_point=get_unique_target_points(post_pop_target_segment_array,post_targeting_mode,\
                                                                                connectivity_information[4][post_pop_index],1) 
                                                     Pre_segment_id=pre_target_points[pre_target_point,0]
                                                     Post_segment_id=post_target_point[0,0]
                                                     Pre_fraction=pre_target_points[pre_target_point,1]
                                                     Post_fraction=post_target_point[0,1] 

                                                     if connectivity_information[2][pair_index][2]=="variable conductance":
                                                        if string.lower(connectivity_information[2][pair][2])=="gaussian":
                                                           gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%f%s"%(connectivity_information[2][pair_index][3]*conductance_scaling,connectivity_information[2][pair_index][4]))
                                                           nml_doc.gap_junctions.append(gap_junction)
		                                           gap_counter+=1
                                                        #other options can be added such as gamma distribution
                                                        conn =neuroml.ElectricalConnection(id=conn_count,pre_cell="%d"%Pre_cell,post_cell="%d"%Post_cell,synapse=gap,\
                                                             pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                                                             pre_fraction_along="%f"%Pre_fraction,post_fraction_along="%f"%Post_fraction)
                                            
		                                        if projection_counter==0:
                                                           net.electrical_projections.append(proj)
                                                           projection_counter+=1
                                               
		                                        proj.electrical_connections.append(conn)
		                                        conn_count+=1
                                                        x=1

                                                     if connectivity_information[2][pair_index][2]=="constant conductance":
                                                        conn =neuroml.ElectricalConnection(id=conn_count,pre_cell="%d"%Pre_cell,post_cell="%d"%Post_cell,synapse=gap_id_per_pair,\
                                                              pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                                                              pre_fraction_along="%f"%Pre_fraction,post_fraction_along="%f"%Post_fraction)
                                            
		                                        if projection_counter==0:
                                                           net.electrical_projections.append(proj)
                                                           projection_counter+=1
                                               
		                                        proj.electrical_connections.append(conn)
		                                        conn_count+=1
                                                        x=1

           if connectivity_information[0]=="Vervaeke_2010_multi_compartment":
               cell_names=[]
               for cell in range(cell_array[0]):
                   cell_names.append(cell_array[cell+1][0])
               
               gap_counter=0
               initial_projection_counter=0
               segment_group_list=[]
               #for the time beging V2010 uses probabilities of targeting specific segment groups and a pool of segments per segment group; sufficient as for 2010-     detailed model
               segment_group_list.append("segment groups")
               for cell_population in range(0,len(Golgi_pop_index_array)):
                   segment_group_list.append(connectivity_information[cell_population+2][0])
               target_segment_array=extract_morphology_information(cell_names,segment_group_list)
               
               for pre_pop_index in range(0,len(Golgi_pop_index_array)):
                   
                   for post_pop_index in range(0,len(Golgi_pop_index_array)):
                       if pre_pop_index<=post_pop_index:
                          proj = neuroml.ElectricalProjection(id="proj%d"%initial_projection_counter,
		                presynaptic_population=Golgi_pop_index_array[pre_pop_index], 
		                postsynaptic_population=Golgi_pop_index_array[post_pop_index])
                          
                          initial_projection_counter+=1
                          projection_counter=0
	                  conn_count = 0
                          pre_cell_positions=cell_position_array[pre_pop_index]
                          post_cell_positions=cell_position_array[post_pop_index]
                          for Pre_cell in range(cell_array[pre_pop_index+1][1]):
                          #scripted so that to avoid inclusion of projection and gap_junction/synapse components if there are no connections; otherwise the mod files are not compiled.
                                  for Post_cell in range(cell_array[post_pop_index+1][1]):
                                      if pre_pop_index==post_pop_index:
                                         compare_ids=Pre_cell < Post_cell
                                      if pre_pop_index < post_pop_index:
                                         compare_ids=Pre_cell<=Post_cell
                                      if compare_ids:
                                         distance_between_cells=distance(pre_cell_positions[Pre_cell],post_cell_positions[Post_cell])/connectivity_information[1]
                                         if random.random() <connection_probability_vervaeke_2010(distance_between_cells):
                                            if connectivity_information[-1][0]== "maximal connection length":
                                               if connectivity_information[-1][1] != None:
                                                  z=0
                                                  while z==0:
                                                      x=0
                                                      while x==0:
                                                          pre_segment_group=random.sample(range(0,len(connectivity_information[pre_pop_index+2][0])),1)
                                                          pre_segment_group=pre_segment_group[0]
                                                          if random.random() < connectivity_information[pre_pop_index+2][1][pre_segment_group]:
                                                             pre_group=connectivity_information[pre_pop_index+2][0][pre_segment_group]
                                                             x=1
                                                      y=0
                                                      while y==0:
                                                          post_segment_group=random.sample(range(0,len(connectivity_information[post_pop_index+2][0])),1)
                                                          post_segment_group=post_segment_group[0]
                                                          if random.random() < connectivity_information[post_pop_index+2][1][post_segment_group]:
                                                             post_group=connectivity_information[post_pop_index+2][0][post_segment_group]
                                                             y=1
                                                      for segment_group in range(0,len(target_segment_array[pre_pop_index])):
                                                          if target_segment_array[pre_pop_index][segment_group+1][0]==pre_group:
                                                             pre_segment_ids=target_segment_array[pre_pop_index][segment_group+1][1:]
                                                             break
                                                      for segment_group in range(0,len(target_segment_array[post_pop_index])):
                                                          if target_segment_array[post_pop_index][segment_group+1][0]==post_group:
                                                             post_segment_ids=target_segment_array[post_pop_index][segment_group+1][1:]
                                                             break
                                            
                                                      Pre_segment_id=random.sample(pre_segment_ids,1)
                                                      Pre_segment_id=Pre_segment_id[0]
                                                      Post_segment_id=random.sample(post_segment_ids,1)
                                                      Post_segment_id=Post_segment_id[0]
                                                      pre_fraction=random.random()
                                                      post_fraction=random.random()
                                                      if get_3D_connection_length(cell_names,cell_position_array,pre_pop_index,post_pop_index,Pre_cell,\
                                                         Post_cell,Pre_segment_id,Post_segment_id,pre_fraction,post_fraction) <=connectivity_information[-1][1]:
                                                         z=1
                                               else:
                                                  x=0
                                                  while x==0:
                                                      pre_segment_group=random.sample(range(0,len(connectivity_information[pre_pop_index+2][0])),1)
                                                      pre_segment_group=pre_segment_group[0]
                                                      if random.random() < connectivity_information[pre_pop_index+2][1][pre_segment_group]:
                                                         pre_group=connectivity_information[pre_pop_index+2][0][pre_segment_group]
                                                         x=1
                                                   
                                                  y=0
                                                  while y==0:
                                                      post_segment_group=random.sample(range(0,len(connectivity_information[post_pop_index+2][0])),1)
                                                      post_segment_group=post_segment_group[0]
                                                      if random.random() < connectivity_information[post_pop_index+2][1][post_segment_group]:
                                                         post_group=connectivity_information[post_pop_index+2][0][post_segment_group]
                                                         y=1
                                                                   
                                                  for segment_group in range(0,len(target_segment_array[pre_pop_index])):
                                                      if target_segment_array[pre_pop_index][segment_group+1][0]==pre_group:
                                                         pre_segment_ids=target_segment_array[pre_pop_index][segment_group+1][1:]
                                                         break
                                                  for segment_group in range(0,len(target_segment_array[post_pop_index])):
                                                      if target_segment_array[post_pop_index][segment_group+1][0]==post_group:
                                                         post_segment_ids=target_segment_array[post_pop_index][segment_group+1][1:]
                                                         break
                                            
                                                  Pre_segment_id=random.sample(pre_segment_ids,1)
                                                  Pre_segment_id=Pre_segment_id[0]
                                                  Post_segment_id=random.sample(post_segment_ids,1)
                                                  Post_segment_id=Post_segment_id[0]
                                                  pre_fraction=random.random()
                                                  post_fraction=random.random()
                                            
                                            if connectivity_information[-2][0]=="testing":
                                               gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%fpS"%(synaptic_weight_vervaeke_2010(distance_between_cells)*connectivity_information[-2][1]))
                                            else:
                                               gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%fpS"%synaptic_weight_vervaeke_2010(distance_between_cells))
                                            
                                            conn =neuroml.ElectricalConnection(id=conn_count,pre_cell="%d"%Pre_cell,post_cell="%d"%Post_cell,synapse=gap_junction.id,\
                                                                             pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                                                                             pre_fraction_along="%f"%random.random(),post_fraction_along="%f"%random.random())
                                            
		                            nml_doc.gap_junctions.append(gap_junction)
		                            gap_counter+=1
		                            if projection_counter==0:
                                               net.electrical_projections.append(proj)
                                               projection_counter+=1
                                               
		                            proj.electrical_connections.append(conn)
		                            conn_count+=1
               




           if connectivity_information[0]=="Vervaeke_2010_one_compartment":
               gap_counter=0
               initial_projection_counter=0
               for pre_pop_index in range(0,len(Golgi_pop_index_array)):
                   for post_pop_index in range(0,len(Golgi_pop_index_array)):
                       if pre_pop_index<=post_pop_index:
                          proj = neuroml.ElectricalProjection(id="proj%d"%initial_projection_counter,
		                presynaptic_population=Golgi_pop_index_array[pre_pop_index], 
		                postsynaptic_population=Golgi_pop_index_array[post_pop_index])
                          
                          initial_projection_counter+=1
                          projection_counter=0
	                  conn_count = 0
                          pre_cell_positions=cell_position_array[pre_pop_index]
                          post_cell_positions=cell_position_array[post_pop_index]
                          for Pre_cell in range(cell_array[pre_pop_index+1][1]):
                          #scripted so that to avoid inclusion of projection and gap_junction/synapse components if there are no connections; otherwise the mod files are not compiled.
                                  for Post_cell in range(cell_array[post_pop_index+1][1]):
                                      if pre_pop_index==post_pop_index:
                                         compare_ids=Pre_cell <Post_cell
                                      if pre_pop_index<post_pop_index:
                                         compare_ids=Pre_cell<=Post_cell                         
                                      if compare_ids:
                                         distance_between_cells=distance(pre_cell_positions[Pre_cell],post_cell_positions[Post_cell])/connectivity_information[1]
                                         if random.random() <connection_probability_vervaeke_2010(distance_between_cells):
                                            gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%fpS"%synaptic_weight_vervaeke_2010(distance_between_cells))
                                            conn =neuroml.ElectricalConnection(id=conn_count,pre_cell="%d"%Pre_cell,post_cell="%d"%Post_cell,synapse=gap_junction.id)
                                            
		                            nml_doc.gap_junctions.append(gap_junction)
		                            gap_counter+=1
		                            if projection_counter==0:
                                               net.electrical_projections.append(proj)
                                               projection_counter+=1
                                               
		                            proj.electrical_connections.append(conn)
		                            conn_count+=1
               
                

           
           if connectivity_information[0]=="uniform random":
               gap_junction0 = neuroml.GapJunction(id="gap_junction0", conductance=connectivity_information[1][1])
               gap_counter=0
               initial_projection_counter=0
               for pre_pop_index in range(0,len(Golgi_pop_index_array)):
                   for post_pop_index in range(0,len(Golgi_pop_index_array)):
                       if pre_pop_index<=post_pop_index:
                          proj = neuroml.ElectricalProjection(id="proj%d"%initial_projection_counter,
		                presynaptic_population=Golgi_pop_index_array[pre_pop_index], 
		                postsynaptic_population=Golgi_pop_index_array[post_pop_index])
                          initial_projection_counter+=1
                          projection_counter=0
                          conn_count=0
                          for Pre_cell in range(cell_array[pre_pop_index+1][1]):
                          # randomly Connect cells with defined probability for now; scripted so that to avoid inclusion of projection and gap_junction/synapse components if there are no connections; otherwise the mod files are not compiled.
                                  for Post_cell in range(cell_array[post_pop_index+1][1]):
                                      if pre_pop_index==post_pop_index:
                                         compare_ids=Pre_cell < Post_cell
                                      if pre_pop_index < post_pop_index:
                                         compare_ids=Pre_cell<=Post_cell
                                      if compare_ids:
                                         if random.random() < connectivity_information[1][0]:
                                            conn =neuroml.ElectricalConnection(id=conn_count,pre_cell="%d"%Pre_cell,post_cell="%d"%Post_cell,synapse=gap_junction0.id)
                                            if gap_counter==0:
		                               nml_doc.gap_junctions.append(gap_junction0)
		                               gap_counter+=1
		                            if projection_counter==0:
                                               net.electrical_projections.append(proj)
                                               projection_counter+=1
                                               
		                            proj.electrical_connections.append(conn)
		                            conn_count+=1
              
               
                                         

                                     

               
             
           


             
                      
	  

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
        if output[1]==True:
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
        
	if string.lower(population_type) =="list":
	   for x in range(cell_array[0]):
	       disp = "display_voltages%d"%x
	       ls.create_display(disp, "Voltages Golgi_pop%d"%x, "-75", "50")
	       
	       max_traces = 20
	       if cell_array[x+1][1]<=max_traces:
	          for i in range(cell_array[x+1][1]):
		      quantity = "%s/%i/%s/v"%(Golgi_pop_index_array[x], i,cell_array[x+1][0])
	              ls.add_line_to_display(disp, "../%s/%i: Vm"%(Golgi_pop_index_array[x],i), quantity, "1mV", pynml.get_next_hex_color())
                      of0 = 'Volts%d_file0_%d'%(x,i)
                      ls.create_output_file(of0, "simulations/%s/sim%d/Golgi_pop%d_cell%d.dat"%(simulation_parameters[3],simulation_parameters[4],x,i))
		      ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
					   
	       else:
		  randomly_select_displayed_cells=random.sample(range(cell_array[x+1][1]),max_traces)
		  for y in randomly_select_displayed_cells:
		      quantity = "%s/%i/%s/v"%(Golgi_pop_index_array[x], y,cell_array[x+1][0])
		      ls.add_line_to_display(disp, "../%s/%i: Vm"%(Golgi_pop_index_array[x],y), quantity, "1mV", pynml.get_next_hex_color())
					      
		  for i in range(cell_array[x+1][1]):
		      quantity = "%s/%i/%s/v"%(Golgi_pop_index_array[x], i,cell_array[x+1][0])
                      of0 = 'Volts%d_file0_%d'%(x,i)
                      ls.create_output_file(of0, "simulations/%s/sim%d/Golgi_pop%d_cell%d.dat"%(simulation_parameters[3],simulation_parameters[4],x,i))
		      ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
        else:
	    for x in range(cell_array[0]):
	        disp = "display_voltages%d"%x
	        ls.create_display(disp, "Voltages Golgi_pop%d"%x, "-75", "50")
	        max_traces = 20
	        if cell_array[x+1][1]<=max_traces:
		   for i in range(cell_array[x+1][1]):
		       quantity = "%s[%i]/v"%(Golgi_pop_index_array[x], i)
		       ls.add_line_to_display(disp, "%s[%i]: Vm"%(Golgi_pop_index_array[x],i), quantity, "1mV", pynml.get_next_hex_color())
                       of0 = 'Volts%d_file0_%d'%(x,i)
	               ls.create_output_file(of0, "simulations/%s/sim%d/Golgi_pop%d_cell%d.dat"%(simulation_parameters[3],simulation_parameters[4],x,i))
		       ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
	        else:
		   randomly_select_displayed_cells=random.sample(range(cell_array[x+1][1]),max_traces)
		   for y in randomly_select_displayed_cells:
		       quantity = "%s[%i]/v"%(Golgi_pop_index_array[x], y)
		       ls.add_line_to_display(disp, "%s[%i]: Vm"%(Golgi_pop_index_array[x],y), quantity, "1mV", pynml.get_next_hex_color())
					      
		   for i in range(cell_array[x+1][1]):
		       quantity = "%s[%i]/v"%(Golgi_pop_index_array[x], i)
		       of0 = 'Volts%d_file0_%d'%(x,i)
		       ls.create_output_file(of0, "simulations/%s/sim%d/Golgi_pop%d_cell%d.dat"%(simulation_parameters[3],simulation_parameters[4],x,i))
		       ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
	# save LEMS file
        lems_file_name = ls.save_to_file()
        if string.lower(simulation_parameters[6][0])=="plot":
           if simulation_parameters[6][1]==True:
              if simulation_parameters[2]=="jNeuroML":
	         results1 = pynml.run_lems_with_jneuroml(lems_file_name, nogui=True, load_saved_data=True, plot=True)
                 print("Finished building network and running simulation with %s"%simulation_parameters[2])
              elif simulation_parameters[2]=="jNeuroML_NEURON":
                 results1 = pynml.run_lems_with_jneuroml_neuron(lems_file_name, nogui=True, load_saved_data=True, plot=True)
                 print("Finished building a network and running simulation with %s"%simulation_parameters[2])
              else:
                 print("Finished building a network")
           else:
              if simulation_parameters[2]=="jNeuroML":
	         results1 = pynml.run_lems_with_jneuroml(lems_file_name, nogui=True, load_saved_data=False, plot=False)
                 print("Finished building a network and running simulation with %s"%simulation_parameters[2])
              elif simulation_parameters[2]=="jNeuroML_NEURON":
                 results1 = pynml.run_lems_with_jneuroml_neuron(lems_file_name, nogui=True, load_saved_data=False, plot=False)
                 print("Finished building a network and running simulation with %s"%simulation_parameters[2])
              else:
                 print("Finished building a network")
         

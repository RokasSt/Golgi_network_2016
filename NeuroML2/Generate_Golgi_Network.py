
import neuroml
from pyneuroml import pynml
from pyneuroml.lems.LEMSSimulation import LEMSSimulation
import math
import neuroml.writers as writers
from neuroml.utils import validate_neuroml2
import random
import numpy as np
import string


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
	   for x in range(cell_array[0]):
	      Golgi_pop = neuroml.Population(id="Golgi_pop%d"%x, size =cell_array[x+1][1], type="populationList",
		                  component=cell_array[x+1][0])
	      Golgi_pop_index_array.append("Golgi_pop%d"%x)
              neuroml_Golgi_pop_array.append(Golgi_pop)
	      net.populations.append(Golgi_pop)


	   cell_position_array=[]
           
           for cell_population in range(cell_array[0]):
               
	       cell_position_array.append(np.zeros([cell_array[cell_population+1][1],3]))
               

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
                 
	   

        

           #if connectivity_information[0]=="Vervaeke_2012_based":
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
                                            conn =neuroml.ElectricalConnection(id=conn_count,\
                                                                               pre_cell="../%s/%d/%s"%(Golgi_pop_index_array[pre_pop_index],Pre_cell,cell_array[pre_pop_index+1][0]),\
                                                                               post_cell="../%s/%d/%s"%(Golgi_pop_index_array[post_pop_index],Post_cell,cell_array[post_pop_index+1][0]),\
                                                                               synapse=gap_junction.id)
                                            
		                            nml_doc.gap_junctions.append(gap_junction)
		                            gap_counter+=1
		                            if projection_counter==0:
                                               net.electrical_projections.append(proj)
                                               projection_counter+=1
                                               
		                            proj.electrical_connections.append(conn)
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
                                            if connectivity_information[-1][0]=="testing":
                                               gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%fpS"%(synaptic_weight_vervaeke_2010(distance_between_cells)*connectivity_information[-1][1]))
                                            else:
                                               gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%fpS"%synaptic_weight_vervaeke_2010(distance_between_cells))
                                               gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%fpS"%synaptic_weight_vervaeke_2010(distance_between_cells)*connectivity_information[-1][1])
                                            conn =neuroml.ElectricalConnection(id=conn_count,\
                                                                                pre_cell="../%s/%d/%s"%(Golgi_pop_index_array[pre_pop_index],Pre_cell,cell_array[pre_pop_index+1][0]),\
                                                                              post_cell="../%s/%d/%s"%(Golgi_pop_index_array[post_pop_index],Post_cell,cell_array[post_pop_index+1][0]),\
                                                                               synapse=gap_junction.id,pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                                                                               pre_fraction_along="%f"%random.random(),post_fraction_along="%f"%random.random())
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
                                            conn =neuroml.ElectricalConnection(id=conn_count, \
				   pre_cell="../%s/%d/%s"%(Golgi_pop_index_array[pre_pop_index],Pre_cell,cell_array[pre_pop_index+1][0]),
				   post_cell="../%s/%d/%s"%(Golgi_pop_index_array[post_pop_index],Post_cell,cell_array[post_pop_index+1][0]),synapse=gap_junction0.id)
                                            if gap_counter==0:
		                               nml_doc.gap_junctions.append(gap_junction0)
		                               gap_counter+=1
		                            if projection_counter==0:
                                               net.electrical_projections.append(proj)
                                               projection_counter+=1
                                               
		                            proj.electrical_connections.append(conn)
		                            conn_count+=1
               

	   


        
           if input_information[0]=="testing":
              neuroml_input_array=[]
              for pulse_x in range(0,len(input_information)-2):
                  Input_list=neuroml.InputList(id="Input_list%d"%pulse_x, component="Input_%d"%pulse_x)
                  neuroml_input_array.append(Input_list)
                  net.input_lists.append(Input_list)
              for pop in range(0,len(Golgi_pop_index_array)):
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
           if connectivity_information[0]=="Vervaeke_2012_based":
               cell_names=[]
               for cell in range(cell_array[0]):
                   cell_names.append(cell_array[cell+1][0])
               
               gap_counter=0
               initial_projection_counter=0
               segment_group_list=[]
               segment_group_list.append("segment groups")
               for cell_population in range(0,len(Golgi_pop_index_array)):
                   segment_group_list.append(connectivity_information[cell_population+4][0])
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
                                            if connectivity_information[3]=="segments and subsegments":
                                               x=0
                                               while x==0:
                                                   for pre_segment in range(0,len(connectivity_information[pre_pop_index+4][0])):
                                                       if random.random() < connectivity_information[pre_pop_index+4][1][pre_segment]:
                                                          pre_seg=connectivity_information[pre_pop_index+4][0][pre_segment]
                                                          pre_seg_index=pre_segment
                                                          for post_segment in range(0,len(connectivity_information[post_pop_index+4][0])):
                                                              if random.random() < connectivity_information[post_pop_index+4][1][post_segment]:
                                                                 post_seg=connectivity_information[post_pop_index+4][0][post_segment]
                                                                 post_seg_index=post_segment
                                                                 for segment in range(0,len(target_segment_array[pre_pop_index])-1):
                                                                     if target_segment_array[pre_pop_index][segment+1][0]==pre_seg:
                                                                        pre_segment_ids=target_segment_array[pre_pop_index][segment+1][1:]
                                                                        break
                                                                 for segment in range(0,len(target_segment_array[post_pop_index])-1):
                                                                     if target_segment_array[post_pop_index][segment+1][0]==post_seg:
                                                                        post_segment_ids=target_segment_array[post_pop_index][segment+1][1:]
                                                                        break
                                                                 Pre_segment_id=random.sample(pre_segment_ids,1)
                                                                 Pre_segment_id=Pre_segment_id[0]
                                                                 Post_segment_id=random.sample(post_segment_ids,1)
                                                                 Post_segment_id=Post_segment_id[0]
                                                                 if connectivity_information[2][0]=="constant conductance":
                                                                    gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%f%s"%(connectivity_information[2][1],connectivity_information[2][2]))
                                                                 if connectivity_information[2][0]=="variable conductance":
                                                                    if string.lower(connectivity_information[2][1])=="gaussian":
                                                                       gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%f%s"%(random.gauss(connectivity_information[2][2],connectivity_information[2][3]),connectivity_information[2][4]))
                                                                    #other options can be added such as gamma distribution
                                                                 
                                                                 
                                                                 
                                                                 # maybe better for loops below; probabilities of subsegments will control the average number of GJ contacts per segment 
                                                                 for subseg in range(0,len(connectivity_information[pre_pop_index+4][2][pre_seg_index])):
                                                                     
                                                                     if random.random() < connectivity_information[pre_pop_index+4][2][pre_seg_index][subseg][1]:
                                                                        pre_subseg_id=subseg
                                                                        pre_subseg=connectivity_information[pre_pop_index+4][2][pre_seg_index][subseg][0]
                                                                        for subseg2 in range(0,len(connectivity_information[post_pop_index+4][2][post_seg_index])):
                                                                            if random.random() < connectivity_information[post_pop_index+4][2][post_seg_index][subseg2][1]: 
                                                                               post_subseg_id=subseg2
                                                                               post_subseg=connectivity_information[post_pop_index+4][2][post_seg_index][subseg2][0]
                                                                               
                                                                               pre_fraction_before_pre_subseg=0
                                                                               post_fraction_before_post_subseg=0
                                                                               if pre_subseg_id !=0:
                                                                                  for ind in range(0,pre_subseg_id):
                                                                                      pre_fraction_before_pre_subseg=pre_fraction_before_pre_subseg+connectivity_information[pre_pop_index+4][2][pre_seg_index][ind][0]
                                                                               random_pre_fraction=random.uniform(0,pre_subseg)
                                                                               Pre_fraction_final=random_pre_fraction+pre_fraction_before_pre_subseg


                                                                               if post_subseg_id !=0:
                                                                                  for ind in range(0,post_subseg_id):
                                                                                      post_fraction_before_post_subseg=post_fraction_before_post_subseg+connectivity_information[post_pop_index+4][2][post_seg_index][ind][0]
                                                                               random_post_fraction=random.uniform(0,post_subseg)
                                                                               Post_fraction_final=random_post_fraction+post_fraction_before_post_subseg
                                                                               
                                                                               conn =neuroml.ElectricalConnection(id=conn_count,pre_cell="%d"%Pre_cell,post_cell="%d"%Post_cell,synapse=gap_junction.id,\
                                                                               pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                                                                               pre_fraction_along="%f"%Pre_fraction_final,post_fraction_along="%f"%Post_fraction_final)
                                            
		                                                               nml_doc.gap_junctions.append(gap_junction)
		                                                               gap_counter+=1
		                                                               if projection_counter==0:
                                                                                  net.electrical_projections.append(proj)
                                                                                  projection_counter+=1
                                               
		                                                               proj.electrical_connections.append(conn)
		                                                               conn_count+=1
                                                                               x=1
                                            if connectivity_information[3]=="segment groups and segments":
                                               x=0
                                               while x==0:
                                                   for pre_segment_group in range(0,len(connectivity_information[pre_pop_index+4][0])):
                                                       if random.random() < connectivity_information[pre_pop_index+4][1][pre_segment_group]:
                                                          pre_group=connectivity_information[pre_pop_index+4][0][pre_segment_group]
                                                          for post_segment_group in range(0,len(connectivity_information[post_pop_index+4][0])):
                                                              if random.random() < connectivity_information[post_pop_index+4][1][post_segment_group]:
                                                                 post_group=connectivity_information[post_pop_index+4][0][post_segment_group]
                                                                 for segment_group in range(0,len(target_segment_array[pre_pop_index])-1):
                                                                     if target_segment_array[pre_pop_index][segment_group+1][0]==pre_group:
                                                                        pre_segment_ids=target_segment_array[pre_pop_index][segment_group+1][1:]
                                                                        break
                                                                 for segment_group in range(0,len(target_segment_array[post_pop_index])-1):
                                                                     if target_segment_array[post_pop_index][segment_group+1][0]==post_group:
                                                                        post_segment_ids=target_segment_array[post_pop_index][segment_group+1][1:]
                                                                        break
                                                                 Pre_segment_id=random.sample(pre_segment_ids,1)
                                                                 Pre_segment_id=Pre_segment_id[0]
                                                                 Post_segment_id=random.sample(post_segment_ids,1)
                                                                 Post_segment_id=Post_segment_id[0]
                                                                 if connectivity_information[2][0]=="constant conductance":
                                                                    gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%f%s"%(connectivity_information[2][1],connectivity_information[2][2]))
                                                                 if connectivity_information[2][0]=="variable conductance":
                                                                    if connectivity_information[2][1]=="gaussian":
                                                                       gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%f%s"%(random.gauss(connectivity_information[2][2],connectivity_information[2][3]),connectivity_information[2][4]))
                                                                    #other options can be added such as gamma distribution
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
                                                                 x=1
                                                                 
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
                                         compare_ids=Pre_cell < Post_cell
                                      if pre_pop_index < post_pop_index:
                                         compare_ids=Pre_cell<=Post_cell
                                      if compare_ids:
                                         distance_between_cells=distance(pre_cell_positions[Pre_cell],post_cell_positions[Post_cell])/connectivity_information[1]
                                         if random.random() <connection_probability_vervaeke_2010(distance_between_cells):
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
                                                       
                                                                   
                                            for segment_group in range(0,len(target_segment_array[pre_pop_index])-1):
                                                if target_segment_array[pre_pop_index][segment_group+1][0]==pre_group:
                                                   pre_segment_ids=target_segment_array[pre_pop_index][segment_group+1][1:]
                                                   break
                                            for segment_group in range(0,len(target_segment_array[post_pop_index])-1):
                                                if target_segment_array[post_pop_index][segment_group+1][0]==post_group:
                                                   post_segment_ids=target_segment_array[post_pop_index][segment_group+1][1:]
                                                   break
                                            Pre_segment_id=random.sample(pre_segment_ids,1)
                                            Pre_segment_id=Pre_segment_id[0]
                                            Post_segment_id=random.sample(post_segment_ids,1)
                                            Post_segment_id=Post_segment_id[0]
                                            if connectivity_information[-1][0]=="testing":
                                               gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%fpS"%(synaptic_weight_vervaeke_2010(distance_between_cells)*connectivity_information[-1][1]))
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
              if simulation_parameters[2]=="jNeuroML_NEURON":
                 results1 = pynml.run_lems_with_jneuroml_neuron(lems_file_name, nogui=True, load_saved_data=True, plot=True)
           else:
              if simulation_parameters[2]=="jNeuroML":
	         results1 = pynml.run_lems_with_jneuroml(lems_file_name, nogui=True, load_saved_data=False, plot=False)
              if simulation_parameters[2]=="jNeuroML_NEURON":
                 results1 = pynml.run_lems_with_jneuroml_neuron(lems_file_name, nogui=True, load_saved_data=False, plot=False)
         

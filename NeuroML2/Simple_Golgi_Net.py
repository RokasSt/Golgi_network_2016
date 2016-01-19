
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

### a main script for generating and running golgi cell network
def generate_and_run_golgi_cell_net(ref,cell_array,location_array, connectivity_information,input_information,simulation_parameters,population_type):
        
        
        random.seed(12345)
        nml_doc = neuroml.NeuroMLDocument(id=ref)
        #cell_array will have to include cell_types and no_of_cells
        #connectivity_information is a list of lists that will have to include connectivity parameters; now code only for a random configuration with parameters connection_probability and conductance_strength

     
        for x in range(cell_array[0]):
            include_cell=neuroml.IncludeType(href="%s.cell.nml"%cell_array[x+1][0])
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
                 
	   

             #Define GapJunction and ElectricalProjection elements; however inclusion of these elements in the nml file is conditional (see below)

             #For now assume only one Golgi population and code firstly for a uniform-random connectivity case; then extend the model with different connectivity rules

           if connectivity_information[0]=="uniform random":
               gap_junction0 = neuroml.GapJunction(id="gap_junction0", conductance=connectivity_information[1][1])
               neuroml_projection_array=[]
               initial_projection_counter=0
               for pre_pop_index in range(0,len(Golgi_pop_index_array)):
                   for post_pop_index in range(0,len(Golgi_pop_index_array)):
                       if pre_pop_index<=post_pop_index:
                          proj = neuroml.ElectricalProjection(id="proj%d"%initial_projection_counter,
		                presynaptic_population=Golgi_pop_index_array[pre_pop_index], 
		                postsynaptic_population=Golgi_pop_index_array[post_pop_index])
                          neuroml_projection_array.append(proj)
                          initial_projection_counter+=1

               gap_counter=0
               for proj_index in range(initial_projection_counter):
                   
	           projection_counter=0
	           conn_count = 0
	           for pre_pop_index in range(0,len(Golgi_pop_index_array)):
                       for post_pop_Index in range(0,len(Golgi_pop_index_array)):
                           if pre_pop_index<=post_pop_index:
                              for pre_cell in range(cell_array[pre_pop_index+1][1]):
                          # randomly Connect cells with defined probability for now; scripted so that to avoid inclusion of projection and gap_junction/synapse components if there are no connections; otherwise the mod files are not compiled.
                                  for post_cell in range(cell_array[post_pop_index+1][1]):
                                      if pre_cell<post_cell:
                                         if random.random() < connectivity_information[1][0]:
                                            conn =neuroml.ElectricalConnection(id=conn_count, \
				   pre_cell="../%s/%d/%s"%(Golgi_pop_index_array[pre_pop_index],pre_cell,cell_array[pre_pop_index+1][0]),
				   post_cell="../%s/%d/%s"%(Golgi_pop_index_array[post_pop_index],post_cell,cell_array[post_pop_index+1][0]),synapse=gap_junction0.id)
                                            if gap_counter==0:
		                               nml_doc.gap_junctions.append(gap_junction0)
		                               gap_counter+=1
		                            if projection_counter==0:
                                               net.electrical_projections.append(neuroml_projection_array[proj_index])
                                               projection_counter+=1
                                               projection=neuroml_projection_array[proj_index]
		                            projection.electrical_connections.append(conn)
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


           if connectivity_information[0]=="Vervaeke_2010_one_compartment":
               neuroml_projection_array=[]
               initial_projection_counter=0
               for pre_pop_index in range(0,len(Golgi_pop_index_array)):
                   for post_pop_index in range(0,len(Golgi_pop_index_array)):
                       if pre_pop_index<=post_pop_index:
                          proj = neuroml.ElectricalProjection(id="proj%d"%initial_projection_counter,
		                presynaptic_population=Golgi_pop_index_array[pre_pop_index], 
		                postsynaptic_population=Golgi_pop_index_array[post_pop_index])
                          neuroml_projection_array.append(proj)
                          initial_projection_counter+=1
               gap_counter=0
               for proj_index in range(initial_projection_counter):
                   
	           projection_counter=0
	           conn_count = 0
	           for pre_pop_index in range(0,len(Golgi_pop_index_array)):
                       for post_pop_index in range(0,len(Golgi_pop_index_array)):
                           if pre_pop_index<=post_pop_index:
                              pre_cell_positions=cell_position_array[pre_pop_index]
                              post_cell_positions=cell_position_array[post_pop_index]
                              for Pre_cell in range(cell_array[pre_pop_index+1][1]):
                          # randomly Connect cells with defined probability for now; scripted so that to avoid inclusion of projection and gap_junction/synapse components if there are no connections; otherwise the mod files are not compiled.
                                  for Post_cell in range(cell_array[post_pop_index+1][1]):
                                      if Pre_cell<Post_cell:
                                         distance_between_cells=distance(pre_cell_positions[Pre_cell],post_cell_positions[Post_cell])/connectivity_information[1]
                                         if random.random() <connection_probability_vervaeke_2010(distance_between_cells):
                                            conn =neuroml.ElectricalConnection(id=conn_count,pre_cell="%d"%Pre_cell,post_cell="%d"%Post_cell,synapse=gap_junction0.id)
                                            gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%fnS"%synaptic_weight_vervaeke_2010(distance_between_cells))
		                            nml_doc.gap_junctions.append(gap_junction)
		                            gap_counter+=1
		                            if projection_counter==0:
                                               net.electrical_projections.append(neuroml_projection_array[proj_index])
                                               projection_counter+=1
                                               projection=neuroml_projection_array[proj_index]
		                            projection.electrical_connections.append(conn)
		                            conn_count+=1

                

           
           if connectivity_information[0]=="uniform random":
               gap_junction0 = neuroml.GapJunction(id="gap_junction0", conductance=connectivity_information[1][1])
               neuroml_projection_array=[]
               initial_projection_counter=0
               for pre_pop_index in range(0,len(Golgi_pop_index_array)):
                   for post_pop_index in range(0,len(Golgi_pop_index_array)):
                       if pre_pop_index<=post_pop_index:
                          proj = neuroml.ElectricalProjection(id="proj%d"%initial_projection_counter,
		                presynaptic_population=Golgi_pop_index_array[pre_pop_index], 
		                postsynaptic_population=Golgi_pop_index_array[post_pop_index])
                          neuroml_projection_array.append(proj)
                          initial_projection_counter+=1
              
               gap_counter=0
               for proj_index in range(initial_projection_counter):
                   
	           projection_counter=0
	           conn_count = 0
	           for pre_pop_index in range(0,len(Golgi_pop_index_array)):
                       for post_pop_index in range(0,len(Golgi_pop_index_array)):
                           if pre_pop_index<=post_pop_index:
                              for Pre_cell in range(cell_array[pre_pop_index+1][1]):
                          # randomly Connect cells with defined probability for now; scripted so that to avoid inclusion of projection and gap_junction/synapse components if there are no connections; otherwise the mod files are not compiled.
                                  for Post_cell in range(cell_array[post_pop_index+1][1]):
                                      if Pre_cell<Post_cell:
                                         if random.random() < connectivity_information[1][0]:
                                            conn =neuroml.ElectricalConnection(id=conn_count,pre_cell="%d"%Pre_cell,post_cell="%d"%Post_cell,synapse=gap_junction0.id)
                                            if gap_counter==0:
		                               nml_doc.gap_junctions.append(gap_junction0)
		                               gap_counter+=1
		                            if projection_counter==0:
                                               net.electrical_projections.append(neuroml_projection_array[proj_index])
                                               projection_counter+=1
                                               projection=neuroml_projection_array[proj_index]
		                            projection.electrical_connections.append(conn)
		                            conn_count+=1

               
             
              


             
                      
	   

        nml_file = '%s.net.nml'%ref

       

        writers.NeuroMLWriter.write(nml_doc,nml_file)

        print("Written network file to: "+nml_file)
    
        ###### Validate the NeuroML2 ######   

        validate_neuroml2(nml_file)

        if simulation_parameters[2]=="jNeuroML" or simulation_parameters[2]=="jNeuroML_NEURON":
        
        # Create a LEMSSimulation to manage creation of LEMS file

           ls = LEMSSimulation(ref, simulation_parameters[0], simulation_parameters[1])

        # Point to network as target of simulation
    
           ls.assign_simulation_target(net.id)

           ls.include_neuroml2_file(nml_file)

        # Specify Displays and Output Files
        if simulation_parameters[2]=="jNeuroML":
	   if string.lower(population_type) =="list":
	      for x in range(cell_array[0]):
	         disp = "display_voltages%d"%x
	         ls.create_display(disp, "Voltages Golgi_pop%d"%x, "-75", "50")
	         of0 = 'Volts%d_file0'%x
	         ls.create_output_file(of0, "Golgi_pop%d_0_jNeuroML.dat"%x)
	         dat_file_counter=0
	         max_traces = 20
	         if cell_array[x+1][1]<=max_traces:
	            for i in range(cell_array[x+1][1]):
		        quantity = "%s/%i/%s/v"%(Golgi_pop_index_array[x], i,cell_array[x+1][0])
			ls.add_line_to_display(disp, "../%s/%i: Vm"%(Golgi_pop_index_array[x],i), quantity, "1mV", pynml.get_next_hex_color())
		        ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
					   
	         else:
		    randomly_select_displayed_cells=random.sample(range(cell_array[x+1][1]),max_traces)
		    for y in randomly_select_displayed_cells:
		       quantity = "%s/%i/%s/v"%(Golgi_pop_index_array[x], y,cell_array[x+1][0])
		       ls.add_line_to_display(disp, "../%s/%i: Vm"%(Golgi_pop_index_array[x],y), quantity, "1mV", pynml.get_next_hex_color())
					      
		    for i in range(cell_array[x+1][1]):
		        quantity = "%s/%i/%s/v"%(Golgi_pop_index_array[x], i,cell_array[x+1][0])
		        if i<=max_traces:
			   ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
		        else:
			   max_traces=max_traces+max_traces
			   del of0
			   dat_file_counter+=1
			   of0='Volts%d_file%d'%(x,dat_file_counter)
		           ls.create_output_file(of0, "Golgi_pop%d_%d_jNeuroML.dat"%(x,dat_file_counter))
		           ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
           else:
	      for x in range(cell_array[0]):
	         disp = "display_voltages%d"%x
	         ls.create_display(disp, "Voltages Golgi_pop%d"%x, "-75", "50")
		 of0 = 'Volts%d_file0'%x
		 ls.create_output_file(of0, "Golgi_pop%d_0_jNeuroML.dat"%x)
		 dat_file_counter=0
		 max_traces = 20
		 if cell_array[x+1][1]<=max_traces:
		    for i in range(cell_array[x+1][1]):
		       quantity = "%s[%i]/v"%(Golgi_pop_index_array[x], i)
		       ls.add_line_to_display(disp, "%s[%i]: Vm"%(Golgi_pop_index_array[x],i), quantity, "1mV", pynml.get_next_hex_color())
		       ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
	         else:
		    randomly_select_displayed_cells=random.sample(range(cell_array[x+1][1]),max_traces)
		    for y in randomly_select_displayed_cells:
		       quantity = "%s[%i]/v"%(Golgi_pop_index_array[x], y)
		       ls.add_line_to_display(disp, "%s[%i]: Vm"%(Golgi_pop_index_array[x],y), quantity, "1mV", pynml.get_next_hex_color())
					      
		    for i in range(cell_array[x+1][1]):
		       quantity = "%s[%i]/v"%(Golgi_pop_index_array[x], i)
		       if i<=max_traces:
		          ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
		       else:
			  max_traces=max_traces+max_traces
			  del of0
			  dat_file_counter+=1
			  of0='Volts%d_file%d'%(x,dat_file_counter)
			  ls.create_output_file(of0, "Golgi_pop%d_%d_jNeuroML.dat"%(x,dat_file_counter))
			  ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
	   lems_file_name = ls.save_to_file()
	   results1 = pynml.run_lems_with_jneuroml(lems_file_name, nogui=True, load_saved_data=True, plot=True)

        if simulation_parameters[2]=="jNeuroML_NEURON":
           if string.lower(population_type) =="list":
	      for x in range(cell_array[0]):
	         disp = "display_voltages%d"%x
		 ls.create_display(disp, "Voltages Golgi_pop%d"%x, "-75", "50")
		 of0 = 'Volts%d_file0'%x
		 ls.create_output_file(of0, "Golgi_pop%d_0_NEURON.dat"%x)
		 dat_file_counter=0
		 max_traces = 20
		 if cell_array[x+1][1]<=max_traces:
		    for i in range(cell_array[x+1][1]):
		       quantity = "%s/%i/%s/v"%(Golgi_pop_index_array[x], i,cell_array[x+1][0])
		       ls.add_line_to_display(disp, "../%s/%i: Vm"%(Golgi_pop_index_array[x],i), quantity, "1mV", pynml.get_next_hex_color())
		       ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
		 else:
		    randomly_select_displayed_cells=random.sample(range(cell_array[x+1][1]),max_traces)
		    for y in randomly_select_displayed_cells:
		       quantity = "%s/%i/%s/v"%(Golgi_pop_index_array[x], y,cell_array[x+1][0])
		       ls.add_line_to_display(disp, "../%s/%i: Vm"%(Golgi_pop_index_array[x],y), quantity, "1mV", pynml.get_next_hex_color())
	            for i in range(cell_array[x+1][1]):
	               quantity = "%s/%i/%s/v"%(Golgi_pop_index_array[x], i,cell_array[x+1][0])
		       if i<=max_traces:
		          ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
		       else:
		          max_traces=max_traces+max_traces
		          del of0
		          dat_file_counter+=1
		          of0='Volts%d_file%d'%(x,dat_file_counter)
		          ls.create_output_file(of0, "Golgi_pop%d_%d_NEURON.dat"%(x,dat_file_counter))
			  ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
	   else:
		     for x in range(cell_array[0]):
		        disp = "display_voltages%d"%x
		        ls.create_display(disp, "Voltages Golgi_pop%d"%x, "-75", "50")
		        of0 = 'Volts%d_file0'%x
		        ls.create_output_file(of0, "Golgi_pop%d_0_NEURON.dat"%x)
		        dat_file_counter=0
		        max_traces = 20
		        if cell_array[x+1][1]<=max_traces:
		           for i in range(cell_array[x+1][1]):
			      quantity = "%s[%i]/v"%(Golgi_pop_index_array[x], i)
			      ls.add_line_to_display(disp, "%s[%i]: Vm"%(Golgi_pop_index_array[x],i), quantity, "1mV", pynml.get_next_hex_color())
			      ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
			   
			else:
		             randomly_select_displayed_cells=random.sample(range(cell_array[x+1][1]),max_traces)
		             for y in randomly_select_displayed_cells:
		                 quantity = "%s[%i]/v"%(Golgi_pop_index_array[x], y)
			         ls.add_line_to_display(disp, "%s[%i]: Vm"%(Golgi_pop_index_array[x],y), quantity, "1mV", pynml.get_next_hex_color())
			      
		             for i in range(cell_array[x+1][1]):
			         quantity = "%s[%i]/v"%(Golgi_pop_index_array[x], i)
			         if i<=max_traces:
			            ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
			         else:
		                    max_traces=max_traces+max_traces
		                    del of0
		                    dat_file_counter+=1
		                    of0='Volts%d_file%d'%(x,dat_file_counter)
		                    ls.create_output_file(of0, "Golgi_pop%d_%d_NEURON.dat"%(x,dat_file_counter))
			            ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
                # Save to LEMS XML file
           lems_file_name = ls.save_to_file() 
                # Run with jNeuroML_NEURON
           results1 = pynml.run_lems_with_jneuroml_neuron(lems_file_name, nogui=True, load_saved_data=True, plot=True)
         

if __name__ == "__main__":
    
    # a line below is a Cell_array for testing generation of multiple populations; code generates two populations and four projections as expected
    Cell_array=[2,["Very_Simple_Golgi",4],["Very_Simple_Golgi",4]]
    
    #Cell_array=[1,["Very_Simple_Golgi",8]]
    Position_array=["random",350, 350, 350]
    Conn_array=["uniform random",[1,"2nS"]]
    Input_array=["testing",0.5,["50.0ms","200.0ms","4E-5uA"],["250.0ms","200.0ms","-0.5E-5uA"]]
    # 0.0002 ms, 0.0003 ms timesteps produce, on average, a 0.5 ms spike time difference between JNeuroML and NEURON simulations. Qualitatively, the traces are the same.
    Sim_array=[500,0.0003,"no simulation"]
    #Conn_array=["Vervaeke_2010_one_compartment",1]     # second parameter controls spatial scale
    generate_and_run_golgi_cell_net("Simple_Golgi_Net",Cell_array,Position_array,Conn_array,Input_array,Sim_array,"list")
   
        
    
	


import neuroml
from pyneuroml import pynml
from pyneuroml.lems.LEMSSimulation import LEMSSimulation
import math
import neuroml.writers as writers
from neuroml.utils import validate_neuroml2
import random
import numpy as np

def generate_and_run_golgi_cell_net(ref,cell_array,location_array, connectivity_information,input_information,simulation_parameters,population_type):
        
        
        random.seed(12345)
        nml_doc = neuroml.NeuroMLDocument(id=ref)
        #cell_array will have to include cell_types and no_of_cells
        #connectivity_information is a list of lists that will have to include connectivity parameters; now code only for a random configuration with parameters connection_probability and conductance_strength

     

        
        include_cell=neuroml.IncludeType(href="%s.cell.nml"%cell_type)
        nml_doc.includes.append(include_cell)

        localization_type=location_array[0]
        x_dim=location_array[1]
        y_dim=location_array[2]
        z_dim=location_array[3]
        
        if input_information[0]=="testing":
           fraction_of_cells_to_target=input_information[1]
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
        
        if population_type ==None:
	   for x in range(1,cell_array[0]+1):
	   Golgi_pop0 = neuroml.Population(id="Golgi_pop0", size = no_of_cells, type="populationList",
		                  component=cell_type)
	   net.populations.append(Golgi_pop0)



	   cell_positions=np.zeros([no_of_cells,3])

           if localization_type=="random":
	      for cell in range(no_of_cells):
	         Golgi_cell=neuroml.Instance(id="%d"%cell)
	         Golgi_pop0.instances.append(Golgi_cell)
	         X=random.random()
	         Y=random.random()
	         Z=random.random()
                 cell_positions[cell,0]=x_dim*X
                 cell_positions[cell,1]=y_dim*Y
                 cell_positions[cell,2]=z_dim*Z

              
	         Golgi_cell.location=neuroml.Location(x=x_dim*X, y=y_dim*Y, z=z_dim*Z)
	   

             #Define GapJunction and ElectricalProjection elements; however inclusion of these elements in the nml file is conditional (see below)


           gap_junction0 = neuroml.GapJunction(id="gap_junction0", conductance=conductance_strength)
       
      
        
           proj1 = neuroml.ElectricalProjection(id="Golgi_to_Golgi0",
		                presynaptic_population=Golgi_pop0.id, 
		                postsynaptic_population=Golgi_pop0.id)


         

	   projection_counter=0
	   conn_count = 0
	   for pre in range(no_of_cells):
        
    
            # randomly Connect cells with defined probability for now; scripted so that to avoid inclusion of projection and gap_junction/synapse components if there are no connections; otherwise the mod files are not compiled.
    
	       for post in range(no_of_cells):
		   if random.random() < connection_probability:
		      conn = \
		      neuroml.ElectricalConnection(id=conn_count, \
				   pre_cell="../%s/%d/%s"%(Golgi_pop0.id,pre,cell_type),
				   post_cell="../%s/%d/%s"%(Golgi_pop0.id,post,cell_type),synapse=gap_junction0.id)
                     
		      if projection_counter==0:
		         nml_doc.gap_junctions.append(gap_junction0)
		         net.electrical_projections.append(proj1)
		         projection_counter+=1
		      proj1.electrical_connections.append(conn)
		      conn_count+=1

	


        

           Input_list1=neuroml.InputList(id="Input_list1", component="Input_1")
           net.input_lists.append(Input_list1)
           Input_list2=neuroml.InputList(id="Input_list2", component="Input_2")
           net.input_lists.append(Input_list2)


           randomly_select_target_cells=random.sample(range(no_of_cells),testing_inputs[0]*no_of_cells)


           for i in randomly_select_target_cells:
              Inp = neuroml.Input(target="../%s/%d/%s"%(Golgi_pop0.id,i,cell_type),id="%d"%i,destination="synapses")
              Input_list1.input.append(Inp)

           for i in randomly_select_target_cells:
              Inp = neuroml.Input(target="../%s/%d/%s"%(Golgi_pop0.id,i,cell_type),id="%d"%i,destination="synapses")
              Input_list2.input.append(Inp)

        else:
         
           Golgi_pop0 = neuroml.Population(id="Golgi_pop0", size = no_of_cells,
		                  component=cell_type)
	   net.populations.append(Golgi_pop0)



	   cell_positions=np.empty([no_of_cells,3])
           if localization_type=="random":
	      for cell in range(no_of_cells):
	      
	         X=random.random()
	         Y=random.random()
	         Z=random.random()
	         cell_positions[cell,0]=x_dim*X
                 cell_positions[cell,1]=y_dim*Y
                 cell_positions[cell,2]=z_dim*Z
	   

             #Define GapJunction and ElectricalProjection elements; however inclusion of these elements in the nml file is conditional (see below)


           gap_junction0 = neuroml.GapJunction(id="gap_junction0", conductance=conductance_strength)
       
      
        
           proj1 = neuroml.ElectricalProjection(id="Golgi_to_Golgi0",
		                presynaptic_population=Golgi_pop0.id, 
		                postsynaptic_population=Golgi_pop0.id)


         

	   projection_counter=0
	   conn_count = 0
	   for pre in range(no_of_cells):
        
    
            # randomly Connect cells with defined probability for now; scripted so that to avoid inclusion of projection and gap_junction/synapse components if there are no connections; otherwise the mod files are not compiled.
    
	       for post in range(no_of_cells):
		   if random.random() < connection_probability:
		      conn = \
		      neuroml.ElectricalConnection(id=conn_count, \
				   pre_cell="%d"%pre,
				   post_cell="%d"%post,synapse=gap_junction0.id)
                     
		      if projection_counter==0:
		         nml_doc.gap_junctions.append(gap_junction0)
		         net.electrical_projections.append(proj1)
		         projection_counter+=1
		      proj1.electrical_connections.append(conn)
		      conn_count+=1

	
           #block for explicit inputs
           randomly_select_target_cells=random.sample(range(no_of_cells),testing_inputs[0]*no_of_cells)
           
        
           for i in randomly_select_target_cells:
              Inp = neuroml.ExplicitInput(target="%d"%i,input=Pulse_generator1.id,destination="synapses")
              net.explicit_inputs.append(Inp)

           for i in randomly_select_target_cells:
              Inp = neuroml.ExplicitInput(target="%d"%i,input=Pulse_generator2.id,destination="synapses")
              net.explicit_inputs.append(Inp)
 
           
           #block for explicit inputs
        nml_file = '%s.net.nml'%ref

        return nml_doc, nml_file, net.id, Golgi_pop0.id


def Set_and_run_simulation(nml_document,nml_file_name,ref,duration,time_step, network_id,population_id,pop_size,cell_component,simulator):

    

    cell_component_nml="%s.cell.nml"%cell_component

    writers.NeuroMLWriter.write(nml_document,nml_file_name)

    print("Written network file to: "+nml_file_name)
    
    ###### Validate the NeuroML2 ######   

    validate_neuroml2(nml_file_name)


    # Create a LEMSSimulation to manage creation of LEMS file

    ls = LEMSSimulation(ref, duration, time_step)

    # Point to network as target of simulation
    
    ls.assign_simulation_target(network_id)
#
    #ls.include_neuroml2_file(cell_component_nml)

    ls.include_neuroml2_file(nml_file_name)


    #cell_file ="Very_Simple_Golgi.cell.nml"
    #channel_Na="Golgi_Na.channel.nml"
    #channel_NaR="Golgi_NaR.channel.nml"
    #channel_NaP="Golgi_NaP.channel.nml"
    #channel_KA="Golgi_KA.channel.nml"
    #channel_KM="Golgi_KM.channel.nml"
    #channel_KV="Golgi_KV.channel.nml"
    #channel_BK="Golgi_BK.channel.nml"
    #channel_Ca_HVA="Golgi_Ca_HVA.channel.nml"
    #channel_Ca_LVA="Golgi_Ca_LVA.channel.nml"
    #channel_hcn1f="Golgi_hcn1f.channel.nml"
    #channel_hcn1s="Golgi_hcn1s.channel.nml"
    #channel_hcn2f="Golgi_hcn2f.channel.nml"
    #channel_hcn2s="Golgi_hcn2s.channel.nml"
    #channel_leak="LeakCond.channel.nml"
    #decaymodel_ca="Golgi_CALC.nml"
    #decaymodel_ca2="Golgi_CALC_ca2.nml"
    #twoCa_pools="cellTwoCaPools.xml"

    # Include existing NeuroML2 files
    #ls.include_neuroml2_file(channel_Na)
    #ls.include_neuroml2_file(channel_NaR)  
    #ls.include_neuroml2_file(channel_NaP)
    #ls.include_neuroml2_file(channel_KA)
    #ls.include_neuroml2_file(channel_KM)
    #ls.include_neuroml2_file(channel_KV)
    #ls.include_neuroml2_file(channel_BK)
    #ls.include_neuroml2_file(channel_Ca_HVA)
    #ls.include_neuroml2_file(channel_Ca_LVA)
    #ls.include_neuroml2_file(channel_hcn1f)
    #ls.include_neuroml2_file(channel_hcn1s)
    #ls.include_neuroml2_file(channel_hcn2f)
    #ls.include_neuroml2_file(channel_hcn2s)
    #ls.include_neuroml2_file(channel_leak)
    #ls.include_neuroml2_file(decaymodel_ca)
    #ls.include_neuroml2_file(decaymodel_ca2)
    #ls.include_lems_file(twoCa_pools)

    # Specify Displays and Output Files
    disp0 = "display_voltages0"
    ls.create_display(disp0, "Voltages Golgi_pop0", "-75", "50")


    of0 = 'Volts0_file'
    ls.create_output_file(of0, "Golgi_pop0.dat")

    max_traces = 20

    for i in range(pop_size):
	 quantity = "%s/%i/%s/v"%(population_id, i,cell_component)
	 if i<max_traces:
	    ls.add_line_to_display(disp0, "../%s/%i: Vm"%(population_id,i), quantity, "1mV", pynml.get_next_hex_color())
	    ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
	    

    # Save to LEMS XML file
    lems_file_name = ls.save_to_file()
    # Run with jNeuroML
    if simulator=="jNeuroML":
       results1 = pynml.run_lems_with_jneuroml(lems_file_name, nogui=True, load_saved_data=True, plot=True)
    # Run with jNeuroML_NEURON
    if simulator=="jNeuroML_NEURON":
       results1 = pynml.run_lems_with_jneuroml_neuron(lems_file_name, nogui=True, load_saved_data=True, plot=True)


if __name__ == "__main__":
    
    
    Cell_array=[1,["Very_Simple_Golgi",2]]
    Position_array=["random",350, 350, 350]
    Conn_array=["random",[1,"0.5nS"]]
    Input_array=["testing",1,["50.0ms","200.0ms","4E-5uA"],["250.0ms","200.0ms","-0.5E-5uA"]]
    Sim_array=[500,0.0005,"jNeuroML"]
    
    generate_and_run_golgi_cell_net("Simple_Golgi_Net",Cell_array,Position_array,Conn_array,Input_array,Sim_array,"not a list")
   
        
    
	

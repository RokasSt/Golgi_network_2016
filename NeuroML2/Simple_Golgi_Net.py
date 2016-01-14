
import neuroml
from pyneuroml import pynml
from pyneuroml.lems.LEMSSimulation import LEMSSimulation
import math
import neuroml.writers as writers
from neuroml.utils import validate_neuroml2
import random


def generate_golgi_cell_net(ref,cell_type,
                        x_dim, y_dim, z_dim, no_of_cells, connection_probability, conductance_strength,pulse_delay1,pulse_duration1,pulse_amplitude1,pulse_delay2,pulse_duration2,pulse_amplitude2
                        ):
        
        random.seed(12345)
        nml_doc = neuroml.NeuroMLDocument(id=ref)
        
        
        
        nml_doc.include=neuroml.Include("%s.cell.nml"%cell_type)
        

        gap_junction0 = neuroml.GapJunction(id="gap_junction0", conductance=conductance_strength)
        nml_doc.gap_junctions.append(gap_junction0)

	

	Pulse_generator1=neuroml.PulseGenerator(id="Input_1",delay=pulse_delay1, duration=pulse_duration1, amplitude=pulse_amplitude1)
	nml_doc.pulse_generators.append(Pulse_generator1)
    Pulse_generator2=neuroml.PulseGenerator(id="Input_2",delay=pulse_delay2, duration=pulse_duration2, amplitude=pulse_amplitude2)
	nml_doc.pulse_generators.append(Pulse_generator2)

	

	# Create network
	net = neuroml.Network(id=ref+"_network",type="networkWithTemperature",temperature="23 degC")
	nml_doc.networks.append(net)


	# Create populations
	
	Golgi_pop0 = neuroml.Population(id="Golgi_pop0", size = no_of_cells, type="populationList",
		                  component=cell_type)
	net.populations.append(Golgi_pop0)



	
	for cell in range(0,no_of_cells):
	   Golgi_cell=neuroml.Instance(id="%d"%cell)
	   Golgi_pop0.instances.append(Golgi_cell)
	   X=random.random()
	   Y=random.random()
	   Z=random.random()
	   Golgi_cell.location=neuroml.Location(x=x_dim*X,y=y_dim*Y, z=z_dim*Z)
	   

	# Create a projection between them
	#proj1 = neuroml.Projection(id="Golgi_to_Golgi0", synapse=syn0.id,
		                #presynaptic_population=Golgi_pop0.id, 
		                #postsynaptic_population=Golgi_pop0.id)
	#net.projections.append(proj1)
        proj1 = neuroml.ElectricalProjection(id="Golgi_to_Golgi0",
		                presynaptic_population=Golgi_pop0.id, 
		                postsynaptic_population=Golgi_pop0.id)
	net.electrical_projections.append(proj1)

         

	
	conn_count = 0
	for pre in range(0,no_of_cells):

    
            # randomly Connect cells with defined probability for now
    
	    for post in range(0,no_of_cells):
	      if random.random() < connection_probability:
		conn = \
		  neuroml.ElectricalConnection(id=conn_count, \
		           pre_cell_id="../%s/%d/Very_Simple_Golgi/%s"%(Golgi_pop0.id,pre,cell_type),
		           post_cell_id="../%s/%d/Very_Simple_Golgi/%s"%(Golgi_pop0.id,post,cell_type),synapse=gap_junction0.id)
		proj1.connections.append(conn)
		conn_count+=1

	    Input_list1=neuroml.InputList(id="Input_list1", component="Input_1")
        net.input_lists.append(Input_list1)
        Input_list2=neuroml.InputList(id="Input_list1", component="Input_2")
        net.input_lists.append(Input_list2)
        
        for i in range(0,no_of_cells):
            Inp = neuroml.Input(target="../%s/%d/%s"%(Golgi_pop0.id,i,cell_type),id="%d"%i,destination="synapses")
            Input_list1.inputs.append(Inp)

       for i in range(0,no_of_cells):
            Inp = neuroml.Input(target="../%s/%d/%s"%(Golgi_pop0.id,i,cell_type),id="%d"%i,destination="synapses")
            Input_list2.inputs.append(Inp)

       

        nml_file = '%s.net.nml'%ref

        return nml_doc, nml_file, net.id, Golgi_pop0.id


def Set_and_run_simulation(nml_document,nml_file_name,ref,duration,time_step, network_id,population_id,pop_size,cell_component):

    

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
    ls.include_neuroml2_file(cell_component_nml)

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
    results1 = pynml.run_lems_with_jneuroml(lems_file_name, nogui=True, load_saved_data=True, plot=True)
    # Run with jNeuroML_NEURON
    #results1 = pynml.run_lems_with_jneuroml_neuron(lems_file_name, nogui=True, load_saved_data=True, plot=True)




if __name__ == "__main__":
        
        
    nml_doc, nml_file, net_id,population_id =generate_golgi_cell_net("Simple_Golgi_Net","Very_Simple_Golgi", 350, 350, 350, 2, 0,"0.5nS","50.0ms","200.0ms","4E-5uA","200.0ms","200.0ms","-0.5E-5uA")
        
	Set_and_run_simulation(nml_doc,nml_file,"Simple_Golgi_Net",500,0.003, net_id,population_id,2,"Very_Simple_Golgi")
	

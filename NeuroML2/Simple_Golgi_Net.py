
import neuroml
from pyneuroml import pynml
from pyneuroml.lems.LEMSSimulation import LEMSSimulation


import neuroml.loaders as loaders

import random
random.seed(12345)

ref = "Simple_Golgi_Net"
nml_doc = neuroml.NeuroMLDocument(id=ref)



cell_file ="Simple_Golgi.cell.nml"
channel_Na="Golgi_Na.channel.nml"
channel_NaR="Golgi_NaR.channel.nml"
channel_NaP="Golgi_NaP.channel.nml"
channel_KA="Golgi_KA.channel.nml"
channel_KM="Golgi_KM.channel.nml"
channel_KV="Golgi_KV.channel.nml"
channel_BK="Golgi_BK.channel.nml"
channel_Ca_HVA="Golgi_Ca_HVA.channel.nml"
channel_Ca_LVA="Golgi_Ca_LVA.channel.nml"
channel_hcn1f="Golgi_hcn1f.channel.nml"
channel_hcn1s="Golgi_hcn1s.channel.nml"
channel_hcn2f="Golgi_hcn2f.channel.nml"
channel_hcn2s="Golgi_hcn2s.channel.nml"
channel_leak="LeakCond.channel.nml"
decaymodel_ca="Golgi_CALC.nml"
decaymodel_ca2="Golgi_CALC_ca2.nml"
twoCa_pools="cellTwoCaPools.xml"




doc = loaders.NeuroMLLoader.load(cell_file)



syn0 = neuroml.ExpTwoSynapse(id="syn0", gbase="1nS",
                             erev="0mV",
                             tau_rise="0.5ms",
                             tau_decay="10ms")
nml_doc.exp_two_synapses.append(syn0)

#<poissonFiringSynapse id="poissonFiringSyn" averageRate="50 Hz" synapse="synInput" spikeTarget="./synInput"/>
#pfs = neuroml.PoissonFiringSynapse(id="poissonFiringSyn", average_rate="150 Hz",synapse=syn0.id, spike_target="./%s"%syn0.id)
#nml_doc.poisson_firing_synapses.append(pfs)

Pulse_generator1=neuroml.PulseGenerator(id="Input_1",delay="200.0ms", duration="200.0ms", amplitude="-0.5E-5uA")
nml_doc.pulse_generators.append(Pulse_generator1)

Pulse_generator2=neuroml.PulseGenerator(id="Input_2",delay="800.0ms", duration="200.0ms", amplitude="4E-5uA")
nml_doc.pulse_generators.append(Pulse_generator2)


# Create network
net = neuroml.Network(id=ref+"_network")
nml_doc.networks.append(net)


# Create populations
size0 = 10
Golgi_pop0 = neuroml.Population(id="Golgi_pop0", size = size0, type="populationList",
                          component="Simple_Golgi")
net.populations.append(Golgi_pop0)

#..... will be separate populations below if needed
#size1 = 10
#pop1 = neuroml.Population(id="Pop1", size = size1, component=Simple_Golgi.id)
#net.populations.append(pop1)

grid_size=float(1000)
for cell in range(0,size0):
   Golgi_cell=neuroml.Instance(id="%d"%cell)
   Golgi_pop0.instances.append(Golgi_cell)
   X=random.random()
   Y=random.random()
   Z=random.random()
   Golgi_cell.location=neuroml.Location(x=grid_size*X,y=grid_size*Y, z=grid_size*Z)
   

# Create a projection between them
proj1 = neuroml.Projection(id="Golgi_to_Golgi0", synapse=syn0.id,
                        presynaptic_population=Golgi_pop0.id, 
                        postsynaptic_population=Golgi_pop0.id)
net.projections.append(proj1)

prob_connection = 0.5
conn_count = 0
for pre in range(0,size0):

    
    # randomly Connect cells with defined probability for now
    
    for post in range(0,size0):
      if random.random() <= prob_connection:
        conn = \
          neuroml.Connection(id=conn_count, \
                   pre_cell_id="../%s/%d/Simple_Golgi"%(Golgi_pop0.id,pre),
                   post_cell_id="../%s/%d/Simple_Golgi"%(Golgi_pop0.id,post))
        proj1.connections.append(conn)
        conn_count+=1

Input_list1= neuroml.InputList(id="Input_list1", component="Input_1")
net.input_lists.append(Input_list1)
Input_list2= neuroml.InputList(id="Input_list2", component="Input_2")
net.input_lists.append(Input_list2)

for i in range(size0):
     Input=neuroml.Input(target="../%s/%d/Simple_Golgi"%(Golgi_pop0.id,i), id="%d"%i, destination="synapses")
     Input_list1.input.append(Input)

for i in range(size0):
     Input=neuroml.Input(target="../%s/%d/Simple_Golgi"%(Golgi_pop0.id,i), id="%d"%i, destination="synapses")
     Input_list2.input.append(Input)






import neuroml.writers as writers

nml_file = '%s.net.nml'%ref
writers.NeuroMLWriter.write(nml_doc, nml_file)


print("Written network file to: "+nml_file)


###### Validate the NeuroML ######    

from neuroml.utils import validate_neuroml2

validate_neuroml2(nml_file)

# Create a LEMSSimulation to manage creation of LEMS file
duration = 1000  # ms
dt = 0.001  # ms
ls = LEMSSimulation(ref, duration, dt)


# Point to network as target of simulation
ls.assign_simulation_target(net.id)

cell_file ="Simple_Golgi.cell.nml"
channel_Na="Golgi_Na.channel.nml"
channel_NaR="Golgi_NaR.channel.nml"
channel_NaP="Golgi_NaP.channel.nml"
channel_KA="Golgi_KA.channel.nml"
channel_KM="Golgi_KM.channel.nml"
channel_KV="Golgi_KV.channel.nml"
channel_BK="Golgi_BK.channel.nml"
channel_Ca_HVA="Golgi_Ca_HVA.channel.nml"
channel_Ca_LVA="Golgi_Ca_LVA.channel.nml"
channel_hcn1f="Golgi_hcn1f.channel.nml"
channel_hcn1s="Golgi_hcn1s.channel.nml"
channel_hcn2f="Golgi_hcn2f.channel.nml"
channel_hcn2s="Golgi_hcn2s.channel.nml"
channel_leak="LeakCond.channel.nml"
decaymodel_ca="Golgi_CALC.nml"
decaymodel_ca2="Golgi_CALC_ca2.nml"
twoCa_pools="cellTwoCaPools.xml"



# Include existing NeuroML2 files
ls.include_neuroml2_file(nml_file)
ls.include_neuroml2_file(cell_file)
ls.include_neuroml2_file(channel_Na)
ls.include_neuroml2_file(channel_NaR)  
ls.include_neuroml2_file(channel_NaP)
ls.include_neuroml2_file(channel_KA)
ls.include_neuroml2_file(channel_KM)
ls.include_neuroml2_file(channel_KV)
ls.include_neuroml2_file(channel_BK)
ls.include_neuroml2_file(channel_Ca_HVA)
ls.include_neuroml2_file(channel_Ca_LVA)
ls.include_neuroml2_file(channel_hcn1f)
ls.include_neuroml2_file(channel_hcn1s)
ls.include_neuroml2_file(channel_hcn2f)
ls.include_neuroml2_file(channel_hcn2s)
ls.include_neuroml2_file(channel_leak)
ls.include_neuroml2_file(decaymodel_ca)
ls.include_neuroml2_file(decaymodel_ca2)
ls.include_lems_file(twoCa_pools)

# Specify Displays and Output Files
disp0 = "display_voltages0"
ls.create_display(disp0, "Voltages Golgi_pop0", "-75", "50")


of0 = 'Volts0_file'
ls.create_output_file(of0, "v_pop0.dat")

max_traces = 20

for i in range(size0):
    quantity = "%s/%i/Simple_Golgi/v"%(Golgi_pop0.id, i)
    if i<max_traces:
        ls.add_line_to_display(disp0, "../%s/%i: Vm"%(Golgi_pop0.id,i), quantity, "1mV", pynml.get_next_hex_color())
    ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
    


# Save to LEMS XML file
lems_file_name = ls.save_to_file()

# Run with jNeuroML
results1 = pynml.run_lems_with_jneuroml(lems_file_name, nogui=True, load_saved_data=True, plot=True)

# Run with jNeuroML_NEURON
#results1 = pynml.run_lems_with_jneuroml_neuron(lems_file_name, nogui=True, load_saved_data=True, plot=True)

import neuroml
from pyneuroml import pynml
from pyneuroml.lems.LEMSSimulation import LEMSSimulation
import neuroml.loaders as loaders

import random
random.seed(12345)

ref = "Simple_Golgi_Net"
nml_doc = neuroml.NeuroMLDocument(id=ref)



cell_file = 'Simple_Golgi.cell.nml'
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
Simple_Golgi = doc.cells[0]



nml_doc.cells.append(Golgi_cell)


syn0 = neuroml.ExpTwoSynapse(id="syn0", gbase="1nS",
                             erev="0mV",
                             tau_rise="0.5ms",
                             tau_decay="10ms")
nml_doc.exp_two_synapses.append(syn0)

#<poissonFiringSynapse id="poissonFiringSyn" averageRate="50 Hz" synapse="synInput" spikeTarget="./synInput"/>
pfs = neuroml.PoissonFiringSynapse(id="poissonFiringSyn",
                                   average_rate="150 Hz",
                                   synapse=syn0.id, 
                                   spike_target="./%s"%syn0.id)
nml_doc.poisson_firing_synapses.append(pfs)

# Create network
net = neuroml.Network(id=ref+"_network")
nml_doc.networks.append(net)


# Create populations
size0 = 10
pop0 = neuroml.Population(id="Pop0", size = size0,
                          component=Simple_Golgi.id)
net.populations.append(pop0)

size1 = 10
pop1 = neuroml.Population(id="Pop1", size = size1,
                          component=Simple_Golgi.id)
net.populations.append(pop1)


# Create a projection between them
proj1 = neuroml.Projection(id="Proj0", synapse=syn0.id,
                        presynaptic_population=pop0.id, 
                        postsynaptic_population=pop1.id)
net.projections.append(proj1)

prob_connection = 0.5
conn_count = 0
for pre in range(0,size0):

    
    # Connect cells with defined probability
    
    for post in range(0,size1):
      if random.random() <= prob_connection:
        conn = \
          neuroml.Connection(id=conn_count, \
                   pre_cell_id="../%s[%i]"%(pop0.id,pre),
                   post_cell_id="../%s[%i]"%(pop1.id,post))
        proj1.connections.append(conn)
        conn_count+=1


for i in range(size0):
    expInp = neuroml.ExplicitInput(target='%s[%i]'%(pop0.id,i),
                                   input=pfs.id,
                                   destination="synapses")
    net.explicit_inputs.append(expInp)


import neuroml.writers as writers

nml_file = '%s.net.nml'%ref
writers.NeuroMLWriter.write(nml_doc, nml_file)


print("Written network file to: "+nml_file)


###### Validate the NeuroML ######    

from neuroml.utils import validate_neuroml2

validate_neuroml2(nml_file)

# Create a LEMSSimulation to manage creation of LEMS file
duration = 1000  # ms
dt = 0.05  # ms
ls = LEMSSimulation(ref, duration, dt)


# Point to network as target of simulation
ls.assign_simulation_target(net.id)

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
ls.include_neuroml2_file(twoCa_pools)

# Specify Displays and Output Files
disp0 = "display_voltages0"
ls.create_display(disp0, "Voltages Pop0", "-68", "-47")
disp1 = "display_voltages1"
ls.create_display(disp1, "Voltages Pop1", "-68", "-47")

of0 = 'Volts0_file'
ls.create_output_file(of0, "v_pop0.dat")
of1 = 'Volts1_file'
ls.create_output_file(of1, "v_pop1.dat")

max_traces = 10

for i in range(size0):
    quantity = "%s[%i]/v"%(pop0.id, i)
    if i<max_traces:
        ls.add_line_to_display(disp0, "%s[%i]: Vm"%(pop0.id,i), quantity, "1mV", pynml.get_next_hex_color())
    ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
    
for i in range(size1):
    quantity = "%s[%i]/v"%(pop1.id, i)
    if i<max_traces:
        ls.add_line_to_display(disp1, "%s[%i]: Vm"%(pop1.id,i), quantity, "1mV", pynml.get_next_hex_color())
    ls.add_column_to_output_file(of1, 'v%i'%i, quantity)

# Save to LEMS XML file
lems_file_name = ls.save_to_file()

# Run with jNeuroML
results1 = pynml.run_lems_with_jneuroml(lems_file_name, nogui=True, load_saved_data=True, plot=True)

# Run with jNeuroML_NEURON
#results1 = pynml.run_lems_with_jneuroml_neuron(lems_file_name, nogui=True, load_saved_data=True, plot=True)

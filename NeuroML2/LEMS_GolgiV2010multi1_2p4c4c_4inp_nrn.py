'''
Neuron simulator export for:

Components:
    null (Type: include)
    gap_junction0 (Type: gapJunction:  conductance=6.269854762E-9 (SI conductance))
    gap_junction1 (Type: gapJunction:  conductance=5.155667859E-9 (SI conductance))
    gap_junction2 (Type: gapJunction:  conductance=2.0623374926E-8 (SI conductance))
    gap_junction3 (Type: gapJunction:  conductance=1.1709368986999999E-8 (SI conductance))
    Input_0 (Type: pulseGenerator:  delay=0.02 (SI time) duration=0.2 (SI time) amplitude=4.0000000000000004E-11 (SI current))
    Input_1 (Type: pulseGenerator:  delay=0.22 (SI time) duration=0.2 (SI time) amplitude=-5.0000000000000005E-12 (SI current))
    GolgiV2010multi1_2p4c4c_4inp_network (Type: networkWithTemperature:  temperature=296.15 (SI temperature))
    null (Type: include)
    null (Type: include)
    null (Type: include)
    Very_Simple_Golgi_test_morph (Type: cell)
    null (Type: notes)
    Golgi_Na (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    Golgi_KV (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    LeakCond (Type: ionChannelPassive:  conductance=1.0E-11 (SI conductance))
    GolgiV2010multi1_2p4c4c_4inp (Type: Simulation:  length=0.45 (SI time) step=5.0E-6 (SI time))


    This NEURON file has been generated by org.neuroml.export (see https://github.com/NeuroML/org.neuroml.export)
         org.neuroml.export  v1.4.3
         org.neuroml.model   v1.4.3
         jLEMS               v0.9.8.1

'''

import neuron

import time
h = neuron.h
h.load_file("stdlib.hoc")

h.load_file("stdgui.hoc")

h("objref p")
h("p = new PythonObject()")

# Adding simulation Component(id=GolgiV2010multi1_2p4c4c_4inp type=Simulation) of network/component: GolgiV2010multi1_2p4c4c_4inp_network (Type: networkWithTemperature:  temperature=296.15 (SI temperature))

# Temperature used for network: 296.15 K
h.celsius = 296.15 - 273.15

print("Population Golgi_pop0 contains 2 instance(s) of component: Very_Simple_Golgi_test_morph of type: cell")

h.load_file("Very_Simple_Golgi_test_morph.hoc")
a_Golgi_pop0 = []
h("n_Golgi_pop0 = 2")
h("objectvar a_Golgi_pop0[n_Golgi_pop0]")
for i in range(int(h.n_Golgi_pop0)):
    h("a_Golgi_pop0[%i] = new Very_Simple_Golgi_test_morph()"%i)
    h("access a_Golgi_pop0[%i].Soma"%i)


h("proc initialiseV_Golgi_pop0() { for i = 0, n_Golgi_pop0-1 { a_Golgi_pop0[i].set_initial_v() } }")
h("objref fih_Golgi_pop0")
h('{fih_Golgi_pop0 = new FInitializeHandler(0, "initialiseV_Golgi_pop0()")}')

h("proc initialiseIons_Golgi_pop0() { for i = 0, n_Golgi_pop0-1 { a_Golgi_pop0[i].set_initial_ion_properties() } }")
h("objref fih_ion_Golgi_pop0")
h('{fih_ion_Golgi_pop0 = new FInitializeHandler(1, "initialiseIons_Golgi_pop0()")}')

print("Population Golgi_pop1 contains 2 instance(s) of component: Very_Simple_Golgi_test_morph of type: cell")

h.load_file("Very_Simple_Golgi_test_morph.hoc")
a_Golgi_pop1 = []
h("n_Golgi_pop1 = 2")
h("objectvar a_Golgi_pop1[n_Golgi_pop1]")
for i in range(int(h.n_Golgi_pop1)):
    h("a_Golgi_pop1[%i] = new Very_Simple_Golgi_test_morph()"%i)
    h("access a_Golgi_pop1[%i].Soma"%i)


h("proc initialiseV_Golgi_pop1() { for i = 0, n_Golgi_pop1-1 { a_Golgi_pop1[i].set_initial_v() } }")
h("objref fih_Golgi_pop1")
h('{fih_Golgi_pop1 = new FInitializeHandler(0, "initialiseV_Golgi_pop1()")}')

h("proc initialiseIons_Golgi_pop1() { for i = 0, n_Golgi_pop1-1 { a_Golgi_pop1[i].set_initial_ion_properties() } }")
h("objref fih_ion_Golgi_pop1")
h('{fih_ion_Golgi_pop1 = new FInitializeHandler(1, "initialiseIons_Golgi_pop1()")}')

'''
Adding projection: proj1
From Golgi_pop0 to Golgi_pop1 3 connection(s)
'''
h("objectvar syn_proj1_gap_junction0_A[3]")

h("objectvar syn_proj1_gap_junction0_B[3]")

h("a_Golgi_pop0[0].Section_3 { syn_proj1_gap_junction0_A[0] = new gap_junction0(0.341560) }")
h("a_Golgi_pop1[0].Section_1 { syn_proj1_gap_junction0_B[0] = new gap_junction0(0.023521) }")
h("setpointer syn_proj1_gap_junction0_A[0].vpeer, a_Golgi_pop1[0].Section_1.v(0.023521)")
h("setpointer syn_proj1_gap_junction0_B[0].vpeer, a_Golgi_pop0[0].Section_3.v(0.341560)")
h("a_Golgi_pop0[0].Section_3 { syn_proj1_gap_junction0_A[1] = new gap_junction0(0.770834) }")
h("a_Golgi_pop1[1].Section_3 { syn_proj1_gap_junction0_B[1] = new gap_junction0(0.178874) }")
h("setpointer syn_proj1_gap_junction0_A[1].vpeer, a_Golgi_pop1[1].Section_3.v(0.178874)")
h("setpointer syn_proj1_gap_junction0_B[1].vpeer, a_Golgi_pop0[0].Section_3.v(0.770834)")
h("a_Golgi_pop0[1].Section_1 { syn_proj1_gap_junction0_A[2] = new gap_junction0(0.709386) }")
h("a_Golgi_pop1[1].dend_1 { syn_proj1_gap_junction0_B[2] = new gap_junction0(0.824834) }")
h("setpointer syn_proj1_gap_junction0_A[2].vpeer, a_Golgi_pop1[1].dend_1.v(0.824834)")
h("setpointer syn_proj1_gap_junction0_B[2].vpeer, a_Golgi_pop0[1].Section_1.v(0.709386)")
'''
Adding projection: proj2
From Golgi_pop1 to Golgi_pop1 1 connection(s)
'''
h("objectvar syn_proj2_gap_junction3_A[1]")

h("objectvar syn_proj2_gap_junction3_B[1]")

h("a_Golgi_pop1[0].dend_1 { syn_proj2_gap_junction3_A[0] = new gap_junction3(0.588609) }")
h("a_Golgi_pop1[1].Section_1 { syn_proj2_gap_junction3_B[0] = new gap_junction3(0.518239) }")
h("setpointer syn_proj2_gap_junction3_A[0].vpeer, a_Golgi_pop1[1].Section_1.v(0.518239)")
h("setpointer syn_proj2_gap_junction3_B[0].vpeer, a_Golgi_pop1[0].dend_1.v(0.588609)")
# Adding input: Component(id=null type=explicitInput)

h("objectvar explicitInput_Input_0_Golgi_pop0_1_a_Golgi_pop01_Soma")
h("a_Golgi_pop0[1].Soma { explicitInput_Input_0_Golgi_pop0_1_a_Golgi_pop01_Soma = new Input_0(0.5) } ")

# Adding input: Component(id=null type=explicitInput)

h("objectvar explicitInput_Input_1_Golgi_pop0_1_a_Golgi_pop01_Soma")
h("a_Golgi_pop0[1].Soma { explicitInput_Input_1_Golgi_pop0_1_a_Golgi_pop01_Soma = new Input_1(0.5) } ")

# Adding input: Component(id=null type=explicitInput)

h("objectvar explicitInput_Input_0_Golgi_pop1_0_a_Golgi_pop10_Soma")
h("a_Golgi_pop1[0].Soma { explicitInput_Input_0_Golgi_pop1_0_a_Golgi_pop10_Soma = new Input_0(0.5) } ")

# Adding input: Component(id=null type=explicitInput)

h("objectvar explicitInput_Input_1_Golgi_pop1_0_a_Golgi_pop10_Soma")
h("a_Golgi_pop1[0].Soma { explicitInput_Input_1_Golgi_pop1_0_a_Golgi_pop10_Soma = new Input_1(0.5) } ")

trec = h.Vector()
trec.record(h._ref_t)

h.tstop = 450

h.dt = 0.005

h.steps_per_ms = 200.0



# File to save: time
# Column: time
h(' objectvar v_time ')
h(' { v_time = new Vector() } ')
h(' v_time.record(&t) ')
h.v_time.resize((h.tstop * h.steps_per_ms) + 1)

# File to save: Volts1_file0_1
# Column: Golgi_pop1[1]/v
h(' objectvar v_v1_Volts1_file0_1 ')
h(' { v_v1_Volts1_file0_1 = new Vector() } ')
h(' v_v1_Volts1_file0_1.record(&a_Golgi_pop1[1].Soma.v(0.5)) ')
h.v_v1_Volts1_file0_1.resize((h.tstop * h.steps_per_ms) + 1)

# File to save: Volts1_file0_0
# Column: Golgi_pop1[0]/v
h(' objectvar v_v0_Volts1_file0_0 ')
h(' { v_v0_Volts1_file0_0 = new Vector() } ')
h(' v_v0_Volts1_file0_0.record(&a_Golgi_pop1[0].Soma.v(0.5)) ')
h.v_v0_Volts1_file0_0.resize((h.tstop * h.steps_per_ms) + 1)

# File to save: Volts0_file0_0
# Column: Golgi_pop0[0]/v
h(' objectvar v_v0_Volts0_file0_0 ')
h(' { v_v0_Volts0_file0_0 = new Vector() } ')
h(' v_v0_Volts0_file0_0.record(&a_Golgi_pop0[0].Soma.v(0.5)) ')
h.v_v0_Volts0_file0_0.resize((h.tstop * h.steps_per_ms) + 1)

# File to save: Volts0_file0_1
# Column: Golgi_pop0[1]/v
h(' objectvar v_v1_Volts0_file0_1 ')
h(' { v_v1_Volts0_file0_1 = new Vector() } ')
h(' v_v1_Volts0_file0_1.record(&a_Golgi_pop0[1].Soma.v(0.5)) ')
h.v_v1_Volts0_file0_1.resize((h.tstop * h.steps_per_ms) + 1)



sim_start = time.time()
print("Running a simulation of %sms (dt = %sms)" % (h.tstop, h.dt))

h.run()

sim_end = time.time()
sim_time = sim_end - sim_start
print("Finished simulation in %f seconds (%f mins), saving results..."%(sim_time, sim_time/60.0))


# File to save: time
py_v_time = [ t/1000 for t in h.v_time.to_python() ]  # Convert to Python list for speed...

f_time_f2 = open('time.dat', 'w')
for i in range(int(h.tstop * h.steps_per_ms) + 1):
    f_time_f2.write('%f'% py_v_time[i])  # Save in SI units...+ '\n')
f_time_f2.close()
print("Saved data to: time.dat")

# File to save: Volts1_file0_1
py_v_v1_Volts1_file0_1 = [ float(x  / 1000.0) for x in h.v_v1_Volts1_file0_1.to_python() ]  # Convert to Python list for speed, variable has dim: voltage

f_Volts1_file0_1_f2 = open('simulations/V2010multi1_2p4c4c_4inp/sim0/Golgi_pop1_cell1.dat', 'w')
for i in range(int(h.tstop * h.steps_per_ms) + 1):
    f_Volts1_file0_1_f2.write('%e\t'% py_v_time[i]  + '%e\t'%(py_v_v1_Volts1_file0_1[i]) + '\n')
f_Volts1_file0_1_f2.close()
print("Saved data to: simulations/V2010multi1_2p4c4c_4inp/sim0/Golgi_pop1_cell1.dat")

# File to save: Volts1_file0_0
py_v_v0_Volts1_file0_0 = [ float(x  / 1000.0) for x in h.v_v0_Volts1_file0_0.to_python() ]  # Convert to Python list for speed, variable has dim: voltage

f_Volts1_file0_0_f2 = open('simulations/V2010multi1_2p4c4c_4inp/sim0/Golgi_pop1_cell0.dat', 'w')
for i in range(int(h.tstop * h.steps_per_ms) + 1):
    f_Volts1_file0_0_f2.write('%e\t'% py_v_time[i]  + '%e\t'%(py_v_v0_Volts1_file0_0[i]) + '\n')
f_Volts1_file0_0_f2.close()
print("Saved data to: simulations/V2010multi1_2p4c4c_4inp/sim0/Golgi_pop1_cell0.dat")

# File to save: Volts0_file0_0
py_v_v0_Volts0_file0_0 = [ float(x  / 1000.0) for x in h.v_v0_Volts0_file0_0.to_python() ]  # Convert to Python list for speed, variable has dim: voltage

f_Volts0_file0_0_f2 = open('simulations/V2010multi1_2p4c4c_4inp/sim0/Golgi_pop0_cell0.dat', 'w')
for i in range(int(h.tstop * h.steps_per_ms) + 1):
    f_Volts0_file0_0_f2.write('%e\t'% py_v_time[i]  + '%e\t'%(py_v_v0_Volts0_file0_0[i]) + '\n')
f_Volts0_file0_0_f2.close()
print("Saved data to: simulations/V2010multi1_2p4c4c_4inp/sim0/Golgi_pop0_cell0.dat")

# File to save: Volts0_file0_1
py_v_v1_Volts0_file0_1 = [ float(x  / 1000.0) for x in h.v_v1_Volts0_file0_1.to_python() ]  # Convert to Python list for speed, variable has dim: voltage

f_Volts0_file0_1_f2 = open('simulations/V2010multi1_2p4c4c_4inp/sim0/Golgi_pop0_cell1.dat', 'w')
for i in range(int(h.tstop * h.steps_per_ms) + 1):
    f_Volts0_file0_1_f2.write('%e\t'% py_v_time[i]  + '%e\t'%(py_v_v1_Volts0_file0_1[i]) + '\n')
f_Volts0_file0_1_f2.close()
print("Saved data to: simulations/V2010multi1_2p4c4c_4inp/sim0/Golgi_pop0_cell1.dat")

save_end = time.time()
save_time = save_end - sim_end
print("Finished saving results in %f seconds"%(save_time))

print("Done")

quit()

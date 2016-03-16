'''
Neuron simulator export for:

Components:
    null (Type: include)
    null (Type: include)
    null (Type: include)
    Pulse_vrpop0_Golgi_pop0_0 (Type: pulseGenerator:  delay=0.0 (SI time) duration=1.0 (SI time) amplitude=-5.595589999999999E-12 (SI current))
    XFpop0_Golgi_pop0_cell0_syn0_0 (Type: spikeArray)
    XFpop0_Golgi_pop0_cell0_syn1_0 (Type: spikeArray)
    XFpop0_background_Golgi_pop0_cell0_syn0_0 (Type: spikeArray)
    XFpop0_background_Golgi_pop0_cell0_syn1_0 (Type: spikeArray)
    Golgi_V2010_test_savings_trial0_network (Type: networkWithTemperature:  temperature=296.15 (SI temperature))
    null (Type: include)
    null (Type: include)
    null (Type: include)
    null (Type: include)
    null (Type: include)
    null (Type: include)
    null (Type: include)
    null (Type: include)
    null (Type: include)
    null (Type: include)
    null (Type: include)
    null (Type: include)
    null (Type: include)
    null (Type: include)
    null (Type: include)
    null (Type: include)
    null (Type: include)
    Golgi_10comp_13channels_2CaPools (Type: cell2CaPools)
    null (Type: notes)
    Golgi_Ca_HVA (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    Golgi_Ca_LVA (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    Golgi_CALC (Type: decayingPoolConcentrationModel:  restingConc=5.0E-5 (SI concentration) decayConstant=7.69231E-4 (SI time) shellThickness=2.0378E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    null (Type: notes)
    Golgi_CALC_ca2 (Type: decayingPoolConcentrationModel_independentCa:  restingConc=5.0E-5 (SI concentration) decayConstant=7.69231E-4 (SI time) shellThickness=2.0378E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    null (Type: notes)
    Golgi_hcn1f (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    Golgi_hcn1s (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    Golgi_hcn2f (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    Golgi_hcn2s (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    Golgi_KA (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    Golgi_KC (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    Golgi_Kslow (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    Golgi_KAHP (Type: ionChannelKS:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    Golgi_KV (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    LeakCond (Type: ionChannelPassive:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    Golgi_NaP (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    Golgi_NaR (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    Golgi_NaT (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    MFSpikeSyn (Type: expThreeSynapse:  tauRise=1.0E-4 (SI time) tauDecay1=7.0E-4 (SI time) tauDecay2=0.0025 (SI time) peakTime1=2.270228507231199E-4 (SI time) waveformFactor1=1.61360214664657 (dimensionless) peakTime2=3.3529956509043755E-4 (SI time) waveformFactor2=1.1911769125863751 (dimensionless) gbase1=7.0E-10 (SI conductance) gbase2=2.0000000000000003E-10 (SI conductance) erev=0.0 (SI voltage))
    PFSpikeSyn (Type: expTwoSynapse:  tauRise=1.0E-4 (SI time) tauDecay=0.0010600000000000002 (SI time) peakTime=2.606776292901149E-4 (SI time) waveformFactor=1.4120085501889936 (dimensionless) gbase=6.700000000000001E-10 (SI conductance) erev=0.0 (SI voltage))
    Golgi_V2010_test_savings_trial0 (Type: Simulation:  length=1.0 (SI time) step=5.0E-7 (SI time))


    This NEURON file has been generated by org.neuroml.export (see https://github.com/NeuroML/org.neuroml.export)
         org.neuroml.export  v1.4.4
         org.neuroml.model   v1.4.4
         jLEMS               v0.9.8.4

'''

import neuron

import time
h = neuron.h
h.load_file("nrngui.hoc")

h("objref p")
h("p = new PythonObject()")

# Adding simulation Component(id=Golgi_V2010_test_savings_trial0 type=Simulation) of network/component: Golgi_V2010_test_savings_trial0_network (Type: networkWithTemperature:  temperature=296.15 (SI temperature))

# Temperature used for network: 296.15 K
h.celsius = 296.15 - 273.15

print("Population Golgi_pop0 contains 1 instance(s) of component: Golgi_10comp_13channels_2CaPools of type: cell2CaPools")

print("Setting the default initial concentrations for ca (used in Golgi_10comp_13channels_2CaPools) to 5.0E-5 mM (internal), 2.0 mM (external)")
h("cai0_ca_ion = 5.0E-5")
h("cao0_ca_ion = 2.0")

print("Setting the default initial concentrations for ca2 (used in Golgi_10comp_13channels_2CaPools) to 5.0E-5 mM (internal), 2.0 mM (external)")
h("ca2i0_ca2_ion = 5.0E-5")
h("ca2o0_ca2_ion = 2.0")

h.load_file("Golgi_10comp_13channels_2CaPools.hoc")
a_Golgi_pop0 = []
h("n_Golgi_pop0 = 1")
h("objectvar a_Golgi_pop0[n_Golgi_pop0]")
for i in range(int(h.n_Golgi_pop0)):
    h("a_Golgi_pop0[%i] = new Golgi_10comp_13channels_2CaPools()"%i)
    h("access a_Golgi_pop0[%i].Soma"%i)

h("a_Golgi_pop0[0].position(26.097358307679269, 7.374411669300995, 1.715263517116622)")

h("proc initialiseV_Golgi_pop0() { for i = 0, n_Golgi_pop0-1 { a_Golgi_pop0[i].set_initial_v() } }")
h("objref fih_Golgi_pop0")
h('{fih_Golgi_pop0 = new FInitializeHandler(0, "initialiseV_Golgi_pop0()")}')

h("proc initialiseIons_Golgi_pop0() { for i = 0, n_Golgi_pop0-1 { a_Golgi_pop0[i].set_initial_ion_properties() } }")
h("objref fih_ion_Golgi_pop0")
h('{fih_ion_Golgi_pop0 = new FInitializeHandler(1, "initialiseIons_Golgi_pop0()")}')

print("Population InputPop_XFpop0_Golgi_pop0_cell0_syn0_0 contains 1 instance(s) of component: XFpop0_Golgi_pop0_cell0_syn0_0 of type: spikeArray")

h(" {n_InputPop_XFpop0_Golgi_pop0_cell0_syn0_0 = 1} ")
'''
Population InputPop_XFpop0_Golgi_pop0_cell0_syn0_0 contains instances of Component(id=XFpop0_Golgi_pop0_cell0_syn0_0 type=spikeArray)
whose dynamics will be implemented as a mechanism (XFpop0_Golgi_pop0_cell0_syn0_0) in a mod file
'''
h(" create InputPop_XFpop0_Golgi_pop0_cell0_syn0_0[1]")
h(" objectvar m_XFpop0_Golgi_pop0_cell0_syn0_0_InputPop_XFpop0_Golgi_pop0_cell0_syn0_0[1] ")

for i in range(int(h.n_InputPop_XFpop0_Golgi_pop0_cell0_syn0_0)):
    h.InputPop_XFpop0_Golgi_pop0_cell0_syn0_0[i].L = 10.0
    h.InputPop_XFpop0_Golgi_pop0_cell0_syn0_0[i](0.5).diam = 10.0
    h.InputPop_XFpop0_Golgi_pop0_cell0_syn0_0[i](0.5).cm = 318.31927
    h.InputPop_XFpop0_Golgi_pop0_cell0_syn0_0[i].push()
    h(" InputPop_XFpop0_Golgi_pop0_cell0_syn0_0[%i]  { m_XFpop0_Golgi_pop0_cell0_syn0_0_InputPop_XFpop0_Golgi_pop0_cell0_syn0_0[%i] = new XFpop0_Golgi_pop0_cell0_syn0_0(0.5) } "%(i,i))

    h.pop_section()
print("Population InputPop_XFpop0_Golgi_pop0_cell0_syn1_0 contains 1 instance(s) of component: XFpop0_Golgi_pop0_cell0_syn1_0 of type: spikeArray")

h(" {n_InputPop_XFpop0_Golgi_pop0_cell0_syn1_0 = 1} ")
'''
Population InputPop_XFpop0_Golgi_pop0_cell0_syn1_0 contains instances of Component(id=XFpop0_Golgi_pop0_cell0_syn1_0 type=spikeArray)
whose dynamics will be implemented as a mechanism (XFpop0_Golgi_pop0_cell0_syn1_0) in a mod file
'''
h(" create InputPop_XFpop0_Golgi_pop0_cell0_syn1_0[1]")
h(" objectvar m_XFpop0_Golgi_pop0_cell0_syn1_0_InputPop_XFpop0_Golgi_pop0_cell0_syn1_0[1] ")

for i in range(int(h.n_InputPop_XFpop0_Golgi_pop0_cell0_syn1_0)):
    h.InputPop_XFpop0_Golgi_pop0_cell0_syn1_0[i].L = 10.0
    h.InputPop_XFpop0_Golgi_pop0_cell0_syn1_0[i](0.5).diam = 10.0
    h.InputPop_XFpop0_Golgi_pop0_cell0_syn1_0[i](0.5).cm = 318.31927
    h.InputPop_XFpop0_Golgi_pop0_cell0_syn1_0[i].push()
    h(" InputPop_XFpop0_Golgi_pop0_cell0_syn1_0[%i]  { m_XFpop0_Golgi_pop0_cell0_syn1_0_InputPop_XFpop0_Golgi_pop0_cell0_syn1_0[%i] = new XFpop0_Golgi_pop0_cell0_syn1_0(0.5) } "%(i,i))

    h.pop_section()
print("Population InputPop_XFpop0_background_Golgi_pop0_cell0_syn0_0 contains 1 instance(s) of component: XFpop0_background_Golgi_pop0_cell0_syn0_0 of type: spikeArray")

h(" {n_InputPop_XFpop0_background_Golgi_pop0_cell0_syn0_0 = 1} ")
'''
Population InputPop_XFpop0_background_Golgi_pop0_cell0_syn0_0 contains instances of Component(id=XFpop0_background_Golgi_pop0_cell0_syn0_0 type=spikeArray)
whose dynamics will be implemented as a mechanism (XFpop0_background_Golgi_pop0_cell0_syn0_0) in a mod file
'''
h(" create InputPop_XFpop0_background_Golgi_pop0_cell0_syn0_0[1]")
h(" objectvar m_XFpop0_background_Golgi_pop0_cell0_syn0_0_InputPop_XFpop0_background_Golgi_pop0_cell0_syn0_0[1] ")

for i in range(int(h.n_InputPop_XFpop0_background_Golgi_pop0_cell0_syn0_0)):
    h.InputPop_XFpop0_background_Golgi_pop0_cell0_syn0_0[i].L = 10.0
    h.InputPop_XFpop0_background_Golgi_pop0_cell0_syn0_0[i](0.5).diam = 10.0
    h.InputPop_XFpop0_background_Golgi_pop0_cell0_syn0_0[i](0.5).cm = 318.31927
    h.InputPop_XFpop0_background_Golgi_pop0_cell0_syn0_0[i].push()
    h(" InputPop_XFpop0_background_Golgi_pop0_cell0_syn0_0[%i]  { m_XFpop0_background_Golgi_pop0_cell0_syn0_0_InputPop_XFpop0_background_Golgi_pop0_cell0_syn0_0[%i] = new XFpop0_background_Golgi_pop0_cell0_syn0_0(0.5) } "%(i,i))

    h.pop_section()
print("Population InputPop_XFpop0_background_Golgi_pop0_cell0_syn1_0 contains 1 instance(s) of component: XFpop0_background_Golgi_pop0_cell0_syn1_0 of type: spikeArray")

h(" {n_InputPop_XFpop0_background_Golgi_pop0_cell0_syn1_0 = 1} ")
'''
Population InputPop_XFpop0_background_Golgi_pop0_cell0_syn1_0 contains instances of Component(id=XFpop0_background_Golgi_pop0_cell0_syn1_0 type=spikeArray)
whose dynamics will be implemented as a mechanism (XFpop0_background_Golgi_pop0_cell0_syn1_0) in a mod file
'''
h(" create InputPop_XFpop0_background_Golgi_pop0_cell0_syn1_0[1]")
h(" objectvar m_XFpop0_background_Golgi_pop0_cell0_syn1_0_InputPop_XFpop0_background_Golgi_pop0_cell0_syn1_0[1] ")

for i in range(int(h.n_InputPop_XFpop0_background_Golgi_pop0_cell0_syn1_0)):
    h.InputPop_XFpop0_background_Golgi_pop0_cell0_syn1_0[i].L = 10.0
    h.InputPop_XFpop0_background_Golgi_pop0_cell0_syn1_0[i](0.5).diam = 10.0
    h.InputPop_XFpop0_background_Golgi_pop0_cell0_syn1_0[i](0.5).cm = 318.31927
    h.InputPop_XFpop0_background_Golgi_pop0_cell0_syn1_0[i].push()
    h(" InputPop_XFpop0_background_Golgi_pop0_cell0_syn1_0[%i]  { m_XFpop0_background_Golgi_pop0_cell0_syn1_0_InputPop_XFpop0_background_Golgi_pop0_cell0_syn1_0[%i] = new XFpop0_background_Golgi_pop0_cell0_syn1_0(0.5) } "%(i,i))

    h.pop_section()
# Adding projection: InputProj_XFpop0_Golgi_pop0_cell0_syn0_0, from InputPop_XFpop0_Golgi_pop0_cell0_syn0_0 to Golgi_pop0 with synapse MFSpikeSyn, 1 connection(s)
h("objectvar syn_InputProj_XFpop0_Golgi_pop0_cell0_syn0_0_MFSpikeSyn[1]")

# Connection 0: 0, seg 0 (0.500000) -> 0, seg 9 (0.640256)
h("a_Golgi_pop0[0].Dend_bl_1_first syn_InputProj_XFpop0_Golgi_pop0_cell0_syn0_0_MFSpikeSyn[0] = new MFSpikeSyn(0.640256)")
h("objectvar nc_syn_InputProj_XFpop0_Golgi_pop0_cell0_syn0_0_MFSpikeSyn_0")
h("InputPop_XFpop0_Golgi_pop0_cell0_syn0_0[0] nc_syn_InputProj_XFpop0_Golgi_pop0_cell0_syn0_0_MFSpikeSyn_0 = new NetCon(m_XFpop0_Golgi_pop0_cell0_syn0_0_InputPop_XFpop0_Golgi_pop0_cell0_syn0_0[0], syn_InputProj_XFpop0_Golgi_pop0_cell0_syn0_0_MFSpikeSyn[0], 0.000000, 0.0, 1.0)")  

# Adding projection: InputProj_XFpop0_Golgi_pop0_cell0_syn1_0, from InputPop_XFpop0_Golgi_pop0_cell0_syn1_0 to Golgi_pop0 with synapse PFSpikeSyn, 1 connection(s)
h("objectvar syn_InputProj_XFpop0_Golgi_pop0_cell0_syn1_0_PFSpikeSyn[1]")

# Connection 0: 0, seg 0 (0.500000) -> 0, seg 4 (0.882272)
h("a_Golgi_pop0[0].Dend_ap_2_first syn_InputProj_XFpop0_Golgi_pop0_cell0_syn1_0_PFSpikeSyn[0] = new PFSpikeSyn(0.882272)")
h("objectvar nc_syn_InputProj_XFpop0_Golgi_pop0_cell0_syn1_0_PFSpikeSyn_0")
h("InputPop_XFpop0_Golgi_pop0_cell0_syn1_0[0] nc_syn_InputProj_XFpop0_Golgi_pop0_cell0_syn1_0_PFSpikeSyn_0 = new NetCon(m_XFpop0_Golgi_pop0_cell0_syn1_0_InputPop_XFpop0_Golgi_pop0_cell0_syn1_0[0], syn_InputProj_XFpop0_Golgi_pop0_cell0_syn1_0_PFSpikeSyn[0], 0.000000, 0.0, 1.0)")  

# Adding projection: InputProj_XFpop0_background_Golgi_pop0_cell0_syn0_0, from InputPop_XFpop0_background_Golgi_pop0_cell0_syn0_0 to Golgi_pop0 with synapse MFSpikeSyn, 1 connection(s)
h("objectvar syn_InputProj_XFpop0_background_Golgi_pop0_cell0_syn0_0_MFSpikeSyn[1]")

# Connection 0: 0, seg 0 (0.500000) -> 0, seg 9 (0.640256)
h("a_Golgi_pop0[0].Dend_bl_1_first syn_InputProj_XFpop0_background_Golgi_pop0_cell0_syn0_0_MFSpikeSyn[0] = new MFSpikeSyn(0.640256)")
h("objectvar nc_syn_InputProj_XFpop0_background_Golgi_pop0_cell0_syn0_0_MFSpikeSyn_0")
h("InputPop_XFpop0_background_Golgi_pop0_cell0_syn0_0[0] nc_syn_InputProj_XFpop0_background_Golgi_pop0_cell0_syn0_0_MFSpikeSyn_0 = new NetCon(m_XFpop0_background_Golgi_pop0_cell0_syn0_0_InputPop_XFpop0_background_Golgi_pop0_cell0_syn0_0[0], syn_InputProj_XFpop0_background_Golgi_pop0_cell0_syn0_0_MFSpikeSyn[0], 0.000000, 0.0, 1.0)")  

# Adding projection: InputProj_XFpop0_background_Golgi_pop0_cell0_syn1_0, from InputPop_XFpop0_background_Golgi_pop0_cell0_syn1_0 to Golgi_pop0 with synapse PFSpikeSyn, 1 connection(s)
h("objectvar syn_InputProj_XFpop0_background_Golgi_pop0_cell0_syn1_0_PFSpikeSyn[1]")

# Connection 0: 0, seg 0 (0.500000) -> 0, seg 4 (0.882272)
h("a_Golgi_pop0[0].Dend_ap_2_first syn_InputProj_XFpop0_background_Golgi_pop0_cell0_syn1_0_PFSpikeSyn[0] = new PFSpikeSyn(0.882272)")
h("objectvar nc_syn_InputProj_XFpop0_background_Golgi_pop0_cell0_syn1_0_PFSpikeSyn_0")
h("InputPop_XFpop0_background_Golgi_pop0_cell0_syn1_0[0] nc_syn_InputProj_XFpop0_background_Golgi_pop0_cell0_syn1_0_PFSpikeSyn_0 = new NetCon(m_XFpop0_background_Golgi_pop0_cell0_syn1_0_InputPop_XFpop0_background_Golgi_pop0_cell0_syn1_0[0], syn_InputProj_XFpop0_background_Golgi_pop0_cell0_syn1_0_PFSpikeSyn[0], 0.000000, 0.0, 1.0)")  

# Adding input: Component(id=0 type=input)

h("objectvar vrpop0_Golgi_pop0_0_0")
h("a_Golgi_pop0[0].Soma { vrpop0_Golgi_pop0_0_0 = new Pulse_vrpop0_Golgi_pop0_0(0.500000) } ")

trec = h.Vector()
trec.record(h._ref_t)

h.tstop = 1000

h.dt = 0.0005

h.steps_per_ms = 2000.0

# Display: display_display_voltagesGolgi_pop0
display_display_voltagesGolgi_pop0 = h.Graph(0)
display_display_voltagesGolgi_pop0.size(0,h.tstop,-80.0,50.0)
display_display_voltagesGolgi_pop0.view(0, -80.0, h.tstop, 130.0, 80, 330, 330, 250)
h.graphList[0].append(display_display_voltagesGolgi_pop0)
# Line, plotting: Golgi_pop0/0/Golgi_10comp_13channels_2CaPools/v
display_display_voltagesGolgi_pop0.addexpr("a_Golgi_pop0[0].Soma.v(0.5)", "a_Golgi_pop0[0].Soma.v(0.5)", 1, 1, 0.8, 0.9, 2)



# File to save: time
# Column: time
h(' objectvar v_time ')
h(' { v_time = new Vector() } ')
h(' v_time.record(&t) ')
h.v_time.resize((h.tstop * h.steps_per_ms) + 1)

# File to save: Volts0_file0_0
# Column: Golgi_pop0/0/Golgi_10comp_13channels_2CaPools/v
h(' objectvar v_v0_Volts0_file0_0 ')
h(' { v_v0_Volts0_file0_0 = new Vector() } ')
h(' v_v0_Volts0_file0_0.record(&a_Golgi_pop0[0].Soma.v(0.5)) ')
h.v_v0_Volts0_file0_0.resize((h.tstop * h.steps_per_ms) + 1)



h.nrncontrolmenu()
sim_start = time.time()
print("Running a simulation of %sms (dt = %sms)" % (h.tstop, h.dt))

h.run()

sim_end = time.time()
sim_time = sim_end - sim_start
print("Finished simulation in %f seconds (%f mins), saving results..."%(sim_time, sim_time/60.0))

display_display_voltagesGolgi_pop0.exec_menu("View = plot")

# File to save: time
py_v_time = [ t/1000 for t in h.v_time.to_python() ]  # Convert to Python list for speed...

f_time_f2 = open('time.dat', 'w')
for i in range(int(h.tstop * h.steps_per_ms) + 1):
    f_time_f2.write('%f'% py_v_time[i])  # Save in SI units...+ '\n')
f_time_f2.close()
print("Saved data to: time.dat")

# File to save: Volts0_file0_0
py_v_v0_Volts0_file0_0 = [ float(x  / 1000.0) for x in h.v_v0_Volts0_file0_0.to_python() ]  # Convert to Python list for speed, variable has dim: voltage

f_Volts0_file0_0_f2 = open('/home/rokas/Golgi_network_2016/PyExperiments/simulations/V2010_test_savings/sim0/Golgi_pop0_cell0.dat', 'w')
for i in range(int(h.tstop * h.steps_per_ms) + 1):
    f_Volts0_file0_0_f2.write('%e\t'% py_v_time[i]  + '%e\t'%(py_v_v0_Volts0_file0_0[i]) + '\n')
f_Volts0_file0_0_f2.close()
print("Saved data to: /home/rokas/Golgi_network_2016/PyExperiments/simulations/V2010_test_savings/sim0/Golgi_pop0_cell0.dat")

save_end = time.time()
save_time = save_end - sim_end
print("Finished saving results in %f seconds"%(save_time))

print("Done")


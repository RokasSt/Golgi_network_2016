
from  Generate_Golgi_Network import *
import os.path

def run_simulations(network_parameters,sim_duration,time_step,simulator,experiment_identifier,no_of_trials,seed_specifier,plot_specifier,save_soma_specifier):
    
    Cell_array=network_parameters[0]
    Position_array=network_parameters[1]
    Conn_array=network_parameters[2]
    Input_array=network_parameters[3]
    
    for simulation_trial in range(0,no_of_trials):
        Sim_array=[sim_duration,time_step,simulator,experiment_identifier,simulation_trial,["seed",seed_specifier[1]],["plot",plot_specifier[1]]]
        newpath = r'simulations/%s/sim%d'%(experiment_identifier,simulation_trial)
        if not os.path.exists(newpath):
               os.makedirs(newpath)
        if seed_specifier[1]==True:
           sim_params,pop_params=generate_golgi_cell_net("Simple_Golgi_Net",Cell_array,Position_array,Conn_array,Input_array,Sim_array,"not a list",["output",True])

           if save_soma_specifier[1]=="Yes":
              save_soma_positions(pop_params,r'simulations/%s'%(experiment_identifier))
              print("saved soma positions in the experiment directory %s"%r'simulations/%s'%(experiment_identifier))
           generate_LEMS_and_run(sim_params,pop_params)
        else:
           sim_params,pop_params=generate_golgi_cell_net("Simple_Golgi_Net%d"%simulation_trial,Cell_array,Position_array,Conn_array,Input_array,Sim_array,"not a list",["output",True])

           if save_soma_specifier[1]=="Yes":
              save_soma_positions(pop_params,r'simulations/%s/sim%d'%(experiment_identifier,simulation_trial))
              print("saved soma positions in the experiment directory %s"%r'simulations/%s/sim%d'%(experiment_identifier,simulation_trial))
           generate_LEMS_and_run(sim_params,pop_params)
           
if __name__ == "__main__":


    #Cell_array=[1,["Very_Simple_Golgi_test_morph",2]]
    #Conn_array=["Vervaeke_2010_multi_compartment",1,[["dendrite_group"],[1]],["testing",4]]
    
    net_params=[]
    net_params[0] =[2,["Very_Simple_Golgi_test_morph",4],["Very_Simple_Golgi_test_morph",4]]
    net_params[1]=["random",100, 100, 100]
    net_params[2]=["Vervaeke_2010_multi_compartment",1,[["dendrite_group"],[1]],[["dendrite_group"],[1]],["testing",4]]
    ne_params[3]=["testing",0.5,["20.0ms","200.0ms","4E-5uA"],["220.0ms","200.0ms","-0.5E-5uA"]]
    run_simulations(net_params,450,0.005,"jNeuroML_NEURON","V2010multi1_2p4c4c_4inp",1,["seed specifier",True],["plot specifier",True],["save somata positions","Yes"])



    
    #ordering of arguments inside lists matters! see examples below for the exact order of different arguments in input arrays

    # a line below is a Cell_array for testing generation of multiple populations; code generates two populations and four projections as expected
    #Cell_array=[2,["Very_Simple_Golgi_test_morph",4],["Very_Simple_Golgi_test_morph",4]]
   

    #test one multi-compartment cell with no connections
    #Cell_array=[1,["Very_Simple_Golgi_test_morph",2]]

    #Cell_array=[1,["Very_Simple_Golgi",3]]
    #Position_array=["random",100, 100, 100]
    #Conn_array=["uniform random",[1,"2nS"]]
    #Input_array=["testing",0.5,["20.0ms","200.0ms","4E-5uA"],["220.0ms","200.0ms","-0.5E-5uA"]]
    # 0.0002 ms, 0.0003 ms timesteps produce, on average, a 0.5 ms spike time difference between JNeuroML and NEURON simulations. Qualitatively, the traces are the same.
    
    #use larger timestep if simulated with NEURON
    #a line below is a template for sim_array:
    #Sim_array=[simulation time,simulation timestep, simulate or not simulate: if simulate then either "jNeuroML_NEURON" or "jNeuroML" string has to be specified; otherwise a different string such as "no simulation" has to be specified; experiment_specifier, ["seed","True"],["plot",True]]

    #Sim_array=[450,0.005,"jNeuroML_NEURON","NEURON_V2010multi1",0,["seed","True"],["plot",True]]

    #Sim_array=[450,0.005,"no simulation","NEURON_V2012multi1_2c_1input",0,["seed","True"],["plot",True]]
    
    #Conn_array=["Vervaeke_2010_one_compartment",1]     # second parameter controls spatial scale

    #Conn_array=["Vervaeke_2010_multi_compartment",1,[["dendrite_group"],[1]],[["dendrite_group"],[1]]]

    #Below: modify conn_array by introducing a scaling factor that scales a hard-coded pico-level conductance to nano-scale; this can be used to test the presence of the electrical connection because input to one of the cells elicits noticeable spiking response in the second cell. Pico-level conductance at a single gap-junction is not sufficient to elicit action potentials in the second cell. This optional parameter, if present, has to be appended at the end of conn_array.
    
    #Conn_array=["Vervaeke_2010_multi_compartment",1,[["dendrite_group"],[1]],["testing",4]]

    #template for connectivity array for models with simulated GJ density
    #Conn_array=["Vervaeke_2012_based",spatial scale,["homogeneous or heterogeneous conductance",a value of a discrete GJ conductance,"units e.g. pS or nS"],["level of applying probabilities: segment/segment groups and subsegment"],\
    #[list of segments with their respective probabilities for each cell or list of segments each with list of subsegment probabilities
    #testing case 1 with segment probabilities (note that appropriate names of segment groups are passed); either constant or variable conductance:
    
    #one cell group
    #Conn_array=["Vervaeke_2012_based",1,["constant conductance",2000,"pS"],"segment groups and segments",[["Section_1","dend_1"],[0.7,0.3]]]
    #two cell groups
    #Conn_array=["Vervaeke_2012_based",1,["constant conductance",426,"pS"],"segment groups and segments",[["Section_1","dend_1"],[0.7,0.3]],[["Section_1","dend_1"],[0.7,0.3]]]
    #testing case 2 with subsegment probabilities:
                                            
    #one cell group with subsegment probabilities of only one segment
    #Conn_array=["Vervaeke_2012_based",1,["variable conductance","Gaussian",426,10,"pS"],"segments and subsegments",[["Section_1"],[1],[[[0.25,0.2],[0.25,0.4],[0.25,0.4],[0.25,0]]]]]
                                                                  
    #generate_and_run_golgi_cell_net("Simple_Golgi_Net",Cell_array,Position_array,Conn_array,Input_array,Sim_array,"not a list")

    #use different references to generate different network examples
    #generate_and_run_golgi_cell_net("V2010_2cells_1input",Cell_array,Position_array,Conn_array,Input_array,Sim_array,"not a list")
    
    #generate_and_run_golgi_cell_net("V2012_2cells_1input",Cell_array,Position_array,Conn_array,Input_array,Sim_array,"not a list")

   
 


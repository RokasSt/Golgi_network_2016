
from  Generate_Golgi_Network_v2 import *
import os.path

def run_simulations(network_parameters,simulation_parameters):  
    
    if simulation_parameters['globalSeed']:
       for simulation_trial in range(0,simulation_parameters['numTrials']):
           for exp_i in range(0,len(network_parameters)):
               Cell_array=network_parameters['experiment%d'%(exp_id)]['popParams']
               Position_array=network_parameters['experiment%d'%(exp_id)]['distributionParams']
               Conn_array=network_parameters['experiment%d'%(exp_id)]['connParams']
               Input_array=network_parameters['experiment%d'%(exp_id)]['inputParams']
               Sim_array=simulation_parameters
               Sim_array['experimentID']=network_parameters['experiment%d'%(exp_id)]['experimentID']
               newpath = r'simulations/%s/sim%d'%(network_parameters['experiment%d'%(exp_id)]['experimentID'],simulation_trial)
               if not os.path.exists(newpath):
                  os.makedirs(newpath)
               sim_params,pop_params=generate_golgi_cell_net("Golgi_%s"%(network_parameters['experiment%d'%(exp_id)]['experimentID']),\
                                                    Cell_array,Position_array,Conn_array,Input_array,Sim_array)
               if simulation_parameters['plotSpecifier']:
                  save_soma_positions(pop_params,r'simulations/%s'%(network_parameters['experiment%d'%(exp_id)]['experimentID']))
                  print("saved soma positions in the experiment directory %s"%r'simulations/%s'%(network_parameters['experiment%d'%(exp_id)]['experimentID']))
               generate_LEMS_and_run(sim_params,pop_params)
    else:
       if simulation_parameters['trialSeed']:
          for simulation_trial in range(0,simulation_parameters['numTrials']):
              seed_number=random.sample(range(0,15000),1)[0]
              for exp_i in range(0,len(network_parameters)):
                  Cell_array=network_parameters['experiment%d'%(exp_id)]['popParams']
                  Position_array=network_parameters['experiment%d'%(exp_id)]['distributionParams']
                  Conn_array=network_parameters['experiment%d'%(exp_id)]['connParams']
                  Input_array=network_parameters['experiment%d'%(exp_id)]['inputParams']
                  Sim_array=simulation_parameters
                  Sim_array['experimentID']=network_parameters['experiment%d'%(exp_id)]['experimentID']
                  Sim_array['trialSeedNumber']=seed_number
                  newpath = r'simulations/%s/sim%d'%(network_parameters['experiment%d'%(exp_id)]['experimentID'],simulation_trial)
                  if not os.path.exists(newpath):
                     os.makedirs(newpath)
                  sim_params,pop_params=generate_golgi_cell_net("Golgi_%s_trial%d"%(network_parameters['experiment%d'%(exp_id)]['experimentID'],simulation_trial),\
                                            Cell_array,Position_array,Conn_array,Input_array,Sim_array)
                  if save_soma_specifier[1]=="Yes":
                     save_soma_positions(pop_params,r'simulations/%s/sim%d'%(network_parameters['experiment%d'%(exp_id)]['experimentID'],simulation_trial))
                     print("saved soma positions in the experiment directory %s"%r'simulations/%s/sim%d'%(network_parameters['experiment%d'%(exp_id)]['experimentID'],simulation_trial))
                  generate_LEMS_and_run(sim_params,pop_params)
           
if __name__ == "__main__":














    ######### The block below was used for testing 2010based-generation of Golgi cell networks


    
    #net_params_multiple=[]
    #net_params=[]
    #net_params.append([2,["Very_Simple_Golgi_test_morph",10],["Very_Simple_Golgi_test_morph",10]])
    #net_params.append(["random",100, 100, 100])
    #net_params.append(["Vervaeke_2010_multi_compartment",1,[["dendrite_group"],[1]],[["dendrite_group"],[1]],["testing",4],["maximal connection length",200]])
    #net_params.append(["testing",0.5,["20.0ms","200.0ms","4E-5uA"],["220.0ms","200.0ms","-0.5E-5uA"]])
   
    #net_params2=[]
    #net_params2.append([2,["Very_Simple_Golgi_test_morph",10],["Very_Simple_Golgi_test_morph",10]])
    #net_params2.append(["random",100, 100, 100])
    #net_params2.append(["Vervaeke_2010_multi_compartment",20,[["dendrite_group"],[1]],[["dendrite_group"],[1]],["testing",4],["maximal connection length",200]])
    #net_params2.append(["testing",0.5,["20.0ms","200.0ms","4E-5uA"],["220.0ms","200.0ms","-0.5E-5uA"]])

    #net_params_multiple.append(net_params)
    #net_params_multiple.append(net_params2)
    # check firstly randomization : no simulation
    
    #run_simulations(net_params_multiple,450,0.005,"jNeuroML_NEURON",["test_iteration_1","test_iteration_2"],5,["seed specifier",False,"trial seed",True],["plot specifier",False],["save somata positions","Yes"],"list")




    ##############







  










    #run_simulations(net_params_multiple,450,0.005,"jNeuroML_NEURON",["test_Lists_and_sync","test_Lists2_and_sync"],5,["seed specifier",False],["plot specifier",False],["save somata positions","Yes"],"list")
    


    #net_params[3]=["variable basal firing rate",["amplitude distribution","gaussian","100","50","nA"],["offset distribution","uniform",50,100]]

    
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








    ######### the block below is used to test 2012based- generation of Golgi networks






    net_params_test_2012_multiple=[]
    net_params_2012_net1=[]
    net_params_2012_net2=[]
    net_params_2012_net1.append([2,["Very_Simple_Golgi_test_morph",15],["Very_Simple_Golgi_test_morph",15]])
    net_params_2012_net1.append(["random no overlap",100, 100, 100])
    net_params_2012_net1.append( ["Vervaeke_2012_based",1,[["Very_Simple_Golgi_test_morph","Very_Simple_Golgi_test_morph","constant conductance",426,"pS"]],["segment groups and segments","segment groups and segments"],[  [["Section_1","dend_1"],[0.7,0.3]],  [["Section_1","dend_1"],[0.7,0.3]]    ],[["Very_Simple_Golgi_test_morph","Very_Simple_Golgi_test_morph","constant number of GJ contacts per pair", 8]],["testing",4],["maximal connection length",150]                    ]                          )
    net_params_2012_net1.append([  ["variable basal firing rate",["amplitude distribution","gaussian",[100,100],[20,20],"nA"],["offset distribution","constant",[50,50],"ms"]]            ] )
    net_params_test_2012_multiple.append(net_params_2012_net1)
  
    net_params_2012_net2.append([2,["Very_Simple_Golgi_test_morph",15],["Very_Simple_Golgi_test_morph",15]])
    net_params_2012_net2.append(["random no overlap",100, 100, 100])
    net_params_2012_net2.append( ["Vervaeke_2012_based",1,[["Very_Simple_Golgi_test_morph","Very_Simple_Golgi_test_morph","constant conductance",426,"pS"]],["segment groups and segments","segment groups and segments"],[  [["Section_1","dend_1"],[0.7,0.3]],  [["Section_1","dend_1"],[0.7,0.3]]    ],[["Very_Simple_Golgi_test_morph","Very_Simple_Golgi_test_morph","constant number of GJ contacts per pair", 8]],["testing",4],["maximal connection length",150]                    ]                          )
    net_params_2012_net2.append([  ["variable basal firing rate",["amplitude distribution","constant",[100,100],"nA"],["offset distribution","constant",[50,50],"ms"]]            ] )
    net_params_test_2012_multiple.append(net_params_2012_net2)
    

    run_simulations(net_params_test_2012_multiple,450,0.005,"no simulation",["2012based_test_1","2012based_test_2"],2,["seed specifier",False,"trial seed",True],["plot specifier",False],["save somata positions","Yes"],"list")


    net_params_test_2012_multiple={}
    net_params_test_2012_multiple['experiment1']={}
    net_params_test_2012_multiple['experiment2']={}
    
    net_params_test_2012_multiple['experiment1']['experimentID']="2012based_test_1"
    net_params_test_2012_multiple['experiment2']['experimentID']="2012based_test_2"
    #exp1
    net_params_test_2012_multiple['experiment1']['popParams']=[]
    net_params_test_2012_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop0','cellType':"Very_Simple_Golgi_test_morph",'size':15})
    net_params_test_2012_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop1','cellType':"Very_Simple_Golgi_test_morph",'size':15})
    net_params_test_2012_multiple['experiment1']['distributionParams']={}
    net_params_test_2012_multiple['experiment1']['distributionParams']['distributionModel']="random no overlap"
    net_params_test_2012_multiple['experiment1']['distributionParams']['xDim']=100
    net_params_test_2012_multiple['experiment1']['distributionParams']['yDim']=100
    net_params_test_2012_multiple['experiment1']['distributionParams']['yDim']=100
    net_params_test_2012_multiple['experiment1']['connParams']={}
    net_params_test_2012_multiple['experiment1']['connParams']['connModel']="Vervaeke_2012_based"
    net_params_test_2012_multiple['experiment1']['connParams']['populationPairs']=[]
    net_params_test_2012_multiple['experiment1']['connParams']['populationPairs'].append({'prePopID':'Golgi_pop0',\
                                                    'postPopID':'Golgi_pop1','conductanceModel':"constant",\
                                                    'conductanceValue':426,'units':"pS",\
                                                     'gapJunctionModel':"constant number of GJ contacts per pair",'numberGJ':8,\
                                                     'spatialScale':1,'testingConductanceScale':4,'maximalConnDistance':150,\
                            'targetingModelprePop':{'model':"segment groups and segments",'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]},\
                            'targetingModelpostPop':{'model':"segment groups and segments",\
                                                'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]}})
    
    
    net_params_test_2012_multiple['experiment1']['inputParams']=[]
    inputGroups_pop0_exp1=[]
    inputGroups_pop0_exp1.append({'inputModel':"variable basal firing rate",'amplitudeDistribution':"gaussian",'average':100,'variance':20,'ampUnits':"nA",\
                             'offsetDistribution':"constant",'offset':50,'offsetUnits':"ms"})
    synapseList_pop0_exp1=[]
    synapseList_pop0_exp1.append({'synapseType':"MFSpikeSyn",'synapseMode':"persistent",'averageRate':50,\
                             'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                             'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]})
                            
    synapseList_pop0_exp1.append({'synapseType':"MFSpikeSyn",'synapseMode':"persistent",'averageRate':100,\
                             'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                             'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]})


    inputGroups_pop0_exp1.append({'inputModel':'MF','targetingRegime':"uniform",'fractionToTarget':0.5,'synapseList':synapseList_pop0_exp1})

    inputGroups_pop1_exp1=[]
    inputGroups_pop1_exp1.append({'inputModel':"variable basal firing rate",'amplitudeDistribution':"gaussian",'average':100,'variance':20,'ampUnits':"nA",\
                             'offsetDistribution':"constant",'offset':50,'offsetUnits':"ms"})
    synapseList_pop1_exp1=[]
    synapseList_pop1_exp1.append({'synapseType':"MFSpikeSyn",'synapseMode':"transient",'averageRate':50,'delay':80,'duration':100,'units':'ms',  \
                             'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segments and subsegments",\
                             'segmentList':["Soma","dend_3"],'segmentProbabilities':[0.7,0.3],'fractionAlongANDsubsegProbabilities':[[[0.5,1],[0.5,0]],[[0.5,0.7],[0.5,0.3]]]})
                            
    synapseList_pop1_exp1.append({'synapseType':"MFSpikeSyn",'synapseMode':"persistent",'averageRate':100,\
                             'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segments and subsegments",\
                             'segmentList':["Soma","dend_3"],'segmentProbabilities':[0.7,0.3],'fractionAlongANDsubsegProbabilities':[[[0.5,1],[0.5,1]],[[0.5,0.7],[0.5,0.3]]] })


    inputGroups_pop1.append({'inputModel':'MF','targetingRegime':"uniform",'fractionToTarget':0.5,'synapseList':synapseList_pop1_exp1})
    
                             
    net_params_test_2012_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp1})
    net_params_test_2012_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop1','inputGroups':inputGroups_pop1_exp1})

    ### exp 2
    net_params_test_2012_multiple['experiment2']['popParams']=[]
    net_params_test_2012_multiple['experiment2']['popParams'].append({'popID':'Golgi_pop0','cellType':"Very_Simple_Golgi_test_morph",'size':15})
    net_params_test_2012_multiple['experiment2']['popParams'].append({'popID':'Golgi_pop1','cellType':"Very_Simple_Golgi_test_morph",'size':15})
    
    net_params_test_2012_multiple['experiment2']['distributionParams']={}
    net_params_test_2012_multiple['experiment2']['distributionParams']['distributionModel']="random no overlap"
    net_params_test_2012_multiple['experiment2']['distributionParams']['xDim']=100
    net_params_test_2012_multiple['experiment2']['distributionParams']['yDim']=100
    net_params_test_2012_multiple['experiment2']['distributionParams']['yDim']=100
    
    net_params_test_2012_multiple['experiment2']['connParams']={}
    net_params_test_2012_multiple['experiment2']['connParams']['connModel']="Vervaeke_2012_based"
    net_params_test_2012_multiple['experiment2']['connParams']['populationPairs']=[]
    net_params_test_2012_multiple['experiment2']['connParams']['populationPairs'].append({'prePopID':'Golgi_pop0',\
                                                    'postPopID':'Golgi_pop1','conductanceModel':"constant",\
                                                    'conductanceValue':426,'units':"pS",\
                                                     'gapJunctionModel':"constant number of GJ contacts per pair",'numberGJ':8,\
                                                     'spatialScale':1,'testingConductanceScale':4,'maximalConnDistance':150,\
                            'targetingModelprePop':{'model':"segment groups and segments",'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]},\
                            'targetingModelpostPop':{'model':"segment groups and segments",\
                                                'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]}})
    
    
    net_params_test_2012_multiple['experiment2']['inputParams']=[]
    inputGroups_pop0_exp2=[]
    inputGroups_pop0_exp2.append({'inputModel':"variable basal firing rate",'amplitudeDistribution':"constant",'value':100,'ampUnits':"nA",\
                             'offsetDistribution':"constant",'offset':50,'offsetUnits':"ms"})
    synapseList_pop0_exp2=[]
    synapseList_pop0_exp2.append({'synapseType':"MFSpikeSyn",'synapseMode':"persistent",'averageRate':50,\
                             'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                             'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]})
                            
    synapseList_pop0_exp2.append({'synapseType':"MFSpikeSyn",'synapseMode':"persistent",'averageRate':100,\
                             'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                             'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]})


    inputGroups_pop0_exp2.append({'inputModel':'MF','targetingRegime':"uniform",'fractionToTarget':0.5,'synapseList':synapseList_pop0_exp2})

    inputGroups_pop1_exp2=[]
    inputGroups_pop1_exp2.append({'inputModel':"variable basal firing rate",'amplitudeDistribution':"gaussian",'average':100,'variance':20,'ampUnits':"nA",\
                             'offsetDistribution':"constant",'offset':50,'offsetUnits':"ms"})
    synapseList_pop1_exp2=[]
    synapseList_pop1_exp2.append({'synapseType':"MFSpikeSyn",'synapseMode':"transient",'averageRate':50,'delay':80,'duration':100,'units':'ms',  \
                             'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segments and subsegments",\
                             'segmentList':["Soma","dend_3"],'segmentProbabilities':[0.7,0.3],'fractionAlongANDsubsegProbabilities':[[[0.5,1],[0.5,0]],[[0.5,0.7],[0.5,0.3]]]})
                            
    synapseList_pop1_exp2.append({'synapseType':"MFSpikeSyn",'synapseMode':"persistent",'averageRate':100,\
                             'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segments and subsegments",\
                             'segmentList':["Soma","dend_3"],'segmentProbabilities':[0.7,0.3],'fractionAlongANDsubsegProbabilities':[[[0.5,1],[0.5,1]],[[0.5,0.7],[0.5,0.3]]] })


    inputGroups_pop1_exp2.append({'inputModel':'MF','targetingRegime':"uniform",'fractionToTarget':0.5,'synapseList':synapseList_pop1_exp2})
    
                             
    net_params_test_2012_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp2})
    net_params_test_2012_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop1','inputGroups':inputGroups_pop1_exp2})

    
    sim_params={'simulator':"no simulation",'duration':450,'timeStep':0.005,'numTrials':2,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,'saveSomataPositions':True}
    
    ##### run all simulations
    run_simulations(net_params_test_2012_multiple,sim_params)

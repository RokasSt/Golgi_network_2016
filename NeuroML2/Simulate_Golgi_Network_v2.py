
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


   #########    Based on 2010 rules



    net_params_test_2010_multiple={}
    net_params_test_2010_multiple['experiment1']={}
    net_params_test_2010_multiple['experiment2']={}
    
    net_params_test_2010_multiple['experiment1']['experimentID']="test_iteration_1"
    net_params_test_2010_multiple['experiment2']['experimentID']="test_iteration_2"
    #exp1
    net_params_test_2010_multiple['experiment1']['popParams']=[]
    net_params_test_2010_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop0','cellType':"Very_Simple_Golgi_test_morph",'size':10})
    net_params_test_2010_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop1','cellType':"Very_Simple_Golgi_test_morph",'size':10})

    net_params_test_2010_multiple['experiment1']['distributionParams']={}
    net_params_test_2010_multiple['experiment1']['distributionParams']['distributionModel']="random"
    net_params_test_2010_multiple['experiment1']['distributionParams']['xDim']=100
    net_params_test_2010_multiple['experiment1']['distributionParams']['yDim']=100
    net_params_test_2010_multiple['experiment1']['distributionParams']['yDim']=100

    ##### as conductance levels are soma-to-soma distance-dependent in a Vervaeke_2010_based model, subcellular targeting is not implemented in this configuration. If   one wants to specify multiple GJs per cell pair with constant or heterogeneous conductances one can use Vervaeke_2012_based connModel
    net_params_test_2010_multiple['experiment1']['connParams']={}
    net_params_test_2010_multiple['experiment1']['connParams']['connModel']="Vervaeke_2010_based"
    net_params_test_2010_multiple['experiment1']['connParams']['populationPairs']=[]
    net_params_test_2010_multiple['experiment1']['connParams']['populationPairs'].append({'prePopID':'Golgi_pop0',\
                                                    'postPopID':'Golgi_pop1','spatialScale':1,'testingConductanceScale':4,'maximalConnDistance':200,'normalizeConductances':True,\
                            'prePoptargetGroup':{'segmentGroupList':["dendrite_group"],'segmentGroupProbabilities':[1]},\
                            'postPoptargetGroup':{'segmentGroupList':["dendrite_group"],'segmentGroupProbabilities':[1]}})

    net_params_test_2010_multiple['experiment1']['inputParams']=[]

    inputGroups_pop0_2010exp1=[]
    inputGroups_pop0_2010exp1.append({'inputModel':"testing",'testingModel':"pulseGenerators",'cellFractionToTarget':0.5,'delay':20,'duration':200,'amplitude':4E-5,
                         'ampUnits':"uA",'timeUnit':'ms'})

    inputGroups_pop1_2010exp1=[]
    inputGroups_pop1_2010exp1.append({'inputModel':"testing",'testingModel':"pulseGenerators",'cellFractionToTarget':0.5,'delay':220,'duration':200,'amplitude':-0.5E-5,
                         'ampUnits':"uA",'timeUnits':'ms'})




    net_params_test_2010_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_2010exp1})
    net_params_test_2010_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop1','inputGroups':inputGroups_pop1_2010exp1})



    #exp2
    net_params_test_2010_multiple['experiment2']['popParams']=[]
    net_params_test_2010_multiple['experiment2']['popParams'].append({'popID':'Golgi_pop0','cellType':"Very_Simple_Golgi_test_morph",'size':10})
    net_params_test_2010_multiple['experiment2']['popParams'].append({'popID':'Golgi_pop1','cellType':"Very_Simple_Golgi_test_morph",'size':10})

    net_params_test_2010_multiple['experiment2']['distributionParams']={}
    net_params_test_2010_multiple['experiment2']['distributionParams']['distributionModel']="random"
    net_params_test_2010_multiple['experiment2']['distributionParams']['xDim']=100
    net_params_test_2010_multiple['experiment2']['distributionParams']['yDim']=100
    net_params_test_2010_multiple['experiment2']['distributionParams']['yDim']=100

    ##### as conductance levels are soma-to-soma distance-dependent in a Vervaeke_2010_based model, subcellular targeting is not implemented in this configuration. If   one wants to specify multiple GJs per cell pair with constant or heterogeneous conductances one can use Vervaeke_2012_based connModel
    net_params_test_2010_multiple['experiment2']['connParams']={}
    net_params_test_2010_multiple['experiment2']['connParams']['connModel']="Vervaeke_2010_based"
    net_params_test_2010_multiple['experiment2']['connParams']['populationPairs']=[]
    net_params_test_2010_multiple['experiment2']['connParams']['populationPairs'].append({'prePopID':'Golgi_pop0',\
                                                    'postPopID':'Golgi_pop1','spatialScale':20,'testingConductanceScale':4,'maximalConnDistance':200,'normalizeConductances':True,\
                            'prePoptargetGroup':{'segmentGroupList':["dendrite_group"],'segmentGroupProbabilities':[1]},\
                            'postPoptargetGroup':{'segmentGroupList':["dendrite_group"],'segmentGroupProbabilities':[1]}})

    net_params_test_2010_multiple['experiment1']['inputParams']=[]
    inputGroups_pop0_2010exp1=[]
    inputGroups_pop0_2010exp1.append({'inputModel':"testing",'testingModel':"pulseGenerators",'cellFractionToTarget':0.5,'delay':20,'duration':200,'amplitude':4E-5,
                         'ampUnits':"uA",'timeUnit':'ms'})

    inputGroups_pop1_2010exp1=[]
    inputGroups_pop1_2010exp1.append({'inputModel':"testing",'testingModel':"pulseGenerators",'cellFractionToTarget':0.5,'delay':220,'duration':200,'amplitude':-0.5E-5,
                         'ampUnits':"uA",'timeUnits':'ms'})




    net_params_test_2010_multiple['experiment2']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_2010exp1})
    net_params_test_2010_multiple['experiment2']['inputParams'].append({'popName':'Golgi_pop1','inputGroups':inputGroups_pop1_2010exp1})



    sim_params={'simulator':"no simulation",'duration':450,'timeStep':0.005,'numTrials':5,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,'saveSomataPositions':True}
    
    ##### run all simulations
    run_simulations(net_params_test_2012_multiple,sim_params)


    ##############

  

    ###################### Based on 2012 rules


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

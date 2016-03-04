import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from PythonUtils.Simulate_Golgi_Network_v2 import *

################ similar to Golgi_V2012_test2.py but contains two populations. Golgi_V2012_test2.py is used for testing and debugging

if __name__ == "__main__":
   
    net_params_test_2012_multiple={}
    net_params_test_2012_multiple['experiment1']={}
    
    
    net_params_test_2012_multiple['experiment1']['experimentID']="V2012_test1"
    #exp1 other experiments can be added that differ from the exp1 by specific parameter values
    net_params_test_2012_multiple['experiment1']['popParams']=[]
    net_params_test_2012_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_5comp_3channels_1CaPool",'size':15})
    net_params_test_2012_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop1','cellType':"Golgi_5comp_3channels_1CaPool",'size':15})

    net_params_test_2012_multiple['experiment1']['distributionParams']={}
    net_params_test_2012_multiple['experiment1']['distributionParams']['populationList']=[]
    net_params_test_2012_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Golgi_pop0','distributionModel':'explicit_cell_numbers','distanceModel':'random_minimal_distance',\
            'minimal_distance':25,'xDim':100,'yDim':100,'zDim':100})
    net_params_test_2012_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Golgi_pop1','distributionModel':'explicit_cell_numbers','distanceModel':'random_minimal_distance',\
            'minimal_distance':25,'xDim':100,'yDim':100,'zDim':100})

    net_params_test_2012_multiple['experiment1']['connParams']={}
    net_params_test_2012_multiple['experiment1']['connParams']['populationPairs']=[]
    net_params_test_2012_multiple['experiment1']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2012_based",'prePopID':'Golgi_pop0',\
                                                    'postPopID':'Golgi_pop1','conductanceModel':"variable","distribution":"gaussian",\
                                                    'averageConductance':426,'stdDev':20,'units':"pS",'maximalConnDistance':150,\
                                                     'gapJunctionModel':"constant number of GJ contacts per pair",'numberGJ':8,\
                                                     'spatialScale':1,'testingConductanceScale':1,\
                            'targetingModelprePop':{'model':"segment groups and segments",'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]},\
                            'targetingModelpostPop':{'model':"segment groups and segments",\
                                                'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]}})
    
    
    

    
    net_params_test_2012_multiple['experiment1']['inputParams']=[]
    inputGroups_pop0_exp1=[]
    inputGroups_pop0_exp1.append({'inputModel':"variable_basal_firing_rate",'amplitudeDistribution':"gaussian",'averageAmp':50,'stDevAmp':25,'ampUnits':"pA",\
                             'offsetDistribution':"constant",'valueOffset':50,'offsetUnits':"ms"})
    synapseList_pop0_exp1=[]
    synapseList_pop0_exp1.append({'synapseType':"PFSpikeSyn",'synapseMode':"transient",'averageRate':300,'delay':80,'duration':100,'units':'ms',\
                             'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                             'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]})
                            
    synapseList_pop0_exp1.append({'synapseType':"PFSpikeSyn",'synapseMode':"persistent",'averageRate':100,\
                             'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                             'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]})
    

    inputGroups_pop0_exp1.append({'inputModel':'XF','targetingRegime':"uniform",'fractionToTarget':0.5,\
                                  'synapseList':synapseList_pop0_exp1,'colocalizeSynapses':False})

    inputGroups_pop1_exp1=[]
    inputGroups_pop1_exp1.append({'inputModel':"variable_basal_firing_rate",'amplitudeDistribution':"gaussian",'averageAmp':50,'stDevAmp':25,'ampUnits':"pA",\
                            'offsetDistribution':"constant",'valueOffset':50,'offsetUnits':"ms"})
   
    synapseList_pop1_exp1=[]
    synapseList_pop1_exp1.append({'synapseType':"PFSpikeSyn",'synapseMode':"transient",'averageRate':150,'delay':80,'duration':100,'units':'ms',\
                             'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segments and subsegments",\
                             'segmentList':["Soma","dend_3"],'segmentProbabilities':[0.7,0.3],'fractionAlongANDsubsegProbabilities':[[[0.25,1],[0.25,0]],[[0.25,0.7],[0.25,0.3]]]})
    ##### Note that segment fractionAlongs and probabilities have to add to 1                  
    synapseList_pop1_exp1.append({'synapseType':"PFSpikeSyn",'synapseMode':"persistent",'averageRate':100,\
                             'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segments and subsegments",\
                             'segmentList':["Soma","dend_3"],'segmentProbabilities':[0.7,0.3],'fractionAlongANDsubsegProbabilities':[[[0.25,1],[0.25,0]],[[0.25,0.7],[0.25,0.3]]]})


    inputGroups_pop1_exp1.append({'inputModel':'XF','targetingRegime':"uniform",'fractionToTarget':0.5,\
                                  'synapseList':synapseList_pop1_exp1,'colocalizeSynapses':False})
    
                             
    net_params_test_2012_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp1})
    net_params_test_2012_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop1','inputGroups':inputGroups_pop1_exp1})

   
    sim_params={'simulator':"no simulation",'duration':450,'timeStep':0.005,'numTrials':1,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,\
    'saveSomataPositions':True,'parentDirRequired':True,'parentDir':parentdir,'currentDirRequired':True,'currentDir':currentdir,'networkDir':'example'}
    
    ##### run all simulations
    run_simulations(net_params_test_2012_multiple,sim_params)

   
   

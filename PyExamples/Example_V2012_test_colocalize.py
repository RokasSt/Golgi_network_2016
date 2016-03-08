import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from PythonUtils.Simulate_Golgi_Network_v2 import *

################ similar to Golgi_V2012_test2.py but contains two populations. Golgi_V2012_test2.py is used for testing and debugging

if __name__ == "__main__":
   
    net_params_test_2012_multiple={}
    net_params_test_2012_multiple['experiment1']={}
    
    
    net_params_test_2012_multiple['experiment1']['experimentID']="V2012_test1_import_colocalize"
    #exp1 other experiments can be added that differ from the exp1 by specific parameter values
    net_params_test_2012_multiple['experiment1']['popParams']=[]
    net_params_test_2012_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_5comp_3channels_1CaPool",'size':15})
    

    net_params_test_2012_multiple['experiment1']['distributionParams']={}
    net_params_test_2012_multiple['experiment1']['distributionParams']['populationList']=[]
    net_params_test_2012_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Golgi_pop0','distributionModel':'explicit_cell_numbers','distanceModel':'random_minimal_distance',\
            'minimal_distance':25,'xDim':40,'yDim':40,'zDim':40})
  

    net_params_test_2012_multiple['experiment1']['connParams']={}
    net_params_test_2012_multiple['experiment1']['connParams']['populationPairs']=[]
    net_params_test_2012_multiple['experiment1']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2012_based",'prePopID':'Golgi_pop0',\
                                                    'postPopID':'Golgi_pop0','conductanceModel':"variable","distribution":"gaussian",\
                                                    'averageConductance':426,'stdDev':20,'units':"pS",'maximalConnDistance':150,\
                                                     'gapJunctionModel':"variable number of GJ contacts per pair",'distributionGJ':'binomial',\
'maxNoGJs':10,'averageNoGJs':7, 'spatialScale':1,'testingConductanceScale':1,\
                            'targetingModelprePop':{'model':"segment groups and segments",'segmentGroupList':["Section_1","dend_1"],\
                            'segmentGroupProbabilities':{"Section_1":0.7,"dend_1":0.3}},'targetingModelpostPop':{'model':"segment groups and segments",\
                                                'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':{"Section_1":0.7,"dend_1":0.3} }})
    
    
    

    
    net_params_test_2012_multiple['experiment1']['inputParams']=[]
    inputGroups_pop0_exp1=[]
    inputGroups_pop0_exp1.append({'inputModel':"variable_basal_firing_rate",'inputLabel':'vrpop0','amplitudeDistribution':"gaussian",'averageAmp':50,'stDevAmp':25,'ampUnits':"pA",\
                             'offsetDistribution':"constant",'valueOffset':50,'offsetUnits':"ms"})
   

   
  
    synapseList_pop0_exp1=[]
    synapseList_pop0_exp1.append({'synapseType':"MFSpikeSyn"})
    synapseList_pop0_exp1.append({'synapseType':"MF_PF_SpikeSynNMDA"})
    inputGroups_pop0_exp1.append({'inputModel':'XF','targetingRegime':"uniform",'inputLabel':'MF_AMPA_NMDA','fractionToTarget':0.5,\
                            'synapseList':synapseList_pop0_exp1,'colocalizeSynapses':True,'synapseMode':"transient",'averageRate':150,'delay':80,'duration':100,'units':'ms',\
   'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segments and subsegments",\
      'segmentList':["Soma","dend_1"],'segmentProbabilities':{"Soma":0.7,"dend_1":0.3},\
'fractionAlongANDsubsegProbabilities':{"Soma":[{"fractionAlong":0.25,"Prob":1},{"fractionAlong":0.25,"Prob":0}],"dend_1":[{"fractionAlong":0.5,"Prob":0.7},{"fractionAlong":0.5,"Prob":0.3}]}})
  
   
   
                             
    net_params_test_2012_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp1})
   

    library_params={'libraryScale':1,'simulator':'jNeuroML'}
    sim_params={'simulator':"no simulation",'duration':450,'timeStep':0.005,'numTrials':1,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,\
    'saveSomataPositions':True,'parentDirRequired':True,'parentDir':parentdir,'currentDirRequired':True,'currentDir':currentdir,'networkDir':'example',\
        'saveInputReceivingCellID':True,'importPoissonTrainLibraries':True,'PoissonTrainLibraryID':'newlyGenerated','libraryParams':library_params}
    # alternatively, 'PoissonTrainLibraryID':'experimentID' but then requires the same number of trials.
    ##### run all simulations
    # introduce group label
    library_params={'libraryScale':1,'simulator':'jNeuroML'}
    
    #generatePoissonTrainLibraries(net_params_test_2012_multiple,sim_params,library_params)
    
    run_simulations(net_params_test_2012_multiple,sim_params)

   
   

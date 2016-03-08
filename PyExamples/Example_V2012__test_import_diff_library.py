import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from PythonUtils.Simulate_Golgi_Network_v2 import *

################ similar to Golgi_V2012_test2.py but contains two populations. Golgi_V2012_test2.py is used for testing and debugging

if __name__ == "__main__":
   
    net_params_test_2012_multiple={}
    net_params_test_2012_multiple['experiment1']={}
    
    
    net_params_test_2012_multiple['experiment1']['experimentID']="V2012_test_import_diff_library"
    #exp1 other experiments can be added that differ from the exp1 by specific parameter values
    net_params_test_2012_multiple['experiment1']['popParams']=[]
    net_params_test_2012_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_10comp_13channels_2CaPools",'size':2,"NeuroML2CellType":"cell2CaPools"})
   

    net_params_test_2012_multiple['experiment1']['distributionParams']={}
    net_params_test_2012_multiple['experiment1']['distributionParams']['populationList']=[]
    net_params_test_2012_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Golgi_pop0','distributionModel':'explicit_cell_numbers','distanceModel':'random_minimal_distance',\
            'minimal_distance':10,'xDim':40,'yDim':40,'zDim':40})
    

    net_params_test_2012_multiple['experiment1']['connParams']={}
    net_params_test_2012_multiple['experiment1']['connParams']['populationPairs']=[]
    net_params_test_2012_multiple['experiment1']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2012_based",'prePopID':'Golgi_pop0',\
                                                    'postPopID':'Golgi_pop0','conductanceModel':"variable","distribution":"gaussian",\
                                                    'averageConductance':426,'stdDev':20,'units':"pS",'maximalConnDistance':100,\
                                                     'gapJunctionModel':"constant number of GJ contacts per pair",'numberGJ':8,\
                                                     'spatialScale':1,'testingConductanceScale':1,\
                            'targetingModelprePop':{'model':"segment groups and segments",'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
                            'segmentGroupProbabilities':{"apical_dendrite_group":0.8,"basal_dendrite_group":0.2}},'targetingModelpostPop':{'model':"segment groups and segments", 'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":0.8,"basal_dendrite_group":0.2} }})
    
    
    

    
    net_params_test_2012_multiple['experiment1']['inputParams']=[]
    inputGroups_pop0_exp1=[]
    inputGroups_pop0_exp1.append({'inputModel':"variable_basal_firing_rate",'inputLabel':'vrpop0','amplitudeDistribution':"gaussian",'averageAmp':50,'stDevAmp':25,'ampUnits':"pA",\
                             'offsetDistribution':"constant",'valueOffset':50,'offsetUnits':"ms"})
    synapseList_pop0_exp1=[]
    synapseList_pop0_exp1.append({'synapseType':"PFSpikeSyn",'inputIdLibrary':"XFpop0_Golgi_pop0_syn0",\
                        'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                           'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})
                            
    synapseList_pop0_exp1.append({'synapseType':"PFSpikeSyn",'inputIdLibrary':"XFpop0_Golgi_pop0_syn0",\
                             'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                             'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})
    

    inputGroups_pop0_exp1.append({'inputModel':'XF','inputLabel':'XFpop0','targetingRegime':"uniform",'fractionToTarget':0.5,\
                                  'synapseList':synapseList_pop0_exp1,'colocalizeSynapses':False})

    
                             
    net_params_test_2012_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp1})
    

    library_params={'libraryScale':1,'simulator':'jNeuroML'}
    sim_params={'simulator':"no simulation",'duration':450,'timeStep':0.0005,'numTrials':1,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,\
    'saveSomataPositions':True,'parentDirRequired':True,'parentDir':parentdir,'currentDirRequired':True,'currentDir':currentdir,'networkDir':'example',\
        'saveInputReceivingCellID':True,'importPoissonTrainLibraries':True,'PoissonTrainLibraryID':"V2012_test1_import",'libraryParams':library_params}
    # alternatively, 'PoissonTrainLibraryID':'experimentID' but then requires the same number of trials.
    ##### run all simulations
    # introduce group label
    library_params={'libraryScale':1,'simulator':'jNeuroML'}
    
    #generatePoissonTrainLibraries(net_params_test_2012_multiple,sim_params,library_params)
    
    run_simulations(net_params_test_2012_multiple,sim_params)

   
   

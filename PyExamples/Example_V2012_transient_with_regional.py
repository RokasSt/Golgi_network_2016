import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from PythonUtils.Simulate_Golgi_Network_v2 import *

################ similar to Golgi_V2012_test2.py but contains two populations. Golgi_V2012_test2.py is used for testing and debugging

if __name__ == "__main__":
   
    net_params_test_2012_multiple={}
    net_params_test_2012_multiple['experiment1']={}
    
    
    net_params_test_2012_multiple['experiment1']['experimentID']="V2012_test_transient_plus_regional"
    #exp1 other experiments can be added that differ from the exp1 by specific parameter values
    net_params_test_2012_multiple['experiment1']['popParams']=[]
    net_params_test_2012_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_10comp_13channels_2CaPools",\
'size':50,"NeuroML2CellType":"cell2CaPools"})
   

    net_params_test_2012_multiple['experiment1']['distributionParams']={}
    net_params_test_2012_multiple['experiment1']['distributionParams']['populationList']=[]
    net_params_test_2012_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Golgi_pop0','distributionModel':'explicit_cell_numbers','distanceModel':'random_minimal_distance',\
            'minimal_distance':25,'xDim':350,'yDim':350,'zDim':350})
    

    net_params_test_2012_multiple['experiment1']['connParams']={}
    net_params_test_2012_multiple['experiment1']['connParams']['populationPairs']=[]
    net_params_test_2012_multiple['experiment1']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2012_based",'prePopID':'Golgi_pop0',\
                                                    'postPopID':'Golgi_pop0','conductanceModel':"variable","distribution":"gaussian",\
                                                    'averageConductance':426,'stdDev':20,'units':"pS",'maximalConnDistance':300,\
                                                     'gapJunctionModel':"constant number of GJ contacts per pair",'numberGJ':8,\
                                                     'spatialScale':1,'testingConductanceScale':1,\
                            'targetingModelprePop':{'model':"segment groups and segments",'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
                            'segmentGroupProbabilities':{"apical_dendrite_group":0.8,"basal_dendrite_group":0.2}},'targetingModelpostPop':{'model':"segment groups and segments", 'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":0.8,"basal_dendrite_group":0.2} }})
    
    
    

    
    net_params_test_2012_multiple['experiment1']['inputParams']=[]
    inputGroups_pop0_exp1=[]
    inputGroups_pop0_exp1.append({'inputModel':"variable_basal_firing_rate",'inputLabel':'vrpop0','amplitudeDistribution':"gaussian",'averageAmp':50,'stDevAmp':25,'ampUnits':"pA",\
                             'offsetDistribution':"constant",'valueOffset':50,'offsetUnits':"ms"})
    synapseList_pop0_exp1=[]
    synapseList_pop0_exp1.append({'synapseType':"PFSpikeSyn",'synapseMode':"transient",'averageRate':300,'delay':80,'duration':100,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})
                            
    synapseList_pop0_exp1.append({'synapseType':"PFSpikeSyn",'synapseMode':"persistent",'averageRate':100,\
                             'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                             'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})
    

    inputGroups_pop0_exp1.append({'inputModel':'XF','inputLabel':'XFpop0', 'targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[50,150],'yVector':[50,150],'zVector':[50,150]} ],'fractionToTarget':1,'synapseList':synapseList_pop0_exp1,'colocalizeSynapses':False})

    
                             
    net_params_test_2012_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp1})
    

    
    sim_params={'simulator':"no simulation",'duration':450,'timeStep':0.0005,'numTrials':1,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,\
    'saveSomataPositions':True,'parentDirRequired':True,'parentDir':parentdir,'currentDirRequired':True,'currentDir':currentdir,'networkDir':'example',\
        'saveInputReceivingCellID':True}
   
    
    run_simulations(net_params_test_2012_multiple,sim_params)

   
   

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from PythonUtils.Simulate_Golgi_Network_v2 import *


################ similar to Golgi_V2012_test2.py but contains two populations. Golgi_V2012_test2.py is used for testing and debugging

if __name__ == "__main__":
   
    net_params_V2010_multiple={}
    net_params_V2010_multiple['experiment1']={}
    
    
    net_params_V2010_multiple['experiment1']['experimentID']="V2010_test_savings"
   
    
    
    #exp1 
    net_params_V2010_multiple['experiment1']['popParams']=[]
    net_params_V2010_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_10comp_13channels_2CaPools",\
'size':1,"NeuroML2CellType":"cell2CaPools"})
   

    net_params_V2010_multiple['experiment1']['distributionParams']={}
    net_params_V2010_multiple['experiment1']['distributionParams']['populationList']=[]
    net_params_V2010_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Golgi_pop0',\
    'distributionModel':'explicit_cell_numbers','distanceModel':'random_no_overlap','xDim':50,'yDim':50,'zDim':50})
    

    net_params_V2010_multiple['experiment1']['connParams']={}
    net_params_V2010_multiple['experiment1']['connParams']['populationPairs']=[]
    net_params_V2010_multiple['experiment1']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
    'postPopID':'Golgi_pop0','spatialScale':0.5,'testingConductanceScale':1,'units':'nS','normalizeConductances':True,\
        'prePoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5 }},\
        'postPoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5}}})

    
    
    net_params_V2010_multiple['experiment1']['inputParams']=[]
    inputGroups_pop0_exp1=[]
    inputGroups_pop0_exp1.append({'inputModel':"variable_basal_firing_rate",'inputLabel':'vrpop0','amplitudeDistribution':"gaussian",'averageAmp':0,\
    'stDevAmp':50,'ampUnits':"pA",'offsetDistribution':"constant",'valueOffset':0,'offsetUnits':"ms"})
    synapseList0_pop0_exp1=[]
    synapseList0_pop0_exp1.append({'synapseType':"MFSpikeSyn",'synapseMode':"transient",'averageRate':200,'delay':600,'duration':10,'units':'ms',\
                      'numberModel':"constant number of inputs per cell",'noInputs':1,'targetingModel':"segment groups and segments",\
                       'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList0_pop0_exp1.append({'synapseType':"PFSpikeSyn",'synapseMode':"transient",'averageRate':350,'delay':610,'duration':15,'units':'ms',\
                      'numberModel':"constant number of inputs per cell",'noInputs':1,'targetingModel':"segment groups and segments",\
                       'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    synapseList1_pop0_exp1=[]
    synapseList1_pop0_exp1.append({'synapseType':"MFSpikeSyn",'synapseMode':"persistent",'averageRate':2,\
                      'numberModel':"constant number of inputs per cell",'noInputs':1,'targetingModel':"segment groups and segments",\
                        'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})
    

    synapseList1_pop0_exp1.append({'synapseType':"PFSpikeSyn",'synapseMode':"persistent",'averageRate':0.5,\
                     'numberModel':"constant number of inputs per cell",'noInputs':1,'targetingModel':"segment groups and segments",\
                       'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})
    

    inputGroups_pop0_exp1.append({'inputModel':'XF','inputLabel':'XFpop0','targetingRegime':"uniform",'fractionToTarget':0.22,\
                              'synapseList':synapseList0_pop0_exp1,'colocalizeSynapses':False})

    inputGroups_pop0_exp1.append({'inputModel':'XF','inputLabel':'XFpop0_background','targetingRegime':"uniform",'fractionToTarget':1,\
                                 'synapseList':synapseList1_pop0_exp1,'colocalizeSynapses':False})
    
                             
    net_params_V2010_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp1})
    

   

    
    
    #######
    
    library_params={'libraryScale':2,'simulator':'jNeuroML_NEURON','timeStep':0.01}

    sim_params={'simulator':"jNeuroML_NEURON",'duration':3000,'timeStep':0.0003,'numTrials':1,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,\
    'saveSomataPositions':True,'parentDirRequired':True,'parentDir':parentdir,'currentDirRequired':True,'currentDir':currentdir,'networkDir':'experiment',\
        'saveInputReceivingCellID':True,'importPoissonTrainLibraries':True,'PoissonTrainLibraryID':'newlyGenerated','libraryParams':library_params}
    
    
    #generatePoissonTrainLibraries(net_params_V2010_multiple,sim_params,library_params)
    
    
    
    run_simulations(net_params_V2010_multiple,sim_params)

   

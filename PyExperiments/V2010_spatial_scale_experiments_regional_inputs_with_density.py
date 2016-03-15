import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from PythonUtils.Simulate_Golgi_Network_v2 import *

################ similar to Golgi_V2012_test2.py but contains two populations. Golgi_V2012_test2.py is used for testing and debugging

if __name__ == "__main__":
   
    net_params_V2010_multiple={}
    net_params_V2010_multiple['experiment1']={}
    net_params_V2010_multiple['experiment2']={}
    net_params_V2010_multiple['experiment3']={}
    net_params_V2010_multiple['experiment4']={}
    net_params_V2010_multiple['experiment5']={}
    
    
    net_params_V2010_multiple['experiment1']['experimentID']="V2010_sp_scale_05_regional_dens"
    net_params_V2010_multiple['experiment2']['experimentID']="V2010_sp_scale_1_regional_dens"
    net_params_V2010_multiple['experiment3']['experimentID']="V2010_sp_scale_5_regional_dens"
    net_params_V2010_multiple['experiment4']['experimentID']="V2010_sp_scale_25_regional_dens"
    net_params_V2010_multiple['experiment5']['experimentID']="V2010_sp_scale_128_regional_dens"
    
    
    #exp1 
    net_params_V2010_multiple['experiment1']['popParams']=[]
    net_params_V2010_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_10comp_13channels_2CaPools",\
'size':112,"NeuroML2CellType":"cell2CaPools"})
   

    net_params_V2010_multiple['experiment1']['distributionParams']={}
    net_params_V2010_multiple['experiment1']['distributionParams']['populationList']=[]
    net_params_V2010_multiple['experiment1']['distributionParams']['populationList'].append({'distributionModel':"density_profile",'popID':'Golgi_pop0','densityFilePath':'/home/rokas/Golgi_data/Pure NeuG density matrix of shape 69 630.txt',\
    'planeDimensions':{'dim1':'x','dim2':'y'},'dim1CoordinateVector':[0,3000],'dim2CoordinateVector':[0,110],'dim3':'z','dim3Boundary':120,\
    'distanceModel':'random','canonicalVolumeBaseAreainMicrons':5.00318495*5.00318495 })
    

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
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList0_pop0_exp1.append({'synapseType':"PFSpikeSyn",'synapseMode':"transient",'averageRate':350,'delay':610,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    synapseList1_pop0_exp1=[]
    synapseList1_pop0_exp1.append({'synapseType':"MFSpikeSyn",'synapseMode':"persistent",'averageRate':2,\
                       'numberModel':"constant number of inputs per cell",'noInputs':20,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})
    

    synapseList1_pop0_exp1.append({'synapseType':"PFSpikeSyn",'synapseMode':"persistent",'averageRate':0.5,\
                       'numberModel':"constant number of inputs per cell",'noInputs':100,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})
    

    inputGroups_pop0_exp1.append({'inputModel':'XF','inputLabel':'XFpop0', 'targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[225,325],'yVector':[225,325],'zVector':[0,80]},'fractionToTarget':1,\
                                  'synapseList':synapseList0_pop0_exp1,'colocalizeSynapses':False})

    inputGroups_pop0_exp1.append({'inputModel':'XF','inputLabel':'XFpop0_background','targetingRegime':"uniform",'fractionToTarget':1,\
                                  'synapseList':synapseList1_pop0_exp1,'colocalizeSynapses':False})
    
                             
    net_params_V2010_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp1})
    

    #exp2
    net_params_V2010_multiple['experiment2']['popParams']=[]
    net_params_V2010_multiple['experiment2']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_10comp_13channels_2CaPools",\
'size':112,"NeuroML2CellType":"cell2CaPools"})
   

    net_params_V2010_multiple['experiment2']['distributionParams']={}
    net_params_V2010_multiple['experiment2']['distributionParams']['populationList']=[]
    net_params_V2010_multiple['experiment2']['distributionParams']['populationList'].append({'distributionModel':"density_profile",'popID':'Golgi_pop0','densityFilePath':'/home/rokas/Golgi_data/Pure NeuG density matrix of shape 69 630.txt',\
    'planeDimensions':{'dim1':'x','dim2':'y'},'dim1CoordinateVector':[0,3000],'dim2CoordinateVector':[0,110],'dim3':'z','dim3Boundary':120,\
    'distanceModel':'random','canonicalVolumeBaseAreainMicrons':5.00318495*5.00318495 })
    

    net_params_V2010_multiple['experiment2']['connParams']={}
    net_params_V2010_multiple['experiment2']['connParams']['populationPairs']=[]
    net_params_V2010_multiple['experiment2']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
    'postPopID':'Golgi_pop0','spatialScale':1.0,'testingConductanceScale':1,'units':'nS','normalizeConductances':True,\
        'prePoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5 }},\
        'postPoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5}}})

    
    
    net_params_V2010_multiple['experiment2']['inputParams']=[]
    inputGroups_pop0_exp2=[]
    inputGroups_pop0_exp2.append({'inputModel':"variable_basal_firing_rate",'inputLabel':'vrpop0','amplitudeDistribution':"gaussian",'averageAmp':0,\
    'stDevAmp':50,'ampUnits':"pA",'offsetDistribution':"constant",'valueOffset':0,'offsetUnits':"ms"})
    synapseList0_pop0_exp2=[]
    synapseList0_pop0_exp2.append({'synapseType':"MFSpikeSyn",'synapseMode':"transient",'averageRate':200,'delay':600,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList0_pop0_exp2.append({'synapseType':"PFSpikeSyn",'synapseMode':"transient",'averageRate':350,'delay':610,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    synapseList1_pop0_exp2=[]
    synapseList1_pop0_exp2.append({'synapseType':"MFSpikeSyn",'synapseMode':"persistent",'averageRate':2,\
                       'numberModel':"constant number of inputs per cell",'noInputs':20,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})
    

    synapseList1_pop0_exp2.append({'synapseType':"PFSpikeSyn",'synapseMode':"persistent",'averageRate':0.5,\
                       'numberModel':"constant number of inputs per cell",'noInputs':100,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})
    

    inputGroups_pop0_exp2.append({'inputModel':'XF','inputLabel':'XFpop0','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[225,325],'yVector':[225,325],'zVector':[0,80]},'fractionToTarget':1,\
                                  'synapseList':synapseList0_pop0_exp2,'colocalizeSynapses':False})

    inputGroups_pop0_exp2.append({'inputModel':'XF','inputLabel':'XFpop0_background','targetingRegime':"uniform",'fractionToTarget':1,\
                                  'synapseList':synapseList1_pop0_exp2,'colocalizeSynapses':False})
    
                             
    net_params_V2010_multiple['experiment2']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp2})



    #exp3
    net_params_V2010_multiple['experiment3']['popParams']=[]
    net_params_V2010_multiple['experiment3']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_10comp_13channels_2CaPools",\
'size':112,"NeuroML2CellType":"cell2CaPools"})
   

    net_params_V2010_multiple['experiment3']['distributionParams']={}
    net_params_V2010_multiple['experiment3']['distributionParams']['populationList']=[]
    net_params_V2010_multiple['experiment3']['distributionParams']['populationList'].append({'distributionModel':"density_profile",'popID':'Golgi_pop0','densityFilePath':'/home/rokas/Golgi_data/Pure NeuG density matrix of shape 69 630.txt',\
    'planeDimensions':{'dim1':'x','dim2':'y'},'dim1CoordinateVector':[0,3000],'dim2CoordinateVector':[0,110],'dim3':'z','dim3Boundary':120,\
    'distanceModel':'random','canonicalVolumeBaseAreainMicrons':5.00318495*5.00318495})
    

    net_params_V2010_multiple['experiment3']['connParams']={}
    net_params_V2010_multiple['experiment3']['connParams']['populationPairs']=[]
    net_params_V2010_multiple['experiment3']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
    'postPopID':'Golgi_pop0','spatialScale':5.0,'testingConductanceScale':1,'units':'nS','normalizeConductances':True,\
        'prePoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5 }},\
        'postPoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5}}})

    
    
    net_params_V2010_multiple['experiment3']['inputParams']=[]
    inputGroups_pop0_exp3=[]
    inputGroups_pop0_exp3.append({'inputModel':"variable_basal_firing_rate",'inputLabel':'vrpop0','amplitudeDistribution':"gaussian",'averageAmp':0,\
    'stDevAmp':50,'ampUnits':"pA",'offsetDistribution':"constant",'valueOffset':0,'offsetUnits':"ms"})
    synapseList0_pop0_exp3=[]
    synapseList0_pop0_exp3.append({'synapseType':"MFSpikeSyn",'synapseMode':"transient",'averageRate':200,'delay':600,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList0_pop0_exp3.append({'synapseType':"PFSpikeSyn",'synapseMode':"transient",'averageRate':350,'delay':610,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    synapseList1_pop0_exp3=[]
    synapseList1_pop0_exp3.append({'synapseType':"MFSpikeSyn",'synapseMode':"persistent",'averageRate':2,\
                       'numberModel':"constant number of inputs per cell",'noInputs':20,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})
    

    synapseList1_pop0_exp3.append({'synapseType':"PFSpikeSyn",'synapseMode':"persistent",'averageRate':0.5,\
                       'numberModel':"constant number of inputs per cell",'noInputs':100,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})
    

    inputGroups_pop0_exp3.append({'inputModel':'XF','inputLabel':'XFpop0','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[225,325],'yVector':[225,325],'zVector':[0,80]},'fractionToTarget':1,\
                                  'synapseList':synapseList0_pop0_exp3,'colocalizeSynapses':False})

    inputGroups_pop0_exp3.append({'inputModel':'XF','inputLabel':'XFpop0_background','targetingRegime':"uniform",'fractionToTarget':1,\
                                  'synapseList':synapseList1_pop0_exp3,'colocalizeSynapses':False})
    
                             
    net_params_V2010_multiple['experiment3']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp3})

    #exp4
    net_params_V2010_multiple['experiment4']['popParams']=[]
    net_params_V2010_multiple['experiment4']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_10comp_13channels_2CaPools",\
'size':112,"NeuroML2CellType":"cell2CaPools"})
   

    net_params_V2010_multiple['experiment4']['distributionParams']={}
    net_params_V2010_multiple['experiment4']['distributionParams']['populationList']=[]
    net_params_V2010_multiple['experiment4']['distributionParams']['populationList'].append({'distributionModel':"density_profile",'popID':'Golgi_pop0','densityFilePath':'/home/rokas/Golgi_data/Pure NeuG density matrix of shape 69 630.txt',\
    'planeDimensions':{'dim1':'x','dim2':'y'},'dim1CoordinateVector':[0,3000],'dim2CoordinateVector':[0,110],'dim3':'z','dim3Boundary':120,\
    'distanceModel':'random','canonicalVolumeBaseAreainMicrons':5.00318495*5.00318495})
    

    net_params_V2010_multiple['experiment4']['connParams']={}
    net_params_V2010_multiple['experiment4']['connParams']['populationPairs']=[]
    net_params_V2010_multiple['experiment4']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
    'postPopID':'Golgi_pop0','spatialScale':25,'testingConductanceScale':1,'units':'nS','normalizeConductances':True,\
        'prePoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5 }},\
        'postPoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5}}})

    
    
    net_params_V2010_multiple['experiment4']['inputParams']=[]
    inputGroups_pop0_exp4=[]
    inputGroups_pop0_exp4.append({'inputModel':"variable_basal_firing_rate",'inputLabel':'vrpop0','amplitudeDistribution':"gaussian",'averageAmp':0,\
    'stDevAmp':50,'ampUnits':"pA",'offsetDistribution':"constant",'valueOffset':0,'offsetUnits':"ms"})
    synapseList0_pop0_exp4=[]
    synapseList0_pop0_exp4.append({'synapseType':"MFSpikeSyn",'synapseMode':"transient",'averageRate':200,'delay':600,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList0_pop0_exp4.append({'synapseType':"PFSpikeSyn",'synapseMode':"transient",'averageRate':350,'delay':610,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    synapseList1_pop0_exp4=[]
    synapseList1_pop0_exp4.append({'synapseType':"MFSpikeSyn",'synapseMode':"persistent",'averageRate':2,\
                       'numberModel':"constant number of inputs per cell",'noInputs':20,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})
    

    synapseList1_pop0_exp4.append({'synapseType':"PFSpikeSyn",'synapseMode':"persistent",'averageRate':0.5,\
                       'numberModel':"constant number of inputs per cell",'noInputs':100,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})
    

    inputGroups_pop0_exp4.append({'inputModel':'XF','inputLabel':'XFpop0','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[225,325],'yVector':[225,325],'zVector':[0,80]},'fractionToTarget':1,\
                                  'synapseList':synapseList0_pop0_exp4,'colocalizeSynapses':False})

    inputGroups_pop0_exp4.append({'inputModel':'XF','inputLabel':'XFpop0_background','targetingRegime':"uniform",'fractionToTarget':1,\
                                  'synapseList':synapseList1_pop0_exp4,'colocalizeSynapses':False})
    
                             
    net_params_V2010_multiple['experiment4']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp4})


    #exp5
    net_params_V2010_multiple['experiment5']['popParams']=[]
    net_params_V2010_multiple['experiment5']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_10comp_13channels_2CaPools",\
'size':112,"NeuroML2CellType":"cell2CaPools"})
   

    net_params_V2010_multiple['experiment5']['distributionParams']={}
    net_params_V2010_multiple['experiment5']['distributionParams']['populationList']=[]
    net_params_V2010_multiple['experiment5']['distributionParams']['populationList'].append({'distributionModel':"density_profile",'popID':'Golgi_pop0','densityFilePath':'/home/rokas/Golgi_data/Pure NeuG density matrix of shape 69 630.txt',\
    'planeDimensions':{'dim1':'x','dim2':'y'},'dim1CoordinateVector':[0,3000],'dim2CoordinateVector':[0,110],'dim3':'z','dim3Boundary':120,\
    'distanceModel':'random','canonicalVolumeBaseAreainMicrons':5.00318495*5.00318495})
    

    net_params_V2010_multiple['experiment5']['connParams']={}
    net_params_V2010_multiple['experiment5']['connParams']['populationPairs']=[]
    net_params_V2010_multiple['experiment5']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
    'postPopID':'Golgi_pop0','spatialScale':128.0,'testingConductanceScale':1,'units':'nS','normalizeConductances':True,\
        'prePoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5 }},\
        'postPoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5}}})

    
    
    net_params_V2010_multiple['experiment5']['inputParams']=[]
    inputGroups_pop0_exp5=[]
    inputGroups_pop0_exp5.append({'inputModel':"variable_basal_firing_rate",'inputLabel':'vrpop0','amplitudeDistribution':"gaussian",'averageAmp':0,\
    'stDevAmp':50,'ampUnits':"pA",'offsetDistribution':"constant",'valueOffset':0,'offsetUnits':"ms"})
    synapseList0_pop0_exp5=[]
    synapseList0_pop0_exp5.append({'synapseType':"MFSpikeSyn",'synapseMode':"transient",'averageRate':200,'delay':600,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList0_pop0_exp5.append({'synapseType':"PFSpikeSyn",'synapseMode':"transient",'averageRate':350,'delay':610,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    synapseList1_pop0_exp5=[]
    synapseList1_pop0_exp5.append({'synapseType':"MFSpikeSyn",'synapseMode':"persistent",'averageRate':2,\
                       'numberModel':"constant number of inputs per cell",'noInputs':20,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})
    

    synapseList1_pop0_exp5.append({'synapseType':"PFSpikeSyn",'synapseMode':"persistent",'averageRate':0.5,\
                       'numberModel':"constant number of inputs per cell",'noInputs':100,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})
    

    inputGroups_pop0_exp5.append({'inputModel':'XF','inputLabel':'XFpop0','targetingRegime':"3D_region_specific",'regionList':[{'xVector':[225,325],'yVector':[225,325],'zVector':[0,80]},'fractionToTarget':1,\
                                  'synapseList':synapseList0_pop0_exp5,'colocalizeSynapses':False})

    inputGroups_pop0_exp5.append({'inputModel':'XF','inputLabel':'XFpop0_background','targetingRegime':"uniform",'fractionToTarget':1,\
                                  'synapseList':synapseList1_pop0_exp5,'colocalizeSynapses':False})
    
                             
    net_params_V2010_multiple['experiment5']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp5})

    
    
    #######
    
    library_params={'libraryScale':3,'simulator':'jNeuroML'}
    sim_params={'simulator':"jNeuroML_NEURON",'duration':3000,'timeStep':0.0003,'numTrials':15,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,\
    'saveSomataPositions':True,'parentDirRequired':True,'parentDir':parentdir,'currentDirRequired':True,'currentDir':currentdir,'networkDir':'example',\
        'saveInputReceivingCellID':True,'importPoissonTrainLibraries':True,'PoissonTrainLibraryID':'newlyGenerated','libraryParams':library_params}
    
    
    generatePoissonTrainLibraries(net_params_V2010_multiple,sim_params,library_params)
    
    run_simulations(net_params_V2010_multiple,sim_params)

   

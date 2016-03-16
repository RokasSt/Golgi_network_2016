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
    
    
    net_params_V2010_multiple['experiment1']['experimentID']="V2010_regional_from_left_to_right_200ms"
    net_params_V2010_multiple['experiment2']['experimentID']="V2010_regional_from_left_to_right_100ms"
    net_params_V2010_multiple['experiment3']['experimentID']="V2010_regional_from_left_to_right_50ms"
    net_params_V2010_multiple['experiment4']['experimentID']="V2010_regional_all_0ms"
    net_params_V2010_multiple['experiment5']['experimentID']="V2010_regional_middle_left_right_200ms"
    
    
    
    
    #exp1 
    net_params_V2010_multiple['experiment1']['popParams']=[]
    net_params_V2010_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_10comp_13channels_2CaPools",\
'size':0,"NeuroML2CellType":"cell2CaPools"})
   

    net_params_V2010_multiple['experiment1']['distributionParams']={}
    net_params_V2010_multiple['experiment1']['distributionParams']['populationList']=[]
    net_params_V2010_multiple['experiment1']['distributionParams']['populationList'].append({'distributionModel':"density_profile",'popID':'Golgi_pop0','densityFilePath':'/home/rokas/Golgi_data/Pure NeuG density matrix of shape 69 630.txt',\
    'planeDimensions':{'dim1':'x','dim2':'y'},'dim1CoordinateVector':[0,3000],'dim2CoordinateVector':[0,110],'dim3':'z','dim3Boundary':100,\
    'distanceModel':'random','canonicalVolumeBaseAreainMicrons':5.00318495*5.00318495 })
    

    net_params_V2010_multiple['experiment1']['connParams']={}
    net_params_V2010_multiple['experiment1']['connParams']['populationPairs']=[]
    net_params_V2010_multiple['experiment1']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
    'postPopID':'Golgi_pop0','spatialScale':1.0,'testingConductanceScale':1,'units':'nS','normalizeConductances':False,\
        'prePoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5 }},\
        'postPoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5}}})

    
    
    net_params_V2010_multiple['experiment1']['inputParams']=[]
    ####### left band
    inputGroups_pop0_exp1=[]
    inputGroups_pop0_exp1.append({'inputModel':"variable_basal_firing_rate",'inputLabel':'vrpop0','amplitudeDistribution':"gaussian",'averageAmp':0,\
    'stDevAmp':32,'ampUnits':"pA",'offsetDistribution':"constant",'valueOffset':0,'offsetUnits':"ms"})
    synapseList0_pop0_exp1=[]
    synapseList0_pop0_exp1.append({'synapseType':"MF",'synapseMode':"transient",'averageRate':200,'delay':600,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList0_pop0_exp1.append({'synapseType':"PF",'synapseMode':"transient",'averageRate':350,'delay':610,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    
    inputGroups_pop0_exp1.append({'inputModel':'XF','inputLabel':'XFpop0l','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[0,1000],'yVector':[0,110],'zVector':[0,100]}],'fractionToTarget':0.22,'synapseList':synapseList0_pop0_exp1,'colocalizeSynapses':False})

    ##### middle band
    synapseList1_pop0_exp1=[]
    synapseList1_pop0_exp1.append({'synapseType':"MF",'synapseMode':"transient",'averageRate':200,'delay':825,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList1_pop0_exp1.append({'synapseType':"PF",'synapseMode':"transient",'averageRate':350,'delay':835,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    
    inputGroups_pop0_exp1.append({'inputModel':'XF','inputLabel':'XFpop0m','targetingRegime':"3D_region_specific",\
'regionList':[{'xVector':[1000,2000],'yVector':[0,110],'zVector':[0,100]}],'fractionToTarget':0.22,'synapseList':synapseList1_pop0_exp1,'colocalizeSynapses':False})

    ###### right band
    synapseList2_pop0_exp1=[]
    synapseList2_pop0_exp1.append({'synapseType':"MF",'synapseMode':"transient",'averageRate':200,'delay':1050,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList2_pop0_exp1.append({'synapseType':"PF",'synapseMode':"transient",'averageRate':350,'delay':1060,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    
    inputGroups_pop0_exp1.append({'inputModel':'XF','inputLabel':'XFpop0r','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[2000,3000],'yVector':[0,110],'zVector':[0,100]}],'fractionToTarget':0.22,'synapseList':synapseList2_pop0_exp1,'colocalizeSynapses':False})


    ####### background
    synapseList3_pop0_exp1=[]
    synapseList3_pop0_exp1.append({'synapseType':"MF",'synapseMode':"persistent",'averageRate':2,\
                       'numberModel':"constant number of inputs per cell",'noInputs':20,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})
    

    synapseList3_pop0_exp1.append({'synapseType':"PF",'synapseMode':"persistent",'averageRate':0.5,\
                       'numberModel':"constant number of inputs per cell",'noInputs':100,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})



    inputGroups_pop0_exp1.append({'inputModel':'XF','inputLabel':'XFpop0b','targetingRegime':"uniform",'fractionToTarget':1,\
                                  'synapseList':synapseList3_pop0_exp1,'colocalizeSynapses':False})
    
                             
    net_params_V2010_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp1})
    

    #exp2
    net_params_V2010_multiple['experiment2']['popParams']=[]
    net_params_V2010_multiple['experiment2']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_10comp_13channels_2CaPools",\
'size':0,"NeuroML2CellType":"cell2CaPools"})
   

    net_params_V2010_multiple['experiment2']['distributionParams']={}
    net_params_V2010_multiple['experiment2']['distributionParams']['populationList']=[]
    net_params_V2010_multiple['experiment2']['distributionParams']['populationList'].append({'distributionModel':"density_profile",'popID':'Golgi_pop0','densityFilePath':'/home/rokas/Golgi_data/Pure NeuG density matrix of shape 69 630.txt',\
    'planeDimensions':{'dim1':'x','dim2':'y'},'dim1CoordinateVector':[0,3000],'dim2CoordinateVector':[0,110],'dim3':'z','dim3Boundary':100,\
    'distanceModel':'random','canonicalVolumeBaseAreainMicrons':5.00318495*5.00318495 })
    

    net_params_V2010_multiple['experiment2']['connParams']={}
    net_params_V2010_multiple['experiment2']['connParams']['populationPairs']=[]
    net_params_V2010_multiple['experiment2']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
    'postPopID':'Golgi_pop0','spatialScale':1.0,'testingConductanceScale':1,'units':'nS','normalizeConductances':False,\
        'prePoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5 }},\
        'postPoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5}}})

    
    
    net_params_V2010_multiple['experiment2']['inputParams']=[]
    ####### left band
    inputGroups_pop0_exp2=[]
    inputGroups_pop0_exp2.append({'inputModel':"variable_basal_firing_rate",'inputLabel':'vrpop0','amplitudeDistribution':"gaussian",'averageAmp':0,\
    'stDevAmp':32,'ampUnits':"pA",'offsetDistribution':"constant",'valueOffset':0,'offsetUnits':"ms"})
    synapseList0_pop0_exp2=[]
    synapseList0_pop0_exp2.append({'synapseType':"MF",'synapseMode':"transient",'averageRate':200,'delay':600,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList0_pop0_exp2.append({'synapseType':"PF",'synapseMode':"transient",'averageRate':350,'delay':610,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    
    inputGroups_pop0_exp2.append({'inputModel':'XF','inputLabel':'XFpop0l','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[0,1000],'yVector':[0,110],'zVector':[0,100]}],'fractionToTarget':0.22,'synapseList':synapseList0_pop0_exp2,'colocalizeSynapses':False})

    ##### middle band
    synapseList1_pop0_exp2=[]
    synapseList1_pop0_exp2.append({'synapseType':"MF",'synapseMode':"transient",'averageRate':200,'delay':725,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList1_pop0_exp2.append({'synapseType':"PF",'synapseMode':"transient",'averageRate':350,'delay':735,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    
    inputGroups_pop0_exp2.append({'inputModel':'XF','inputLabel':'XFpop0m','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[1000,2000],'yVector':[0,110],'zVector':[0,100]}],'fractionToTarget':0.22,'synapseList':synapseList1_pop0_exp2,'colocalizeSynapses':False})

    ###### right band
    synapseList2_pop0_exp2=[]
    synapseList2_pop0_exp2.append({'synapseType':"MF",'synapseMode':"transient",'averageRate':200,'delay':850,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList2_pop0_exp2.append({'synapseType':"PF",'synapseMode':"transient",'averageRate':350,'delay':860,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    
    inputGroups_pop0_exp2.append({'inputModel':'XF','inputLabel':'XFpop0r','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[2000,3000],'yVector':[0,110],'zVector':[0,100]}],'fractionToTarget':0.22,'synapseList':synapseList2_pop0_exp2,'colocalizeSynapses':False})


    ####### background
    synapseList3_pop0_exp2=[]
    synapseList3_pop0_exp2.append({'synapseType':"MF",'synapseMode':"persistent",'averageRate':2,\
                       'numberModel':"constant number of inputs per cell",'noInputs':20,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})
    

    synapseList3_pop0_exp2.append({'synapseType':"PF",'synapseMode':"persistent",'averageRate':0.5,\
                       'numberModel':"constant number of inputs per cell",'noInputs':100,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})



    inputGroups_pop0_exp2.append({'inputModel':'XF','inputLabel':'XFpop0b','targetingRegime':"uniform",'fractionToTarget':1,\
                                  'synapseList':synapseList3_pop0_exp2,'colocalizeSynapses':False})
    
                             
    net_params_V2010_multiple['experiment2']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp2})

    #exp3
    net_params_V2010_multiple['experiment3']['popParams']=[]
    net_params_V2010_multiple['experiment3']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_10comp_13channels_2CaPools",\
'size':0,"NeuroML2CellType":"cell2CaPools"})
   

    net_params_V2010_multiple['experiment3']['distributionParams']={}
    net_params_V2010_multiple['experiment3']['distributionParams']['populationList']=[]
    net_params_V2010_multiple['experiment3']['distributionParams']['populationList'].append({'distributionModel':"density_profile",'popID':'Golgi_pop0','densityFilePath':'/home/rokas/Golgi_data/Pure NeuG density matrix of shape 69 630.txt',\
    'planeDimensions':{'dim1':'x','dim2':'y'},'dim1CoordinateVector':[0,3000],'dim2CoordinateVector':[0,110],'dim3':'z','dim3Boundary':100,\
    'distanceModel':'random','canonicalVolumeBaseAreainMicrons':5.00318495*5.00318495 })
    

    net_params_V2010_multiple['experiment3']['connParams']={}
    net_params_V2010_multiple['experiment3']['connParams']['populationPairs']=[]
    net_params_V2010_multiple['experiment3']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
    'postPopID':'Golgi_pop0','spatialScale':1.0,'testingConductanceScale':1,'units':'nS','normalizeConductances':False,\
        'prePoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5 }},\
        'postPoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5}}})

    
    
    net_params_V2010_multiple['experiment3']['inputParams']=[]
    ####### left band
    inputGroups_pop0_exp3=[]
    inputGroups_pop0_exp3.append({'inputModel':"variable_basal_firing_rate",'inputLabel':'vrpop0','amplitudeDistribution':"gaussian",'averageAmp':0,\
    'stDevAmp':32,'ampUnits':"pA",'offsetDistribution':"constant",'valueOffset':0,'offsetUnits':"ms"})
    synapseList0_pop0_exp3=[]
    synapseList0_pop0_exp3.append({'synapseType':"MF",'synapseMode':"transient",'averageRate':200,'delay':600,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList0_pop0_exp3.append({'synapseType':"PF",'synapseMode':"transient",'averageRate':350,'delay':610,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    
    inputGroups_pop0_exp3.append({'inputModel':'XF','inputLabel':'XFpop0l','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[0,1000],'yVector':[0,110],'zVector':[0,100]}],'fractionToTarget':0.22,'synapseList':synapseList0_pop0_exp3,'colocalizeSynapses':False})

    ##### middle band
    synapseList1_pop0_exp3=[]
    synapseList1_pop0_exp3.append({'synapseType':"MF",'synapseMode':"transient",'averageRate':200,'delay':675,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList1_pop0_exp3.append({'synapseType':"PF",'synapseMode':"transient",'averageRate':350,'delay':685,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    
    inputGroups_pop0_exp3.append({'inputModel':'XF','inputLabel':'XFpop0m','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[1000,2000],'yVector':[0,110],'zVector':[0,100]}],'fractionToTarget':0.22,'synapseList':synapseList1_pop0_exp3,'colocalizeSynapses':False})

    ###### right band
    synapseList2_pop0_exp3=[]
    synapseList2_pop0_exp3.append({'synapseType':"MF",'synapseMode':"transient",'averageRate':200,'delay':750,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList2_pop0_exp3.append({'synapseType':"PF",'synapseMode':"transient",'averageRate':350,'delay':810,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    
    inputGroups_pop0_exp3.append({'inputModel':'XF','inputLabel':'XFpop0r','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[2000,3000],'yVector':[0,110],'zVector':[0,100]}],'fractionToTarget':0.22,'synapseList':synapseList2_pop0_exp3,'colocalizeSynapses':False})


    ####### background
    synapseList3_pop0_exp3=[]
    synapseList3_pop0_exp3.append({'synapseType':"MF",'synapseMode':"persistent",'averageRate':2,\
                       'numberModel':"constant number of inputs per cell",'noInputs':20,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})
    

    synapseList3_pop0_exp3.append({'synapseType':"PF",'synapseMode':"persistent",'averageRate':0.5,\
                       'numberModel':"constant number of inputs per cell",'noInputs':100,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})



    inputGroups_pop0_exp3.append({'inputModel':'XF','inputLabel':'XFpop0b','targetingRegime':"uniform",'fractionToTarget':1,\
                                  'synapseList':synapseList3_pop0_exp3,'colocalizeSynapses':False})
    
                             
    net_params_V2010_multiple['experiment3']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp3})
    

    #exp4
    net_params_V2010_multiple['experiment4']['popParams']=[]
    net_params_V2010_multiple['experiment4']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_10comp_13channels_2CaPools",\
'size':112,"NeuroML2CellType":"cell2CaPools"})
   

    net_params_V2010_multiple['experiment4']['distributionParams']={}
    net_params_V2010_multiple['experiment4']['distributionParams']['populationList']=[]
    net_params_V2010_multiple['experiment4']['distributionParams']['populationList'].append({'distributionModel':"density_profile",'popID':'Golgi_pop0','densityFilePath':'/home/rokas/Golgi_data/Pure NeuG density matrix of shape 69 630.txt',\
    'planeDimensions':{'dim1':'x','dim2':'y'},'dim1CoordinateVector':[0,3000],'dim2CoordinateVector':[0,110],'dim3':'z','dim3Boundary':100,\
    'distanceModel':'random','canonicalVolumeBaseAreainMicrons':5.00318495*5.00318495 })
    

    net_params_V2010_multiple['experiment4']['connParams']={}
    net_params_V2010_multiple['experiment4']['connParams']['populationPairs']=[]
    net_params_V2010_multiple['experiment4']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
    'postPopID':'Golgi_pop0','spatialScale':1.0,'testingConductanceScale':1,'units':'nS','normalizeConductances':False,\
        'prePoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5 }},\
        'postPoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5}}})

    
    
    net_params_V2010_multiple['experiment4']['inputParams']=[]
    ####### left band
    inputGroups_pop0_exp4=[]
    inputGroups_pop0_exp4.append({'inputModel':"variable_basal_firing_rate",'inputLabel':'vrpop0','amplitudeDistribution':"gaussian",'averageAmp':0,\
    'stDevAmp':0,'ampUnits':"pA",'offsetDistribution':"constant",'valueOffset':0,'offsetUnits':"ms"})
    synapseList0_pop0_exp4=[]
    synapseList0_pop0_exp4.append({'synapseType':"MF",'synapseMode':"transient",'averageRate':200,'delay':600,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList0_pop0_exp4.append({'synapseType':"PF",'synapseMode':"transient",'averageRate':350,'delay':610,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    
    inputGroups_pop0_exp4.append({'inputModel':'XF','inputLabel':'XFpop0l','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[0,1000],'yVector':[0,110],'zVector':[0,100]}],'fractionToTarget':0.22,'synapseList':synapseList0_pop0_exp4,'colocalizeSynapses':False})

    ##### middle band
    synapseList1_pop0_exp4=[]
    synapseList1_pop0_exp4.append({'synapseType':"MF",'synapseMode':"transient",'averageRate':200,'delay':600,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList1_pop0_exp4.append({'synapseType':"PF",'synapseMode':"transient",'averageRate':350,'delay':610,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    
    inputGroups_pop0_exp4.append({'inputModel':'XF','inputLabel':'XFpop0m','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[1000,2000],'yVector':[0,110],'zVector':[0,100]}],'fractionToTarget':0.22,'synapseList':synapseList1_pop0_exp4,'colocalizeSynapses':False})

    ###### right band
    synapseList2_pop0_exp4=[]
    synapseList2_pop0_exp4.append({'synapseType':"MF",'synapseMode':"transient",'averageRate':200,'delay':600,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList2_pop0_exp4.append({'synapseType':"PF",'synapseMode':"transient",'averageRate':350,'delay':610,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    
    inputGroups_pop0_exp4.append({'inputModel':'XF','inputLabel':'XFpop0r','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[2000,3000],'yVector':[0,110],'zVector':[0,100]}],'fractionToTarget':0.22,'synapseList':synapseList2_pop0_exp4,'colocalizeSynapses':False})


    ####### background
    synapseList3_pop0_exp4=[]
    synapseList3_pop0_exp4.append({'synapseType':"MF",'synapseMode':"persistent",'averageRate':2,\
                       'numberModel':"constant number of inputs per cell",'noInputs':20,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})
    

    synapseList3_pop0_exp4.append({'synapseType':"PF",'synapseMode':"persistent",'averageRate':0.5,\
                       'numberModel':"constant number of inputs per cell",'noInputs':100,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})



    inputGroups_pop0_exp4.append({'inputModel':'XF','inputLabel':'XFpop0b','targetingRegime':"uniform",'fractionToTarget':1,\
                                  'synapseList':synapseList3_pop0_exp4,'colocalizeSynapses':False})
    
                             
    net_params_V2010_multiple['experiment4']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp4})
    

    #exp5
    net_params_V2010_multiple['experiment5']['popParams']=[]
    net_params_V2010_multiple['experiment5']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_10comp_13channels_2CaPools",\
'size':0,"NeuroML2CellType":"cell2CaPools"})
   

    net_params_V2010_multiple['experiment5']['distributionParams']={}
    net_params_V2010_multiple['experiment5']['distributionParams']['populationList']=[]
    net_params_V2010_multiple['experiment5']['distributionParams']['populationList'].append({'distributionModel':"density_profile",'popID':'Golgi_pop0','densityFilePath':'/home/rokas/Golgi_data/Pure NeuG density matrix of shape 69 630.txt',\
    'planeDimensions':{'dim1':'x','dim2':'y'},'dim1CoordinateVector':[0,3000],'dim2CoordinateVector':[0,110],'dim3':'z','dim3Boundary':100,\
    'distanceModel':'random','canonicalVolumeBaseAreainMicrons':5.00318495*5.00318495 })
    

    net_params_V2010_multiple['experiment5']['connParams']={}
    net_params_V2010_multiple['experiment5']['connParams']['populationPairs']=[]
    net_params_V2010_multiple['experiment5']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
    'postPopID':'Golgi_pop0','spatialScale':1.0,'testingConductanceScale':1,'units':'nS','normalizeConductances':False,\
        'prePoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5 }},\
        'postPoptargetGroup':{'segmentGroupList':["apical_dendrite_group","basal_dendrite_group"],\
        'segmentGroupProbabilities':{"apical_dendrite_group":0.5,"basal_dendrite_group":0.5}}})

    
    
    net_params_V2010_multiple['experiment5']['inputParams']=[]
    ####### left band
    inputGroups_pop0_exp5=[]
    inputGroups_pop0_exp5.append({'inputModel':"variable_basal_firing_rate",'inputLabel':'vrpop0','amplitudeDistribution':"gaussian",'averageAmp':0,\
    'stDevAmp':32,'ampUnits':"pA",'offsetDistribution':"constant",'valueOffset':0,'offsetUnits':"ms"})
    synapseList0_pop0_exp5=[]
    synapseList0_pop0_exp5.append({'synapseType':"MF",'synapseMode':"transient",'averageRate':200,'delay':825,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList0_pop0_exp5.append({'synapseType':"PF",'synapseMode':"transient",'averageRate':350,'delay':835,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    
    inputGroups_pop0_exp5.append({'inputModel':'XF','inputLabel':'XFpop0l','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[0,1000],'yVector':[0,110],'zVector':[0,100]}],'fractionToTarget':0.22,'synapseList':synapseList0_pop0_exp5,'colocalizeSynapses':False})

    ##### middle band
    synapseList1_pop0_exp5=[]
    synapseList1_pop0_exp5.append({'synapseType':"MF",'synapseMode':"transient",'averageRate':200,'delay':600,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList1_pop0_exp5.append({'synapseType':"PF",'synapseMode':"transient",'averageRate':350,'delay':610,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    
    inputGroups_pop0_exp5.append({'inputModel':'XF','inputLabel':'XFpop0m','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[1000,2000],'yVector':[0,110],'zVector':[0,100]}],'fractionToTarget':0.22,'synapseList':synapseList1_pop0_exp5,'colocalizeSynapses':False})

    ###### right band
    synapseList2_pop0_exp5=[]
    synapseList2_pop0_exp5.append({'synapseType':"MF",'synapseMode':"transient",'averageRate':200,'delay':1050,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})

    synapseList2_pop0_exp5.append({'synapseType':"PF",'synapseMode':"transient",'averageRate':350,'delay':1060,'duration':15,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})

    
    inputGroups_pop0_exp5.append({'inputModel':'XF','inputLabel':'XFpop0r','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[2000,3000],'yVector':[0,110],'zVector':[0,100]}],'fractionToTarget':0.22,'synapseList':synapseList2_pop0_exp5,'colocalizeSynapses':False})


    ####### background
    synapseList3_pop0_exp5=[]
    synapseList3_pop0_exp5.append({'synapseType':"MF",'synapseMode':"persistent",'averageRate':2,\
                       'numberModel':"constant number of inputs per cell",'noInputs':20,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basal_dendrite_group"],'segmentGroupProbabilities':{"basal_dendrite_group":1}})
    

    synapseList3_pop0_exp5.append({'synapseType':"PF",'synapseMode':"persistent",'averageRate':0.5,\
                       'numberModel':"constant number of inputs per cell",'noInputs':100,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical_dendrite_group"],'segmentGroupProbabilities':{"apical_dendrite_group":1}})



    inputGroups_pop0_exp5.append({'inputModel':'XF','inputLabel':'XFpop0b','targetingRegime':"uniform",'fractionToTarget':1,\
                                  'synapseList':synapseList3_pop0_exp5,'colocalizeSynapses':False})
    
                             
    net_params_V2010_multiple['experiment5']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp5})
    
    #######
    
    
    sim_params={'simulator':"no simulation",'duration':3000,'timeStep':0.0005,'numTrials':4,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,\
    'saveSomataPositions':True,'parentDirRequired':True,'parentDir':parentdir,'currentDirRequired':True,'currentDir':currentdir,'networkDir':'experiment',\
        'saveInputReceivingCellID':True}
    
    
    
    
    run_simulations(net_params_V2010_multiple,sim_params)

   

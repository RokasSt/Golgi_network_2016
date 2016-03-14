import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from PythonUtils.Simulate_Golgi_Network_v2 import *



if __name__ == "__main__":
   
    net_params_test_2012_multiple={}
    net_params_test_2012_multiple['experiment1']={}
    net_params_test_2012_multiple['experiment2']={}
    
    net_params_test_2012_multiple['experiment1']['experimentID']="V2012_test_1"
    net_params_test_2012_multiple['experiment2']['experimentID']="V2012_test_2"
    #exp1
    net_params_test_2012_multiple['experiment1']['popParams']=[]
    net_params_test_2012_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop0','cellType':"Very_Simple_Golgi_test_morph",'size':15})
    net_params_test_2012_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop1','cellType':"Very_Simple_Golgi_test_morph",'size':15})

    net_params_test_2012_multiple['experiment1']['distributionParams']={}
    net_params_test_2012_multiple['experiment1']['distributionParams']['populationList']=[]
    net_params_test_2012_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Golgi_pop0','distributionModel':'explicit_cell_numbers','distanceModel':'random_minimal_distance',\
            'minimal_distance':25,'xDim':100,'yDim':100,'zDim':100})
    net_params_test_2012_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Golgi_pop1','distributionModel':'explicit_cell_numbers','distanceModel':'random_minimal_distance',\
            'minimal_distance':25,'xDim':100,'yDim':100,'zDim':100})

    net_params_test_2012_multiple['experiment1']['connParams']={}
    net_params_test_2012_multiple['experiment1']['connParams']['populationPairs']=[]
    net_params_test_2012_multiple['experiment1']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2012_based",'prePopID':'Golgi_pop0',\
                                                    'postPopID':'Golgi_pop1','conductanceModel':"constant",\
                                                    'conductanceValue':426,'units':"pS",\
                                                     'gapJunctionModel':"constant number of GJ contacts per pair",'numberGJ':8,\
                                                     'spatialScale':1,'testingConductanceScale':4,'maximalConnDistance':150,\
                            'targetingModelprePop':{'model':"segment groups and segments",'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]},\
                            'targetingModelpostPop':{'model':"segment groups and segments",\
                                                'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]}})
    

    

    
    net_params_test_2012_multiple['experiment1']['inputParams']=[]
    inputGroups_pop0_exp1=[]
    inputGroups_pop0_exp1.append({'inputModel':"variable_basal_firing_rate",'inputLabel':'vbpop0','amplitudeDistribution':"gaussian",'averageAmp':100,'stDevAmp':20,'ampUnits':"nA",\
                             'offsetDistribution':"constant",'valueOffset':50,'offsetUnits':"ms"})
    synapseList_pop0_exp1=[]
    synapseList_pop0_exp1.append({'synapseType':"PFSpikeSyn",'synapseMode':"persistent",'averageRate':50})
                            
    synapseList_pop0_exp1.append({'synapseType':"PFSpikeSyn",'synapseMode':"persistent",'averageRate':100})
    
    targeting_params0_pop0={'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
    'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]}
    
    inputGroups_pop0_exp1.append({'inputModel':'XF','inputLabel':'MFpop0','targetingRegime':"uniform",'fractionToTarget':0.5,\
                                  'synapseList':synapseList_pop0_exp1,'colocalizeSynapses':True,'sharedTargetingParameters':targeting_params0_pop0})

    inputGroups_pop1_exp1=[]
    inputGroups_pop1_exp1.append({'inputModel':"variable_basal_firing_rate",'inputLabel':'vbpop1','amplitudeDistribution':"gaussian",'averageAmp':100,'stDevAmp':20,'ampUnits':"nA",\
                             'offsetDistribution':"constant",'valueOffset':50,'offsetUnits':"ms"})
    synapseList_pop1_exp1=[]
    synapseList_pop1_exp1.append({'synapseType':"PFSpikeSyn",'synapseMode':"transient",'averageRate':50,'delay':80,'duration':100,'units':'ms')
                            
    synapseList_pop1_exp1.append({'synapseType':"PFSpikeSyn",'synapseMode':"persistent",'averageRate':100})

    targeting_params0_pop1={'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segments and subsegments",\
                             'segmentList':["Soma","dend_3"],'segmentProbabilities':[0.7,0.3],'fractionAlongANDsubsegProbabilities':[[[0.5,1],[0.5,0]],[[0.5,0.7],[0.5,0.3]]]}

    inputGroups_pop1_exp1.append({'inputModel':'XF','inputLabel':'MFpop1','targetingRegime':"uniform",'fractionToTarget':0.5,\
                                  'synapseList':synapseList_pop1_exp1,'colocalizeSynapses':True,'sharedTargetingParameters':targeting_params0_pop1})
    
                             
    net_params_test_2012_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp1})
    net_params_test_2012_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop1','inputGroups':inputGroups_pop1_exp1})

    ### exp 2
    net_params_test_2012_multiple['experiment2']['popParams']=[]
    net_params_test_2012_multiple['experiment2']['popParams'].append({'popID':'Golgi_pop0','cellType':"Very_Simple_Golgi_test_morph",'size':15})
    net_params_test_2012_multiple['experiment2']['popParams'].append({'popID':'Golgi_pop1','cellType':"Very_Simple_Golgi_test_morph",'size':15})
    
    net_params_test_2012_multiple['experiment2']['distributionParams']={}
    net_params_test_2012_multiple['experiment2']['distributionParams']['populationList']=[]
    net_params_test_2012_multiple['experiment2']['distributionParams']['populationList'].append({'popID':'Golgi_pop0','distributionModel':'explicit_cell_numbers','distanceModel':'random_minimal_distance',\
                                                                     'minimal_distance':25,'xDim':100,'yDim':100,'zDim':100})
    net_params_test_2012_multiple['experiment2']['distributionParams']['populationList'].append({'popID':'Golgi_pop1','distributionModel':'explicit_cell_numbers','distanceModel':'random_minimal_distance',\
                                                                    'minimal_distance':25,'xDim':100,'yDim':100,'zDim':100})
    
    net_params_test_2012_multiple['experiment2']['connParams']={}
    net_params_test_2012_multiple['experiment2']['connParams']['populationPairs']=[]
    net_params_test_2012_multiple['experiment2']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2012_based",'prePopID':'Golgi_pop0',\
                                                    'postPopID':'Golgi_pop1','conductanceModel':"constant",\
                                                    'conductanceValue':426,'units':"pS",\
                                                     'gapJunctionModel':"constant number of GJ contacts per pair",'numberGJ':8,\
                                                     'spatialScale':1,'testingConductanceScale':4,'maximalConnDistance':150,\
                            'targetingModelprePop':{'model':"segment groups and segments",'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]},\
                            'targetingModelpostPop':{'model':"segment groups and segments",\
                                                'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]}})
    
    
    net_params_test_2012_multiple['experiment2']['inputParams']=[]
    inputGroups_pop0_exp2=[]
    inputGroups_pop0_exp2.append({'inputModel':"variable_basal_firing_rate",'inputLabel':'vbpop0','amplitudeDistribution':"constant",'valueAmp':100,'ampUnits':"nA",\
                             'offsetDistribution':"constant",'valueOffset':50,'offsetUnits':"ms"})
    synapseList_pop0_exp2=[]
    synapseList_pop0_exp2.append({'synapseType':"PFSpikeSyn",'synapseMode':"persistent",'averageRate':50})
                            
    synapseList_pop0_exp2.append({'synapseType':"PFSpikeSyn",'synapseMode':"persistent",'averageRate':100})

    targeting_params1_pop0={'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                            'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]}

    inputGroups_pop0_exp2.append({'inputModel':'XF','inputLabel':'MFpop0','targetingRegime':"uniform",'fractionToTarget':0.5,\
                                  'synapseList':synapseList_pop0_exp2,'colocalizeSynapses':True,'sharedTargetingParameters':targeting_params1_pop0})

    inputGroups_pop1_exp2=[]
    inputGroups_pop1_exp2.append({'inputModel':"variable_basal_firing_rate",'inputLabel':'vbpop1','amplitudeDistribution':"constant",'valueAmp':100,'ampUnits':"nA",\
                             'offsetDistribution':"constant",'valueOffset':50,'offsetUnits':"ms"})
    synapseList_pop1_exp2=[]
    synapseList_pop1_exp2.append({'synapseType':"PFSpikeSyn",'synapseMode':"transient",'averageRate':50,'delay':80,'duration':100,'units':'ms'})
                            
    synapseList_pop1_exp2.append({'synapseType':"PFSpikeSyn",'synapseMode':"persistent",'averageRate':100})

    targeting_params1_pop1={'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segments and subsegments",\
                             'segmentList':["Soma","dend_3"],'segmentProbabilities':[0.7,0.3],'fractionAlongANDsubsegProbabilities':[[[0.5,1],[0.5,1]],[[0.5,0.7],[0.5,0.3]]]}

    inputGroups_pop1_exp2.append({'inputModel':'XF','inputLabel':'MFpop1','targetingRegime':"uniform",'fractionToTarget':0.5,\
                                  'synapseList':synapseList_pop1_exp2,'colocalizeSynapses':True,'sharedTargetingParameters':targeting_params1_pop1})
     


    ####### format for 3D region specific targeting:
    #inputGroups_pop1_exp2.append({'inputModel':'XF','inputLabel':'MFpop1','targetingRegime':"uniform",'fractionToTarget':0.5,'synapseList':synapseList_pop1_exp2}) 
    #inputGroups_pop1_exp2.append({'inputModel':'XF','inputLabel':'MFpop1','targetingRegime':"3D region specific",\
    #       'regionList':[ {'xVector':[0,100],'yVector':[0,100],'zVector':[0,100]} ],'fractionToTarget':0.5,'synapseList':synapseList_pop1_exp2}) 
    # 
    #
                             
    net_params_test_2012_multiple['experiment2']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp2})
    net_params_test_2012_multiple['experiment2']['inputParams'].append({'popName':'Golgi_pop1','inputGroups':inputGroups_pop1_exp2})

    
    ####### change 'simulator' to "jNeuroML_NEURON" in order to run simulations in NEURON

    sim_params={'simulator':"no simulation",'duration':450,'timeStep':0.005,'numTrials':5,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,\
    'saveSomataPositions':True,'parentDirRequired':True,'parentDir':parentdir,'currentDirRequired':True,'currentDir':currentdir,'networkDir':'example'}
    
    ##### run all simulations
    run_simulations(net_params_test_2010_multiple,sim_params)

   
   

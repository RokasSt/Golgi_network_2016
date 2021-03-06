from Simulate_Golgi_Network_v2 import *


if __name__ == "__main__":


    net_params_test_2010_multiple={}
    net_params_test_2010_multiple['experiment1']={}
    net_params_test_2010_multiple['experiment2']={}
    
    net_params_test_2010_multiple['experiment1']['experimentID']="test_v2_exp1"
    net_params_test_2010_multiple['experiment2']['experimentID']="test_v2_exp2"
    #exp1
    net_params_test_2010_multiple['experiment1']['popParams']=[]
    net_params_test_2010_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop0','cellType':"Very_Simple_Golgi_test_morph",'size':10})
    net_params_test_2010_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop1','cellType':"Very_Simple_Golgi_test_morph",'size':10})

    net_params_test_2010_multiple['experiment1']['distributionParams']={}
    net_params_test_2010_multiple['experiment1']['distributionParams']['distributionModel']="random_no_overlap"
    net_params_test_2010_multiple['experiment1']['distributionParams']['xDim']=100
    net_params_test_2010_multiple['experiment1']['distributionParams']['yDim']=100
    net_params_test_2010_multiple['experiment1']['distributionParams']['zDim']=100

    ##### below lines to make a reference template for the density based model:
    #   net_params_test_2010_multiple['experiment1']['distributionParams']={}
    #   net_params_test_2010_multiple['experiment1']['distributionParams']['distributionModel']="density based"
    #   net_params_test_2010_multiple['experiment1']['distributionParams']['populationList']=[]
    #   net_params_test_2010_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Golgi_pop0','densityFilePath':'/home/rokas/Golgi_data/GlyT2 density matrix of shape 35 152.txt',\
    #   'planeDimensions':{'dim1':'x','dim2':'z'},'dim1CoordinateVector':[1300,1500],'dim2CoordinateVector':[0,50]})
    #   net_params_test_2010_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Golgi_pop1','densityFilePath':'/home/rokas/Golgi_data/GlyT2 density matrix of shape 35 152.txt',\
    #   'planeDimensions':{'dim1':'x','dim2':'z'},'dim1CoordinateVector':[1300,1500],'dim2CoordinateVector':[0,50],'dim3':'y','dim3CoordinateVector':[0,200],\
    #   'distanceModel':'minimal_distance','minimalDistance':25})
    

    ##### no need to have explicit subcellular targeting in the case of soma-to-soma distance dependent conductance mode ("Vervaeke_2010_based")
    net_params_test_2010_multiple['experiment1']['connParams']={}
    net_params_test_2010_multiple['experiment1']['connParams']['populationPairs']=[]
    net_params_test_2010_multiple['experiment1']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
                                                    'postPopID':'Golgi_pop1','spatialScale':1,'testingConductanceScale':1,'units':'nS','maximalConnDistance':200,'normalizeConductances':False,\
                            'prePoptargetGroup':{'segmentGroupList':["dendrite_group"],'segmentGroupProbabilities':[1]},\
                            'postPoptargetGroup':{'segmentGroupList':["dendrite_group"],'segmentGroupProbabilities':[1]}})


    net_params_test_2010_multiple['experiment1']['inputParams']=[]

    inputGroups_pop0_2010exp1=[]
    inputGroups_pop0_2010exp1.append({'inputModel':"testing",'testingModel':"pulseGenerators",'cellFractionToTarget':0.5,\
                                      'pulseParameters':[{'delay':20,'duration':200,'amplitude':4E-5},{'delay':220,'duration':200,'amplitude':-0.5E-5}],\
                         'ampUnits':"uA",'timeUnits':'ms'})

    inputGroups_pop1_2010exp1=[]
    inputGroups_pop1_2010exp1.append({'inputModel':"testing",'testingModel':"pulseGenerators",'cellFractionToTarget':0.5,\
                            'pulseParameters':[{'delay':0,'duration':100,'amplitude':4E-5},{'delay':220,'duration':200,'amplitude':-0.5E-5}],\
                         'ampUnits':"uA",'timeUnits':'ms'})




    net_params_test_2010_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_2010exp1})
    net_params_test_2010_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop1','inputGroups':inputGroups_pop1_2010exp1})



    #exp2
    net_params_test_2010_multiple['experiment2']['popParams']=[]
    net_params_test_2010_multiple['experiment2']['popParams'].append({'popID':'Golgi_pop0','cellType':"Very_Simple_Golgi_test_morph",'size':10})
    net_params_test_2010_multiple['experiment2']['popParams'].append({'popID':'Golgi_pop1','cellType':"Very_Simple_Golgi_test_morph",'size':10})

    net_params_test_2010_multiple['experiment2']['distributionParams']={}
    net_params_test_2010_multiple['experiment2']['distributionParams']['distributionModel']="random_no_overlap"
    net_params_test_2010_multiple['experiment2']['distributionParams']['xDim']=100
    net_params_test_2010_multiple['experiment2']['distributionParams']['yDim']=100
    net_params_test_2010_multiple['experiment2']['distributionParams']['zDim']=100

    ##### as conductance levels are soma-to-soma distance-dependent in a Vervaeke_2010_based model, subcellular targeting is not implemented in this configuration. If   one wants to specify multiple GJs per cell pair with constant or heterogeneous conductances one can use Vervaeke_2012_based connModel
    net_params_test_2010_multiple['experiment2']['connParams']={}
    net_params_test_2010_multiple['experiment2']['connParams']['populationPairs']=[]
    net_params_test_2010_multiple['experiment2']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
                                                    'postPopID':'Golgi_pop1','spatialScale':20,'testingConductanceScale':1,'maximalConnDistance':200,'units':'nS','normalizeConductances':True,\
                            'prePoptargetGroup':{'segmentGroupList':["dendrite_group"],'segmentGroupProbabilities':[1]},\
                            'postPoptargetGroup':{'segmentGroupList':["dendrite_group"],'segmentGroupProbabilities':[1]}})

    net_params_test_2010_multiple['experiment2']['inputParams']=[]
    inputGroups_pop0_2010exp2=[]
    inputGroups_pop0_2010exp2.append({'inputModel':"testing",'testingModel':"pulseGenerators",'cellFractionToTarget':0.5,\
                    'pulseParameters':[{'delay':20,'duration':200,'amplitude':4E-5},{'delay':220,'duration':200,'amplitude':-0.5E-5}],\
                         'ampUnits':"uA",'timeUnits':'ms'})

    inputGroups_pop1_2010exp2=[]
    inputGroups_pop1_2010exp2.append({'inputModel':"testing",'testingModel':"pulseGenerators",'cellFractionToTarget':0.5,\
                        'pulseParameters':[{'delay':0,'duration':100,'amplitude':4E-5},{'delay':220,'duration':200,'amplitude':-0.5E-5}],\
                         'ampUnits':"uA",'timeUnits':'ms'})




    net_params_test_2010_multiple['experiment2']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_2010exp2})
    net_params_test_2010_multiple['experiment2']['inputParams'].append({'popName':'Golgi_pop1','inputGroups':inputGroups_pop1_2010exp2})

    ####### change 'simulator' to "jNeuroML_NEURON" in order to run simulations in NEURON

    sim_params={'simulator':"no simulation",'duration':450,'timeStep':0.005,'numTrials':5,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,'saveSomataPositions':True}
    
    ##### run all simulations
    run_simulations(net_params_test_2010_multiple,sim_params)

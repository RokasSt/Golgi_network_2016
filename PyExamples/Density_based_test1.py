
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from PythonUtils.Simulate_Golgi_Network_v2 import *


if __name__ == "__main__":


    net_params_test_2010_multiple={}
    net_params_test_2010_multiple['experiment1']={}
   
    
    net_params_test_2010_multiple['experiment1']['experimentID']="test_v2_exp1"
    
    #exp1
    net_params_test_2010_multiple['experiment1']['popParams']=[]
    net_params_test_2010_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_5comp_3channels_1CaPool",'size':10})
    net_params_test_2010_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop1','cellType':"Golgi_5comp_3channels_1CaPool",'size':10})

    net_params_test_2010_multiple['experiment1']['distributionParams']={}
    net_params_test_2010_multiple['experiment1']['distributionParams']['populationList']=[]
    net_params_test_2010_multiple['experiment1']['distributionParams']['populationList'].append({'distributionModel':"density_profile",'popID':'Golgi_pop0','densityFilePath':'/home/rokas/Golgi_data/GlyT2 density matrix of shape 35 152.txt',\
    'planeDimensions':{'dim1':'x','dim2':'z'},'dim1CoordinateVector':[1300,1500],'dim2CoordinateVector':[0,50],'dim3':'y','dim3CoordinateVector':[0,200],\
    'distanceModel':'random','canonicalVolumeBaseArea':54})
    net_params_test_2010_multiple['experiment1']['distributionParams']['populationList'].append({'distributionModel':"density_profile",'popID':'Golgi_pop1','densityFilePath':'/home/rokas/Golgi_data/GlyT2 density matrix of shape 35 152.txt',\
    'planeDimensions':{'dim1':'x','dim2':'z'},'dim1CoordinateVector':[1300,1500],'dim2CoordinateVector':[0,50],'dim3':'y','dim3CoordinateVector':[0,200],\
    'distanceModel':'random','canonicalVolumeBaseArea':54})
    #### note on 'distanceModel': other options for 'distanceModel' include : 'random_no_overlap', 'random_minimal_distance'
    
    ##### no need to have explicit subcellular targeting in the case of soma-to-soma distance dependent conductance mode ("Vervaeke_2010_based")
    net_params_test_2010_multiple['experiment1']['connParams']={}
    net_params_test_2010_multiple['experiment1']['connParams']['populationPairs']=[]
    net_params_test_2010_multiple['experiment1']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
                                                    'postPopID':'Golgi_pop1','spatialScale':1,'testingConductanceScale':1,'units':'nS','maximalConnDistance':200,'normalizeConductances':True,\
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



    
    ####### change 'simulator' to "jNeuroML_NEURON" in order to run simulations in NEURON

    sim_params={'simulator':"no simulation",'duration':450,'timeStep':0.005,'numTrials':1,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,\
    'saveSomataPositions':True,'parentDirRequired':True,'parentDir':parentdir,'currentDirRequired':True,'currentDir':currentdir,'networkDir':'example'}
    
    ##### run all simulations
    run_simulations(net_params_test_2010_multiple,sim_params)

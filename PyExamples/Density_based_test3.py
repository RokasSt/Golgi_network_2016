
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from PythonUtils.Simulate_Golgi_Network_v2 import *


if __name__ == "__main__":


    net_params_test_2010_multiple={}
    net_params_test_2010_multiple['experiment1']={}
   
    
    net_params_test_2010_multiple['experiment1']['experimentID']="test_density_3"
    
    #exp1
    net_params_test_2010_multiple['experiment1']['popParams']=[]
    net_params_test_2010_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_040408_C1",'size':0,"NeuroML2CellType":"cell2CaPools"})
    

    net_params_test_2010_multiple['experiment1']['distributionParams']={}
    net_params_test_2010_multiple['experiment1']['distributionParams']['populationList']=[]
    net_params_test_2010_multiple['experiment1']['distributionParams']['populationList'].append({'distributionModel':"density_profile",'popID':'Golgi_pop0','densityFilePath':'/home/rokas/Golgi_data/Pure NeuG density matrix of shape 69 630.txt',\
    'planeDimensions':{'dim1':'x','dim2':'y'},'dim1CoordinateVector':[1900,2000],'dim2CoordinateVector':[0,100],'dim3':'z','dim3Boundary':400,\
    'distanceModel':'random_no_overlap','canonicalVolumeBaseAreainMicrons':400})
    
    #### note on 'distanceModel': other options for 'distanceModel' include : 'random_no_overlap', 'random_minimal_distance'
    
    ##### no need to have explicit subcellular targeting in the case of soma-to-soma distance dependent conductance mode ("Vervaeke_2010_based")
    net_params_test_2010_multiple['experiment1']['connParams']={}
    net_params_test_2010_multiple['experiment1']['connParams']['populationPairs']=[]
    net_params_test_2010_multiple['experiment1']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
                                                   'postPopID':'Golgi_pop0','spatialScale':1,'testingConductanceScale':1,'units':'nS','normalizeConductances':False,\
                            'prePoptargetGroup':{'segmentGroupList':["dendrite_group"],'segmentGroupProbabilities':{"dendrite_group":1}},\
                            'postPoptargetGroup':{'segmentGroupList':["dendrite_group"],'segmentGroupProbabilities':{"dendrite_group":1}}})


    net_params_test_2010_multiple['experiment1']['inputParams']=[]

    inputGroups_pop0_2010exp1=[]
    #### note that a series of pulses can be specified for each population: 'pulseParameters' points to a list than can contain multiple dictionaries
    inputGroups_pop0_2010exp1.append({'inputModel':"testing",'inputLabel':'PulsePop0','testingModel':"pulseGenerators",'cellFractionToTarget':0.5,\
                                      'pulseParameters':[{'delay':20,'duration':200,'amplitude':4E-5}],\
                         'ampUnits':"uA",'timeUnits':'ms'})

    net_params_test_2010_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_2010exp1})


    ####### change 'simulator' to "jNeuroML_NEURON" in order to run simulations in NEURON

    sim_params={'simulator':"no simulation",'duration':450,'timeStep':0.005,'numTrials':1,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,\
    'saveSomataPositions':True,'parentDirRequired':True,'parentDir':parentdir,'currentDirRequired':True,'currentDir':currentdir,'networkDir':'example',\
    'saveInputReceivingCellID':True}
    
    ##### run all simulations
    run_simulations(net_params_test_2010_multiple,sim_params)

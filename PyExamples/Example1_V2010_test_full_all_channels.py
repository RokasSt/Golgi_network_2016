
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from PythonUtils.Simulate_Golgi_Network_v2 import *


if __name__ == "__main__":


    net_params_test_2010_multiple={}
    net_params_test_2010_multiple['experiment1']={}
    
    
    net_params_test_2010_multiple['experiment1']['experimentID']="test_full_morph_all_channels_exp1"
    
    #exp1
    net_params_test_2010_multiple['experiment1']['popParams']=[]
    # by default "cell" componentType is used if "NeuroML2CellType" is not in the popParams array
    net_params_test_2010_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_040408_C1",'size':2,"NeuroML2CellType":"cell2CaPools"})
    
   
    net_params_test_2010_multiple['experiment1']['distributionParams']={}
    net_params_test_2010_multiple['experiment1']['distributionParams']['populationList']=[]
    net_params_test_2010_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Golgi_pop0','distributionModel':'explicit_cell_numbers','distanceModel':'random_no_overlap','xDim':40,'yDim':40,'zDim':40})
    

   
    net_params_test_2010_multiple['experiment1']['connParams']={}
    net_params_test_2010_multiple['experiment1']['connParams']['populationPairs']=[]
    net_params_test_2010_multiple['experiment1']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
                                                    'postPopID':'Golgi_pop0','spatialScale':1,'testingConductanceScale':2,'units':'nS','maximalConnDistance':200,'normalizeConductances':False,\
                            'prePoptargetGroup':{'segmentGroupList':["apical"],'segmentGroupProbabilities':[1]},\
                            'postPoptargetGroup':{'segmentGroupList':["apical"],'segmentGroupProbabilities':[1]}})


    net_params_test_2010_multiple['experiment1']['inputParams']=[]

    inputGroups_pop0_2010exp1=[]
    inputGroups_pop0_2010exp1.append({'inputModel':"testing",'testingModel':"pulseGenerators",'cellFractionToTarget':0.5,\
                                      'pulseParameters':[{'delay':20,'duration':200,'amplitude':50E-5},{'delay':220,'duration':200,'amplitude':-50E-5}],\
                         'ampUnits':"uA",'timeUnits':'ms'})

   




    net_params_test_2010_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_2010exp1})
    



    

   ####### change 'simulator' to "jNeuroML_NEURON" in order to run simulations in NEURON

    sim_params={'simulator':"no simulation",'duration':450,'timeStep':0.0005,'numTrials':1,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,\
    'saveSomataPositions':True,'parentDirRequired':True,'parentDir':parentdir,'currentDirRequired':True,'currentDir':currentdir,'networkDir':'example'}
    
    ##### run all simulations
    run_simulations(net_params_test_2010_multiple,sim_params)

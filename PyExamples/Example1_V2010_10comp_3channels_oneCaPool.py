
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from PythonUtils.Simulate_Golgi_Network_v2 import *

##################   Golgi_V2012_test2.py is used for testing and debugging
if __name__ == "__main__":


    net_params_test_2010_multiple={}
    net_params_test_2010_multiple['experiment1']={}

    
    net_params_test_2010_multiple['experiment1']['experimentID']="test_10comp_3channels_exp1"
    
    #exp1
    net_params_test_2010_multiple['experiment1']['popParams']=[]
    net_params_test_2010_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_10comp_3channels_1CaPool",'size':2})
   

    net_params_test_2010_multiple['experiment1']['distributionParams']={}
    net_params_test_2010_multiple['experiment1']['distributionParams']['populationList']=[]
    net_params_test_2010_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Golgi_pop0','distributionModel':'explicit_cell_numbers','distanceModel':'random_no_overlap','xDim':50,'yDim':50,'zDim':50})
    
    

   
    net_params_test_2010_multiple['experiment1']['connParams']={}
    net_params_test_2010_multiple['experiment1']['connParams']['populationPairs']=[]
    net_params_test_2010_multiple['experiment1']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
                                                    'postPopID':'Golgi_pop0','spatialScale':1,'testingConductanceScale':1,'units':'nS','maximalConnDistance':200,'normalizeConductances':False,\
                            'prePoptargetGroup':{'segmentGroupList':["dendrite_group"],'segmentGroupProbabilities':[1]},\
                            'postPoptargetGroup':{'segmentGroupList':["dendrite_group"],'segmentGroupProbabilities':[1]}})


    net_params_test_2010_multiple['experiment1']['inputParams']=[]

    inputGroups_pop0_2010exp1=[]
    #### note that a series of pulses can be specified for each population: 'pulseParameters' points to a list than can contain multiple dictionaries
    inputGroups_pop0_2010exp1.append({'inputModel':"testing",'testingModel':"pulseGenerators",'cellFractionToTarget':0.5,\
                                      'pulseParameters':[{'delay':20,'duration':200,'amplitude':4E-5}],\
                         'ampUnits':"uA",'timeUnits':'ms'})




    net_params_test_2010_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_2010exp1})
    



   

    ####### change 'simulator' to "jNeuroML_NEURON" in order to run simulations in NEURON

    sim_params={'simulator':"no simulation",'duration':450,'timeStep':0.005,'numTrials':1,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,\
    'saveSomataPositions':True,'parentDirRequired':True,'parentDir':parentdir,'currentDirRequired':True,'currentDir':currentdir,'networkDir':'example'}
    
    ##### run all simulations
    run_simulations(net_params_test_2010_multiple,sim_params)

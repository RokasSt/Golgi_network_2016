
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from PythonUtils.Simulate_Golgi_Network_v2 import *


if __name__ == "__main__":


    net_params_test_2010_multiple={}
    net_params_test_2010_multiple['experiment1']={}
    #net_params_test_2010_multiple['experiment2']={}
    
    net_params_test_2010_multiple['experiment1']['experimentID']="test_V2010_exp1_10cells"
    #net_params_test_2010_multiple['experiment2']['experimentID']="test_V2010_exp2"
    #exp1 note that the number of cells can easily be given based on the uniform density (previous studies around 4607 cells/ per mm3) and x,y,z dimensions in micro m.
    net_params_test_2010_multiple['experiment1']['popParams']=[]
    net_params_test_2010_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_5comp_3channels_1CaPool",'size':10})
   

    net_params_test_2010_multiple['experiment1']['distributionParams']={}
    net_params_test_2010_multiple['experiment1']['distributionParams']['populationList']=[]
    net_params_test_2010_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Golgi_pop0','distributionModel':'explicit_cell_numbers','distanceModel':'random_minimal_distance','minimal_distance':30,'xDim':80,'yDim':80,'zDim':80})
   
    

   
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
    



    #exp2
    #net_params_test_2010_multiple['experiment2']['popParams']=[]
    #net_params_test_2010_multiple['experiment2']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_5comp_3channels_1CaPool",'size':180})
   

    #net_params_test_2010_multiple['experiment2']['distributionParams']={}
    #net_params_test_2010_multiple['experiment2']['distributionParams']['populationList']=[]
    #net_params_test_2010_multiple['experiment2']['distributionParams']['populationList'].append({'popID':'Golgi_pop0','distributionModel':'explicit_cell_numbers','distanceModel':'random_no_overlap','xDim':700,'yDim':700,'zDim':80})
   

    ##### as conductance levels are soma-to-soma distance-dependent in a Vervaeke_2010_based model, subcellular targeting is not implemented in this configuration. If   one wants to specify multiple GJs per cell pair with constant or heterogeneous conductances one can use Vervaeke_2012_based connModel
    #net_params_test_2010_multiple['experiment2']['connParams']={}
    #net_params_test_2010_multiple['experiment2']['connParams']['populationPairs']=[]
    #net_params_test_2010_multiple['experiment2']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
                                               #     'postPopID':'Golgi_pop0','spatialScale':20,'testingConductanceScale':1,'units':'nS','normalizeConductances':True,\
                          #  'prePoptargetGroup':{'segmentGroupList':["dendrite_group"],'segmentGroupProbabilities':{"dendrite_group":1}},\
                           # 'postPoptargetGroup':{'segmentGroupList':["dendrite_group"],'segmentGroupProbabilities':{"dendrite_group":1}}})

    #net_params_test_2010_multiple['experiment2']['inputParams']=[]
    #inputGroups_pop0_2010exp2=[]
    #inputGroups_pop0_2010exp2.append({'inputModel':"testing",'inputLabel':'PulsePop0','testingModel':"pulseGenerators",'cellFractionToTarget':0.5,\
                  #  'pulseParameters':[{'delay':20,'duration':200,'amplitude':4E-5}],\
                      #   'ampUnits':"uA",'timeUnits':'ms'})

   

    #net_params_test_2010_multiple['experiment2']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_2010exp2})
   

    ####### change 'simulator' to "jNeuroML_NEURON" in order to run simulations in NEURON

    sim_params={'simulator':"jNeuroML_NEURON",'duration':3000,'timeStep':0.005,'numTrials':1,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,\
    'saveSomataPositions':True,'parentDirRequired':True,'parentDir':parentdir,'currentDirRequired':True,'currentDir':currentdir,'networkDir':'example',\
    'saveInputReceivingCellID':True}
    
    ##### run all simulations
    run_simulations(net_params_test_2010_multiple,sim_params)

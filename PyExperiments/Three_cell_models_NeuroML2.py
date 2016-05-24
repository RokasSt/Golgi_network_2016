
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from PythonUtils.Simulate_Golgi_Network_v2 import *


if __name__ == "__main__":


    net_params_multiple={}
    net_params_multiple['experiment1']={}
    
    
    net_params_multiple['experiment1']['experimentID']="three_cell_models_NeuroML2"
    
    #exp1
    net_params_multiple['experiment1']['popParams']=[]
    net_params_multiple['experiment1']['popParams'].append({'popID':'Full_model','cellType':"Golgi_040408_C1",'size':2,"NeuroML2CellType":"cell2CaPools"})

    #######net_params_multiple['experiment1']['popParams'].append({'popID':'Reduced',\
    #'cellType':"Golgi_10comp_13channels_2CaPools",'size':1,"NeuroML2CellType":"cell2CaPools"})
   # net_params_multiple['experiment1']['popParams'].append({'popID':'Solinas',\
   # 'cellType':"Golgi_5comp_all_channels_twoCaPools",'size':1,"NeuroML2CellType":"cell2CaPools"})

    net_params_multiple['experiment1']['distributionParams']={}
    net_params_multiple['experiment1']['distributionParams']['populationList']=[]
    
    net_params_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Full_model','distributionModel':'explicit_cell_numbers','distanceModel':'random_no_overlap','xDim':40,'yDim':40,'zDim':40})

    #net_params_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Reduced','distributionModel':'explicit_cell_numbers','distanceModel':'random_no_overlap','xDim':50,'yDim':50,'zDim':50})
    
   # net_params_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Solinas','distributionModel':'explicit_cell_numbers','distanceModel':'random_no_overlap','xDim':50,'yDim':50,'zDim':50})
   
    net_params_multiple['experiment1']['connParams']={}
    net_params_multiple['experiment1']['connParams']['populationPairs']=[]
    net_params_multiple['experiment1']['connParams']['populationPairs'].append({'electricalConnModel':"none",'prePopID':'Golgi_pop0',\
                             #                    'postPopID':'Golgi_pop0','spatialScale':1,'testingConductanceScale':1,'units':'nS','normalizeConductances':False,\
                      #   'prePoptargetGroup':{'segmentGroupList':["apical"],'segmentGroupProbabilities':[1]},\
                       #   'postPoptargetGroup':{'segmentGroupList':["apical"],'segmentGroupProbabilities':[1]}})


    net_params_multiple['experiment1']['inputParams']=[]

    inputGroups_pop0_2010exp1=[]
    inputGroups_pop0_2010exp1.append({'inputModel':"testing",'inputLabel':'pop0pulse','testingModel':"pulseGenerators",'cellFractionToTarget':1,\
                                      'pulseParameters':[{'delay':200,'duration':300,'amplitude':0},{'delay':800,'duration':300,'amplitude':0}],\
                         'ampUnits':"pA",'timeUnits':'ms'})


    net_params_multiple['experiment1']['inputParams'].append({'popName':'Full_model','inputGroups':inputGroups_pop0_2010exp1})

    
    #inputGroups_pop1_2010exp1=[]
    #inputGroups_pop1_2010exp1.append({'inputModel':"testing",'inputLabel':'pop0pulse','testingModel':"pulseGenerators",'cellFractionToTarget':1,\
                                   #   'pulseParameters':[{'delay':200,'duration':300,'amplitude':0},{'delay':800,'duration':300,'amplitude':0}],\
                        # 'ampUnits':"pA",'timeUnits':'ms'})


    #net_params_multiple['experiment1']['inputParams'].append({'popName':'Reduced','inputGroups':inputGroups_pop1_2010exp1})

    
    #inputGroups_pop2_2010exp1=[]
    #inputGroups_pop2_2010exp1.append({'inputModel':"testing",'inputLabel':'pop0pulse','testingModel':"pulseGenerators",'cellFractionToTarget':1,\
                                  #    'pulseParameters':[{'delay':200,'duration':300,'amplitude':0},{'delay':800,'duration':300,'amplitude':0}],\
                         #'ampUnits':"pA",'timeUnits':'ms'})


    #net_params_multiple['experiment1']['inputParams'].append({'popName':'Solinas','inputGroups':inputGroups_pop2_2010exp1})

    

   ####### change 'simulator' to "jNeuroML_NEURON" in order to run simulations in NEURON

    sim_params={'simulator':"no simulation",'duration':1500,'timeStep':0.0025,'numTrials':1,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,\
    'saveSomataPositions':True,'parentDirRequired':True,'parentDir':parentdir,'currentDirRequired':True,'currentDir':currentdir,'networkDir':'experiment', 'saveInputReceivingCellID':False}
    
    ##### run all simulations
    run_simulations(net_params_multiple,sim_params)

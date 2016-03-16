import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from PythonUtils.Simulate_Golgi_Network_v2 import *

################ similar to Golgi_V2012_test2.py but contains two populations. Golgi_V2012_test2.py is used for testing and debugging

if __name__ == "__main__":
   
    net_params_V2010_multiple={}
    net_params_V2010_multiple['experiment1']={}
    
    
    
    net_params_V2010_multiple['experiment1']['experimentID']="V2010_test_syn_with_no_import"
    
    
    
    
    #exp1 
    net_params_V2010_multiple['experiment1']['popParams']=[]
    net_params_V2010_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_040408_C1",\
'size':1,"NeuroML2CellType":"cell2CaPools"})
   

    net_params_V2010_multiple['experiment1']['distributionParams']={}
    net_params_V2010_multiple['experiment1']['distributionParams']['populationList']=[]
    net_params_V2010_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Golgi_pop0','distributionModel':'explicit_cell_numbers','distanceModel':'random','xDim':30,'yDim':30,'zDim':30})
    

    net_params_V2010_multiple['experiment1']['connParams']={}
    net_params_V2010_multiple['experiment1']['connParams']['populationPairs']=[]
    net_params_V2010_multiple['experiment1']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
    'postPopID':'Golgi_pop0','spatialScale':1.0,'testingConductanceScale':1,'units':'nS','normalizeConductances':False,\
        'prePoptargetGroup':{'segmentGroupList':["apical","basolateral"],\
        'segmentGroupProbabilities':{"apical":0.5,"basolateral":0.5 }},\
        'postPoptargetGroup':{'segmentGroupList':["apical","basolateral"],\
        'segmentGroupProbabilities':{"apical":0.5,"basolateral":0.5}}})

    
    
    net_params_V2010_multiple['experiment1']['inputParams']=[]
    ####### left band
    inputGroups_pop0_exp1=[]
    synapseList0_pop0_exp1=[]
    synapseList0_pop0_exp1.append({'synapseType':"MFSpikeSyn",'synapseMode':"transient",'averageRate':200,'delay':600,'duration':10,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basolateral"],'segmentGroupProbabilities':{"basolateral":1}})

    
    
    inputGroups_pop0_exp1.append({'inputModel':'XF','inputLabel':'XFpop0l','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[0,1000],'yVector':[0,110],'zVector':[0,100]}],'fractionToTarget':1,'synapseList':synapseList0_pop0_exp1,'colocalizeSynapses':False})

    net_params_V2010_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp1})  

    
    #######
    
    
    sim_params={'simulator':"no simulation",'duration':3500,'timeStep':0.0003,'numTrials':1,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,\
    'saveSomataPositions':True,'parentDirRequired':True,'parentDir':parentdir,'currentDirRequired':True,'currentDir':currentdir,'networkDir':'experiment',\
        'saveInputReceivingCellID':True}
    
    
   
    
    run_simulations(net_params_V2010_multiple,sim_params)

   

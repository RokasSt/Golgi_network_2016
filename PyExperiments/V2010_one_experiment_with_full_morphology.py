import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from PythonUtils.Simulate_Golgi_Network_v2 import *

################ similar to Golgi_V2012_test2.py but contains two populations. Golgi_V2012_test2.py is used for testing and debugging

if __name__ == "__main__":
   
    net_params_V2010_multiple={}
    net_params_V2010_multiple['experiment1']={}
   
    
    net_params_V2010_multiple['experiment1']['experimentID']="V2010_sp_scale_1_dens_full_morph"
    
    
    
    #exp1 if you are firstly generating input trains, initially set some reasonable boundary for the size of population; later,when the cells are distributed by the anatomical distribution, code will adjust the size to the true value.
    net_params_V2010_multiple['experiment1']['popParams']=[]
    net_params_V2010_multiple['experiment1']['popParams'].append({'popID':'Golgi_pop0','cellType':"Golgi_040408_C1T",\
'size':0,"NeuroML2CellType":"cell2CaPools"})
   

    net_params_V2010_multiple['experiment1']['distributionParams']={}
    net_params_V2010_multiple['experiment1']['distributionParams']['populationList']=[]
    net_params_V2010_multiple['experiment1']['distributionParams']['populationList'].append({'distributionModel':"density_profile",'popID':'Golgi_pop0','densityFilePath':'/home/rokas/Golgi_data/Pure NeuG density matrix of shape 69 630.txt',\
    'planeDimensions':{'dim1':'x','dim2':'y'},'dim1CoordinateVector':[0,3000],'dim2CoordinateVector':[0,110],'dim3':'z','dim3Boundary':300,\
    'distanceModel':'random','canonicalVolumeBaseAreainMicrons':5.00318495*5.00318495 })

    net_params_V2010_multiple['experiment1']['connParams']={}
    net_params_V2010_multiple['experiment1']['connParams']['populationPairs']=[]
    net_params_V2010_multiple['experiment1']['connParams']['populationPairs'].append({'electricalConnModel':"Vervaeke_2010_based",'prePopID':'Golgi_pop0',\
    'postPopID':'Golgi_pop0','spatialScale':1,'testingConductanceScale':1,'units':'nS','normalizeConductances':True,\
        'prePoptargetGroup':{'segmentGroupList':["apical","basolateral"],\
        'segmentGroupProbabilities':{"apical":0.5,"basolateral":0.5 }},\
        'postPoptargetGroup':{'segmentGroupList':["apical","basolateral"],\
        'segmentGroupProbabilities':{"apical":0.5,"basolateral":0.5}}})

    
    
    net_params_V2010_multiple['experiment1']['inputParams']=[]
    inputGroups_pop0_exp1=[]
    inputGroups_pop0_exp1.append({'inputModel':"variable_basal_firing_rate",'inputLabel':'vrpop0','amplitudeDistribution':"gaussian",'averageAmp':0,\
    'stDevAmp':32,'ampUnits':"pA",'offsetDistribution':"constant",'valueOffset':0,'offsetUnits':"ms"})
    synapseList0_pop0_exp1=[]
    synapseList0_pop0_exp1.append({'synapseType':"MF",'synapseMode':"transient",'averageRate':200,'delay':600,'duration':250,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':8,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basolateral"],'segmentGroupProbabilities':{"basolateral":1}})

    synapseList0_pop0_exp1.append({'synapseType':"PF", 'synapseMode':"transient",'averageRate':350,'delay':850,'duration':250,'units':'ms',\
                       'numberModel':"constant number of inputs per cell",'noInputs':50,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical"],'segmentGroupProbabilities':{"apical":1}})

    synapseList1_pop0_exp1=[]
    synapseList1_pop0_exp1.append({'synapseType':"MF",'synapseMode':"persistent",'averageRate':2,\
                       'numberModel':"constant number of inputs per cell",'noInputs':20,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["basolateral"],'segmentGroupProbabilities':{"basolateral":1}})
    

    synapseList1_pop0_exp1.append({'synapseType':"PF",'synapseMode':"persistent",'averageRate':0.5,\
                       'numberModel':"constant number of inputs per cell",'noInputs':100,'targetingModel':"segment groups and segments",\
                         'segmentGroupList':["apical"],'segmentGroupProbabilities':{"apical":1}})
    

    inputGroups_pop0_exp1.append({'inputModel':'XF','inputLabel':'XFpop0','targetingRegime':"3D_region_specific",'regionList':[ {'xVector':[1300,1900],'yVector':[0,110],'zVector':[0,100]}],'fractionToTarget':0.22,\
                                  'synapseList':synapseList0_pop0_exp1,'colocalizeSynapses':False})

    inputGroups_pop0_exp1.append({'inputModel':'XF','inputLabel':'XFpop0_background','targetingRegime':"uniform",'fractionToTarget':1,\
                                  'synapseList':synapseList1_pop0_exp1,'colocalizeSynapses':False})
    
                             
    net_params_V2010_multiple['experiment1']['inputParams'].append({'popName':'Golgi_pop0','inputGroups':inputGroups_pop0_exp1})
    

    







    
    
    #######
    
    

    sim_params={'simulator':"no simulation",'duration':2500,'timeStep':0.0025,'numTrials':1,'globalSeed':False,'trialSeed':True,'plotSpecifier':False,\
    'saveSomataPositions':True,'parentDirRequired':True,'parentDir':parentdir,'currentDirRequired':True,'currentDir':currentdir,'networkDir':'experiment',\
        'saveInputReceivingCellID':True}
    
    
   
    run_simulations(net_params_V2010_multiple,sim_params)

   

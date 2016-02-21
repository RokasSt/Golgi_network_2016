
from  Generate_Golgi_Network_v2 import *
import os.path

def run_simulations(network_parameters,simulation_parameters):  
    
    if simulation_parameters['globalSeed']:
       for simulation_trial in range(0,simulation_parameters['numTrials']):
           for exp_i in range(0,len(network_parameters)):
               Cell_array=network_parameters['experiment%d'%(exp_id)]['popParams']
               Position_array=network_parameters['experiment%d'%(exp_id)]['distributionParams']
               Conn_array=network_parameters['experiment%d'%(exp_id)]['connParams']
               Input_array=network_parameters['experiment%d'%(exp_id)]['inputParams']
               Sim_array=simulation_parameters
               Sim_array['experimentID']=network_parameters['experiment%d'%(exp_id)]['experimentID']
               Sim_array['simID']=simulation_trial
               newpath = r'simulations/%s/sim%d'%(network_parameters['experiment%d'%(exp_id)]['experimentID'],simulation_trial)
               if not os.path.exists(newpath):
                  os.makedirs(newpath)
               sim_params,pop_params=generate_golgi_cell_net("Golgi_%s"%(network_parameters['experiment%d'%(exp_id)]['experimentID']),\
                                                    Cell_array,Position_array,Conn_array,Input_array,Sim_array)
               if simulation_parameters['plotSpecifier']:
                  save_soma_positions(pop_params,r'simulations/%s'%(network_parameters['experiment%d'%(exp_id)]['experimentID']))
                  print("saved soma positions in the experiment directory %s"%r'simulations/%s'%(network_parameters['experiment%d'%(exp_id)]['experimentID']))
               generate_LEMS_and_run(sim_params,pop_params)
    else:
       if simulation_parameters['trialSeed']:
          for simulation_trial in range(0,simulation_parameters['numTrials']):
              seed_number=random.sample(range(0,15000),1)[0]
              for exp_i in range(0,len(network_parameters)):
                  Cell_array=network_parameters['experiment%d'%(exp_id)]['popParams']
                  Position_array=network_parameters['experiment%d'%(exp_id)]['distributionParams']
                  Conn_array=network_parameters['experiment%d'%(exp_id)]['connParams']
                  Input_array=network_parameters['experiment%d'%(exp_id)]['inputParams']
                  Sim_array=simulation_parameters
                  Sim_array['experimentID']=network_parameters['experiment%d'%(exp_id)]['experimentID']
                  Sim_array['simID']=simulation_trial
                  Sim_array['trialSeedNumber']=seed_number
                  newpath = r'simulations/%s/sim%d'%(network_parameters['experiment%d'%(exp_id)]['experimentID'],simulation_trial)
                  if not os.path.exists(newpath):
                     os.makedirs(newpath)
                  sim_params,pop_params=generate_golgi_cell_net("Golgi_%s_trial%d"%(network_parameters['experiment%d'%(exp_id)]['experimentID'],simulation_trial),\
                                            Cell_array,Position_array,Conn_array,Input_array,Sim_array)
                  if save_soma_specifier[1]=="Yes":
                     save_soma_positions(pop_params,r'simulations/%s/sim%d'%(network_parameters['experiment%d'%(exp_id)]['experimentID'],simulation_trial))
                     print("saved soma positions in the experiment directory %s"%r'simulations/%s/sim%d'%(network_parameters['experiment%d'%(exp_id)]['experimentID'],simulation_trial))
                  generate_LEMS_and_run(sim_params,pop_params)
           

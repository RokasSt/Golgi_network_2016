
import neuroml
from pyneuroml import pynml
from pyneuroml.lems.LEMSSimulation import LEMSSimulation
import math
import neuroml.writers as writers
from neuroml.utils import validate_neuroml2
import random
import numpy as np
import string
import collections
import os.path
from methods_v2 import *
from cell_distribution_models import *
from connectivity_models import *
from input_models import *


### a main script for generating and running golgi cell network by Rokas Stanislovas (2016)
def generate_golgi_cell_net(ref,cell_array,location_array,connectivity_information,input_information,simulation_parameters):
        
        
        if simulation_parameters['globalSeed']:
           random.seed(12345)
           seed=12345
        else:
           if simulation_parameters["trialSeed"]:
              random.seed(simulation_parameters["trialSeedNumber"])
              seed=simulation_parameters["trialSeedNumber"]

        nml_doc = neuroml.NeuroMLDocument(id=ref)
        #cell_array will have to include cell_types and no_of_cells
        #connectivity_information is a list of lists that will have to include connectivity parameters; now code only for a random configuration with parameters connection_probability and conductance_strength

        
        cell_type_list=[]
        for x in range(0,len(cell_array)):
            cell_type_list.append(cell_array[x]['cellType'])
            
        unique_cell_names=np.unique(cell_type_list)

        for unique_cell in unique_cell_names:
            if 'networkDir' in simulation_parameters and 'parentDirRequired' in simulation_parameters:
               if simulation_parameters['parentDirRequired'] and (simulation_parameters['networkDir']=="example" or simulation_parameters['networkDir']=="experiment"):
                  include_cell=neuroml.IncludeType(href="/../../../"+"%s.cell.nml"%unique_cell)
            else:
               include_cell=neuroml.IncludeType(href="%s.cell.nml"%unique_cell)

            nml_doc.includes.append(include_cell)

	
	# Create network
	net = neuroml.Network(id=ref+"_network",type="networkWithTemperature",temperature="23 degC")
	nml_doc.networks.append(net)

        Note_string="Parameter arrays for building this network are listed below:\n"

        
        Golgi_pop_index_array=[]
        neuroml_Golgi_pop_array={}

        for x in range(0,len(cell_array)):
	    Golgi_pop = neuroml.Population(id=cell_array[x]['popID'], size =cell_array[x]['size'], type="populationList",
		                  component=cell_array[x]['cellType'])
	    Golgi_pop_index_array.append(cell_array[x]['popID'])
            neuroml_Golgi_pop_array[cell_array[x]['popID']]=Golgi_pop
	    

        
        
	cell_position_array={}
	
	Note_string=Note_string+"Cell distribution parameters:\n"
	
        no_density_model=True
        #################  
         ##### below lines to make a reference template for the density based model:
    #   net_params_test_2010_multiple['experiment1']['distributionParams']={}
    #   net_params_test_2010_multiple['experiment1']['distributionParams']['distributionModel']="density based"
    #   net_params_test_2010_multiple['experiment1']['distributionParams']['populationList']=[]
    #   net_params_test_2010_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Golgi_pop0','densityFilePath':'/home/rokas/Golgi_data/GlyT2 density matrix of shape 35 152.txt',\
    #   'planeDimensions':{'dim1':'x','dim2':'z'},'dim1CoordinateVector':[1300,1500],'dim2CoordinateVector':[0,50],'distanceModel':'minimal_distance',\
    #   'minimalDistance':25})
    #   net_params_test_2010_multiple['experiment1']['distributionParams']['populationList'].append({'popID':'Golgi_pop1','densityFilePath':'/home/rokas/Golgi_data/GlyT2 density matrix of shape 35 152.txt',\
    #   'planeDimensions':{'dim1':'x','dim2':'z'},'dim1CoordinateVector':[1300,1500],'dim2CoordinateVector':[0,50],'dim3':'y','dim3Boundary':200,\
    #   'distanceModel':'minimal_distance/random/random_no_overlap','minimalDistance':25,'canonicalVolumeBaseArea':54})  
	if string.lower(location_array['distributionModel'])=="density based":
           ### will override cell numbers in cell_array if specified
           no_density_model=False
    
           Note_string=Note_string+"Model: density based\n"
           Note_string=Note_string+"Model parameters:\n"
           for cell_group in range(0,len(location_array['populationList'])):
               total_no_of_cells=0
               cellPopName=location_array['populationList'][cell_group]['popID']
               golgi_pop=neuroml_Golgi_pop_array[cellPopName]
               for pop in range(0,len(cell_array)):
                   if cellPopName==cell_array[pop]['popID']:
                      if simulation_parameters['parentDirRequired']:
                         cell_type_name=simulation_parameters['parentDir']+"/NeuroML2"+"/"+cell_array[pop]['cellType']
                      else:
                         cell_type_name=cell_array[pop]['cellType']
                      pop_index_popParams=pop

               densityFilePath=location_array['populationList'][cell_group]['densityFilePath']
               location_parameters=location_array['populationList'][cell_group]
               golgi_pop_object=neuroml_Golgi_pop_array[cellPopName]
               

               pop_position_array, total_no_of_cells,Golgi_pop=density_model(densityFilePath,location_parameters,cell_type_name,golgi_pop_object,seed)


               cell_array[pop_index_popParams]['size']=total_no_of_cells


               cell_position_array[cell_array[pop_index_popParams]['popID']]=pop_position_array
          
               net.populations.append(Golgi_pop)

               Note_string=Note_string+"%s"%location_array['populationList'][cell_group]+"\n"
               
        if no_density_model:
           ###### if no_density model it assumes that dimensions of a cubic environment are specified
           x_dim=location_array['xDim']
           y_dim=location_array['yDim']
           z_dim=location_array['zDim']
           for cell_population in range(0,len(cell_array)):
               cell_position_array[ cell_array[cell_population]['popID'] ]=np.zeros([cell_array[cell_population]['size'],3])
              
        ##############
        if string.lower(location_array['distributionModel'])=="random_minimal_distance":
           Note_string=Note_string+"Model: random with global minimal distance between cell bodies\n"
           Note_string=Note_string+"Model parameters:\n"
           for cell_pop in range(0,len(cell_array)):
               golgi_pop_object=neuroml_Golgi_pop_array[cell_array[cell_pop]['popID']]
               cell_position_array,Golgi_pop=random_minimal_distance(cell_position_array,cell_array,location_array,\
               cell_pop,cell_array[cell_pop]['size'],golgi_pop_object,x_dim,y_dim,z_dim,seed)

               net.populations.append(Golgi_pop)
               
           Note_string=Note_string+"%s"%location_array+"\n"
        ############  random positioning but no overlap between somata                  
        if string.lower(location_array['distributionModel'])=="random_no_overlap":
           Note_string=Note_string+"Model: random with no overlap of cell bodies\n"
           Note_string=Note_string+"Model parameters:\n"
           cell_diameter_array={}
           for cell_pop in range(0,len(cell_array)):
               if simulation_parameters['parentDirRequired']:
                  cell_diameter=get_soma_diameter(simulation_parameters['parentDir']+"/NeuroML2"+"/"+cell_array[cell_pop]['cellType'])
               else:
                  cell_diameter=get_soma_diameter(cell_array[cell_pop]['cellType'])
               cell_diameter_array[cell_array[cell_pop]['popID']]=cell_diameter

           for cell_pop in range(0,len(cell_array)):

               golgi_pop_object=neuroml_Golgi_pop_array[cell_array[cell_pop]['popID']]
               
               cell_position_array,Golgi_pop=random_no_overlap(cell_position_array,cell_array,cell_array[cell_pop]['popID'],cell_diameter_array,\
               cell_pop,cell_array[cell_pop]['size'],golgi_pop_object,x_dim,y_dim,z_dim,seed)

               net.populations.append(Golgi_pop)
               
           Note_string=Note_string+"%s"%location_array+"\n"

        ###### simply random positioning in a cubic environment               
        if string.lower(location_array['distributionModel'])=="random":
           Note_string=Note_string+"Model: random positions with cell bodies overlaping"
           Note_string=Note_string+"Model parameters:\n"
           for cell_pop in range(0,len(cell_array)):
               golgi_pop=neuroml_Golgi_pop_array[cell_array[cell_pop]['popID']]
               for cell in range(0,cell_array[cell_pop]['size']):
	           Golgi_cell=neuroml.Instance(id="%d"%cell)
	           golgi_pop.instances.append(Golgi_cell)
	           X=random.random()
	           Y=random.random()
	           Z=random.random()
                   cell_position_array[cell_array[cell_pop]['popID']][cell,0]=x_dim*X
                   cell_position_array[cell_array[cell_pop]['popID']][cell,1]=y_dim*Y
                   cell_position_array[cell_array[cell_pop]['popID']][cell,2]=z_dim*Z
                   Golgi_cell.location=neuroml.Location(x=x_dim*X, y=y_dim*Y, z=z_dim*Z)
                   print cell_position_array[cell_array[cell_pop]['popID']][cell,0], cell_position_array[cell_array[cell_pop]['popID']][cell,1], cell_position_array[cell_array[cell_pop]['popID']][cell,2]
               net.populations.append(golgi_pop)
           Note_string=Note_string+"%s"%location_array+"\n"
   
        ##### include cell_array into notes once the final pop sizes are known
        Note_string=Note_string+"Population parameters:"+"\n"
        for cell_pop in range(0,len(cell_array)):
            Note_string=Note_string+"%s"%cell_array[cell_pop]+"\n"
        Note_string=Note_string+"Connectivity parameters for a list of population pairs:"+"\n" 
        ############################################ connectivity block
        synapse_name_array=[]        
        connMatrix_array=[]
        initial_projection_counter=0
        synapse_counter=0
        for pair in range(0,len(connectivity_information['populationPairs']) ):
            prePop=connectivity_information['populationPairs'][pair]['prePopID']  
            postPop=connectivity_information['populationPairs'][pair]['postPopID']
            for pop in range(0,len(cell_array)):
                if cell_array[pop]['popID']==prePop:
                   prePop_listIndex=pop
                   prePopSize=cell_array[pop]['size']
                if cell_array[pop]['popID']==postPop:
                   postPop_listIndex=pop
                   postPopSize=cell_array[pop]['size']
            
            if 'electricalConnModel' in connectivity_information['populationPairs'][pair]:
               ########## 2012 publication-based generation of model connectivity 
               if connectivity_information['populationPairs'][pair]['electricalConnModel']=="Vervaeke_2012_based" or connectivity_information['populationPairs'][pair]['electricalConnModel']=="explicit_connection_probabilities":
                  pair_connectivity_parameters=connectivity_information['populationPairs'][pair]
                  pre_pop_cell_component=cell_array[prePop_listIndex]['cellType']
                  post_pop_cell_component=cell_array[postPop_listIndex]['cellType']
                  pre_pop_cell_positions=cell_position_array[prePop]
                  post_pop_cell_positions=cell_position_array[postPop]
                  if simulation_parameters['parentDirRequired']:
                     proj, nonempty_projection,gap_junction_array=Vervaeke_2012_AND_explicit_conn_prob_model(pair,initial_projection_counter,prePop,prePop_listIndex,prePopSize,pre_pop_cell_component,pre_pop_cell_positions,\
                                postPop,postPop_listIndex,postPopSize,post_pop_cell_component,post_pop_cell_positions,pair_connectivity_parameters,seed,\
                                simulation_parameters['parentDir'])
                  else:
                     proj, nonempty_projection,gap_junction_array=Vervaeke_2012_AND_explicit_conn_prob_model(pair,initial_projection_counter,prePop,prePop_listIndex,prePopSize,pre_pop_cell_component,pre_pop_cell_positions,\
                                postPop,postPop_listIndex,postPopSize,post_pop_cell_component,post_pop_cell_positions,pair_connectivity_parameters,seed)
                
                  if nonempty_projection:
                     initial_projection_counter+=1
                     net.electrical_projections.append(proj)
                     for gapJ in range(0,len(gap_junction_array)):
                         nml_doc.gap_junctions.append(gap_junction_array[gapJ])
               

               ############# 2010, both connection probabilities and synaptic weights are distance-dependent              
               if connectivity_information['populationPairs'][pair]['electricalConnModel']=="Vervaeke_2010_based":
                  pair_connectivity_parameters=connectivity_information['populationPairs'][pair]
                  pre_pop_cell_component=cell_array[prePop_listIndex]['cellType']
                  post_pop_cell_component=cell_array[postPop_listIndex]['cellType']
                  pre_pop_cell_positions=cell_position_array[prePop]
                  post_pop_cell_positions=cell_position_array[postPop]
                  
                  if simulation_parameters['parentDirRequired']:
                     proj, nonempty_projection,gap_junction_array=Vervaeke_2010_model(pair,initial_projection_counter,prePop,prePop_listIndex,prePopSize,pre_pop_cell_component,pre_pop_cell_positions,\
                                postPop,postPop_listIndex,postPopSize,post_pop_cell_component,post_pop_cell_positions,pair_connectivity_parameters,seed,\
                                simulation_parameters['parentDir'])
                  else:
                     proj, nonempty_projection,gap_junction_array=Vervaeke_2010_model(pair,initial_projection_counter,prePop,prePop_listIndex,prePopSize,pre_pop_cell_component,pre_pop_cell_positions,\
                                postPop,postPop_listIndex,postPopSize,post_pop_cell_component,post_pop_cell_positions,pair_connectivity_parameters,seed)

                  if nonempty_projection:
                     initial_projection_counter+=1
                     net.electrical_projections.append(proj)
                     for gapJ in range(0,len(gap_junction_array)):
                         nml_doc.gap_junctions.append(gap_junction_array[gapJ])

            #######  introduce chemical connections into network building    
            if 'chemicalConnModel' in connectivity_information['populationPairs'][pair]:    
               pair_connectivity_parameters=connectivity_information['populationPairs'][pair]
               pre_pop_cell_component=cell_array[prePop_listIndex]['cellType']
               post_pop_cell_component=cell_array[postPop_listIndex]['cellType']
               pre_pop_cell_positions=cell_position_array[prePop]
               post_pop_cell_positions=cell_position_array[postPop]
               
               if simulation_parameters['parentDirRequired']:
                  proj, nonempty_projection,gap_junction_array,synapse_name=chemical_connection_model(pair,initial_projection_counter,prePop,prePop_listIndex,prePopSize,pre_pop_cell_component,pre_pop_cell_positions,\
                                postPop,postPop_listIndex,postPopSize,post_pop_cell_component,post_pop_cell_positions,pair_connectivity_parameters,seed,\
                                simulation_parameters['parentDir'])
               else:
                  proj, nonempty_projection,gap_junction_array,synapse_name=chemical_connection_model(pair,initial_projection_counter,prePop,prePop_listIndex,prePopSize,pre_pop_cell_component,pre_pop_cell_positions,\
                                postPop,postPop_listIndex,postPopSize,post_pop_cell_component,post_pop_cell_positions,pair_connectivity_parameters,seed)

               synapse_name_array.append(synapse_name)
               if nonempty_projection:
                  initial_projection_counter+=1
                  net.electrical_projections.append(proj)
                  for gapJ in range(0,len(gap_junction_array)):
                      nml_doc.gap_junctions.append(gap_junction_array[gapJ])
            
            Note_string=Note_string+"%s"%connectivity_information['populationPairs'][pair]+"\n"                                      
        ####################        input block                                                           
        Note_string=Note_string+"Input parameters for a list of populations:"+"\n" 
        for pop in range(0,len(input_information)):
            popID=input_information[pop]['popName']
            Note_string=Note_string+"Input group parameters for %s:"%popID+"\n" 
            for pop in range(0,len(cell_array)):
                if cell_array[pop]['popID']==popID:
                   pop_listIndex=pop
                   popSize=cell_array[pop]['size']
            input_group_array=input_information[pop]['inputGroups']
            cellType=cell_array[pop_listIndex]['cellType']
            for input_group in range(0,len(input_group_array)):
                if input_group_array[input_group]['inputModel']=='XF' and input_group_array[input_group]['targetingRegime']=="uniform":
                   if simulation_parameters['parentDirRequired']:
                      input_list,poisson_synapse_array,synapse_name_list=XF_input_model_uniform(popID,popSize,cellType,input_group_array[input_group],seed,\
                      simulation_parameters['parentDir'])
                   else:
                      input_list,poisson_synapse_array,synapse_name_list=XF_input_model_uniform(popID,popSize,cellType,input_group_array[input_group],seed)                                          
                   

                   synapse_name_array.extend(synapse_name_list)

                   net.input_lists.append(input_list)

                   for poisson_syn in range(0,len(poisson_synapse_array)):
          
                       nml_doc.poisson_firing_synapses.append(poisson_synapse_array[poisson_syn])

                if input_group_array[input_group]['inputModel']=='XF' and input_group_array[input_group]['targetingRegime']=="3D_region_specific":
                        
                   if simulation_parameters['parentDirRequired']:
                           
                      input_list,poisson_synapse_array,synapse_name_list=XF_input_model_3D_region_specific(popID,cellType,input_group_array[input_group],\
                      cell_position_array[popID],seed,simulation_parameters['parentDir'])   

                   else:
                      input_list,poisson_synapse_array,synapse_name_list=XF_input_model_3D_region_specific(popID,cellType,input_group_array[input_group],\
                      cell_position_array[popID],seed)                                          
                   

                   synapse_name_array.extend(synapse_name_list)

                   net.input_lists.append(input_list)

                   for poisson_syn in range(0,len(poisson_synapse_array)):
          
                       nml_doc.poisson_firing_synapses.append(poisson_synapse_array[poisson_syn])                
        
	        ###### implementing physiological heterogeneity between cells with variations in a basal firing rate
                if input_group_array[input_group]['inputModel']=="variable_basal_firing_rate":

                   input_list_array,pulseGenerator_array=variable_basal_firing_rate(popID,popSize,cellType,input_group_array[input_group],\
                   simulation_parameters['duration'],seed)                                          

                   for input_list in range(0,len(input_list_array)):
          
                       net.input_lists.append(input_list_array[input_list])
                       nml_doc.pulse_generators.append(pulseGenerator_array[input_list])
                   
	               
	        ##############
                if input_group_array[input_group]['inputModel']=="testing":

                   input_list_array,pulseGenerator_array=testing(popID,popSize,cellType,input_group_array[input_group],seed)                                          

                   for input_list in range(0,len(input_list_array)):
          
                       net.input_lists.append(input_list_array[input_list])
                       nml_doc.pulse_generators.append(pulseGenerator_array[input_list])

                
                Note_string=Note_string+"%s"%input_group_array[input_group]+"\n"            

        ##############       
	unique_synapse_names=np.unique(synapse_name_array)
        for unique_synapse in unique_synapse_names:
            if 'networkDir' in simulation_parameters and 'parentDirRequired' in simulation_parameters:
               if simulation_parameters['parentDirRequired'] and ( simulation_parameters['networkDir']=="example" or simulation_parameters['networkDir']=="experiment"):
                  include_synapse=neuroml.IncludeType(href="/../../../"+"%s.synapse.nml"%unique_synapse)
            else:
               include_synapse=neuroml.IncludeType(href="%s.synapse.nml"%unique_synapse)
            nml_doc.includes.append(include_synapse)
                                                 
        net.notes=Note_string
        
        if simulation_parameters['parentDirRequired']:

           if 'networkDir' in simulation_parameters:
               if  simulation_parameters['networkDir']=="example":
                   nml_file_dir =simulation_parameters['parentDir']+"/NeuroML2/NML2_LEMS_Net_Examples/"+simulation_parameters['experimentID']+"/"+"sim%d"%simulation_parameters['simID']+"/"+'%s.net.nml'%ref
                   path=simulation_parameters['parentDir']+"/NeuroML2/NML2_LEMS_Net_Examples/"+simulation_parameters['experimentID']+"/"+"sim%d"%simulation_parameters['simID']
               if simulation_parameters['networkDir']=="experiment":
                  nml_file_dir =simulation_parameters['parentDir']+"/NeuroML2/NML2_LEMS_Experiments/"+simulation_parameters['experimentID']+"/"+"sim%d"%simulation_parameters['simID']+"/"+'%s.net.nml'%ref
                  path=simulation_parameters['parentDir']+"/NeuroML2/NML2_LEMS_Experiments/"+simulation_parameters['experimentID']+"/"+"sim%d"%simulation_parameters['simID']

        

               if not os.path.exists(path):
                  os.makedirs(path)
        else:
           nml_file_dir ='%s.net.nml'%ref
        
        writers.NeuroMLWriter.write(nml_doc,nml_file_dir)


        nml_file='%s.net.nml'%ref

        print("Written network file to: "+nml_file_dir)
    
        ###### Validate the NeuroML2 ######   

        validate_neuroml2(nml_file_dir)

        sim_info_array={}
        sim_info_array['ref']=ref
        sim_info_array['netID']=net.id
        sim_info_array['simParams']=simulation_parameters
        sim_info_array['nmlFile']=nml_file
        sim_info_array['nmlPath']=path

        cell_info_array={}
        cell_info_array['popParams']=cell_array
        cell_info_array['cellPositionArray']=cell_position_array
        
        return sim_info_array, cell_info_array

def generate_LEMS_and_run(sim_array,pop_array):
        ref= sim_array['ref']
        net_id=sim_array['netID']
        simulation_parameters=sim_array['simParams']
        nml_file=sim_array['nmlFile']
        path=sim_array['nmlPath']

        cell_array=pop_array['popParams']
        
        
        # Create a LEMSSimulation to manage creation of LEMS file

        ls = LEMSSimulation(ref, simulation_parameters['duration'], simulation_parameters['timeStep'])
        
        # Point to network as target of simulation
    
        ls.assign_simulation_target(net_id)
        print simulation_parameters['parentDir']
        ls.include_neuroml2_file(nml_file,True,path)
        #ls.include_neuroml2_file("/home/rokas/Golgi_network_2016/NeuroML2/Very_Simple_Golgi_test_morph.cell.nml")
        

        # Specify Displays and Output Files
	for x in range(0,len(cell_array)):
	    disp = "display_voltages%s"%(cell_array[x]['popID'])
	    ls.create_display(disp, "Voltages %s"%(cell_array[x]['popID']), "-75", "50")
	       
	    max_traces = 20
	    if cell_array[x]['size']<=max_traces:
	       for i in range(cell_array[x]['size']):
		   quantity = "%s/%i/%s/v"%(cell_array[x]['popID'], i,cell_array[x]['cellType'])
	           ls.add_line_to_display(disp, "../%s/%i: Vm"%(cell_array[x]['popID'],i), quantity, "1mV", pynml.get_next_hex_color())
                   of0 = 'Volts%d_file0_%d'%(x,i)
                   ls.create_output_file(of0, "simulations/%s/sim%d/%s_cell%d.dat"%(simulation_parameters['experimentID'],simulation_parameters['simID'],\
                                                                                    cell_array[x]['popID'],i))
		   ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
					   
	    else:
	       randomly_select_displayed_cells=random.sample(range(cell_array[x]['size']),max_traces)
	       for y in randomly_select_displayed_cells:
                   quantity = "%s/%i/%s/v"%(cell_array[x]['popID'], y, cell_array[x]['cellType'])
		   ls.add_line_to_display(disp, "../%s/%i: Vm"%(cell_array[x]['popID'],y), quantity, "1mV", pynml.get_next_hex_color())
					      
	       for i in range(cell_array[x]['size']):
		   quantity = "%s/%i/%s/v"%(cell_array[x]['popID'], i,cell_array[x]['cellType'])
                   of0 = 'Volts%d_file0_%d'%(x,i)
                   ls.create_output_file(of0, "simulations/%s/sim%d/%s_cell%d.dat"%(simulation_parameters['experimentID'],\
                   simulation_parameters['simID'],x,i))
		   ls.add_column_to_output_file(of0, 'v%i'%i, quantity)
       
	# save LEMS file
        if simulation_parameters['parentDirRequired']:
           if simulation_parameters['networkDir']=="example":
              lems_file_name_dir=simulation_parameters['parentDir']+"/NeuroML2/NML2_LEMS_Net_Examples/"+simulation_parameters['experimentID']+"/"+"sim%d"%simulation_parameters['simID']+"/"+"LEMS_%s.xml"%ref
              lems_file_name = ls.save_to_file(lems_file_name_dir)
              

           if simulation_parameters['networkDir']=="experiment":
              lems_file_name_dir=simulation_parameters['parentDir']+"/NeuroML2/NML2_LEMS_Experiments/"+simulation_parameters['experimentID']+"/"+"sim%d"%simulation_parameters['simID']+"/"+"LEMS_%s.xml"%ref
              lems_file_name = ls.save_to_file(lems_file_name_dir)
        else:
           lems_file_name = ls.save_to_file()
           lems_file_name_dir="LEMS_%s.xml"%ref

        if simulation_parameters['plotSpecifier']:
           if simulation_parameters['simulator']=="jNeuroML":
              print("Finished building a network. Starts running a simulation with jNeuroML for %s"%lems_file_name_dir)
	      results1 = pynml.run_lems_with_jneuroml(lems_file_name, nogui=True, load_saved_data=True, plot=True)
              print("Finished running simulation with jNeuroML")
           elif simulation_parameters['simulator']=="jNeuroML_NEURON":
              print("Finished building a network. Starts running a simulation with NEURON for %s"%lems_file_name_dir)
              results1 = pynml.run_lems_with_jneuroml_neuron(lems_file_name, nogui=True, load_saved_data=True, plot=True)
              print("Finished running simulation with jNeuroML_NEURON")
           else:
              print("Finished building a network")
        else:
           if simulation_parameters['simulator']=="jNeuroML":
              print("Finished building a network. Starts running a simulation with jNeuroML for %s"%lems_file_name_dir)
	      results1 = pynml.run_lems_with_jneuroml(lems_file_name, nogui=True, load_saved_data=False, plot=False)
              print("Finished running simulation with jNeuroML")
           elif simulation_parameters['simulator']=="jNeuroML_NEURON":
              print("Finished building a network. Starts running a simulation with NEURON for %s"%lems_file_name_dir)
              results1 = pynml.run_lems_with_jneuroml_neuron(lems_file_name, nogui=True, load_saved_data=False, plot=False)
              print("Finished running simulation with jNeuroML_NEURON")
           else:
              print("Finished building a network")
         

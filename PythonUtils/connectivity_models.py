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

from methods_v2 import *




def Vervaeke_2012_AND_explicit_conn_prob_model(pair_id,projection_id,prePop,prePop_listIndex,prePopSize,preCellType,preNML2Type,pre_cell_positions,\
                                               postPop,postPop_listIndex,postPopSize,postCellType,postNML2Type,post_cell_positions,\
                                               connectivity_parameters,seed_number,parentDir=None):
    random.seed(seed_number)
    nonempty_projection=False
    gapJ_object_array=[]
    gap_counter=0
    #######
    if parentDir != None:
       preCellTypeFile=parentDir+"/NeuroML2"+"/"+preCellType
       postCellTypeFile=parentDir+"/NeuroML2"+"/"+postCellType
    else:
       preCellTypeFile=preCellType
       postCellTypeFile=postCellType
       
    if connectivity_parameters['targetingModelprePop']['model']=="segment groups and segments":
       pre_pop_target_segment_array=extract_morphology_information([preCellTypeFile],{preCellTypeFile:preNML2Type},\
                                                                                          ["segment groups",  \
                          connectivity_parameters['targetingModelprePop']['segmentGroupList']])

    if connectivity_parameters['targetingModelprePop']['model']=="segments and subsegments":
       pre_pop_target_segment_array=extract_morphology_information([preCellTypeFile],{preCellTypeFile:preNML2Type}, \
                                                  ["segments",connectivity_parameters['targetingModelprePop']['segmentList']])

    if connectivity_parameters['targetingModelpostPop']['model']=="segment groups and segments":
       post_pop_target_segment_array=extract_morphology_information([postCellTypeFile],{postCellTypeFile:postNML2Type},\
                                  ["segment groups",connectivity_parameters['targetingModelpostPop']['segmentGroupList'] ] )

    if connectivity_parameters['targetingModelpostPop']['model']=="segments and subsegments":
       post_pop_target_segment_array=extract_morphology_information([postCellTypeFile],{postCellTypeFile:postNML2Type}, \
            ["segments",connectivity_parameters['targetingModelpostPop']['segmentGroupList']])  
                                            
    proj = neuroml.ElectricalProjection(id="proj%d"%projection_id,presynaptic_population=prePop,postsynaptic_population=postPop)
    
    
    conn_count = 0
    
                                                                              
    if connectivity_parameters['gapJunctionModel']=="constant number of GJ contacts per pair":
       no_of_GJcon_per_pair=connectivity_parameters['numberGJ']
    if connectivity_parameters['gapJunctionModel']=="variable number of GJ contacts per pair":
       if connectivity_parameters['distribution']=="binomial":
          no_of_GJcon_per_pair=np.random.binomial(connectivity_parameters['maxNoGJs'],\
          connectivity_parameters['averageNoGJs']/connectivity_parameters['maxNoGJs'])
       #### other models can be added in the future

    conductance_scaling=1

    if 'testingConductanceScale' in connectivity_parameters:
       conductance_scaling=connectivity_parameters['testingConductanceScale']
 
    if connectivity_parameters['conductanceModel']=="constant":
       conductance_value=connectivity_parameters['conductanceValue']
       conductance_units=connectivity_parameters['units']
       gap_junction = neuroml.GapJunction(id="gap_junction%d%d"%(pair_id,gap_counter),conductance="%f%s"%(conductance_value*conductance_scaling,conductance_units)) 
       gap_id_per_pair="gap_junction%d"%gap_counter        
       gapJ_object_array.append(gap_junction)
       gap_counter+=1


    spatial_scale=1
    if 'spatialScale' in connectivity_parameters:
       spatial_scale=connectivity_parameters['spatialScale']
                                    
    for Pre_cell in range(0,prePopSize):
        for Post_cell in range(0,postPopSize):
                       
            if connectivity_parameters['electricalConnModel']=="explicit_connection_probabilities":
               connection_probability=connectivity_parameters['connProbability']
                          
            if connectivity_parameters['electricalConnModel']=="Vervaeke_2012_based":
               distance_between_cells=distance(pre_cell_positions[Pre_cell],post_cell_positions[Post_cell])/spatial_scale
               connection_probability=connection_probability_vervaeke_2010(distance_between_cells)
                          
            if random.random() < connection_probability:

               if connectivity_parameters['targetingModelprePop']['model']=="segment groups and segments":
                  pre_target_points=get_unique_target_points(pre_pop_target_segment_array,"segment groups and segments",\
                             [connectivity_parameters['targetingModelprePop']['segmentGroupList'],\
connectivity_parameters['targetingModelprePop']['segmentGroupProbabilities']],no_of_GJcon_per_pair)

               if connectivity_parameters['targetingModelprePop']['model']=="segments and subsegments":
                  pre_target_points=get_unique_target_points(pre_pop_target_segment_array,"segments and subsegments",\
 [connectivity_parameters['targetingModelprePop']['segmentList'],\
 connectivity_parameters['targetingModelprePop']['segmentProbabilities'],\
 connectivity_parameters['targetingModelprePop']['fractionAlongANDsubsegProbabilities']],no_of_GJcon_per_pair)
       
               if connectivity_parameters['targetingModelpostPop']['model']=="segment groups and segments":

                  post_targeting_mode="segment groups and segments"

                  post_targeting_parameters=[connectivity_parameters['targetingModelpostPop']['segmentGroupList'],\
                       connectivity_parameters['targetingModelpostPop']['segmentGroupProbabilities']]

               if connectivity_parameters['targetingModelpostPop']['model']=="segments and subsegments":

                  post_targeting_mode="segments and subsegments"

                  post_targeting_parameters=[connectivity_parameters['targetingModelpostPop']['segmentList'],\
 connectivity_parameters['targetingModelpostPop']['segmentProbabilities'],connectivity_parameters['targetingModelpostPop']['fractionAlongANDsubsegProbabilities']]

                  for pre_target_point in range(0,len(pre_target_points)):
                      if 'maximalConnDistance' in connectivity_parameters:
                         x=0
                         while x==0:
                             post_target_point=get_unique_target_points(post_pop_target_segment_array,post_targeting_mode,post_targeting_parameters,1) 

                             if get_3D_connection_length(preCellTypeFile,postCellTypeFile,preNML2Type,postNML2Type,pre_cell_positions,post_cell_positions,Pre_cell,\
                                Post_cell,pre_target_points[pre_target_point,0],post_target_point[0,0],\
                                pre_target_points[pre_target_point,1],post_target_point[0,1]) <=connectivity_parameters['maximalConnDistance']:
                                x=1
                      else:
                         post_target_point=get_unique_target_points(post_pop_target_segment_array,post_targeting_mode,\
                                                                             post_targeting_parameters,1)

                      Pre_segment_id=pre_target_points[pre_target_point,0]
                      Post_segment_id=post_target_point[0,0]
                      Pre_fraction=pre_target_points[pre_target_point,1]
                      Post_fraction=post_target_point[0,1]

                      if connectivity_parameters['conductanceModel']=="variable":
                         if string.lower(connectivity_parameters['distribution'])=="gaussian":
                            conductance=random.gauss(connectivity_parameters['averageConductance'],\
                     connectivity_parameters['stdDev'])
                            conductanceUnits=connectivity_parameters['units']
                            gap_junction = neuroml.GapJunction(id="gap_junction%d%d"%(pair_id,gap_counter), conductance="%f%s"%(conductance*conductance_scaling,conductanceUnits) )
                            gapJ_object_array.append(gap_junction)        
		            gap_counter+=1
                         #other options can be added such as gamma distribution
                      
                      conn =neuroml.ElectricalConnectionInstance(id=conn_count,\
pre_cell="../%s/%d/%s"%(prePop,Pre_cell,preCellType),\
post_cell="../%s/%d/%s"%(postPop,Post_cell,postCellType),synapse=gap_junction.id,\
                                                             pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                                                             pre_fraction_along="%f"%Pre_fraction,post_fraction_along="%f"%Post_fraction)
                                            
		      nonempty_projection=True
                      proj.electrical_connection_instances.append(conn)
		      conn_count+=1

    

    return proj, nonempty_projection,gapJ_object_array



def Vervaeke_2010_model(pair_id,projection_id,prePop,prePop_listIndex,prePopSize,preCellType,preNML2Type,pre_cell_positions,\
                                               postPop,postPop_listIndex,postPopSize,postCellType,postNML2Type,post_cell_positions,\
                                               connectivity_parameters,seed_number,parentDir=None):

    random.seed(seed_number)

    if parentDir != None:
       preCellTypeFile=parentDir+"/NeuroML2"+"/"+preCellType
       postCellTypeFile=parentDir+"/NeuroML2"+"/"+postCellType
    else:
       preCellTypeFile=preCellType
       postCellTypeFile=postCellType
    
    nonempty_projection=False
    gapJ_object_array=[]
    gap_counter=0
    #######
    if 'prePoptargetGroup' in connectivity_parameters:
       pre_pop_target_segment_array=extract_morphology_information([preCellTypeFile],{preCellTypeFile:preNML2Type},\
                                                                                          ["segment groups",  \
connectivity_parameters['prePoptargetGroup']['segmentGroupList']])

    if 'postPoptargetGroup' in connectivity_parameters:
       post_pop_target_segment_array=extract_morphology_information([postCellTypeFile],{postCellTypeFile:postNML2Type},\
                                  ["segment groups",connectivity_parameters['postPoptargetGroup']['segmentGroupList'] ] )

                                            
    proj = neuroml.ElectricalProjection(id="proj%d"%projection_id,presynaptic_population=prePop,postsynaptic_population=postPop)
    
    conn_count = 0
                                                                              
    conductance_scaling=1
                                                        
    conductance_array=[]
    conductance_array_spatial_scale1=[]
    make_conductance_array_no_spatial_scale=False

              
    if 'testingConductanceScale' in connectivity_parameters:
       conductance_scaling=connectivity_parameters['testingConductanceScale']
 

    spatial_scale=1

    if 'spatialScale' in connectivity_parameters:
       spatial_scale=connectivity_parameters['spatialScale']

    if connectivity_parameters['normalizeConductances']:
                                                        
       if spatial_scale != 1:
                     
          make_conductance_array_no_spatial_scale=True
                                 
    for Pre_cell in range(0,prePopSize):
        for Post_cell in range(0,postPopSize):
                                                        
            distance_between_cells=distance(pre_cell_positions[Pre_cell],post_cell_positions[Post_cell])/spatial_scale

            if connectivity_parameters['normalizeConductances']:
                                                        
               if make_conductance_array_no_spatial_scale:
                  distance_between_cells_spatial_scale1=spatial_scale*distance_between_cells
                             
                                                        
            if random.random() <connection_probability_vervaeke_2010(distance_between_cells):

               conductanceValue=synaptic_weight_vervaeke_2010(distance_between_cells)
               conductance_array.append(conductanceValue)
                                                        
               if make_conductance_array_no_spatial_scale:
                  conductanceValueN=synaptic_weight_vervaeke_2010(distance_between_cells_spatial_scale1)
                  conductance_array_spatial_scale1.append(conductanceValueN)
                                                        
               if 'prePoptargetGroup' in connectivity_parameters:
                  pre_target_points=get_unique_target_points(pre_pop_target_segment_array,"segment groups and segments",\
                             [connectivity_parameters['prePoptargetGroup' ]['segmentGroupList'],\
connectivity_parameters['prePoptargetGroup']['segmentGroupProbabilities']],1)

       
               if 'postPoptargetGroup' in connectivity_parameters:

                  post_targeting_mode="segment groups and segments"

                  post_targeting_parameters=[connectivity_parameters['postPoptargetGroup']['segmentGroupList'],\
connectivity_parameters['postPoptargetGroup']['segmentGroupProbabilities']]

                          
               if 'maximalConnDistance' in connectivity_parameters:
                  x=0
                  while x==0:
                     post_target_point=get_unique_target_points(post_pop_target_segment_array,post_targeting_mode,post_targeting_parameters,1) 
                     if get_3D_connection_length(preCellTypeFile,postCellTypeFile,preNML2Type,postNML2Type,pre_cell_positions,post_cell_positions,Pre_cell,\
                        Post_cell,pre_target_points[0,0],post_target_point[0,0],\
                        pre_target_points[0,1],post_target_point[0,1]) <=connectivity_parameters['maximalConnDistance']:
                        x=1
               else:
                  post_target_point=get_unique_target_points(post_pop_target_segment_array,post_targeting_mode,\
                                                                             post_targeting_parameters,1)

               Pre_segment_id=pre_target_points[0,0]
               Post_segment_id=post_target_point[0,0]
               Pre_fraction=pre_target_points[0,1]
               Post_fraction=post_target_point[0,1]

                          
               conn =neuroml.ElectricalConnectionInstance(id=conn_count,\
pre_cell="../%s/%d/%s"%(prePop,Pre_cell,preCellType),\
post_cell="../%s/%d/%s"%(postPop,Post_cell,postCellType),synapse="gap_junction%d%d"%(pair_id,gap_counter),\
                                                             pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                                                             pre_fraction_along="%f"%Pre_fraction,post_fraction_along="%f"%Post_fraction)
               gap_counter+=1                         
	       nonempty_projection=True

               proj.electrical_connection_instances.append(conn)
	       conn_count+=1
    ########
    conductanceUnits=connectivity_parameters['units']
    if len(conductance_array)==gap_counter:
       for GJ in range(0,len(conductance_array)):
           if make_conductance_array_no_spatial_scale:
              conductanceValue=conductance_array[GJ]*(sum(conductance_array_spatial_scale1)/sum(conductance_array))
              gap_junction = neuroml.GapJunction(id="gap_junction%d%d"%(pair_id,GJ), conductance="%f%s"%(conductanceValue*conductance_scaling,conductanceUnits) )
              gapJ_object_array.append(gap_junction) 
           else:
              conductanceValue=conductance_array[GJ]
              gap_junction = neuroml.GapJunction(id="gap_junction%d%d"%(pair_id,GJ), conductance="%f%s"%(conductanceValue*conductance_scaling,conductanceUnits) )
              gapJ_object_array.append(gap_junction) 
                           


    return proj, nonempty_projection,gapJ_object_array





#below lines to make a reference template for the chemical connections:
    # net_params_test_2012_multiple['experiment1']['connParams']['populationPairs'].append({'chemicalConnModel':"explicit_connection_probabilities",\
        #'prePopID':'Golgi_pop1','postPopID':'Golgi_pop2','synapse':'Golgi_to_gran_cell','connProb_from_PreCell_to_PostCell':0.5,'number_of_PostCellSynapses_per_PreCell':1,\
         # ,'targetingModelpostPop':{'model':"segment groups and segments",'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]}})
  
    #below lines to make a reference template for the chemical connections:
    # net_params_test_2012_multiple['experiment1']['connParams']['populationPairs'].append({'chemicalConnModel':"fixedNo_of_PostTargetCells",\
        #'prePopID':'Golgi_pop1','postPopID':'Golgi_pop2','chooseTargetMode':'random','synapse':'Golgi_to_gran_cell','number_of_PostTargetCells_per_PreCell':10,\
        # 'number_of_PostCellSynapses_per_PreCell':1,'targetingModelprePop':{'model':"segment groups and segments",'segmentGroupList':["axon_group"],'segmentGroupProbabilities':[1]},\
        #  'targetingModelpostPop':{'model':"segment groups and segments",'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]}})
   
    # net_params_test_2012_multiple['experiment1']['connParams']['populationPairs'].append({'chemicalConnModel':"variableNo_of_PostTargetCells",\
        #'prePopID':'Golgi_pop1','postPopID':'Golgi_pop2','synapse':'Golgi_to_gran_cell','chooseTargetMode':'random','targetNoModel':{'modelType':'binomial','average':15,'maxTargetNo':30},\
        # 'number_of_PostCellSynapses_per_PreCell':1,'targetingModelprePop':{'model':"segment groups and segments",'segmentGroupList':["axon_group"],'segmentGroupProbabilities':[1]},\
        #  'targetingModelpostPop':{'model':"segment groups and segments",'segmentGroupList':["Section_1","dend_1"],'segmentGroupProbabilities':[0.7,0.3]}})


    # 'maximalConnDistance' can also be included
    ##############


def chemical_connection_model(pair_id,projection_id,prePop,prePop_listIndex,prePopSize,preCellType,preNML2Type,pre_cell_positions,\
                                               postPop,postPop_listIndex,postPopSize,postCellType,postNML2Type,post_cell_positions,\
                                               connectivity_parameters,seed_number,parentDir=None):
    random.seed(seed_number)

    if parentDir != None:
       preCellTypeFile=parentDir+"/NeuroML2"+"/"+preCellType
       postCellTypeFile=parentDir+"/NeuroML2"+"/"+postCellType
    else:
       preCellTypeFile=preCellType
       postCellTypeFile=postCellType
    
    nonempty_projection=False
    gapJ_object_array=[]
    gap_counter=0
    #######
    if connectivity_parameters['targetingModelprePop']['model']=="segment groups and segments":
       pre_pop_target_segment_array=extract_morphology_information([preCellTypeFile],{preCellTypeFile:preNML2Type},\
                                                                                          ["segment groups",  \
                          connectivity_parameters['targetingModelprePop']['segmentGroupList']])

    if connectivity_parameters['targetingModelprePop']['model']=="segments and subsegments":
       pre_pop_target_segment_array=extract_morphology_information([preCellTypeFile],{preCellTypeFile:preNML2Type},\
                                                  ["segments",connectivity_parameters['targetingModelprePop']['segmentList']])

 
    if connectivity_parameters['targetingModelpostPop']['model']=="segment groups and segments":
       post_pop_target_segment_array=extract_morphology_information([postCellTypeFile],{postCellTypeFile:postNML2Type},\
                                  ["segment groups",connectivity_parameters['targetingModelpostPop']['segmentGroupList'] ] )

    if connectivity_parameters['targetingModelpostPop']['model']=="segments and subsegments":
       post_pop_target_segment_array=extract_morphology_information([postCellTypeFile],{postCellTypeFile:postNML2Type},\
            ["segments",connectivity_parameters['targetingModelpostPop']['segmentGroupList']])  
                                            
    proj = neuroml.Projection(id="proj%d"%projection_id,presynaptic_population=prePop,postsynaptic_population=postPop,synapse=connectivity_parameters['synapse'])
    
    synapse_name=connectivity_parameters['synapse']

    conn_count = 0
    #### for now,  no_of_Synapses_Onto_TargetCell is fixed for each presynaptic cell of a given population
    no_of_Synapses_Onto_TargetCell=connectivity_parameters['number_of_PostCellSynapses_per_PreCell']
    ######## connect pre and post populations according to a given probability and a number of synapses made by a single presynaptic cell onto a single postsynaptic cell
    if connectivity_parameters['chemicalConnModel']=="explicit_connection_probabilities":

       connection_probability=connectivity_parameters['connProb_from_PreCell_to_PostCell']   
                          
       for Pre_cell in range(0,prePopSize):

           

           if connectivity_parameters['targetingModelprePop']['model']=="segment groups and segments":
              pre_target_points=get_unique_target_points(pre_pop_target_segment_array,"segment groups and segments",\
                             [connectivity_parameters['targetingModelprePop']['segmentGroupList'],\
connectivity_parameters['targetingModelprePop']['segmentGroupProbabilities']],no_of_Synapses_Onto_TargetCell)

           if connectivity_parameters['targetingModelprePop']['model']=="segments and subsegments":
              pre_target_points=get_unique_target_points(pre_pop_target_segment_array,"segments and subsegments",\
 [connectivity_parameters['targetingModelprePop']['segmentList'],\
 connectivity_parameters['targetingModelprePop']['segmentProbabilities'],connectivity_parameters['targetingModelprePop']['fractionAlongANDsubsegProbabilities']],\
                                       no_of_Synapses_Onto_TargetCell)

           for Post_cell in range(0,postPopSize):
                          
               if random.random() < connection_probability:
                  
                  if connectivity_parameters['targetingModelpostPop']['model']=="segment groups and segments":

                      post_targeting_mode="segment groups and segments"

                      post_targeting_parameters=[connectivity_parameters['targetingModelpostPop']['segmentGroupList'],\
                      connectivity_parameters['targetingModelpostPop']['segmentGroupProbabilities']]

                  if connectivity_parameters['targetingModelpostPop']['model']=="segments and subsegments":

                     post_targeting_mode="segments and subsegments"

                     post_targeting_parameters=[connectivity_parameters['targetingModelpostPop']['segmentList'],\
 connectivity_parameters['targetingModelpostPop']['segmentProbabilities'],connectivity_parameters['targetingModelpostPop']['fractionAlongANDsubsegProbabilities']]

                  for pre_target_point in range(0,no_of_Synapses_Onto_TargetCell):
                      if 'maximalConnDistance' in connectivity_parameters:
                         x=0
                         while x==0:
                            post_target_points=get_unique_target_points(post_pop_target_segment_array,post_targeting_mode,post_targeting_parameters,1) 

                            if get_3D_connection_length(preCellTypeFile,postCellTypeFile,preNML2Type,postNML2Type,pre_cell_positions,post_cell_positions,Pre_cell,\
                               Post_cell,pre_target_points[pre_target_point,0],post_target_point[0,0],\
                               pre_target_points[pre_target_point,1],post_target_point[0,1]) <=connectivity_parameters['maximalConnDistance']:
                               x=1
                      else:
                         post_target_point=get_unique_target_points(post_pop_target_segment_array,post_targeting_mode,\
                                                                             post_targeting_parameters,1)

                      Pre_segment_id=pre_target_points[pre_target_point,0]
                      Post_segment_id=post_target_point[0,0]
                      Pre_fraction=pre_target_points[pre_target_point,1]
                      Post_fraction=post_target_point[0,1]
                      
                      conn =neuroml.Connection(id=conn_count,pre_cell="../%s/%d/%s"%(prePop,Pre_cell,preCellType),\
                            post_cell="../%s/%d/%s"%(postPop,Post_cell,postCellType),\
                            pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                            pre_fraction_along="%f"%Pre_fraction,post_fraction_along="%f"%Post_fraction)
                                            
		      nonempty_projection=True
                      proj.connections.append(conn)
		      conn_count+=1

 
    ##### projection in which each presynaptic cell contacts a fixed number of postsynaptic cells
    if connectivity_parameters['chemicalConnModel']=="fixedNo_of_PostTargetCells":  
                          
       for Pre_cell in range(0,prePopSize):

           if connectivity_parameters['chooseTargetMode']=='random':
  
              randomly_selected_target_cells=random.sample(range(postPopSize),int(round(connectivity_parameters['number_of_PostTargetCells_per_PreCell'])))
              
           ###### other chooseTargetModes can be added in the future


           if connectivity_parameters['targetingModelprePop']['model']=="segment groups and segments":
              pre_target_points=get_unique_target_points(pre_pop_target_segment_array,"segment groups and segments",\
                             [connectivity_parameters['targetingModelprePop']['segmentGroupList'],\
connectivity_parameters['targetingModelprePop']['segmentGroupProbabilities']],no_of_Synapses_Onto_TargetCell)

           if connectivity_parameters['targetingModelprePop']['model']=="segments and subsegments":
              pre_target_points=get_unique_target_points(pre_pop_target_segment_array,"segments and subsegments",\
 [connectivity_parameters['targetingModelprePop']['segmentList'],\
 connectivity_parameters['targetingModelprePop']['segmentProbabilities'],connectivity_parameters['targetingModelprePop']['fractionAlongANDsubsegProbabilities']],\
                                       no_of_Synapses_Onto_TargetCell)

           for Post_cell in randomly_selected_target_cells:
                          
               if connectivity_parameters['targetingModelpostPop']['model']=="segment groups and segments":

                  post_targeting_mode="segment groups and segments"

                  post_targeting_parameters=[connectivity_parameters['targetingModelpostPop']['segmentGroupList'],\
                  connectivity_parameters['targetingModelpostPop']['segmentGroupProbabilities']]

               if connectivity_parameters['targetingModelpostPop']['model']=="segments and subsegments":

                  post_targeting_mode="segments and subsegments"

                  post_targeting_parameters=[connectivity_parameters['targetingModelpostPop']['segmentList'],\
 connectivity_parameters['targetingModelpostPop']['segmentProbabilities'],connectivity_parameters['targetingModelpostPop']['fractionAlongANDsubsegProbabilities']]

               for pre_target_point in range(0,no_of_Synapses_Onto_TargetCell):
                   if 'maximalConnDistance' in connectivity_parameters:
                      x=0
                      while x==0:
                         post_target_points=get_unique_target_points(post_pop_target_segment_array,post_targeting_mode,post_targeting_parameters,1) 

                         if get_3D_connection_length(preCellTypeFile,postCellTypeFile,preNML2Type,postNML2Type,pre_cell_positions,post_cell_positions,Pre_cell,\
                            Post_cell,pre_target_points[pre_target_point,0],post_target_point[0,0],\
                            pre_target_points[pre_target_point,1],post_target_point[0,1]) <=connectivity_parameters['maximalConnDistance']:
                            x=1
                   else:
                      post_target_point=get_unique_target_points(post_pop_target_segment_array,post_targeting_mode,\
                                                                             post_targeting_parameters,1)

                   Pre_segment_id=pre_target_points[pre_target_point,0]
                   Post_segment_id=post_target_point[0,0]
                   Pre_fraction=pre_target_points[pre_target_point,1]
                   Post_fraction=post_target_point[0,1]
                      
                   conn =neuroml.Connection(id=conn_count,pre_cell="../%s/%d/%s"%(prePop,Pre_cell,preCellType),\
                         post_cell="../%s/%d/%s"%(postPop,Post_cell,postCellType),\
                         pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                         pre_fraction_along="%f"%Pre_fraction,post_fraction_along="%f"%Post_fraction)
                                            
		   nonempty_projection=True
                   proj.connections.append(conn)
		   conn_count+=1
   
    ############ projection in which each presynaptic cell of a given presynaptic population has a variable number of postsynaptic targets according to a given statistical distribution
    if connectivity_parameters['chemicalConnModel']=="variableNo_of_PostTargetCells":  
                          
       for Pre_cell in range(0,prePopSize):

           if connectivity_parameters['targetNoModel']['modelType']=='binomial':

              no_of_targets=np.random.binomial(connectivity_parameters['targetNoModel']['maxTargetNo'],\
                                 connectivity_parameters['targetNoModel']['average']/connectivity_parameters['targetNoModel']['maxTargetNo'])


           ####### other distributions can be added in the future
              
           if connectivity_parameters['chooseTargetMode']=='random':
  
              randomly_selected_target_cells=random.sample(range(postPopSize),int(round(no_of_targets)))
              
           ###### other chooseTargetModes can be added in the future


           if connectivity_parameters['targetingModelprePop']['model']=="segment groups and segments":
              pre_target_points=get_unique_target_points(pre_pop_target_segment_array,"segment groups and segments",\
                             [connectivity_parameters['targetingModelprePop']['segmentGroupList'],\
connectivity_parameters['targetingModelprePop']['segmentGroupProbabilities']],no_of_Synapses_Onto_TargetCell)

           if connectivity_parameters['targetingModelprePop']['model']=="segments and subsegments":
              pre_target_points=get_unique_target_points(pre_pop_target_segment_array,"segments and subsegments",\
 [connectivity_parameters['targetingModelprePop']['segmentList'],\
 connectivity_parameters['targetingModelprePop']['segmentProbabilities'],connectivity_parameters['targetingModelprePop']['fractionAlongANDsubsegProbabilities']],\
                                       no_of_Synapses_Onto_TargetCell)

           for Post_cell in randomly_selected_target_cells:
                          
               if connectivity_parameters['targetingModelpostPop']['model']=="segment groups and segments":

                  post_targeting_mode="segment groups and segments"

                  post_targeting_parameters=[connectivity_parameters['targetingModelpostPop']['segmentGroupList'],\
                  connectivity_parameters['targetingModelpostPop']['segmentGroupProbabilities']]

               if connectivity_parameters['targetingModelpostPop']['model']=="segments and subsegments":

                  post_targeting_mode="segments and subsegments"

                  post_targeting_parameters=[connectivity_parameters['targetingModelpostPop']['segmentList'],\
 connectivity_parameters['targetingModelpostPop']['segmentProbabilities'],connectivity_parameters['targetingModelpostPop']['fractionAlongANDsubsegProbabilities']]

               for pre_target_point in range(0,no_of_Synapses_Onto_TargetCell):
                   if 'maximalConnDistance' in connectivity_parameters:
                      x=0
                      while x==0:
                         post_target_points=get_unique_target_points(post_pop_target_segment_array,post_targeting_mode,post_targeting_parameters,1) 

                         if get_3D_connection_length(preCellTypeFile,postCellTypeFile,preNML2Type,postNML2Type,pre_cell_positions,post_cell_positions,Pre_cell,\
                            Post_cell,pre_target_points[pre_target_point,0],post_target_point[0,0],\
                            pre_target_points[pre_target_point,1],post_target_point[0,1]) <=connectivity_parameters['maximalConnDistance']:
                            x=1
                   else:
                      post_target_point=get_unique_target_points(post_pop_target_segment_array,post_targeting_mode,\
                                                                             post_targeting_parameters,1)

                   Pre_segment_id=pre_target_points[pre_target_point,0]
                   Post_segment_id=post_target_point[0,0]
                   Pre_fraction=pre_target_points[pre_target_point,1]
                   Post_fraction=post_target_point[0,1]
                      
                   conn =neuroml.Connection(id=conn_count,pre_cell="../%s/%d/%s"%(prePop,Pre_cell,preCellType),\
                         post_cell="../%s/%d/%s"%(postPop,Post_cell,postCellType),\
                         pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                         pre_fraction_along="%f"%Pre_fraction,post_fraction_along="%f"%Post_fraction)
                                            
		   nonempty_projection=True
                   proj.connections.append(conn)
		   conn_count+=1
   






    return proj, nonempty_projection,gapJ_object_array,synapse_name




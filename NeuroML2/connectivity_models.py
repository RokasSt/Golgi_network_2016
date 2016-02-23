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

from methods import *




def Vervaeke_2012_AND_explicit_conn_prob_model(pair,initial_projection_count,gap_count,prePop,prePop_listIndex,prePopSize,postPop,postPop_listIndex,postPopSize,\
                                               cell_array,connectivity_information,cell_position_array):
    nonempty_projection=False
    gapJ_object_array=[]
    gap_counter=gap_count
    initial_projection_counter=initial_projection_count
    #######
    if connectivity_information['populationPairs'][pair]['targetingModelprePop']['model']=="segment groups and segments":
       pre_pop_target_segment_array=extract_morphology_information([cell_array[prePop_listIndex]['cellType']],\
                                                                                          ["segment groups",  \
connectivity_information['populationPairs'][pair]['targetingModelprePop']['segmentGroupList']])

    if connectivity_information['populationPairs'][pair]['targetingModelprePop']['model']=="segments and subsegments":
       pre_pop_target_segment_array=extract_morphology_information([cell_array[prePop_listIndex]['cellType']],\
                                                  ["segments",connectivity_information['populationPairs'][pair]['targetingModelprePop']['segmentList']])

    if connectivity_information['populationPairs'][pair]['targetingModelpostPop']['model']=="segment groups and segments":
       post_pop_target_segment_array=extract_morphology_information([cell_array[postPop_listIndex]['cellType']  ],\
                                  ["segment groups",connectivity_information['populationPairs'][pair]['targetingModelpostPop']['segmentGroupList'] ] )

    if connectivity_information['populationPairs'][pair]['targetingModelpostPop']['model']=="segments and subsegments":
       post_pop_target_segment_array=extract_morphology_information([cell_array[postPop_listIndex]['cellType']],\
            ["segments",connectivity_information['populationPairs'][pair]['targetingModelpostPop']['segmentGroupList']])  
                                            
    proj = neuroml.ElectricalProjection(id="proj%d"%initial_projection_counter,\
		                presynaptic_population=prePop,\ 
		                postsynaptic_population=postPop)
    
    
    conn_count = 0
    pre_cell_positions=cell_position_array[prePop]
    post_cell_positions=cell_position_array[postPop]
                                                                              
    if connectivity_information['populationPairs'][pair]['gapJunctionModel']=="constant number of GJ contacts per pair":
       no_of_GJcon_per_pair=connectivity_information['populationPairs'][pair]['numberGJ']
    if connectivity_information['populationPairs'][pair]['gapJunctionModel']=="variable number of GJ contacts per pair":
       if connectivity_information['populationPairs'][pair]['distribution']=="binomial":
          no_of_GJcon_per_pair=np.random.binomial(connectivity_information['populationPairs'][pair]['maxNoGJs'],\
          connectivity_information['populationPairs'][pair]['averageNoGJs']/connectivity_information['populationPairs'][pair]['maxNoGJs'])
       #### other models can be added in the future

    conductance_scaling=1

    if 'testingConductanceScale' in connectivity_information['populationPairs'][pair]:
       conductance_scaling=connectivity_information['populationPairs'][pair]['testingConductanceScale']
 
    if connectivity_information['populationPairs'][pair]['conductanceModel']=="constant":
       conductance_value=connectivity_information['populationPairs'][pair]['conductanceValue']
       conductance_units=connectivity_information[2][pair]['units']
       gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter,conductance="%f%s"%(conductance_value*conductance_scaling,conductance_units)) 
       gap_id_per_pair="gap_junction%d"%gap_counter        
       gapJ_object_array.append(gap_junction)
       gap_counter+=1


    spatial_scale=1
    if 'spatialScale' in connectivity_information['populationPairs'][pair]:
       spatial_scale=connectivity_information['populationPairs'][pair]['spatialScale']
                                    
    for Pre_cell in range(0,prePopSize):
        for Post_cell in range(0,postPopSize):
                       
            if connectivity_information['populationPairs'][pair]['connModel']=="explicit_connection_probabilities":
               connection_probability=connectivity_information['populationPairs'][pair]['connProbabilities']
                          
            if connectivity_information['populationPairs'][pair]['connModel']=="Vervaeke_2012_based":
               distance_between_cells=distance(pre_cell_positions[Pre_cell],post_cell_positions[Post_cell])/spatial_scale
               connection_probability=connection_probability_vervaeke_2010(distance_between_cells)
                          
            if random.random() < connection_probability:

               if connectivity_information['populationPairs'][pair]['targetingModelprePop']['model']=="segment groups and segments":
                  pre_target_points=get_unique_target_points(pre_pop_target_segment_array,"segment groups and segments",\
                             [connectivity_information['populationPairs'][pair]['targetingModelprePop']['segmentGroupList'],\
connectivity_information['populationPairs'][pair]['targetingModelprePop']['segmentGroupProbabilities']],no_of_GJcon_per_pair)

               if connectivity_information['populationPairs'][pair]['targetingModelprePop']['model']=="segments and subsegments":
                  pre_target_points=get_unique_target_points(pre_pop_target_segment_array,"segments and subsegments",\
 [connectivity_information['populationPairs'][pair]['targetingModelprePop']['segmentList'],\
 connectivity_information['populationPairs'][pair]['targetingModelprePop']['segmentProbabilities'],[connectivity_information['populationPairs'][pair]['targetingModelprePop']['fractionAlongANDsubsegProbabilities']],no_of_GJcon_per_pair)
       
               if connectivity_information['populationPairs'][pair]['targetingModelpostPop']['model']=="segment groups and segments":

                  post_targeting_mode="segment groups and segments"

                  post_targeting_parameters=[connectivity_information['populationPairs'][pair]['targetingModelpostPop']['segmentGroupList'],\
connectivity_information['populationPairs'][pair]['targetingModelpostPop']['segmentGroupProbabilities']]

               if connectivity_information['populationPairs'][pair]['targetingModelpostPop']['model']=="segments and subsegments":

                  post_targeting_mode="segments and subsegments"

                  post_targeting_parameters=[connectivity_information['populationPairs'][pair]['targetingModelpostPop']['segmentList'],\
 connectivity_information['populationPairs'][pair]['targetingModelpostPop']['segmentProbabilities'],[connectivity_information['populationPairs'][pair]['targetingModelpostPop']['fractionAlongANDsubsegProbabilities']]

                  for pre_target_point in range(0,len(pre_target_points)):
                      if 'maximalConnDistance' in connectivity_information['populationPairs'][pair]:
                         x=0
                         while x==0:
                             post_target_point=get_unique_target_points(post_pop_target_segment_array,post_targeting_mode,post_targeting_parameters,1) 
                             if get_3D_connection_length(cell_names,cell_position_array,pre_pop_index,post_pop_index,Pre_cell,\
                                Post_cell,pre_target_points[pre_target_point,0],post_target_point[0,0],\
                                pre_target_points[pre_target_point,1],post_target_point[0,1]) <=connectivity_information['populationPairs'][pair]['maximalConnDistance']:
                                x=1
                      else:
                         post_target_point=get_unique_target_points(post_pop_target_segment_array,post_targeting_mode,\
                                                                             post_targeting_parameters,1)

                      Pre_segment_id=pre_target_points[pre_target_point,0]
                      Post_segment_id=post_target_point[0,0]
                      Pre_fraction=pre_target_points[pre_target_point,1]
                      Post_fraction=post_target_point[0,1]

                      if connectivity_information['populationPairs'][pair]['conductanceModel']=="variable":
                         if string.lower(connectivity_information['populationPairs'][pair]['distribution'])=="gaussian":
                            conductance=random.gauss(connectivity_information['populationPairs'][pair]['averageConductance'],\
                     connectivity_information['populationPairs'][pair]['stdDev'])
                            conductanceUnits=connectivity_information['populationPairs'][pair]['units']
                            gap_junction = neuroml.GapJunction(id="gap_junction%d"%gap_counter, conductance="%f%s"%(conductance*conductance_scaling,conductanceUnits) )
                            gapJ_object_array.append(gap_junction)        
		            gap_counter+=1
                         #other options can be added such as gamma distribution
                      
                      conn =neuroml.ElectricalConnectionInstance(id=conn_count,\
pre_cell="../%s/%d/%s"%(prePop,Pre_cell,cell_array[prePop_listIndex]['cellType']),\
post_cell="../%s/%d/%s"%(postPop,Post_cell,cell_array[postPop_listIndex]['cellType']),synapse=gap_junction.id,\
                                                             pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                                                             pre_fraction_along="%f"%Pre_fraction,post_fraction_along="%f"%Post_fraction)
                                            
		      nonempty_projection=True
                      proj.electrical_connection_instances.append(conn)
		      conn_count+=1

    

    return proj, nonempty_projection, gap_counter,gapJ_object_array



def Vervaeke_2010_model(pair,initial_projection_count,gap_count,prePop,prePop_listIndex,postPop,postPop_listIndex,cell_array,\
                                                                         connectivity_information,cell_position_array):
    nonempty_projection=False
    gapJ_object_array=[]
    gap_counter=gap_count
    initial_projection_counter=initial_projection_count
    #######
    if 'prePoptargetGroup' in connectivity_information['populationPairs'][pair]:
       pre_pop_target_segment_array=extract_morphology_information([cell_array[prePop_listIndex]['cellType']],\
                                                                                          ["segment groups",  \
connectivity_information['populationPairs'][pair]['prePoptargetGroup']['segmentGroupList']])

    if 'postPoptargetGroup' in connectivity_information['populationPairs'][pair]:
       post_pop_target_segment_array=extract_morphology_information([cell_array[postPop_listIndex]['cellType']  ],\
                                  ["segment groups",connectivity_information['populationPairs'][pair]['postPoptargetGroup']['segmentGroupList'] ] )

                                            
    proj = neuroml.ElectricalProjection(id="proj%d"%initial_projection_counter,\
		                presynaptic_population=prePop,\ 
		                postsynaptic_population=postPop)
    
    conn_count = 0
    pre_cell_positions=cell_position_array[prePop]
    post_cell_positions=cell_position_array[postPop]
                                                                              
    conductance_scaling=1
                                                        
    conductance_array=[]
    conductance_array_spatial_scale1=[]
    make_conductance_array_no_spatial_scale=False

              
    if 'testingConductanceScale' in connectivity_information['populationPairs'][pair]:
       conductance_scaling=connectivity_information['populationPairs'][pair]['testingConductanceScale']
 

    spatial_scale=1
    if 'spatialScale' in connectivity_information['populationPairs'][pair]:
       spatial_scale=connectivity_information['populationPairs'][pair]['spatialScale']

    if connectivity_information['populationPairs'][pair]['normalizeConductances']:
                                                        
       if spatial_scale != 1:
                     
          make_conductance_array_no_spatial_scale=True
                                 
    for Pre_cell in range(0,prePopSize):
        for Post_cell in range(0,postPopSize):
                                                        
            distance_between_cells=distance(pre_cell_positions[Pre_cell],post_cell_positions[Post_cell])/spatial_scale

            if connectivity_information['populationPairs'][pair]['normalizeConductances']:
                                                        
               if make_conductance_array_no_spatial_scale:
                  distance_between_cells_spatial_scale1=spatial_scale*distance_between_cells
                             
                                                        
            if random.random() <connection_probability_vervaeke_2010(distance_between_cells):

               conductanceValue=synaptic_weight_vervaeke_2010(distance_between_cells)
               conductance_array.append(conductanceValue)
                                                        
               if make_conductance_array_no_spatial_scale:
                  conductanceValueN=synaptic_weight_vervaeke_2010(distance_between_cells_spatial_scale1)
                  conductance_array_spatial_scale1.append(conductanceValueN)
                                                        
               if 'prePoptargetGroup' in connectivity_information['populationPairs'][pair]:
                  pre_target_points=get_unique_target_points(pre_pop_target_segment_array,"segment groups and segments",\
                             [connectivity_information['populationPairs'][pair]['targetingModelprePop']['segmentGroupList'],\
connectivity_information['populationPairs'][pair]['targetingModelprePop']['segmentGroupProbabilities']],1)

       
               if 'postPoptargetGroup' in connectivity_information['populationPairs'][pair]:

                  post_targeting_mode="segment groups and segments"

                  post_targeting_parameters=[connectivity_information['populationPairs'][pair]['targetingModelpostPop']['segmentGroupList'],\
connectivity_information['populationPairs'][pair]['targetingModelpostPop']['segmentGroupProbabilities']]

                          
               if 'maximalConnDistance' in connectivity_information['populationPairs'][pair]:
                  x=0
                  while x==0:
                     post_target_point=get_unique_target_points(post_pop_target_segment_array,post_targeting_mode,post_targeting_parameters,1) 
                     if get_3D_connection_length(cell_names,cell_position_array,pre_pop_index,post_pop_index,Pre_cell,\
                        Post_cell,pre_target_points[0,0],post_target_point[0,0],\
                        pre_target_points[0,1],post_target_point[0,1]) <=connectivity_information['populationPairs'][pair]['maximalConnDistance']:
                        x=1
               else:
                 post_target_point=get_unique_target_points(post_pop_target_segment_array,post_targeting_mode,\
                                                                             post_targeting_parameters,1)

               Pre_segment_id=pre_target_points[pre_target_point,0]
               Post_segment_id=post_target_point[0,0]
               Pre_fraction=pre_target_points[pre_target_point,1]
               Post_fraction=post_target_point[0,1]

                          
               conn =neuroml.ElectricalConnectionInstance(id=conn_count,\
pre_cell="../%s/%d/%s"%(prePop,Pre_cell,cell_array[prePop_listIndex]['cellType']),\
post_cell="../%s/%d/%s"%(postPop,Post_cell,cell_array[postPop_listIndex]['cellType']),synapse="gap_junction%d"%(pair,gap_counter),\
                                                             pre_segment="%d"%Pre_segment_id,post_segment="%d"%Post_segment_id,\
                                                             pre_fraction_along="%f"%Pre_fraction,post_fraction_along="%f"%Post_fraction)
               gap_counter+=1                         
	       nonempty_projection=True

               proj.electrical_connection_instances.append(conn)
	       conn_count+=1
    ########
    conductanceUnits=connectivity_information['populationPairs'][pair]['units']
    if len(conductance_array)==gap_counter:
       for GJ in range(0,len(conductance_array)):
           if make_conductance_array_no_spatial_scale:
              conductanceValue=conductance_array[GJ]*(sum(conductance_array_spatial_scale1)/sum(conductance_array))
              gap_junction = neuroml.GapJunction(id="gap_junction%d%d"%(pair,GJ), conductance="%f%s"%(conductanceValue*conductance_scaling,conductanceUnits) )
              gapJ_object_array.append(gap_junction) 
           else:
              conductanceValue=conductance_array[GJ]
              gap_junction = neuroml.GapJunction(id="gap_junction%d%d"%(pair,GJ), conductance="%f%s"%(conductanceValue*conductance_scaling,conductanceUnits) )
              gapJ_object_array.append(gap_junction) 
                           


    return proj, nonempty_projection, gap_counter,gapJ_object_array

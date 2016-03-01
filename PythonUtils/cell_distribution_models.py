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





def density_model(popIndex=None,location_parameters,golgi_pop_object,cell_position_array=None,cell_array=None,cell_diameter_array=None,seed_number):
    random.seed(seed_number)
    densityFilePath=location_parameters['densityFilePath']
    X_array,Y_array,density_values=load_density_data(densityFilePath)
    dim_X_array=np.shape(X_array)
    dim_Y_array=np.shape(Y_array)
    ## assume meshgrid
    if dim_X_array==dim_Y_array:
       ## assume that data is not normalized and distribute cells on a specific region on a density sheet
       X_max=np.nanmax(X_array)
       Y_max=np.nanmax(Y_array)
       X_vector=X_array[0]
       Y_vector=Y_array[0]
       left_x_index=None
       right_x_index=None
       low_y_index=None
       high_y_index=None

       left_x_found=False
       right_x_found=False
       low_y_found=False
       high_y_found=False
       for X_value in range(0,len(X_vector)):
           if left_x_found==False:
              if X_vector[X_value] > location_parameters['dim1CoordinateVector'][0]:
                 left_x_index=X_value
                 left_x_found=True
           if right_x_found==False:
              if X_vector[X_value] > location_parameters['dim1CoordinateVector'][1]:
                 right_x_index=X_value-1
                 right_x_found=True
       for Y_value in range(0,len(Y_vector)):
           if low_y_found==False: 
              if Y_vector[Y_value] > location_parameters['dim2CoordinateVector'][0]:
                 low_y_index=Y_value
                 low_y_found=True
           if high_y_found==False:
              if Y_vector[Y_value] > location_parameters['dim2CoordinateVector'][1]:
                 high_y_index=Y_value-1
                 high_y_found=True
       if left_x_found and right_x_found and low_y_found and high_y_found:
          X_index_array=range(left_x_index,right_x_index+1)
          Y_index_array=range(low_y_index,high_y_index+1)
          ##### assume that discrete density sheet is in mmm3. thus convert cell_diameter and dim3 to mm:
          dim3Boundary=location_parameters['dim3Boundary']/1000
          ### find density points that fall within a region specified by 'dim1CoordinateVector' and 'dim2CoordinateVector'
                     
                     
          base_area=location_parameters['canonicalVolumeBaseArea']
          canonical_volume=math.pi*((base_area/2)**2)*dim3Boundary
          
          dim_dict={'x':0,'y':1,'z':2}
          
          pop_position_array=np.zeros([0,3])
                      
          for X_index in range(0,len(X_index_array)):
              for Y_index in range(0,len(Y_index_array)):
                  density_value=density_values[X_index_array[X_index],Y_index_array[Y_index]]
                  no_of_cells_per_density_point=density_value*canonical_volume
                  total_no_of_cells=total_no_of_cells+no_of_cells_per_density_point
                  X_square_centre=X_array[X_index_array[X_index],Y_index_array[Y_index]]
                  Y_square_centre=Y_array[X_index_array[X_index],Y_index_array[Y_index]]
                  X_left_corner=X_square_centre-(math.sqrt(base_area)/2)
                  Y_left_corner=Y_square_centre-(math.sqrt(base_area)/2)

                  if location_parameters['distanceModel']=="minimal_distance":
                     
                              
                  if location_parameters['distanceModel']=="random_no_overlap":
                     dim_dict_max_values={}
                     dim_dict_max_values['x_dim']=sqrt(base_area)
                     dim_dict_max_values['y_dim']=sqrt(base_area)
                     dim_dict_max_values['z_dim']=dim3Boundary
                     dim_dict_offsets={'x_dim_offset':X_left_corner,'y_dim_offset':Y_left_corner,'z_dim_offset':0}
                     dim_dict_mappings={}
                     dim_dict_mappings['dim1']=location_parameters['planeDimensions']['dim1']
                     dim_dict_mappings['dim2']=location_parameters['planeDimensions']['dim2']
                     dim_dict_mappings['dim3']=location_parameters['planeDimensions']['dim3']
                     
                     pop_position_array_internal ,golgi_pop_object=random_no_overlap(cell_position_array,cell_array,cell_diameter_array,popIndex,total_no_of_cells,\
                     golgi_pop_object,dim_dict_max_values,dim_dict_mappings,dim_dict_offsets,seed_number)
                     
                     pop_position_array=np.vstack((pop_position_array,pop_position_array_internal))
                     

                  if location_parameters['distanceModel']=="random":
                     
                     for cell in range(0,no_of_cells_per_density_point):
	                 Golgi_cell=neuroml.Instance(id="%d"%cell)
	                 golgi_pop_object.instances.append(Golgi_cell)
	                 X=random.random()
	                 Y=random.random()
	                 Z=random.random()
	                 cell_position=np.zeros([0,3])         
	                
                         cell_position[0,dim_dict[location_parameters['planeDimensions']['dim1']]]=X_left_corner+sqrt(base_area)*X
                                       
                         cell_position[0,dim_dict[location_parameters['planeDimensions']['dim2']]]=Y_left_corner+sqrt(base_area)*Y

                         cell_position[0,dim_dict[location_parameters['planeDimensions']['dim3']]]=dim3Boundary*Z
                         
                         pop_position_array=np.vstack((pop_position_array,cell_position))

                         Golgi_cell.location=neuroml.Location(x=X_left_corner+sqrt(base_area)*X, y=Y_left_corner+sqrt(base_area)*Y, z=dim3Boundary*Z)

                         print pop_position_array[cell,0], pop_position_array[cell,1], pop_position_array[cell,2]
                                                                                                                          
    ### override any specified value of population Size
                                                                                                                          
    return pop_position_array, total_no_of_cells,golgi_pop_object



def random_minimal_distance(cell_array_pop,location_array,popIndex,popSize,golgi_pop_object,x_dim,y_dim,z_dim,seed_number):
    random.seed(seed_number)
    pop_position_array[ cell_array[cell_population]['popID'] ]=np.zeros([cell_array_pop['size'],3])
    for cell in range(0,popSize):
	Golgi_cell=neuroml.Instance(id="%d"%cell)
	golgi_pop_object.instances.append(Golgi_cell)
        if popIndex==0 and cell==0:
            X=random.random()
            Y=random.random()
            Z=random.random()
            cell_position_array[cell_array[popIndex]['popID']][cell,0]=x_dim*X
            cell_position_array[cell_array[popIndex]['popID']][cell,1]=y_dim*Y
            cell_position_array[cell_array[popIndex]['popID']][cell,2]=z_dim*Z
            Golgi_cell.location=neuroml.Location(x=x_dim*X, y=y_dim*Y, z=z_dim*Z)
            print cell_position_array[cell_array[popIndex]['popID']][cell,0], cell_position_array[cell_array[popIndex]['popID']][cell,1],\
 cell_position_array[cell_array[popIndex]['popID']][cell,2]
        else:
            x=0
            while x==0:
                overlap_counter=0
                X=(random.random())*x_dim
	        Y=(random.random())*y_dim
	        Z=(random.random())*z_dim
                for cell_pop_x in range(0,len(cell_array)):
                    pop_cell_positions=cell_position_array[cell_array[cell_pop_x]['popID']]
                    for cell_x in range(0,cell_array[cell_pop_x]['size']):
                        if cell_position_array[cell_array[cell_pop_x]['popID']][cell_x,0]+cell_position_array[cell_array[cell_pop_x]['popID']][cell_x,1]+cell_position_array[cell_array[cell_pop_x]['popID']][cell_x,2] >0:
                           if string.lower(location_array['metricMode'])=="uniform":
                              if distance([X,Y,Z],cell_position_array[cell_array[cell_pop_x]['popID']][cell_x]) < location_array['globalMetric']:
                                 overlap_counter+=1
                           #if string.lower(location_array['metricMode'])=="cell group specific": might be added in the future
                                              
                if overlap_counter==0:
                   cell_position_array[cell_array[cell_pop]['popID']][cell,0]=X
                   cell_position_array[cell_array[cell_pop]['popID']][cell,1]=Y
                   cell_position_array[cell_array[cell_pop]['popID']][cell,2]=Z
                   Golgi_cell.location=neuroml.Location(x=X, y=Y, z=Z)
                               
                   print cell_position_array[cell_array[cell_pop]['popID']][cell,0], cell_position_array[cell_array[cell_pop]['popID']][cell,1], cell_position_array[cell_array[cell_pop]['popID']][cell,2]
                   x=1


    return pop_position_array,golgi_pop_object


def random_no_overlap(cell_position_array,cell_array,cell_diameter_array,popIndex,popSize=None,golgi_pop_object,dim_dict_max_values,dim_dict_mappings=None,\
                      dim_dict_offsets={'x_dim_offset':0,'y_dim_offset':0,'z_dim_offset':0},seed_number):

    random.seed(seed_number)
    cell_diameter=cell_diameter_array[cell_array[popIndex]['popID']]
    if popSize ==None:
       popSize=cell_array[popIndex]['size']
       pop_position_array=np.zeros([cell_array[popIndex]['size'],3])
    else:
       pop_position_array=np.zeros([popSize,3])
    for cell in range(0,popSize):
	Golgi_cell=neuroml.Instance(id="%d"%cell)
	golgi_pop_object.instances.append(Golgi_cell)
	if popIndex==0 and cell==0:
           X=random.random()
	   Y=random.random()
	   Z=random.random()
	   Xcoordinate=dim_dict_offsets['x_dim_offset']+dim_dict_max_values['x_dim']*X
           Ycoordinate=dim_dict_offsets['y_dim_offset']+dim_dict_max_values['y_dim']*Y
           Zcoordinate=dim_dict_offsets['z_dim_offset']+dim_dict_max_values['z_dim']*Z
	   if dim_dict_mappings != None:
              pop_position_array[cell,dim_dict_mappings['dim1']]=Xcoordinate
              pop_position_array[cell,dim_dict_mappings['dim2']]=Ycoordinate
              pop_position_array[cell,dim_dict_mappings['dim2']]=Zcoordinate
           else:
             pop_position_array[cell,0]=Xcoordinate
             pop_position_array[cell,1]=Ycoordinate
             pop_position_array[cell,2]=Zcoordinate
           Golgi_cell.location=neuroml.Location(x=Xcoordinate, y=Ycoordinate,z=Zcoordinate)
           print pop_position_array[cell,0], pop_position_array[cell,1],pop_position_array[cell,2]
           
        else:
           x=0
           while x==0:
              overlap_counter=0
              X=random.random()
	      Y=random.random()
	      Z=random.random()
	      Xcoordinate=dim_dict_offsets['x_dim_offset']+dim_dict_max_values['x_dim']*X
              Ycoordinate=dim_dict_offsets['y_dim_offset']+dim_dict_max_values['y_dim']*Y
              Zcoordinate=dim_dict_offsets['z_dim_offset']+dim_dict_max_values['z_dim']*Z
              for cell_pop_x in range(0,len(cell_array)):
                  pop_cell_positions=cell_position_array[cell_array[cell_pop_x]['popID']]
                  for cell_x in range(0,len(pop_cell_positions):
                      if pop_cell_positions[cell_x,0]+pop_cell_positions[cell_x,1]+pop_cell_positions[cell_x,2] >0:
                         if distance([Xcoordinate,Ycoordinate,Zcoordinate],pop_cell_positions[cell_x]) < (cell_diameter_array[cell_array[popIndex]['popID']]+cell_diameter_array[cell_array[cell_pop_x]['popID']])/2:
                            overlap_counter+=1
                            
              if overlap_counter==0:
                  
                 if dim_dict_mappings != None:
                    pop_position_array[cell,dim_dict_mappings['dim1']]=Xcoordinate
                    pop_position_array[cell,dim_dict_mappings['dim2']]=Ycoordinate
                    pop_position_array[cell,dim_dict_mappings['dim2']]=Zcoordinate
                 else:
                    pop_position_array[cell,0]=Xcoordinate
                    pop_position_array[cell,1]=Ycoordinate
                    pop_position_array[cell,2]=Zcoordinate
                    
                 Golgi_cell.location=neuroml.Location(x=Xcoordinate, y=Ycoordinate, z=Zcoordinate)
                               
                 print pop_position_array[cell,0], cell_position_array[cell,1], cell_position_array[cell,2]
                 x=1   


    return pop_position_array,golgi_pop_object

                     

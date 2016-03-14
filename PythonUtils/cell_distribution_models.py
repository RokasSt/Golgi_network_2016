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





def density_model(location_parameters,cell_position_array,cellType,seed_number,popIndex=None,cell_array=None,cell_diameter_array=None):
    random.seed(seed_number)
    densityFilePath=location_parameters['densityFilePath']
    X_array,Y_array,density_values=load_density_data(densityFilePath)
    dim_X_array=np.shape(X_array)
    print dim_X_array
    dim_Y_array=np.shape(Y_array)
    print dim_Y_array
    print np.shape(density_values)
    ## assume meshgrid
    if dim_X_array==dim_Y_array:
       ## assume that data is not normalized and distribute cells on a specific region on a density sheet
       X_max=np.nanmax(X_array)
       Y_max=np.nanmax(Y_array)
       X_vector=X_array[0]
       Y_vector=Y_array[0:,0]
       print np.nanmax(X_vector)
       print np.nanmax(Y_vector)
       print X_vector
       print Y_vector
       print len(X_vector)
       print len(Y_vector)
       print np.nanmax(density_values)
       print np.nanmin(density_values)
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
                 print("found left x boundary %d"%left_x_index)
           if right_x_found==False:
              if X_vector[X_value] > location_parameters['dim1CoordinateVector'][1]:
                 right_x_index=X_value-1
                 right_x_found=True
                 print("found right x boundary %d"%right_x_index)
       for Y_value in range(0,len(Y_vector)):
           if low_y_found==False: 
              if Y_vector[Y_value] > location_parameters['dim2CoordinateVector'][0]:
                 low_y_index=Y_value
                 low_y_found=True
                 print("found low y boundary %d"%low_y_index)
           if high_y_found==False:
              if Y_vector[Y_value] > location_parameters['dim2CoordinateVector'][1]:
                 high_y_index=Y_value-1
                 high_y_found=True
                 print("found high y boundary %d"%high_y_index)
       if left_x_found and right_x_found and low_y_found and high_y_found:
          X_index_array=range(left_x_index,right_x_index+1)
          Y_index_array=range(low_y_index,high_y_index+1)
          print X_index_array
          print Y_index_array
          a="Region was found"
          ##### assume that the discrete density sheet is in mmm3. thus convert dim3 to mm:
          dim3Boundary=float(location_parameters['dim3Boundary'])/1000
        

          base_area=float(location_parameters['canonicalVolumeBaseAreainMicrons'])/(10**6)

          canonical_volume=base_area*dim3Boundary


          base_area_microns=float(location_parameters['canonicalVolumeBaseAreainMicrons'])
          dim3Boundary_microns=float(location_parameters['dim3Boundary'])

          dim_dict={'x':0,'y':1,'z':2}
          
          pop_position_array=np.zeros([0,3])
 
          total_no_of_cells=0       
          cell_no_per_voxel_array=np.zeros([len(Y_index_array),len(X_index_array)])

          for Y_index in range(0,len(Y_index_array)):
              for X_index in range(0,len(X_index_array)):

                  density_value=density_values[Y_index_array[Y_index],X_index_array[X_index]]
          
 
                  if int(round(density_value*canonical_volume)) >=1:

                     no_of_cells_per_density_point=int(round(density_value*canonical_volume))


                  else:
                     if int(round(density_value*canonical_volume,1))==0.1 and density_value*canonical_volume < 0.1:
                     
                        voxel_probability=density_value*canonical_volume*10

                     else:
 
                        voxel_probability=density_value*canonical_volume

                     if voxel_probability > random.random():

                        no_of_cells_per_density_point=1

                     else:
                   
                        no_of_cells_per_density_point=0

                  cell_no_per_voxel_array[Y_index,X_index]=no_of_cells_per_density_point

                  total_no_of_cells=total_no_of_cells+no_of_cells_per_density_point

          golgi_pop_object = neuroml.Population(id=location_parameters['popID'], size =total_no_of_cells, type="populationList", component=cellType)
          cell_counter=0
          for Y_index in range(0,len(Y_index_array)):
              for X_index in range(0,len(X_index_array)):
                  X_square_centre=X_array[Y_index_array[Y_index], X_index_array[X_index]]
                  Y_square_centre=Y_array[Y_index_array[Y_index], X_index_array[X_index]]
                  no_of_cells_per_density_point=int(round(cell_no_per_voxel_array[Y_index,X_index]))
                  X_left_corner=X_square_centre-(math.sqrt(base_area_microns)/2)
                  Y_left_corner=Y_square_centre-(math.sqrt(base_area_microns)/2)
 
                  if no_of_cells_per_density_point !=0:

                     if location_parameters['distanceModel']=="random_minimal_distance":
                        minimal_distance=location_parameters['minimal_distance']
                        dim_dict_max_values={}
                        dim_dict_max_values['x_dim']=math.sqrt(base_area_microns)
                        dim_dict_max_values['y_dim']=math.sqrt(base_area_microns)
                        dim_dict_max_values['z_dim']=dim3Boundary_microns
                        dim_dict_offsets={'x_dim_offset':X_left_corner,'y_dim_offset':Y_left_corner,'z_dim_offset':0}
                        dim_dict_mappings={}
                        dim_dict_mappings['dim1']=dim_dict[location_parameters['planeDimensions']['dim1']]
                        dim_dict_mappings['dim2']=dim_dict[location_parameters['planeDimensions']['dim2']]
                        dim_dict_mappings['dim3']=dim_dict[location_parameters['dim3']]

                        distance_dict={}
                        distance_dict['criterion']='minimal_distance'
                        distance_dict['minimal_distance']=minimal_distance
                        cell_position_array,golgi_pop_object,cell_counter=distance_dependent_positions(cell_position_array,cell_array,distance_dict,popIndex,\
                        seed_number,golgi_pop_object,dim_dict_max_values,dim_dict_offsets,no_of_cells_per_density_point,dim_dict_mappings,cell_counter)
                     
                        
                              
                     if location_parameters['distanceModel']=="random_no_overlap":
                        dim_dict_max_values={}
                        dim_dict_max_values['x_dim']=math.sqrt(base_area_microns)
                        dim_dict_max_values['y_dim']=math.sqrt(base_area_microns)
                        dim_dict_max_values['z_dim']=dim3Boundary_microns
                        dim_dict_offsets={'x_dim_offset':X_left_corner,'y_dim_offset':Y_left_corner,'z_dim_offset':0}
                        dim_dict_mappings={}
                        dim_dict_mappings['dim1']=dim_dict[location_parameters['planeDimensions']['dim1']]
                        dim_dict_mappings['dim2']=dim_dict[location_parameters['planeDimensions']['dim2']]
                        dim_dict_mappings['dim3']=dim_dict[location_parameters['dim3']]
                        distance_dict={}
                        distance_dict['criterion']='no_overlap'
                        distance_dict['cellDiameters']=cell_diameter_array
                        cell_position_array,golgi_pop_object,cell_counter=distance_dependent_positions(cell_position_array,cell_array,distance_dict,popIndex,\
seed_number,golgi_pop_object,dim_dict_max_values,dim_dict_offsets,no_of_cells_per_density_point,dim_dict_mappings,cell_counter)
                     
                        
                     if location_parameters['distanceModel']=="random":
                     
                        for cell in range(0,no_of_cells_per_density_point):
	                    Golgi_cell=neuroml.Instance(id="%d"%(cell_counter))
	                    cell_counter+=1
	                    X=random.random()
	                    Y=random.random()
	                    Z=random.random()
	                    cell_position=np.zeros([1,3])         
	                
                            cell_position[0,dim_dict[location_parameters['planeDimensions']['dim1']]]=X_left_corner+math.sqrt(base_area_microns)*X
                                       
                            cell_position[0,dim_dict[location_parameters['planeDimensions']['dim2']]]=Y_left_corner+math.sqrt(base_area_microns)*Y

                            cell_position[0,dim_dict[location_parameters['dim3']]]=dim3Boundary_microns*Z
                         
                            cell_position_array[location_parameters['popID']]=np.vstack((cell_position_array[location_parameters['popID']],cell_position))

                            Golgi_cell.location=neuroml.Location(x=cell_position[0,0], y=cell_position[0,1], z=cell_position[0,2])
                            golgi_pop_object.instances.append(Golgi_cell)
                            print cell_position[cell,0], cell_position[cell,1], cell_position[cell,2]
                                                                                                                          
    ### override any specified value of population Size
                                                                                                                          
    return cell_position_array, total_no_of_cells,golgi_pop_object


    


def distance_dependent_positions(cell_position_array,cell_array,distance_criterion_dict,popIndex,seed_number,golgi_pop_object,dim_dict_max_values,\
                      dim_dict_offsets={'x_dim_offset':0,'y_dim_offset':0,'z_dim_offset':0},popSize=None,dim_dict_mappings=None,cell_count=None):

    random.seed(seed_number)
    
    if distance_criterion_dict['criterion']=='no_overlap':
       cell_diameter_array=distance_criterion_dict['cellDiameters']
       cell_diameter=cell_diameter_array[cell_array[popIndex]['popID']]
       
    if distance_criterion_dict['criterion']=='minimal_distance':
       minimal_distance=distance_criterion_dict['minimal_distance']
       
    if popSize ==None:
       popSize=cell_array[popIndex]['size']
       
    
    use_cell_count=False
    if cell_count !=None:
       use_cell_count=True
    for cell in range(0,popSize):
        if use_cell_count:
           Golgi_cell=neuroml.Instance(id="%d"%cell_count)
           cell_count+=1
        else:
	   Golgi_cell=neuroml.Instance(id="%d"%cell)
	golgi_pop_object.instances.append(Golgi_cell)
	cell_position=np.zeros([1,3])
	if popIndex==0 and cell==0:
           X=random.random()
	   Y=random.random()
	   Z=random.random()
	   Xcoordinate=dim_dict_offsets['x_dim_offset']+dim_dict_max_values['x_dim']*X
           Ycoordinate=dim_dict_offsets['y_dim_offset']+dim_dict_max_values['y_dim']*Y
           Zcoordinate=dim_dict_offsets['z_dim_offset']+dim_dict_max_values['z_dim']*Z
	   if dim_dict_mappings != None:
              cell_position[0,dim_dict_mappings['dim1']]=Xcoordinate
              cell_position[0,dim_dict_mappings['dim2']]=Ycoordinate
              cell_position[0,dim_dict_mappings['dim3']]=Zcoordinate
           else:
              cell_position[0,0]=Xcoordinate
              cell_position[0,1]=Ycoordinate
              cell_position[0,2]=Zcoordinate
           cell_position_array[cell_array[popIndex]['popID']]=np.vstack((cell_position_array[cell_array[popIndex]['popID']],cell_position))
           Golgi_cell.location=neuroml.Location(x=cell_position[0,0], y=cell_position[0,1],z=cell_position[0,2])
           print cell_position[0,0], cell_position[0,1], cell_position[0,2]
           
        else:
           x=0
           try_cell_position=np.zeros([1,3])     
           while x==0:
              overlap_counter=0
              X=random.random()
	      Y=random.random()
	      Z=random.random()
	      Xcoordinate=dim_dict_offsets['x_dim_offset']+dim_dict_max_values['x_dim']*X
              Ycoordinate=dim_dict_offsets['y_dim_offset']+dim_dict_max_values['y_dim']*Y
              Zcoordinate=dim_dict_offsets['z_dim_offset']+dim_dict_max_values['z_dim']*Z
              if dim_dict_mappings != None:
                 try_cell_position[0,dim_dict_mappings['dim1']]=Xcoordinate
                 try_cell_position[0,dim_dict_mappings['dim2']]=Ycoordinate
                 try_cell_position[0,dim_dict_mappings['dim3']]=Zcoordinate
              else:
                 try_cell_position[0,0]=Xcoordinate
                 try_cell_position[0,1]=Ycoordinate
                 try_cell_position[0,2]=Zcoordinate
              Xtry=try_cell_position[0,0]
              Ytry=try_cell_position[0,1]
              Ztry=try_cell_position[0,2]
              for cell_pop_x in range(0,len(cell_array)):
                  pop_cell_positions=cell_position_array[cell_array[cell_pop_x]['popID']]
                  for cell_x in range(0,len(pop_cell_positions)):
                      if pop_cell_positions[cell_x,0]+pop_cell_positions[cell_x,1]+pop_cell_positions[cell_x,2] >0:
                          
                         if distance_criterion_dict['criterion']=='no_overlap':
                            if distance([Xtry,Ytry,Ztry],pop_cell_positions[cell_x]) < (cell_diameter_array[cell_array[popIndex]['popID']]+cell_diameter_array[cell_array[cell_pop_x]['popID']])/2:
                               overlap_counter+=1
                         else:
                            if distance_criterion_dict['criterion']=='minimal_distance':
                               if distance([Xtry,Ytry,Ztry],pop_cell_positions[cell_x]) < minimal_distance:
                                  overlap_counter+=1

                         
              
              if overlap_counter==0:
                 cell_position[0,0]=Xtry
                 cell_position[0,1]=Ytry
                 cell_position[0,2]=Ztry
                 
                 cell_position_array[cell_array[popIndex]['popID']]=np.vstack((cell_position_array[cell_array[popIndex]['popID']],cell_position))
                 Golgi_cell.location=neuroml.Location(x=cell_position[0,0], y=cell_position[0,1], z=cell_position[0,2])
                               
                 print cell_position[0,0], cell_position[0,1], cell_position[0,2]
                 x=1   

              

    if use_cell_count:
       return cell_position_array,golgi_pop_object,cell_count
    else:
       return cell_position_array,golgi_pop_object

                     

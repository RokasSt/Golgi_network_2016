####### saving an old block for reference
if string.lower(location_array['distributionModel'])=="density_profile_based":
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

               pop_position_array, total_no_of_cells,Golgi_pop=density_model(densityFilePath,location_parameters,golgi_pop_object,cell_diameter_array,seed)


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

                  print simulation_parameters['parentDir']+"/NeuroML2"+"/"+cell_array[cell_pop]['cellType']

                  if "NeuroML2CellType" in cell_array[cell_pop]:
                     cell_diameter=get_soma_diameter(simulation_parameters['parentDir']+"/NeuroML2"+"/"+cell_array[cell_pop]['cellType'],cell_array[cell_pop]["NeuroML2CellType"])
                  else:
                     cell_diameter=get_soma_diameter(simulation_parameters['parentDir']+"/NeuroML2"+"/"+cell_array[cell_pop]['cellType'])
               else:

                  if "NeuroML2CellType" in cell_array[cell_pop]:
                     cell_diameter=get_soma_diameter(cell_array[cell_pop]['cellType'],cell_array[cell_pop]["NeuroML2CellType"])
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

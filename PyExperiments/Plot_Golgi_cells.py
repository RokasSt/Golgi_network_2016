
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from PythonUtils.methods_v2 import plot_voltage_traces, plot_which_cells_with_inputs

if __name__ == "__main__":

#when using "one population one subplot" each pop has to be specified; if no cells have to be plotted for a specific pop pass empty list [] both in the case of "random fraction" and "explicit lists". For example:
  #   plot_voltage_traces(1,"V2010multi1_2p4c4c_4inp",0,["one population one subplot","random fraction",[[1.0],[]] ],["seed specifier",True],["save specifier",True,"testing_plot1.jpeg"],False)

   #plot_voltage_traces(2,"V2010multi1_2p4c4c_4inp",0,["one population one subplot","random fraction",[[1.0],[1.0]] ],["seed specifier",True],["save specifier",True,"testing_plot1.jpeg"],False)

   #plot_voltage_traces(2,"V2010multi1_2p4c4c_4inp",0,["one population one subplot","explicit lists",[[0,1],[0,1]]],["seed specifier",True],["save specifier",True,"testing_plot2.jpeg"],False)  

  # plot_voltage_traces(2,"V2010multi1_2p4c4c_4inp",0,["pairs",[[0,1] ],"explicit lists",[   [  [0,1],[0,1] ]   ]    ],["seed specifier",True], ["save specifier",True,"testing_plot3.pdf"]   ,False)  

   #plot_voltage_traces(2,"V2010multi1_2p4c4c_4inp",0,["pairs",[[0,1]],"random fraction",[  [1,0.5]    ]   ],["seed specifier",True],["save specifier",True,"testing_plot4.pdf"],True)  

   #plot_voltage_traces(2,"test_Lists",0,["one population one subplot","random fraction",[[1],[1]]],["seed specifier",True],["save specifier",True,"testing_lists1.pdf"],False)  
  
  #plot_voltage_traces(2,"test_Lists_and_sync",2,["one population one subplot","random fraction",[[1],[1]]],["seed specifier",False],["save specifier",False],False)  
  
   #plot_voltage_traces(2,"test_Lists2_and_sync",2,["one population one subplot","random fraction",[[1],[1]]],["seed specifier",False],["save specifier",False],False)  

  #plot_voltage_traces(2,"test_Lists_and_sync",1,["one population one subplot","explicit lists",[ [],[5,6,7,8,9] ] ],["seed specifier",False],["save specifier",False],True)  


  #####################
  



  #plot_params={}
  #plot_params['noOfPops']=3
  #plot_params['popIDList']=["Full_model","Reduced","Solinas"]
  #plot_params['expID']="three_cell_models_NeuroML2"
  #plot_params['trialID']=0
  #plot_params['subplotParams']=["population_list","explicit lists",{"Full_model":[0],"Reduced":[0],"Solinas":[0]}]
  #plot_params['seedSpecifier']=False
  #plot_params['saveSpecifier']=True
  #plot_params['figureName']="three_cell_models_NeuroML2_pcm.png"
  #plot_params['legendSpecifier']=True
  
  

  #########################
  #plot_voltage_traces(plot_params)


  
  

  ####### for network simulations


  plot_params={}
  plot_params['noOfPops']=1
  plot_params['popIDList']=["Golgi_pop0"]
  plot_params['expID']="V2010_regional_from_left_to_right_200ms"
  plot_params['trialID']=0
  plot_params['subplotParams']=["one population one subplot","explicit lists",{"Golgi_pop0":[16,59,49]}]
  plot_params['seedSpecifier']=False
  plot_params['saveSpecifier']=True
  plot_params['figureName']="V2010_reg_ltor_200ms_16_59_49.pdf"
  plot_params['title']="Voltage traces for cells 16, 59 and 49 in"
  plot_params['legendSpecifier']=True
  plot_params['inputIDdict']={'Golgi_pop0':['XFpop0l','XFpop0m','XFpop0r']}
  plot_params['colourArray']=['red','blue','green']
  
  plot_which_cells_with_inputs(plot_params)
  

  #########################
  plot_voltage_traces(plot_params)









   

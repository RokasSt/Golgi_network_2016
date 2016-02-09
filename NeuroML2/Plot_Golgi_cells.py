from methods import *


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

  plot_voltage_traces(2,"test_Lists_and_sync",1,["one population one subplot","explicit lists",[ [],[5,6,7,8,9] ] ],["seed specifier",False],["save specifier",False],True)  

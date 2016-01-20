
from  Generate_Golgi_Network import *




if __name__ == "__main__":
    
    
    Cell_array=[1,["Very_Simple_Golgi",2]]
    Position_array=["random",350, 350, 350]
    Conn_array=["uniform random",[0,"0.5nS"]]
    Input_array=["testing",1,["50.0ms","200.0ms","4E-5uA"],["250.0ms","200.0ms","-0.5E-5uA"]]
    Sim_array=[500,0.0005,"jNeuroML"]
    
    generate_and_run_golgi_cell_net("Simple_Golgi_Net",Cell_array,Position_array,Conn_array,Input_array,Sim_array,"not a list")

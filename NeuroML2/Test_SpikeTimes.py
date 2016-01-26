
import os.path

from pyelectro import analysis
from pyelectro import io

import os
import numpy as np


def get_spike_times(data_file):

    #data_file = '.dat'
    delimiter = '\t'
    if os.path.isfile(data_file):
       times, data = analysis.load_csv_data(data_file, delimiter=delimiter)
    elif os.path.isfile('txt/simulations/'+data_file):
         times, data = analysis.load_csv_data('txt/simulations/'+data_file, delimiter=delimiter)

    print("Loaded data with %i times & %i datapoints from %s"%(len(times),len(data),data_file))

   
    results = analysis.max_min(data, times)

    Spike_time_array=np.asarray(results['maxima_times'])

    Spike_time_aray=np.transpose(Spike_time_array)
  
    print results['maxima_times']

    np.savetxt('txt/simulations/Golgi_pop0_0_NEURON_V2010multi1_1c_1input.txt',Spike_time_array,fmt='%f',newline=" ")
        
    return results['maxima_times']









if __name__ == "__main__":

   get_spike_times('Golgi_pop0_0_NEURON_V2010multi1_1c_1input.dat')
   print "testing reading of spike times"

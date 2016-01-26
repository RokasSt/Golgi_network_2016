
import sys
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import seaborn as sns
import pyspike
import itertools




import utils



n_trials = 

sim_duration =
n_cells = 
n_excluded_cells = 0

fig, ax = plt.subplots(figsize=(4,2),ncols=1,nrows=2, sharex=True)
lines = []
labels = []

distances = []
color = sns.color_palette()[0]

for trial in range(n_trials):
    
    sim_dir = '../simulations/' + sim_ref
    time = np.loadtxt(sim_dir + '/time.dat')
    spike_trains = []
    for cell in range(n_cells):
        spikes = np.loadtxt('{}/Golgi_network_{}'.format(sim_dir, cell))
        spikes = np.loadtxt("PySpike_testdata.txt")
        print spikes
        spike_trains = spk.load_spike_trains_from_txt("PySpike_testdata.txt".format(,
                                              edges=(0, sim_duration))
        
        if trial==0:
            ax[0].scatter(spikes,
                          np.zeros_like(spikes)+cell,
                          marker='|',
                          s=2,
                          c=color)
    distances.append(pyspike.spike_profile_multi(spike_trains[n_excluded_cells:]))

# average synchrony index across trials
average_distance = distances[0]
for distance in distances[1:]:
    average_distance.add(distance)
average_distance.mul_scalar(1./n_trials)


xmin = 50
xmax = 1900
x, y = average_distance.get_plottable_data()
ximin = np.searchsorted(x, xmin)
ximax = np.searchsorted(x, xmax)
lines.append(ax[1].plot(x[ximin:ximax+1], 1-y[ximin:ximax+1], lw=2, c=color)[0])
#labels.append('{:g}'.format(variance_scaling))
ax[1].plot(x[:ximin+1], 1-y[:ximin+1], lw=2, c=color, alpha=0.4)
ax[1].plot(x[ximax:], 1-y[ximax:], lw=2, c=color, alpha=0.4)

ax[0].locator_params(tight=True, nbins=4)
ax[1].locator_params(axis='y', tight=False, nbins=4)
#ax[0].set_yticks([45 * k for k in range(n_models)])
#ax[0].set_ylim((45*n_models-1, 0))
ax[1].set_xticks([0, 310, 1000, 2000])
ax[0].set_ylabel('Cell number')
ax[1].set_xlabel('Time (ms)')
ax[1].set_ylabel('Synchrony index')
plt.tight_layout()
# fig.subplots_adjust(hspace=.5)
# fig.legend(lines, labels, title='Variance scaling', loc='center', ncol=n_models,
#            bbox_to_anchor=(0.55, 0.55))
fig.savefig('Desync_Golgi_Net.pdf')

        
                    

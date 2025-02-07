import pandas as pd
from mayavi import mlab
import numpy as np


#PUT THE CHANNELS YOU WANT HERE!
channels_to_plot=np.array([400,431,467,803,905])

crystal_positions = pd.read_csv('df_crystal_positions.csv')

all_channels=crystal_positions['Channel'].values

indices_to_plot=channels_to_plot-1

all_indices=all_indices = np.arange(0, 988)

other_indices=np.setdiff1d(all_indices,indices_to_plot)


fig = mlab.figure(1, size=(600,600), fgcolor=(1,1,1))
mlab.clf()


mlab.points3d(crystal_positions['X'][indices_to_plot],
        crystal_positions['Y'][indices_to_plot],
        crystal_positions['Z'][indices_to_plot],
        mode='cube',
        scale_factor=50,
        opacity=0.8,
        color=(1,0,0))


mlab.points3d(crystal_positions['X'][all_indices],
        crystal_positions['Y'][all_indices],
        crystal_positions['Z'][all_indices],
        mode='cube',
        scale_factor=50,
        opacity=0.1,
        color=(1,1,1))

mlab.show()

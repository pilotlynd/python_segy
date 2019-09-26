import numpy as np
import segyio
import os
import matplotlib.pyplot as plt
from gain import *

data_dir = 'data/test'

agc = True


for im in os.listdir(data_dir):
    if im.endswith(".segy") or im.endswith(".sgy"):
        filename = os.path.join(data_dir, im)
        with segyio.open(filename,'r',ignore_geometry=True) as f:
            f.mmap()

            sourceX = f.attributes(segyio.TraceField.SourceX)[:]
            trace_num = len(sourceX)#number of trace, The sourceX under the same shot is the same character.
            if trace_num>500:
                data = np.asarray([np.copy(x) for x in f.trace[0:500]]).T

                if agc:
                    data = gain(data,0.004,'agc',0.05,1)
                if data.shape[0]>600:
                    x = data[400:600,100:300]
                else:
                    x = data[:,:]

            else:
                data = np.asarray([np.copy(x) for x in f.trace[:]]).T
                if agc:
                    data = gain(data,0.004,'agc',0.05,1)
                if data.shape[0]>600:
                    x = data[400:600,100:300]
                else:
                    x = data[:,:]
            
            f.close()
        plt.imshow(x,vmin=-1,vmax=1)
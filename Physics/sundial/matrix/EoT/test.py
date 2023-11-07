import numpy as np
import matplotlib.pyplot as plt
import Run
import banc_vectorManip as vMp

v=np.array([])
for d in np.range(0,365):
    np.append(v,getEoT(d*86400))

plt.plot(v)
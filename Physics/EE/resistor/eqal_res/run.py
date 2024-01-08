import numpy as np
import matplotlib.pyplot as plt

def rep(R1,R2):
    return (R1**-1+R2**-1)**-1

R0=np.arange(0,10e3,1)
R1=10e3
R2=1e3
Re=rep(R0,R1)+R2

plt.plot(R0,Re)
plt.show()
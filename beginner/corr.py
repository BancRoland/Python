import matplotlib.pyplot as plt
import numpy as np

barker13=np.array([1,1,1,1,1,0,0,1,1,0,1,0,1])*2-1
code=np.array([0,0,0,0,0.5,1,1,1,1,0,-1,0,1,0,0,0,0,0.5,0,0,0])
plt.plot(np.correlate(barker13,barker13,"full"))
plt.plot(np.correlate(barker13,code,"full"))
plt.grid()
plt.show()
#!/bin/python3

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)
y2=np.cos(x)

plt.plot(x,y,label='sin(x)')
plt.plot(x,y2,label='cos(x)')
plt.xlabel('xcím')
plt.ylabel('ycím')
plt.title('Ez egy címsor')
#plt.legend(['sin(x)','cos(x)'])
plt.legend()
plt.grid()
plt.show()

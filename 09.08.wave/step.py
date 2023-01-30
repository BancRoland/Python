#!/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import math
import cmath

fs=44100
f=10
T=10

#t = np.linspace(0, T, T*fs)
t=np.arange(0, T, 1/fs)

y0=t-np.floor(t)
#y0=np.exp(1j*2*np.pi*f*t);


plt.plot(t,np.real(y0))
plt.plot(t,np.imag(y0))
plt.grid()
plt.show()


#plt.plot(t,y,label='sin(x)')
#plt.plot(t,y2,label='cos(x)')
#plt.xlabel('xcím')
#plt.ylabel('ycím')
#plt.title('Ez egy címsor')
#plt.legend(['sin(x)','cos(x)'])
#plt.legend()
#plt.grid()
#plt.show()


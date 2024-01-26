#!/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import math
import cmath

fs=44100	#Hz	mintavételi frekvencia
f0=500		#Hz	alapfrekvencia
T0=2		#sec	sweepidő
a=100		#Hz/sec	frekvenciameredekség
T=10		#sec	futásidő

#t = np.linspace(0, T, T*fs)
t=np.arange(0, T, 1/fs)

f=f0+a*T0*(t/T0-np.floor(t/T0))
#y0=np.exp(1j*2*np.pi*f*t);

integf=[];
val=0;

for i in f:
	val=val+i
	integf.append(val)



plt.figure(2)
plt.plot(t,np.real(integf))
plt.plot(t,np.imag(integf))
plt.grid()
plt.show()

plt.figure(1)
plt.plot(t,np.real(f))
plt.plot(t,np.imag(f))
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


import numpy as np
import matplotlib.pyplot as plt
from numpy import random as rnd
from run import *

fs=44100
T=1
t=np.arange(0,T ,1/fs)
f=5000.5
v=np.exp(1j*2*np.pi*t*f)
spec=np.fft.fft(v)/len(v)
spec2=np.fft.fft(cosWind(v))/len(v)
cs=spec[int(T*f-100):int(T*f+100)]
cs2=spec2[int(T*f-100):int(T*f+100)]

plt.plot(A2dB(abs(spec)),'o-')
plt.plot(A2dB(abs(spec2)),'o-')
#plt.plot(abs(spec),'o-')
plt.title(max(abs(spec)))
plt.show()
print(np.sqrt(np.sum(abs(cs)**2)))
print(np.sqrt(np.sum(abs(cs2)**2)))

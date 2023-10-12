import numpy as np
import matplotlib.pyplot as plt

def HannWindow(v):
    wind=(1-np.cos(np.arange(len(v))/len(v)*2*np.pi))
    return(wind*v)

LEN=100
signal=np.sin(np.arange(0,LEN,0.1))+1e-4*np.sin(20*np.arange(0,LEN,0.1))+1e-5*np.sin(10*np.arange(0,LEN,0.1))+1e-3*np.sin(5*np.arange(0,LEN,0.1))
signal=0.00001*np.random.randn(len(signal))+signal

plt.plot(signal)
plt.show()
plt.plot(HannWindow(signal))
plt.show()

plt.plot(20*np.log10(np.abs(np.fft.fft(signal/len(signal)))),'.-')
plt.plot(20*np.log10(np.abs(np.fft.fft(HannWindow(signal)/len(signal)))),'.-')
plt.show()

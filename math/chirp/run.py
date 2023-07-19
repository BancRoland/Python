import matplotlib.pyplot as plt
import numpy as np
import math
import cmath

SR=44100
fmax=SR/1000
n=2*SR
f=np.arange(0,n)
T=1/SR
t=np.arange(0,n/SR,T)
f=fmax/n*SR*t
p=2*math.pi*fmax/n*SR*t**2/2
# s=np.sin(p)
samples0=np.exp(1j*p)
samples1=np.concatenate((samples0, np.conj(samples0[::-1])))
samples=np.concatenate((samples1, samples1[::-1]))

plt.figure()
plt.plot(np.real(samples),'.-')
plt.plot(np.imag(samples),'.-')
plt.plot(np.abs(samples),'--', color='grey', alpha=0.5)
plt.plot(-np.abs(samples),'--', color='grey', alpha=0.5)
plt.legend(["Real","Imag","Abs"])
# plt.title(title)
plt.grid()
plt.show()

FFT=np.fft.fft(samples)
plt.figure()
# plt.plot(np.real(FFT),'.-')
# plt.plot(np.imag(FFT),'.-')
plt.plot(np.abs(FFT),'--', color='grey', alpha=0.5)
plt.plot(-np.abs(FFT),'--', color='grey', alpha=0.5)
plt.legend(["Real","Imag","Abs"])
# plt.title(title)
plt.grid()
plt.show()



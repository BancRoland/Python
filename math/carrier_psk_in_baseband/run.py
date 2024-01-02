import numpy as np
import matplotlib.pyplot as plt


f=10
t=np.arange(0,1,0.001)
signal=np.exp(1j*2*np.pi*f*t)

signal=np.concatenate([signal,1j*signal,-1*signal])

plt.plot(np.real(signal))
plt.plot(np.imag(signal))
plt.show()

signal=np.real(signal)

spec=np.fft.fft(signal)
plt.plot(np.abs(spec))
plt.show()

spec[int(len(spec)/2):]=np.zeros(len(spec[int(len(spec)/2):]))
signal=np.fft.ifft(spec)

mix=np.exp(-1j*2*np.pi*np.arange(len(signal))/len(signal)*20)

sig2=signal*mix

plt.plot(np.real(sig2))
plt.plot(np.imag(sig2))
plt.show()
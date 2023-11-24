from ssl import HAS_NPN
import numpy as np
import matplotlib.pyplot as plt

LEN=100
N=3
powSpec=np.zeros(LEN*N)
powSpecN=np.zeros(LEN*N)
Hsum=np.zeros(LEN*N)

HWlen=20
channelHw=np.fft.fft(np.concatenate([np.random.randn(HWlen)+1j*np.random.randn(HWlen),np.zeros(len(powSpecN)-HWlen)]))

CicLen=1000
for i in range(CicLen):
    signal=np.random.randn(LEN)+1j*np.random.randn(LEN)
    signal=np.concatenate([signal,np.zeros((N-1)*LEN)])
    signal=np.fft.ifft(signal)
    signalN=0.5*np.fft.ifft(np.random.randn(len(signal))+1j*np.random.randn(len(signal)))+signal
    
    powSpec=powSpec+np.fft.fft(signal)*np.conjugate(np.fft.fft(signal))
    powSpecN=powSpecN+np.fft.fft(signalN)*np.conjugate(np.fft.fft(signalN))

    y=channelHw*np.fft.fft(signalN)
    H=y*np.conj(np.fft.fft(signal))

    Hsum=H+Hsum

    
powSpecN=powSpecN/CicLen
powSpec=powSpec/CicLen
Hsum=Hsum/CicLen/powSpecN

plt.plot(np.real(channelHw))
plt.plot(np.imag(channelHw))
plt.title("Átviteli függvény")
plt.xlabel("frequency")
plt.show()

plt.plot(np.real(signal))
plt.plot(np.imag(signal))
plt.title("Signal")
plt.xlabel("time")
plt.show()

plt.plot(np.abs(np.fft.fft(signal)))
plt.plot(np.abs(np.fft.fft(signalN)))
plt.show()

plt.plot(np.abs(powSpecN))
plt.plot(np.abs(powSpec))
# plt.ylim([0,3])
plt.grid()
plt.show()

y=channelHw*np.fft.fft(signalN)

H=y*np.conj(np.fft.fft(signal))

plt.subplot(2,1,1)
plt.plot(np.real(channelHw))
plt.plot(np.imag(channelHw))
plt.subplot(2,1,2)
plt.plot(np.real(Hsum))
plt.plot(np.imag(Hsum))
plt.show()

# plt.plot(np.abs(np.fft.fft(y/(signal+1))))
# plt.show()


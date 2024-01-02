import numpy as np
import matplotlib.pyplot as plt

def hanning(v):
    w=(1-np.cos(2*np.pi*np.arange(len(v))/len(v)))
    return v

t=np.arange(0,1,0.001)
a=40
A=[a, a+0.1, a+0.2, a+0.3, a+0.4, a+0.5]
# A=[a, a+1, a+2, a+3, a+4, a+5]
A=[a]

for i in range(len(A)):
    sig=np.sign(np.sin(2*np.pi*A[i]*t+1e-5))
    # sig=np.concatenate([np.ones(10),np.zeros(10),np.ones(10),np.zeros(10),np.ones(10),np.zeros(10)])
    # sig=2*sig-1
    sig=sig+0.00001*np.random.randn(len(sig))

    # plt.plot(sig,"o-")
    # plt.show()
    plt.subplot(len(A),2,2*i+1)
    plt.plot(20*np.log10(np.abs(np.fft.fft(hanning(sig)))),"o-")

    plt.subplot(len(A),2,2*i+2)
    plt.plot(sig,"o-")
    # plt.show()

    # plt.plot(20*np.log10(np.abs(np.fft.fft(sig[0:-3:]))),"o-")
plt.show()
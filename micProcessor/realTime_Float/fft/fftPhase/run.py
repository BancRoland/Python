import matplotlib.pyplot as plt
import numpy as np
import struct

def convI32(v):
	num=v[3]+256*v[2]+256**2*v[1]+256**3*v[0]
	return num

def dd(v):
	return(v*2)


size=2**13
fs=44100
f=np.linspace(0,fs,size)
total=np.ones(size)
#file = open("pipe", "rb")
file = open("/dev/stdin", "rb")
byte = file.read(4*size)
while byte:
    byte = file.read(4*size)
    num2=np.array(struct.unpack("<" + "f" * size, byte))
    plt.ion()
    plt.clf()
    spec=np.fft.fft(num2)/size
    #spec=np.fft.fft(num2)/size
    plt.subplot(2,1,1)
    #plt.plot(f,np.real(phCorr))
    plt.plot(f,np.imag(spec))
    #plt.ylim([-1, 1])
    plt.ylim([-1e-3, 1e-3])
    plt.xlim([500, 5000])
    plt.grid()
    plt.subplot(2,1,2)
    #plt.plot(f,np.real(phCorr))
    plt.plot(f,np.real(spec))
    #plt.plot(f,20*np.log10(np.real(spec)))
    #plt.ylim([-1, 1])
    plt.ylim([-1e-3, 1e-3])
    plt.xlim([500, 5000])
    plt.grid()
    
    plt.show()
    plt.pause(.000001)
    

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
    absSpec=20*np.log10(np.abs(np.fft.fft(num2)/size))
    plt.ion()
    plt.clf()
    plt.plot(f,absSpec)
    plt.ylim([-150, 0])
    plt.xlim([0, fs/2])
    plt.grid()
    
    plt.show()
    plt.pause(.000001)
    

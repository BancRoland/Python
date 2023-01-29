import matplotlib.pyplot as plt
import numpy as np
import struct

def convI32(v):
	num=v[3]+256*v[2]+256**2*v[1]+256**3*v[0]
	return num

def dd(v):
	return(v*2)


size=2**13
total=np.ones(size)
file = open("pipe", "rb")
byte = file.read(4*size)
while byte:
    byte = file.read(4*size)
    num2=np.array(struct.unpack("<" + "f" * size, byte))
    plt.ion()
    plt.clf()
    plt.plot(num2)
    plt.ylim([-1, 1])
    plt.show()
    plt.pause(.000001)

#!/bin/python3
# import uhd
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
from datetime import datetime

DEC=10_000

filesize=100_000_000 

cntr=0
TYPESIZE=2

# sampRX00=np.fromfile('outRX.dat', count=filesize, offset=cntr*filesize*8, dtype=np.complex64)
sampRX00=np.fromfile('outRX.dat', count=filesize, offset=cntr*filesize*TYPESIZE, dtype=np.int16)
size=np.size(sampRX00)

decDiffOut=np.zeros(0)
decAmpDiffOut=np.zeros(0)
decOut=np.zeros(0)


MEM=0+0j


while(size):

    cntr=cntr+1
    print(cntr)
    # print(size)

    sampRX0=sampRX00[0::2]+1j*sampRX00[1::2]
    sampRX=sampRX0[0:int(size/2):DEC]

    sampDIFF=np.zeros(len(sampRX))+1j*np.zeros(len(sampRX))
    sampAmpDIFF=np.zeros(len(sampRX))

    sampDIFF[0]=sampRX[0]-MEM
    sampAmpDIFF[0]=np.abs(sampRX[0])-np.abs(MEM)

    for i in range(len(sampRX)-1):
        sampDIFF[i+1]=sampRX[i+1]-sampRX[i]
        sampAmpDIFF[i+1]=np.abs(sampRX[i+1])-np.abs(sampRX[i])
    MEM=sampRX[-1]

    decDiffOut=np.concatenate([np.array(decDiffOut),np.array(sampDIFF)])
    decAmpDiffOut=np.concatenate([np.array(decAmpDiffOut),np.array(sampAmpDIFF)])

    decOut=np.concatenate([np.array(decOut),np.array(sampRX)])
    print(np.size(decOut))
    
    # sampRX00=np.fromfile('outRX.dat', count=filesize, offset=cntr*filesize*8, dtype=np.complex64)
    sampRX00=np.fromfile('outRX.dat', count=filesize, offset=cntr*filesize*TYPESIZE, dtype=np.int16)
    size=np.size(sampRX00)


# decOutC=decOut[0::2]+1j*decOut[1::2]

t=np.arange(len(decOut))*DEC

plt.figure(figsize=(12, 6)) #, dpi=80)
plt.title("Mintaértékek Decimálva")
plt.grid()
plt.plot(t,np.real(decOut),'-')
plt.plot(t,np.imag(decOut),'-')


plt.plot(t,np.abs(decDiffOut),'.-')

plt.plot(t,decAmpDiffOut,'.-')

plt.legend(["Im","Re","P_diff","A_diff"])

plt.xlabel("decimálatlan mintaszám")
plt.savefig("out.png")

plt.show()


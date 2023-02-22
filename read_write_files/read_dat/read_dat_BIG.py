#!/bin/python3
import uhd
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
from datetime import datetime

now = datetime.now()
dstr = now.strftime("%Y-%m-%d_%H-%M-%S")

filesize=100_000_000

# with open("out.dat", mode="rb") as input:
#     samples = input.read()

i=0
sampTX0=np.fromfile('outTX.dat', count=filesize, offset=i*filesize*8, dtype=np.complex64)
sampRX0=np.fromfile('outRX.dat', count=filesize, offset=i*filesize*8, dtype=np.complex64)

size=min(np.size(sampRX0),np.size(sampTX0))
diff=np.zeros(0)

while(size):

    i=i+1

    print(f'size= {size}')

    step=100_000

    sampTX=sampTX0[0:size:step]
    sampRX=sampRX0[0:size:step]
    n=np.arange(0,size,step)


    # samples0=np.fromfile('togrc.dat', dtype=np.complex64)

    off=0

    diff=np.concatenate([np.array(diff),np.array(sampRX*np.conj(sampTX))])

    sampTX0=np.fromfile('outTX.dat', count=filesize, offset=i*filesize*8, dtype=np.complex64)
    sampRX0=np.fromfile('outRX.dat', count=filesize, offset=i*filesize*8, dtype=np.complex64)

    size=min(np.size(sampRX0),np.size(sampTX0))

    # diff=sampRX+(sampTX)

    # plt.figure()
    # plt.plot(np.real(sampTX),'.-')
    # plt.plot(np.imag(sampTX),'.-')
    # plt.xlim(0+off,128+off)
    # plt.show()

plt.figure()
# plt.plot(np.real(diff[0::10_000]),'.-')
# plt.plot(np.imag(diff[0::10_000]),'.-')
plt.plot(np.angle(diff),'.-')
plt.plot(np.log10(np.abs(diff)),'.-')
plt.show()

    # start=int(4.59e7)
    # stop=int(4.63e7)
    # plt.figure()
    # plt.plot(range(start,stop),np.real(sampTX0[start:stop]),'.-')
    # plt.plot(range(start,stop),np.imag(sampRX0[start:stop]),'.-')
    # plt.show()


    # plt.figure()
    # plt.plot(np.abs(fftpack.fft(sampRX)),'.-')
    # plt.show()

    # plt.xlabel('xcím')
    # plt.ylabel('ycím')
    # title=('frq= %.2f MHz \nsamprate= %.2f Msamp/sec \nDate= %s' %(center_freq/1E6,sample_rate/1E6,dstr));
    # print(title)
    # plt.title(title)
    # #plt.legend(['sin(x)','cos(x)'])
    # plt.legend()
    # plt.grid()
    # plt.savefig(dstr+'.png')

    #plt.close()

    # sampTX0=np.fromfile('outTX.dat', count=filesize, dtype=np.complex64)
    # sampRX0=np.fromfile('outRX.dat', count=filesize, dtype=np.complex64)

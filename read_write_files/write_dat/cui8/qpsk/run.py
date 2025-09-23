#!/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import math
import cmath
import sys
sys.path.append('/home/roland/Desktop/Python/DSP')
import dsp

def comp2cui8(v):
    code=np.zeros(len(v)*2)
    code[::2]=np.real(v)+128
    code[1::2]=np.imag(v)+128
    out=code.astype('uint8')
    return out


symNum    = 100    # []     number of symbols
f_sample  = 800000 # [Hz]     sample rate
f_symbol  = 800   # [Hz]     symbol rate
f_offset  = 10000       # frequency offset error simulation
A   = 0
noise_val = 40  #szórás

samples_in_one_symbol = int(np.floor(f_sample/f_symbol))


# code = np.array([1,0,1,2,3,1])
code = dsp.get_random_qpsk(symNum)
dsp.complex_plot(code)
# plt.show()
code2 = dsp.inc(code,samples_in_one_symbol)
dsp.complex_plot(code2)
# plt.show()



signal= A*dsp.upmix(code2,f_offset,f_sample)
dsp.complex_plot(signal)
# plt.show()



# signal=A*np.exp(1j*np.pi*2*np.arange(N)/N*fc*T)
# print(np.sqrt(np.sum(np.abs(signal)**2)/len(signal)))
print((np.mean(np.abs(signal)**2)))
signal=dsp.agwn(signal,noise_val)
print((np.mean(np.abs(signal)**2)))
# print(np.sqrt(np.mean(np.abs(signal)**2)-64**2))

out=comp2cui8(signal)
out.tofile("out.cui8")
print("Done")

# Create binary file from numpy array

# nparray.tofile("out0.dat")

# nparray.tofile("out.cf32", format="np.complex64")
# Print data from the binary file

#print(np.fromfile("list.bin",  dtype=float))

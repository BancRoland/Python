#!/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import math
import cmath
import sys
sys.path.append('/home/roland/Desktop/Python/DSP')
import dsp

def hex_to_binary(hex_string):
    return ' '.join(f'{int(c, 16):04b}' for c in hex_string)



def comp2cui8(v):
    code=np.zeros(len(v)*2)
    code[::2]=np.real(v)+127
    code[1::2]=np.imag(v)+127
    out=code.astype('uint8')
    return out


symNum    = 10000    # []     number of symbols
f_sample  = 800000 # [Hz]     sample rate
f_symbol  = 32000   # [Hz]     symbol rate
f_offset  = 10000       # frequency offset error simulation
A   = 30
noise_val = 10  #szórás

samples_in_one_symbol = int(np.floor(f_sample/f_symbol))


# code = np.array([1,0,1,2,3,1])

# code = dsp.get_random_qpsk(symNum)

# print(code[0:10])

random = np.floor(np.random.random(100)*4)
print("corr_code = [", end="")
for i in random:
    print(f"{int(i)}, ", end="")
print("]")

# # barker_phases = np.array([0,0,0,0,0,2,2,0,0,2,0,2,0])
# barker_phases = np.array([2,2,2,2,2,2,2,0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,2,2,2,0,0,2,0,2,0])
corr_code = np.array([0, 1, 1, 2, 1, 2, 1, 0, 3, 1, 3, 1, 1, 2, 1, 1, 0, 0, 0, 1, 3, 3, 1, 3, 2, 0, 3, 0, 1, 2, 3, 0, 3, 0, 2, 1, 2, 3, 3, 2, 3, 2, 2, 3, 3, 2, 0, 1, 1, 1, 3, 3, 0, 3, 1, 0, 2, 0, 1, 3, 2, 1, 0, 3, 2, 3, 3, 1, 2, 3, 3, 3, 3, 0, 3, 3, 0, 1, 3, 3, 1, 2, 2, 3, 2, 3, 3, 1, 0, 0, 1, 0, 1, 3, 3, 3, 0, 2, 0, 2])

code = np.exp(1j*corr_code*2*np.pi/4)


# code = dsp.get_random_qpsk(100)




# A = 1
code = np.concatenate((dsp.get_random_qpsk(symNum-400), code, dsp.get_random_qpsk(symNum)))
# code = np.concatenate((np.zeros(10*len(code)), code, np.zeros(10*len(code))))

# dsp.complex_plot(code)
# plt.show()
code2 = dsp.inc(code,samples_in_one_symbol)
# print(code2[0:10])

# dsp.complex_plot(code2)
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

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
T   = 2     # [sec]
sr  = 100000 # [Hz]
LEN = sr*T
f   = 25000
A   = 64

signal=A*np.exp(1j*np.pi*2*np.arange(LEN)/LEN*f*T)
# print(np.sqrt(np.sum(np.abs(signal)**2)/len(signal)))
print((np.mean(np.abs(signal)**2)))
signal=dsp.agwn(signal,10)
print((np.mean(np.abs(signal)**2)))
# print(np.sqrt(np.mean(np.abs(signal)**2)-64**2))

out=comp2cui8(signal)
out.tofile("out.cui8")

# Create binary file from numpy array

# nparray.tofile("out0.dat")

# nparray.tofile("out.cf32", format="np.complex64")
# Print data from the binary file

#print(np.fromfile("list.bin",  dtype=float))

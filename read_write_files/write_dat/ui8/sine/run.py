#!/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import math
import cmath
import sys
sys.path.append('/home/roland/Desktop/Python/DSP')
import dsp


T   = 2     # [sec]
sr  = 44100 # [Hz]
LEN = sr*T
f   = 1000
A   = 64

signal=A*np.exp(1j*np.pi*2*np.arange(LEN)/LEN*f*T)
# print(np.sqrt(np.sum(np.abs(signal)**2)/len(signal)))
print((np.mean(np.abs(signal)**2)))
signal=dsp.agwn(signal,10)
print((np.mean(np.abs(signal)**2)))
# print(np.sqrt(np.mean(np.abs(signal)**2)-64**2))
signal=np.real(signal+128.0)
plt.plot(signal)
plt.show()
out=signal.astype('uint8')
out.tofile("out.ui8")
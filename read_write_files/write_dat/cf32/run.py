#!/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import math
import cmath

def comp2cf32(v):
    code=np.zeros(len(v)*2)
    code[::2]=np.real(v)
    code[1::2]=np.imag(v)
    out=code.astype('float32')
    return out

# Declare numpy array

A=[1, 2, 3, 4, 5, 6]
B=[9, 8, 7, 6, 5, 4]
C=[1+2j, 3+5j, 4+9j]

print(C)

out=comp2cf32(C)
out.tofile("out.cf32")

# Create binary file from numpy array

# nparray.tofile("out0.dat")

# nparray.tofile("out.cf32", format="np.complex64")
# Print data from the binary file

#print(np.fromfile("list.bin",  dtype=float))

#!/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import math
import cmath

# Declare numpy array

A=[1, 2, 3, 4, 5, 6]
B=[9, 8, 7, 6, 5, 4]
C=[1+2j, 3+5j, 4+9j]

print(C)

nparray =np.array(C)

# Create binary file from numpy array

nparray.tofile("out0.dat")

# Print data from the binary file

#print(np.fromfile("list.bin",  dtype=float))

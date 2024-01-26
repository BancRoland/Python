#!/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import math
import cmath

repet=10
inc=1
# Declare numpy array
C0=[1+2j, 3+5j, 4+9j]
print(C0)

# C1=np.zeros(len(C0)*repet, dtype=np.complex64)
C1=[]
#sorminta
for i in range(repet):
    print('thing')
    C1 = C1 + C0
print(C1)

C2=np.zeros(len(C1)*inc, dtype=np.complex64)

for i in range(len(C1)):
    for k in range(inc):
        C2[inc*i+k]=C1[i]
print(C2)

plt.plot(np.real(C2),'.-')
plt.plot(np.imag(C2),'.-')
plt.grid()
plt.show()

#nparray =np.array(C)

# Print data from the binary file

#print(np.fromfile("list.bin",  dtype=float))

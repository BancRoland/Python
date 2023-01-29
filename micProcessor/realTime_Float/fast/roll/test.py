import matplotlib.pyplot as plt
import numpy as np
import struct

a=np.array([1, 2, 3, 4, 5, 6])
b=np.arange(10)
size=2
n=5
print(b[size:])
print(b[0:-(size)])
b[0:-size]=b[size:]
print(a)
print(b)

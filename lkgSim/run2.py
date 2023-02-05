import numpy as np
import matplotlib.pyplot as plt
from numpy import random

A=random.normal(size=(100,100))
B=random.normal(size=(10000))
#print(A)
"""
plt.imshow(A, cmap='gray', interpolation='nearest')
plt.colorbar()
plt.show()
"""



C=0
D=0
for i in B:
	#print(i)
	C=C+i
	D=D+i**2
print("sum= ",C)
print("sumSqr= ",np.sqrt(D/len(B)))
#print(B)
print("sum(B)",sum(B))
print("np.sqrt(sum(B**2)/len(B))", np.sqrt(sum(B**2)/len(B)))

plt.figure()
plt.plot(B,'.')
plt.show()

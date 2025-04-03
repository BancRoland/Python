import matplotlib.pyplot as plt
import numpy as np

w=np.load("out.npy")
w=w[0:11]
w=2*w-1
u=np.convolve(w,w[::-1])

plt.plot(w,"o-")
plt.show()

plt.plot(10*np.log10(np.abs(u)),"o-")
plt.show()
import numpy as np
import matplotlib.pyplot as plt

sig=np.random.randn(1000)+1j*np.random.randn(1000)

plt.plot(np.real(sig))
plt.plot(np.imag(sig))
plt.show()

plt.plot(np.abs(np.convolve(sig,np.conjugate(sig[::-1]), mode="full")))
plt.show()
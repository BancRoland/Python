import matplotlib.pyplot as plt
import numpy as np

Z_0=50
Z_L=75
k=2*np.pi
l=np.arange(100)/100

Z_in=Z_0*(Z_L+1j*np.tan(k*l)*Z_0)/(Z_0+1j*np.tan(k*l)*Z_L)

plt.plot(l,np.real(Z_in))
plt.plot(l,np.imag(Z_in))
plt.plot(l,np.abs(Z_in),color="gray")
plt.ylim([-100,100])
plt.grid()
plt.show()

plt.plot(l,np.imag(Z_in)/np.real(Z_in),color="C2")
plt.grid()
plt.show()
import numpy as np
import matplotlib.pyplot as plt
from numpy import random
from func import *

n=1*8*1024/64
A=1
As=1
fs=0.5e6
fsig=110000
fc=1e9
c=3e8

dk=15
ds=0.1
#t=np.arange(0,n/fs,1/fs)
t=np.linspace(0,n/fs,n)

M=[]
M2=np.array([[]])
M2=random.normal(size=(1,len(t)))
M2=np.empty(shape=[0, len(t)])
"""
M2=np.array([[1, 2, 3]])
a=[4, 5, 6]
b=np.vstack([M2,a])
print(b)
"""

for fc in np.arange(1500,2000,5):
	K0=A*np.exp(1j*2*np.pi*fsig*t)
	S0=As*np.exp(1j*2*np.pi*fsig*t)
	lamb=c/(fc*1e6)
	k=2*np.pi/lamb
	K=K0*np.exp(-1j*k*dk)
	S=S0*np.exp(-1j*k*ds)
	P=K+S
	spec=np.fft.fft(cosWind(P))/len(P)
	M.append(max(abs(spec)))
	M2=np.vstack([M2, spec])

	"""
	#plt.plot(t,np.real(P),'.-')
	#plt.figure()
	plt.plot(abs(spec),'.-')
	plt.show()
	"""
	
#plt.ylim(0,2)
plt.show()



plt.figure()
plt.imshow(A2dB(abs(M2)), cmap='gray', interpolation='nearest')
plt.colorbar()
plt.clim(-20,10)
plt.show()

img=A2dB(abs(np.fft.fft(M2, axis=0)))

plt.figure()
plt.imshow(np.fft.fftshift(img), cmap='gray', interpolation='nearest')
plt.colorbar()
plt.clim(-20,40)
plt.show()

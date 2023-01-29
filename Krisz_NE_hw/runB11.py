import matplotlib.pyplot as plt
import numpy as np
import struct

def LPF(v, a):
	w=np.zeros(len(v))*1j+np.zeros(len(v))
	for i in range(len(v)-1):
		w[i+1]=(1-a)*w[i]+a*v[i]
	return(w)
	
def INC(v,a):
	w=np.zeros(0)
	for i in v:
		w=np.append(w,i*np.ones(a))
	return(w)

file=open("b11_23571113.wav",'rb')
#file=open("sajat_23571113.wav",'rb')
#file=open("b13_br.i16",'rb')

data=np.fromfile(file, dtype='<i2')/2**16

plt.plot(abs(np.fft.fft(data**2)))
plt.plot(data)
plt.show()

barker=np.array((0,0,0,0,0,1,1,0,0,1,0,1,0))*2-1
barker11=np.array((0,0,0,1,1,1,0,1,1,0,1))*2-1
sajat=np.array((0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1))*2-1

plt.figure()
plt.plot(barker11)
plt.show()

plt.figure()
plt.plot(INC(barker11,71976-66268),'.-')
plt.show()

fs=44100
f=np.arange(len(data))/len(data)*fs
t=np.arange(len(data))
#LO=np.exp(1j*2*np.pi*t*8869/len(data))

LO=np.exp(1j*2*np.pi*t*9018/2/len(data))

data2=LPF(LO*data,0.01)
plt.figure()
plt.plot(np.real(data2))
plt.plot(np.imag(data2))
#plt.xlim(30000, 40000)
plt.plot()
plt.show()

plt.figure()
corr0=np.correlate((data2[0:20000]),data2[0:20000], 'full')
plt.plot(np.abs(corr0))
#plt.plot(np.imag(corr),'.-')
plt.show()


plt.figure()
barker2=INC(barker11,int((4794)/11))
#corr=np.correlate(INC(barker,71976-66268),data2)
corr=np.correlate(barker2,data2, 'full')
plt.plot(np.abs(corr))
#plt.plot(np.imag(corr),'.-')
plt.show()

"""
for f in range(4400,4600,1):
	LO=np.exp(1j*2*np.pi*t*f/len(data))

	data2=LPF(LO*data,1)
	#plt.figure()
	plt.clf()
	plt.title(f)

	plt.plot(np.real(data2))
	plt.plot(np.imag(data2))
	plt.xlim(30000, 40000)
	plt.draw()
	plt.pause(0.001)
"""


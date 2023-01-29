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

#file=open("b11_23571113.wav",'rb')
file=open("sajat_23571113.wav",'rb')
#file=open("b13_br.i16",'rb')

data=np.fromfile(file, dtype='<i2')/2**16

plt.plot(abs(np.fft.fft(data**2)))
#plt.plot(abs(np.fft.fft(data**2)))
#plt.plot(data)
plt.show()

barker=np.array((0,0,0,0,0,1,1,0,0,1,0,1,0))*2-1
barker11=np.array((0,0,0,1,1,1,0,1,1,0,1))*2-1

sajat=np.array((0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1))*2-1
#sajat=np.array((1,0,1,1,1,1,1,0,1,1,1,0,0,0,1,0,0,1,1,0,1,1,0,0,0,1,0,1,1,0,1,0))*2-1

"""
plt.figure()
plt.plot(sajat)
plt.show()

plt.figure()
plt.plot(INC(sajat,71976-66268),'.-')
plt.show()
"""

fs=44100
f=np.arange(len(data))/len(data)*fs
t=np.arange(len(data))
LO=np.exp(1j*2*np.pi*t*4445/len(data))


data2=LPF(LO*data,0.01)


plt.figure()
corr0=np.correlate(data2[0:30000],data2[0:30000], 'full')
plt.plot(np.abs(corr0))
#plt.plot(np.imag(corr),'.-')
plt.show()

sajat2=INC(sajat,int(14086/len(sajat)))

plt.figure()
plt.plot(np.real(data2[0:20000]))
plt.plot(np.imag(data2[0:20000]))
plt.plot(sajat2*0.25)
#plt.plot(np.imag(corr),'.-')
plt.show()

plt.figure()

#corr=np.correlate(INC(barker,71976-66268),data2)
corr=np.correlate(sajat2,data2, 'full')
plt.plot(np.abs(corr))
#plt.ylim(0,100)
plt.show()

"""
for f in range(0,1000,5):
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


import matplotlib.pyplot as plt
import numpy as np

A=1000
signal0=np.fft.ifft(np.concatenate([np.random.randn(A+1)+1j*np.random.randn(A+1),np.zeros(2*A*6),np.random.randn(A)+1j*np.random.randn(A)]))

plt.plot(np.real(signal0))
plt.plot(np.imag(signal0))
plt.show()

corr=np.convolve(signal0,np.conjugate(signal0)[::-1])
plt.plot(np.real(corr))
plt.plot(np.imag(corr))
plt.show()

off=25
# for off in [1,2,3,4,5,6,7,8]:

ph0=0.8
step=10
noise=0.1
signalA=(noise*np.random.randn(len(signal0))+signal0)[::step]
signalB=(noise*np.random.randn(len(signal0))+(signal0*np.exp(1j*np.ones(len(signal0))*ph0)))[off::step]
signalA=signalA[:int(len(signal0)/step-10)]
signalB=signalB[:int(len(signal0)/step-10)]

# plt.subplot(3,1,1)
# plt.plot(np.real(signalA))
# plt.plot(np.imag(signalA))

# plt.subplot(3,1,2)
# plt.plot(np.real(signalB))
# plt.plot(np.imag(signalB))

# corr=np.convolve(signalA,np.conjugate(signalB))
corr=np.convolve(signalA,np.conjugate(signalB)[::-1])
print(len(corr))
# plt.subplot(3,1,3)
plt.title("CORR")
plt.plot(np.real(corr))
plt.plot(np.imag(corr))
plt.show()


specA=np.fft.fft(signalA)
specB=np.fft.fft(signalB)
vec=np.fft.fftshift(specA*np.conjugate(specB))

plt.plot(np.real(vec))
plt.plot(np.imag(vec))
plt.show()

plt.plot(np.angle(vec))
plt.show()

plt.scatter(np.real(vec), np.imag(vec))
plt.show()

vec2=vec[int(len(vec)/4):int(3*len(vec)/4)]
demodVec=vec2[0:-1:]*np.conjugate(vec2[1::])

# plt.plot(np.angle(vec2))
# plt.show()

# plt.subplot(2,1,1)
# plt.plot(np.real(demodVec))
# plt.plot(np.imag(demodVec))
# plt.subplot(2,1,2)
# plt.plot(np.angle(demodVec))
# plt.show()

# plt.scatter(np.real(demodVec), np.imag(demodVec))
# plt.scatter(np.real(np.average(demodVec)), np.imag(np.average(demodVec)))
# plt.show()

print(off)
print(step*len(vec)*np.average(np.angle(demodVec))/(2*np.pi))
print(step*len(vec)*np.angle(np.average(demodVec/np.abs(demodVec)))/(2*np.pi))
print(step*len(vec)*np.angle(np.average(demodVec))/(2*np.pi))
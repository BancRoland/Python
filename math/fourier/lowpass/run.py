import matplotlib.pyplot as plt
import numpy as np

# fs=44100
# fc=400

# N=1000
# f=np.arange(N)/N*fs
# spec=np.concatenate([np.ones(int(fc*2/fs*N)),np.zeros(N-int(fc*2/fs*N))])
# imp=np.fft.fftshift(np.fft.ifft(spec))

# plt.plot(f,spec)
# plt.grid()
# plt.xlabel("frequency [Hz]")
# plt.ylabel("val []")
# plt.show()

# t=np.arange(N)/fs
# plt.plot(t,np.real(imp),label="real")
# plt.plot(t,np.imag(imp),label="imag")
# plt.plot(t,np.abs(imp), linestyle="--", alpha=0.5, color="grey", label="abs")
# plt.plot(t,-np.abs(imp), linestyle="--", alpha=0.5, color="grey")
# plt.legend()
# plt.xlabel("time [sec]")
# plt.ylabel("val []")
# plt.grid()
# plt.show()



fs=44100
fc=800

N=1000
f=np.arange(N)/N*fs
a=int(fc/fs*N)
spec=np.concatenate([np.zeros(1),1j*np.ones(a),np.zeros(N-2*a-1),-1j*np.ones(a)])
imp=np.fft.fftshift(np.fft.ifft(spec))

plt.plot(f,spec)
plt.grid()
plt.xlabel("frequency [Hz]")
plt.ylabel("val []")
plt.show()

t=np.arange(N)/fs
plt.plot(t,np.real(imp),label="real")
plt.plot(t,np.imag(imp),label="imag")
plt.plot(t,np.abs(imp), linestyle="--", alpha=0.5, color="grey", label="abs")
plt.plot(t,-np.abs(imp), linestyle="--", alpha=0.5, color="grey")
plt.legend()
plt.xlabel("time [sec]")
plt.ylabel("val []")
plt.grid()
plt.show()
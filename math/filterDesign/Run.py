import numpy as np
import matplotlib.pyplot as plt

# def FIR_taps(fc,fs,LEN):
#     f=fc/fs
#     # print(f'fc  ={fc}')
#     # print(f'fs  ={fs}')
#     x=np.arange(-LEN//2,LEN//2)+0.5
#     hx=2*fc/fs*np.sin(2*np.pi*f*x)/(2*np.pi*f*x)
#     # plt.plot(np.abs(np.fft.fft(hx)))
#     # plt.show()
#     return(hx)

# def FIR_lpf(v,hx):
#     # out=np.convolve(v,hx, mode='same')
#     out=np.convolve(v,hx, mode='same')
#     return(out)


fc=100e3
fs=800e3
LEN=300

f=fc/fs
x=np.arange(-LEN//2,LEN//2)+0.5
hx0=2*fc/fs*np.sin(2*np.pi*f*x)/(2*np.pi*f*x)
window=1-np.cos(np.arange(0,LEN)/LEN*2*np.pi)
hx=hx0*window
# plt.plot(window)
plt.plot(hx)
plt.plot(np.abs(np.fft.fft(hx)))
plt.show()

# for i in [1, 2, 4, 64, 71]:
for i in [71]:
    I=i-1
    plt.plot(np.arange(len(hx)*(1+i))/(len(hx)*(1+i)),20*np.log10(np.abs(np.fft.fft(np.concatenate([np.zeros(i*len(hx)),hx],)))),'.-', alpha=0.5)
plt.show()

plt.plot(np.real(hx))
plt.plot(np.imag(hx))
plt.plot(np.abs(hx),color="gray",alpha=0.8)
plt.show()

IMP=np.concatenate([np.ones(100),np.zeros(500),np.ones(90)])
hx=np.fft.fftshift(np.fft.ifft(IMP))
plt.plot(np.real(hx))
plt.plot(np.imag(hx))
plt.plot(np.abs(hx),color="gray",alpha=0.8)
plt.show()

plt.plot(20*np.log10(np.abs(np.fft.fft(np.concatenate([np.zeros(10000),hx])))))
plt.show()

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

def FIR_lpf(v,hx):
    out=np.convolve(v,hx, mode='same')
    return(out)

def HannWindow(v):
    wind=(1-np.cos(np.arange(len(v))/len(v)*2*np.pi))/2
    return(wind*v)




fc=100e3
fs=800e3
FIR_LEN=300
SIG_LEN=20000

test=HannWindow(np.ones(SIG_LEN))
plt.plot(test)
plt.show()
plt.plot(20*np.log10(np.abs(np.abs(np.fft.fft(test/SIG_LEN)))))
plt.show()

f=fc/fs
x=np.arange(-FIR_LEN//2,FIR_LEN//2)+0.5
hx0=2*fc/fs*np.sin(2*np.pi*f*x)/(2*np.pi*f*x)
hx=HannWindow(hx0)
# plt.plot(window)

plt.plot(hx0)
plt.plot(np.abs(np.fft.fft(hx0)))
plt.title("original pulse")
plt.grid()
plt.show()

plt.plot(hx)
plt.plot(np.abs(np.fft.fft(hx)))
plt.title("windowed pulse")
plt.grid()
plt.show()

## sum of sines:
# sig=1j*np.zeros(SIG_LEN)
# for f in np.arange(-200000,200000,10000):
# # # for f in [100,200,500,1000,2000,5000,10000,15000]:
# # for f in [1000]:
#     sig=sig+np.exp(1j*2*np.pi*f/fs*np.arange(0,SIG_LEN))
# plt.plot(np.real(sig))
# plt.plot(np.imag(sig))
# plt.show()

# plt.plot(np.fft.fftshift(20*np.log10(np.abs(np.fft.fft(sig/SIG_LEN)))),".-",label="original")
# plt.plot(np.fft.fftshift(20*np.log10(np.abs(np.fft.fft(FIR_lpf(sig/SIG_LEN,hx))))),".-",label="normSig-HannFilt")
# plt.plot(np.fft.fftshift(20*np.log10(np.abs(np.fft.fft(FIR_lpf(sig/SIG_LEN,hx0))))),".-",label="normSig-normFilt")
# plt.plot(np.fft.fftshift(20*np.log10(np.abs(np.fft.fft(FIR_lpf(HannWindow(sig/SIG_LEN),hx0))))),".-",label="HannSig-normFilt")
# plt.plot(np.fft.fftshift(20*np.log10(np.abs(np.fft.fft(FIR_lpf(HannWindow(sig/SIG_LEN),hx))))),".-",label="HannSig-HannFilt")

# plt.grid()
# plt.legend()
# plt.show()


noise=2*np.random.random(SIG_LEN)-1
# plt.title("noise")
# plt.plot(noise)
# plt.plot(FIR_lpf(noise,hx))
# plt.xlabel("time")
# # plt.plot(np.abs(np.fft.fft(FIR_lpf(noise,hx))))
# plt.show()


plt.title("noise")
plt.plot(20*np.log10(np.abs(np.fft.fft(HannWindow(noise)))))
plt.plot(20*np.log10(np.abs(np.fft.fft(HannWindow(FIR_lpf(noise,hx))))))
plt.xlabel("frequency")
# plt.plot(np.abs(np.fft.fft(FIR_lpf(noise,hx))))
plt.show()

for i in [1, 2, 4, 64, 71]:
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




import numpy as np
import matplotlib.pyplot as plt

def HannWindow(v):
    wind=(1-np.cos(np.arange(len(v))/len(v)*2*np.pi))
    return(wind*v)

def FIR_taps(fc,fs,LEN):
    f=fc/fs
    x=np.arange(-LEN//2,LEN//2)+0.5
    hx=2*fc/fs*np.sin(2*np.pi*f*x)/(2*np.pi*f*x)
    return(hx)

def FIR_lpf(v,hx):
    out=np.convolve(v,hx, mode='same')
    return(out)

def myFFT(v):
    out=np.fft.fft(HannWindow(v/len(v)))
    return np.fft.fftshift(out)

def complexPlot(v):
    plt.plot(v,color="black",alpha=0.5)
    plt.plot(np.real(v),"C0")
    plt.plot(np.imag(v),"C1")
    plt.grid()
    plt.show()

def FM_mod(sig_m,alpha):
    out=np.exp(1j*np.zeros(len(sig_m)))
    out[0]=1+1j*0
    for i in range(len(sig_m)-1):
       out[i+1]=out[i]*np.exp(1j*alpha*sig_m[i-1])
    return out


fs=800e3
fm=15000
fc=10e3

FIR_LEN=100
SIG_LEN=64000

hx=FIR_taps(fc,fs,FIR_LEN)
window=(1-np.cos(np.arange(0,len(hx))/len(hx)*2*np.pi))/2
hx=HannWindow(hx)

noise=FIR_lpf(np.random.randn(SIG_LEN),hx)

complexPlot(noise)
plt.plot(np.log10(np.abs(myFFT(noise))))
plt.show()

t=np.arange(0,SIG_LEN)/fs
sig_m=np.sin(2*np.pi*fm*t)
sig_m=noise

alpha=0.5
out=FM_mod(sig_m,alpha)

# out=np.exp(1j*np.zeros(len(sig_m)))
# out[0]=1+1j*0

# alpha=0.5
# for i in range(len(sig_m)-1):
#     out[i+1]=out[i]*np.exp(1j*alpha*sig_m[i-1])

plt.plot(t,sig_m,color="black",alpha=0.5)
plt.plot(t,np.real(out),"C0")
plt.plot(t,np.imag(out),"C1")
plt.grid()
plt.show()

#Carson's Rule
delta_f=sig_m*alpha*fs
f_mod=fc
BW=2*(max(delta_f)+f_mod)
print(f"BW= {BW}")
print(f"f_mod= {f_mod}")
print(f"delta_f= {delta_f}")

plt.plot(20*np.log10(np.abs(myFFT(out))))
# plt.plot(20*np.log10(np.abs(np.fft.fftshift(np.fft.fft(out/len(out))))),alpha=0.5)
plt.show()


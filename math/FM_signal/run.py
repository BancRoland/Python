import numpy as np
import matplotlib.pyplot as plt

def normalize(v):
    return v/max(np.abs(v))

def HannWindow(v):
    wind=(1-np.cos(np.arange(len(v))/len(v)*2*np.pi))/2
    return(wind*v)

def FIR_taps(fc,fs,LEN):
    f=fc/fs
    x=np.arange(-LEN//2,LEN//2)+0.5
    hx=fc/fs*np.sin(2*np.pi*f*x)/(2*np.pi*f*x)
    return(hx)

def FIR_lpf(v,hx):
    out=np.convolve(v,hx, mode='same')
    return(out)

def myFFT(v):
    out=np.fft.fft(HannWindow(v/len(v)))
    return np.fft.fftshift(out)

def myFFTplot(v,fs):
    f=fs*(np.arange(0,len(v))-int(SIG_LEN/2))/len(v)
    out0=np.fft.fft(HannWindow(v/len(v)))
    out0=np.fft.fftshift(out0)
    plt.plot(f,20*np.log10(np.abs(out0)))
    # out1=np.fft.fft(v/len(v))
    # out1=np.fft.fftshift(out1)
    # plt.plot(f,10*np.log10(np.abs(out1)))
    plt.xlabel("frequency [Hz]")
    plt.ylabel("Power [dB]")
    plt.grid()
    # plt.show()

def complexPlot(v):
    plt.plot(v,color="black",alpha=0.5)
    plt.plot(np.real(v),"C0")
    plt.plot(np.imag(v),"C1")
    plt.grid()
    plt.show()

def FM_mod(sig_m,fd,fs):
    alpha=2*np.pi*fd/fs
    out=np.exp(1j*np.zeros(len(sig_m)))
    out[0]=1+1j*0
    for i in range(len(sig_m)-1):
       out[i+1]=out[i]*np.exp(1j*alpha*sig_m[i-1])
    return out


fs=800e3
fm=1000
fc=10e3
fd=75000    # frekvencialöket [Hz]

FIR_LEN=100
SIG_LEN=64000

hx0=FIR_taps(fc,fs,FIR_LEN)
hx=HannWindow(hx0)

random=(2*np.random.random(SIG_LEN)-1)
noise=FIR_lpf(random,hx)
# noise=random

complexPlot(random)
complexPlot(noise)
f=fs*(np.arange(0,SIG_LEN)-int(SIG_LEN/2))/SIG_LEN
plt.plot(f,np.log10(np.abs(myFFT(noise))))
plt.show()

plt.plot(np.fft.fftshift(np.abs(np.fft.fft(hx))))
plt.show()

t=np.arange(0,SIG_LEN)/fs
# sig_m=np.sin(2*np.pi*fm*t)
sig_m=normalize(noise)
# sig_m=np.ones(SIG_LEN)


# complexPlot(sig_m)
myFFTplot(sig_m,fs)
plt.axvline(fc,color="C1",linestyle="--")
plt.axvline(-fc,color="C1",linestyle="--")
plt.xlabel("frequency [Hz]")
plt.ylabel("Power [dB]")
plt.grid()
plt.show()

out=FM_mod(sig_m,fd,fs)


plt.plot(t,np.real(out),"C0")
plt.plot(t,np.imag(out),"C1")
plt.plot(t,sig_m,color="black",alpha=0.5)
plt.grid()
plt.show()

#Carson's Rule
# delta_f=sig_m*alpha*fs

BW=2*(fd+fm)

myFFTplot(out,fs)
plt.axvline(BW/2,color="C1",linestyle="--")
plt.axvline(-BW/2,color="C1",linestyle="--")
plt.show()
# plt.plot(f,20*np.log10(np.abs(myFFT(out))))
# # plt.plot(20*np.log10(np.abs(np.fft.fftshift(np.fft.fft(out/len(out))))),alpha=0.5)
# plt.show()


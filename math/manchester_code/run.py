import numpy as np
import matplotlib.pyplot as plt

fs=44100
fd=1000

data=[0,0,1,0,1,0,1,1,1,0,1,1,1,0,0,0]
data=np.round(np.random.random(100))

def FFT_bandbpass(v,f_min,f_max,fs):
    vspec=np.fft.fft(v)
    # vspec[0:int(len(v)*f_min/fs):]=0
    # vspec[-int(len(v)*f_min/fs)+1::]=0
    vspec[int(len(v)*f_max/fs):-int(len(v)*f_max/fs)+1:]=0
    return np.fft.ifft(vspec)

LEN=100
bit=np.append(np.ones(LEN),-1*np.ones(LEN))

out0=np.array([])

for i in data:
    out0=np.append(out0,(2*i-1)*bit)

out0=np.concatenate([np.zeros(2000), out0, np.zeros(2000)])

plt.plot(data)
plt.show()


out=out0+0.1*np.random.randn(len(out0))
plt.plot(out,color="C1")
plt.plot(out0,color="C0")
plt.show()

if 0:
    # plt.plot(np.log10(np.abs(np.fft.fftshift(np.fft.fft(out)))))
    plt.plot(np.log10(np.abs(np.fft.fft(out))))
    plt.title("spectrum")
    plt.show()

outF=FFT_bandbpass(out,0,1/100,1)

if 0:
    plt.plot(outF)
    plt.title("Filtered")
    plt.show()

plt.subplot(3,1,1)
plt.plot(out,alpha=0.5,color="C2")
plt.plot(outF,alpha=0.5,color="C1")
plt.plot(out0,color="C0")
plt.grid()
plt.subplot(3,1,2)
for i in range(100):
    plt.plot(outF[int(100*np.random.rand())::100],"o",alpha=0.1,color="black")
plt.plot(outF[0::100],"o-",alpha=1,color="C0")
plt.plot(outF[50::100],"o-",alpha=1,color="C1")
plt.grid()
plt.subplot(3,1,3)
for i in range(100):
    phase=int(50*np.random.rand())
    plt.plot(outF[phase:-50:100][:30:]+outF[50+phase:-1:100][:30:],"o",alpha=0.1,color="C0")
    plt.plot(outF[phase:-50:100][:30:]*np.abs(outF[phase:-50:100][:30:])+outF[50+phase:-1:100][:30:]*np.abs(outF[50+phase:-1:100][:30:]),"o",alpha=0.1,color="C1")
    
plt.grid()
plt.show()

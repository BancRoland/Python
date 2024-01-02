import matplotlib.pyplot as plt
import numpy as np



LEN=2**18
INT=100

val=10*np.log10(2* 0.5**3*2/3/LEN)

NoiseSpec = 1j*np.zeros(LEN)
HannNoiseSpec = 1j*np.zeros(LEN)
cw = 1*np.exp(1j*100.5*2*np.pi*np.arange(LEN)/LEN)
# cw = np.zeros(LEN)

def HannWind(v):
    w=(1-np.cos(np.arange(len(v))/len(v)*2*np.pi))/2
    return v*w

def HannSigPow(v):
    signalSpec=np.fft.fftshift(np.fft.fft(HannWind(v))/len(v))
    pow=8/3*signalSpec*np.conj(signalSpec)
    return pow

def SigPow(v):
    signalSpec=np.fft.fftshift(np.fft.fft(v)/len(v))
    pow=signalSpec*np.conj(signalSpec)
    return pow

for i in range(INT):
    noise=cw+1*(np.random.random(LEN)+1j*np.random.random(LEN)-0.5-0.5j)
    NoiseSpec = NoiseSpec + SigPow(noise)
    HannNoiseSpec = HannNoiseSpec + HannSigPow(noise)
    if i == 0:
        plt.plot(np.real(noise))
        plt.plot(np.imag(noise))
        plt.plot(np.abs(noise), "--", color="gray", alpha=0.5)
        plt.plot(-np.abs(noise), "--", color="gray", alpha=0.5)
        plt.show()


# plt.plot(10*np.log10(powSumm/INT))
plt.plot(10*np.log10(NoiseSpec/INT),"o-",alpha=0.8,color="C0")
plt.plot(10*np.log10(HannNoiseSpec/INT),"o-",alpha=0.8,color="C1")
# plt.plot(np.fft.fftshift(NoiseSpec/INT),"o-",alpha=1)
plt.xlabel("frequency []")
plt.ylabel("power [dBr]")
plt.axhline(val,linestyle="--",color="C2")
plt.title(f"avg= {np.average(10*np.log10(np.fft.fftshift(NoiseSpec/INT)))}\ncalculated: {val}")
plt.grid()
plt.show()
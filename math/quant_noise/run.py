import matplotlib.pyplot as plt
import numpy as np

LEN=2**18
INT=100
NoiseSpec=1j*np.zeros(LEN)
# cw = np.exp(1j*10*2*np.pi*np.arange(LEN)/LEN)
cw = np.zeros(LEN)

def HannWind(v):
    w=(1-np.cos(np.arange(len(v))/len(v)*2*np.pi))/2
    return v*w*2
    # return v

for i in range(INT):
    noise=cw+np.random.random(LEN)+1j*np.random.random(LEN)-0.5-0.5j
    signalSpec=np.fft.fftshift(np.fft.fft(noise)/LEN)
    pow=signalSpec*np.conj(signalSpec)
    # pow=np.abs(np.fft.fft(noise/len(noise)))**2
    pow=np.abs(np.fft.fft(HannWind(noise))/len(noise))**2
    NoiseSpec=NoiseSpec+pow
    if i == 0:
        plt.plot(np.real(noise))
        plt.plot(np.imag(noise))
        plt.plot(np.abs(noise), "--", color="gray", alpha=0.5)
        plt.plot(-np.abs(noise), "--", color="gray", alpha=0.5)
        plt.show()

# plt.plot(10*np.log10(powSumm/INT))

plt.plot(NoiseSpec/INT)
# plt.ylim([0,0.2])
plt.xlabel("frequency []")
plt.ylabel("power []")
plt.title(f"avg= {np.average(NoiseSpec/INT)}")
plt.grid()
plt.show()

# plt.plot(10*np.log10(powSumm/INT))
plt.plot(10*np.log10(np.fft.fftshift(NoiseSpec/INT)),"-",alpha=1)
plt.xlabel("frequency []")
plt.ylabel("power [dBr]")
plt.title(f"avg= {np.average(10*np.log10(np.fft.fftshift(NoiseSpec/INT)))}")
plt.grid()
plt.show()
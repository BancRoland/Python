import wave
import argparse
import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np

def LPF(v,a):
    out=1j*np.zeros(len(v))
    out[0]=v[0]
    for i in range(len(v)-1):
        out[i+1]=(1-a)*out[i]+a*v[i+1]
    return out


# parser = argparse.ArgumentParser()
# # parser.add_argument("file", help="file to read")
# parser.add_argument("-f","--file", help="file to read from", nargs='?', type=str, required=True)
# args = parser.parse_args()


# Specify the path to your WAV file
# file_path = 'path/to/your/file.wav'

samplerate, data = wavfile.read("dcf77_hole_minute.wav")

# plt.plot(data)
# plt.show()

# plt.plot(np.abs(np.fft.fft(data)))
# plt.show()

f=74469

mix=np.exp(1j*2*np.pi*f*np.arange(len(data))/len(data))

# plt.plot(np.real(mix))
# plt.plot(np.imag(mix))
# plt.plot(np.abs(mix),color="gray",alpha=0.5)
# plt.plot(-np.abs(mix),color="gray",alpha=0.5)
# plt.show()

data2=data*mix
a=5e-2
data3=LPF(data2,a)
data3=LPF(data3,a)

plt.plot(np.real(data3),label="real")
plt.plot(np.imag(data3),label="imag")
plt.plot(np.abs(data3),color="gray",alpha=0.5,label="abs")
plt.plot(-np.abs(data3),color="gray",alpha=0.5)
plt.grid()
plt.legend()
plt.show()

plt.plot(np.angle(data3),label="phase")
plt.grid()
plt.legend()
plt.show()

# data4=data3[:-1:]*np.conj(data3[1::])

# plt.plot(np.real(data4))
# plt.plot(np.imag(data4))
# plt.plot(np.abs(data4),color="gray",alpha=0.5)
# plt.plot(-np.abs(data4),color="gray",alpha=0.5)
# plt.show()
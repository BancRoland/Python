#!/bin/python3
# import uhd
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
from datetime import datetime
import argparse

import matplotlib
matplotlib.use('Agg')

parser = argparse.ArgumentParser()
# parser.add_argument("file", help="file to read")
parser.add_argument("-f","--file", help="file to read from", nargs='?', type=str, required=True),
parser.add_argument("-l","--length", help="length of FFT", nargs='?', type=int, required=True)
args = parser.parse_args()


now = datetime.now()
dstr = now.strftime("%Y-%m-%d_%H-%M-%S")

length=args.length


def powerSpectrum():
    out= 1j*np.zeros(length)
    P=0
    while True:
      
        samples0=np.fromfile(args.file, dtype=np.uint8, count=2*length, offset=P*2*length)
        samples=samples0[0::2]+1j*samples0[1::2]
        samples=samples-128*(1+1j)

        # plt.figure()
        # plt.plot(np.real(samples))
        # plt.plot(np.imag(samples))
        # plt.plot(np.abs(samples),"--",color="gray",alpha=0.5)
        # plt.grid()
        # plt.show()

        # if np.max(np.abs(np.real(samples))) >=127 or np.max(np.abs(np.imag(samples))) >=127:
        #     print("ADC OVERFLOW!")
        #     plt.figure()
        #     plt.plot(np.real(samples))
        #     plt.plot(np.imag(samples))
        #     plt.plot(np.abs(samples),"--",color="gray",alpha=0.5)
        #     plt.plot(-np.abs(samples),"-",color="gray",alpha=0.5)
        #     plt.axhline(127,linestyle=":")
        #     plt.axhline(-128,linestyle=":")
        #     plt.grid()
        #     plt.show()

        if len(samples) != length:
            print("ERROR")
            return out/P

        P=P+1

        out += np.fft.fftshift(np.abs(fftpack.fft(samples/128/length)))**2



out = powerSpectrum()

plt.figure()
plt.plot(10*np.log10(out))
plt.grid()
plt.xlabel("frequency []")
plt.ylabel("power [dB]")
plt.title("Power Spectrum")
plt.show()
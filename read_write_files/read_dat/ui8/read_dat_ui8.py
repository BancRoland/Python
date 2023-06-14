#!/bin/python3
# import uhd
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
from datetime import datetime
import argparse


parser = argparse.ArgumentParser()
# parser.add_argument("file", help="file to read")
parser.add_argument("-f","--file", help="file to read from", nargs='?', type=str, required=True)
args = parser.parse_args()


now = datetime.now()
dstr = now.strftime("%Y-%m-%d_%H-%M-%S")


# with open("out.dat", mode="rb") as input:
#     samples = input.read()

samples=np.fromfile(args.file, dtype=np.uint8)
# samples=samples0[0::2]+1j*samples0[1::2]

print(len(samples))
# print(samples[0:10])

plt.figure()
plt.plot(samples,'.-')
# plt.plot(np.real(samples),'.-')
# plt.plot(np.imag(samples),'.-')
# plt.plot(np.abs(samples),'--', color='grey', alpha=0.5)
# plt.plot(-np.abs(samples),'--', color='grey', alpha=0.5)
# plt.legend(["Real","Imag","Abs"])
# plt.title(title)
plt.grid()
plt.show()

# plt.figure()
# plt.plot(np.abs(fftpack.fft(samples)))
# plt.show()

# plt.xlabel('xcím')
# plt.ylabel('ycím')
# title=('frq= %.2f MHz \nsamprate= %.2f Msamp/sec \nDate= %s' %(center_freq/1E6,sample_rate/1E6,dstr));
# print(title)
# plt.title(title)
# #plt.legend(['sin(x)','cos(x)'])
# plt.legend()
# plt.grid()
# plt.savefig(dstr+'.png')

#plt.close()


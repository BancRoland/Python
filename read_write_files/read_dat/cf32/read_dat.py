#!/bin/python3
# import uhd
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
from datetime import datetime

now = datetime.now()
dstr = now.strftime("%Y-%m-%d_%H-%M-%S")


# with open("out.dat", mode="rb") as input:
#     samples = input.read()

samples=np.fromfile('c96_384_1x0.bin', dtype=np.complex64)


print(len(samples))
# print(samples[0:10])

plt.figure()
plt.plot(np.real(samples),'.-')
plt.plot(np.imag(samples),'.-')
plt.plot(np.abs(samples),'--', color='grey', alpha=0.5)
plt.plot(-np.abs(samples),'--', color='grey', alpha=0.5)
plt.legend(["Real","Imag","Abs"])
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


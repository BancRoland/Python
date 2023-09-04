#!/bin/python3
# import uhd
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
from datetime import datetime
import argparse

def comp2cui8(v):
    code=np.zeros(len(v)*2)
    code[::2]=np.real(v)+127
    code[1::2]=np.imag(v)+127
    out=code.astype('uint8')
    return out


parser = argparse.ArgumentParser()
# parser.add_argument("file", help="file to read")
parser.add_argument("-f","--file", help="file to read from", nargs='?', type=str, required=True)
args = parser.parse_args()


now = datetime.now()
dstr = now.strftime("%Y-%m-%d_%H-%M-%S")


# with open("out.dat", mode="rb") as input:
#     samples = input.read()

samples0=np.fromfile(args.file, dtype=np.uint8)
samples=samples0[0::2]+1j*samples0[1::2]
samples=samples-128*(1+1j)

# samples=samples[11800:12200]
samp2=np.zeros(len(samples))
samp3=np.zeros(len(samples))

alpha=0.1

for i in range(len(samples)-1):
    samp2[i+1]=samp2[i]*(1-alpha)+alpha*np.abs(samples[i])

for i in range(len(samples)-1):
    samp3[i+1]=np.abs(samples[i+1])-np.abs(samples[i])

# plt.figure()
# # plt.plot(samples,'.-')
# plt.plot(np.real(samples),'.-')
# plt.plot(np.imag(samples),'.-')
# plt.plot(np.abs(samples),'--', color='grey', alpha=0.5)
# plt.plot(-np.abs(samples),'--', color='grey', alpha=0.5)
# plt.legend(["Real","Imag","Abs"])
# # plt.title(title)
# plt.grid()
# plt.show()

# plt.figure()
# # plt.plot(np.abs(samples),'o-')
# # plt.plot(np.abs(samp2),'o-')
# plt.plot(samp3,'o-')
# # plt.legend(["Real","Imag","Abs"])
# plt.grid()
# plt.show()

avg=np.zeros(len(samples))+1j*np.zeros(len(samples))
AVG=50
for i in range(len(samples)-AVG):
    avg[i]=np.mean(np.abs(samples[i:i+AVG]))

plt.figure()
plt.plot(np.abs(samples),'.-')
plt.plot(np.abs(avg),'.-')
plt.legend(["Clear","samples"])
plt.grid()
plt.show()


clear=np.zeros(len(samples))+1j*np.zeros(len(samples))
for i in range(len(samples)):
    # clear[i]=samples[i]
    if(np.abs(samples[i])>=19):
        clear[i]=1

diff=np.zeros(len(samples))
for i in range(len(samples)-1):
    diff[i]=np.abs(samples[i+1])-np.abs(samples[i])

plt.figure()
plt.plot(diff,'.-')
plt.legend(["Clear","samples"])
plt.grid()
plt.show()



plt.figure()
# plt.plot(samples,'.-')
plt.plot(np.real(clear),'.-')
plt.plot(np.imag(clear),'.-')
plt.plot(np.abs(clear),'--', color='grey', alpha=0.5)
plt.plot(-np.abs(clear),'--', color='grey', alpha=0.5)
plt.legend(["Real","Imag","Abs"])
# plt.title(title)
plt.grid()
plt.show()

plt.figure()
# plt.plot(samples,'.-')
plt.plot(np.abs(clear)*127,'.-')
plt.plot(np.abs(samples),'.-')
plt.legend(["Clear","samples"])
plt.grid()
plt.show()

for i in range(len(clear)):
    print(f"{np.abs(clear[i]):.0f}", end ="")
print("")

out=comp2cui8(10*clear)
out.tofile("clear.cui8")


# for P in range(1000):
#     samples0=np.fromfile(args.file, dtype=np.uint8, count=200000, offset=P*200000)
#     samples=samples0[0::2]+1j*samples0[1::2]
#     samples=samples-128*(1+1j)

#     print(len(samples))
#     # print(samples[0:10])

#     plt.figure()
#     plt.plot(np.abs(samples),'o-')
#     # plt.legend(["Real","Imag","Abs"])
#     plt.grid()
#     plt.show()

#     # plt.figure()
#     # # plt.plot(samples,'.-')
#     # plt.plot(np.real(samples),'.-')
#     # plt.plot(np.imag(samples),'.-')
#     # plt.plot(np.abs(samples),'--', color='grey', alpha=0.5)
#     # plt.plot(-np.abs(samples),'--', color='grey', alpha=0.5)
#     # plt.legend(["Real","Imag","Abs"])
#     # # plt.title(title)
#     # plt.grid()
#     # plt.show()

#     # plt.figure()
#     # plt.plot(np.abs(fftpack.fft(samples)))
#     # plt.show()

#     # plt.xlabel('xcím')
#     # plt.ylabel('ycím')
#     # title=('frq= %.2f MHz \nsamprate= %.2f Msamp/sec \nDate= %s' %(center_freq/1E6,sample_rate/1E6,dstr));
#     # print(title)
#     # plt.title(title)
#     # #plt.legend(['sin(x)','cos(x)'])
#     # plt.legend()
#     # plt.grid()
#     # plt.savefig(dstr+'.png')

#     #plt.close()


import numpy as np
import matplotlib.pyplot as plt
import math
import cmath
import struct
import sys

def compPlot(v,title,filename):
    plt.figure()
    plt.plot(np.real(v),'.-')
    plt.plot(np.imag(v),'.-')
    plt.plot(np.abs(v),'--', color='grey', alpha=0.5)
    plt.plot(-np.abs(v),'--', color='grey', alpha=0.5)
    plt.legend(["Real","Imag","Abs"])
    plt.title(title)
    plt.savefig(filename)
    plt.show()

DEBUG=0 #debug mód

print(f'sys.argv[1]= {sys.argv[1]}')
samples0=np.fromfile(sys.argv[1], dtype=np.complex64)

TAPScode=np.conjugate(samples0[::-1])
# samples1=np.trim_zeros(samples) #??? lehet kellene

TAPSfile_name=str(sys.argv[1])[:-4:]+".taps"
print(TAPSfile_name)

if DEBUG:
    title=f"TAPS"
    compPlot(TAPScode,title,"taps.png")
    plt.plot(np.real(TAPScode))
    plt.plot(np.imag(TAPScode))
    plt.show()

# TAPScode=np.conj(codeINC[::-1])
# TAPSfile_name=f'c{len(cplxCode1)}_{RANGE}_1x0.taps'
with open(TAPSfile_name, 'w') as f:
    for i in range(len(TAPScode)):
        if TAPScode[i] == 0j:
            f.write("(0+0j)")
        else:
            f.write(str((TAPScode[i])))
        if i != len(TAPScode)-1:
            f.write(",")
    f.close()



"""

DEBUG=1 #debug mód

RANGE=120
INCVAL=1


# #HEXcodePair=["0x64C4646E", "0x13B3B9B3"]
# HEXcodePair=["0x3B9B919B9131919BE6464C46E646E6EC", "0x91313B313B9B3B31E6464C46E646E6EC"]

# data = np.genfromtxt(fname="data1.txt", delimiter="\t", skip_header=0, filling_values='NaN')	#lineáris chirp
# data = np.genfromtxt(fname="data2.txt", delimiter="\t", skip_header=0, filling_values='NaN')	#nemlin chirp
data = np.genfromtxt(fname="data.csv", delimiter="\t", skip_header=0, filling_values='NaN')	#artillery chirp

print(data)

cplxCode1=data[:,0]+1j*data[:,1]    #[-1.+1.j -1.-1.j -1.+1.j  1.+1.j  1.-1.j ...

code=np.concatenate((cplxCode1,np.zeros(RANGE)))
codeINC=INC(code,INCVAL)

if DEBUG:
    title=f"Alkalmazott komplex kód\n{len(cplxCode1)} db C.KÓD; {RANGE} db NULLA;"
    compPlot(codeINC,title,"fig1.png")

    title=f"Alkalmazott komplex kód atuokorrelációja"
    compPlot(np.correlate(codeINC,codeINC,'full'),title,"fig2.png")

code_cf64=np.zeros(len(codeINC)*2)
code_cf64[::2]=np.real(codeINC)
code_cf64[1::2]=np.imag(codeINC)

code_cf32=code_cf64.astype('float32')


TAPScode=np.conj(codeINC[::-1])
TAPSfile_name=f'c{len(cplxCode1)}_{RANGE}_1x0.taps'
with open(TAPSfile_name, 'w') as f:
    for i in range(len(TAPScode)):
        if TAPScode[i] == 0j:
            f.write("(0+0j)")
        else:
            f.write(str((TAPScode[i])))
        if i != len(TAPScode)-1:
            f.write(",")
    f.close()


bin_name=f'c{len(cplxCode1)}_{RANGE}_1x0.bin'

code_cf32.tofile(bin_name)


if DEBUG:
    f=open("togrc.dat",'rb')
    for i in range(100):
        bites=f.read(4)
        print(struct.unpack('f',bites))
"""
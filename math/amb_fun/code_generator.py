import numpy as np
import matplotlib.pyplot as plt
import math
import cmath
import struct

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

def hex2bin(HEXcode):                                                   #"0x64C4646E"
    bincode=bin(int(HEXcode[2:], 16))[2:].zfill((len(HEXcode)-2)*4)     #"01100100110001000110010001101110"
    BINcode=np.array(list(map(int, bincode)))                           #[0 1 1 0 0 1 0 0 1 1 0 0 0 1 0 0 0 1 1 0 0 1 0 0 0 1 1 0 1 1 1 0]
    return BINcode

def bin2comp(codeRAW):                                          #np.array([0 1 1 0 0 1 0 0 1 1 0 0...
    code2digits=np.reshape(codeRAW, (int(len(codeRAW)/2), 2))   #[[0 1], [1 0], [0 1]...
    codedAng=code2digits[:,0]*2+code2digits[:,1]                #[1 2 1 0 3 0 1 0 1 2 1 0 1 2 3 2]
    cplxCode=np.exp(1j*2*np.pi*(codedAng/4+1/8))*np.sqrt(2)     #[-1.+1.j -1.-1.j -1.+1.j  1.+1.j  1.-1.j ...
    return cplxCode

def hex2comp(HEXcode):
    return bin2comp(hex2bin(HEXcode))

def INC(v,a):
    w=np.array([], dtype=np.complex64)
    #w=np.zeros(len(v)*a)
    for i in v:
        w=np.append(w,np.ones(a)*i)
    return w

# def ROT(v):
#     np.arange(len(v))
#     np.ones(len(v))+1j*np.zeros(len(v))

#     return w


DEBUG=1 #debug mód

RANGE=121
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
# plt.figure()
# plt.plot(np.real(code_cf64))
# plt.plot(np.imag(code_cf64))
# plt.show()
# print(type(code_cf64[0]))

# code_cf32=code_cf64.astype('float32')
code_cf64_N=np.floor(code_cf64/max(np.abs(code_cf64))*32767)
code_ci16=code_cf64_N.astype('int16')

print(code_cf64_N)
print(code_ci16)


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


bin_name=f'c{len(cplxCode1)}_{RANGE}_1x0.ci16'

# code_cf32.tofile(bin_name)
code_ci16.tofile(bin_name)


# if DEBUG:
#     f=open(bin_name,'rb')
#     for i in range(100):
#         bites=f.read(4)
#         print(struct.unpack('s',bites))

# cplxCode1=np.ones(13)+1j*np.zeros(13)

N=10
cplxCode1=INC(cplxCode1,N)
# cplxCode1=np.concatenate((cplxCode1,np.zeros(130-13)))

pic=np.ones((len(cplxCode1)*N, len(cplxCode1)*2-1), dtype=np.complex128)

rot=np.exp(1j*2*3.14159*np.arange(len(cplxCode1))/len(cplxCode1)/N)

for i in range(len(cplxCode1)*N):
    pic[i, :]=np.correlate(cplxCode1*rot**i,cplxCode1,'full')

pic2=np.concatenate((pic[len(cplxCode1):0:-1, :],pic[0:len(cplxCode1), :]))
pic3=np.where(pic2==0,1e-10,pic2)
# pic3=pic2

plt.imshow(np.log10(np.abs(pic3)), aspect='equal', vmin=0, vmax=np.log10(np.max(abs(pic3))))
# plt.imshow(np.log10(np.abs(np.fft.fftshift(pic, axes=0))), aspect='auto', vmin=0, vmax=np.log10(np.max(abs(pic))))
plt.colorbar()
plt.show()







pic=np.ones(np.shape(pic), dtype=np.complex128)


for i in range(len(cplxCode1)):
    pic[i, :]=np.correlate(cplxCode1,cplxCode1,'full')

pic2=np.concatenate((pic[len(cplxCode1):0:-1, :],pic[0:len(cplxCode1), :]))
pic3=np.where(pic2==0,1e-10,pic2)
# pic3=pic2
pic4=np.abs(np.fft.fftshift(np.fft.fft(pic3,axis=0), axes=0))
pic5=np.where(pic4==0,1e-10,pic4)


plt.imshow(np.log10(pic5), aspect='equal', vmin=0, vmax=np.log10(np.max(abs(pic4))))
# plt.imshow(np.log10(np.abs(np.fft.fftshift(pic, axes=0))), aspect='auto', vmin=0, vmax=np.log10(np.max(abs(pic))))
plt.colorbar()
plt.show()

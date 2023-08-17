import numpy as np
import matplotlib.pyplot as plt
import math
import cmath
import struct
import argparse

PI=3.14159
DEBUG_CHRP=0    # plot out the generated raw chirp data
DEBUG_CORR=0    # plot out the correlation function
DEBUG_UAMB=0    # plot out the unambiguity function

parser = argparse.ArgumentParser()
parser.add_argument("-sr","--sr", help="samprate", nargs='?', type=float, required=True)
parser.add_argument("-fmin","--Fmin", help="starting frq", nargs='?', type=float, required=True)
parser.add_argument("-fmax","--Fmax", help="ending frq", nargs='?', type=float, required=True)
parser.add_argument("-C","--codes", help="number of code samples", nargs='?', type=int, required=True)
parser.add_argument("-Z","--zeros", help="number of zero samples", nargs='?', type=int, required=True)
args = parser.parse_args()

sr=args.sr    #[Hz]
fmin=args.Fmin #[Hz]
fmax=args.Fmax  #[Hz]
LEN=args.codes      #[Samp] number of samples
RANGE=args.zeros   #[Samp] number of zeros

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

INCVAL=1
fres=(fmax-fmin)/LEN
print(fres)

print(LEN)
print(len(np.arange(0,fres*LEN,fres)))

f=fmin*np.ones(LEN)+np.arange(0,fres*LEN,fres)
p=np.zeros(LEN)


for i in range(LEN-1):
    p[i+1]=p[i]+2*PI*f[i]/sr

# plt.plot(p)
# plt.show()

cplxCode1=np.exp(1j*p)
if DEBUG_CHRP:
    plt.plot(np.real(cplxCode1),'-')
    plt.plot(np.imag(cplxCode1),'-')
    plt.show()

# DEBUG=0 #debug mód

cplxCode_cf=np.zeros(len(cplxCode1)*2)
cplxCode_cf[::2]=np.real(cplxCode1)
cplxCode_cf[1::2]=np.imag(cplxCode1)

cplxCode_cf32=cplxCode_cf.astype('float32')
bin_name_0=f'c{len(cplxCode1)}.cf32'
cplxCode_cf32.tofile(bin_name_0)



# # cplxCode1=data[:,0]+1j*data[:,1]    #[-1.+1.j -1.-1.j -1.+1.j  1.+1.j  1.-1.j ...

# code=np.concatenate((cplxCode1,np.zeros(RANGE)))
# codeINC=INC(code,INCVAL)

# if DEBUG_CORR:
#     title=f"Alkalmazott komplex kód\n{len(cplxCode1)} db C.KÓD; {RANGE} db NULLA;"
#     compPlot(codeINC,title,"fig1.png")

#     title=f"Alkalmazott komplex kód atuokorrelációja"
#     compPlot(np.correlate(codeINC,codeINC,'full'),title,"fig2.png")

# code_cf64=np.zeros(len(codeINC)*2)
# code_cf64[::2]=np.real(codeINC)
# code_cf64[1::2]=np.imag(codeINC)
# # plt.figure()
# # plt.plot(np.real(code_cf64))
# # plt.plot(np.imag(code_cf64))
# # plt.show()
# # print(type(code_cf64[0]))

# # code_cf32=code_cf64.astype('float32')
# code_cf64_N=np.floor(code_cf64/max(np.abs(code_cf64))*32767)
# code_ci16=code_cf64_N.astype('int16')

# print(code_cf64_N)
# print(code_ci16)


# TAPScode=np.conj(codeINC[::-1])
# TAPSfile_name=f'c{len(cplxCode1)}_{RANGE}_1x0.taps'
# with open(TAPSfile_name, 'w') as f:
#     for i in range(len(TAPScode)):
#         if TAPScode[i] == 0j:
#             f.write("(0+0j)")
#         else:
#             f.write(str((TAPScode[i])))
#         if i != len(TAPScode)-1:
#             f.write(",")
#     f.close()


# bin_name=f'c{len(cplxCode1)}_{RANGE}_1x0.ci16'

# # code_cf32.tofile(bin_name)
# code_ci16.tofile(bin_name)



# # if DEBUG:
# #     f=open(bin_name,'rb')
# #     for i in range(100):
# #         bites=f.read(4)
# #         print(struct.unpack('s',bites))

# # cplxCode1=np.ones(13)+1j*np.zeros(13)

# if DEBUG_UAMB:
#     N=2
#     cplxCode1=INC(cplxCode1,N)
#     # cplxCode1=np.concatenate((cplxCode1,np.zeros(130-13)))

#     pic=np.ones((len(cplxCode1)*N, len(cplxCode1)*2-1), dtype=np.complex128)

#     rot=np.exp(1j*2*3.14159*np.arange(len(cplxCode1))/len(cplxCode1)/N)

#     for i in range(len(cplxCode1)*N):
#         pic[i, :]=np.correlate(cplxCode1*rot**i,cplxCode1,'full')

#     pic2=np.concatenate((pic[-len(cplxCode1):-1, :],pic[0:len(cplxCode1), :]))
#     pic3=np.where(pic2==0,1e-10,pic2)

#     plt.imshow(np.log10(np.abs(pic3)), aspect='equal', vmin=0, vmax=np.log10(np.max(abs(pic3))))
#     # plt.imshow(np.log10(np.abs(np.fft.fftshift(pic, axes=0))), aspect='auto', vmin=0, vmax=np.log10(np.max(abs(pic))))
#     plt.colorbar()
#     plt.show()

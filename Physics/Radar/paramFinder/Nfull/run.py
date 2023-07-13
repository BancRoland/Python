from cProfile import label
import numpy as np
import argparse
import math
import matplotlib.pyplot as plt

def docPars(nC, nZ, nS, srA):

    print(f'{nC*nS/srA*1000}')
    print('\nNcode=[\'Codes\'', end='')
    for i in nC:
        print(f', {i:.0f}', end='')
    print(']')

    print('Nzeros=[\'Zeros\'', end='')
    for i in nZ:
        print(f', {i:.0f}', end='')
    print(']')

    print('dSamp=[\'DoppSamp\'', end='')
    for i in nS:
        print(f', {i:.0f}', end='')
    print(']')

#EZEKET KELLL ÁLLÍTGATNI:
# srA=[10e6]
srA=[100e6, 50e6, 20e6, 10e6]
multA=[1, 3 , 5, 7]   #Hányzorosaikat fogadom el a kettőhatványoknak DopplerMintaszának (1,3,5,7) jöhet szóba




# RmaxVmax=0
vped=1



parser = argparse.ArgumentParser(description="calculate the parameters of an impulse radar")

parser.add_argument("-c","--c", help="speed of wave [m/s] ", nargs='?', type=float, default=299792458)
parser.add_argument("-cFrq","--cFrq", help="Frequency of the carrier wave [Hz] ", nargs='?', type=float, required=True)
parser.add_argument("-sr","--samprate", help="Samplerate of the signalflow [samp/sec] ", nargs='?', type=float, required=True)
parser.add_argument("-Rmn","--RminD", help="Desired minimum distance [m]", nargs='?', type=float, default=1000.0)
parser.add_argument("-Rmx","--RmaxD", help="Desired maximum distance [m]", nargs='?', type=float, default=8000.0)
parser.add_argument("-RT","--TestR", help="Test distance for SNR [m]", nargs='?', type=float, default=1000.0)

args=parser.parse_args()

c=args.c
k=1.38e-23          # Boltzmann constant [J/K]

cFrq=args.cFrq      # centerFrequency [Hz]
sr=args.samprate    # sample rate [samp/sec]

Rmin=args.RminD
Rmax=args.RmaxD
print(f'Rmin=\t{Rmin/1000:.0f} km')
print(f'Rmax=\t{Rmax/1000:.0f} km')


#-------BEAGLE PARAMS-------

TsweepB=0.0005
TburstB=TsweepB*128
VmaxB=c/cFrq/4/TsweepB
VresB=c/cFrq/2/TburstB

Tburst=TburstB
# Tburst=0.03755  #5500m cent.   R*2^k*4/c
# Tburst=0.04096  #6000m cent.   R*2^k*4/c

nf=np.arange(0,2*4*Rmin/c*sr)
r=nf/sr*c/2

print(2*Rmax/c*sr)
print(Rmax)
print(sr)
print(c)
nc=np.zeros(int(np.ceil(2*Rmax/c*sr)+1))
print(np.ceil(2*Rmax/c*sr))
nc=np.append(nc,np.arange(1,1+np.floor(2*Rmin/c*sr)))
nc=np.append(nc,np.floor(2*Rmin/c*sr)*np.ones(len(nf)-len(nc)))


Temp=290      # Temperature for noise [K]
Pow=3.2        # Peak power of the transmitter [Watt]
rcs=0.5        # Radar cross section [m^2]
G_dB=29.5      # Antenna gain [dB]
Gain=10**(G_dB/10.0)
R_test=args.TestR    # Antenna gain [dB]
L=125.9
R_test=Rmax
TLlim=35
lmbd=c/cFrq
SNR_0=Pow*Gain**2*rcs*lmbd**2/((4*math.pi)**3*R_test**4)/(k*Temp)/L
print(SNR_0)


# plt.plot(nf, nc, linestyle='o-')
plt.step(nf, nc, '-', where='post')
plt.axvline(Rmin*2/c*sr, color='k', linestyle='--', linewidth=0.8)
plt.axvline(Rmax*2/c*sr, color='k', linestyle='--', linewidth=0.8)
plt.axvline(Rmin*2*2/c*sr, color='k', linestyle='--', linewidth=0.8)
plt.axvline(Rmax*2*2/c*sr, color='k', linestyle='--', linewidth=0.8)
plt.axvline((Rmax+Rmin)*2/c*sr, color='r', linestyle='--', linewidth=0.8)
plt.ylim(bottom=0)
plt.title("Number of Ones for given periodlength")
plt.ylabel("SNR []")
plt.xlabel("Nf [sample]")
plt.legend()
plt.grid()
plt.show()


plt.step(nf, np.floor(Tburst*c/2/r)*nc/sr*SNR_0, color='0.8', label=f"NAIVE", where='post')
for i in multA:
    k=np.log2(Tburst*c/2/r/i)
    # plt.plot(r,k)
    # plt.plot(r,np.floor(k), color=(0,0,i/7))
    snrV=i*2**np.floor(k)*nc/sr*SNR_0
    plt.step(nf,snrV, label=f"{i:.0f}*2^k", where='post')
plt.axvline(Rmin*2/c*sr, color='k', linestyle='--', linewidth=0.8)
plt.axvline(Rmax*2/c*sr, color='k', linestyle='--', linewidth=0.8)
plt.axvline(Rmin*2*2/c*sr, color='k', linestyle='--', linewidth=0.8)
plt.axvline(Rmax*2*2/c*sr, color='k', linestyle='--', linewidth=0.8)
plt.axvline((Rmax+Rmin)*2/c*sr, color='r', linestyle='--', linewidth=0.8)
plt.ylim(bottom=0)
plt.title("SNR in linear scale for fullen samples")
plt.ylabel("SNR []")
plt.xlabel("Nf [sample]")
plt.legend()
plt.grid()
plt.show()


plt.step(r/2, np.floor(Tburst*c/2/r)*nc/sr*SNR_0, color='0.8', label=f"NAIVE", where='post')
for i in multA:
    k=np.log2(Tburst*c/2/r/i)
    # plt.plot(r,k)
    # plt.plot(r,np.floor(k), color=(0,0,i/7))
    snrV=i*2**np.floor(k)*nc/sr*SNR_0
    plt.step(r/2,snrV, label=f"{i:.0f}*2^k", where='post')
plt.axvline(Rmin, color='k', linestyle='--', linewidth=0.8)
plt.axvline(Rmax, color='k', linestyle='--', linewidth=0.8)
# plt.axvline(Rmin*2, color='k', linestyle='--', linewidth=0.8)
# plt.axvline(Rmax*2, color='k', linestyle='--', linewidth=0.8)
plt.axvline((Rmax+Rmin)/2, color='r', linestyle='--', linewidth=0.8)
plt.ylim(bottom=0)
plt.ylabel("SNR []")
plt.xlabel("Ru/2 [m]")
plt.title("SNR in linear scale for distances")
plt.legend()
plt.grid()
plt.show()


plt.step(nf, 10*np.log10(i*np.floor(Tburst*c/2/r/i)*nc/sr*SNR_0), color='0.8', label=f"NAIVE", where='post')
for i in multA:
    k=np.log2(Tburst*c/2/r/i)
    plt.step(nf, 10*np.log10(i*2**np.floor(k)*nc/sr*SNR_0), label=f"{i:.0f}*2^k", where='post')
    # print(f'Nf for i={i}:\t{max(10*np.log10(i*2**np.floor(k)*nc/sr*SNR_0))}')
plt.xlabel("Nf [samp]")
plt.axvline(Rmin*2/c*sr, color='k', linestyle='--', linewidth=0.8)
plt.axvline(Rmax*2/c*sr, color='k', linestyle='--', linewidth=0.8)
plt.axvline(Rmin*2*2/c*sr, color='k', linestyle='--', linewidth=0.8)
plt.axvline(Rmax*2*2/c*sr, color='k', linestyle='--', linewidth=0.8)
plt.axvline((Rmax+Rmin)*2/c*sr, color='r', linestyle='--', linewidth=0.8)
plt.ylim(bottom=0)
plt.ylabel("SNR [dB]")
plt.title("SNR for fullen samples")
plt.legend()
plt.grid()
plt.show()
import numpy as np
import argparse
import math
import matplotlib.pyplot as plt



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

Temp=290      # Temperature for noise [K]
Pow=3.2        # Peak power of the transmitter [Watt]
rcs=0.5        # Radar cross section [m^2]
G_dB=29.5      # Antenna gain [dB]
Gain=10**(G_dB/10.0)
L=125.9
R_test=Rmax
TLlim=35
lmbd=c/cFrq
SNR_0=Pow*Gain**2*rcs*lmbd**2/((4*math.pi)**3*R_test**4)/(k*Temp)/L
print(SNR_0)

def docPars(nC, nZ, nS, srA, P):
    
    # print('SNR vals=[', end='')
    # for i in np.arange(len(srA)):
    #     # print(10*np.log10(nS[i]*nC[i]/srA[i]*SNR_0))
    #     print(f'{10*np.log10(nS[i]*nC[i]/srA[i]*SNR_0):.1f}', end=' ')
    #     # print(f'{nC[i]*nS[i]/srA[i]*1000:.1f}', end=' ')
    #     # print(f'{nC*nS/srA[i]*1000}', end='')
    # print(']')

    print('SNR=[', end='')
    for i in P:
        print(f' {i:.2f}', end='')
    print(']')

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

    print(f'RZmin={Rmin}')
    print(f'RZmax={Rmax}')


naiveP=[]
naiveC=[]
naiveZ=[]
naiveS=[]

pow2P=[]
pow2C=[]
pow2Z=[]
pow2S=[]

ipow2P=[]
ipow2C=[]
ipow2Z=[]
ipow2S=[]

# svrC=[]
# svrZ=[]
# svrS=[]
        

for sr in srA:

    Nc=np.floor(2*Rmin*sr/c)
    Nz=np.ceil(2*Rmax*sr/c+1)
    dS=Tburst*sr/(Nz+Nc)
    P=10*np.log10(dS*Nc/sr*SNR_0)
    # naive approach

    naiveP=np.append(naiveP,P)
    naiveC=np.append(naiveC,Nc)
    naiveZ=np.append(naiveZ,Nz)
    naiveS=np.append(naiveS,dS)


    #POW2 approach:
    dS=2**np.floor(np.log2(Tburst*c/(2*Rmax)))
    Nf=np.ceil(sr*Tburst/dS)
    Nc=np.floor(min(2*Rmin*sr/c,2*(c*Tburst/dS/2-Rmax)*sr/c))
    Nz=Nf-Nc
    P=10*np.log10(dS*Nc/sr*SNR_0)

    pow2P=np.append(pow2P,P)
    pow2C=np.append(pow2C,Nc)
    pow2Z=np.append(pow2Z,Nz)
    pow2S=np.append(pow2S,dS)

print('\n\n\nNaive approach')
docPars(naiveC, naiveZ, naiveS, srA, naiveP)

# print('\n\n\nPOW2 approach')
# docPars(pow2C, pow2Z, pow2S, srA, pow2P)


print("\n\n\niPOW2 approach:", end=' ')
for j in multA:
    A=np.log2(Tburst*c/2/((Rmin+Rmax)*j))
    # print(np.log2(Tburst*c/2/((Rmin+Rmax)*j)))

    dS=2**np.floor(A)*j  
    Nf=np.floor(sr*Tburst/dS)
    Nc=np.floor(min(2*Rmin*sr/c,2*(Nf/sr*c/2-Rmax)*sr/c))
    Nz=Nf-Nc
    Pfloor=10*np.log10(dS*Nc/sr*SNR_0)

    dS=2**np.ceil(A)*j  
    Nf=np.floor(sr*Tburst/dS)
    Nc=np.floor(min(2*Rmin*sr/c,2*(Nf/sr*c/2-Rmax)*sr/c))
    Nz=Nf-Nc
    Pceil=10*np.log10(dS*Nc/sr*SNR_0)

    if Pfloor > Pceil:
        i=np.floor(A)
    else:
        i=np.ceil(A)


    ipow2P=[]   #POWER
    ipow2C=[]   #CODE
    ipow2Z=[]   #ZEROS
    ipow2S=[]   #SAMPLES


    
    for sr in srA:
        
        dS=2**i*j  
        Nf=np.floor(sr*Tburst/dS)
        Nc=np.floor(min(2*Rmin*sr/c,2*(Nf/sr*c/2-Rmax)*sr/c))
        Nz=Nf-Nc

        P=10*np.log10(dS*Nc/sr*SNR_0)

        ipow2P=np.append(ipow2P,P)
        ipow2C=np.append(ipow2C,Nc)
        ipow2Z=np.append(ipow2Z,Nz)
        ipow2S=np.append(ipow2S,dS)

    print(f'\n\niPOW2 approaches for 2^{i:.0f}*{j}:')
    docPars(ipow2C, ipow2Z, ipow2S, srA, ipow2P)

import numpy as np
import argparse
import math
import matplotlib.pyplot as plt


#EZEKET KELLL ÁLLÍTGATNI:
# srA=[100e6]
srA=[100e6, 50e6, 20e6, 10e6]
multA=[1]   #Hányzorosaikat fogadom el a kettőhatványoknak DopplerMintaszának (1,3,5,7) jöhet szóba




RmaxVmax=0

# def loadbar(a,f):
#     o="|"
#     for i in range(int(f)):
#         if i <= a:
#             o=o+"#"
#         else:
#             o=o+"_"
#     o=o+"|"
#     print(o)


parser = argparse.ArgumentParser(description="calculate the parameters of an impulse radar")

parser.add_argument("-c","--c", help="speed of wave [m/s] ", nargs='?', type=float, default=299792458)
parser.add_argument("-cFrq","--cFrq", help="Frequency of the carrier wave [Hz] ", nargs='?', type=float, required=True)
parser.add_argument("-sr","--samprate", help="Samplerate of the signalflow [samp/sec] ", nargs='?', type=float, required=True)
parser.add_argument("-Rmn","--RminD", help="Desired minimum distance [m]", nargs='?', type=float, default=1000.0)
parser.add_argument("-Rmx","--RmaxD", help="Desired maximum distance [m]", nargs='?', type=float, default=8000.0)
parser.add_argument("-Lat","--Lat", help="centre of interest", nargs='?', type=float, default=47.47046393386676)
parser.add_argument("-Lon","--Lon", help="centre of interest", nargs='?', type=float, default=19.085548731155377)
parser.add_argument("-F","--ffti", help="multiplier of two factor", nargs='?', type=float, default=1)


args=parser.parse_args()

c=args.c
k=1.38e-23          # Boltzmann constant [J/K]

cFrq=args.cFrq      # centerFrequency [Hz]
sr=args.samprate    # sample rate [samp/sec]
ffti=args.ffti

Rmin=args.RminD
Rmax=args.RmaxD
Lat=args.Lat
Lon=args.Lon
# print(f'Rmin=\t{Rmin/1000:.0f} km')
# print(f'Rmax=\t{Rmax/1000:.0f} km')


#-------BEAGLE PARAMS-------

TsweepB=0.0005
TburstB=TsweepB*128
VmaxB=c/cFrq/4/TsweepB
VresB=c/cFrq/2/TburstB

# Tburst=TburstB
# Tburst=0.03755  #5500m cent.   R*2^k*4/c
Tburst=0.04096  #6000m cent.   R*2^k*4/c



naiveC=[]
naiveZ=[]
naiveS=[]

velCell=3 #hanyadik távolságcella az RV mátrixon egy gyalogos

# for i in [1,3,5]:
for j in np.arange(7,12):
    # print(f'{Outer/1000:.3f} km')
    Outer=TburstB*c/2/(2**j*ffti)/2
    Inner=(c/cFrq/2*velCell)*c/2/(2**j*ffti)/2
    print(f'{Lon}, {Lat}, {Inner:.0f}, {Outer:.0f}, 80ffffff, dS= {2**j*ffti} lehetséges DZK')
    # print(f'{(c/cFrq/2*velCell)*c/2/(2**j*i)/2/1000:.3f} km')
    


# for sr in srA:

#     Nc=np.round(2*Rmin*sr/c)
#     Nz=np.round(2*Rmax*sr/c)
#     print(f"\n\n---sr=\t{sr/1e6} MS/s---\n\n")
#     print("\nNaive approach:")
#     # print(f'Ncode=\t{Nc:.0f}\t->\t{Nc*c/sr/2:.2f} m\nNzeros=\t{Nz:.0f}\t->\t{(Nz)*c/sr/2:.2f} m')
#     # print(f'dSamp=\t{TburstB*sr/(Nz+Nc):.2f}')
    
#     print(f'dSamp=\t{Tburst*sr/(Nz+Nc):.0f}')
#     print(f'\nNfull=\t{Nc+Nz:.0f}')
#     print(f'Ncode=\t{Nc:.0f}')
#     print(f'Nzeros=\t{Nz:.0f}')
#     print(f'\nRu=\t{(Nc+Nz)/sr*c/2/1000:.3f} km')
#     print(f'Rmin=\t{Nc*c/sr/2/1000:.3f} km')
#     print(f'Rmax=\t{Nz*c/sr/2/1000:.3f} km')

    
#     # Ncode=['Codes',3336,625,250,125]
#     # Nzeros=['Zeros',5000,2500,1000,500]
#     # dSamp=['DoppSamp',1024, 1024, 1024, 1024]

#     naiveC=np.append(naiveC,Nc)
#     naiveZ=np.append(naiveZ,Nz)
#     naiveS=np.append(naiveS,Tburst*sr/(Nz+Nc))


#     print("\nFFT approach:")
#     for j in multA:
#         print(f'\n######-------dSamp MULTIP=\t{j}\t-------######\n')
#         # print(f'log2(TburstB*c/(4*Rmax*{j}))={np.log2(TburstB*c/(4*Rmax*j)):.2f}')
#         # print(f'log2(TburstB*c/(4*Rmax*{j}))={np.log2(TburstB*c/(4*Rmin*j)):.2f}')
#         if np.ceil(np.log2(Tburst*c/(4*Rmax*j)))==np.ceil(np.log2(Tburst*c/(4*Rmin*j))):    #megadott tartományba nem esik bele 2^x-el osztott fulltáv
#             print(f"NO SOLUTIONS FOR 2^n*{j}!")
#         else:
#             # print(f"Solutions for 2^n*{j}:")
#             for i in np.arange(np.ceil(np.log2(Tburst*c/(4*Rmax*j))),np.ceil(np.log2(Tburst*c/(4*Rmin*j)))):
#                 print(f'\n-------------Solutions for 2^{i:.0f}*{j}:')
#                 # print(f'Ru=\t{TburstB/(2**i*j)*c/2:.2f}')
#                 # print(f'Rc=\t{TburstB/(2**i*j)*c/4:.2f}')
#                 # print(f'Rmin\t<\tRc\t<\tRmax')
#                 # print(f'{Rmin}\t<\t{TburstB/(2**i*j)*c/4:.2f}\t<\t{Rmax}')
#                 NfFrac=sr*Tburst/(2**i*j)
#                 # print(f'Nfrac=\t{NfFrac:.2f}')
#                 # print(f'dS=\t2^{i:.0f}*{j} = {2**i*j:.0f} Samples\t->\tRu=\t{c*TburstB/(2**i*j)/2/1000:,.3f} km')
#                 if np.floor(NfFrac) == np.ceil(NfFrac):
#                     Nf=[NfFrac]
#                 else:
#                     Nf=[np.floor(NfFrac),np.ceil(NfFrac)]
#                 # print(f'Possible Nfull=\t[{np.floor(NfFrac):.0f} ... {np.ceil(NfFrac):.0f}]')         
#                 for k in Nf:
#                     print(f'\ndSamp=\t{2**i*j:.0f}={2**i:.0f}*{j}')
#                     print(f'\nNfull=\t{k:.0f}')
#                     Nc1=max(Nc,k-Nz)
#                     print(f'Ncode=\t{Nc1:.0f}')
#                     print(f'Nzeros=\t{k-Nc1:.0f}')
#                     print(f'\nRu=\t{k/sr*c/2/1000:.3f} km')
#                     print(f'Rmin=\t{Nc1*c/sr/2/1000:.3f} km')
#                     print(f'Rmax=\t{(k-Nc1)*c/sr/2/1000:.3f} km')
#                     # print(f'\nRmax/Rmin=\t{(k-Nc1)/Nc1:.2f}')
#                     # print(np.floor((k-Nc1)/Nc1))
#                     # print(np.ceil((k-Nc1)/Nc1))
#                     # print(k/np.floor((k-Nc1)/Nc1))
#                     # print(k/np.ceil((k-Nc1)/Nc1))
#                     print(f'\n-------')

# print('\n\n\nNaive approaches')
# print('\nNcode=[\'Codes\'', end='')
# for i in naiveC:
#     print(f', {i:.0f}', end='')
# print(']')

# print('Nzeros=[\'Zeros\'', end='')
# for i in naiveZ:
#     print(f', {i:.0f}', end='')
# print(']')

# print('dSamp=[\'DoppSamp\'', end='')
# for i in naiveS:
#     print(f', {i:.0f}', end='')
# print(']')

                    
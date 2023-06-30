import numpy as np
import argparse
import math
import matplotlib.pyplot as plt

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

parser.add_argument("-c","--c", help="speed of wave [m/s] ", nargs='?', type=float, default=3e8)
parser.add_argument("-cFrq","--cFrq", help="Frequency of the carrier wave [Hz] ", nargs='?', type=float, required=True)
parser.add_argument("-sr","--samprate", help="Samplerate of the signalflow [samp/sec] ", nargs='?', type=float, required=True)
parser.add_argument("-Nc","--Ncode", help="code samples number [samples] ", nargs='?', type=int, required=True)
parser.add_argument("-Nz","--Nzeros", help="zero samples number [samples] ", nargs='?', type=int, required=True)
parser.add_argument("-dS","--dSamp", help="doppler samples number [line of samples] ", nargs='?', type=int, required=True)
parser.add_argument("-dD","--dDec", help="doppler decimation value [samples] ", nargs='?', type=int, default=1)
parser.add_argument("-T","--Temp", help="Temperature for noise [K]", nargs='?', type=int, default=290)
parser.add_argument("-P","--Pow", help="Peak power of the transmitter [Watt]", nargs='?', type=float, default=1.0)
parser.add_argument("-RCS","--RCS", help="Radar cross section of a target [m^2]", nargs='?', type=float, default=1.0)
parser.add_argument("-G","--Gain", help="Antenna gain [dB]", nargs='?', type=float, default=1.0)
parser.add_argument("-RT","--TestD", help="Test distance for SNR [m]", nargs='?', type=float, default=0.0)


# parser.add_argument("-r","--radius", help="radius of the circle", nargs='?', type=float, const=1, default=7, required=True)

# parser.add_argument("-pi","--pi", help="the ratio called pi", nargs='?', type=float, const=1, default=3.14159)

args=parser.parse_args()
# answer=args.radius**2*args.pi

c=args.c
k=1.38e-23          # Boltzmann constant [J/K]

cFrq=args.cFrq      # centerFrequency [Hz]
sr=args.samprate    # sample rate [samp/sec]
Ncode=args.Ncode    # correlation code samples []
Nzeros=args.Nzeros  # zeros for range []
dSamp=args.dSamp    # dopplerSamples
dDec=args.dDec      # doppler decimation value
Temp=args.Temp      # Temperature for noise [K]
Pow=args.Pow        # Peak power of the transmitter [Watt]
rcs=args.RCS        # Radar cross section [m^2]
G_dB=args.Gain      # Antenna gain [dB]
R_test=args.TestD    # Antenna gain [dB]


print("\n-------------Wave-------------")
print(f'c= \t\t\033[1m{c:,} m/s\033[0m'.replace(',', ' '))
print(f'cFrq= \t\t\033[1m{cFrq/1e9} GHz\033[0m')
lmbd=c/cFrq
print(f'lambda= \t\033[1m{lmbd} m\033[0m')

print("\n-------------CODE-------------")
print(f'samprate= \t\033[1m{sr/1e6} MHz\033[0m')
print(f'Codes= \t\t\033[1m{Ncode} samp\033[0m')
print(f'Zeros= \t\t\033[1m{Nzeros} samp\033[0m')
fullLen=Ncode+Nzeros
print(f'Full length= \t\033[1m{fullLen} samp\033[0m')
PRF=sr/fullLen
print(f'PRF= \t\t\033[1m{PRF/1000:.2f} kHz\033[0m')
fillFactor=100*Ncode/fullLen
print(f'FillFactor= \t\033[1m{fillFactor:.2f} %\033[0m')
# loadbar(fillFactor/2,100/2)
print(f'doppler Samples= \t\033[1m{dSamp} \033[0m')
print(f'doppler Decimation= \t\033[1m{dDec} \033[0m')

print("\n-------------OPERATION-------------")
R_min=Ncode/sr*c/2
print(f'Min Range= \t\033[1m{R_min:,.2f} m \033[0m'.replace(',', ' '))
R_unamb=fullLen/sr*c/2
print(f'Unamb. range=\t\033[1m{R_unamb:,.2f} m \033[0m'.replace(',', ' '))
R_max=Nzeros/sr*c/2
print(f'Max Range= \t\033[1m{R_max:,} m \033[0m'.replace(',', ' '))
rangeRes=fullLen/sr*c/2/fullLen
print(f'Range Res= \t\033[1m{rangeRes:.2f} m\033[0m')
blindSpeed=PRF*c/cFrq/2/dDec
print(f'Blind speed= \t\033[1m{blindSpeed:.2f} m/sec = {blindSpeed*3.6:.2f} km/h\033[0m')
vmax=blindSpeed/2
print(f'Max velocity= \t\033[1m+-{vmax:.2f} m/sec = {vmax*3.6:.2f} km/h\033[0m')
print(f'velocity res= \t\033[1m{blindSpeed/dSamp:.2f} m/sec = {blindSpeed/dSamp*3.6:.2f} km/h\033[0m\n')
print(f'minimal time in one range cell= \t\033[1m{rangeRes/vmax:.2f} sec\033[0m')
print(f'max possible doppler samples= \t\033[1m{rangeRes/vmax*sr/fullLen:.0f}\033[0m\n')    #so the target doesnt get out of the range resolution
print(f'')
print(f'max possible velocity without spreading = \t\033[1m{rangeRes/(dDec*dSamp*(fullLen/sr)):.2f} m/sec \t= {rangeRes/(dDec*dSamp*(fullLen/sr))*3.6:.2f} km/h\033[0m')    #so the target doesnt get out of the range resolution

print("\n-------------Power factors-------------")
print(f'RCS =               \033[1m{rcs:.2f} m^2\033[0m')
print(f'Peak power= \t\033[1m{Pow:.2f} Watt\033[0m')
P_avg=Pow*fillFactor/100
print(f'Average power= \t\033[1m{P_avg:.2f} Watt\033[0m')
Bdop=PRF/dDec/dSamp
print(f'Noise power= \t\033[1m{k*sr*Temp*1e12:.2f} fW\033[0m')
Pnoise=k*Bdop*Temp
# print(f'Noise power for one cell= \t\033[1m{Pnoise:.2f} Watt\033[0m')
print(f'Target RCS= \t\033[1m{rcs:.2f} m^2\033[0m')
print(f'Ant gain= \t\033[1m{G_dB:.2f} dB\033[0m')
Gain=10**(G_dB/10.0)

print(f'')
print(f'Theorical maximum Range= \t\033[1m{math.pow((P_avg*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*k*Temp*Bdop),1/4):,.0f} m\033[0m'.replace(',', ' '))
L=125.9
TH=20.9
print(f'Maximum Range with losses= \t\033[1m{math.pow((P_avg*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*k*Temp*Bdop*L*TH),1/4):,.0f} m\033[0m'.replace(',', ' '))

Pmax=(P_avg*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*R_max**4)
print(f'')
print(f'SNR value at:')
print(f'MAX dist=    \033[1m{10*math.log10(Pmax/Pnoise/L):.2f} dB\033[0m')
Pmin=(P_avg*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*R_min**4)
print(f'MIN dist=    \033[1m{10*math.log10(Pmin/Pnoise/L):.2f} dB\033[0m')


if R_test!=0.0:
    Ptest=(P_avg*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*R_test**4)
    print(f'\033[1m{R_test:.0f} m\033[0m =     \033[1m{10*math.log10(Ptest/Pnoise/L):.2f} dB\033[0m')

print(f'')
print(f'Threshold=   \033[1m{10*math.log10(TH):.2f} dB\033[0m')
print(f'NoiseLevel=  \033[1m{10*math.log10(L):.2f} dB\033[0m')



R=np.arange(rangeRes,2*R_unamb,rangeRes)
Pnoise_dB=10*np.log10(Pnoise)
PnoiseLoss_dB=10*np.log10(Pnoise*L)
PnoiseTrsh_dB=10*np.log10(Pnoise*L*TH)

# for rcs in [0.5, 10, 100]:
#     P_refl=(P_avg*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*R**4)
#     P_refl_dB=10*np.log10(P_refl)
#     plt.plot(R,P_refl_dB,'-.', color=(0,0,0))
# plt.axvline(x=R_min, color='r', linestyle='-')
# plt.axvline(x=R_max, color='b', linestyle='-')
# plt.axvline(x=R_unamb, color='k', linestyle='-')
# plt.axhline(Pnoise_dB, color='k', linestyle='-')
# plt.axhline(PnoiseLoss_dB, color='k', linestyle='-')
# plt.axhline(PnoiseTrsh_dB, color='k', linestyle='-')
# plt.xlim([0,2*R_unamb])
# # plt.yscale('log')
# plt.grid(True)
# plt.show()

plt.figure(figsize=(8, 5))
TLlim=35
RCSs=[0.5, 5, 100]
RCStext=[f"Ember     RCS=","Autó        RCS=","FTS          RCS="]
for i in range(len(RCSs)):
    P_refl=(P_avg*Gain**2*RCSs[i]*lmbd**2)/((4*math.pi)**3*R**4)
    P_refl_dB=10*np.log10(P_refl)
    plt.plot(R,P_refl_dB-PnoiseLoss_dB,'-', color=(i%3/3,(i+1)%3/3,(i+2)%3/3))
plt.axvline(x=R_min, color='g', linestyle='--')
plt.text(R_min, 1, f'R_min', rotation=90, fontsize = 10, color='g', va='baseline', ha='right')
plt.axvline(x=R_max, color='r', linestyle='--')
plt.text(R_max, 1, f'R_max', rotation=90, fontsize = 10, color='r', va='baseline', ha='right')
plt.axvline(x=R_unamb, color='k', linestyle='-')
plt.text(R_unamb, 1, f'R_unamb', rotation=90, fontsize = 10, color='k', va='baseline', ha='left')
plt.axhline(13.2, color='k', linestyle=':')
plt.text(0, 13.2+1, 'Original Threshold = 13.2 dB', fontsize = 10, va='baseline', ha='left')
plt.axhline(TLlim, color='k', linestyle=':')
plt.text(0, TLlim+1, f'TL limit = {TLlim} dB', fontsize = 10, va='baseline', ha='left')
# plt.axhline(PnoiseLoss_dB, color='k', linestyle='-')
# plt.axhline(PnoiseTrsh_dB, color='k', linestyle='-')
plt.xlim([0,R_unamb])
plt.ylim([0,80])
# plt.yscale('log')
plt.legend([RCStext[i]+str(RCSs[i])+" m^2" for i in range(3)])
plt.grid(True)
plt.xlabel("céltárgy távolság [m]")
plt.ylabel("SNR [dB]")
plt.title("SNR értékek adott céltárgyakra", fontsize = 20)
plt.savefig('plot.png')
plt.show()

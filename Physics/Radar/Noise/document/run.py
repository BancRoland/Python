import numpy as np
import argparse
import math
import matplotlib.pyplot as plt

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


def rowPrint(v,dec,mult=1):   #rowname    multiplier(for km and such)     decimal places
    print(v[0], end="\t")
    for i in range(len(v)-1):
        print(f'{v[i+1]/mult:.{dec}f}', end="\t")
    print()


parser = argparse.ArgumentParser(description="calculate the parameters of an impulse radar")

parser.add_argument("-c","--c", help="speed of wave [m/s] ", nargs='?', type=float, default=299792458)
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
parser.add_argument("-RT","--TestR", help="Test distance for SNR [m]", nargs='?', type=float, default=0.0)


#EZEKET KELLL ÁLLÍTGATNI:
Ncode=['Codes', 615, 308, 123, 61]
Nzeros=['Zeros', 947, 474, 189, 95]
dSamp=['DoppSamp', 4096, 4096, 4096, 4096]




args=parser.parse_args()
# answer=args.radius**2*args.pi

RT1=5000
RT2=6000

c=args.c
k=1.38e-23          # Boltzmann constant [J/K]

col=4
L=125.9
TH=20.9

cFrq=9.9e9      # centerFrequency [Hz]
sr=['samprate [MS/s]',100e6, 50e6, 20e6, 10e6]    # sample rate [samp/sec]

dDec=['DoppDec',1, 1, 1, 1]      # doppler decimation value
Temp=290      # Temperature for noise [K]
Pow=3.2        # Peak power of the transmitter [Watt]
rcs=0.5        # Radar cross section [m^2]
G_dB=29.5      # Antenna gain [dB]
Gain=10**(G_dB/10.0)
R_test=args.TestR    # Antenna gain [dB]

fullLen=['Full length',0,0,0,0]
PRF=['PRF [kHz]',0,0,0,0]
fillFactor=['FillFactor [%]',0,0,0,0]
R_min=['R_min [km]',0,0,0,0]
R_unamb=['R_u [km]',0,0,0,0]
R_max=['R_max [km]',0,0,0,0]
rangeRes=['R_res [m]',0,0,0,0]
blindSpeed=['v_blind [km/h]',0,0,0,0]
vmax=['v_max [km/h]',0,0,0,0]
vres=['v_res [km/h]',0,0,0,0]
Tc=['T_coh [msec]',0,0,0,0]
P_avg=['P_avg',0,0,0,0]
Bdop=['Bdop',0,0,0,0]
Pnoise=['-',0,0,0,0]
SNRmax=[f'SNR(Rmax,ped) [dB]',0,0,0,0]
SNRmin=[f'SNR(Rmin,ped) [dB]',0,0,0,0]
SNR_T1=[f'SNR({RT1/1000:.0f}km,ped) [dB]',0,0,0,0]
SNR_T2=[f'SNR({RT2/1000:.0f}km,ped) [dB]',0,0,0,0]




# RmaxD=args.RmaxD
# RminD=args.RminD

# RmaxD=8000
# RminD=1000
# RumbD=RmaxD+RminD

#-------BEAGLE PARAMS-------

TsweepB=0.0005
TburstB=TsweepB*128
VmaxB=c/cFrq/4/TsweepB
VresB=c/cFrq/2/TburstB

lmbd=c/cFrq



for i in np.arange(1,col+1):
    fullLen[i]=Ncode[i]+Nzeros[i]
    PRF[i]=sr[i]/fullLen[i]  #T=fullen/sr
    fillFactor[i]=100*Ncode[i]/fullLen[i]
    R_min[i]=Ncode[i]/sr[i]*c/2
    R_unamb[i]=fullLen[i]/sr[i]*c/2
    R_max[i]=Nzeros[i]/sr[i]*c/2 #=c*Nzeros*T0/2
    rangeRes[i]=c/sr[i]/2
    blindSpeed[i]=PRF[i]*c/cFrq/2/dDec[i]#=lmbda/(2*T)/dDec
    vmax[i]=blindSpeed[i]/2
    vres[i]=blindSpeed[i]/dSamp[i]
    Tc[i]=dDec[i]*dSamp[i]*fullLen[i]/sr[i]
    P_avg[i]=Pow*fillFactor[i]/100
    Bdop[i]=PRF[i]/dDec[i]/dSamp[i]
    Pnoise[i]=k*Bdop[i]*Temp
    Pmax=(P_avg[i]*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*R_max[i]**4)
    SNRmax[i]=10*math.log10(Pmax/Pnoise[i]/L)
    Pmin=(P_avg[i]*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*R_min[i]**4)
    SNRmin[i]=10*math.log10(Pmin/Pnoise[i]/L)



for i in range(4):
    Ptest=(P_avg[i+1]*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*RT1**4)
    SNR_T1[i+1]=10*math.log10(Ptest/Pnoise[i+1]/L)
    Ptest=(P_avg[i+1]*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*RT2**4)
    SNR_T2[i+1]=10*math.log10(Ptest/Pnoise[i+1]/L)
    # print(f'SNR({RT/1000:.0f}km,ped) [dB]\t\033[1m{10*math.log10(Ptest/Pnoise/L):.1f}\033[0m')




rowPrint(sr,0,1e6)
rowPrint(Ncode,0)
rowPrint(Nzeros,0)
rowPrint(dSamp,0)
rowPrint(dDec,0)
rowPrint(fullLen,0)
rowPrint(PRF,1,1000)
rowPrint(fillFactor,1)
rowPrint(rangeRes,2)
rowPrint(R_min,3,1000)
rowPrint(R_max,3,1000)
rowPrint(R_unamb,3,1000)
rowPrint(vres,2,1/3.6)
rowPrint(blindSpeed,0,1/3.6)
rowPrint(vmax,0,1/3.6)
rowPrint(Tc,1,1/1000)
rowPrint(SNRmin,2)
rowPrint(SNRmax,2)
rowPrint(SNR_T1,2)
rowPrint(SNR_T2,2)

# for i in range(len(Table)):
#     print(Table[i][0], end="\t")
#     for j in range(4):
#         print(Table[i][j+1], end="\t")
#         rowPrint(Table)
#     print("")

# print(Table[i][0], end="\t")
# for j in range(4):
#     print(Table[i][j+1], end="\t")
#     rowPrint()
# print("")

    # print(Ncode[i], end='   ')
    # print(Nzeros[i], end='   ')
    # print(dSamp[i], end='   ')
    # print(dDec[i], end='   ')
    # print(fullLen[i], end='   ')
    # print(PRF[i], end='   ')
    # print(fillFactor[i], end='   ')


# print(f'SNR(Rmax,ped) [dB]\t\033[1m{10*math.log10(Pmax/Pnoise/L):.1f}\033[0m')
# print(f'SNR(Rmin,ped) [dB]\t\033[1m{10*math.log10(Pmin/Pnoise/L):.1f}\033[0m')


for srA in np.arange(1,5):
    R=np.arange(rangeRes[srA],2*R_unamb[srA],rangeRes[srA])
    Pnoise_dB=10*np.log10(Pnoise[srA])
    PnoiseLoss_dB=10*np.log10(Pnoise[srA]*L)
    PnoiseTrsh_dB=10*np.log10(Pnoise[srA]*L*TH)

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
        P_refl=(P_avg[srA]*Gain**2*RCSs[i]*lmbd**2)/((4*math.pi)**3*R**4)
        P_refl_dB=10*np.log10(P_refl)
        plt.plot(R,P_refl_dB-PnoiseLoss_dB,'-', color=(i%3/3,(i+1)%3/3,(i+2)%3/3))
    plt.axvline(x=R_min[srA], color='g', linestyle='--')
    plt.text(R_min[srA], 1, f'R_min', rotation=90, fontsize = 10, color='g', va='baseline', ha='right')
    plt.axvline(x=R_max[srA], color='r', linestyle='--')
    plt.text(R_max[srA], 1, f'R_max', rotation=90, fontsize = 10, color='r', va='baseline', ha='right')
    plt.axvline(x=R_unamb[srA], color='k', linestyle='-')
    plt.text(R_unamb[srA], 1, f'R_unamb', rotation=90, fontsize = 10, color='k', va='baseline', ha='left')
    plt.axhline(13.2, color='k', linestyle=':')
    plt.text(0, 13.2+1, 'Original limit = 13.2 dB', fontsize = 10, va='baseline', ha='left')
    plt.axhline(TLlim, color='k', linestyle=':')
    plt.text(0, TLlim+1, f'TL limit = {TLlim} dB', fontsize = 10, va='baseline', ha='left')
    # plt.axhline(PnoiseLoss_dB, color='k', linestyle='-')
    # plt.axhline(PnoiseTrsh_dB, color='k', linestyle='-')
    plt.xlim([0,R_unamb[srA]])
    plt.ylim([0,80])
    # plt.yscale('log')
    plt.legend([RCStext[i]+str(RCSs[i])+" m^2" for i in range(3)])
    plt.grid(True)
    plt.xlabel("céltárgy távolság [m]")
    plt.ylabel("SNR [dB]")
    plt.title("SNR értékek adott céltárgyakra", fontsize = 20)
    bbox_props = dict(boxstyle="square", facecolor="white", edgecolor="gray", alpha=0.9)
    plt.text(0, 80, f'sr=   {sr[srA]/1e6:.1f} MHz\nNc=   {Ncode[srA]}\nNz=    {Nzeros[srA]}\ndS=   {dSamp[srA]}\ndD=    {dDec[srA]}', fontsize = 10, va='top', ha='left', bbox=bbox_props)
    plt.savefig(f'plot_{sr[srA]/1e6:.0f}.png')
    plt.show()


    plt.figure(figsize=(8, 5))
    V=np.arange(vres[srA]/100,10*vres[srA],10*vres[srA]/100)

    Vbeag=c/cFrq/2/TburstB
    Tcoh=lmbd/2/V
    # plt.axvline(x=R_min, color='g', linestyle='--')
    # plt.text(R_min, 1, f'R_min', rotation=90, fontsize = 10, color='g', va='baseline', ha='right')
    plt.axhline(y=vres[srA]*3.6, color='k', linestyle='--')
    plt.axvline(x=Tc[srA], color='k', linestyle='--')

    # plt.axhline(y=3.6/10, color='g', linestyle='--')
    # plt.axhline(y=Vbeag*3.6, color='r', linestyle='--')
    plt.plot([0, 2*TburstB], [Vbeag*3.6, Vbeag*3.6], color='r', linestyle='--', label='Beagle')
    plt.plot([TburstB, TburstB], [0, 2*Vbeag*3.6], color='r', linestyle='--')

    plt.plot([0, 2*TburstB], [vres[srA]*3.6, vres[srA]*3.6,], color='k', linestyle='--', label='Kuvik')
    plt.plot([Tc[srA], Tc[srA]], [0, 2*Vbeag*3.6], color='k', linestyle='--')
    # plt.text(R_max, 1, f'R_max', rotation=90, fontsize = 10, color='r', va='baseline', ha='right')
    # plt.axvline(x=R_unamb, color='k', linestyle='-')
    # plt.text(R_unamb, 1, f'R_unamb', rotation=90, fontsize = 10, color='k', va='baseline', ha='left')

    # plt.axhline(13.2, color='k', linestyle=':')
    # plt.text(0, 13.2+1, 'Original Threshold = 13.2 dB', fontsize = 10, va='baseline', ha='left')
    # plt.axhline(TLlim, color='k', linestyle=':')
    # plt.text(0, TLlim+1, f'TL limit = {TLlim} dB', fontsize = 10, va='baseline', ha='left')
    # # plt.axhline(PnoiseLoss_dB, color='k', linestyle='-')
    # # plt.axhline(PnoiseTrsh_dB, color='k', linestyle='-')
    plt.xlim([0,2*TburstB])
    plt.ylim([0,2*Vbeag*3.6])
    # # plt.yscale('log')
    # plt.legend([RCStext[i]+str(RCSs[i])+" m^2" for i in range(3)])
    plt.legend()
    plt.plot(Tcoh,V*3.6,'-')
    plt.plot(Tc[srA],vres[srA]*3.6, 'ko',)
    plt.grid(True)
    plt.xlabel("koherenciaidő [sec]")
    plt.ylabel("sebességfelbontás [km/h]")
    plt.title("Koherenciaidő és sebességfelbontás kapcsolata", fontsize = 20)
    plt.text(0.001, 2*Vbeag*3.6*0.99, f'sr= {sr[srA]/1e6:.1f} MHz\nNc= {Ncode[srA]}\nNz= {Nzeros[srA]}\ndS= {dSamp[srA]}\ndD= {dDec[srA]}', fontsize = 10, va='top', ha='left', bbox=bbox_props)
    # plt.savefig('plot.png')
    plt.show()

    if RmaxVmax:
        plt.figure(figsize=(8, 5))
        R=np.arange(0,10*R_max[srA],rangeRes[srA])
        Vm=(c**2)/(8*cFrq*R*dDec)
        plt.axhline(y=vmax*3.6, color='k', linestyle='--')
        plt.axvline(x=R_max[srA], color='k', linestyle='--')
        plt.plot(R,Vm*3.6,'o-')
        plt.grid(True)
        plt.xlabel("R_max [m]")
        plt.ylabel("V_max [km/h]")
        plt.title("R_max és V_max kapcsolata", fontsize = 20)
        # plt.savefig('plot.png')
        plt.show()
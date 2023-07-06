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


parser = argparse.ArgumentParser(description="calculate the parameters of an impulse radar")

parser.add_argument("-c","--c", help="speed of wave [m/s] ", nargs='?', type=float, default=299792458)
parser.add_argument("-cFrq","--cFrq", help="Frequency of the carrier wave [Hz] ", nargs='?', type=float, required=True)
parser.add_argument("-sr","--samprate", help="Samplerate of the signalflow [samp/sec] ", nargs='?', type=float, required=True)
# parser.add_argument("-Nc","--Ncode", help="code samples number [samples] ", nargs='?', type=int, required=True)
# parser.add_argument("-Nz","--Nzeros", help="zero samples number [samples] ", nargs='?', type=int, required=True)
# parser.add_argument("-dS","--dSamp", help="doppler samples number [line of samples] ", nargs='?', type=int, required=True)
# parser.add_argument("-dD","--dDec", help="doppler decimation value [samples] ", nargs='?', type=int, default=1)
# parser.add_argument("-T","--Temp", help="Temperature for noise [K]", nargs='?', type=int, default=290)
# parser.add_argument("-P","--Pow", help="Peak power of the transmitter [Watt]", nargs='?', type=float, default=1.0)
# parser.add_argument("-RCS","--RCS", help="Radar cross section of a target [m^2]", nargs='?', type=float, default=1.0)
# parser.add_argument("-G","--Gain", help="Antenna gain [dB]", nargs='?', type=float, default=1.0)
# parser.add_argument("-RT","--TestR", help="Test distance for SNR [m]", nargs='?', type=float, default=0.0)
parser.add_argument("-Rmn","--RminD", help="Desired minimum distance [m]", nargs='?', type=float, default=1000.0)
parser.add_argument("-Rmx","--RmaxD", help="Desired maximum distance [m]", nargs='?', type=float, default=8000.0)



# parser.add_argument("-r","--radius", help="radius of the circle", nargs='?', type=float, const=1, default=7, required=True)

# parser.add_argument("-pi","--pi", help="the ratio called pi", nargs='?', type=float, const=1, default=3.14159)

args=parser.parse_args()
# answer=args.radius**2*args.pi

c=args.c
k=1.38e-23          # Boltzmann constant [J/K]

cFrq=args.cFrq      # centerFrequency [Hz]
sr=args.samprate    # sample rate [samp/sec]
# Ncode=args.Ncode    # correlation code samples []
# Nzeros=args.Nzeros  # zeros for range []
# dSamp=args.dSamp    # dopplerSamples
# dDec=args.dDec      # doppler decimation value
# Temp=args.Temp      # Temperature for noise [K]
# Pow=args.Pow        # Peak power of the transmitter [Watt]
# rcs=args.RCS        # Radar cross section [m^2]
# G_dB=args.Gain      # Antenna gain [dB]
# R_test=args.TestR    # Antenna gain [dB]

Rmin=args.RminD
Rmax=args.RmaxD
print(Rmin)
print(Rmax)
# print(Rmax1)
# print(Rmax2)


# RmaxD=8000
# RminD=1000
Rumb=Rmax+Rmin

#-------BEAGLE PARAMS-------

TsweepB=0.0005
TburstB=TsweepB*128
VmaxB=c/cFrq/4/TsweepB
VresB=c/cFrq/2/TburstB

dS=c*TburstB/2/Rumb
# print(f'Rumb1={Rumb1}')
# print(f'dSamp1={dS1}')

# Nc1=np.ceil(2*Rmin1*sr/c)
# Nc2=np.floor(2*Rmin2*sr/c)
# Nz1=np.ceil(2*Rmax1*sr/c)
# Nz2=np.floor(2*Rmax2*sr/c)
Nc=2*Rmin*sr/c
Nz=2*Rmax*sr/c
# print("\nPeremfeltétlek alapján adódó hosszak")
# print(f'Nc1=\t{Nc1:.0f}')
# print(f'Nc2=\t{Nc2:.0f}')
# print(f'Nz1=\t{Nz1:.0f}')
# print(f'Nz2=\t{Nz2:.0f}')

print("\nNaive approach:")
print(f'Ncode=\t{Nc:.0f}\t->\t{Nc*c/sr/2:.2f} m\nNzeros=\t{Nz:.0f}\t->\t{(Nz)*c/sr/2:.2f} m')
print(f'dSamp=\t{TburstB*sr/(Nz+Nc):.2f}')

# for i in np.arange(10,20):
#     for j in np.arange(0,5):
#         print(f'{(2*j+1)*TburstB*c/2/2**i:,.2f}'.replace(',', ' '), end='\t')
#     print('')

for j in [1,3,5,7,9]:
    print(f'\n-----dSamp MULTIP=\t{j}')
    print(f'log2(2*Nc1/{j})={np.log2(2*Nc/j):.2f}')
    print(f'log2(2*Nz2/{j})={np.log2(2*Nz/j):.2f}')
    if np.ceil(np.log2(2*Nc/j))==np.ceil(np.log2(2*Nz/j)):    #megadott tartományba nem eseik bele 2^x-el osztott fulltáv
        print(f"NO SOLUTIONS FOR 2^n*{j}!")
    else:
        print(f"Solutions for 2^n*{j}:")
        for i in np.arange(np.ceil(np.log2(0.5*Nc/j)),np.ceil(np.log2(0.5*Nz/j))):
            NfFrac=sr*TburstB/(2**i*j)
            print(NfFrac)
            print(f'dS=\t2^{i:.0f}*{j} = {2**i*j:.0f} Samples\t->\tRu=\t{c*TburstB/(2**i*j)/2/1000:,.3f} km')
            # print(f'{NfFrac}')
            # print(f'{np.floor(NfFrac)}')
            # print(f'{np.ceil(NfFrac)}')
            if np.floor(NfFrac) == np.ceil(NfFrac):
                Nf=[NfFrac]
            else:
                Nf=[np.floor(NfFrac),np.ceil(NfFrac)]
            print(f'Possible Nfull=\t[{np.floor(NfFrac):.0f} ... {np.ceil(NfFrac):.0f}]')         
            for k in Nf:
                print(f'\nNfull=\t{k:.0f}')
                Nc1=max(Nc,k-Nz)
                # Nc20=min(Nc,k-Nz)
                # print(f'Nc10=\t{Nc10}')
                # print(f'Nc20=\t{Nc20}')
                print(f'Possible Nc=\t{Nc1:.0f}')
                print(f'Ncode=\t{Nc1:.0f}\t->\t{Nc1*c/sr/2:.2f} m\nNzeros=\t{k-Nc1:.0f}\t->\t{(k-Nc1)*c/sr/2:.2f} m\ndSamp=\t{2**i*j:.0f}\t->\t{2**i:.0f}*{j}')

# print(f'\nlog2(dSamp1/3)={np.log2(dS1/3)}')
# print(f'log2(dSamp2/3)={np.log2(dS2/3)}')
# if np.ceil(np.log2(dS1/3))==np.ceil(np.log2(dS2/3)):
#     print("NO SOLUTIONS FOR 2^n*3!")
# else:
#     print("Solutions for 2^n*3:")
#     for i in np.arange(np.ceil(np.log2(dS2/3)),np.ceil(np.log2(dS1/3))):
#         print(i)

# print(f'\nlog2(dSamp1/5)={np.log2(dS1/5)}')
# print(f'log2(dSamp2/5)={np.log2(dS2/5)}')
# if np.ceil(np.log2(dS1/5))==np.ceil(np.log2(dS2/5)):
#     print("NO SOLUTIONS FOR 2^n*5!")
# else:
#     print("Solutions for 2^n*5:")
#     for i in np.arange(np.ceil(np.log2(dS2/5)),np.ceil(np.log2(dS1/5))):
#         print(i)

# dS11=2**np.floor(np.log2(dS1))
# print(f'dS11={dS11}\tRu={c*TburstB/dS11}')

# Nfull11=(c*TburstB/dS11)/(c/sr)
# print(f'Nfull11=\t{np.floor(Nfull11):.2f}')
# print(f'Ruamb11=\t{np.floor(Nfull11)/sr*c:.2f}')

# Nc11=Nfull11*Rmin1/Rumb1
# print(f'Nc11=\t{np.floor(Nc11):.2f} samp\t->\t{np.floor(Nc11)/sr*c:.2f} m')
# Nz11=Nfull11-np.floor(Nc11)
# print(f'Nz11=\t{Nz11:.2f} samp\t->\t{Nz11/sr*c:.2f} m')


# print(f'Nmin12=\t{np.ceil(Nfull11*Rmin1/Rumb1):.2f}')
# print(f'Rmin12=\t{np.ceil(Nfull11*Rmin1/Rumb1)/sr*c:.2f}')


# print(f'Ruamb12={np.ceil(Nfull11)/sr*c:.2f}')


# print(f'log2(dSamp1/3)={np.log2(dS1/3)}')
# print(f'log2(dSamp1/5)={np.log2(dS1/5)}')

# dS2=c*TburstB/Rumb2
# print(f'dSamp2={dS2}')
# print(f'log2(dSamp2)={np.log2(dS2)}'),
# print(f'log2(dSamp2/3)={np.log2(dS2/3)}')
# print(f'log2(dSamp2/5)={np.log2(dS2/5)}')

# print("\n-------------Wave-------------")
# print(f'c= \t\033[1m{c:,} m/s\033[0m'.replace(',', ' '))
# print(f'cFrq= \t\033[1m{cFrq/1e9} GHz\033[0m')
# lmbd=c/cFrq
# print(f'lambda= \t\033[1m{lmbd:.3f} m\033[0m')

# print("\n-------------For given expectations-------------")
# # print(f'fullLen*dSamp*dDec should be= \t\033[1m{lmbd*sr/2/VresB:,.2f}\033[0m'.replace(',', ' '))
# dSampD=2*VmaxB/VresB
# print(f'dSamp should be= \t\033[1m{dSampD:.2f} samp\033[0m')
# # print(f'fullLen*dDec should be= \t\033[1m{lmbd*sr/4/VmaxB:.2f} samp\033[0m')
# NzerosD=2*sr*RmaxD/c
# print(f'Nzeros should be= \t\033[1m{NzerosD:.2f} samp\033[0m')
# NonesD=2*sr*RminD/c
# print(f'Ncodes should be= \t\033[1m{NonesD:.2f} samp\033[0m')
# NfullD=NonesD+NzerosD
# print(f'Nfull should be= \t\033[1m{NfullD:.2f} samp\033[0m')
# dDecD=lmbd*sr/4/VmaxB/NfullD
# print(f'dDec should be= \t\033[1m{dDecD:.2f}\033[0m')
# print(f'dDec*dSamp should be= \t\033[1m{dDecD*dSampD:.2f}\033[0m')
# print(f'Nfull should be (if range is flexible)= \t\033[1m{lmbd*sr/2/VresB/(np.floor(dDecD)*dSampD):.2f} samp\033[0m')
# print(f'Nzeros should be (if range is flexible)= \t\033[1m{lmbd*sr/2/VresB/(np.floor(dDecD)*dSampD)-NonesD:.2f} samp\033[0m'),
# print(f'Nzeros should be (based on input dSamp*dDec)= \t\033[1m{lmbd*sr/2/VresB/(dSamp*dDec)-NonesD:.2f} samp\033[0m')

# # print(f'For Beagle equiv full length should be= \t\033[1m{} samp\033[0m')


# print("\n-------------CODE-------------")
# print(f'samprate= \t\033[1m{sr/1e6} MHz\033[0m')
# print(f'Codes= \t\033[1m{Ncode} samp\033[0m')
# print(f'Zeros= \t\033[1m{Nzeros} samp\033[0m')
# fullLen=Ncode+Nzeros
# print(f'Full length= \t\033[1m{fullLen} samp\033[0m')
# PRF=sr/fullLen  #T=fullen/sr
# print(f'PRF= \t\033[1m{PRF/1000:.2f} kHz\033[0m')
# fillFactor=100*Ncode/fullLen
# print(f'FillFactor= \t\033[1m{fillFactor:.2f} %\033[0m')
# # loadbar(fillFactor/2,100/2)
# print(f'doppler Samples= \t\033[1m{dSamp} \033[0m')
# print(f'doppler Decimation= \t\033[1m{dDec} \033[0m')

# print("\n-------------OPERATION-------------")
# R_min=Ncode/sr*c/2
# print(f'Min Range= \t\033[1m{R_min:,.2f} m\033[0m'.replace(',', ' '))
# R_unamb=fullLen/sr*c/2
# print(f'Unamb. range=\t\033[1m{R_unamb:,.2f} m\033[0m'.replace(',', ' '))
# R_max=Nzeros/sr*c/2 #=c*Nzeros*T0/2
# print(f'Max Range= \t\033[1m{R_max:,.2f} m\033[0m'.replace(',', ' '))
# rangeRes=c/sr/2#=T0*c/2
# print(f'Range Res= \t\033[1m{rangeRes:.2f} m\033[0m')
# blindSpeed=PRF*c/cFrq/2/dDec#=lmbda/(2*T)/dDec
# print(f'Blind speed= \t\033[1m{blindSpeed:.2f} m/sec = {blindSpeed*3.6:.2f} km/h\033[0m')
# vmax=blindSpeed/2
# print(f'Max velocity= \t\033[1m+-{vmax:.2f} m/sec = {vmax*3.6:.2f} km/h\033[0m')
# vres=blindSpeed/dSamp
# print(f'velocity res= \t\033[1m{vres:.2f} m/sec = {vres*3.6:.2f} km/h\033[0m\n')
# # print(f'minimal time in one range cell= \t\033[1m{rangeRes/vmax:.2f} sec\033[0m')
# print(f'max possible doppler samples for max speed= \t\033[1m{rangeRes/vmax*sr/fullLen/dDec:.0f}\033[0m')    #so the target doesnt get out of the range resolution
# print(f'max possible doppler samples for res speed= \t\033[1m{rangeRes/vres*sr/fullLen/dDec:.0f}\033[0m')    #so the target doesnt get out of the range resolution
# Tc=dDec*dSamp*fullLen/sr
# print(f'Time coherence required= \t\033[1m{Tc:.3f} sec\033[0m\n')    #so the target stays coherent

# print(f'')
# print(f'max possible velocity without spreading = \t\033[1m{rangeRes/(dDec*dSamp*(fullLen/sr)):.2f} m/sec = {rangeRes/(dDec*dSamp*(fullLen/sr))*3.6:.2f} km/h\033[0m')    #so the target doesnt get out of the range resolution

# print("\n-------------Power factors-------------")
# print(f'RCS =\t\033[1m{rcs:.2f} m^2\033[0m')
# print(f'Peak power= \t\033[1m{Pow:.2f} Watt\033[0m')
# P_avg=Pow*fillFactor/100
# print(f'Average power= \t\033[1m{P_avg:.2f} Watt\033[0m')
# Bdop=PRF/dDec/dSamp
# print(f'Noise power= \t\033[1m{k*sr*Temp*1e12:.2f} fW\033[0m')
# Pnoise=k*Bdop*Temp
# # print(f'Noise power for one cell= \t\033[1m{Pnoise:.2f} Watt\033[0m')
# print(f'Target RCS= \t\033[1m{rcs:.2f} m^2\033[0m')
# print(f'Ant gain= \t\033[1m{G_dB:.2f} dB\033[0m')
# Gain=10**(G_dB/10.0)

# print(f'')
# print(f'Theoretical maximum Range= \t\033[1m{math.pow((P_avg*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*k*Temp*Bdop),1/4):,.0f} m\033[0m'.replace(',', ' '))
# L=125.9
# TH=20.9
# print(f'Maximum Range with losses= \t\033[1m{math.pow((P_avg*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*k*Temp*Bdop*L*TH),1/4):,.0f} m\033[0m'.replace(',', ' '))

# Pmax=(P_avg*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*R_max**4)
# print(f'')
# print(f'SNR value at:')
# print(f'MAX dist=\t\033[1m{10*math.log10(Pmax/Pnoise/L):.2f} dB\033[0m')
# Pmin=(P_avg*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*R_min**4)
# print(f'MIN dist=\t\033[1m{10*math.log10(Pmin/Pnoise/L):.2f} dB\033[0m')

# Ptest=(P_avg*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*2000**4)
# print(f'At 2000 m\033[0m =\t\033[1m{10*math.log10(Ptest/Pnoise/L):.2f} dB\033[0m')

# Ptest=(P_avg*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*3000**4)
# print(f'At 3000 m\033[0m =\t\033[1m{10*math.log10(Ptest/Pnoise/L):.2f} dB\033[0m')


# if R_test!=0.0:
#     Ptest=(P_avg*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*R_test**4)
#     print(f'At \033[1m{R_test:.0f} m\033[0m =\t\033[1m{10*math.log10(Ptest/Pnoise/L):.2f} dB\033[0m'),

# print(f'')
# print(f'Threshold=\t\033[1m{10*math.log10(TH):.2f} dB\033[0m')
# print(f'Losses=\t\033[1m{10*math.log10(L):.2f} dB\033[0m')



# R=np.arange(rangeRes,2*R_unamb,rangeRes)
# Pnoise_dB=10*np.log10(Pnoise)
# PnoiseLoss_dB=10*np.log10(Pnoise*L)
# PnoiseTrsh_dB=10*np.log10(Pnoise*L*TH)

# # for rcs in [0.5, 10, 100]:
# #     P_refl=(P_avg*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*R**4)
# #     P_refl_dB=10*np.log10(P_refl)
# #     plt.plot(R,P_refl_dB,'-.', color=(0,0,0))
# # plt.axvline(x=R_min, color='r', linestyle='-')
# # plt.axvline(x=R_max, color='b', linestyle='-')
# # plt.axvline(x=R_unamb, color='k', linestyle='-')
# # plt.axhline(Pnoise_dB, color='k', linestyle='-')
# # plt.axhline(PnoiseLoss_dB, color='k', linestyle='-')
# # plt.axhline(PnoiseTrsh_dB, color='k', linestyle='-')
# # plt.xlim([0,2*R_unamb])
# # # plt.yscale('log')
# # plt.grid(True)
# # plt.show()

# plt.figure(figsize=(8, 5))
# TLlim=35
# RCSs=[0.5, 5, 100]
# RCStext=[f"Ember     RCS=","Autó        RCS=","FTS          RCS="]
# for i in range(len(RCSs)):
#     P_refl=(P_avg*Gain**2*RCSs[i]*lmbd**2)/((4*math.pi)**3*R**4)
#     P_refl_dB=10*np.log10(P_refl)
#     plt.plot(R,P_refl_dB-PnoiseLoss_dB,'-', color=(i%3/3,(i+1)%3/3,(i+2)%3/3))
# plt.axvline(x=R_min, color='g', linestyle='--')
# plt.text(R_min, 1, f'R_min', rotation=90, fontsize = 10, color='g', va='baseline', ha='right')
# plt.axvline(x=R_max, color='r', linestyle='--')
# plt.text(R_max, 1, f'R_max', rotation=90, fontsize = 10, color='r', va='baseline', ha='right')
# plt.axvline(x=R_unamb, color='k', linestyle='-')
# plt.text(R_unamb, 1, f'R_unamb', rotation=90, fontsize = 10, color='k', va='baseline', ha='left')
# plt.axhline(13.2, color='k', linestyle=':')
# plt.text(0, 13.2+1, 'Original Threshold = 13.2 dB', fontsize = 10, va='baseline', ha='left')
# plt.axhline(TLlim, color='k', linestyle=':')
# plt.text(0, TLlim+1, f'TL limit = {TLlim} dB', fontsize = 10, va='baseline', ha='left')
# # plt.axhline(PnoiseLoss_dB, color='k', linestyle='-')
# # plt.axhline(PnoiseTrsh_dB, color='k', linestyle='-')
# plt.xlim([0,R_unamb])
# plt.ylim([0,80])
# # plt.yscale('log')
# plt.legend([RCStext[i]+str(RCSs[i])+" m^2" for i in range(3)])
# plt.grid(True)
# plt.xlabel("céltárgy távolság [m]")
# plt.ylabel("SNR [dB]")
# plt.title("SNR értékek adott céltárgyakra", fontsize = 20)
# plt.text(R_unamb*0.99, 10, f'sr= {sr/1e6:.1f} MHz\nNc= {Ncode}\nNz= {Nzeros}\ndS= {dSamp}\ndD= {dDec}', fontsize = 10, va='bottom', ha='right')
# plt.savefig('plot.png')
# plt.show()


# plt.figure(figsize=(8, 5))
# V=np.arange(vres/100,10*vres,10*vres/100)

# Vbeag=c/cFrq/2/TburstB
# Tcoh=lmbd/2/V
# # plt.axvline(x=R_min, color='g', linestyle='--')
# # plt.text(R_min, 1, f'R_min', rotation=90, fontsize = 10, color='g', va='baseline', ha='right')
# plt.axhline(y=vres*3.6, color='k', linestyle='--')
# plt.axvline(x=Tc, color='k', linestyle='--')

# # plt.axhline(y=3.6/10, color='g', linestyle='--')
# # plt.axhline(y=Vbeag*3.6, color='r', linestyle='--')
# plt.plot([0, 2*TburstB], [Vbeag*3.6, Vbeag*3.6], color='r', linestyle='--', label='Beagle')
# plt.plot([TburstB, TburstB], [0, 2*Vbeag*3.6], color='r', linestyle='--')

# plt.plot([0, 2*TburstB], [vres*3.6, vres*3.6,], color='k', linestyle='--', label='Kuvik')
# plt.plot([Tc, Tc], [0, 2*Vbeag*3.6], color='k', linestyle='--')
# # plt.text(R_max, 1, f'R_max', rotation=90, fontsize = 10, color='r', va='baseline', ha='right')
# # plt.axvline(x=R_unamb, color='k', linestyle='-')
# # plt.text(R_unamb, 1, f'R_unamb', rotation=90, fontsize = 10, color='k', va='baseline', ha='left')

# # plt.axhline(13.2, color='k', linestyle=':')
# # plt.text(0, 13.2+1, 'Original Threshold = 13.2 dB', fontsize = 10, va='baseline', ha='left')
# # plt.axhline(TLlim, color='k', linestyle=':')
# # plt.text(0, TLlim+1, f'TL limit = {TLlim} dB', fontsize = 10, va='baseline', ha='left')
# # # plt.axhline(PnoiseLoss_dB, color='k', linestyle='-')
# # # plt.axhline(PnoiseTrsh_dB, color='k', linestyle='-')
# plt.xlim([0,2*TburstB])
# plt.ylim([0,2*Vbeag*3.6])
# # # plt.yscale('log')
# # plt.legend([RCStext[i]+str(RCSs[i])+" m^2" for i in range(3)])
# plt.legend()
# plt.plot(Tcoh,V*3.6,'-')
# plt.plot(Tc,vres*3.6, 'ko',)
# plt.grid(True)
# plt.xlabel("koherenciaidő [sec]")
# plt.ylabel("sebességfelbontás [km/h]")
# plt.title("Koherenciaidő és sebességfelbontás kapcsolata", fontsize = 20)
# plt.text(0.001, 2*Vbeag*3.6*0.99, f'sr= {sr/1e6:.1f} MHz\nNc= {Ncode}\nNz= {Nzeros}\ndS= {dSamp}\ndD= {dDec}', fontsize = 10, va='top', ha='left')
# # plt.savefig('plot.png')
# plt.show()

# if RmaxVmax:
#     plt.figure(figsize=(8, 5))
#     R=np.arange(0,10*R_max,rangeRes)
#     Vm=(c**2)/(8*cFrq*R*dDec)
#     plt.axhline(y=vmax*3.6, color='k', linestyle='--')
#     plt.axvline(x=R_max, color='k', linestyle='--')
#     plt.plot(R,Vm*3.6,'o-')
#     plt.grid(True)
#     plt.xlabel("R_max [m]")
#     plt.ylabel("V_max [km/h]")
#     plt.title("R_max és V_max kapcsolata", fontsize = 20)
#     # plt.savefig('plot.png')
#     plt.show()
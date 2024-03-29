import numpy as np
import argparse
import math
import matplotlib.pyplot as plt
import subprocess
import csv


# RmaxVmax=0




def rowPrint(v,dec,file,mult=1):   #rowname    multiplier(for km and such)     decimal places
        file.write(f"{v[0]}\t")
        for i in range(len(v)-1):
            file.write(f'{v[i+1]/mult:.{dec}f}\t')
        file.write("\n")


parser = argparse.ArgumentParser(description="calculate the parameters of an impulse radar")

parser.add_argument("-c","--c", help="speed of wave [m/s] ", nargs='?', type=float, default=299792458)
parser.add_argument("-cFrq","--cFrq", help="carrier Frq [Hz] ", nargs='?', type=float, default=1000)
parser.add_argument("-RT","--TestR", help="Test distance for SNR [m]", nargs='?', type=float, default=0.0)
parser.add_argument("-DIR","--DIR", help="Beam azimut direction [deg]", nargs='?', type=float, default=0.0)
parser.add_argument("-BW","--BW", help="Beam azimuth width [deg]", nargs='?', type=float, default=0.0)
# -FA $Fa -FL $Fl -FALT $FAlt -FDIR $Fdir
parser.add_argument("-FA","--FA", help="Geological altitude [deg]", nargs='?', type=float, default=0.0)
parser.add_argument("-FL","--FL", help="Geological longitude [deg]", nargs='?', type=float, default=0.0)
parser.add_argument("-FALT","--FALT", help="viewpoint height [m]", nargs='?', type=float, default=10000.0)
parser.add_argument("-FDIR","--FDIR", help="wievpoint tilt [deg]", nargs='?', type=float, default=0.0)

parser.add_argument("-RZMIN","--RZMIN", help="wievpoint tilt [deg]", nargs='?', type=float, default=0.0)
parser.add_argument("-RZMAX","--RZMAX", help="wievpoint tilt [deg]", nargs='?', type=float, default=0.0)
parser.add_argument("-FLDRN","--FLDRN", help="Foldername", nargs='?', type=str, default="unnamed")

args=parser.parse_args()
BW=args.BW
DIR=args.DIR
c=args.c
R_test=args.TestR    # Antenna gain [dB]
Fa=args.FA
Fl=args.FL
FAlt=args.FALT
FDir=args.FDIR
fldrN=args.FLDRN
cFrq=args.cFrq      # centerFrequency [Hz]


RZmin=args.RZMIN
RZmax=args.RZMAX

Centre=f"{Fa}, {Fl}"



sr=['samprate [MS/s]']
Ncode=['Codes']
Nzeros=['Zeros']
dSamp=['DoppSamp']

with open('input.csv', newline='') as f:
    reader = csv.reader(f, delimiter='\t')
    sr=next(reader)
    Ncode=next(reader)
    Nzeros=next(reader)
    dSamp=next(reader)

for i in range(len(sr)-1):
    sr[i+1]=eval(sr[i+1])
    Ncode[i+1]=eval(Ncode[i+1])
    Nzeros[i+1]=eval(Nzeros[i+1])
    dSamp[i+1]=eval(dSamp[i+1])



k=1.38e-23          # Boltzmann constant [J/K]

col=4
L=125.9
TH=20.9



dDec=['DoppDec', 1, 1, 1, 1]      # doppler decimation value
Temp=290      # Temperature for noise [K]
Pow=3.2        # Peak power of the transmitter [Watt]
rcs=0.5        # Radar cross section [m^2]
G_dB=29.5      # Antenna gain [dB]
Gain=10**(G_dB/10.0)

fullLen=['N_F []',0,0,0,0]
PRF=['PRF [Hz]',0,0,0,0]
fc=['f_c [Hz]',0,0,0,0]
fillFactor=['FillFactor [%]',0,0,0,0]
R_min=['R_min [m]',0,0,0,0]
R_unamb=['R_u [m]',0,0,0,0]
R_max=['R_max [m]',0,0,0,0]
r_res=['R_res [m]',0,0,0,0]
blindSpeed=['v_blind [m/s]',0,0,0,0]
vmax=['v_max [m/s]',0,0,0,0]
vres=['v_res [m/s]',0,0,0,0]
T_c=['T_c [msec]',0,0,0,0]
T0=['T_0 [msec]',0,0,0,0]
T_B=['T_B [msec]',0,0,0,0]
v_c=['v_c [m/s]',0,0,0,0]
P_avg=['P_avg',0,0,0,0]
Bdop=['Bdop',0,0,0,0]
Pnoise=['-',0,0,0,0]
SNRmax=[f'SNR(Rmax,ped) [dB]',0,0,0,0]
SNRmin=[f'SNR(Rmin,ped) [dB]',0,0,0,0]
SNR_T1=[f'SNR({RZmin:.0f}m,ped) [dB]',0,0,0,0]
SNR_T2=[f'SNR({RZmax:.0f}m,ped) [dB]',0,0,0,0]



#-------BEAGLE PARAMS-------

TsweepB=0.0005
TburstB=TsweepB*128
VmaxB=c/cFrq/4/TsweepB
VresB=c/cFrq/2/TburstB

lmbd=c/cFrq

# print(Gain**2*lmbd**2/((4*math.pi)**3*R_test**4)/(k*Temp)/L)

print(cFrq)
print(fullLen)
print(sr)

for i in np.arange(1,len(sr)):
    fc[i]=cFrq
    fullLen[i]=Ncode[i]+Nzeros[i]
    T0[i]=fullLen[i]/sr[i]
    T_B[i]=T0[i]*dSamp[i]
    PRF[i]=sr[i]/fullLen[i]  #T=fullen/sr
    fillFactor[i]=100*Ncode[i]/fullLen[i]
    R_min[i]=Ncode[i]/sr[i]*c/2
    R_unamb[i]=fullLen[i]/sr[i]*c/2
    R_max[i]=(Nzeros[i]+1)/sr[i]*c/2 #=c*Nzeros*T0/2
    r_res[i]=c/sr[i]/2
    # blindSpeed[i]=PRF[i]*c/cFrq/2/dDec[i]#=lmbda/(2*T)/dDec
    blindSpeed[i]=c/(2*cFrq*fullLen[i]/sr[i])
    print(c)
    print(cFrq)
    print(fullLen[i])
    print(sr[i])
    vmax[i]=blindSpeed[i]/2
    vres[i]=blindSpeed[i]/dSamp[i]
    T_c[i]=dDec[i]*dSamp[i]*fullLen[i]/sr[i]
    P_avg[i]=Pow*fillFactor[i]/100
    Bdop[i]=PRF[i]/dDec[i]/dSamp[i]
    Pnoise[i]=k*Bdop[i]*Temp
    Pmax=(P_avg[i]*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*R_max[i]**4)
    SNRmax[i]=10*math.log10(Pmax/Pnoise[i]/L)
    Pmin=(P_avg[i]*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*R_min[i]**4)
    SNRmin[i]=10*math.log10(Pmin/Pnoise[i]/L)
    # vc[i]=c/2/dSamp[i]
    v_c[i]=r_res[i]/T_B[i]



for i in range(len(sr)-1):
    Ptest=(P_avg[i+1]*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*RZmin**4)
    SNR_T1[i+1]=10*math.log10(Ptest/Pnoise[i+1]/L)
    Ptest=(P_avg[i+1]*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*RZmax**4)
    SNR_T2[i+1]=10*math.log10(Ptest/Pnoise[i+1]/L)
    # print(f'SNR({RT/1000:.0f}km,ped) [dB]\t\033[1m{10*math.log10(Ptest/Pnoise/L):.1f}\033[0m')


print(f'\n')
with open("params.txt", "w") as file:
    rowPrint(sr,0,file)
    rowPrint(fc,0,file)
    rowPrint(Ncode,0,file)
    rowPrint(Nzeros,0,file)
    rowPrint(dSamp,0,file)
    rowPrint(dDec,0,file)
    rowPrint(fullLen,0,file)
    # rowPrint(PRF,1,file)
    # rowPrint(fillFactor,1,file)
    rowPrint(r_res,3,file)
    rowPrint(R_min,3,file)
    rowPrint(R_max,3,file)
    rowPrint(R_unamb,3,file)
    rowPrint(vres,3,file)
    rowPrint(v_c,3,file)
    rowPrint(blindSpeed,3,file)
    rowPrint(vmax,3,file)
    rowPrint(T_c,4,file)
    rowPrint(T0,4,file)
    rowPrint(T_B,4,file)
    # rowPrint(SNRmin,2,file)
    # rowPrint(SNRmax,2,file)
    # rowPrint(SNR_T1,2,file)
    # rowPrint(SNR_T2,2,file)

subprocess.run(['mkdir', f'{fldrN}'])
subprocess.run(['mv', 'params.txt', f'{fldrN}/params.txt'], check=True)


# print(f'lenSR={len(sr)}')
for srA in np.arange(1,len(sr)):
    R=np.arange(r_res[srA],2*R_unamb[srA],r_res[srA])
    Pnoise_dB=10*np.log10(Pnoise[srA])
    PnoiseLoss_dB=10*np.log10(Pnoise[srA]*L)
    PnoiseTrsh_dB=10*np.log10(Pnoise[srA]*L*TH)

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
    # subprocess.run(['mkdir', f'{R_min}', f"{Fa}", f"{Fl}", f"{FAlt}", f"{FDir}"], check=True)
    plt.savefig(f'./{fldrN}/plot_{Ncode[srA]:.0f}_{Nzeros[srA]:.0f}_{sr[srA]/1e6:.0f}.png')
    # plt.show()


    plt.figure(figsize=(8, 5))
    V=np.arange(vres[srA]/100,10*vres[srA],10*vres[srA]/100)

    Vbeag=c/cFrq/2/TburstB
    Tcoh=lmbd/2/V
    # plt.axvline(x=R_min, color='g', linestyle='--')
    # plt.text(R_min, 1, f'R_min', rotation=90, fontsize = 10, color='g', va='baseline', ha='right')
    plt.axhline(y=vres[srA]*3.6, color='k', linestyle='--')
    plt.axvline(x=T_c[srA], color='k', linestyle='--')
    # plt.axhline(y=3.6/10, color='g', linestyle='--')
    # plt.axhline(y=Vbeag*3.6, color='r', linestyle='--')
    plt.plot([0, 2*TburstB], [Vbeag*3.6, Vbeag*3.6], color='r', linestyle='--', label='Beagle')
    plt.plot([TburstB, TburstB], [0, 2*Vbeag*3.6], color='r', linestyle='--')
    plt.plot([0, 2*TburstB], [vres[srA]*3.6, vres[srA]*3.6,], color='k', linestyle='--', label='Kuvik')
    plt.plot([T_c[srA], T_c[srA]], [0, 2*Vbeag*3.6], color='k', linestyle='--')
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
    plt.plot(T_c[srA],vres[srA]*3.6, 'ko',)
    plt.grid(True)
    plt.xlabel("koherenciaidő [sec]")
    plt.ylabel("sebességfelbontás [km/h]")
    plt.title("Koherenciaidő és sebességfelbontás kapcsolata", fontsize = 20)
    plt.text(0.001, 2*Vbeag*3.6*0.99, f'sr= {sr[srA]/1e6:.1f} MHz\nNc= {Ncode[srA]}\nNz= {Nzeros[srA]}\ndS= {dSamp[srA]}\ndD= {dDec[srA]}', fontsize = 10, va='top', ha='left', bbox=bbox_props)
    # plt.savefig('plot.png')
    # plt.show()



for i in np.arange(1,len(sr)):
    with open("./KML/coordRing.txt", "w") as file:
        file.write(f"{Centre}, {RZmin:.0f}, {RZmax:.0f}, 40ff0000, Relevancia Zóna\n")
        file.write(f"{Centre}, {R_min[i]:.0f}, {R_max[i]:.0f}, 4000ff00, Detekciós Zóna\n")
        file.write(f"{Centre}, {R_max[i]:.0f}, {R_min[i]+R_max[i]:.0f}, 400000ff, Áthallási Zóna\n")

    # echo -e "$CENTRE, $Rmin, 400000ff, ff000000, 3, Áthallási zóna 0" > coordCirc.txt

    with open("./KML/coordCirc.txt", "w") as file:
        file.write(f"{Centre}, {R_min[i]:.0f}, 400000ff, ff000000, 3, Áthallási zóna 0")

    # echo -e "$CENTRE, $Rmin, $Rusd, $DIR, $BW, 4000ff00, Detektálási nyaláb" > coordRingSlice.txt

    with open("./KML/coordRingSlice.txt", "w") as file:
        file.write(f"{Centre}, {R_min[i]:.0f}, {R_max[i]:.0f}, {DIR}, {BW}, 4000ff00, Detektálási nyaláb\n")
        file.write(f"{Centre}, {R_max[i]:.0f},  {R_min[i]+R_max[i]:.0f}, {DIR}, {BW}, 400000ff, Áthallási nyaláb\n")

    # echo -e "$CENTRE, $Rmin, $DIR, $BW, 400000ff, ff000000, 3, Áthallási nyaláb 0" > coordSlice.txt
    with open("./KML/coordSlice.txt", "w") as file:
        file.write(f"{Centre}, {R_min[i]:.0f}, {DIR}, {BW}, 400000ff, ff000000, 3, Áthallási nyaláb 0\n")

    with open("./KML/docName.txt", "w") as file:
        file.write(f"{Ncode[i]}_{Nzeros[i]}")


    #  echo -e "$CENTRE, 6649, 9369, 80ffffff, dS=512 lehetséges DZK" > coordRing.txt
    # bash generate.sh $Fa $Fl $FAlt $Fdir

    result = subprocess.run(['bash', './KML/generate.sh', f"{Fa}", f"{Fl}", f"{FAlt}", f"{FDir}", f"{fldrN}"], check=True)
    # print(result.stdout)
import numpy as np
import argparse
import math

def loadbar(a,f):
    o="|"
    for i in range(int(f)):
        if i <= a:
            o=o+"#"
        else:
            o=o+"_"
    o=o+"|"
    print(o)


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
loadbar(fillFactor/2,100/2)
print(f'doppler Samples= \t\033[1m{dSamp} \033[0m')
print(f'doppler Decimation= \t\033[1m{dDec} \033[0m')

print("\n-------------OPERATION-------------")
print(f'Min Range= \t\033[1m{Ncode/sr*c/2:,} m \033[0m'.replace(',', ' '))
R_max=fullLen/sr*c/2
print(f'Max Range= \t\033[1m{R_max:,} m \033[0m'.replace(',', ' '))
rangeRes=fullLen/sr*c/2/fullLen
print(f'Range Res= \t\033[1m{rangeRes:.2f} m\033[0m')
blindSpeed=PRF*c/cFrq/2
print(f'Blind speed= \t\033[1m{blindSpeed/dDec:.2f} m/sec = {blindSpeed/dDec*3.6:.2f} km/h\033[0m')
vmax=blindSpeed/2/dDec
print(f'Max velocity= \t\033[1m+-{vmax:.2f} m/sec = {vmax*3.6:.2f} km/h\033[0m')
print(f'velocity res= \t\033[1m{blindSpeed/dSamp:.2f} m/sec = {blindSpeed/dSamp*3.6:.2f} km/h\033[0m\n')
print(f'minimal time in one range cell= \t\033[1m{rangeRes/vmax:.2f} sec\033[0m')
print(f'max possible doppler samples= \t\033[1m{rangeRes/vmax*sr/fullLen:.2f}\033[0m\n')    #so the target doesnt get out of the range resolution
print(f'max possible velocity without spreading = \t\033[1m{rangeRes/(dDec*dSamp*(fullLen/sr)):.2f} m/sec \t= {rangeRes/(dDec*dSamp*(fullLen/sr))*3.6:.2f} km/h\033[0m')    #so the target doesnt get out of the range resolution

print("\n-------------Power factors-------------")
print(f'Peak power= \t\033[1m{Pow:.2f} Watt\033[0m')
P_avg=Pow*fillFactor/100
print(f'Average power= \t\033[1m{P_avg:.2f} Watt\033[0m')
Bdop=PRF/dDec/dSamp
print(f'Noise power= \t\033[1m{k*sr*Temp*1e12:.2f} fW\033[0m')
Pnoise=k*Bdop*Temp
# print(f'Noise power for one cell= \t\033[1m{Pnoise:.2f} Watt\033[0m')
print(f'Target RCS= \t\033[1m{rcs:.2f} m^2\033[0m')
print(f'Ant gain= \t\033[1m{G_dB:.2f} \033[0m')
Gain=10**(G_dB/10.0)
Pref=(P_avg*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*R_max**4)
# print(f'Reflected Power from the end of range= \t\033[1m{Pref*1e12:.2f} fW\033[0m')
print(f'SNR= \t\t\033[1m{10*math.log10(Pref/Pnoise):.2f} dB\033[0m')
print(f'Theorical maximum Range= \t\033[1m{math.pow((P_avg*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*k*Temp*Bdop),1/4):.2f} m\033[0m')
L=125.9
TH=20.9
print(f'Maximum Range with losses= \t\033[1m{math.pow((P_avg*Gain**2*rcs*lmbd**2)/((4*math.pi)**3*k*Temp*Bdop*L*TH),1/4):.2f} m\033[0m')
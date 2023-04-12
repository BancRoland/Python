import numpy as np
import argparse

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


# parser.add_argument("-r","--radius", help="radius of the circle", nargs='?', type=float, const=1, default=7, required=True)

# parser.add_argument("-pi","--pi", help="the ratio called pi", nargs='?', type=float, const=1, default=3.14159)

args=parser.parse_args()
# answer=args.radius**2*args.pi

c=args.c

cFrq=args.cFrq # centerFrequency[Hz]
sr=args.samprate     #sample rate [samp/sec]
Ncode=args.Ncode   #correlation code samples []
Nzeros=args.Nzeros #zeros for range []
dSamp=args.dSamp    #dopplerSamples
dDec=args.dDec      #doppler decimation value


print("\n-------------Wave-------------")
print(f'c= \t\t\033[1m{c:,} m/s\033[0m'.replace(',', ' '))
print(f'cFrq= \t\t\033[1m{cFrq/1e9} GHz\033[0m')
print(f'lambda= \t\033[1m{c/cFrq} m\033[0m')
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
print(f'Max Range= \t\033[1m{fullLen/sr*c/2:,} m \033[0m'.replace(',', ' '))
print(f'Range Res= \t\033[1m{fullLen/sr*c/2/fullLen:.2f} m\033[0m')
blindSpeed=PRF*c/cFrq/2
print(f'Blind speed= \t\033[1m{blindSpeed/dDec:.2f} m/sec = {blindSpeed/dDec*3.6:.2f} km/h\033[0m')
print(f'Max velocity= \t\033[1m+-{blindSpeed/2/dDec:.2f} m/sec = {blindSpeed/2/dDec*3.6:.2f} km/h\033[0m')
print(f'velocity res= \t\033[1m{blindSpeed/dSamp:.2f} m/sec = {blindSpeed/dSamp*3.6:.2f} km/h\033[0m\n')
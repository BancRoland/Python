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


parser = argparse.ArgumentParser(description="calculate the area of circle with radius r")

parser.add_argument("-cFrq","--cFrq", help="Frequency of the carrier wave [Hz] ", nargs='?', type=float, default=10e9)

# parser.add_argument("-r","--radius", help="radius of the circle", nargs='?', type=float, const=1, default=7, required=True)

# parser.add_argument("-pi","--pi", help="the ratio called pi", nargs='?', type=float, const=1, default=3.14159)

args=parser.parse_args()
# answer=args.radius**2*args.pi

cFrq=args.cFrq # centerFrequency[Hz]
sr=100e6     #sample rate [samp/sec]
Ncode=1024   #correlation code samples []
Nzeros=6144 #zeros for range []
dSamp=512   #dopplerSamples

c=3e8

print("\n-------------EM Wave-------------")
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
print("\n-------------OPERATION-------------")
print(f'Min Range= \t\033[1m{Ncode/sr*c/2/1000:.2f} km \033[0m')
print(f'Max Range= \t\033[1m{fullLen/sr*c/2/1000:.2f} km\033[0m')
print(f'Range Res= \t\033[1m{fullLen/sr*c/2/fullLen:.2f} m\033[0m')
blindSpeed=PRF*c/cFrq
print(f'Max velocity= \t\033[1m+-{blindSpeed/4:.2f} m/sec = {blindSpeed/4*3.6:.2f} km/h\033[0m')
print(f'velocity res= \t\033[1m{blindSpeed/2/dSamp:.2f} m/sec = {blindSpeed/2/dSamp*3.6:.2f} km/h\033[0m\n')
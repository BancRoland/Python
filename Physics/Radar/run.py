import numpy as np
import argparse

parser = argparse.ArgumentParser(description="calculate the area of circle with radius r")

parser.add_argument("-cFrq","--cFrq", help="Frequency of the carrier wave [Hz] ", nargs='?', type=float, default=10e9)

# parser.add_argument("-r","--radius", help="radius of the circle", nargs='?', type=float, const=1, default=7, required=True)

# parser.add_argument("-pi","--pi", help="the ratio called pi", nargs='?', type=float, const=1, default=3.14159)

args=parser.parse_args()
# answer=args.radius**2*args.pi

cFrq=args.cFrq # centerFrequency[Hz]
sr=100e6     #sample rate [samp/sec]
Ncode=16   #correlation code samples []
Nzeros=128 #zeros for range []
dSamp=1024   #dopplerSamples

c=3e8

print(f'cFrq={cFrq/1e9} GHz')
print(f'lambda={c/cFrq} m')
print(f'samprate={sr/1e6} MHz')

print(f'Codes= {Ncode}')
print(f'Zeros= {Nzeros}')
fullLen=Ncode+Nzeros
print(f'Full length= {fullLen}')
PRF=sr/fullLen
print(f'PRF= {PRF:.2f} Hz')
print(f'Max Range= {fullLen/sr*c/2:.2f} m')
print(f'Range Res= {fullLen/sr*c/2/fullLen:.2f} m')
blindSpeed=PRF*c/cFrq
print(f'Max velocity= +-{blindSpeed/4:.2f} m/sec = {blindSpeed/4*3.6:.2f} km/h')
print(f'velocity res= {blindSpeed/2/dSamp:.2f} m/sec = {blindSpeed/2/dSamp*3.6:.2f} km/h')
#!/bin/python3
# import uhd
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
from datetime import datetime
import argparse


parser = argparse.ArgumentParser()
# parser.add_argument("file", help="file to read")
parser.add_argument("-f","--file", help="file to read from", nargs='?', type=str, required=True)
parser.add_argument("-d","--decimation", help="decimation value", nargs='?', type=int, default=2)
parser.add_argument("-m","--multip", help="filesize multiplicator", nargs='?', type=int, default=100)    # ennyiszeresét olvassa be együttesen a decimációs értéknek
args = parser.parse_args()
# print(args.file)

# DEC=10_000
DEC=args.decimation


now = datetime.now()
dstr = now.strftime("%Y-%m-%d_%H-%M-%S")

filesize=DEC*2*args.multip  #Együttesen beolvasott fileméret

if filesize<=DEC:
    print("DECIMATION CANNOT BE BIGGER THAN THE FILESIZE!")
else:

    i=0 #inkrementéációs szám, a beolvasási állapot számontartásához

    diff=np.zeros(0)
    decOut=np.zeros(0)+1j*np.zeros(0)

    while(True):

        sampRX0=np.fromfile(args.file, count=filesize, offset=i*filesize*2, dtype=np.int16)

        size=np.size(sampRX0)
        if not size:
            break

        sampRX=sampRX0[0:size:DEC]+sampRX0[1:size:DEC]*1j
        decOut=np.concatenate([np.array(decOut),np.array(sampRX)])
        n=np.arange(0,size,DEC)

        i=i+1

        
    fullSize=np.size(decOut)
    nF=DEC/2*np.arange(0,fullSize)

    plt.figure()
    plt.plot(nF,np.real(decOut),'.-')
    plt.plot(nF,np.imag(decOut),'.-')
    plt.xlabel("decimálatlan mintaszám")
    plt.xlim([0, DEC/2*fullSize])
    plt.show()

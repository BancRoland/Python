#!/bin/python3
# import uhd
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
from datetime import datetime

DEC=100     #Megjelenítés, és tárolás érdekében alkalmazott decimálás

now = datetime.now()
dstr = now.strftime("%Y-%m-%d_%H-%M-%S")

filesize=1_000_000  #Együttesen beolvasott fileméret

i=0 #inkrementéációs szám, a beolvasási állapot számontartásához

sampRX0=np.fromfile('outRX.dat', count=filesize, offset=i*filesize*8, dtype=np.complex64)

size=np.size(sampRX0)
diff=np.zeros(0)
decOut=np.zeros(0)

while(size):

    i=i+1

    sampRX=sampRX0[0:size:DEC]
    n=np.arange(0,size,DEC)

    decOut=np.concatenate([np.array(decOut),np.array(sampRX)])

    sampRX0=np.fromfile('outRX.dat', count=filesize, offset=i*filesize*8, dtype=np.complex64)

    size=np.size(sampRX0)


plt.figure()
plt.plot(np.real(decOut),'.-')
plt.plot(np.imag(decOut),'.-')
plt.show()

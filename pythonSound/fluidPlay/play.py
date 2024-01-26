#!/bin/python3
# sudo apt-get install libportaudio2
# pip install sounddevice

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import time

m=0.5        #modulációs mélység
fc=1_000    #vivő
fm=100      #moduláló
fs=44100
T=1
t = np.arange(0,T,1/fs)
C = np.sin(2*np.pi*fc*t)
M = np.sin(2*np.pi*fm*t)

Y = C * (1+m*M)

sd.play(0.01* Y, fs)
time.sleep(T)	#enélkül nem működik


plt.plot(t[:int(0.1*fs)],Y[:int(0.1*fs)],label='sin(x)')
plt.xlabel('xcím')
plt.ylabel('ycím')
plt.title('Ez egy címsor')
plt.legend()
plt.grid()
plt.show()

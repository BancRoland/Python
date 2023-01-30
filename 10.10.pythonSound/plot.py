#!/bin/python3
# sudo apt-get install libportaudio2
# pip install sounddevice

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import time

f=1000;
fs=44100
T=1
t=np.arange(0,T,1/fs);
y = t/T*np.sin(2*np.pi*f*t)


sd.play(0.1* y, fs)
time.sleep(1)	#enélkül nem működik


plt.plot(t,y,label='sin(x)')
plt.xlabel('xcím')
plt.ylabel('ycím')
plt.title('Ez egy címsor')
plt.legend()
plt.grid()
plt.show()

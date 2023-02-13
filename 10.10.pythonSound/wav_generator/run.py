import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import write


Nz=0       #kitöltőnullák
sr=130      #samprate
fs=44100    
f=1000      #modFrq
rep=10      #repeat


def inc(v, R):
    w=np.zeros(len(v)*R)
    print(len(v)*R)
    for i in range(len(v)):
        for j in range(R):
            #print(i*R+j)
            #w[i*R+j]=v[i]
            w[i*R+j]=v[i]
    return(w)

def repeat(v,a):
    w=np.zeros(len(v)*a)
    for i in range(a):
        w[(i*len(v)):((i+1)*len(v))]=np.array(v)
    return(w)

def upmix(v,f,fs):
    P=np.arange(len(v))*f/fs*2*np.pi
    mix=np.exp(1j*P)
    w=v*mix
    return(w)

def dec(v,a):
    w=v[::a]
    return(w)

def resa(v,fs,b):
    w=dec(inc(v,fs),b)
    return(w)




code=[1,1,1,1,1,0,0,1,1,0,1,0,1]
code1=np.array(code)*2-1
code11=np.concatenate([code1,np.zeros(Nz)])
code2=repeat(code11,rep)
code21=np.concatenate([np.zeros(Nz),code2])
code3=resa(code21,fs,sr)
code4=upmix(code3,f,fs)
plt.plot(code4,'.-')
plt.show()

scaled = np.int16(code4 * 32767)
write('out.wav', fs, scaled)
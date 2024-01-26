import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import write


Nz=13      #kitöltőnullák
sr=100      #samprate
fs=44100    
f=1000      #modFrq
rep=10      #repeat


def inc(v, R):
    w=np.zeros(len(v)*R)+1j*np.zeros(len(v)*R)
    print(len(v)*R)
    for i in range(len(v)):
        for j in range(R):
            #print(i*R+j)
            #w[i*R+j]=v[i]
            w[i*R+j]=v[i]
    return(w)

def repeat(v,a):
    w=np.zeros(len(v)*a)+1j*np.zeros(len(v)*a)
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

def encode(m,c):
    w=np.zeros(len(m)*len(c))+1j*np.zeros(len(m)*len(c))
    for i in range(len(m)):
        w[(i*len(c)):((i+1)*len(c))]=m[i]*c
    return(w)


codeM0=[0,1,2,3]

codeC=[1,1,1,1,1,0,0,1,1,0,1,0,1]   #ez a alap kód, ezt ne buzeráld

codeM=np.exp(1j*np.array(codeM0)/4*2*np.pi)
code1=(np.array(codeC)+1j*np.zeros(len(codeC)))*2-1
code10=encode(codeM,code1)
plt.plot(np.real(code10),'.-')
plt.plot(np.imag(code10),'.-')
plt.show()
# code11=np.concatenate([code10,np.zeros(Nz)])
code2=repeat(code10,rep)
code21=np.concatenate([np.zeros(Nz),code2])
#code3=resa(code21,fs,sr)
code3=inc(code21,int(fs/sr))
code4=upmix(code3,f,fs)


plt.plot(np.real(code21),'.-')
plt.plot(np.imag(code21),'.-')
plt.title(f'bitrate: {sr} simbol/sec, sampFrq: {fs} Hz,\n codeLen: {len(codeC)}, zeros: {Nz}')
plt.grid()
plt.savefig('code.png')
plt.show()


scaled = np.int16(code4 * 32767)
write('out.wav', fs, scaled)
import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import write


Nz=13      #kitöltőnullák
sr=100      #samprate
fs=44100    
f=1000      #modFrq
rep=10   #repeat
QPSK_N=16  # 4*4 es QAM


# beadott v vektort R szeresére incrementálja
def inc(v, R):
    w=np.zeros(len(v)*R)+1j*np.zeros(len(v)*R)
    print(len(v)*R)
    for i in range(len(v)):
        for j in range(R):
            #print(i*R+j)
            #w[i*R+j]=v[i]
            w[i*R+j]=v[i]
    return(w)

#beadott v vektort a szor ismétli
def repeat(v,a):
    w=np.zeros(len(v)*a)+1j*np.zeros(len(v)*a)
    for i in range(a):
        w[(i*len(v)):((i+1)*len(v))]=np.array(v)
    return(w)

#beadott v vektort felkeveri f frekvncijú harmónikussal fs mintavétel mellett
def upmix(v,f,fs):
    P=np.arange(len(v))*f/fs*2*np.pi
    mix=np.exp(1j*P)
    w=v*mix
    return(w)

#beadott v vektor w decimálja
def dec(v,a):
    w=v[::a]
    return(w)

#beadott v vektort b/fs ujraminteveszi
def resa(v,fs,b):
    w=dec(inc(v,fs),b)
    return(w)

#beadott m vektort c kóddal moduálja
def encode(m,c):
    wlen=len(m)*len(c)
    w=np.zeros(wlen)+1j*np.zeros(wlen)
    for i in range(len(m)):
        w[(i*len(c)):((i+1)*len(c))]=m[i]*c
    return(w)




# codeM0=np.array([-3-3j, -1-3j, 1-3j, 3-3j,  -3-1j, -1-1j, 1-1j, 3-1j,  -3+1j, -1+1j, 1+1j, 3+1j,  -3+3j, -1+3j, 1+3j, 3+3j])
codeM0=np.zeros(QPSK_N)+1j*np.zeros(QPSK_N)
for i in range(QPSK_N):
    codeM0[i]=np.exp(i*1j*2*np.pi/QPSK_N)

codeM=codeM0/np.max(np.abs(codeM0))     #Normált konstelláiós sorozat

codeC=[1,1,1,1,1,0,0,1,1,0,1,0,1]   #ez a alap kód, ezt ne buzeráld
codeB13=(np.array(codeC)+1j*np.zeros(len(codeC)))*2-1

header=np.array([0,0,0,0,0,0,0,0])

codeR=np.random.randint(QPSK_N, size=20)
codeR=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])

codeR=np.concatenate([header,codeR])

code10=encode(codeM[codeR%QPSK_N],codeB13)


plt.plot(np.real(codeM),np.imag(codeM),'o:')
plt.title(f'bitrate: {sr} simbol/sec, sampFrq: {fs} Hz,\n codeLen: {len(codeC)}, zeros: {Nz}')
plt.grid()
plt.axis('square')
plt.xlim(-1,1)
plt.ylim(-1,1)
plt.savefig('codeCONST.png')
plt.show()

# code11=np.concatenate([code10,np.zeros(Nz)])
code2=repeat(code10,rep)
code21=np.concatenate([np.zeros(Nz),code2])
#code3=resa(code21,fs,sr)
code3=inc(code21,int(fs/sr))
code4=upmix(code3,f,fs)

plt.plot(np.real(code10),'.-')
plt.plot(np.imag(code10),'.-')
plt.title(f'bitrate: {sr} simbol/sec, sampFrq: {fs} Hz,\n codeLen: {len(codeC)}, zeros: {Nz}')
plt.grid()
plt.savefig('codeTIME0.png')
plt.show()

plt.plot(np.real(code21),'.-')
plt.plot(np.imag(code21),'.-')
plt.title(f'bitrate: {sr} simbol/sec, sampFrq: {fs} Hz,\n codeLen: {len(codeC)}, zeros: {Nz}')
plt.grid()
plt.savefig('codeTIME.png')
plt.show()


scaled = np.int16(np.real(code4) * 32767)
write('out.wav', fs, scaled)

import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import write


Nz=20      #kitöltőnullák
sr=100      #samprate
fs=44100    
f=1000      #modFrq
rep=2      #repeat

DEBUG=0 #debug mód

def comp2cf32(v):
    code=np.zeros(len(v)*2)
    code[::2]=np.real(v)
    code[1::2]=np.imag(v)
    out=code.astype('float32')
    return out

def compPlot(v,title,filename):
    plt.figure()
    plt.plot(np.real(v),'.-')
    plt.plot(np.imag(v),'.-')
    plt.plot(np.abs(v),'--', color='grey', alpha=0.5)
    plt.plot(-np.abs(v),'--', color='grey', alpha=0.5)
    plt.legend(["Real","Imag","Abs"])
    plt.title(title)
    plt.grid()
    plt.savefig(filename)
    plt.show()
    

def hex2bin(HEXcode):                                                   #"0x64C4646E"
    bincode=bin(int(HEXcode[2:], 16))[2:].zfill((len(HEXcode)-2)*4)     #"01100100110001000110010001101110"
    BINcode=np.array(list(map(int, bincode)))                           #[0 1 1 0 0 1 0 0 1 1 0 0 0 1 0 0 0 1 1 0 0 1 0 0 0 1 1 0 1 1 1 0]
    if DEBUG:
        print(HEXcode)
        print(bincode)
        print(BINcode)
    return BINcode

def bin2comp(codeRAW):                                          #np.array([0 1 1 0 0 1 0 0 1 1 0 0...
    code2digits=np.reshape(codeRAW, (int(len(codeRAW)/2), 2))   #[[0 1], [1 0], [0 1]...
    codedAng=code2digits[:,0]*2+code2digits[:,1]                #[1 2 1 0 3 0 1 0 1 2 1 0 1 2 3 2]
    cplxCode=np.exp(1j*2*np.pi*(codedAng/4+1/8))*np.sqrt(2)     #[-1.+1.j -1.-1.j -1.+1.j  1.+1.j  1.-1.j ...
    if DEBUG:
        print(codeRAW)
        print(code2digits)
        print(cplxCode)
    return cplxCode

def hex2comp(HEXcode):
    if DEBUG:
        print(HEXcode)
        print(bin2comp(hex2bin(HEXcode)))
    return bin2comp(hex2bin(HEXcode))

def inc(v, R):
    w=np.zeros(len(v)*R)*1j
    print(len(v)*R)
    for i in range(len(v)):
        for j in range(R):
            #print(i*R+j)
            #w[i*R+j]=v[i]
            w[i*R+j]=v[i]
    return(w)

def repeat(v,a):
    w=np.zeros(len(v)*a)*1j
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



HEXcodePair=["0x64C4646E", "0x13B3B9B3"]
cplxCode1=np.round(hex2comp(HEXcodePair[0]))/(1+1j)
cplxCode2=np.round(hex2comp(HEXcodePair[1]))/(1+1j)

print(cplxCode1)


# code=[1,1,1,1,1,0,0,1,1,0,1,0,1]
# code1=np.array(code)*2-1
code110=np.concatenate([cplxCode1,np.zeros(Nz),cplxCode2])
out=comp2cf32(code110)
out.tofile("compCode.cf32")

code11=np.concatenate([code110,np.zeros(Nz)])
# code11=np.concatenate([cplxCode1,np.zeros(Nz),cplxCode2,np.zeros(Nz)])
print(code11)
code2=repeat(code11,rep)
code21=np.concatenate([np.zeros(Nz),code2])
#code3=resa(code21,fs,sr)
code3=inc(code21,int(fs/sr))
code4=upmix(code3,f,fs)


title=f'bitrate: {sr} simbol/sec, sampFrq: {fs} Hz,\n codeLen: {len(cplxCode2)}, zeros: {Nz}'
compPlot(code21,title,'code.png')
# plt.plot(code21,'.-')
# plt.plot(code21,'.-')
# plt.title(f'bitrate: {sr} simbol/sec, sampFrq: {fs} Hz,\n codeLen: {len(cplxCode2)}, zeros: {Nz}')
# plt.grid()
# plt.savefig('code.png')
# plt.show()


scaled = np.int16(code4 * 32767)
write('out.wav', fs, scaled)

import numpy as np
import uhd
import matplotlib.pyplot as plt
import math
import cmath

#input_file="togrc.bin"

#count=2**21
#offset=0

def INC(v,a):
    w=np.array([])
    for i in v:
        w=np.append(w,np.ones(a)*i)
    return w

def DEC(v,a):
    w=np.zeros(int(len(v)/a), dtype='complex')
    for i in range(int(len(v)/a)):
        w[i]=np.sum(v[i*a:(i+1)*a])
        #w=np.append(w,np.sum(v[i*a:(i+1)*a]))
        #print(i)
    return w

DECVAL=2
fs0=2500000
fs=fs0/DECVAL


input= np.fromfile("out.dat", dtype=np.complex64)[0:1000000]
code=np.fromfile("togrc.dat", dtype=np.complex64)

t=np.arange(len(input)/DECVAL)/fs

# plt.plot(np.real(input),'.-')
# plt.plot(np.imag(input),'.-')
# plt.show()

plt.figure(figsize=(12, 8))
plt.plot(np.real(code),'.-')
plt.plot(np.imag(code),'.-')
plt.title("Alkalmazott kód")
plt.grid()
plt.legend(['Real','Imag'])
plt.savefig("fig1.png")
plt.show()

codeD=DEC(code,DECVAL)
plt.figure(figsize=(12, 8))
plt.plot(t[0:len(codeD)],np.real(codeD),'.-')
plt.plot(t[0:len(codeD)],np.imag(codeD),'.-')
plt.title('Decimált kód')
plt.xlabel("time [sec]")
plt.ylabel("jelérték []")
plt.grid()
plt.legend(['Real','Imag'])
plt.savefig("fig2.png")
plt.xlim(0,0.001)
plt.savefig("fig2.0.png")
plt.show()

autoCorr=np.correlate(codeD,codeD, 'full')+1e-5
plt.figure(figsize=(12, 8))
plt.plot(t[0:len(autoCorr)],np.abs(autoCorr),'.-')
plt.title('Decimált kód autokorrelációja')
plt.xlabel("time [sec]")
plt.ylabel("jelérték []")
plt.grid()
plt.savefig("fig2.1.png")
plt.xlim(0.003,0.003+0.001)
plt.savefig("fig2.2.png")
plt.show()

plt.figure(figsize=(12, 8))
plt.plot(t[0:len(autoCorr)],20*np.log10(np.abs(autoCorr)),'.-')
plt.title('Decimált kód autokorrelációja logaritmikus skálán')
plt.xlabel("time [sec]")
plt.ylabel("jelérték [dBp]")
plt.grid()
plt.ylim(50,100)
plt.savefig("fig2.3.png")
plt.xlim(0.003,0.003+0.001)
plt.savefig("fig2.4.png")
plt.show()


inputD=DEC(input,DECVAL)
plt.figure(figsize=(12, 8))
plt.plot(t,np.real(inputD),'.-')
plt.plot(t,np.imag(inputD),'.-')
plt.legend(['Real','Imag'])
plt.title('decimated input')
plt.xlabel("time [sec]")
plt.ylabel("jelérték []")
plt.grid()
plt.savefig("fig3.png")
plt.xlim(0.1003+0,0.1003+0.001)
plt.savefig("fig3.1.png")
plt.show()


correlated=np.correlate(inputD,codeD,"full")
plt.figure(figsize=(12, 8))
#plt.plot(t,np.real(correlated),'.-')
#plt.plot(t,np.imag(correlated),'.-')
plt.plot(t,np.abs(correlated)[0:len(t)],'.-')
print(len(code))
print(len(code)/DECVAL)
plt.title('korreláltatott jelek')
plt.xlabel("time [sec]")
plt.ylabel("jelérték []")
plt.grid()
plt.savefig("fig4.png")
plt.xlim(0.1003+0,0.1003+0.001)
plt.savefig("fig4.1.png")
plt.show()


SegLen=int(len(code)/DECVAL)
correlated=np.correlate(inputD,codeD,"full")
plt.figure(figsize=(12, 8))
#plt.plot(t,np.real(correlated),'.-')
#plt.plot(t,np.imag(correlated),'.-')
for i in range(1):
    plt.plot(t[0:SegLen],20*np.log10(np.abs(correlated)[(i+2)*SegLen:(i+3)*SegLen]),'.-')
plt.title('korreláltatott jelek egyetlen szakasza')
plt.xlabel("time [sec]")
plt.ylabel("jelérték [dBp]")
plt.grid()
plt.savefig("fig5.png")
plt.show()


SegLen=int(len(code)/DECVAL)
correlated=np.correlate(inputD,codeD,"full")
plt.figure(figsize=(12, 8))
#plt.plot(t,np.real(correlated),'.-')
#plt.plot(t,np.imag(correlated),'.-')
for i in range(10):
    plt.plot(t[0:SegLen],20*np.log10(np.abs(correlated)[(i+2)*SegLen:(i+3)*SegLen]),'.-')
plt.title('korreláltatott jelek egyetlen szakasza önmagára lapolva')
plt.xlabel("time [sec]")
plt.ylabel("jelérték [dBp]")
plt.grid()
plt.savefig("fig6.png")
plt.show()


# print(len(inputD))
# print('a')
# print(len(inputD) / SegLen)
# print('b')
# print(int(len(inputD)/SegLen))


RNG=int(len(inputD)/SegLen)-1
sumSig=np.zeros(SegLen)
for i in range(RNG):
    sumSig=sumSig+correlated[((i+2)*SegLen):((i+3)*SegLen)]/RNG

plt.figure(figsize=(12, 8))
for i in range(RNG):
    plt.plot(t[0:SegLen],20*np.log10(np.abs(correlated)[(i)*SegLen:(i+1)*SegLen]),'.', alpha=0.1, color='black')
plt.plot(t[0:SegLen],20*np.log10(abs(sumSig)),'.-')
plt.title('STACKELT korreláltatott jelszakaszok')
plt.xlabel("time [sec]")
plt.ylabel("jelérték [dBp]")
plt.legend(['STACKED','single'])
plt.grid()
plt.savefig("fig7.png")
plt.show()
   




# plt.plot(np.fft.fftshift(np.abs(np.fft.fft(input))))
# plt.show()

# plt.plot(np.abs(np.correlate(input,input,"full")))
# plt.show()

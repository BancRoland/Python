import numpy as np
import matplotlib.pyplot as plt

fs=44100
fd=1000

# data=[0,0,1,0,1,0,1,1,1,0,1,1,1,0,0,0]
data=np.round(np.random.random(150))

def FFT_bandbpass(v,f_min,f_max,fs):
    vspec=np.fft.fft(v)
    # vspec[0:int(len(v)*f_min/fs):]=0
    # vspec[-int(len(v)*f_min/fs)+1::]=0
    vspec[int(len(v)*f_max/fs):-int(len(v)*f_max/fs)+1:]=0
    return np.fft.ifft(vspec)

def ManchCorr(v,Mlen):  #v: complex vector with anchester code in it    Mlen: length of one simbol (halfbit) in a manchester code minimum is 1
    mix=np.exp(-1j*np.arange(len(v))/len(v)*2*np.pi*len(v)/Mlen)
    out=np.sum(v**2*mix)/len(v)

    sampDelVal=int(np.round((1-np.angle(out)/2/np.pi)*Mlen))
    # plt.plot(v**2,color="black")
    # plt.plot(np.real(mix),color="C0")
    # plt.plot(np.imag(mix),color="C1")
    # plt.show()

    # plt.plot(np.real(v**2*mix),color="C0")
    # plt.plot(np.imag(v**2*mix),color="C1")
    # plt.title(f"avg = {np.abs(np.sum(v**2*mix)/len(v))}")
    # plt.show()
    return out, sampDelVal
    


LEN=100
bit=np.append(np.ones(LEN),-1*np.ones(LEN))

out00=np.array([])

for i in data:
    out00=np.append(out00,(2*i-1)*bit)

out0=np.concatenate([np.zeros(1000), out00, np.zeros(2000)])

if 0:
    plt.plot(data)
    plt.show()


out=out0+0.5*np.random.randn(len(out0))

if 0:
    plt.plot(out,color="C1")
    plt.plot(out0,color="C0")
    plt.show()

if 0:
    plt.plot(np.log10(np.abs(np.fft.fftshift(np.fft.fft(out)))))
    # plt.plot(np.log10(np.abs(np.fft.fft(out))))
    plt.axvspan(int(len(out)/2-len(out)/100),int(len(out)/2+len(out)/100),color="C1",alpha=0.5)
    plt.title("spectrum")
    plt.show()

outF=FFT_bandbpass(out,0,1/100,1)

if 0:
    plt.plot(outF)
    plt.title("Filtered")
    plt.show()

if 0:
    plt.plot(np.log10(np.abs(np.fft.fftshift(np.fft.fft(outF**2)))))
    # plt.plot(np.log10(np.abs(np.fft.fft(out))))
    plt.title("spectrum")
    plt.show()


if 0:
    plt.plot(outF[0:10000:10]**2,'.-')
    plt.plot(outF[10:10010:10]**2,'.-')
    plt.plot(outF[20:10020:10]**2,'.-')
    plt.plot(outF[50:10050:10]**2,'.-')
    plt.plot(np.cos(np.arange(10e2)/10e2*2*np.pi*100),"--")
    plt.show()

off_list=[0, 10, 20, 50]
for i in range(len(off_list)):

    delayedSignal = outF[off_list[i]:10000+off_list[i]:10]
    plt.subplot(len(off_list),1,i+1)
    plt.plot(np.real((np.fft.fft(delayedSignal**2))),'.-')
    plt.plot(np.imag((np.fft.fft(delayedSignal**2))),'.-')
    val=np.fft.fft(delayedSignal**2)[100]/10000
    val2=(0.5-np.angle(val)/2/np.pi)*100
    print(f"{off_list[i]}:   abs: {np.abs(val):.2f}  phase: {val2:.2f}")
    funResult = ManchCorr(delayedSignal,10)
    print(f"abs: {np.abs(funResult)}  phase: {(0.5-np.angle(funResult)/2/np.pi)*100}")
plt.show()


# for i in [0, 5, 12, 33, 64, 79]:
#     # getting some samples
#     outR=outF[i:10000:]

#     val3, sampDelVal=ManchCorr(outR,100)
#     val4=(0.5-np.angle(val3)/2/np.pi)*100
#     print(f"!!!!!!!!! abs: {np.abs(val3)}  detected shift: {150-sampDelVal} usedDelay: {sampDelVal}")

#     plt.subplot(2,1,1)
#     plt.plot(outR[sampDelVal:10000:100],'.-')
#     plt.subplot(2,1,2)
#     plt.plot(outF[50:10000:100],'.-')
#     plt.show()


#     samps=outR[sampDelVal:10000:100]
#     DATA=np.zeros(len(samps))
#     k=0
#     for i in range(len(samps)):
#         if samps[i] > 0.5:
#             DATA[k]=1
#             k=k+1
#         if samps[i] < -0.5:
#             DATA[k]=-1
#             k=k+1

#     mix=np.cos(np.arange(len(DATA))/len(DATA)*2*np.pi*len(DATA)/2)
#     plt.subplot(2,1,1)
#     plt.plot(DATA,'.-')
#     plt.subplot(2,1,2)
#     plt.plot(out00[50:10000:100],'.-')
#     plt.show()

#     plt.subplot(2,1,1)
#     plt.plot((DATA*mix)[::2],'.-')
#     plt.subplot(2,1,2)
#     plt.plot(data[:len((DATA*mix)[::2]):],'.-')
#     plt.show()

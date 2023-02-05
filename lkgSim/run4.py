import numpy as np
import matplotlib.pyplot as plt


def A2dB(a):
	return 20*np.log10(a)

def dB2A(dB):
	return 10**(dB/20)
	
def Atten(arr,Att):
	return arr/dB2A(Att)
	
def calVal(a,Att):
	b=Atten(1,Att)
	if b == a:
		return "INF"
	else:
		return A2dB(np.abs((a+b)/(b-a)))
		
def calLeak(a):
	b=dB2A(a)
	k=min(b)/max(b)
	f=(1-k)/(k+1)
	return f
	
		
def cosWind(v):
	w=(np.ones(len(v))-np.cos(np.linspace(0,2*np.pi,len(v))))/2
	return w*v*np.sqrt(8/3)

f=np.arange(1500,1600,2)
#print(f)
k=0.01
a=0.9
a2=0.0
Att=0
K=k*np.exp(1j*2*np.pi*f/8)
S=a*k*np.exp(1j*2*np.pi*f/47)
S2=a2*k*np.exp(1j*2*np.pi*f/23)
P=np.abs(Atten(K,Att)+S+S2)
p2=A2dB(P)

plt.figure()
plt.plot(f,p2,'.-')
plt.ylim(-140,0)
plt.title(calLeak(p2))
plt.show()

spec=np.fft.fft(P)/len(P)*2
spec[0]=spec[0]/2
spec2=np.fft.fft(cosWind(P))/len(P)
plt.figure()
plt.plot(A2dB(np.abs(spec)),'.-')
#plt.plot(np.log10(np.abs(spec2)),'.-')
plt.ylim(-140,0)
plt.xlim(-1,int(len(spec)/2))
plt.grid()
plt.show()

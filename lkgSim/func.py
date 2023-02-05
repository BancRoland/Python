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
		
def cosWind(v):
	w=(np.ones(len(v))-np.cos(np.linspace(0,2*np.pi,len(v))))/2
	return w*v*np.sqrt(8/3)


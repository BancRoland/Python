import numpy as np
import matplotlib.pyplot as plt
import math

def pltC(V):
    plt.plot(np.real(V),'.-')
    plt.plot(np.imag(V),'.-')
    plt.plot(np.abs(V), '.-', color="gray", alpha=0.5)
    plt.show()

def proRev(V):
    return np.concatenate([[V[0]],V[:0:-1]])
    

LEN=100
sig=np.random.randn(LEN)+1j*np.random.randn(LEN)
t=np.arange(LEN)
# sig=np.sin(t/LEN*2*math.pi)
sig=np.concatenate([np.zeros(LEN),[-10-1j*10,20+1j*10,-10-1j*10,10+1j*10,-10-1j*10,10+1j*10],sig,np.zeros(LEN)])
sig_fft=np.fft.fft(sig)

# pltC(sig_fft)
# pltC(sig)
# pltC(np.fft.ifft(np.conj(sig_fft)))


# pltC(sig_fft)
# pltC(np.fft.fft(sig[::-1]))

pltC(proRev(sig))

plt.plot(np.real(sig_fft),'.-', color="C0")
plt.plot(np.imag(sig_fft),'.-', color="C1")
plt.plot(np.abs(sig_fft), '.-', color="gray", alpha=0.5)

sig_fft_rev=np.fft.fft(proRev(sig))
plt.plot(np.real(sig_fft_rev+150+150j),'.-', color="C0")
plt.plot(np.imag(sig_fft_rev+150+150j),'.-', color="C1")
plt.plot(np.abs(sig_fft_rev)+150, '.-', color="gray", alpha=0.5)
plt.show()




plt.plot(np.real(sig),'.-', color="C0")
plt.plot(np.imag(sig),'.-', color="C1")
plt.plot(np.abs(sig), '.-', color="gray", alpha=0.5)

sig3=np.fft.ifft(proRev(sig_fft))
plt.plot(np.real(sig3+1.5+1.50j),'.-', color="C0")
plt.plot(np.imag(sig3+1.50+1.50j),'.-', color="C1")
plt.plot(np.abs(sig3)+1.50, '.-', color="gray", alpha=0.5)
plt.show()


import matplotlib.pyplot as plt
import numpy as np

def cplot(samples):
    plt.figure()
    plt.plot(np.real(samples),'.-')
    plt.plot(np.imag(samples),'.-')
    plt.plot(np.abs(samples),'--', color='grey', alpha=0.5)
    plt.plot(-np.abs(samples),'--', color='grey', alpha=0.5)
    plt.legend(["Real","Imag","Abs"])
    # plt.title(title)
    plt.grid()
    plt.show()

# a=np.zeros(LEN)+1j*np.zeros(LEN)
# a[0]=1
# cplot(a)
# A=np.fft.fft(a)
# cplot(A)

ONES=12
ZEROS=121

# b=np.concatenate([np.ones(ONES+1),np.zeros(ZEROS),np.ones(ONES)])
# # b=np.array([1,1,1,0,0,0,0,0,0,1,1])
# B=np.fft.ifft(b)
# cplot(np.fft.fftshift(B))

LEN=100
fc=800e3/3
fs=800e3
f=fc/fs
x=np.arange(-LEN//2,LEN//2)+0.5
hx=2*fc/fs*np.sin(2*np.pi*f*x)/(2*np.pi*f*x)
cplot(hx)
print(hx)
plt.plot(np.log10(np.abs(np.fft.fft(hx))))
plt.show()
# cplot(np.fft.fft(hx))

noise=np.random.randn(2**18)+1j*np.random.randn(2**18)

cplot(noise)
plt.plot(np.log10(np.abs(np.fft.fft(noise))))
plt.show()

out=np.convolve(noise,hx, mode='same')
print(len(out))
plt.plot(np.log10(np.abs(np.fft.fft(noise))),'.')
plt.plot(np.log10(np.abs(np.fft.fft(out))),'.')
plt.axvline(len(out)*fc/fs,color="gray",linestyle="--",alpha=0.9)
plt.axvline(len(out)*(1-fc/fs),color="gray",linestyle="--",alpha=0.9)
plt.show()
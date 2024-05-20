import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('/home/roland/Desktop/Python/DSP')
import dsp


fc = 10
fs = 1000
# n_samp0 = 1000
# N = 100
multiply = 100
f_simb=1
T=2
n_samp0=fs*T
# baseband_signal=[1,-1,1,-1,0,1]
# baseband_signal = 2*np.random.randint(2, size=N)-np.ones(N)
# baseband_signal = np.random.randint(2, size=N)

# print(baseband_signal)

sig = 2*dsp.sines(fc,fs,n_samp0)
# sig=dsp.modulate_harmronic(fc,fs,f_simb,baseband_signal)

n_samp=len(sig)
t=np.arange(n_samp)/fs

noise = 0.01*np.sqrt(fs)*dsp.agwn(np.zeros(n_samp),1)
print(f"signal energy= {np.sum(np.abs(sig**2))/fs} J")
print(f"noise energy= {np.sum(np.abs(noise**2))/fs} J")
print(f"signal power= {np.sum(np.abs(sig**2))/n_samp}")
print(f"noise power= {np.sum(np.abs(noise**2))/n_samp}")
# plt.plot(sig2)
# plt.show()

noisy_signal=(sig+noise)/np.sqrt(fs)
print(f"full time energy= {np.sum(np.abs(noisy_signal**2))}")
spectrum = np.fft.fft(noisy_signal)/np.sqrt(n_samp)
print(f"full spectrum energy= {np.sum(np.abs(spectrum**2))}")

# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
plt.figure(figsize=[20,10])
plt.subplot(3,1,1)
dsp.complex_plot(sig,t=t)
plt.subplot(3,1,2)
dsp.complex_plot(noisy_signal,t=t)
plt.title(f"Time Domain\nfull energy= {np.sum(np.abs(noisy_signal)**2):.3f}")
plt.subplot(3,1,3)
dsp.complex_plot(spectrum,t=t/T*fs)
plt.title(f"Frq domain\nfull energy= {np.sum(np.abs(spectrum)**2):.3f}")
plt.xlabel("frequency")

# Adjust layout to create more space for titles and labels
# plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.6)

# plt.tight_layout()
plt.savefig(f"figure.png")
plt.show()



import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('/home/roland/Desktop/Python/DSP')
import dsp


fc = 1         # [Hz]
fs = 10000    # [Hz]
NPD = 0.001     # [W/Hz] Noise Power Density 
Signalpower = 20   # [dB]
T = 1          # [sec]
n_samp0 = fs*T  # [samps]
# baseband_signal=[1,-1,1,-1,0,1]
# baseband_signal = 2*np.random.randint(2, size=N)-np.ones(N)
# baseband_signal = np.random.randint(2, size=N)

# print(baseband_signal)

sig = np.sqrt(10**(Signalpower/10))*dsp.sines(fc,fs,n_samp0)
# sig=dsp.modulate_harmronic(fc,fs,f_simb,baseband_signal)

n_samp = len(sig)
t=np.arange(n_samp)/fs

noise = np.sqrt(fs*NPD)*dsp.agwn(np.zeros(n_samp),1)

print(f"T = {T} sec")
print(f"fc = {fc} Hz")
print(f"fs = {fs} Hz")
print(f"signal energy = {np.sum(np.abs(sig**2))/fs:.3f} J")
print(f"noise energy = {np.sum(np.abs(noise**2))/fs:.3f} J")
# print(f"signal power= {np.sum(np.abs(sig**2))/n_samp}")
# print(f"noise power= {np.sum(np.abs(noise**2))/n_samp}")

print(f"signal power = {np.sum(np.abs(sig**2))/fs/T:.3f} W/Hz")
print(f"noise power = {np.sum(np.abs(noise**2))/fs/T:.3f} W/Hz")
print(f"noise spectral power density = {np.sum(np.abs(noise**2))/fs/T/fs:.3f} W/Hz")

noisy_signal=(sig+noise)
print(f"full time energy = {np.sum(np.abs(noisy_signal**2)/fs):.3f} J")
spectrum = np.fft.fft(noisy_signal)/np.sqrt(fs*T)
print(f"full spectrum energy = {np.sum(np.abs((spectrum)**2)/fs):.3f} J")

plt.figure(figsize=[20,10])
plt.subplot(3,1,1)
dsp.complex_plot(sig,t=t)
plt.subplot(3,1,2)
dsp.complex_plot(noisy_signal,t=t)
plt.title(f"Time Domain\nfull energy = {np.sum(np.abs(noisy_signal)**2)/fs:.3f} J")
plt.subplot(3,1,3)
dsp.complex_plot(np.abs(spectrum)**2/fs,t=t/T*fs)
plt.title(f"Frq domain\nfull energy = {np.sum(np.abs(spectrum)**2)/fs:.3f} J")
plt.xlabel("frequency")



# Adjust layout to create more space for titles and labels
# plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.6)

# plt.tight_layout()
plt.savefig(f"figure.png")
# plt.show()

plt.figure(figsize=[10,5])
plt.plot(t/T*fs,10*np.log10(np.abs(spectrum)**2/fs))
plt.title(f"power density spectrum")
plt.xlabel("frequency [Hz]")
plt.ylabel("power [dB]")
plt.grid()
plt.savefig(f"power_density_spectrum.png")

plt.figure(figsize=[10,5])
dsp.complex_plot(spectrum,t=t/T*fs)
plt.title(f"signal spectrum")
plt.xlabel("frequency [Hz]")
plt.savefig(f"signal_spectrum.png")


# getting the expected power density:

AVG_NUM = 100

pow_spec=np.zeros(len(spectrum))
for i in range(AVG_NUM):
    sig = np.sqrt(10**(Signalpower/10))*dsp.sines(fc,fs,n_samp0)
    # sig=dsp.modulate_harmronic(fc,fs,f_simb,baseband_signal)

    n_samp = len(sig)
    t=np.arange(n_samp)/fs

    noise = np.sqrt(fs*NPD)*dsp.agwn(np.zeros(n_samp),1)
    noisy_signal=(sig+noise)

    pow_spec+=np.abs(np.fft.fft(noisy_signal)/np.sqrt(fs*T))**2/fs

pow_spec=pow_spec/AVG_NUM

plt.figure(figsize=[10,5])
plt.plot(t/T*fs,10*np.log10(pow_spec))
plt.title(f"Expected power density spectrum")
plt.xlabel("frequency [Hz]")
plt.ylabel("power [dB]")
plt.grid()
plt.savefig(f"expected_power_density_spectrum.png")

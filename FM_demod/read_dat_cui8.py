#!/bin/python3
# import uhd
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
from datetime import datetime
import argparse

# fs=800e3
fs=1024e3
fsD=1187.5
fc=103300000

def FFT_bandass(v,f_min,f_max,fs):
    vspec=np.fft.fft(v)
    vspec[0:int(len(v)*f_min/fs):]=0
    vspec[-int(len(v)*f_min/fs)+1::]=0
    vspec[int(len(v)*f_max/fs):-int(len(v)*f_max/fs)+1:]=0
    return np.fft.ifft(vspec)

PLOT_AUDIO_SPECTRUM=1

parser = argparse.ArgumentParser()
# parser.add_argument("file", help="file to read")
parser.add_argument("-f","--file", help="file to read from", nargs='?', type=str, required=True)
args = parser.parse_args()


now = datetime.now()
dstr = now.strftime("%Y-%m-%d_%H-%M-%S")

for P in range(1000):
    samples0=np.fromfile(args.file, dtype=np.uint8, count=400000, offset=400000*P)
    samples=samples0[0::2]+1j*samples0[1::2]
    samples=samples-128*(1+1j)

    

    print(len(samples))
    # print(samples[0:10])

    if 1:
        plt.figure()
        # plt.plot(samples,'.-')
        plt.plot(np.real(samples),'.-', alpha=0.5)
        plt.plot(np.imag(samples),'.-', alpha=0.5)
        plt.plot(np.abs(samples),'--', color='grey', alpha=0.5)
        plt.plot(-np.abs(samples),'--', color='grey', alpha=0.5)
        plt.legend(["Real","Imag","Abs"])
        plt.axhline(-128,linestyle="--",color="gray")
        plt.axhline(127,linestyle="--",color="gray")
        plt.ylim([-150,150])
        # plt.title(title)
        plt.grid()
        plt.show()
        plt.close()

    spec_samples=np.fft.fft(samples)
    spec_samples[int(len(spec_samples)*100e3/fs):-int(len(spec_samples)*100e3/fs)+1:]=0
    samples=np.fft.ifft(spec_samples)

    if 1:
        f=(np.arange(0,len(samples))/len(samples)*fs)-fs/2+fc
        # window=(1-np.cos(np.arange(len(samples))/len(samples)*np.pi*2))
        # plt.plot(window)
        # plt.show()
        plt.figure()
        plt.plot(f/1000,20*np.log10(np.fft.fftshift(np.abs(np.fft.fft(samples/len(samples))))),'.', color='C0', alpha=0.01)
        # plt.plot(np.log10(np.fft.fftshift(np.abs(np.fft.fft(samples*window)))),'-', color='C1', alpha=0.5)
        plt.xlabel("frequency [kHz]")
        plt.ylabel("Power [dB]")
        plt.grid()
        plt.show()


    
    diff=samples[1::]/samples[0:-1:]

    if 1:
        plt.figure()
        plt.plot(np.real(diff),'.-', alpha=1)
        plt.plot(np.imag(diff),'.-', alpha=1)
        plt.plot(np.abs(diff),'--', color='grey', alpha=0.5)
        plt.plot(-np.abs(diff),'--', color='grey', alpha=0.5)
        plt.legend(["Real","Imag","Abs"])
        plt.grid()
        plt.show()
        plt.close()

    f=(np.arange(0,len(diff))/len(diff)*fs)-fs/2
    # plt.figure()
    # # plt.plot(f,20*np.log10(np.fft.fftshift(np.abs(np.fft.fft(np.imag(diff))))),'-', color='C0')
    # plt.plot(20*np.log10(np.fft.fftshift(np.abs(np.fft.fft(np.imag(diff))))),'-', color='C0')
    # # plt.xlim([0,70e3])
    # plt.grid()
    # plt.xlabel("frequency [Hz]")
    # plt.show()

    
    # plt.figure()
    # # plt.plot(f,np.log10(np.abs(np.fft.fft(np.imag(diff)))),'-', color='C0', alpha=0.5)
    # plt.plot(f,20*np.log10(np.fft.fftshift(np.abs(np.fft.fft(np.imag(diff))))),'-', color='C0')
    # plt.xlim([10,19e3])
    # plt.xscale("log")
    # plt.grid()
    # plt.xlabel("frequency [Hz]")
    # plt.show()

    f=(np.arange(0,len(diff))/len(diff)*fs)

    audio=np.imag(diff)
    if PLOT_AUDIO_SPECTRUM:
        plt.figure()
        plt.plot(f/1000,20*np.log10(np.abs(np.fft.fft(audio/len(audio)))),'-', color='C0', alpha=1)
        plt.title("Audio Spectrum")

        plt.axvspan(30/1000, 15, alpha=0.3, color='C0', label="Mono Audio L+R")

        plt.axvline(19, color="black", alpha=1, linestyle=":")

        plt.axvspan(2*19-15, 2*19+15, alpha=0.3, color='C1', label="Stereo Audio L-R")
        plt.axvline(19*2, color="black", alpha=1, linestyle=":")

        plt.axvspan(3*19-fsD/1000, 3*19+fsD/1000, alpha=0.3, color='C2', label="RBDS")
        plt.axvline(19*3, color="black", alpha=1, linestyle=":")
        
        plt.axvspan(58.65, 76.65, alpha=0.3, color='C3', label="Direct Band")
        plt.axvline(92, color="black", alpha=1, linestyle=":", label="Audos Subcarrier")
        
        plt.xlim([0,99])
        plt.ylim([-100,-30])
        plt.xlabel("freqenycy [kHz]")
        plt.xlabel("Power [dB]")
        plt.legend()
        plt.grid()
        plt.show()

    if 1:
        plt.figure()
        plt.plot(f,20*np.log10(np.abs(np.fft.fft(audio))),'-', color='C0', alpha=0.5)
        plt.xlim(54e3,60e3)
        plt.grid()
        plt.show()

    # plt.plot(f,np.log10(np.abs(np.fft.fft(np.imag(diff)))),'-', color='C0', alpha=0.5)
    # spec=np.fft.fft(audio)
    # spec[int(len(diff)*59e3/fs):-int(len(diff)*59e3/fs)+1:]=0
    # spec[:int(len(diff)*55e3/fs):]=0
    # spec[-int(len(diff)*55e3/fs)+1::]=0
    audioFilt=FFT_bandass(audio,55e3,59e3,fs)
    # plt.plot((np.abs(spec)),'-', color='C0')
    # plt.grid()
    # plt.xlabel("frequency [Hz]")
    # plt.show()

    f=(np.arange(0,len(diff))/len(diff)*fs)
    if 1:
        plt.figure()

        plt.plot(f/1000,20*np.log10(np.abs(np.fft.fft(audio/len(audio)))),'-', color='C0', alpha=0.5)

        plt.axvspan(3*19-fsD/1000, 3*19+fsD/1000, alpha=0.3, color='C2', label="RBDS")
        plt.axvline(19*3, color="black", alpha=1, linestyle=":")
        
        plt.xlim([0,99])
        plt.ylim([-100,-30])
        plt.xlabel("freqenycy [kHz]")
        plt.xlabel("Power [dB]")
        plt.legend()
        plt.title("audiospectrum after filter")
        plt.plot(f/1000,20*np.log10(np.abs(np.fft.fft(audioFilt/len(audioFilt)))),'-', color='C0', alpha=1)
        plt.grid()
        plt.show()


    inv=audioFilt*np.sin(2*np.pi*57e3/fs*np.arange(len(audioFilt)))
    t=np.arange(len(audioFilt))/fs
    if 1:
        plt.plot(np.real(audioFilt))
        plt.plot(np.imag(audioFilt))
        plt.plot(t,np.abs(audioFilt))
        # plt.plot(-np.abs(inv))
        plt.grid()
        plt.show()

    invspec=np.fft.fft(inv)
    invspec[int(len(diff)*4e3/fs):-int(len(diff)*4e3/fs)+1:]=0
    f=(np.arange(0,len(inv))/len(diff)*fs)
    if 1:    
        plt.figure()
        plt.title("dataspectrum")
        plt.plot(f,20*np.log10(np.abs(invspec)),'-', color='C0', alpha=1)
        plt.grid()
        plt.show()

    inv2=np.fft.ifft(invspec)
    t=1e3*np.arange(len(inv2))/fs
    plt.plot(t,np.real(inv2))

    plt.xlabel("time [ms]")
    for i in range(int(len(inv2)/fs*fsD)):
        Td=1/fsD
        plt.scatter(1000*i*Td,inv2[int(i*Td*fs)],color="C1",alpha=1,marker="o")
        plt.scatter(1000*(i+0.25)*Td,inv2[int((i+0.25)*Td*fs)],color="C1",alpha=1,marker="x")
        plt.scatter(1000*(i+0.5)*Td,inv2[int((i+0.5)*Td*fs)],color="C2",alpha=1,marker="o")
        plt.scatter(1000*(i+0.75)*Td,inv2[int((i+0.75)*Td*fs)],color="C2",alpha=1,marker="x")

        plt.axvline(1000*i*Td,linestyle="--",color="C1",alpha=0.4)
        plt.axvline(1000*(i+0.25)*Td,linestyle="--",color="C1",alpha=0.4)
        plt.axvline(1000*(i+0.5)*Td,linestyle="--",color="C2",alpha=0.4)
        plt.axvline(1000*(i+0.75)*Td,linestyle="--",color="C2",alpha=0.4)

    plt.axhline(0,linestyle="--",color="black")
    plt.show()



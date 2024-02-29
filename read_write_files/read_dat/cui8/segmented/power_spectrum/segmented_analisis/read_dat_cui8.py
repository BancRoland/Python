#!/bin/python3
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
from datetime import datetime
import argparse
import os
import sys
sys.path.append('/home/roland/Desktop/Python/DSP')
import dsp


os.makedirs("output", exist_ok = True) 
os.makedirs("output/cpi", exist_ok = True)
os.makedirs("output/cpi/raw", exist_ok = True)
os.makedirs("output/cpi/filt", exist_ok = True) 
os.makedirs("output/powspec", exist_ok = True) 
os.makedirs("output/powspec/full_powspec", exist_ok = True) 
os.makedirs("output/powspec/filt_powspec", exist_ok = True) 

def power_fft(signal):
    return np.fft.fftshift(np.abs(np.fft.fft(signal/len(signal)))**2)

def read_samples(file, LEN, offset=0):
    samples0    = np.fromfile(file, dtype=np.uint8, count=2*LEN, offset=2*LEN*offset)
    samples     = samples0[0::2]+1j*samples0[1::2]
    samples     = samples-127*(1+1j)
    return samples


parser = argparse.ArgumentParser()
parser.add_argument("-f","--file",      help="file to read from",           nargs='?', type=str, required=True)
parser.add_argument("-l","--len",       help="length of segents",           nargs='?', type=int, required=True)
parser.add_argument("-rf","--frq",      help="radio frequency",             nargs='?', type=int, required=True)
parser.add_argument("-s","--samp_rate", help="sample rate",                 nargs='?', type=int, required=True)
parser.add_argument("-sf","--sig_frq",  help="relevant signal frequency",   nargs='?', type=int, required=True)
args = parser.parse_args()

file        = args.file
LEN         = args.len
rf          = args.frq
sr          = args.samp_rate
signal_frq  = args.sig_frq
FIR_LEN     = 100
fc          = 1000
f_sig       = rf + signal_frq

idx=0
log=[]

f_raw   = (np.arange(LEN)/LEN-0.5)*sr+rf
f       = (np.arange(LEN)/LEN-0.5)*sr+f_sig
t       = (np.arange(LEN)+idx*LEN)/sr


average_filt_power_spectrum = np.zeros(LEN, dtype="complex")
raw_average_power_spectrum = np.zeros(LEN, dtype="complex")

raw_samples = read_samples(file, LEN=LEN, offset=0)


while len(raw_samples) == LEN:

    raw_power_spectrum = power_fft(raw_samples)

    filt_samples = dsp.filter_channel(raw_samples, rf, sr, FIR_LEN=FIR_LEN, fc=fc, f_sig=f_sig)
    filt_power_spectrum = power_fft(filt_samples)
    
    average_filt_power_spectrum += filt_power_spectrum
    raw_average_power_spectrum += raw_power_spectrum

    log.append(np.sum(np.abs(filt_power_spectrum)))
    

    # ---------------
    # DISLAY filtered SIGNAL
    # ---------------

    plt.figure(figsize=(12,9))
    plt.subplot(2,1,1)
    plt.plot(t,np.real(filt_samples),".-", color='C0', alpha=1, label="Real")
    plt.plot(t,np.imag(filt_samples),".-", color='C1', alpha=1, label="Imag")
    plt.plot(t,np.abs(filt_samples),"--", color='gray', alpha=0.8, label="Abs")
    plt.plot(t,-np.abs(filt_samples),"-", color='gray', alpha=0.8, label="-Abs")
    plt.legend(loc='upper left')
    plt.ylabel("signal vaule []")
    plt.xlabel("time [sec]")
    plt.grid()
    plt.ylim([-128,127])
    
    plt.subplot(2,1,2)
    plt.plot(f,10*np.log10(filt_power_spectrum),".-")
    plt.grid()
    plt.ylabel("power [dB]")
    plt.xlabel("frequency [Hz]")
    plt.title(f"average power spectrum of filtered signal")
    # plt.ylim([-40,20])
    plt.suptitle(f"file: {file}")
    plt.savefig(f"output/cpi/filt/out_{idx:04d}.png")
    plt.close()


    # ---------------
    # DISLAY RAW SIGNAL
    # ---------------

    plt.figure(figsize=(12,9))
    plt.subplot(2,1,1)
    # dsp.complex_plot(samples)
    plt.plot(t, np.real(raw_samples),   ".-",   color='C0',     alpha=1,    label="Real")
    plt.plot(t, np.imag(raw_samples),   ".-",   color='C1',     alpha=1,    label="Imag")
    plt.plot(t, np.abs(raw_samples),    "--",   color='gray',   alpha=0.8,  label="Abs")
    plt.plot(t, -np.abs(raw_samples),   "-",    color='gray',   alpha=0.8,  label="-Abs")
    plt.legend(loc='upper left')
    plt.ylabel("signal vaule []")
    plt.xlabel("time [sec]")
    plt.grid()
    plt.ylim([-128,127])
    
    plt.subplot(2,1,2)
    plt.plot(f_raw,10*np.log10(raw_power_spectrum),".-")
    plt.grid()
    plt.ylabel("power [dB]")
    plt.xlabel("frequency [Hz]")
    plt.title(f"average power spectrum")
    # plt.ylim([-40,20])
    plt.suptitle(f"file: {file}")
    plt.savefig(f"output/cpi/raw/out_{idx:04d}.png")
    plt.close()


    # -------------
    # PRINT OUT LOGGED POWERS OF RELEWANT SIGNAL
    # -------------

    t2=(np.arange(len(log)))*LEN/sr
    plt.plot(t2,10*np.log10(log), ".-", color='C0', alpha=1, label="Abs")
    plt.grid()
    plt.ylabel("power [dB]")
    plt.xlabel("time [sec]")
    plt.title("Power of signal for a single cpi")
    # plt.ylim([-10,20])
    plt.savefig(f"output/log.png")
    plt.close()


    # -------------
    # AWERAGE POWERSPECTRUM OF RAW SIGNAL
    # -------------

    toprint_RAW_average_power_spectrum = raw_average_power_spectrum/(idx+1)
   
    plt.figure()
    plt.plot(f_raw,10*np.log10(toprint_RAW_average_power_spectrum))
    plt.ylim([-40,40])
    plt.grid()
    plt.ylabel("power [dB]")
    plt.xlabel("frequency [Hz]")
    plt.title("average power spectrum")
    plt.savefig(f"output/powspec/full_powspec/full_awg_power_spec_{idx}.png")
    plt.close()
   
    # -------------
    # AWERAGE POWERSPECTRUM OF FILTERED SIGNAL
    # -------------

    toprint_filt_power_spectrum = average_filt_power_spectrum/(idx+1)

    plt.figure()
    plt.plot(f,10*np.log10(toprint_filt_power_spectrum))
    plt.ylim([-40,40])
    plt.grid()
    plt.ylabel("power [dB]")
    plt.xlabel("frequency [Hz]")
    plt.title("average power spectrum")
    plt.savefig(f"output/powspec/filt_powspec/awg_power_spec_{idx}.png")
    plt.close()


    # -------------
    # INCREMENT INDEX, AND READ FRESH SAMPLES
    # -------------

    idx=idx+1
    print(f"{idx}")

    raw_samples = read_samples(file, LEN=LEN, offset=idx)



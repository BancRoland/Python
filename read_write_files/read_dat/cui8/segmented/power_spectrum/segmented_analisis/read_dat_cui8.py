#!/bin/python3
# import uhd
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

def power_fft(signal):
    return np.fft.fftshift(np.abs(np.fft.fft(signal/len(signal)))**2)

def read_samples(file, LEN, offset=0):
    samples0    = np.fromfile(file, dtype=np.uint8, count=2*LEN, offset=2*LEN*offset)
    samples     = samples0[0::2]+1j*samples0[1::2]
    samples     = samples-128*(1+1j)
    return samples

def plt_plot(samples):
    plt.figure()
    # plt.plot(samples,'.-')
    plt.plot(np.real(samples),  '.-',   color='C0',     alpha=1,    label="Real")
    plt.plot(np.imag(samples),  '.-',   color='C1',     alpha=1,    label="Imag")
    plt.plot(np.abs(samples),   '--',   color='grey',   alpha=0.5,  label="Abs")
    plt.plot(-np.abs(samples),  '--',   color='grey',   alpha=0.5,  label="-Abs")
    plt.legend()
    plt.ylim([-128,128])
    # plt.title(title)
    plt.grid()
    plt.show()


parser = argparse.ArgumentParser()
# parser.add_argument("file", help="file to read")
parser.add_argument("-f","--file",      help="file to read from",   nargs='?', type=str, required=True)
parser.add_argument("-l","--len",       help="length of segents",   nargs='?', type=int, required=True)
parser.add_argument("-rf","--frq",      help="radio frequency",     nargs='?', type=int, required=True)
parser.add_argument("-s","--samp_rate", help="sample rate",         nargs='?', type=int, required=True)
args = parser.parse_args()

file=args.file
LEN=args.len
rf=args.frq
sr=args.samp_rate
FIR_LEN = 100
fc = 1000
f_sig=rf+50750
# 101250750

# with open("out.dat", mode="rb") as input:
#     samples = input.read()
average_power_spectrum = np.zeros(LEN, dtype="complex")
FULL_average_power_spectrum = np.zeros(LEN, dtype="complex")

samples = read_samples(file, LEN=LEN, offset=0)

idx=0
log=[]
while len(samples) == LEN:

    t = (np.arange(len(samples))+idx*LEN)/sr

    FULL_power_spectrum = power_fft(samples)

    samples = dsp.filter_channel(samples, rf, sr, FIR_LEN=FIR_LEN, fc=fc, f_sig=f_sig)
    # dsp.complex_plot(samples)
    # plt.ylim([-15,15])
    # # plt.show()
    # plt.savefig(f"output/iq_{idx:04d}.png")
    # plt.close()

    plt.figure(figsize=(15,10))
    # plt.plot(samples,'.-')
    
    plt.subplot(2,1,1)
    plt.plot(t,20*np.log10(np.abs(samples)),   '.-',   color='C0',   alpha=1,  label="Abs")
    plt.legend()
    plt.ylim([-40,20])
    # plt.title(title)
    plt.grid()
    plt.ylabel("power [dB]")
    plt.xlabel("time [sec]")
    plt.title(f"Signal amplitude values in logarithmic scale at t= {t[0]:.2f}-{t[-1]:.2f} seconds")
    # plt.savefig(f"output/log_abs_{idx:04d}.png")
    # plt.close()

    power_spectrum = power_fft(samples)
    average_power_spectrum += power_spectrum
    FULL_average_power_spectrum += FULL_power_spectrum

    f=(np.arange(len(power_spectrum))/len(power_spectrum)-0.5)*sr+f_sig
    plt.subplot(2,1,2)
    plt.plot(f,10*np.log10(power_spectrum),".-")
    plt.grid()
    plt.ylabel("power [dB]")
    plt.xlabel("frequency [MHz]")
    plt.title(f"average power spectrum")
    plt.ylim([-40,20])
    plt.suptitle(f"file: {file}")
    # plt.show()
    plt.savefig(f"output/out_{idx:04d}.png")
    plt.close()

    idx=idx+1
    print(f"{idx}")

    samples = read_samples(file, LEN=LEN, offset=idx)
    log.append(np.sum(np.abs(power_spectrum)))

    t2=(np.arange(len(log)))*LEN/sr
    # plt.figure(figsize=(10,8))
    plt.plot(t2,10*np.log10(log), ".-", color='C0', alpha=1, label="Abs")
    plt.grid()
    plt.ylabel("power [dB]")
    plt.xlabel("time [sec]")
    plt.title("Power of signal for a single cpi")
    # plt.ylim([-10,20])
    plt.savefig(f"output/log.png")
    plt.close()
    

average_power_spectrum/=idx

f=(np.arange(len(average_power_spectrum))/len(average_power_spectrum)-0.5)*sr+f_sig
plt.figure()
plt.plot(f,10*np.log10(average_power_spectrum))
plt.grid()
plt.ylabel("power [dB]")
plt.xlabel("frequency [MHz]")
plt.title("average power spectrum")
plt.savefig(f"output/awg_power_spec.png")
plt.close()


FULL_average_power_spectrum/=idx

f=(np.arange(len(FULL_average_power_spectrum))/len(FULL_average_power_spectrum)-0.5)*sr+rf
plt.figure()
plt.plot(f,10*np.log10(FULL_average_power_spectrum))
plt.grid()
plt.ylabel("power [dB]")
plt.xlabel("frequency [MHz]")
plt.title("average power spectrum")
plt.savefig(f"output/full_awg_power_spec.png")
plt.close()
# plt.show()



    # plt.xlabel('xcím')
    # plt.ylabel('ycím')
    # title=('frq= %.2f MHz \nsamprate= %.2f Msamp/sec \nDate= %s' %(center_freq/1E6,sample_rate/1E6,dstr));
    # print(title)
    # plt.title(title)
    # #plt.legend(['sin(x)','cos(x)'])
    # plt.legend()
    # plt.grid()
    # plt.savefig(dstr+'.png')

    #plt.close()


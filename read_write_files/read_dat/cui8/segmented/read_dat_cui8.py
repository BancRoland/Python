#!/bin/python3
# import uhd
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
from datetime import datetime
import argparse
import matplotlib
matplotlib.use('Agg')

def plt_plot(samples):
    # plt.figure()
    # plt.plot(samples,'.-')
    plt.plot(np.real(samples),  '.-',   color='C0',     alpha=1,    label="Real")
    plt.plot(np.imag(samples),  '.-',   color='C1',     alpha=1,    label="Imag")
    plt.plot(np.abs(samples),   '--',   color='grey',   alpha=0.5,  label="Abs")
    plt.plot(-np.abs(samples),  '--',   color='grey',   alpha=0.5,  label="-Abs")
    plt.legend()
    plt.ylim([-128,128])
    # plt.title(title)
    plt.grid()
    # plt.show()
    plt.close()

def read_samples(file, LEN, offset=0):
    samples0    = np.fromfile(file, dtype=np.uint8, count=2*LEN, offset=2*LEN*offset)
    samples     = samples0[0::2]+1j*samples0[1::2]
    samples     = samples-128*(1+1j)
    return samples

parser = argparse.ArgumentParser()
# parser.add_argument("file", help="file to read")
parser.add_argument("-f","--file", help="file to read from", nargs='?', type=str, required=True)
parser.add_argument("-l","--len", help="length of segents", nargs='?', type=int, required=True)
args = parser.parse_args()

file=args.file
LEN=args.len

samples = read_samples(file=file, LEN=LEN,offset=0)

idx=0
while len(samples) == LEN:

    print(idx)

    plt_plot(samples)
    plt.close()

    idx=idx+1

    samples = read_samples(file=file, LEN=LEN,offset=idx)

    # plt.figure()
    # plt.plot(np.abs(fftpack.fft(samples)))
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


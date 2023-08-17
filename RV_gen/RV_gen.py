#!/bin/python3
# import uhd
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
from datetime import datetime
import argparse



# A0=400
# A1=600
# B0=200
# B1=300

# A0=0
# A1=1024
# B0=0
# B1=625

# #horiz
# H0=400
# H1=505
# #verti
# V0=225
# V1=300

parser = argparse.ArgumentParser()
# parser.add_argument("file", help="file to read")
parser.add_argument("-f","--file", help="file to read from", nargs='?', type=str, required=True)
parser.add_argument("-c","--codes", help="number of codes", nargs='?', type=int, required=True)
parser.add_argument("-z","--zeros", help="number of zeros", nargs='?', type=int, required=True)
parser.add_argument("-d","--dopp", help="doppler samples", nargs='?', type=int, required=True)
parser.add_argument("-w","--weight", help="weight for FIR", nargs='?', type=str, required=True)
parser.add_argument("-v","--view", help="view dinamically", nargs='?', type=int, default=1)
parser.add_argument("-r","--rot", help="rotate RV matrix", nargs='?', type=int, default=0)
parser.add_argument("-s","--step", help="number of skipped frames", nargs='?', type=int, default=10)

parser.add_argument("-h0","--hor0", help="vertical0", nargs='?', type=int, default=0)
parser.add_argument("-h1","--hor1", help="vertical0", nargs='?', type=int, default=0)
parser.add_argument("-v0","--ver0", help="horizontal0", nargs='?', type=int, default=0)
parser.add_argument("-v1","--ver1", help="horizontal0", nargs='?', type=int, default=0)

args = parser.parse_args()

CODES=args.codes
ZEROS=args.zeros
DOPP=args.dopp
LEN=CODES+ZEROS

ROT=args.rot
VIEW=args.view
STEP=args.step

H0=args.hor0
H1=args.hor1
V0=args.ver0
V1=args.ver1

if H1==0:
    if ROT:
        H1=DOPP
    else:
        H1=LEN
if V1==0:
    if ROT:
        V1=LEN
    else:
        V1=DOPP

code=np.fromfile(args.weight, dtype=np.complex64)

# now = datetime.now()
# dstr = now.strftime("%Y-%m-%d_%H-%M-%S")

filesize=DOPP*LEN*2  #Együttesen beolvasott fileméret

# i=0 #inkrementéációs szám, a beolvasási állapot számontartásához

# sampRX0=np.fromfile('outRX.dat', count=filesize, offset=i*filesize*8, dtype=np.complex64)

if VIEW:
    plt.ion()  # Turn on interactive mode

out=[]

RV=np.ones([10,10])

# plt.figure(figsize=(180, 100), dpi=100)
# plt.title("some title")
# plt.imshow(10*np.log10(np.abs(RV)), cmap="nipy_spectral", vmin=10, vmax=80)
# # plt.colorbar()

plt.figure(figsize=(20, 10))
samples0=np.fromfile(args.file, count=filesize, dtype=np.int16)
samples=samples0[0::2]+1j*samples0[1::2]   
out=np.correlate(samples,code, mode='same')
IMG=out.reshape(DOPP,LEN)
RV0 = np.fft.fft(IMG, axis=0)
max_index = np.argmax(RV0)
# print(f'max_index0= {max_index}')



for P in range(1000):
    # samples=np.fromfile(args.file, dtype=np.complex64, count=filesize, offset=P*filesize)
    samples0=np.fromfile(args.file, count=filesize, offset=STEP*P*filesize*2+max_index*4+4, dtype=np.int16)
    # samples0=np.fromfile(args.file, count=filesize, offset=5*P*filesize*2, dtype=np.int16)
    # samples = np.array(samples0.view(dtype=np.complex64))
    samples=samples0[0::2]+1j*samples0[1::2]   

    # out=np.concatenate([out,np.correlate(samples,code)])
    # out=np.concatenate([out,samples])
    out=np.correlate(samples,code, mode='same')

    IMG=out.reshape(DOPP,LEN)
    if ROT:
        IMG=IMG[:, LEN-V1:LEN-V0]
    else:
        IMG=IMG[:, H0:H1]
        # IMG=IMG[LEN-V1:LEN-V0, :]


    # IMG=np.real(IMG)

    RV0 = np.fft.fft(IMG, axis=0)


    # max_index = np.argmax(RV0)
    # # RV0 = np.hstack([RV0[max_index::],RV0[0:max_index:]])
    # plt.imshow(np.log10(np.hstack([np.abs(RV0),np.abs(RV0)])))
    # plt.show()

    # max_index = np.argmax(RV0)
    # RV0 = np.hstack([RV0[:,max_index+1:],RV0[:,:max_index+1]])
    # print(f'max_index= {max_index}')

    RV = np.fft.fftshift(RV0, axes=0)
    if ROT:
        RV=RV[H0:H1, :]
    else:
        RV=RV[V0:V1, :]

    if ROT:
        RV=np.rot90(RV)

    # plt.imshow(np.abs(RV))
    # plt.figure(figsize=(20, 10))
    # RVs=RV[180:300, 460:580]

    plt.subplots_adjust(left=0.05, right=1, top=0.9, bottom=0.05)  # Remove padding
    RVl=10*np.log10(np.abs(RV))
    MRK=np.argmax(RVl)
    print(f'Max index after FFT shift= {MRK}')
    plt.imshow(RVl, cmap="nipy_spectral", vmin=10, vmax=80)
    # plt.colorbar()
    if P==1:
        plt.colorbar()

    # plt.grid('True')

    if ROT:
        scatter=plt.scatter((MRK%(H1-H0)), np.floor(MRK/(H1-H0)), color='red', marker='o', facecolors='none', s=200)
    else:
        scatter=plt.scatter((MRK%(H1-H0)), np.floor(MRK/(H1-H0)), color='red', marker='o', facecolors='none', s=200)
    plt.title(f'max= {np.max(RVl):.2f} dB\nAVG= {np.mean(RVl):.2f} dB\nSNR= {np.max(RVl)-np.mean(RVl):.2f} dB')
    if VIEW:
        plt.pause(0.1)  # Adjust the pause duration as needed
        plt.show()
    plt.savefig(f"pic_{P}.png")
    scatter.remove()

#!/bin/bash

CFRQ=10e9   #centerFrequency[Hz]
SR=10e6    #sample rate [samp/sec]
NCODE=16  #correlation code samples []
NZEROS=128 #zeros for range []
DSAMP=256   #dopplerSamples []
DDEC=16     #dopplerDecimation []
POW=3.2     #Peak power [W]
RCS=1       #Radar cross section [m^2]
GAIN=29.5   #Antenna gain [dB]

cat header.txt

python3 run.py -c 3e8 -cFrq $CFRQ -sr $SR -Nc $NCODE -Nz $NZEROS -dS $DSAMP -dD $DDEC -P $POW -RCS $RCS -G $GAIN

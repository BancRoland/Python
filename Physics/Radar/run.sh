#!/bin/bash

CFRQ=10e9   #centerFrequency[Hz]
SR=100e6    #sample rate [samp/sec]
NCODE=1024  #correlation code samples []
NZEROS=6144 #zeros for range []
DSAMP=256   #dopplerSamples []
DDEC=1      #dopplerDecimation []
POW=3.2     #Peak power [W]
RCS=1       #Radar cross section [m^2]
GAIN=29.5   #Antenna gain [dB]

cat header.txt

python3 run.py -c 3e8 -cFrq $CFRQ -sr $SR -Nc $NCODE -Nz $NZEROS -dS $DSAMP -dD $DDEC -P $POW -RCS $RCS -G $GAIN

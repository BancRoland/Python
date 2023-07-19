#!/bin/bash

CFRQ=700   #centerFrequency[Hz]
SR=180    #sample rate [samp/sec]
NCODE=1  #correlation code samples []
NZEROS=8 #zeros for range []
DSAMP=16   #dopplerSamples []
DDEC=1     #dopplerDecimation []
POW=3.2     #Peak power [W]
RCS=1       #Radar cross section [m^2]
GAIN=29.5   #Antenna gain [dB]

cat header.txt

python3 run.py -c 340 -cFrq $CFRQ -sr $SR -Nc $NCODE -Nz $NZEROS -dS $DSAMP -dD $DDEC -P $POW -RCS $RCS -G $GAIN

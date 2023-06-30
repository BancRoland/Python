#!/bin/bash

CFRQ=9.9e9      #centerFrequency[Hz]
SR=20e6        #sample rate [samp/sec]
NCODE=110      #correlation code samples []
NZEROS=266     #zeros for range []
# NCODE=1536      #correlation code samples []
# NZEROS=6144     #zeros for range []
DSAMP=256       #dopplerSamples []
DDEC=32          #dopplerDecimation []
POW=3.2         #Peak power [W]
RCS=0.5         #Radar cross section [m^2]
GAIN=29.5       #Antenna gain [dB]

cat header.txt

python3 run.py -cFrq $CFRQ -sr $SR -Nc $NCODE -Nz $NZEROS -dS $DSAMP -dD $DDEC -P $POW -RCS $RCS -G $GAIN -RT 6000

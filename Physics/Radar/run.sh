#!/bin/bash

CFRQ=10e9 # centerFrequency[Hz]
SR=10e6     #sample rate [samp/sec]
NCODE=16   #correlation code samples []
NZEROS=128 #zeros for range []
DSAMP=512   #dopplerSamples
DDEC=16     #dopplerDecimation

cat header.txt

python3 run.py -c 3e8 -cFrq $CFRQ -sr $SR -Nc $NCODE -Nz $NZEROS -dS $DSAMP -dD $DDEC

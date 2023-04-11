#!/bin/bash

CFRQ=10e9 # centerFrequency[Hz]
SR=100e6     #sample rate [samp/sec]
NCODE=1024   #correlation code samples []
NZEROS=6144 #zeros for range []
DSAMP=512   #dopplerSamples

cat header.txt

python3 run.py -c 3e8 -cFrq $CFRQ -sr $SR -Nc $NCODE -Nz $NZEROS -dS $DSAMP

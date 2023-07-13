#!/bin/bash

CFRQ=9.9e9      #centerFrequency[Hz]
SR=100e6        #sample rate [samp/sec]
# NCODE=100      #correlation code samples []
# NZEROS=320     #zeros for range []
NCODE=1250      #correlation code samples []
NZEROS=5000     #zeros for range []
DSAMP=1024       #dopplerSamples []
DDEC=1          #dopplerDecimation []
POW=3.2         #Peak power [W]
RCS=0.5         #Radar cross section [m^2]
GAIN=29.5       #Antenna gain [dB]

# Rmax=1050       #Maximum distance [m]
# Rmin=1000       #Minimum distance [m]


python3 run.py -cFrq $CFRQ -sr $SR -Nc $NCODE -Nz $NZEROS -dS $DSAMP -dD $DDEC -P $POW -RCS $RCS -G $GAIN -RT 6000

cd ./KML
bash generate.sh $NCODE $NZEROS
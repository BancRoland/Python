#!/bin/bash

RZmin=5000
RZmax=6000

mkdir $RZmin\_$RZmax

Fa="47.365187"
Fl="18.428769"

# Fa="47.47046393386676"
# Fl="19.085548731155377"

FAlt=10000   #altitude of the focus [m]
Fdir=0      #direction [deg]


DIR=125.82  #beam direction
BW=2.8  #beamwidth

# CFRQ=9.9e9      #centerFrequency[Hz]
# SR=100e6        #sample rate [samp/sec]
# # NCODE=100      #correlation code samples []
# # NZEROS=320     #zeros for range []
# NCODE=1250      #correlation code samples []
# NZEROS=5000     #zeros for range []
# DSAMP=1024       #dopplerSamples []
# DDEC=1          #dopplerDecimation []
# POW=3.2         #Peak power [W]
# RCS=0.5         #Radar cross section [m^2]
# GAIN=29.5       #Antenna gain [dB]

# Rmax=1050       #Maximum distance [m]
# Rmin=1000       #Minimum distance [m]


# python3 run.py -cFrq $CFRQ -sr $SR -Nc $NCODE -Nz $NZEROS -dS $DSAMP -dD $DDEC -P $POW -RCS $RCS -G $GAIN -RT 6000 -DIR $DIR -BW $BW
cd ./KML
python3 run.py -DIR $DIR -BW $BW -FA $Fa -FL $Fl -FALT $FAlt -FDIR $Fdir -RZMIN $RZmin -RZMAX $RZmax


# cd ./KML
# bash generate.sh $Fa $Fl $FAlt $Fdir
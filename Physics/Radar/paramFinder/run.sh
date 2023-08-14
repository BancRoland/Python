#!/bin/bash
# Impulse radar paramfinder - find how long the correlation code,
#   and the following zeros should be in a period (fftSample) for given inputs.
# Input:
#   -   distance range for survailence. [ Rmin - Rmax ]
#           This range will be inside the unambigutiy zone, but outside of the interference zone.
#   -   multips:    for given RV integration time, it is preferred to have k*2^n amount of periods (fftSamples),
#           where k,n are natural numbers, and k is preferably small.
# Output:   

CFRQ=9.9e9      #centerFrequency[Hz]
Rmin=120       #Minimum distance [m]
Rmax=300       #Maximum distance [m]
samprates="100e6 50e6 20e6 10e6"    #investigated samplerates [Hz]
multips="1 3 5 7"   #investigated multipliers for the two-power samples []


echo $samprates > IN_samprates.csv
echo $multips > IN_multipliers.csv

python3 run.py -cFrq $CFRQ -Rmn $Rmin -Rmx $Rmax
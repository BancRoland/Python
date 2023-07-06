#!/bin/bash

CFRQ=9.9e9      #centerFrequency[Hz]
SR=100e6        #sample rate [samp/sec]
Rmin=600       #Minimum distance [m]
Rmax=1420       #Maximum distance [m]




# cat header.txt

python3 run.py -cFrq $CFRQ -sr $SR -Rmn $Rmin -Rmx $Rmax
# python3 run.py -cFrq $CFRQ -sr $SR -Nc $NCODE -Nz $NZEROS -dS $DSAMP -dD $DDEC -P $POW -RCS $RCS -G $GAIN -RT 6000 -Rmx $Rmax -Rmn $Rmin
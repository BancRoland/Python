#!/bin/bash

DATE=`date "+%F_%T"`

#FOR testvalues!
Rmax=3000       #Maximum distance [m]
Rmin=2500       #Minimum distance [m]


# # CSÁKVÁR
Fa=47.365187
Fl=18.428769
DIR=125.82  #beam direction

# # BÖRGÖND
# Fa=47.135016
# Fl=18.504998
# DIR=190.44  #beam direction



FAlt=10000   #altitude of the focus [m]
Fdir=0      #direction [deg]

BW=2.8  #beamwidth

python3 run.py -DIR $DIR -BW $BW -FA $Fa -FL $Fl -FALT $FAlt -FDIR $Fdir -FLDRN $DATE -RZMIN $Rmin -RZMAX $Rmax

cp input.csv $DATE/input.csv

xclip -sel clip < $DATE/params.txt

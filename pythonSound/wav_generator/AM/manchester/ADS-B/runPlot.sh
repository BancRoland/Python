#!/bin/bash

DATE=`date "+%F_%T"`
bash compile.sh
# rm pipe
# mkfifo pipe

# python3 plotter.py -A 1 -l 2 -s 8 &

arecord -r 44100 -f FLOAT_LE -d 0 -t raw - | ./wire.out | ./mix.out 44100 1000 | ./lpf.out 0.998 | ./decimate.out 882 > mic.cf32 #| tee mic.cf32 > pipe 


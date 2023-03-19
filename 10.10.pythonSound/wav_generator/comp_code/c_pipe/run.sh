#!/bin/bash

bash compile.sh
mkfifo pipe

FS=44100
MFRQ=1000
BITRATE=100
OVERSAMP=3

python3 plotter.py -s 3 -l 30 -A 10000 &

amixer sset 'Headphone Mic Boost',0 1


arecord -r $FS -f FLOAT_LE -d 0 -t raw - | ./wire.out | ./mix.out $FS $MFRQ | lpf.out 0.995 | ./resamp.out $BITRATE $FS $OVERSAMP | ./fir.out compCode.cf32 $OVERSAMP > pipe



#!/bin/bash

DATE=`date "+%F_%T"`
mkfifo pipe
cat pipe | python3 run.py &

amixer -D pulse sset Master 80%
amixer sset 'Headphone Mic Boost',0 1

#arecord -r 44100 -f S32_LE -d 2 -t raw - > mic_$DATE.i32
#arecord -r 10000 -f S32_LE -d 10 -t raw - > pipe
arecord -r 44100 -f FLOAT_LE -d 0 -t raw - > pipe

#cp mic_$DATE.i32 input.i32

#python3 run.py

#cat mic_$DATE.i32 | ./corrDet_dr210 > out.txt

#!/bin/bash

DATE=`date "+%F_%T"`

#touch mic_photo_$DATE.i32

amixer sset 'Headphone Mic Boost',0 1

arecord -r 44100 -f FLOAT_LE -d 0 -t raw - >> mic_photo_$DATE.i32



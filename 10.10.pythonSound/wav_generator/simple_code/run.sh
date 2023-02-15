#!/bin/bash

BITRATE=130
FS=44100
MFRQ=1000

DATE=`date "+%F_%T"`

python3 codeGen.py

amixer sset 'Headphone Mic Boost',0 1

LOC_c=/home/roland/Desktop/c_code/pipeline/stream/downMix/micprocess/barker

#aplay -r 44100 out.wav &
bash aplayer.sh 5 3 &


cd $LOC_c
bash $LOC_c/run.sh 44100 1000 100 &

#echo WTF
#echo ""
#cd $PWD_p
#ls
#aplay -r 44100 out.wav &

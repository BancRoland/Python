#!/bin/bash

BITRATE=130
FS=44100
MFRQ=1000

DATE=`date "+%F_%T"`

python3 codeGen.py

LOC=/home/roland/Desktop/c_code/pipeline/stream/downMix/micprocess/barker
PWD0=eval pwd


amixer -D pulse sset Master 10%


cd $LOC

bash $LOC/run.sh $1 &

sleep 5
echo $PWD0/out.wav

aplay -r 44100 $PWD/out.wav &

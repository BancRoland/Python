#!/bin/bash

if [[ $# -eq 2 ]]
then
	VOL=$1
	NUM=$2
else
	echo "bash aplay.sh [VOL=(0..100)] [NUM=3]"
	VOL=10
	NUM=3
fi
	
amixer -D pulse sset Master $VOL%

sleep 5

for i in $(seq 1 $NUM);
do
	echo $i
	aplay -r 44100 out.wav 
done

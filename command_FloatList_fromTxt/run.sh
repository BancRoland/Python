#!/bin/bash
echo 1400 40 0 1000000 > ctrl.txt
echo start > out.txt

tail -n 1 -f ctrl.txt | python3 run.py >> out.txt &

for i in $(seq 1400 10 1500)
do
	echo $i 50 0 1000000 >> ctrl.txt
	#sleep 0.1
done

#!bin/bash

for i in *.c
do
#	echo $i
#	echo ${i%.*}.out
	gcc $i -lm -o ${i%.*}.out
done

./barker13.out 0 0 > barker13.cf32

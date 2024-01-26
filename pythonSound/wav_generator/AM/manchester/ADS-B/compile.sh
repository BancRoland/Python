#!bin/bash

for i in *.c
do
#	echo $i
#	echo ${i%.*}.out
	gcc $i -lm -o ${i%.*}.out
done

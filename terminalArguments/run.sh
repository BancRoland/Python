#!/bin/bash

echo -e "\n\nprint out the input\n"
python3 parsarg0.py cica
# cica


echo -e "\n\n verbose positional argumets and -v argument\n"
python3 parsarg1.py 2
# 4

python3 parsarg1.py 3 -v
# the squre of 3 equals 9

python3 parsarg1.py 4 --verbose
# the squre of 4 equals 16


echo -e "\n\nverbose options:\n"
python3 parsarg2.py 5 -v 0
# 25

python3 parsarg2.py 6 -v 1
# the square of 6 equals 36

python3 parsarg2.py 7 -v 2
# 7^2 = 49

python3 parsarg2.py 8 -v 3
# usage: parsarg2.py [-h] [-v {0,1,2}] square
# parsarg2.py: error: argument -v/--verbose: invalid choice: 3 (choose from 0, 1, 2)

python3 parsarg2.py 9 -v a
# usage: parsarg2.py [-h] [-v {0,1,2}] square
# parsarg2.py: error: argument -v/--verbose: invalid int value: 'a'


echo -e "\n\nverbose multiple letter:\n"
python3 parsarg3.py 10 -vv
# the square of 10 equals 100


echo -e "\n\ncode for x^y:\n"
python3 parsarg4.py 2 3 -vv
# 2 to the power of 3 is 8


echo -e "\n\nprint filename when running"
python3 parsarg5.py 4 5 -vv
# Running '/home/bancr/Desktop/python/10.11.terminalArguments/parsarg5.py'

echo -e "\n\nquiet option and multiple options"
python3 parsarg6.py 12 13 -v
# 12 to the power 13 equals 106993205379072

python3 parsarg6.py 6 7 -q
# 279936

python3 parsarg6.py 8 9 -vq
# usage: parsarg6.py [-h] [-v | -q] x y
# parsarg6.py: error: argument -q/--quiet: not allowed with argument -v/--verbose
## MERT EXCLUSIVE GROUP

python3 parsarg6.py 10 11
# 10^11 == 100000000000

python3 parsarg7.py -r 10
# 314.159
python3 parsarg7.py -r 10 -pi 4
# 400.0
# meg tudok adni betűvel egy változót, és kötelezővé tudom tenni


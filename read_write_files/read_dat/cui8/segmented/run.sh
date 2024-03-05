#!/bin/bash

LENGTH=1000
# FILE=/home/roland/Desktop/borgond_dielect_ant/data/out_24_02_27_141347.cf32
FILE=~/Desktop/c_code/SDR/field_test/data/out_2024_03_05_154335_550.cui8


python3 read_dat_cui8.py -l $LENGTH -f $FILE
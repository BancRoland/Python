#!/bin/bash

# mkdir meas_$timestamp

# LENGTH=32768
LENGTH=8192
# FILE=/home/roland/Desktop/borgond_dielect_ant/data/out_24_02_27_$timestamp.cf32
FILE=/home/roland/Desktop/Python/read_write_files/write_dat/cui8/sine/out.cui8
FRQ=100000000
SAMP=100000
SIG_FRQ=25000

python3 read_dat_cui8.py -l $LENGTH -f $FILE -rf $FRQ -s $SAMP -sf $SIG_FRQ
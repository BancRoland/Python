#!/bin/bash

LENGTH=4096
FILE=/home/roland/Desktop/borgond_dielect_ant/data/out_24_02_27_141600.cf32
FRQ=101200000
SAMP=300000

python3 read_dat_cui8.py -l $LENGTH -f $FILE -rf $FRQ -s $SAMP
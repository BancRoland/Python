#!/bin/bash

# 14:13:47    a drón 7 m magaasan eltávolodik a az antennától 
# 14:16:00    köberepülés 7 magasan 50 m suarú pályán kb 20 km/h-val de inkább 4 m magasság
# 14:18:41    körbeforgattuk az antennát

# timestamp=141347    #eltavolodas
timestamp=141600  # korbererpules
# timestamp=141841  # korbeforg

# mkdir meas_$timestamp

LENGTH=32768
FILE=/home/roland/Desktop/borgond_dielect_ant/data/out_24_02_27_$timestamp.cf32
FRQ=101200000
SAMP=300000

python3 read_dat_cui8.py -l $LENGTH -f $FILE -rf $FRQ -s $SAMP
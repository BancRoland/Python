#!/bin/bash

NUM=0022
DATE=230801

# CODES=125
# ZEROS=500
DOPP=1024
STEPS=10
ROT=1
VIEW=0



V0=0; V1=0; H0=0; H1=0

# V0=400
# V1=512
# H0=3400
# H1=3500

# V0=400
# V1=510
# H0=300
# H1=400

# V0=400
# V1=510
# H0=300
# H1=400

# cat README_$DATE.txt | grep kr$DATE$NUM
str=$(eval cat /mnt/big_storage/${DATE}_kuvik/README_$DATE.txt | grep kr$DATE$NUM)
arr=( ${str//[!0-9]/ } )
CODES=${arr[2]}
ZEROS=${arr[3]}

# -----
# gcc fir.c -lm -o fir.out
# gcc ci16_2_comp.c -lm -o ci16_2_comp.out

# cat samp.ci16 | ./ci16_2_comp.out | ./fir.out c125.cf32 1 > out.cf32
python3 chirp_gen.py --sr 2 --Fmin -1 --Fmax 1 --codes $CODES --zeros 0
# sudo cat /mnt/big_storage/${DATE}_kuvik/kr$DATE$NUM.ci16 | ./ci16_2_comp.out | ./fir.out c$CODES.cf32 1 > out.cf32

sudo python3 RV_gen.py -f /mnt/big_storage/${DATE}_kuvik/kr$DATE$NUM.ci16 -w c$CODES.cf32 -c $CODES -z $ZEROS -d $DOPP -s $STEPS -v $VIEW -r $ROT -h0 $H0 -h1 $H1 -v0 $V0 -v1 $V1


# python3 RV_gen.py -f out.cf32 -c $CODES -z $ZEROS -d $DOPP
# rm c$CODES.cf32

mkdir pics/pics_$DATE$NUM
mv *.png pics/pics_$DATE$NUM
# -------


# time sudo head -c 100M /mnt/big_storage/${DATE}_kuvik/kr$DATE$NUM.ci16 > test.ci16
# time cat test.ci16 | ./ci16_2_comp.out | ./fir2.out c$CODES.cf32 1 > out2.cf32
# rm test.ci16
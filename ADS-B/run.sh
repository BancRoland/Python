#!/bin/bash

for FILE in $(eval ls /home/roland/Desktop/kuvik/ads-b/log/raw/23_08_25)
do
    echo FILE
done

# # Így van meg egy koordináta:
# head -c 4400k adsb_samp.cui8 > test0.cui8
# tail -c 4300k test0.cui8 > test.cui8
# ./dump1090 --ifile test.cui8 --interactive
# # ./dump1090 --ifile test.cui8
# python3 read_dat_cui8.py -f test.cui8


# Így van meg egy packet
head -c 200k adsb_samp.cui8 > test0.cui8
tail -c 100k test0.cui8 > test.cui8
./dump1090 --ifile test.cui8
# ./dump1090 --ifile test.cui8
python3 read_dat_cui8.py -f test.cui8
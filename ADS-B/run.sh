#!/bin/bash

# # Így van meg egy koordináta:
# head -c 4400k adsb_samp.cui8 > test0.cui8
# tail -c 4300k test0.cui8 > test.cui8
# ./dump1090 --ifile test.cui8 --interactive
# # ./dump1090 --ifile test.cui8
# python3 read_dat_cui8.py -f test.cui8




# Így van meg egy packet
# *8d4d242d582fc72a602dc760adf3;
# CRC: 60adf3 (ok)
# DF 17: ADS-B message.
#   Capability     : 5 (Level 2+3+4 (DF0,4,5,11,20,21,24,code7 - is on airborne))
#   ICAO Address   : 4d242d
#   Extended Squitter  Type: 11
#   Extended Squitter  Sub : 0
#   Extended Squitter  Name: Airborne Position (Baro Altitude)
#     F flag   : odd
#     T flag   : non-UTC
#     Altitude : 8500 feet
#     Latitude : 103728 (not decoded)
#     Longitude: 11719 (not decoded)
head -c 200k adsb_samp.cui8 > test0.cui8
tail -c 100k test0.cui8 > test.cui8
./dump1090 --ifile test.cui8
# ./dump1090 --ifile test.cui8
python3 read_dat_cui8.py -f test.cui8
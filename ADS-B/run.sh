#!/bin/bash

# Így van meg egy koordináta:
# 4960641   	11872   	918  	45.8369 	20.9312 	-------	1693756235
FILE=/home/roland/Desktop/kuvik/ads-b/log/raw/23_08_25/raw_23_08_25_14:55:20.cui8
# head -c 3600k $FILE > test0.cui8
# tail -c 1800k test0.cui8 > test.cui8
# ./dump1090 --ifile test.cui8 --interactive
# python3 read_dat_cui8.py -f test.cui8

# Így van meg egy üzenet:
# 28 HEX -> 28*4=112 bit
# *8d3c4b2e58b3f006dc4b091684b2;
# CRC: 1684b2 (ok)
# DF 17: ADS-B message.
#   Capability     : 5 (Level 2+3+4 (DF0,4,5,11,20,21,24,code7 - is on airborne))
#   ICAO Address   : 3c4b2e
#   Extended Squitter  Type: 11
#   Extended Squitter  Sub : 0
#   Extended Squitter  Name: Airborne Position (Baro Altitude)
#     F flag   : even
#     T flag   : non-UTC
#     Altitude : 34975 feet
#     Latitude : 878 (not decoded)
#     Longitude: 19209 (not decoded)
# ---------------
# head -c 3573k $FILE > test0.cui8
# tail -c 1k test0.cui8 > test.cui8
# ./dump1090 --ifile test.cui8
# python3 read_dat_cui8.py -f test.cui8

# ./dump1090 --ifile clear.cui8
# ---------------
# A DUMP1090 ezt dekódolta, ami ezeket a biteket jelenti
# 8d3c4b2e58b3f006dc4b091684b2
# 8d3c4b2e58b3f006dc4b091684b2
# 8d3c4b2e58b3f006dc4b091684b2
# 1000 1101 0011 1100
# 0100 1011 0010 1110
# 0101 1000 1011 0011
# 1111 0000 0000 0110
# 1101 1100 0100 1011
# 0000 1001 0001 0110
# 1000 0100 1011 0010

# Én pythonnal ezeket dekódoltam
#decodable bitstring (60 HEX=240 bit)
# 1010 0001 0100 0000       EZ A PREAMBLE
# 10 01 01 01  10 10 01 10  01 01 10 10  10 10 01 01 
# 01 10 01 01  10 01 10 10  01 01 10 01  10 10 10 01
# 01 10 01 10  10 01 01 01  10 01 10 10  01 01 10 10
# 10 10 10 11  01 01 01 00  01 01 01 01  01 10 10 01
# 10 10 01 10  10 10 01 00  01 10 01 01  10 01 10 10
# 01 00 01 01  10 01 01 10  01 01 01 10  01 10 10 01
# 10 01 01 01  01 10 01 01  10 01 10 10  01 01 10 01

# dump1090 üzenete ismét:
# 8d3c 4b2e 58b3 f006 dc4b 0916 84b2
# Saját dekódolás:
# 1000 1101 0011 1100     8d3c
# 0100 1011 0010 1110     4b2e
# 0101 1000 1011 0011     58b3
# 111? 000? 0000 0110     ??06
# 1101 110? 0100 1011     d?4b
# 0?00 1001 0001 0110     ?916
# 1000 0100 1011 0010     84b2

# szegmentálás:
# 10001   DOWNLINK FORMAT 17 or 18
# 101     CAPABILITY
# 0011 1100 0100 1011 0010 1110   ICAO
# 01011 000   Type Code
# 1011 0011 1111 0000 0000 0110 1101 1100 0100 1011 0000 1001   DATA
# 0001 0110 1000 0100 1011 0010 Parity Interrogator


head -c 9987k $FILE > test0.cui8
tail -c 2k test0.cui8 > test.cui8
./dump1090 --ifile test.cui8
python3 read_dat_cui8.py -f test.cui8

./dump1090 --ifile clear.cui8
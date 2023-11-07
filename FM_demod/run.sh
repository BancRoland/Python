#!/bin/bash

GAIN=40

rtl_sdr -s 1024000 -f 103300000 -g 40 -n 32768 - > data_1024k_${GAIN}g.cui8
python3 read_dat_cui8.py -f data_1024k_${GAIN}g.cui8

# rtl_sdr -s 2048000 -f 103300000 -g 10 -n 32768 - > data_2048k_10g.cui8
# python3 read_dat_cui8.py -f data_2048k_10g.cui8
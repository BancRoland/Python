#!/bin/bash

DATE=$(date "+%F_%T")
rm pipe
mkfifo pipe
python3 run.py&

sudo cat /dev/hidraw1 > pipe
#cat /dev/random > pipe
echo 9977

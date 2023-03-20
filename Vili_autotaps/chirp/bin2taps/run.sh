#!/bin/bash

binCntr=$(eval ls *.bin | wc -l)

echo $binCntr

if [[ $binCntr -eq 1 ]]
then
    binName=$(ls *.bin)
    echo $binName
    python3 bin2taps.py $binName
    cat bin
else
    echo ERROR!
    echo $binCntr .bin files exists:
    echo *.bin
fi

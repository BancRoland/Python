#!/bin/bash
var0=$(pwd)

rm SUM_FULL.csv
touch SUM_FULL.csv

echo $var0/file
for year in {2020..2024}
# for year in 2024
do
    cd $var0/log/$year
    rm SUM.csv
    touch SUM.csv
    for f in *.csv; do
        cat "$f" >> SUM.csv
    done

    cp SUM.csv $var0
    cat SUM.csv >> $var0/SUM_FULL.csv       # hozzáillesztem az összegzéshez

    # python3 $var0/csv_read.py

    cd $var0
done

mv $var0/SUM_FULL.csv $var0/SUM.csv
python3 $var0/csv_read.py
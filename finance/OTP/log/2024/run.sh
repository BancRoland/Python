#!/bin/bash

rm SUM.csv
touch SUM.csv
for f in *.csv; do
    cat "$f" >> SUM.csv
done

cp SUM.csv ../../
python3 ../../csv_read.py
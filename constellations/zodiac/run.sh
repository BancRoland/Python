#!/bin/bash

source ../venv/bin/activate

source list.sh

# constellations=("${circumpolar[@]}")
constellations=("${full[@]}")
echo $perseus
echo $constellations

rm zodiac0.csv
rm zodiac.csv

echo "Name,Right Ascension,Declination,Apparent Magnitude,Constellation" >> zodiac0.csv
for constellation in "${constellations[@]}"; do

    tail -n +2 constellations/prev/$constellation.csv >> zodiac0.csv
    echo "" >> zodiac0.csv

done
awk 'NF' zodiac0.csv >> zodiac.csv
rm zodiac0.csv

python3 csv_read_zodiac.py
python3 zodiac_plotter.py
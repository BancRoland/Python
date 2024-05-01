#!/bin/bash

source ../venv/bin/activate

# name=full
# name=zodiac_only
# name=zodiac
# name=circumpolar
name=perseus

source scenarios/$name/list.sh
vars=scenarios/$name/variables.toml
rm variables.toml
cp $vars ./variables.toml

constellations_list=("${constellations[@]}")

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
# python3 zodiac_plotter.py -dec_deg0 $Dec_deg -dec_degmin $Dec_min -dec_degsec $Dec_sec -RA_hour $Ra_hour -RA_min $Ra_min -RA_sec $Ra_sec -zrot $zrot
rm ./variables.toml
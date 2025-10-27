#!/bin/bash

source ../venv/bin/activate

# name=blind_elevation
# name=blind_spots
# name=full
# name=equatorial
# name=zodiac_only
# name=zodiac
# name=circumpolar
# name=circumpolar_easy
# name=perseus
# name=spring_midnight
# name=winter_midnight
name=summer_midnight
# name=full_only_border
# name=summer_midnight_all
# name=fall_midnight
# name=full

source scenarios/$name/list.sh
source scenarios/$name/list_lines.sh
vars=scenarios/$name/variables.toml
rm variables.toml
cp $vars ./variables.toml

constellations_list=("${constellations[@]}")
constellations_lines_list=("${lines[@]}")



# For the stars
rm zodiac0.csv
rm zodiac.csv

echo "Name,Right Ascension,Declination,Apparent Magnitude,Constellation" >> zodiac0.csv
for constellation in "${constellations[@]}"; do

    tail -n +2 constellations/prev/$constellation.csv >> zodiac0.csv
    echo "" >> zodiac0.csv

done
awk 'NF' zodiac0.csv >> zodiac.csv
rm zodiac0.csv



# For the lines
rm zodiac0_lines.csv
rm zodiac_lines.csv

echo "Name1,Right Ascension1,Declination1,Apparent Magnitude1,Constellation1,Name2,Right Ascension2,Declination2,Apparent Magnitude2,Constellation2,linestyle,color,width,alpha" >> zodiac0_lines.csv
for line in "${lines[@]}"; do

    tail -n +2 constellations/prev/$line.csv >> zodiac0_lines.csv
    echo "" >> zodiac0_lines.csv

done
awk 'NF' zodiac0_lines.csv >> zodiac_lines.csv
rm zodiac0_lines.csv




python3 csv_read_zodiac.py
python3 zodiac_plotter.py
# python3 zodiac_plotter.py -dec_deg0 $Dec_deg -dec_degmin $Dec_min -dec_degsec $Dec_sec -RA_hour $Ra_hour -RA_min $Ra_min -RA_sec $Ra_sec -zrot $zrot
# rm ./variables.toml

mv toprint.png scenarios/$name
mv toprint2.png scenarios/$name
mv toprint_polar.png scenarios/$name
mv toprint_polar2.png scenarios/$name
mv toprint_polar_lines.png scenarios/$name
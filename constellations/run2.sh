#!/bin/bash

header="Name,Right Ascension,Declination,Apparent Magnitude,Constellation"

# constellation="Sagittarius"
constellations=(
    "Ursa Major"
    "Ursa Minor"
    "Cassiopeia"
    "Cepheus"
    "Pegasus"
    "Perseus"
    "Orion"
    "Boötes"
    "Auriga"
    "Andromeda"
    "Coma Berenices"
    "Hercules"
    "Corona Borealis"
    "Lyra"
    "Cygnus"
    "Aquila"
    "Serpens"
)

for constellation in "${constellations[@]}"; do

    filename="${constellation// /_}"
    file=./zodiac/constellations/${filename}_0.csv

    rm $file
    echo $header >> $file
    cat constellations.csv | grep "$constellation" >> $file

done
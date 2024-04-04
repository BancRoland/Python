#!/bin/bash

header="Name,Right Ascension,Declination,Apparent Magnitude,Constellation"

# constellation="Sagittarius"
constellations=(
    # "Ursa Major"
    # "Ursa Minor"
    # "Cassiopeia"
    # "Cepheus"
    # "Pegasus"
    # "Perseus"
    # "Orion"
    # "Boötes"
    # "Auriga"
    # "Andromeda"
    # "Coma Berenices"
    # "Hercules"
    # "Corona Borealis"
    # "Lyra"
    # "Cygnus"
    # "Aquila"
    # "Serpens"
    # "Delphinus"
    # "Hydra"
    # "Canis Major"
    # "Canes Venatici"
    # "Leo Minor"
    # "Lynx"
    # "Camelopardalis"
    # "Monoceros"
    # "Corvus"
    # "Crater"
    # "Sextans"
    # "Ophiuchus"
    # "Sagittarius"
    # "Vulpecula"
    # "Lacerta"
    # "Triangulum"
    # "Sagitta"
    "Canis Minor"
)

for constellation in "${constellations[@]}"; do

    filename="${constellation// /_}"
    file=./zodiac/constellations/${filename}_0.csv

    rm $file
    echo $header >> $file
    cat constellations.csv | grep "$constellation" >> $file

done
#!/bin/bash

source ../venv/bin/activate

constellations=(
"Andromeda"
"Boötes"
"Capricornus"
"Cygnus"    
# "Hydra"    
# "Lynx"     
"Pegasus"    
"Scorpius" 
"Ursa_Minor"
"Aquarius"
# "Camelopardalis"
"Cassiopeia"       
# "Delphinus"  
# "Lacerta"    
"Lyra"       
"Perseus"      
# "Sextans"     
"Virgo"
"Aquila"     
"Cancer"          
"Cepheus"          
"Draco"      
"Leo"        
# "Monoceros"  
"Pisces"       
"Taurus"
"Aries"      
# "Canes_Venatici"  
"Coma_Berenices"   
"Gemini" 
# "Leo_Minor"
"Ophiuchus"
# "Sagitta"
# "Triangulum"
"Auriga"  
"Canis_Minor"
"Corona_Borealis"
"Hercules"
"Libra"
"Orion"
"Sagittarius"
"Ursa_Major"
)

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
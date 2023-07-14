#!/bin/bash

# CFRQ=9.9e9      #centerFrequency[Hz]
# SR=100e6        #sample rate [samp/sec]
# Rmin=600       #Minimum distance [m]
# Rmax=1420       #Maximum distance [m]
# fftiA=(1 3 5 7)

Fa=$1
Fl=$2


FAlt=$3   #altitude of the focus [m]
Fdir=$4      #firection [deg]

CENTRE="$Fa, $Fl"

fldrN=$5


gcc -o ring.out ring.c -lm                #CentreAltitude, CentreLongitude, Rmin, Rmax, fillColor, name
gcc -lm -o tags.out tags.c                #CentreAltitude, CentreLongitude, name
gcc -o circ.out circ.c -lm                #CentreAltitude, CentreLongitude, Radius, fillColor, edgeColor, edgeWidth, name
gcc -o path.out path.c -lm                #name, edgeColor, edgeWidth\n longitude, altitude, height
gcc -o slice.out slice.c -lm              #CentreAltitude, CentreLongitude, Radius, theta0, alpha, fillColor, edgeColor, edgeWidth, name
gcc -o ringSlice.out ringSlice.c -lm      #CentreAltitude, CentreLongitude, Rmin, Rmax, theta0, alpha, fillColor, edgeColor, edgeWidth, name

name=$(<docName.txt)
# echo $name

outfile=out.kml

echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<kml xmlns=\"http://www.opengis.net/kml/2.2\">
<Document>
<name>$name</name>

    <LookAt>
      <longitude>$Fl</longitude>
      <latitude>$Fa</latitude>
      <altitude>$FAlt</altitude>
      <heading>$Fdir</heading>        <!-- Direction in degrees (0 = north) -->
      <tilt>0</tilt>              <!-- Tilt angle in degrees (0 = straight down) -->
      <range>0</range>         <!-- Distance from the point of interest -->
      <altitudeMode>relativeToGround</altitudeMode>
    </LookAt>" >> $outfile


./ring.out >> $outfile

./circ.out >> $outfile

./slice.out >> $outfile

./ringSlice.out >> $outfile


echo -e "$CENTRE, RADAR" > coordTags.txt
./tags.out >> $outfile

echo -e "Poros út, a0ff0000, 2
18.45666272327564,47.3822744227169,0
18.45989313668887,47.35088673167731,0
18.46118375248061,47.34991827429986,0
18.46404795409673,47.35098408033408,0
18.46507051719443,47.35053676753202,0
18.46767171317832,47.34877350322729,0
18.47176220563825,47.34610919555468,0
18.47654001699182,47.3428555653709,0
18.48116994536275,47.33975066445169,0
18.48223863189492,47.33908996551414,0
18.48476029457003,47.33782432894436,0
18.49511681323541,47.33270746362079,0
18.50384872663293,47.32853594412128,0
18.5049947127632,47.32803451114862,0
18.50548246027286,47.32791332487966,0
18.50577478375718,47.3279512026004,0
18.51069056351649,47.3308711236139,0
18.51486367617241,47.33379139015951,0
18.51764719220909,47.335747064178,0
18.52018511373566,47.33733111059268,0
18.52062241803739,47.33756821997358,0
18.52130897540185,47.33769169581344,0
18.52153075097512,47.33769153049783,0 " > coordPath.txt
./path.out >> $outfile

echo -e "Poros út, ffff0000, 4
18.48117,47.339751,0
18.482239,47.33909,0
18.48476,47.337824,0
18.495117,47.332707,0" > coordPath.txt
./path.out >> $outfile

echo -e "</Document>\n</kml>" >> $outfile

mv out.kml ../$fldrN/$name.kml
echo ./$fldrN/$name.kml
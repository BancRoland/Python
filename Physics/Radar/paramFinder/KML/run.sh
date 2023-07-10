#!/bin/bash

CFRQ=9.9e9      #centerFrequency[Hz]
SR=100e6        #sample rate [samp/sec]
Rmin=600       #Minimum distance [m]
Rmax=1420       #Maximum distance [m]
# ffti=7          #multiplier of two factor
fftiA=(1 3 5 7)

Fa="47.365187"
Fl="18.428769"

# Fa="47.47046393386676"
# Fl="19.085548731155377"

FAlt=20000   #altitude of the focus [m]
Fdir=0      #firection [deg]
DIR=125.82  #beam direction
BW=20.8  #beamwidth

Rusd=1999.5
CENTRE="$Fa, $Fl"
# CENTRE="47.47046393386676, 19.085548731155377"

gcc -o ring.out ring.c -lm                #CentreAltitude, CentreLongitude, Rmin, Rmax, fillColor, name
gcc -lm -o tags.out tags.c                #CentreAltitude, CentreLongitude, name
gcc -o circ.out circ.c -lm                #CentreAltitude, CentreLongitude, Radius, fillColor, edgeColor, edgeWidth, name
gcc -o path.out path.c -lm                #name, edgeColor, edgeWidth\n longitude, altitude, height
gcc -o slice.out slice.c -lm              #CentreAltitude, CentreLongitude, Radius, theta0, alpha, fillColor, edgeColor, edgeWidth, name
gcc -o ringSlice.out ringSlice.c -lm      #CentreAltitude, CentreLongitude, Rmin, Rmax, theta0, alpha, fillColor, edgeColor, edgeWidth, name


for ffti in "${fftiA[@]}"; do

  outfile=twoFac$ffti.kml

  echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>
  <kml xmlns=\"http://www.opengis.net/kml/2.2\">
  <Document>
  <name>twoFac$ffti</name>

      <LookAt>
        <longitude>$Fl</longitude>
        <latitude>$Fa</latitude>
        <altitude>$FAlt</altitude>
        <heading>$Fdir</heading>        <!-- Direction in degrees (0 = north) -->
        <tilt>0</tilt>              <!-- Tilt angle in degrees (0 = straight down) -->
        <range>0</range>         <!-- Distance from the point of interest -->
        <altitudeMode>relativeToGround</altitudeMode>
      </LookAt>" > $outfile


  # echo -e "$CENTRE, 6649, 9369, 80ffffff, dS=512 lehetséges DZK" > coordRing.txt
  # ./ring.out >> out.kml

  # echo -e "$CENTRE, 3325, 4684, 80ffffff, dS=512 lehetséges DZK" > coordRing.txt
  # ./ring.out >> out.kml

  # echo -e "$CENTRE, 1662, 2342, 80ffffff, dS=512 lehetséges DZK" > coordRing.txt
  # ./ring.out >> out.kml

  # echo -e "$CENTRE, 831, 1171, 80ffffff, dS=512 lehetséges DZK" > coordRing.txt
  # ./ring.out >> out.kml

  # echo -e "$CENTRE, 416, 586, 80ffffff, dS=512 lehetséges DZK" > coordRing.txt
  # ./ring.out >> out.kml

  # echo -e "$CENTRE, 208, 293, 80ffffff, dS=512 lehetséges DZK" > coordRing.txt
  python3 fftRing.py -cFrq $CFRQ -sr $SR -Rmn $Rmin -Rmx $Rmax -Lat $Fl -Lon $Fa -F $ffti > coordRing.txt
  ./ring.out >> $outfile


  python3 fftCirc.py -cFrq $CFRQ -sr $SR -Rmn $Rmin -Rmx $Rmax -Lat $Fl -Lon $Fa -F $ffti > coordCirc.txt

  # echo -e "$CENTRE, 6649, 000000ff, 800000ff, 3, dS=512   Vr=V0/3" > coordCirc.txt
  # ./circ.out >> out.kml
  # echo -e "$CENTRE, 3325, 000000ff, 800000ff, 3, dS=1024  Vr=V0/3" > coordCirc.txt
  # ./circ.out >> out.kml
  # echo -e "$CENTRE, 1662, 000000ff, 800000ff, 3, dS=2048  Vr=V0/3" > coordCirc.txt
  # ./circ.out >> out.kml
  # echo -e "$CENTRE, 831, 000000ff, 800000ff, 3, dS=4096  Vr=V0/3" > coordCirc.txt
  # ./circ.out >> out.kml
  # echo -e "$CENTRE, 416, 000000ff, 800000ff, 3, dS=8192  Vr=V0/3" > coordCirc.txt
  # ./circ.out >> out.kml
  # echo -e "$CENTRE, 208, 000000ff, 800000ff, 3, dS=16384 Vr=V0/3" > coordCirc.txt
  # ./circ.out >> out.kml

  # echo -e "$CENTRE, 8866, 00ff0000, 80000f0F, 3, dS=512   Vr=V0/4" > coordCirc.txt
  # ./circ.out >> out.kml
  # echo -e "$CENTRE, 4433, 00ff0000, 80000f0f, 3, dS=1024  Vr=V0/4" > coordCirc.txt
  # ./circ.out >> out.kml
  # echo -e "$CENTRE, 2216, 00ff0000, 80000f0f, 3, dS=2048  Vr=V0/4" > coordCirc.txt
  # ./circ.out >> out.kml
  # echo -e "$CENTRE, 1108, 00ff0000, 80000f0f, 3, dS=4096  Vr=V0/4" > coordCirc.txt
  # ./circ.out >> out.kml
  # echo -e "$CENTRE, 554, 00ff0000, 80000f0f, 3, dS=8192  Vr=V0/4" > coordCirc.txt
  # ./circ.out >> out.kml
  # echo -e "$CENTRE, 277, 00ff0000, 80000f0f, 3, dS=16384 Vr=V0/4" > coordCirc.txt
  # ./circ.out >> out.kml

  # echo -e "$CENTRE, 9369, 00000000, 80000000, 3, dS=512  Tb=64ms" > coordCirc.txt
  # ./circ.out >> out.kml
  # echo -e "$CENTRE, 4684, 00000000, 80000000, 3, dS=1024 Tb=64ms" > coordCirc.txt
  # ./circ.out >> out.kml
  # echo -e "$CENTRE, 2342, 00000000, 80000000, 3, dS=2048 Tb=64ms" > coordCirc.txt
  # ./circ.out >> out.kml
  # echo -e "$CENTRE, 1171, 00000000, 80000000, 3, dS=4096 Tb=64ms" > coordCirc.txt
  # ./circ.out >> out.kml
  # echo -e "$CENTRE, 586, 00000000, 80000000, 3, dS=8192 Tb=64ms" > coordCirc.txt
  # ./circ.out >> out.kml
  # echo -e "$CENTRE, 293, 00000000, 80000000, 3, dS=16384 Tb=64ms" > coordCirc.txt
  ./circ.out >> $outfile
  # ./circ.out






  # echo -e "$CENTRE, 6000, 000000ff, 800000ff, 3, 6 km" > coordCirc.txt
  # ./circ.out >> out.kml


  # echo -e "$CENTRE, $Rmin, 400000ff, ff000000, 3, Áthallási zóna 0" > coordCirc.txt
  # ./circ.out >> out.kml


  # echo -e "$CENTRE, $Rmin, $DIR, $BW, 400000ff, ff000000, 3, Áthallási nyaláb 0" > coordSlice.txt
  # ./slice.out >> out.kml



  # echo -e "$CENTRE, $Rmin, $Rusd, 4000ff00, Detektálási zóna" > coordRing.txt
  # ./ring.out >> out.kml

  # echo -e "$CENTRE, $Rmin, $Rusd, $DIR, $BW, 4000ff00, Detektálási nyaláb" > coordRingSlice.txt
  # ./ringSlice.out >> out.kml

  # echo -e "$CENTRE, $Rusd, $Rmax, 400000ff, Áthallási zóna 1" > coordRing.txt
  # ./ring.out >> out.kml

  # echo -e "$CENTRE, $Rusd, $Rmax, $DIR, $BW, 400000ff, Áthallási nyaláb 1" > coordRingSlice.txt
  # ./ringSlice.out >> out.kml


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



  # echo -e "</Document>\n</kml>" >> out.kml
  echo -e "</Document>\n</kml>" >> $outfile
done
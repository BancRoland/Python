#!/bin/bash

echo Name,Right Ascension,Declination,Apparent Magnitude,Constellation > constellations_test.csv

cat constellations.csv | grep Sagittarius >> constellations_test.csv
cat constellations.csv | grep Scorpius >> constellations_test.csv
cat constellations.csv | grep Libra >> constellations_test.csv

cat constellations.csv | grep Virgo >> constellations_test.csv
cat constellations.csv | grep Leo >> constellations_test.csv
cat constellations.csv | grep Cancer >> constellations_test.csv

cat constellations.csv | grep Gemini >> constellations_test.csv
cat constellations.csv | grep Taurus >> constellations_test.csv
cat constellations.csv | grep Aries >> constellations_test.csv

cat constellations.csv | grep Pisces >> constellations_test.csv
cat constellations.csv | grep Aquarius >> constellations_test.csv
cat constellations.csv | grep Capricornus >> constellations_test.csv

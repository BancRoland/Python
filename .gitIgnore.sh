#!bin/bash

LIM=1M
echo files larger than $LIM:
find . -size +$LIM

find . -size +$LIM > .gitignore


echo
echo *.png >> .gitignore
echo *.PNG >> .gitignore
echo *.log >> .gitignore
echo *.LOG >> .gitignore
echo *.bin >> .gitignore
echo *.BIN >> .gitignore
echo *.dat >> .gitignore
echo *.DAT >> .gitignore
echo *.out >> .gitignore
echo *.o >> .gitignore
echo *.cf32 >> .gitignore
echo *.wav >> .gitignore


echo .gitignore file:
echo
cat .gitignore

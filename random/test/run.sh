#!/bin/bash

for i in {1..4}
do
time echo $i | python3 run.py
done

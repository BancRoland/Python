#!/bin/bash
cd prev
for i in *.csv
do
    result="${i%.csv}"
    echo $result
done
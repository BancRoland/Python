#!/bin/bash

#!/bin/bash

cd ./log/2023
rm SUM.csv
touch SUM.csv
for f in *.csv; do
    cat "$f" >> SUM.csv
done

cp SUM.csv ../../
python3 ../../csv_read.py
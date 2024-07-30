#!/bin/bash
otp_dir=$(pwd)
log_dir=$otp_dir/log
# log_dir=$otp_dir/log_EUR

rm SUM_FULL.csv
touch SUM_FULL.csv
rm SUM.csv

for year in $(ls $log_dir)
do
    cd $log_dir/$year
    rm SUM.csv
    touch SUM.csv
    for f in *.csv; do
        cat "$f" >> SUM.csv
    done

    cp SUM.csv $otp_dir
    cat SUM.csv >> $otp_dir/SUM_FULL.csv       # hozzáillesztem az összegzéshez

    python3 $otp_dir/csv_read.py
    mv balance.png $otp_dir/balance_$year.png
    mv distribution.png $otp_dir/distribution_$year.png

    cd $otp_dir
done

mv $otp_dir/SUM_FULL.csv $otp_dir/SUM.csv
python3 $otp_dir/csv_read.py
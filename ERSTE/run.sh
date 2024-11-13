#!/bin/bash
otp_dir=$(pwd)
log_dir=$otp_dir/log
# log_dir=$otp_dir/log_EUR

echo "REMOVE LAST STANGE CHARARCTER (seems like empty line) FROM THE END OF FILES!"

rm SUM_FULL.csv
touch SUM_FULL.csv
rm SUM.csv

for year in $(ls $log_dir)
do
    echo processing year $year
    cd $log_dir/$year
    rm SUM.csv
    rm SUM_0.csv
    touch SUM.csv
    for f in "$year"*.csv; do
        # cat "$f" >> SUM.csv
        echo file "$f"

        sed '1s/^\xff\xfe//' $f >> temp.csv
        iconv -f utf-16le -t utf-8 temp.csv -o temp2.csv    #UTF-16 ról UTF-8 ra konvertálunk
        tail -n +2 temp2.csv >> SUM.csv

        rm temp.csv
        rm temp2.csv
        
    done

    cp SUM.csv $otp_dir/SUM.csv
    cat SUM.csv >> $otp_dir/SUM_FULL.csv       # hozzáillesztem az összegzéshez

    python3 $otp_dir/csv_read.py
    mv balance.png $otp_dir/balance_$year.png
    mv distribution.png $otp_dir/distribution_$year.png

    cd $otp_dir
done

mv $otp_dir/SUM_FULL.csv $otp_dir/SUM.csv
python3 $otp_dir/csv_read.py
#!/bin/bash

cd ERSTE
bash run.sh
cp fin_dat.npz ../fin_dat_erste.npz

cd ..
cd OTP
bash run.sh
cp fin_dat.npz ../fin_dat_otp.npz

cd ..
cd OTP_EUR
bash run.sh
cp fin_dat.npz ../fin_dat_otp_eur.npz

cd ..
cd puffer_eur
bash run.sh
cp fin_dat.npz ../fin_dat_puff_eur.npz

cd ..
cd savings
bash run.sh
cp fin_dat.npz ../fin_dat_savings.npz

cd ..
python3 process.py
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

date_format = '%Y%m%d'

date=[]
new_month=[]
new_year=[]

for i_year in range(2000,2030):
    for i_new_year in range(1,13):
        date=datetime.strptime(str(i_year)+str(f"{i_new_year:02d}")+"01",date_format)
        new_month.append(date.timestamp())
        if i_new_year == 1:
            new_year.append(date.timestamp())

data_erste = np.load('fin_dat_erste.npz')
data_otp = np.load('fin_dat_otp.npz')
data_otp_eur = np.load('fin_dat_otp_eur.npz')
data_puff_eur = np.load('fin_dat_puff_eur.npz')

date_erste = data_erste['date'].reshape(-1)
date_otp = data_otp['date'].reshape(-1)
date_otp_eur = data_otp_eur['date'].reshape(-1)
date_puff_eur = data_puff_eur['date'].reshape(-1)


Date0 = np.concatenate((data_erste['date'], data_otp['date'], data_otp_eur['date'], data_puff_eur['date']))
inclomes0 = np.concatenate((400*data_erste['incomes'], data_otp['incomes'], 400*data_otp_eur['incomes'], 400*data_puff_eur['incomes']))

# Date = np.concatenate((date_otp,date_erste,date_otp_eur))

balance0 = np.concatenate((400*data_erste['balance'], data_otp['balance'], 400*data_otp_eur['balance'], 400*data_puff_eur['balance']))



idx = np.argsort(Date0)
Date = Date0[idx]
# balance=balance0[idx]
incomes_sorted=inclomes0[idx]



balance=[1545093]
# balance=[0]

for i_income in incomes_sorted:
    balance.append(balance[-1]+i_income)


balance=balance[1::]



plt.step(data_otp['date'], data_otp['balance'],'o-',where='post')
plt.step(data_otp_eur['date'], 400*data_otp_eur['balance'],'o-',where='post')
plt.step(data_erste['date'], 400*data_erste['balance'],'o-',where='post')
plt.step(data_puff_eur['date'], 400*data_puff_eur['balance'],'o-',where='post')
plt.step(Date, balance,'o-',where='post')

for i_new_month in new_month:
    plt.axvline(i_new_month, color="black", linestyle="--", alpha=0.5, linewidth = 1)
for i_new_year in new_year:
    plt.axvline(i_new_year, color="black", linestyle="--", alpha=1, linewidth = 2)
    date_time = datetime.fromtimestamp(i_new_year)
    date_string = date_time.strftime("%Y")
    # plt.text(i_new_year,max(balance),f"{date_string}", horizontalalignment='left', verticalalignment='top', rotation=90)

# plt.grid()
plt.xlim(1.575e9, 1.74e9)
plt.axhline(0)
plt.show()
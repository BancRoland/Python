import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def getCumbal(date,bal):
    cumbal=[]
    cumdate=[]
    for i in range(len(date)-1):
        if date[i+1] > date[i]:
            cumdate.append(date[i])
            cumbal.append(bal[i])
    return np.array(cumdate), np.array(cumbal)


def are_dates_in_same_month(timestamp1, timestamp2):
    # Convert Unix timestamps to datetime objects with UTC timezone
    date1 = datetime.fromtimestamp(timestamp1)
    date2 = datetime.fromtimestamp(timestamp2)
    out = date1.year == date2.year and date1.month == date2.month
    # Compare the year and month
    return out

def getSpending(Date, incomes_sorted):
    spending = [0]
    outDate = []
    for i in range(len(incomes_sorted)):
        
        if incomes_sorted[i] < 0:
            spending.append(spending[-1] + -1*incomes_sorted[i])
            outDate.append(Date[i])
        if i < len(incomes_sorted)-1:
            if not are_dates_in_same_month(Date[i],Date[i+1]):
                spending.append(0)
                outDate.append(Date[i])
    return np.array(outDate),np.array(spending[1::])

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
data_save = np.load('fin_dat_savings.npz')

date_erste = data_erste['date'].reshape(-1)
date_otp = data_otp['date'].reshape(-1)
date_otp_eur = data_otp_eur['date'].reshape(-1)
date_puff_eur = data_puff_eur['date'].reshape(-1)
date_save = data_save['date'].reshape(-1)

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

cumdate,cumbal=getCumbal(Date,balance)

spendingDate, mondthlySpending = getSpending(Date, incomes_sorted)

plt.step(data_otp['date'], data_otp['balance'],'o-',where='post')
plt.step(data_otp_eur['date'], 400*data_otp_eur['balance'],'o-',where='post')
plt.step(data_erste['date'], 400*data_erste['balance'],'o-',where='post')
plt.step(data_puff_eur['date'], 400*data_puff_eur['balance'],'o-',where='post')
plt.step(Date, balance,'o-',where='post', color="gray", alpha=0.2)
plt.step(cumdate, cumbal,'o-',where='post', color="red", alpha=0.8)

plt.step(spendingDate, mondthlySpending,'o-',where='post')

plt.step(data_save['date'], data_save['balance'],'o-',where='post')

for i_new_month in new_month:
    plt.axvline(i_new_month, color="black", linestyle="--", alpha=0.5, linewidth = 1)
for i_new_year in new_year:
    plt.axvline(i_new_year, color="black", linestyle="--", alpha=1, linewidth = 2)
    date_time = datetime.fromtimestamp(i_new_year)
    date_string = date_time.strftime("%Y")
    # plt.text(i_new_year,max(balance),f"{date_string}", horizontalalignment='left', verticalalignment='top', rotation=90)

for i_million in range(10):
    plt.axhline(i_million*1e6, color="black", linestyle="--", alpha=0.5, linewidth = 1)

# plt.grid()
plt.xlim(1.575e9, 1.74e9)
plt.axhline(0)
plt.show()
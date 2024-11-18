import matplotlib.pyplot as plt
import csv
import numpy as np
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

szamla=[]
T=[]
income=[]
valuta=[]
Date=[]
Date2=[]
D6=[]
D7=[]
D8=[]
D9=[]
D10=[]
D11=[]
D12=[]
D13=[]

with open('SUM.csv', newline='') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:

        szamla.append(row[1])
        T.append(row[2])
        income.append(float(row[8].replace('.', '').replace(',', '.'))) # remove millenial dot, change coma to dot
        valuta.append(row[9])
        # Date.append(row[2])
        date_object = datetime.strptime(row[2],'%d.%m.%Y')
        Date.append(date_object.timestamp())
        # if row[3] != valuta[0]:
        #     print(row[3])
        # if(row[4]==""):
        #     print("row 4 is empty")
        #     Date.append(Date[-1])
        # else:
        #     date_object = datetime.strptime(row[4],date_format)
        #     Date.append(date_object.timestamp())
        # Date2.append(row[5])
        # D6.append(row[6])
        # D7.append(row[7])
        # D8.append(row[8])
        # D9.append(row[9])
        # D10.append(row[10])
        # D11.append(row[11])
        # D12.append(row[12])
        # D13.append(row[13])

idx = np.argsort(Date)
income = np.array(income)
Date = np.array(Date)
valuta = np.array(valuta)
incomes_sorted = income[idx]
date_sorted = Date[idx]
valuta_sorted = valuta[idx]

# np.savez("fin_dat.npz", date=date_sorted, incomes=incomes_sorted, valuta=valuta_sorted)

# if 0:
#     plt.plot(incomes_sorted,'o')
#     plt.grid()
#     plt.title("Transactions")
#     plt.xlabel("transaction index []")
#     plt.ylabel(f"value [{valuta[0]}]")
#     plt.show()
#     plt.savefig




balance=[0]
# balance=[0]

for i_income in incomes_sorted:
    balance.append(balance[-1]+i_income)

# plt.step(date_sorted,balance[1::],'o-',where='post')
# for i_new_month in new_month:
#     plt.axvline(i_new_month, color="black", linestyle="--", alpha=0.5, linewidth = 1)
# for i_new_year in new_year:
#     plt.axvline(i_new_year, color="black", linestyle="--", alpha=1, linewidth = 2)
#     date_time = datetime.fromtimestamp(i_new_year)
#     date_string = date_time.strftime("%Y")
#     plt.text(i_new_year,max(balance),f"{date_string}", horizontalalignment='left', verticalalignment='top', rotation=90)

# plt.xlim(date_sorted[0],date_sorted[-1])
# plt.ylim(bottom=0)
# plt.grid(axis='y')
# plt.title("Balance")
# plt.xlabel("Date [UNIX time]")
# plt.ylabel("value [Ft]")
# plt.savefig("balance.png")
# plt.show()
# # plt.close()




# outV = []
# outD = []

# inV = []
# inD = []

# for i_exp in range(len(incomes_sorted)):
#     if incomes_sorted[i_exp]<0:
#         outV.append(-incomes_sorted[i_exp])
#         outD.append(date_sorted[i_exp])
#     else:
#         inV.append(incomes_sorted[i_exp])
#         inD.append(date_sorted[i_exp])

# if 1:
#     # plt.plot(outV,outV,'.')
#     plt.title("Expense distribution")
#     plt.xlabel("vale [10^x]Ft")
#     plt.ylabel("samples")
#     plt.grid()
#     plt.hist(np.log10(outV), bins=100, edgecolor='black')
#     plt.xlim([1,7])
#     plt.savefig("distribution.png")
#     # plt.show()


# # print(2445601-integ[-1])

# # plt.plot(Date,Value,'o')
# # # plt.plot(Date,np.abs(Value),'o')
# # # plt.yscale("log")
# # plt.grid()
# # plt.show()

np.savez("fin_dat.npz", balance=balance[1::], date=date_sorted, incomes=incomes_sorted, valuta=valuta_sorted)
import matplotlib.pyplot as plt
import csv
import numpy as np
from datetime import datetime

date_format = '%Y%m%d'

line=[]
lineU=[]
lineU2=[]

for i_year in range(2000,2030):
    for i_month in range(1,13):
        line=datetime.strptime(str(i_year)+str(f"{i_month:02d}")+"01",date_format)
        lineU.append(line.timestamp())
        if i_month == 1:
            lineU2.append(line.timestamp())
        print(lineU[-1])
        # line.append(datetime.strptime(str(20230101+100*i),date_format).timestamp)
    # line="20230201"
    # lineU=datetime.strptime(line,date_format)
    print(line)

szamla=[]
T=[]
Value=[]
Devi=[]
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
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        szamla.append(row[0])
        T.append(row[1])
        Value.append(eval(row[2]))
        Devi.append(row[3])
        # print(row[4])
        if(row[4]==""):
            print("WOW")
            Date.append(Date[-1])
        else:
            date_object = datetime.strptime(row[4],date_format)
            Date.append(date_object.timestamp())
        Date2.append(row[5])
        D6.append(row[6])
        D7.append(row[7])
        D8.append(row[8])
        D9.append(row[9])
        D10.append(row[10])
        D11.append(row[11])
        D12.append(row[12])
        D13.append(row[13])

idx=np.argsort(Date)
Value=np.array(Value)
Date=np.array(Date)
ValueS=Value[idx]
DateS=Date[idx]


plt.plot(ValueS,'o')
plt.grid()
plt.title("Transactions")
plt.xlabel("transaction index []")
plt.ylabel("value [Ft]")
plt.show()
plt.savefig




integ=[2128151]
for i_month in ValueS:
    integ.append(integ[-1]+i_month)

plt.step(DateS,integ[1::],'o-',where='post')
for i_month in lineU:
    plt.axvline(i_month, color="black", linestyle="--", alpha=0.5, linewidth = 1)
for i_month in lineU2:
    plt.axvline(i_month, color="black", linestyle="--", alpha=1, linewidth = 2)
plt.xlim(DateS[0],DateS[-1])
plt.grid(axis='y')
plt.title("Balance")
plt.xlabel("Date [UNIX time]")
plt.ylabel("value [Ft]")
plt.show()






outV=[]
outD=[]

inV=[]
inD=[]

for i_month in range(len(ValueS)):
    # print(ValueS[i])
    if ValueS[i_month]<0:
        outV.append(-ValueS[i_month])
        outD.append(DateS[i_month])
    else:
        inV.append(ValueS[i_month])
        inD.append(DateS[i_month])

# plt.plot(outV,outV,'.')
plt.title("Expense distribution")
plt.xlabel("vale [10^x]Ft")
plt.ylabel("samples")
plt.grid()
plt.hist(np.log10(outV), bins=100, edgecolor='black')
plt.show()

# print(2445601-integ[-1])

# plt.plot(Date,Value,'o')
# # plt.plot(Date,np.abs(Value),'o')
# # plt.yscale("log")
# plt.grid()
# plt.show()
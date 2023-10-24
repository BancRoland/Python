import matplotlib.pyplot as plt
import csv
import numpy as np
from datetime import datetime, timedelta

def conToTime(time_str):
    # Input string
    # time_str = "+ 10:05"

    # Split the string into its components
    if time_str == "":
        return "---"
    else:
        sign, time_offset = time_str.split()
        minutes, seconds = map(int, time_offset.split(':'))

        # Create a timedelta object based on the sign and offset
        if sign == "+":
            time_delta = minutes*60+seconds #timedelta(minutes=minutes, seconds=seconds)
        else:
            time_delta = -1*(minutes*60+seconds)#timedelta(minutes=minutes, seconds=seconds)

        # print(time_delta)

        return time_delta

def getEOT_csv():
    TABLE=[]

    with open('eot.txt', newline='') as f:
        reader = csv.reader(f, delimiter='	')
        for row in reader:
            TABLE.append(row)

    nR,nC=np.shape(TABLE)
    # print(nR)
    # print(nC)
    EOT=[]
    for c in range(nC-1):
        # print(TABLE[0][c])
        for r in range(nR-1):
            # print(f"{nR*c+r}    {TABLE[r+1][c+1]}   {conToTime(TABLE[r+1][c+1])}")
            if TABLE[r+1][c+1] != "":
                EOT.append(conToTime(TABLE[r+1][c+1]))

    # for i in range(len(EOT)):
    #     print(f"{i} {EOT[i]}")

    # plt.plot(EOT,'.-')
    # plt.show()
    return EOT

# print(TABLE[0][1])
# TABLE=np.array(TABLE)
# print(TABLE)

        # cAzmt.append(eval(row[0]))
        # cElev.append(eval(row[1]))


# cAzmt=cAzmt+90*np.ones(len(cAzmt))

# plt.plot(cAzmt,cElev,'.:')

# plt.legend(["Égiegyenlítő","Nap","műholdak"])

# plt.title(f"2023.03.02.\nműholdkeresés parabolával")
# plt.xlabel("azimut [°]")
# plt.ylabel("eleváció [°]")

# plt.grid()
# plt.savefig('data.png', dpi=300, bbox_inches='tight')
# plt.show()

import matplotlib.pyplot as plt
import csv
import numpy as np

cAzmt=[]
cElev=[]

lAzmt=[]
lElev=[]

sAzmt=[]
sElev=[]

with open('celEq.csv', newline='') as f:
    reader = csv.reader(f, delimiter='	')
    for row in reader:
        cAzmt.append(eval(row[0]))
        cElev.append(eval(row[1]))

cAzmt=cAzmt+90*np.ones(len(cAzmt))

plt.plot(cAzmt,cElev,'.:')

plt.legend(["Égiegyenlítő","Nap","műholdak"])

plt.title(f"2023.03.02.\nműholdkeresés parabolával")
plt.xlabel("azimut [°]")
plt.ylabel("eleváció [°]")

plt.grid()
plt.savefig('data.png', dpi=300, bbox_inches='tight')
plt.show()

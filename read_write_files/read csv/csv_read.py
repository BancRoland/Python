import matplotlib.pyplot as plt
import csv


with open('in.csv', newline='') as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        for d in range(len(row)):
            res = [eval(i) for i in row]

print(res)

plt.plot(res,'.-')
plt.title("Beolvasott értékek")
plt.grid()
plt.savefig('data.png', dpi=300, bbox_inches='tight')
plt.show()

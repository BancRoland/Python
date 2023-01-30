import matplotlib.pyplot as plt

import csv
with open('in.csv', newline='') as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:

        print(len(row))
        
        for d in range(len(row)):
            # print(d)
            print([ord(c) for c in row[d]])
        # print(int(row))
        # res = [eval(i) for i in row]
        # print("Modified list is: ", res)

# plt.plot(res)
# plt.show()

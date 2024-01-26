import matplotlib.pyplot as plt

import csv

with open('in.csv', newline='') as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:

        #print(len(row))
        
        for d in range(len(row)):
            a=([f'{ord(c):08b}' for c in row[d]])
            #print(a)

    b=''.join(a)
    #print(b)

    for i in range(int(len(b)/4)):
        c=(b[4*i:4*i+4])
        #print(c)
        print(int(c,2))

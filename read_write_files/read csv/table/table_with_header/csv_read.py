import matplotlib.pyplot as plt
import csv


sr=['samprate [MS/s]']
Ncode=['Codes']
Nzeros=['Zeros']
dSamp=['DoppSamp']

with open('input.csv', newline='') as f:
    reader = csv.reader(f, delimiter='\t')
    sr=next(reader)
    Ncode=next(reader)
    Nzeros=next(reader)
    dSamp=next(reader)

for i in range(len(sr)-1):
    sr[i+1]=eval(sr[i+1])
    Ncode[i+1]=eval(Ncode[i+1])
    Nzeros[i+1]=eval(Nzeros[i+1])
    dSamp[i+1]=eval(dSamp[i+1])
        

print(sr)
print(Ncode)
print(Nzeros)
print(dSamp)

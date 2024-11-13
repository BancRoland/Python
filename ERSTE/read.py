import numpy as np

data = np.load('fin_dat.npz')
print(data['erste_date'])
print(data['erste_incomes'])
print(data['erste_valuta'])
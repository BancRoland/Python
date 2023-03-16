import numpy as np
import matplotlib.pyplot as plt

# data = np.genfromtxt(fname="data.txt", delimiter="\t", skip_header=1, filling_values='NaN')
data1 = np.genfromtxt(fname="data1.txt", delimiter="\t", skip_header=1, filling_values='NaN')
data2 = np.genfromtxt(fname="data2.txt", delimiter="\t", skip_header=1, filling_values='NaN')

Cdata1=data1[:,0]+1j*data1[:,1]
Cdata2=data2[:,0]+1j*data2[:,1]

print(Cdata1)
print(Cdata2)

# plt.figure()
# plt.plot(np.real(Cdata1),'.-')
# plt.plot(np.imag(Cdata1),'.-')
# plt.grid()
# plt.show()

# plt.figure()
# plt.plot(np.real(Cdata2),'.-')
# plt.plot(np.imag(Cdata2),'.-')
# plt.grid()
# plt.show()

plt.figure()
plt.plot(np.abs(np.correlate(Cdata1,Cdata1,'full')),'.-')
plt.plot(np.abs(np.correlate(Cdata1,Cdata1,'full')))
plt.show()
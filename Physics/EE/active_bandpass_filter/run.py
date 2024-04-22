import matplotlib.pyplot as plt
import numpy as np

def replus(R1,R2):
    return (R1*R2)/(R1+R2)

def replus2(v):
    return np.multiply(v)/np.sum(v)


R1_0  =   10e+03
R2_0  =   100
R3_0  =   10e+03
C_0  =   1.00e-07

f0_0  =   1/(2*np.pi*np.sqrt(replus(R1_0,R2_0)*R3_0)*C_0)
H0_0  =   R3_0/(2*R1_0)
B_0   =   1/(np.pi*R3_0*C_0)
Q_0   =   f0_0/B_0

print(f"f0  =   {f0_0}")
print(f"H0  =   {H0_0}")
print(f"B  =   {B_0}")
print(f"Q  =   {Q_0}")

A=[]
f=[]
for f0_1 in (np.arange(10,100000)):
    w       =   2*np.pi*f0_1
    Z     =   1/(1j*w*C_0)
    A_0       =   R3_0/(R1_0*(1+(R3_0+Z)/Z+Z/R2_0)-Z)
    A.append(A_0)
    f.append(f0_1)
plt.plot(f,20*np.log10(np.abs(A)))
plt.xscale('log')
plt.axvline(f0_0,color="gray",alpha=0.5,linestyle="--")
plt.axhline(20*np.log10(H0_0),color="gray",alpha=0.5,linestyle="--")
plt.axhline(20*np.log10(H0_0)-3,color="gray",alpha=0.5,linestyle="--")
plt.grid()
plt.show()

#-----------------

C   =   0.1e-6
f0  =   5058.023217591067
H0  =   5.0
B  =   318.3098861837907
Q   =   f0/B

R3  =   Q/(np.pi*f0*C)
R1  =   R3/(2*H0)
R2  =   R3/(4*Q**2-2*H0)


print("Calculated parameters for measurement")
print(f"R1_0  =   {R1:.2e}")
print(f"R2_0  =   {R2:.2e}")
print(f"R3_0  =   {R3:.2e}")
print(f"C_0  =   {C:.2e}")


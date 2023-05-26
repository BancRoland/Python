import numpy as np
import matplotlib.pyplot as plt


G=7
R=np.arange(0,15,0.1)
v00=np.arange(0,10,0.1)


Arr=np.empty((0, 150), int)

r0=10
R0=np.sqrt(G**2/v00**4*((v00**2*r0/G+1)**2-1))

plt.figure()
plt.plot(v00,R0)
plt.grid()
plt.show()


plt.figure()
for v0 in v00:
    r=G/v0**2*(np.sqrt(1+v0**4*R**2/G**2)-1)
    v1=v0*R/r
    alpha=np.arccos(1/np.sqrt(1+v0**4*R**2/G**2))
    Arr=np.vstack((Arr,alpha))
    plt.plot(R,2*alpha,'.-')
plt.show()

plt.imshow(Arr)
plt.plot(v00,R0)
plt.show()


# alpha0=47.3
# alpha=alpha0/180*np.pi
# R=6371
# d=42000

# c=np.sqrt(R**2+d**2-2*R*d*np.cos(alpha))   #koszinusztétel
# s=180-np.arcsin(np.sin(alpha)*d/c)/np.pi*180-90

# print(c)
# print(s)
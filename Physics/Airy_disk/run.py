import matplotlib.pyplot as plt
import numpy as np
import math as m


def spirSum(c0):
    c1=np.zeros(len(c0)+1)+np.zeros(len(c0)+1)*1j
    c1[0]=0
    for i in range(len(c0)):
        c1[i+1]=c1[i]+c0[i]/n
    return c1



D=0.3         #[m] távcső átmérője
lmbda=380e-9    #[m] hullámhossz
f=2.5           #[m] fókusztáv
alpha=D/2/f *180/m.pi /1000     #[rad] max látómező az apertúra és a fókusztáv összefüggéséven

n=100
d=np.arange(0,D,D/n)

# print(C)

# for i in range(-80,80):
#     C=np.exp(1j*2*m.pi/lmbda*d*np.sin(0.5*i*1e-7))
#     C2=spirSum(C)
#     plt.plot(np.real(C2), np.imag(C2),'.-', color=(0.2, 0.4, 0.6))
#     plt.plot(np.real(C2[-1]), np.imag(C2[-1]),'o', color=(0., 0., 0.))
N=80
for i in range(-N,N):
    C=np.exp(1j*2*m.pi/lmbda*d*np.sin(0.5*i*1e-7))
    C2=spirSum(C)
    plt.plot(np.real(C2[-1]), np.imag(C2[-1]),'.', color=(0., 0., 0.))
# C2=np.zeros(len(C)+1)+np.zeros(len(C)+1)*1j
# C2[0]=0
# for i in range(len(C)):
#     C2[i+1]=C2[i]+C[i]/n

# print(C2)

plt.plot(np.real(C), np.imag(C),'.')

plt.grid()
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')
plt.xlim([-1.5, 1.5])
plt.ylim([-1.5, 1.5])

plt.show()

# x=np.arange(-alpha,alpha,alpha/100)

# beta=D/lmbda*np.sin(x*m.pi/180)

# I=D*np.sin(beta/2)/(beta/2)*np.cos(x)

# plt.plot(x,I)
# plt.xlabel("szögérték [fok]")
# plt.show()
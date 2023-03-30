# uStrip vonal hullámimpedanciáját számítja ki adott paraméterek alapján

import numpy as np
import matplotlib.pyplot as plt

def imped(W,eps,H=2.1e-3,T=0):
    Z=87/np.sqrt(eps+1.41)*np.log(5.98*H/(0.8*W+T))
    return Z


H=2.1e-3
W_R=np.arange(1.5,5,0.1)*1e-3
eps0=3.8
eps_R=np.arange(3.8,4.8,0.2)

# Z0=87/np.sqrt(eps+1.41)*np.log(5.98*H/(0.8*W+T))

for i in eps_R:
    plt.plot(W_R*1e3, imped(W=W_R,eps=i),'.-',label=f'eps={i:.2}')

plt.title(r'$\mu$-strip impedance values')
plt.xlabel("strip width [mm]")
plt.ylabel("impedance [Ohm]")
plt.axhline(75, color='grey')
plt.axhline(50, color='grey')
plt.axhline(np.sqrt(50*75), color='grey')
plt.grid()
plt.legend()
plt.savefig('fig.png')
plt.show()